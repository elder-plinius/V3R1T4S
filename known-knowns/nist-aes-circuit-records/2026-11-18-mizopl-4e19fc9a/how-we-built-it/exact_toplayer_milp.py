#!/usr/bin/env python3
"""
Exact Top-2-Layer Hitting-Set / Edge-Cover MILP via scipy.optimize.milp (HiGHS).

Given any depth-D linear XOR circuit over 32 inputs, freezes P_{<=D-2} (all linear
masks reachable at depth <= D-2), enumerates 100% of buildable depth-(D-1) masks
B_{D-1} = (P_{<=D-2} ^ P_{<=D-2}) - P_{<=D-2} and all depth-<=D target recipes,
and solves the exact minimum gate count via HiGHS.
"""
from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix


def gf256_mul(a: int, b: int) -> int:
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def build_mixcols_masks(byte_matrix: list[list[int]]) -> tuple[int, ...]:
    masks = [0] * 32
    for in_b in range(4):
        for in_r in range(8):
            in_wire = 8 * in_b + in_r
            in_bytes = [0, 0, 0, 0]
            in_bytes[in_b] = 1 << in_r
            for out_b in range(4):
                acc = 0
                for k in range(4):
                    acc ^= gf256_mul(byte_matrix[out_b][k], in_bytes[k])
                for out_r in range(8):
                    if (acc >> out_r) & 1:
                        masks[8 * out_b + out_r] |= 1 << in_wire
    return tuple(masks)


MIXCOLS_MASKS = build_mixcols_masks(
    [[0x02, 0x03, 0x01, 0x01], [0x01, 0x02, 0x03, 0x01], [0x01, 0x01, 0x02, 0x03], [0x03, 0x01, 0x01, 0x02]]
)
INVMIXCOLS_MASKS = build_mixcols_masks(
    [[0x0E, 0x0B, 0x0D, 0x09], [0x09, 0x0E, 0x0B, 0x0D], [0x0D, 0x09, 0x0E, 0x0B], [0x0B, 0x0D, 0x09, 0x0E]]
)


def earliest_depths(vals: set[int], n_inputs: int = 32, cap: int = 32) -> tuple[dict[int, int], set[int]]:
    lv: dict[int, int] = {1 << i: 0 for i in range(n_inputs)}
    rem = set(vals) - set(lv)
    for d in range(1, cap + 1):
        if not rem:
            break
        cur = list(lv.keys())
        newly: list[int] = []
        for v in list(rem):
            for a in cur:
                b = v ^ a
                if b in lv and b != a:
                    newly.append(v)
                    break
        if not newly:
            break
        for v in newly:
            lv[v] = d
            rem.remove(v)
    return lv, rem


def parse_xor_values(path: Path) -> set[int]:
    text = path.read_text(encoding="utf-8")
    basis = {f"x{i}": (1 << i) for i in range(32)}
    vals: set[int] = set()
    has_begin = any(rl.strip().lower().startswith("begin slp") for rl in text.splitlines())
    in_slp = not has_begin
    for raw in text.splitlines():
        line = raw.split("%", 1)[0].strip()
        if not line or line.startswith(("#", "//")):
            continue
        low = line.lower()
        if low.startswith("begin slp"):
            in_slp = True
            continue
        if low.startswith("end slp"):
            in_slp = False
            continue
        if not in_slp or low.startswith(("inputs:", "outputs:", "internal:", "gatesyntax:", "begin ", "end ")):
            continue
        toks = re.split(r"\s+", line)
        if len(toks) == 4 and toks[0].upper() == "XOR":
            _, ow, i1, i2 = toks
            basis[ow] = basis[i1] ^ basis[i2]
            vals.add(basis[ow])
    return vals


