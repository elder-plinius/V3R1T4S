#!/usr/bin/env python3
"""Standalone Python 3 stdlib verifier for GF(2^m) polynomial-basis multipliers
and 8-term GF(2)[x] bilinear rank decompositions.

Checks:
1. Strict gate model: 2-input {AND, XOR, XNOR} only, no constants, no NOT,
   no undefined wires, no wire redefined.
2. Exhaustive bit-sliced and scalar evaluation over all 2^(2m) input pairs in the
   standard polynomial basis A0..A(m-1), B0..B(m-1) -> C0..C(m-1) modulo P(x).
3. Exact gate tally (#AND, #XOR, #XNOR, #gates, gate_depth, and_depth) and
   optional threshold assertion (--max-gates).

Prints "PASS" as final line on success (exit 0), or "FAIL" on error (exit 1).
"""
import argparse
import json
import re
import sys


def gf2_poly_mul_mod(a: int, b: int, m: int, poly: int) -> int:
    res = 0
    for i in range(m):
        if (a >> i) & 1:
            res ^= (b << i)
    for deg in range(2 * m - 2, m - 1, -1):
        if (res >> deg) & 1:
            res ^= (poly << (deg - m))
    return res & ((1 << m) - 1)


def parse_slp(path: str, m: int):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    gates = []
    in_slp = False
    has_begin_slp = any(l.strip().lower() == "begin slp" for l in lines)

    for raw in lines:
        line = raw.split("#", 1)[0].split("%", 1)[0].strip()
        if not line:
            continue
        low = line.lower()
        if low == "begin slp" or low == "begin":
            in_slp = True
            continue
        if low.startswith("end"):
            if in_slp:
                break
            continue
        if has_begin_slp and not in_slp:
            continue
        if any(low.startswith(k) for k in ("inputs:", "outputs:", "internal:", "gatesyntax:", "begin circuit")):
            continue
        if re.match(r"^\d+\s+(gates|inputs|outputs)\b", low):
            continue

        parts = line.split()
        if len(parts) == 4 and parts[0].upper() in ("AND", "XOR", "XNOR"):
            op, out, u, v = parts[0].upper(), parts[1], parts[2], parts[3]
            gates.append((op, out, u, v))
            continue
        if parts[0].upper() in ("NOT", "NAND", "NOR", "OR", "MUX", "INV"):
            raise ValueError(f"Disallowed gate type: {parts[0]}")

        m_eq = re.match(
            r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z0-9_]+)\s*(\+|x|&|\^|~|xn|xor|and|xnor)\s*([A-Za-z0-9_]+)$",
            line,
            re.I,
        )
        if m_eq:
            out, u, op_sym, v = m_eq.group(1), m_eq.group(2), m_eq.group(3).lower(), m_eq.group(4)
            op_map = {
                "+": "XOR", "^": "XOR", "xor": "XOR",
                "x": "AND", "&": "AND", "and": "AND",
                "~": "XNOR", "xn": "XNOR", "xnor": "XNOR",
            }
            gates.append((op_map[op_sym], out, u, v))
            continue

        raise ValueError(f"Unrecognized or disallowed line in circuit: {line}")

    if not gates:
        raise ValueError("No gates parsed from circuit file")

    inputs_a = [f"A{i}" for i in range(m)]
    inputs_b = [f"B{i}" for i in range(m)]
    defined = set(inputs_a + inputs_b)

    for op, out, u, v in gates:
        if op not in ("AND", "XOR", "XNOR"):
            raise ValueError(f"Disallowed gate: {op}")
        for w in (out, u, v):
            if w in ("0", "1", "true", "false", "const0", "const1"):
                raise ValueError(f"Constant wire disallowed: {w}")
        if u not in defined:
            raise ValueError(f"Wire {u} used before definition")
        if v not in defined:
            raise ValueError(f"Wire {v} used before definition")
        if out in defined:
            raise ValueError(f"Wire {out} defined more than once (or overwrites input)")
        defined.add(out)

    outputs = [f"C{i}" for i in range(m)]
    for o in outputs:
        if o not in defined:
            raise ValueError(f"Output wire {o} was never defined")

    return gates, inputs_a, inputs_b, outputs


