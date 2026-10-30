#!/usr/bin/env python3
"""Rebuild step 2 of the route: split every coefficient of absolute value 2 or more in the rank-1540 integer scheme
into ternary parts, giving a ternary scheme of rank 1548. Standard library only.

Usage (from the package folder):
  python3 -I how-we-built-it/rebuild_split.py how-we-built-it/start/11x14x16_m1540_Z.json OUT.json

The split rule is the one in tools/run_q_upgrades.py (split_vec_ternary, fast_split_to_zt): a vector x with
max |x_i| = a > 1 is written as the sum of a ternary vectors, the first being sign(x), the next sign(x - sign(x)), and so
on; a term (u, v, w) is replaced by every product of the parts of u, v and w, in that loop order. OUT.json is written in
dense rows, the input format of tools/zt_flip_reduce.c (through run_c_opt); check it with
  python3 -I verify-it-yourself/check_fmm_fast.py OUT.json --expect-rank 1548 --expect-class ZT
"""
import json
import sys


def dense(d):
    n1, n2, n3 = d["n"]
    size = {"u": n1 * n2, "v": n2 * n3, "w": n3 * n1}
    out = {}
    for key in ("u", "v", "w"):
        rows = []
        for row in d[key]:
            if d.get("encoding") == "sparse_flat_pairs":
                r = [0] * size[key]
                for i in range(0, len(row), 2):
                    r[row[i]] = row[i + 1]
                rows.append(r)
            else:
                rows.append(list(row))
        out[key] = rows
    return out


def split_vec_ternary(vec):
    if max((abs(x) for x in vec), default=0) <= 1:
        return [list(vec)]
    parts, cur = [], list(vec)
    while any(cur):
        step = [1 if x > 0 else (-1 if x < 0 else 0) for x in cur]
        parts.append(step)
        cur = [a - b for a, b in zip(cur, step)]
    return parts


def main():
    src, dst = sys.argv[1], sys.argv[2]
    d = json.load(open(src))
    rows = dense(d)
    U, V, W, changed = [], [], [], 0
    for u, v, w in zip(rows["u"], rows["v"], rows["w"]):
        pu, pv, pw = split_vec_ternary(u), split_vec_ternary(v), split_vec_ternary(w)
        if len(pu) * len(pv) * len(pw) > 1:
            changed += 1
        for a in pu:
            for b in pv:
                for c in pw:
                    U.append(a); V.append(b); W.append(c)
    json.dump({"n": d["n"], "m": len(U), "u": U, "v": V, "w": W}, open(dst, "w"), separators=(",", ":"))
    print(f"input rank {len(rows['u'])}; terms with a coefficient of absolute value 2 or more: {changed}; "
          f"rank after the ternary split: {len(U)}")


if __name__ == "__main__":
    main()
