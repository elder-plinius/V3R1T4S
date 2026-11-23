#!/usr/bin/env python3
"""
Exact Zone_Top GF(2)^8 Helper Enumeration, Named-Node Canonical CNF Generator,
and 152@10 GD<=7 Affine Feeder Rank/Pigeonhole Auditor.

Standalone script using only the Python 3 standard library.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import shutil
import time
from pathlib import Path

MASK_256 = (1 << 256) - 1


def _build_in_tt() -> tuple[int, ...]:
    in_tt = [0] * 8
    for val in range(256):
        for k in range(8):
            if (val >> (7 - k)) & 1:
                in_tt[k] |= 1 << val
    return tuple(in_tt)


SBOX_IN_TT = _build_in_tt()


def _expand_var_spec(spec: str) -> list[str]:
    out: list[str] = []
    for tok in re.split(r"[\s,]+", spec.strip()):
        if not tok:
            continue
        m = re.match(r"^([A-Za-z_]+)(\d+):([A-Za-z_]*)(\d+)$", tok)
        if m:
            p1, s_idx, p2, e_idx = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
            if p2 and p2 != p1:
                raise ValueError(f"Mismatched range prefix in {tok}")
            step = 1 if e_idx >= s_idx else -1
            for k in range(s_idx, e_idx + step, step):
                out.append(f"{p1}{k}")
        else:
            out.append(tok)
    return out


def parse_ncff_circuit(text: str) -> tuple[list[str], list[str], list[tuple[str, str, tuple[str, str]]]]:
    inputs: list[str] = []
    outputs: list[str] = []
    gates: list[tuple[str, str, tuple[str, str]]] = []
    has_begin = any(rl.strip().lower().startswith("begin slp") for rl in text.splitlines())
    in_slp = not has_begin
    for raw_line in text.splitlines():
        line = raw_line.split("%", 1)[0].strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        low = line.lower()
        if low.startswith("begin slp"):
            in_slp = True
            continue
        if low.startswith("end slp"):
            in_slp = False
            continue
        if low.startswith(("begin ", "end ", "internal:", "gatesyntax:")) or low in ("begin", "end"):
            continue
        if low.startswith("inputs:"):
            inputs = _expand_var_spec(line.split(":", 1)[1])
            continue
        if low.startswith("outputs:"):
            outputs = _expand_var_spec(line.split(":", 1)[1])
            continue
        if not in_slp:
            continue
        toks = line.split()
        if len(toks) != 4:
            raise ValueError(f"Expected 2-input prefix gate line, got: {line}")
        gates.append((toks[0].upper(), toks[1], (toks[2], toks[3])))
    return inputs, outputs, gates


ZONE_TOP_BENCHMARKS: dict[str, dict[str, object]] = {
    "sbox_103_pos_ctrl": {
        "orig_top_gates": 17,
        "max_helpers": 0,
        "targets": [6, 25, 134, 27, 89, 102, 100, 217, 116, 209, 24, 173, 171, 172, 68, 202, 56],
    },
    "invsbox_105": {
        "orig_top_gates": 18,
        "max_helpers": 1,
        "targets": [74, 12, 248, 164, 109, 96, 39, 232, 230, 186, 246, 136, 193, 215, 97, 168, 22],
    },
    "invsbox_126": {
        "orig_top_gates": 18,
        "max_helpers": 1,
        "targets": [200, 214, 194, 28, 100, 146, 60, 29, 136, 228, 254, 155, 232, 121, 142, 134],
    },
    "sbox_124": {
        "orig_top_gates": 19,
        "max_helpers": 1,
        "targets": [165, 35, 12, 133, 56, 127, 13, 229, 45, 111, 162, 90, 95, 232, 86, 39, 31],
    },
}


def exact_helper_enum_f2_8(targets: list[int], max_helpers: int = 1) -> dict[int, dict[str, object]]:
    tset = set(targets)
    inputs = {1 << k for k in range(8)}
    if (tset & inputs) or (0 in tset):
        raise ValueError("Targets must be nonzero non-unit 8-bit masks")
    pool = [m for m in range(1, 256) if m not in inputs and m not in tset]
    results: dict[int, dict[str, object]] = {}

    for h_cnt in range(max_helpers + 1):
        t0 = time.perf_counter()
        checked = 0
        sat_count = 0
        first_witness = None
        total_comb = 1
        for k in range(h_cnt):
            total_comb = total_comb * (len(pool) - k) // (k + 1)

        for comb in itertools.combinations(pool, h_cnt):
            checked += 1
            reach = [1 << k for k in range(8)]
            reach_set = set(reach)
            rem_w = tset | set(comb)
            rem_t = set(tset)
            steps = []
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
                            steps.append((v, a, b))
                            progressed = True
                            break
                if not progressed:
                    break
            if not rem_t:
                sat_count += 1
                if first_witness is None:
                    first_witness = {"helpers": list(comb), "steps": steps}
        dt = time.perf_counter() - t0
        results[h_cnt] = {
            "K": len(targets) + h_cnt,
            "H": h_cnt,
            "status": "SAT" if sat_count > 0 else "UNSAT",
            "sat_helper_tuples": sat_count,
            "subsets_checked": checked,
            "total_subsets": total_comb,
            "runtime_sec": round(dt, 4),
            "witness": first_witness,
        }
    return results


def audit_152_gd10_feeder(circ_path: Path) -> dict[str, object]:
    ins, _, gates = parse_ncff_circuit(circ_path.read_text(encoding="utf-8"))
    tt = {ins[k]: SBOX_IN_TT[k] for k in range(8)}
    gd = {ins[k]: 0 for k in range(8)}
    ad = {ins[k]: 0 for k in range(8)}
    lin_mask = {ins[k]: (1 << k) for k in range(8)}
    lin_cst = {ins[k]: 0 for k in range(8)}
    gate_idx_map: dict[str, int] = {}

    for idx, (op, ow, (i1, i2)) in enumerate(gates):
        gate_idx_map[ow] = idx
        gd[ow] = max(gd[i1], gd[i2]) + 1
        ad[ow] = max(ad[i1], ad[i2]) + (1 if op == "AND" else 0)
        if op == "AND":
            tt[ow] = tt[i1] & tt[i2]
        elif op == "XOR":
            tt[ow] = tt[i1] ^ tt[i2]
        else:
            tt[ow] = (tt[i1] ^ tt[i2]) ^ MASK_256
        if ad[ow] == 0:
            lin_mask[ow] = lin_mask[i1] ^ lin_mask[i2]
            lin_cst[ow] = lin_cst[i1] ^ lin_cst[i2] ^ (1 if op == "XNOR" else 0)

    inv_wires = ["t41", "t42", "t43", "t44"]
    t44_idx = gate_idx_map["t44"]
    a26_idx = gate_idx_map["a26"]
    prefix_gates = gates[: t44_idx + 1]
    feeder_gates = gates[t44_idx + 1 : a26_idx]
    bottom_gates = gates[a26_idx:]

    prefix_lin_wires = list(ins) + [ow for (_, ow, _) in prefix_gates if ad[ow] == 0]
    prefix_mc = {(lin_mask[w], lin_cst[w]): (w, gd[w]) for w in prefix_lin_wires}

    mux_ands = [g for g in bottom_gates if g[0] == "AND"]
    req_aff_set = set()
    for _, _, (i1, i2) in mux_ands:
        lw = i2 if i1 in inv_wires else i1
        req_aff_set.add((lin_mask[lw], lin_cst[lw]))

    distinct_req_aff = sorted(req_aff_set)
    already_in_prefix = [(m, c) for (m, c) in distinct_req_aff if (m, c) in prefix_mc]
    missing_from_prefix = [(m, c) for (m, c) in distinct_req_aff if (m, c) not in prefix_mc]

    basis_37 = [MASK_256]
    for iw in inv_wires:
        basis_37.append(tt[iw])
        for k in range(8):
            basis_37.append(tt[iw] & SBOX_IN_TT[k])
    pivs: dict[int, int] = {}
    for vec in basis_37:
        x = vec
        while x:
            b = x.bit_length() - 1
            if b in pivs:
                x ^= pivs[b]
            else:
                pivs[b] = x
                break
    rank_37 = len(pivs)

    return {
        "prefix_gate_count": len(prefix_gates),
        "feeder_gate_count": len(feeder_gates),
        "bottom_gate_count": len(bottom_gates),
        "bilinear_37_basis_gf2_rank": rank_37,
        "bilinear_37_basis_nullity": 37 - rank_37,
        "distinct_mux_affine_forms_needed": len(distinct_req_aff),
        "already_in_prefix_exact_polarity": len(already_in_prefix),
        "missing_distinct_affine_forms": len(missing_from_prefix),
        "is_feeder_zero_helper_pigeonhole_tight": (len(feeder_gates) == len(missing_from_prefix)),
    }


def main() -> int:
    here = Path(__file__).resolve().parent
    default_circ = here.parent / "results" / "aes-invsbox-a57-ad4-g152-gd10-xx95-25.circ.txt"
    if not default_circ.is_file():
        default_circ = here.parent / "object" / "aes-invsbox-a57-ad4-g152-gd10-xx95-25.circ.txt"

    ap = argparse.ArgumentParser()
    ap.add_argument("--circuit-152", type=Path, default=default_circ)
    ap.add_argument("--kissat", type=str, default=shutil.which("kissat") or "")
    args = ap.parse_args()

    for label, spec in ZONE_TOP_BENCHMARKS.items():
        targets = list(spec["targets"])  # type: ignore[arg-type]
        max_h = int(spec["max_helpers"])  # type: ignore[arg-type]
        res = exact_helper_enum_f2_8(targets, max_helpers=max_h)
        print(f"[Zone_Top] {label}: " + ", ".join(f"H={h} (K={r['K']}): {r['status']}" for h, r in res.items()))

    if args.circuit_152.is_file():
        print(f"[152@10 Feeder] {json.dumps(audit_152_gd10_feeder(args.circuit_152))}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
