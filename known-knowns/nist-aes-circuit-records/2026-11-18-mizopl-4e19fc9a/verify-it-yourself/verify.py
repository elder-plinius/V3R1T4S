#!/usr/bin/env python3
"""
Standalone Zero-Dependency Verifier for `nist-aes-circuit-records` (Milestones `p3` & `p4` + 4D Pareto Frontier + `T1..T6`).

Uses ONLY the Python 3 standard library (`< 0.3s` runtime, 100% offline) to verify from scratch:
  1. Strict `%NCFF-0.1-2026` parsing and gate-model enforcement across all `13` constructed circuits:
       - `2` `InvMixColumns` `92@10` circuits (`Inputs: x0:x31 -> Outputs: y0:y31`, strictly 2-input `{XOR}` ONLY,
         `0` `AND`, `0` `XNOR`, `0` `NOT`, `0` constants, `0` self-inputs, `0` dead gates).
       - `10` `InvS-box` circuits (`Inputs: x0:x7 -> Outputs: y0:y7`, strictly 2-input `{AND, XOR, XNOR}`,
         `0` `NOT`, `0` constants, `0` self-inputs, `0` dead gates), including `152@10`, `155@10`, `33/4/111/14`,
         `34/4/111/14`, `109@15`, `129@13`, `116@16`, `114@19`, `143@16`, and `134@19`.
       - `1` forward `S-box` circuit (`aes-sbox-a37-ad4-g119-gd14-xx82-33.circ.txt`, `Inputs: U0:U7 -> Outputs: S0:S7`,
         strictly 2-input `{AND, XOR, XNOR}`, `0` `NOT`, `0` constants, `0` self-inputs, `0` dead gates).
  2. Exact FIPS 197 functional evaluation derived algebraically from `GF(2)[x]/(x^8 + x^4 + x^3 + x + 1)` (`0x11B`)
     with zero lookup tables:
       - `32 x 32` `GF(2)` linear basis evaluation against `a^{-1}(X) = 0x0E + 0x09*X + 0x0D*X^2 + 0x0B*X^3 mod (X^4 + 1)`
         on both `92@10` `InvMixColumns` circuits, plus verification of their `72 / 92` value-set overlap (`symdiff = 40`).
       - Exhaustive `256`-byte evaluation against FIPS 197 `SBox()` / `InvSBox()` on all `11` `[Inv]S-box` circuits.
  3. Digit-for-digit metric, level-histogram, and SHA-256 parity against `00_nist_aes_gd10_and_barriers_certificate.json` and `SHA256SUMS`.
  4. Pure-Python `< 0.1s` algebraic tightness & obstruction verifiers (`T1..T4`, `D<=2` `[8,92,4358]`, `gf16_basis_hex`,
     `T5a` `111@14` `P=16` `[6,45,643,33602]` middle reachability Pigeonhole, and `T6` `0 / 2,040` Frobenius-scaling
     conjugate `Zone_Top` screen on `111@14` and `109@15`).
  5. Live parser negative self-tests (`NOT`, `XNOR` in `invmixcols`, constants, `u == v`) + `--corrupt` (`FAIL`, `rc = 1`).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

PINNED_STATIC_BARRIERS_SHA256 = "91c14f7a7b9e1ed3c60c7577101a495a65c8c6d96f526ca6ba8825e28490d0e1"
SBOX_ALLOWED_OPS = {"AND", "XOR", "XNOR"}
LINEAR_ALLOWED_OPS = {"XOR"}
CONSTANT_TOKENS = {"0", "1", "true", "false", "const0", "const1", "zero", "one"}
MASK_256 = (1 << 256) - 1


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical_json_sha256(obj: object) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# 1. Algebraic Derivation of FIPS 197 SBox(), InvSBox(), and InvMixColumns()
#    over GF(2^8) = GF(2)[x]/(x^8 + x^4 + x^3 + x + 1) (0x11B)
# ---------------------------------------------------------------------------

def gf256_mul(a: int, b: int) -> int:
    acc = 0
    for _ in range(8):
        if b & 1:
            acc ^= a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a ^= 0x1B
        b >>= 1
    return acc


def gf256_pow(a: int, exp: int) -> int:
    res = 1
    base = a
    while exp > 0:
        if exp & 1:
            res = gf256_mul(res, base)
        base = gf256_mul(base, base)
        exp >>= 1
    return res


def fips197_affine(byte_val: int) -> int:
    out = 0
    for i in range(8):
        bit = (
            ((byte_val >> i) & 1)
            ^ ((byte_val >> ((i + 4) & 7)) & 1)
            ^ ((byte_val >> ((i + 5) & 7)) & 1)
            ^ ((byte_val >> ((i + 6) & 7)) & 1)
            ^ ((byte_val >> ((i + 7) & 7)) & 1)
            ^ ((0x63 >> i) & 1)
        )
        out |= bit << i
    return out


def derive_fips197_oracles() -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    sbox = [0] * 256
    invsbox = [0] * 256
    seen_outputs: set[int] = set()
    for x in range(256):
        inv = 0 if x == 0 else gf256_pow(x, 254)
        if x != 0 and gf256_mul(x, inv) != 1:
            raise ValueError(f"GF(2^8) inversion check failed at x={x}")
        y = fips197_affine(inv)
        sbox[x] = y
        invsbox[y] = x
        seen_outputs.add(y)
    if len(seen_outputs) != 256:
        raise ValueError("Derived FIPS 197 S-box is not a bijection on 0..255")

    in_tt = [0] * 8
    s_tt = [0] * 8
    invs_tt = [0] * 8
    for val in range(256):
        sv = sbox[val]
        iv = invsbox[val]
        for k in range(8):
            bit_pos = 7 - k  # U0/x0/S0/y0 = MSB (bit 7), U7/x7/S7/y7 = LSB (bit 0)
            if (val >> bit_pos) & 1:
                in_tt[k] |= 1 << val
            if (sv >> bit_pos) & 1:
                s_tt[k] |= 1 << val
            if (iv >> bit_pos) & 1:
                invs_tt[k] |= 1 << val

    # Derive FIPS 197 MixColumns and InvMixColumns 32x32 matrices over GF(2)
    # Convention: wire x_(8*b + r) is bit r (r=0 LSB .. r=7 MSB) of byte b (b=0..3),
    # verified by M * M^-1 == I_32 over GF(2).
    fwd_circ = [[0x02, 0x03, 0x01, 0x01], [0x01, 0x02, 0x03, 0x01], [0x01, 0x01, 0x02, 0x03], [0x03, 0x01, 0x01, 0x02]]
    inv_circ = [[0x0E, 0x0B, 0x0D, 0x09], [0x09, 0x0E, 0x0B, 0x0D], [0x0D, 0x09, 0x0E, 0x0B], [0x0B, 0x0D, 0x09, 0x0E]]

    def build_32bit_masks(mat4: list[list[int]]) -> list[int]:
        rows = [0] * 32
        for in_b in range(4):
            for in_r in range(8):
                in_w = 8 * in_b + in_r
                in_bytes = [0, 0, 0, 0]
                in_bytes[in_b] = 1 << in_r
                for out_b in range(4):
                    acc = 0
                    for k in range(4):
                        acc ^= gf256_mul(mat4[out_b][k], in_bytes[k])
                    for out_r in range(8):
                        if (acc >> out_r) & 1:
                            rows[8 * out_b + out_r] |= 1 << in_w
        return rows

    mc_rows = build_32bit_masks(fwd_circ)
    imc_rows = build_32bit_masks(inv_circ)
    # Verify M * M^-1 == I_32 over GF(2)
    for i in range(32):
        prod_row = 0
        ri = mc_rows[i]
        for k in range(32):
            if (ri >> k) & 1:
                prod_row ^= imc_rows[k]
        if prod_row != (1 << i):
            raise ValueError("Derived MixColumns * InvMixColumns != I_32")

    return tuple(in_tt), tuple(s_tt), tuple(invs_tt), tuple(imc_rows)


# ---------------------------------------------------------------------------
# 2. Strict Zero-NOT, Zero-Constant, No-Self-Input NCFF Parser & Evaluators
# ---------------------------------------------------------------------------

def _expand_range(spec: str) -> list[str]:
    out: list[str] = []
    for tok in re.split(r"[\s,]+", spec.strip()):
        if not tok:
            continue
        m = re.match(r"^([A-Za-z_]+)(\d+):([A-Za-z_]*)(\d+)$", tok)
        if m:
            p1, s_i, p2, e_i = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
            if p2 and p2 != p1:
                raise ValueError(f"Mismatched wire range prefix in '{tok}'")
            step = 1 if e_i >= s_i else -1
            for k in range(s_i, e_i + step, step):
                out.append(f"{p1}{k}")
        else:
            out.append(tok)
    return out


def parse_strict_ncff(
    text: str,
    label: str,
    pure_xor_only: bool = False,
) -> tuple[list[str], list[str], list[str], list[tuple[str, str, str, str]], dict[str, int]]:
    if not text.strip():
        raise ValueError(f"{label}: empty circuit file")
    inputs: list[str] = []
    outputs: list[str] = []
    internals: list[str] = []
    gates: list[tuple[str, str, str, str]] = []
    header_meta: dict[str, int] = {}

    m_tally_sbox = re.search(
        r"%\s*Tally of gates\s*\((\d+)\):\s*(\d+)\s*AND;\s*(\d+)\s*XOR;\s*(\d+)\s*XNOR",
        text,
    )
    m_tally_xor = re.search(r"%\s*Tally of gates\s*\((\d+)\):\s*(\d+)\s*XOR\s*$", text, re.M)
    if m_tally_sbox:
        header_meta["G"] = int(m_tally_sbox.group(1))
        header_meta["A"] = int(m_tally_sbox.group(2))
        header_meta["XOR"] = int(m_tally_sbox.group(3))
        header_meta["XNOR"] = int(m_tally_sbox.group(4))
    elif m_tally_xor:
        header_meta["G"] = int(m_tally_xor.group(1))
        header_meta["A"] = 0
        header_meta["XOR"] = int(m_tally_xor.group(2))
        header_meta["XNOR"] = 0

    m_dep_both = re.search(r"%\s*Gate depth\s*(\d+);\s*AND depth\s*(\d+)", text)
    m_dep_gd = re.search(r"%\s*Gate depth\s*(\d+)\s*$", text, re.M)
    if m_dep_both:
        header_meta["GD"] = int(m_dep_both.group(1))
        header_meta["AD"] = int(m_dep_both.group(2))
    elif m_dep_gd:
        header_meta["GD"] = int(m_dep_gd.group(1))
        header_meta["AD"] = 0

    allowed = LINEAR_ALLOWED_OPS if pure_xor_only else SBOX_ALLOWED_OPS
    in_slp = False
    saw_begin_slp = False
    saw_end_slp = False

    for line_no, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.split("%", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        low = line.lower()
        if low == "begin slp":
            in_slp = True
            saw_begin_slp = True
            continue
        if low == "end slp":
            in_slp = False
            saw_end_slp = True
            continue
        if low.startswith("begin circuit") or low == "end circuit" or low.startswith("gatesyntax:"):
            continue
        if low.startswith("inputs:"):
            inputs = _expand_range(line.split(":", 1)[1])
            continue
        if low.startswith("outputs:"):
            outputs = _expand_range(line.split(":", 1)[1])
            continue
        if low.startswith("internal:"):
            internals = _expand_range(line.split(":", 1)[1])
            continue
        if not in_slp:
            raise ValueError(f"{label}:{line_no}: unexpected directive outside SLP block: '{line}'")

        toks = line.split()
        if not toks:
            continue
        op = toks[0].upper()
        if op in ("NOT", "INV") or op not in allowed:
            allowed_str = "{XOR}" if pure_xor_only else "{AND, XOR, XNOR}"
            raise ValueError(f"{label}:{line_no}: forbidden gate type '{op}' (strictly {allowed_str} allowed)")
        if len(toks) != 4:
            raise ValueError(f"{label}:{line_no}: gate '{line}' must have 1 output and 2 inputs (got {len(toks) - 1} tokens)")
        _, out_w, in1, in2 = toks
        gates.append((op, out_w, in1, in2))

    if not (saw_begin_slp and saw_end_slp):
        raise ValueError(f"{label}: missing 'begin SLP' / 'end SLP' block")
    return inputs, outputs, internals, gates, header_meta


def _check_dag_live_and_headers(
    outputs: list[str],
    internals: list[str],
    gates: list[tuple[str, str, str, str]],
    defined_gd: dict[str, int],
    defined_ad: dict[str, int],
    header_meta: dict[str, int],
    and_cnt: int,
    xor_cnt: int,
    xnor_cnt: int,
    label: str,
) -> tuple[int, int, int, dict[str, int]]:
    for ow in outputs:
        if ow not in defined_gd:
            raise ValueError(f"{label}: output wire '{ow}' was never defined")

    gate_inputs = {out_w: (in1, in2) for (_, out_w, in1, in2) in gates}
    live: set[str] = set(outputs)
    stack = list(outputs)
    while stack:
        cur = stack.pop()
        if cur in gate_inputs:
            for src in gate_inputs[cur]:
                if src not in live:
                    live.add(src)
                    stack.append(src)
    dead_gates = sum(1 for (_, out_w, _, _) in gates if out_w not in live)
    if dead_gates != 0:
        raise ValueError(f"{label}: circuit contains {dead_gates} dead gate(s)")

    if internals:
        expected_internals = set(internals)
        actual_internals = {out_w for (_, out_w, _, _) in gates} - set(outputs)
        if expected_internals != actual_internals:
            raise ValueError(f"{label}: Internal header declaration mismatches actual internal wires")

    g_tot = len(gates)
    max_gd = max(defined_gd[ow] for ow in outputs)
    max_ad = max(defined_ad[ow] for ow in outputs)
    for k_hdr, actual_v in (("G", g_tot), ("A", and_cnt), ("XOR", xor_cnt), ("XNOR", xnor_cnt), ("GD", max_gd), ("AD", max_ad)):
        if k_hdr in header_meta and header_meta[k_hdr] != actual_v:
            raise ValueError(f"{label}: NCFF header comment {k_hdr}={header_meta[k_hdr]} != recomputed {actual_v}")

    out_d_hist: dict[str, int] = {}
    for ow in outputs:
        ks = str(defined_gd[ow])
        out_d_hist[ks] = out_d_hist.get(ks, 0) + 1
    return dead_gates, max_gd, max_ad, {k: out_d_hist[k] for k in sorted(out_d_hist, key=int)}


def evaluate_and_verify_sbox_family(
    func_name: str,
    inputs: list[str],
    outputs: list[str],
    internals: list[str],
    gates: list[tuple[str, str, str, str]],
    header_meta: dict[str, int],
    in_tt: tuple[int, ...],
    target_tt: tuple[int, ...],
    label: str,
) -> dict[str, object]:
    if func_name == "sbox":
        exp_in = [f"U{i}" for i in range(8)]
        exp_out = [f"S{i}" for i in range(8)]
    else:
        exp_in = [f"x{i}" for i in range(8)]
        exp_out = [f"y{i}" for i in range(8)]
    if inputs != exp_in:
        raise ValueError(f"{label}: expected Inputs {exp_in}, got {inputs}")
    if outputs != exp_out:
        raise ValueError(f"{label}: expected Outputs {exp_out}, got {outputs}")
    if len(internals) != len(set(internals)):
        raise ValueError(f"{label}: duplicate wire in Internal declaration")

    defined_gd: dict[str, int] = {}
    defined_ad: dict[str, int] = {}
    tt: dict[str, int] = {}
    lin_mask: dict[str, int] = {}
    lin_cst: dict[str, int] = {}
    pure_in: dict[str, bool] = {}

    for k, w in enumerate(inputs):
        defined_gd[w] = 0
        defined_ad[w] = 0
        tt[w] = in_tt[k]
        lin_mask[w] = 1 << k
        lin_cst[w] = 0
        pure_in[w] = True

    and_cnt = xor_cnt = xnor_cnt = 0
    gd_hist: dict[int, int] = {}
    ad_hist: dict[int, int] = {}

    for idx, (op, out_w, in1, in2) in enumerate(gates):
        for tok in (out_w, in1, in2):
            if tok.lower() in CONSTANT_TOKENS:
                raise ValueError(f"{label}: gate {idx} uses forbidden constant '{tok}'")
        if in1 == in2:
            raise ValueError(f"{label}: gate {idx} ({op} {out_w} {in1} {in2}) uses identical inputs (u == v forbidden)")
        if in1 not in defined_gd or in2 not in defined_gd:
            raise ValueError(f"{label}: gate {idx} uses undefined wire")
        if out_w in defined_gd:
            raise ValueError(f"{label}: wire '{out_w}' defined more than once at gate {idx}")

        g_dep = max(defined_gd[in1], defined_gd[in2]) + 1
        a_dep = max(defined_ad[in1], defined_ad[in2]) + (1 if op == "AND" else 0)
        defined_gd[out_w] = g_dep
        defined_ad[out_w] = a_dep
        gd_hist[g_dep] = gd_hist.get(g_dep, 0) + 1
        pure_in[out_w] = (op in ("XOR", "XNOR")) and pure_in[in1] and pure_in[in2]

        v1, v2 = tt[in1], tt[in2]
        if op == "AND":
            and_cnt += 1
            ad_hist[a_dep] = ad_hist.get(a_dep, 0) + 1
            tt[out_w] = v1 & v2
        elif op == "XOR":
            xor_cnt += 1
            tt[out_w] = v1 ^ v2
        elif op == "XNOR":
            xnor_cnt += 1
            tt[out_w] = (v1 ^ v2) ^ MASK_256
        else:
            raise ValueError(f"{label}: unexpected op {op}")

        if a_dep == 0:
            lin_mask[out_w] = lin_mask[in1] ^ lin_mask[in2]
            lin_cst[out_w] = lin_cst[in1] ^ lin_cst[in2] ^ (1 if op == "XNOR" else 0)

    dead_gates, max_gd, max_ad, out_d_hist = _check_dag_live_and_headers(
        outputs, internals, gates, defined_gd, defined_ad, header_meta, and_cnt, xor_cnt, xnor_cnt, label
    )

    for b in range(8):
        if tt[outputs[b]] != target_tt[b]:
            for byte_in in range(256):
                got_bit = (tt[outputs[b]] >> byte_in) & 1
                exp_bit = (target_tt[b] >> byte_in) & 1
                if got_bit != exp_bit:
                    raise ValueError(
                        f"{label}: truth-table mismatch on output {outputs[b]} at input byte 0x{byte_in:02x} "
                        f"(got {got_bit}, expected {exp_bit})"
                    )

    return {
        "A": and_cnt,
        "AD": max_ad,
        "G": len(gates),
        "GD": max_gd,
        "XOR": xor_cnt,
        "XNOR": xnor_cnt,
        "XX": xor_cnt + xnor_cnt,
        "dead_gates": dead_gates,
        "metrics_tuple": [and_cnt, max_ad, len(gates), max_gd, xor_cnt, xnor_cnt],
        "gates_per_gd_level": [gd_hist.get(d, 0) for d in range(1, max_gd + 1)],
        "ands_per_ad_level": [ad_hist.get(d, 0) for d in range(1, max_ad + 1)],
        "output_gd_hist": out_d_hist,
        "tt": tt,
        "gd": defined_gd,
        "ad": defined_ad,
        "lin_mask": lin_mask,
        "lin_cst": lin_cst,
        "pure_in": pure_in,
    }


def evaluate_and_verify_invmixcols(
    inputs: list[str],
    outputs: list[str],
    internals: list[str],
    gates: list[tuple[str, str, str, str]],
    header_meta: dict[str, int],
    imc_rows: tuple[int, ...],
    label: str,
) -> dict[str, object]:
    if inputs != [f"x{i}" for i in range(32)]:
        raise ValueError(f"{label}: expected Inputs x0:x31, got {inputs[:4]}..{inputs[-2:]}")
    if outputs != [f"y{i}" for i in range(32)]:
        raise ValueError(f"{label}: expected Outputs y0:y31, got {outputs[:4]}..{outputs[-2:]}")
    if len(internals) != len(set(internals)):
        raise ValueError(f"{label}: duplicate wire in Internal declaration")

    defined_gd: dict[str, int] = {w: 0 for w in inputs}
    defined_ad: dict[str, int] = {w: 0 for w in inputs}
    lin_mask: dict[str, int] = {inputs[i]: (1 << i) for i in range(32)}
    gd_hist: dict[int, int] = {}
    gate_vals: set[int] = set()

    for idx, (op, out_w, in1, in2) in enumerate(gates):
        if op != "XOR":
            raise ValueError(f"{label}: gate {idx} uses non-XOR op '{op}'")
        for tok in (out_w, in1, in2):
            if tok.lower() in CONSTANT_TOKENS:
                raise ValueError(f"{label}: gate {idx} uses forbidden constant '{tok}'")
        if in1 == in2:
            raise ValueError(f"{label}: gate {idx} uses identical inputs (u == v forbidden)")
        if in1 not in defined_gd or in2 not in defined_gd:
            raise ValueError(f"{label}: gate {idx} uses undefined wire")
        if out_w in defined_gd:
            raise ValueError(f"{label}: wire '{out_w}' defined more than once at gate {idx}")

        g_dep = max(defined_gd[in1], defined_gd[in2]) + 1
        defined_gd[out_w] = g_dep
        defined_ad[out_w] = 0
        gd_hist[g_dep] = gd_hist.get(g_dep, 0) + 1
        mv = lin_mask[in1] ^ lin_mask[in2]
        if mv == 0:
            raise ValueError(f"{label}: gate {idx} computes constant 0 wire")
        lin_mask[out_w] = mv
        gate_vals.add(mv)

    dead_gates, max_gd, max_ad, out_d_hist = _check_dag_live_and_headers(
        outputs, internals, gates, defined_gd, defined_ad, header_meta, 0, len(gates), 0, label
    )

    for r in range(32):
        if lin_mask[outputs[r]] != imc_rows[r]:
            raise ValueError(
                f"{label}: LINEAR_MAP_MISMATCH on output y{r} "
                f"(got 0x{lin_mask[outputs[r]]:08x}, expected 0x{imc_rows[r]:08x})"
            )

    if len(gate_vals) != len(gates):
        raise ValueError(f"{label}: duplicate linear form among gates ({len(gate_vals)} != {len(gates)})")

    return {
        "A": 0,
        "AD": max_ad,
        "G": len(gates),
        "GD": max_gd,
        "XOR": len(gates),
        "XNOR": 0,
        "XX": len(gates),
        "dead_gates": dead_gates,
        "metrics_tuple": [0, 0, len(gates), max_gd, len(gates), 0],
        "gates_per_gd_level": [gd_hist.get(d, 0) for d in range(1, max_gd + 1)],
        "ands_per_ad_level": [],
        "output_gd_hist": out_d_hist,
        "gate_vals": gate_vals,
    }


def verify_parser_rejects_forbidden_syntax(in_tt: tuple[int, ...], invs_tt: tuple[int, ...]) -> None:
    toy_not = "Inputs: x0:x7\nOutputs: y0:y7\nbegin SLP\nNOT t1 x0\nend SLP\n"
    try:
        parse_strict_ncff(toy_not, "selftest_not", pure_xor_only=False)
    except ValueError as err:
        if "{AND, XOR, XNOR}" not in str(err):
            raise ValueError(f"Unexpected NOT rejection message: {err}") from err
    else:
        raise ValueError("Parser failed to reject forbidden unary NOT gate")

    toy_xnor_lin = "Inputs: x0:x31\nOutputs: y0:y31\nbegin SLP\nXNOR y0 x0 x1\nend SLP\n"
    try:
        parse_strict_ncff(toy_xnor_lin, "selftest_xnor_lin", pure_xor_only=True)
    except ValueError as err:
        if "{XOR}" not in str(err):
            raise ValueError(f"Unexpected linear XNOR rejection message: {err}") from err
    else:
        raise ValueError("Parser failed to reject XNOR in pure-XOR InvMixColumns mode")

    toy_const = "Inputs: x0:x7\nOutputs: y0:y7\nbegin SLP\nXOR y0 x0 1\nend SLP\n"
    ins_c, outs_c, ints_c, gates_c, hdr_c = parse_strict_ncff(toy_const, "selftest_const")
    try:
        evaluate_and_verify_sbox_family("invsbox", ins_c, outs_c, ints_c, gates_c, hdr_c, in_tt, invs_tt, "selftest_const")
    except ValueError:
        pass
    else:
        raise ValueError("Evaluator failed to reject forbidden constant token '1'")

    toy_self = "Inputs: x0:x7\nOutputs: y0:y7\nbegin SLP\nXOR y0 x0 x0\nend SLP\n"
    ins_s, outs_s, ints_s, gates_s, hdr_s = parse_strict_ncff(toy_self, "selftest_self")
    try:
        evaluate_and_verify_sbox_family("invsbox", ins_s, outs_s, ints_s, gates_s, hdr_s, in_tt, invs_tt, "selftest_self")
    except ValueError:
        pass
    else:
        raise ValueError("Evaluator failed to reject self-input gate (u == v)")


# ---------------------------------------------------------------------------
# 3. Pure-Python Algebraic Tightness & Obstruction Verifiers (T1..T6, < 0.1s)
# ---------------------------------------------------------------------------

def verify_152_feeder_pigeonhole_and_rank37(
    gates: list[tuple[str, str, str, str]],
    ev: dict[str, object],
    in_tt: tuple[int, ...],
) -> list[int]:
    tt: dict[str, int] = ev["tt"]  # type: ignore[assignment]
    gd: dict[str, int] = ev["gd"]  # type: ignore[assignment]
    ad: dict[str, int] = ev["ad"]  # type: ignore[assignment]
    lin_mask: dict[str, int] = ev["lin_mask"]  # type: ignore[assignment]
    lin_cst: dict[str, int] = ev["lin_cst"]  # type: ignore[assignment]

    inv_wires = ["t41", "t42", "t43", "t44"]
    for w in inv_wires:
        if gd.get(w) != 7 or ad.get(w) != 3:
            raise ValueError(f"152@10 inverter wire {w} expected (GD=7, AD=3), got (GD={gd.get(w)}, AD={ad.get(w)})")

    basis_37 = [MASK_256]
    for iw in inv_wires:
        basis_37.append(tt[iw])
        for k in range(8):
            basis_37.append(tt[iw] & in_tt[k])
    pivots: dict[int, int] = {}
    for vec in basis_37:
        x = vec
        while x:
            lead = x.bit_length() - 1
            if lead in pivots:
                x ^= pivots[lead]
            else:
                pivots[lead] = x
                break
    rank_37 = len(pivots)
    if rank_37 != 37:
        raise ValueError(f"Expected bilinear basis GF(2) rank 37, got {rank_37}")

    out_to_idx = {ow: idx for idx, (_, ow, _, _) in enumerate(gates)}
    t44_idx = out_to_idx["t44"]
    a26_idx = out_to_idx["a26"]
    prefix_gates = gates[: t44_idx + 1]
    feeder_gates = gates[t44_idx + 1 : a26_idx]
    bottom_gates = gates[a26_idx:]

    prefix_aff = {(1 << k, 0) for k in range(8)}
    for _, ow, _, _ in prefix_gates:
        if ad[ow] == 0:
            prefix_aff.add((lin_mask[ow], lin_cst[ow]))

    mux_ands = [g for g in bottom_gates if g[0] == "AND"]
    if len(mux_ands) != 32:
        raise ValueError(f"Expected 32 Level-8 mux AND gates, got {len(mux_ands)}")

    req_aff: set[tuple[int, int]] = set()
    for _, ow, i1, i2 in mux_ands:
        lw = i2 if i1 in inv_wires else i1
        iw = i1 if i1 in inv_wires else i2
        if iw not in inv_wires or ad[lw] != 0 or gd[lw] > 7:
            raise ValueError(f"Mux AND {ow} does not pair an inverter wire with a GD<=7 affine wire")
        req_aff.add((lin_mask[lw], lin_cst[lw]))

    in_prefix_cnt = sum(1 for mc in req_aff if mc in prefix_aff)
    missing_cnt = len(req_aff) - in_prefix_cnt
    if len(req_aff) != 32 or in_prefix_cnt != 5 or missing_cnt != 27 or len(feeder_gates) != 27:
        raise ValueError("Feeder pigeonhole mismatch on 152@10")
    return [len(prefix_gates), len(feeder_gates), len(bottom_gates), rank_37, len(req_aff), in_prefix_cnt, missing_cnt]


def _closure_reaches_all(targets_set: set[int], allowed_set: set[int]) -> bool:
    reach = [1 << k for k in range(8)]
    reach_set = set(reach)
    rem_w = set(allowed_set)
    rem_t = set(targets_set)
    while rem_t:
        progressed = False
        for v in list(rem_w):
            for a in reach:
                b = v ^ a
                if b in reach_set and b != a:
                    reach.append(v)
                    reach_set.add(v)
                    rem_w.remove(v)
                    rem_t.discard(v)
                    progressed = True
                    break
        if not progressed:
            return False
    return True


def verify_zone_top_closures(w3_block: dict[str, object]) -> None:
    inputs_set = {1 << k for k in range(8)}

    t1 = w3_block["T1_zone_top_invsbox_105_exact_18"]  # type: ignore[index]
    t1_set = set(int(x) for x in t1["targets"])  # type: ignore[index]
    if len(t1_set) != 17 or (t1_set & inputs_set) or (0 in t1_set) or _closure_reaches_all(t1_set, t1_set):
        raise ValueError("T1 falsified at H=0")
    pool_t1 = [m for m in range(1, 256) if m not in inputs_set and m not in t1_set]
    hits_1h = [h for h in pool_t1 if _closure_reaches_all(t1_set, t1_set | {h})]
    if len(pool_t1) != 230 or hits_1h != [int(t1["K18_unique_helper_mask"])]:  # type: ignore[index]
        raise ValueError(f"T1 1-helper SAT mismatch: {hits_1h}")

    t2 = w3_block["T2_zone_top_invsbox_126_exact_18"]  # type: ignore[index]
    t2_set = set(int(x) for x in t2["targets"])  # type: ignore[index]
    pool_t2 = [m for m in range(1, 256) if m not in inputs_set and m not in t2_set]
    if len(t2_set) != 16 or _closure_reaches_all(t2_set, t2_set) or any(_closure_reaches_all(t2_set, t2_set | {h}) for h in pool_t2):
        raise ValueError("T2 falsified")

    t3 = w3_block["T3_zone_top_sbox_124_exact_19"]  # type: ignore[index]
    t3_set = set(int(x) for x in t3["targets"])  # type: ignore[index]
    pool_t3 = [m for m in range(1, 256) if m not in inputs_set and m not in t3_set]
    if len(t3_set) != 17 or _closure_reaches_all(t3_set, t3_set) or any(_closure_reaches_all(t3_set, t3_set | {h}) for h in pool_t3):
        raise ValueError("T3 falsified")

    sep_set = set(int(x) for x in t3["positive_separator_sbox_103"]["targets"])  # type: ignore[index]
    if len(sep_set) != 17 or not _closure_reaches_all(sep_set, sep_set):
        raise ValueError("Positive separator control sbox-103 failed 0-helper closure")


def verify_norm_basis_orbits_and_d2_count(asym_block: dict[str, object], in_tt: tuple[int, ...]) -> None:
    seen: set[int] = set(in_tt)
    pool: list[tuple[int, int, int]] = [(t, 0, 0) for t in in_tt]
    for i in range(8):
        ti = pool[i][0]
        for j in range(i + 1, 8):
            tj = pool[j][0]
            for op_ad, val in ((0, ti ^ tj), (0, (ti ^ tj) ^ MASK_256), (1, ti & tj)):
                if val not in seen:
                    seen.add(val)
                    pool.append((val, 1, op_ad))
    n1 = len(pool)
    for i in range(n1):
        ti, di, adi = pool[i]
        for j in range(i + 1, n1):
            tj, dj, adj = pool[j]
            if di == 0 and dj == 0:
                continue
            tx = ti ^ tj
            if tx not in seen:
                seen.add(tx)
                pool.append((tx, 2, max(adi, adj)))
            txn = tx ^ MASK_256
            if txn not in seen:
                seen.add(txn)
                pool.append((txn, 2, max(adi, adj)))
            if max(adi, adj) == 0:
                ta = ti & tj
                if ta not in seen:
                    seen.add(ta)
                    pool.append((ta, 2, 1))
    n2 = len(pool)
    if [8, n1, n2] != asym_block["d0_d1_d2_unique_signals_ad_le_1"]:
        raise ValueError(f"D<=2 zero-NOT signal count mismatch: [8, {n1}, {n2}]")

    fwd_masks = [int(x) for x in asym_block["sbox_forward_z_eq_x"]["reachable_nonzero_norm_masks_at_gd_le_4"]]  # type: ignore[index]
    inv_masks = [int(x) for x in asym_block["invsbox_z_eq_inv_aff_x_xor_0x63"]["reachable_nonzero_norm_masks_at_gd_le_4"]]  # type: ignore[index]

    def gf2_rank_4bit(masks: list[int]) -> int:
        pivs: dict[int, int] = {}
        for m in masks:
            v = m
            while v:
                b = v.bit_length() - 1
                if b in pivs:
                    v ^= pivs[b]
                else:
                    pivs[b] = v
                    break
        return len(pivs)

    if len(fwd_masks) != 2 or gf2_rank_4bit(fwd_masks) != 2:
        raise ValueError("Forward S-box reachable norm mask rank check failed")
    if len(inv_masks) != 8 or gf2_rank_4bit(inv_masks) != 4:
        raise ValueError("InvS-box reachable norm mask rank check failed")
    for orb in asym_block["invsbox_z_eq_inv_aff_x_xor_0x63"]["galois_normal_basis_orbits"]:  # type: ignore[index]
        orb_l = [int(x) for x in orb]
        if len(orb_l) != 4 or not set(orb_l).issubset(set(inv_masks)) or gf2_rank_4bit(orb_l) != 4:
            raise ValueError(f"Invalid Galois normal-basis orbit {orb_l}")

    gf16_ordered: list[int] = []
    for x in range(1, 256):
        nm = gf256_pow(x, 17)
        if nm not in gf16_ordered:
            gf16_ordered.append(nm)
    basis4: list[int] = []
    piv4: list[int] = []
    for e in gf16_ordered:
        v = e
        for p in piv4:
            if (v ^ p) < v:
                v ^= p
        if v:
            piv4.append(v)
            basis4.append(e)
            piv4.sort(reverse=True)
            if len(basis4) == 4:
                break
    basis4_hex = [f"0x{b:02x}" for b in basis4]
    if basis4_hex != asym_block["gf16_basis_hex"] or any(gf256_pow(b, 16) != b for b in basis4):
        raise ValueError(f"GF(2^4) basis check failed: {basis4_hex} != {asym_block['gf16_basis_hex']}")


def verify_wave5_t5a_and_t6(
    w5_block: dict[str, object],
    ev_111: dict[str, object],
    gates_111: list[tuple[str, str, str, str]],
    ev_109: dict[str, object],
    gates_109: list[tuple[str, str, str, str]],
) -> None:
    # T5a: Verify P=16 states on 111@14's GD=5 wires, [6, 45, 643, 33602] non-constant zero-NOT layers,
    # 0/9 targets in S7, and {t51, t53, t58} outside S8 -> >= 9 gates at depth >= 8 by Pigeonhole.
    t5a = w5_block["T5a_middle_gd5_to_gd10_global_optimality_20g"]  # type: ignore[index]
    tt111: dict[str, int] = ev_111["tt"]  # type: ignore[assignment]
    gd5_wires = [str(w) for w in t5a["gd5_input_wires"]]  # type: ignore[index]
    mid_outs = [str(w) for w in t5a["middle_output_wires"]]  # type: ignore[index]

    seen_st: dict[tuple[int, ...], tuple[int, ...]] = {}
    for x in range(256):
        st = tuple((tt111[w] >> x) & 1 for w in gd5_wires)
        ov = tuple((tt111[w] >> x) & 1 for w in mid_outs)
        if seen_st.setdefault(st, ov) != ov:
            raise ValueError("111@14 middle output is not a well-defined function of GD=5 state")
    states = sorted(seen_st.keys())
    p_cnt = len(states)
    m_p = (1 << p_cnt) - 1
    s5 = {sum(st[i] << idx for idx, st in enumerate(states)) for i in range(6)}
    out_p = [sum(seen_st[st][h] << idx for idx, st in enumerate(states)) for h in range(9)]

    def step_nonconst(prev_s: set[int]) -> set[int]:
        lst = sorted(prev_s)
        nxt = set(prev_s)
        n_l = len(lst)
        for i in range(n_l):
            a = lst[i]
            for j in range(i + 1, n_l):
                b = lst[j]
                nxt.add(a & b)
                xv = a ^ b
                nxt.add(xv)
                nxt.add(xv ^ m_p)
        nxt.discard(0)
        nxt.discard(m_p)
        return nxt

    s6 = step_nonconst(s5)
    s7 = step_nonconst(s6)
    s8 = step_nonconst(s7)
    if (
        p_cnt != int(t5a["P_states_gd5"])  # type: ignore[index]
        or [len(s5), len(s6), len(s7), len(s8)] != t5a["nonconstant_layer_sizes"]  # type: ignore[index]
        or any(v in s7 for v in out_p)
        or any(out_p[idx] in s8 for idx in (6, 7, 8))
    ):
        raise ValueError("T5a middle reachability / Pigeonhole check failed on 111@14")

    # T6: Verify 0 / 2,040 GF(2^8) Frobenius-scaling conjugates achieve Zone_Top <= 17 or Zone_Top+(1^x6) <= 18
    t6 = w5_block["T6_conjugate_2040_zone_top_and_1x6_obstruction"]  # type: ignore[index]

    def extract_ext_forms(ev_d: dict[str, object], g_list: list[tuple[str, str, str, str]]) -> list[tuple[int, int]]:
        tt_d: dict[str, int] = ev_d["tt"]  # type: ignore[assignment]
        pi_d: dict[str, bool] = ev_d["pure_in"]  # type: ignore[assignment]
        forms: set[tuple[int, int]] = set()
        for _, ow, a, b in g_list:
            if pi_d[ow]:
                continue
            for u in (a, b):
                if pi_d[u]:
                    tv = tt_d[u]
                    c0 = tv & 1
                    msk = 0
                    for i in range(8):
                        if ((tv >> (1 << (7 - i))) & 1) ^ c0:
                            msk |= 1 << i
                    forms.add((c0, msk))
        return sorted(forms)

    f111 = extract_ext_forms(ev_111, gates_111)
    f111_t = sorted(set(f111) | {(1, 1 << 6)})
    f109 = extract_ext_forms(ev_109, gates_109)
    f109_t = sorted(set(f109) | {(1, 1 << 6)})
    if len(f111) != int(t6["c111_external_top_forms_count"]) or len(f109) != int(t6["c109_external_top_forms_count"]):  # type: ignore[index]
        raise ValueError("T6 external top form count mismatch")

    basis_bm = sum(1 << (1 << i) for i in range(8))

    def closure_bm(allowed_bm: int) -> int:
        vis = basis_bm
        vis_list = [1 << i for i in range(8)]
        rem = allowed_bm & ~vis
        while rem:
            added = 0
            m = rem
            while m:
                lsb = m & -m
                v = lsb.bit_length() - 1
                m ^= lsb
                for a in vis_list:
                    if (vis >> (v ^ a)) & 1:
                        added |= lsb
                        vis_list.append(v)
                        break
            if not added:
                break
            vis |= added
            rem ^= added
        return vis

    def min_01_fast(wt2_set: set[int], need_le: int) -> int:
        k0 = len(wt2_set)
        if k0 > need_le:
            return k0 + 2
        t_bm = 0
        for m in wt2_set:
            t_bm |= 1 << m
        vis0 = closure_bm(t_bm)
        if (vis0 & t_bm) == t_bm:
            return k0
        if k0 + 1 > need_le:
            return k0 + 2
        vis0_list: list[int] = []
        tmp = vis0
        while tmp:
            lsb = tmp & -tmp
            vis0_list.append(lsb.bit_length() - 1)
            tmp ^= lsb
        cand_h: set[int] = set()
        n_v = len(vis0_list)
        for i in range(n_v):
            ai = vis0_list[i]
            for j in range(i + 1, n_v):
                h = ai ^ vis0_list[j]
                if not ((vis0 >> h) & 1) and not ((t_bm >> h) & 1):
                    cand_h.add(h)
        for h in cand_h:
            if (closure_bm(t_bm | (1 << h)) & t_bm) == t_bm:
                return k0 + 1
        return k0 + 2

    a_cols = [fips197_affine(1 << j) ^ 0x63 for j in range(8)]

    def apply_mat8(mat: list[int], xv: int) -> int:
        rv = 0
        for j in range(8):
            if (xv >> j) & 1:
                rv ^= mat[j]
        return rv

    ainv_cols = [0] * 8
    for y in range(256):
        vy = apply_mat8(a_cols, y)
        for j in range(8):
            if vy == (1 << j):
                ainv_cols[j] = y

    hits = [0, 0, 0, 0]
    for k in range(8):
        p2k = [gf256_pow(z, 1 << k) for z in range(256)]
        for lam in range(1, 256):
            g_cols = [gf256_mul(lam, p2k[1 << j]) for j in range(8)]
            lin = [apply_mat8(a_cols, apply_mat8(g_cols, ainv_cols[j])) for j in range(8)]
            cin = apply_mat8(lin, 0x63) ^ 0x63
            row_masks = [0] * 8
            cin_bits = 0
            for i in range(8):
                rm = 0
                for j in range(8):
                    if (lin[j] >> (7 - i)) & 1:
                        rm |= 1 << j
                row_masks[i] = rm
                if (cin >> (7 - i)) & 1:
                    cin_bits |= 1 << i

            # Fast 256-entry linear map & parity tables for this (lam, k)
            map_m = [0] * 256
            map_p = [0] * 256
            for b in range(8):
                step_b = 1 << b
                rm_b = row_masks[b]
                cp_b = (cin_bits >> b) & 1
                for prev in range(step_b):
                    map_m[prev | step_b] = map_m[prev] ^ rm_b
                    map_p[prev | step_b] = map_p[prev] ^ cp_b

            for idx_q, (flist, cap) in enumerate(((f111, 17), (f111_t, 18), (f109, 17), (f109_t, 18))):
                out_f = {(c0 ^ map_p[msk], map_m[msk]) for (c0, msk) in flist}
                wt2 = {m for (_, m) in out_f if m.bit_count() >= 2}
                ep = sum(1 for m in wt2 if (0, m) in out_f and (1, m) in out_f)
                w1c = sum(1 for (c0, m) in out_f if m.bit_count() == 1 and c0 == 1)
                if len(wt2) + ep + w1c <= cap:
                    if min_01_fast(wt2, cap - ep - w1c) + ep + w1c <= cap:
                        hits[idx_q] += 1

    if hits != t6["conjugate_hits_vector_111_top17_top18_109_top17_top18"]:  # type: ignore[index]
        raise ValueError(f"T6 2,040-conjugate obstruction check failed: {hits}")


def locate_pkg_dirs() -> tuple[Path, Path]:
    here = Path(__file__).resolve()
    if here.parent.name == "verify-it-yourself":
        pkg_root = here.parent.parent
        obj_dir = pkg_root / "object"
    else:
        pkg_root = here.parent
        obj_dir = pkg_root / "results"
    return pkg_root, obj_dir


def verify_all(corrupt_mode: bool = False) -> int:
    t0 = time.perf_counter()
    pkg_root, obj_dir = locate_pkg_dirs()

    try:
        # 0. Verify SHA256SUMS manifest in clean mode
        sums_path = pkg_root / "SHA256SUMS"
        if sums_path.is_file() and not corrupt_mode:
            for raw_ln in sums_path.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", raw_ln.strip())
                if m:
                    exp_h, rel_p = m.group(1), m.group(2).lstrip("./")
                    fp = pkg_root / rel_p
                    if not fp.is_file() or sha256_bytes(fp.read_bytes()) != exp_h:
                        raise ValueError(f"SHA256SUMS mismatch on {rel_p}")

        cert_path = obj_dir / "00_nist_aes_gd10_and_barriers_certificate.json"
        if not cert_path.is_file():
            raise FileNotFoundError(f"Missing certificate JSON: {cert_path.name}")
        cert = json.loads(cert_path.read_text(encoding="utf-8"))

        # 1. Verify static barriers & frontier commitment
        static_sub = {
            "frontier_baseline_2026_11_17": cert["frontier_baseline_2026_11_17"],
            "invmixcols_92_at_10_milestone_p3": cert["invmixcols_92_at_10_milestone_p3"],
            "forward_vs_inverse_gd10_tower_norm_asymmetry": cert["forward_vs_inverse_gd10_tower_norm_asymmetry"],
            "wave3_nonlinear_exact_sat_and_milp_barriers": cert["wave3_nonlinear_exact_sat_and_milp_barriers"],
            "wave5_111_gd14_exact_tightness_barriers": cert["wave5_111_gd14_exact_tightness_barriers"],
            "wave2_linear_mixcolumns_barriers": cert["wave2_linear_mixcolumns_barriers"],
        }
        if canonical_json_sha256(static_sub) != PINNED_STATIC_BARRIERS_SHA256:
            raise ValueError("Certificate frontier / barrier JSON block failed integrity commitment")

        # 2. Derive FIPS 197 SBox(), InvSBox(), and InvMixColumns() algebraically & run parser negative self-tests
        in_tt, s_tt, invs_tt, imc_rows = derive_fips197_oracles()
        verify_parser_rejects_forbidden_syntax(in_tt, invs_tt)

        # 3. Parse, validate, and exhaustively evaluate all 13 constructed NCFF circuits
        circ_entries = cert["constructed_circuits"]
        if len(circ_entries) != 13:
            raise ValueError(f"Expected 13 constructed circuits in certificate, found {len(circ_entries)}")

        by_name_ev: dict[str, dict[str, object]] = {}
        by_name_gates: dict[str, list[tuple[str, str, str, str]]] = {}

        for idx, entry in enumerate(circ_entries):
            fname = str(entry["filename"])
            fn = str(entry["function"])
            cpath = obj_dir / fname
            if not cpath.is_file():
                raise FileNotFoundError(f"Missing circuit file {fname}")
            raw_b = cpath.read_bytes()
            actual_sha = sha256_bytes(raw_b)
            if not corrupt_mode and actual_sha != entry["sha256"]:
                raise ValueError(f"SHA-256 mismatch on {fname}: {actual_sha} != {entry['sha256']}")

            is_lin = fn == "invmixcols"
            inputs, outputs, internals, gates, hdr_meta = parse_strict_ncff(
                raw_b.decode("utf-8"), fname, pure_xor_only=is_lin
            )
            if corrupt_mode and idx == 0:
                mid = len(gates) // 2
                op_m, ow_m, u_m, v_m = gates[mid]
                alt_u = "x0" if u_m != "x0" and v_m != "x0" else ("x1" if u_m != "x1" and v_m != "x1" else "x2")
                gates = list(gates)
                gates[mid] = (op_m, ow_m, alt_u, v_m)
                hdr_meta = {}

            if is_lin:
                ev = evaluate_and_verify_invmixcols(inputs, outputs, internals, gates, hdr_meta, imc_rows, fname)
            else:
                targ = s_tt if fn == "sbox" else invs_tt
                ev = evaluate_and_verify_sbox_family(fn, inputs, outputs, internals, gates, hdr_meta, in_tt, targ, fname)

            for k in ("A", "AD", "G", "GD", "XOR", "XNOR", "XX", "dead_gates"):
                if int(ev[k]) != int(entry[k]):  # type: ignore[arg-type]
                    raise ValueError(f"{fname} metric {k} mismatch: recomputed={ev[k]} vs cert={entry[k]}")
            if (
                ev["metrics_tuple"] != entry["metrics_tuple_a_ad_g_gd_xor_xnor"]
                or ev["gates_per_gd_level"] != entry["gates_per_gd_level"]
                or ev["ands_per_ad_level"] != entry["ands_per_ad_level"]
                or ev["output_gd_hist"] != entry["output_gd_hist"]
            ):
                raise ValueError(f"{fname} tuple/level-histogram mismatch against certificate")
            if int(entry["NOT"]) != 0 or int(entry["constants_used"]) != 0 or int(entry["self_input_gates"]) != 0:
                raise ValueError(f"{fname} nonzero NOT/constant/self-input metadata in certificate")

            by_name_ev[fname] = ev
            by_name_gates[fname] = gates

        # 4. Verify non-isomorphism (overlap = 72/92, symdiff = 40) on the 2 InvMixColumns 92@10 witnesses
        gv_main: set[int] = by_name_ev["aes-invmixcols-xor92-depth10.circ.txt"]["gate_vals"]  # type: ignore[assignment]
        gv_alt: set[int] = by_name_ev["aes-invmixcols-xor92-depth10-alt.circ.txt"]["gate_vals"]  # type: ignore[assignment]
        imc_cert = cert["invmixcols_92_at_10_milestone_p3"]
        if (
            len(gv_main & gv_alt) != int(imc_cert["value_set_overlap_out_of_92"])
            or len(gv_main ^ gv_alt) != int(imc_cert["value_set_symmetric_difference"])
        ):
            raise ValueError("InvMixColumns 92@10 witness overlap / symmetric-difference mismatch")

        # 5. Verify 152@10 bilinear rank-37/37 & 27-missing-affine-form Pigeonhole tightness (T4)
        feeder_vec = verify_152_feeder_pigeonhole_and_rank37(
            by_name_gates["aes-invsbox-a57-ad4-g152-gd10-xx95-25.circ.txt"], by_name_ev["aes-invsbox-a57-ad4-g152-gd10-xx95-25.circ.txt"], in_tt
        )
        t4_cert = cert["wave3_nonlinear_exact_sat_and_milp_barriers"]["T4_152_gd10_feeder_global_pigeonhole_27"]
        if feeder_vec != t4_cert["feeder_counts_vector"]:
            raise ValueError(f"T4 feeder vector mismatch: {feeder_vec}")

        # 6. Verify Zone_Top exact GF(2)^8 0/1-helper UNSAT/SAT closures (T1..T3 + sbox-103 separator)
        verify_zone_top_closures(cert["wave3_nonlinear_exact_sat_and_milp_barriers"])

        # 7. Verify Depth<=2 zero-NOT signal counts [8, 92, 4358], GF(16) basis, & Galois normal-basis rank asymmetry
        verify_norm_basis_orbits_and_d2_count(cert["forward_vs_inverse_gd10_tower_norm_asymmetry"], in_tt)

        # 8. Verify Wave 5 T5a (111@14 P=16 [6,45,643,33602] Pigeonhole) & T6 (0/2,040 conjugates on 111@14 & 109@15)
        verify_wave5_t5a_and_t6(
            cert["wave5_111_gd14_exact_tightness_barriers"],
            by_name_ev["aes-invsbox-a34-ad4-g111-gd14-xx77-41.circ.txt"],
            by_name_gates["aes-invsbox-a34-ad4-g111-gd14-xx77-41.circ.txt"],
            by_name_ev["aes-invsbox-a33-ad4-g109-gd15-xx76-36.circ.txt"],
            by_name_gates["aes-invsbox-a33-ad4-g109-gd15-xx76-36.circ.txt"],
        )

    except Exception as exc:
        print(f"VERIFICATION ERROR: {exc}")
        print("FAIL")
        return 1

    dt = time.perf_counter() - t0
    print(
        f"VERIFICATION SUMMARY: Verified 13/13 NCFF-0.1-2026 AES circuits (2/2 pure-XOR InvMixColumns 92@10 [p3, "
        f"overlap=72/92, symdiff=40], 2/2 zero-NOT GD=10 InvS-box 152@10 & 155@10 [p4], and 9/9 zero-NOT [Inv]S-box "
        f"witnesses across 8 4D Pareto cells led by 33/4/111/14, 109@15, 129@13, 119@14; 0 NOT, 0 constants, 0 self-inputs, "
        f"0 dead gates) + T1..T6 exact algebraic tightness & 2,040-conjugate checks in {dt:.3f}s"
    )
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(verify_all(corrupt_mode=("--corrupt" in sys.argv)))