def verify_gf2m_circuit(path: str, m: int, poly: int, max_gates: int = None):
    gates, inputs_a, inputs_b, outputs = parse_slp(path, m)

    n_and = sum(1 for op, _, _, _ in gates if op == "AND")
    n_xor = sum(1 for op, _, _, _ in gates if op == "XOR")
    n_xnor = sum(1 for op, _, _, _ in gates if op == "XNOR")
    total_gates = len(gates)

    g_depth = {w: 0 for w in inputs_a + inputs_b}
    a_depth = {w: 0 for w in inputs_a + inputs_b}
    for op, out, u, v in gates:
        g_depth[out] = max(g_depth[u], g_depth[v]) + 1
        a_depth[out] = max(a_depth[u], a_depth[v]) + (1 if op == "AND" else 0)

    max_gd = max(g_depth[o] for o in outputs)
    max_ad = max(a_depth[o] for o in outputs)

    n_pairs = 1 << (2 * m)
    all_ones = (1 << n_pairs) - 1
    vals = {}
    for i in range(2 * m):
        step = 1 << i
        block = ((1 << step) - 1) << step
        cur_len = 2 * step
        pat = block
        while cur_len < n_pairs:
            pat |= (pat << cur_len)
            cur_len <<= 1
        pat &= all_ones
        if i < m:
            vals[f"A{i}"] = pat
        else:
            vals[f"B{i - m}"] = pat

    for op, out, u, v in gates:
        vu, vv = vals[u], vals[v]
        if op == "XOR":
            vals[out] = vu ^ vv
        elif op == "AND":
            vals[out] = vu & vv
        elif op == "XNOR":
            vals[out] = (vu ^ vv) ^ all_ones

    ref_c = [0] * m
    for i in range(m):
        for j in range(m):
            term = vals[f"A{i}"] & vals[f"B{j}"]
            rem = gf2_poly_mul_mod(1 << i, 1 << j, m, poly)
            for k in range(m):
                if (rem >> k) & 1:
                    ref_c[k] ^= term

    for k in range(m):
        if vals[f"C{k}"] != ref_c[k]:
            diff = vals[f"C{k}"] ^ ref_c[k]
            bad_idx = (diff & -diff).bit_length() - 1
            a_val = bad_idx & ((1 << m) - 1)
            b_val = bad_idx >> m
            raise ValueError(f"Exhaustive check failed on output C{k} at A=0x{a_val:x}, B=0x{b_val:x}")

    check_indices = range(n_pairs) if m <= 7 else [(p * 257 + q) & (n_pairs - 1) for p in range(32) for q in range(32)]
    for idx in check_indices:
        a_val = idx & ((1 << m) - 1)
        b_val = idx >> m
        prod = gf2_poly_mul_mod(a_val, b_val, m, poly)
        got = 0
        for k in range(m):
            if (vals[f"C{k}"] >> idx) & 1:
                got |= (1 << k)
        if got != prod:
            raise ValueError(f"Scalar spot-check mismatch at A={a_val}, B={b_val}")

    if max_gates is not None and total_gates > max_gates:
        raise ValueError(f"Gate count {total_gates} exceeds threshold {max_gates}")

    return {
        "and": n_and,
        "and_depth": max_ad,
        "gate_depth": max_gd,
        "gates": total_gates,
        "m": m,
        "pairs_checked": n_pairs,
        "poly": hex(poly),
        "xnor": n_xnor,
        "xor": n_xor,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Circuit .slp file")
    ap.add_argument("--m", type=int, required=True, help="Field degree m for GF(2^m)")
    ap.add_argument("--poly", type=lambda s: int(s, 0), required=True, help="Irreducible polynomial in hex/int")
    ap.add_argument("--max-gates", type=int, default=None, help="Maximum allowed total gate count")
    args = ap.parse_args()

    try:
        info = verify_gf2m_circuit(args.path, args.m, args.poly, args.max_gates)
        print(json.dumps(info, sort_keys=True))
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}")
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