def solve_top2_milp(vals: set[int], targets: tuple[int, ...], depth_cap: int, time_limit: float = 10.0) -> dict[str, object]:
    lv, unres = earliest_depths(vals, 32, cap=depth_cap)
    if unres:
        raise ValueError(f"Unresolved masks at depth cap {depth_cap}: {len(unres)}")
    tset = set(targets)
    inputs = {1 << i for i in range(32)}

    p_list = sorted(m for m, l in lv.items() if l <= depth_cap - 2)
    p_set = set(p_list)
    base_gates = len(p_set - inputs)

    b_set: set[int] = set()
    for i, pi in enumerate(p_list):
        for j in range(i + 1, len(p_list)):
            m = pi ^ p_list[j]
            if m not in p_set and m != 0:
                b_set.add(m)
    b_list = sorted(b_set)
    b_idx = {m: idx for idx, m in enumerate(b_list)}

    rem_targets = [t for t in targets if t not in p_set]
    recipes_per_t = []
    used_b: set[int] = set()

    for t in rem_targets:
        recs: list[tuple[int, ...]] = []
        if t in b_idx:
            recs.append((b_idx[t],))
            used_b.add(b_idx[t])
        for p in p_list:
            b = t ^ p
            if b in b_idx and b != t:
                recs.append((b_idx[b],))
                used_b.add(b_idx[b])
        for b1 in b_list:
            b2 = t ^ b1
            if b2 > b1 and b2 in b_idx:
                i1, i2 = b_idx[b1], b_idx[b2]
                recs.append((i1, i2))
                used_b.add(i1)
                used_b.add(i2)
        recipes_per_t.append((t, sorted(set(recs))))

    active_b = sorted(used_b)
    remap = {old: new for new, old in enumerate(active_b)}
    n_b = len(active_b)

    r_slices = []
    cur = n_b
    for _, recs in recipes_per_t:
        r_slices.append((cur, len(recs), recs))
        cur += len(recs)
    n_vars = cur

    c = np.zeros(n_vars, dtype=float)
    for k, old_bi in enumerate(active_b):
        if b_list[old_bi] not in tset:
            c[k] = 1.0

    rows_i: list[int] = []
    cols_j: list[int] = []
    vals_v: list[float] = []
    lb: list[float] = []
    ub: list[float] = []
    row_idx = 0

    for start, length, recs in r_slices:
        for r_k in range(length):
            rows_i.append(row_idx)
            cols_j.append(start + r_k)
            vals_v.append(1.0)
        lb.append(1.0)
        ub.append(1.0)
        row_idx += 1

        by_bi: dict[int, list[int]] = {}
        for r_k, tup in enumerate(recs):
            for old_bi in tup:
                by_bi.setdefault(remap[old_bi], []).append(start + r_k)
        for m_bi, r_cols in by_bi.items():
            for rc in r_cols:
                rows_i.append(row_idx)
                cols_j.append(rc)
                vals_v.append(1.0)
            rows_i.append(row_idx)
            cols_j.append(m_bi)
            vals_v.append(-1.0)
            lb.append(-np.inf)
            ub.append(0.0)
            row_idx += 1

    mat_a = csc_matrix((vals_v, (rows_i, cols_j)), shape=(row_idx, n_vars))
    t0 = time.perf_counter()
    res = milp(
        c=c,
        integrality=np.ones(n_vars, dtype=int),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(mat_a, lb, ub),
        options={"time_limit": time_limit, "disp": False},
    )
    dt = time.perf_counter() - t0
    const_part = base_gates + len(rem_targets)
    opt_val = const_part + round(float(res.fun)) if res.success and res.fun is not None else None
    return {
        "orig_G": len(vals),
        "milp_opt_G": opt_val,
        "status": int(res.status),
        "P_size": len(p_list),
        "B_size": n_b,
        "vars": n_vars,
        "sec": round(dt, 4),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--circuit", type=Path, help="Path to 32-bit XOR NCFF circuit file")
    ap.add_argument("--func", choices=("mixcols", "invmixcols"), default="invmixcols")
    ap.add_argument("--depth", type=int, default=10)
    args = ap.parse_args()

    if args.circuit is not None:
        vals = parse_xor_values(args.circuit)
        tmasks = INVMIXCOLS_MASKS if args.func == "invmixcols" else MIXCOLS_MASKS
        print(solve_top2_milp(vals, tmasks, args.depth))
    else:
        print("Pass --circuit <file> --func {mixcols,invmixcols} --depth <D> to run Top-2-Layer HiGHS MILP.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
