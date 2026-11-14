#!/usr/bin/env python
"""Exact verification of the N=3307 window candidate against the bank criterion.

Same evidence structure as the N=4141 claim: r* at >= 50 significant digits from the submitted
coordinate strings (binding pairs/norms located in double via scipy KDTree, recomputed exactly
with decimal at 60 digits from the strings); posted-config integrity; sorted-distance-multiset
non-isometry. Table row read from data/radius.txt (fetched this run).

Usage (from the run root): python code/verify_N3307.py
"""
import sys
from decimal import Decimal, getcontext

import numpy as np
from scipy.spatial import cKDTree

getcontext().prec = 60
N = 3307


def load_xy_strings(path):
    rows = []
    for line in open(path):
        s = line.split()
        if len(s) >= 2:
            rows.append((s[-2], s[-1]))  # last two tokens: handles "index x y" and "x y"
    return rows


def table_row(n):
    for line in open("data/radius.txt"):
        p = line.split()
        if p and p[0] == str(n):
            return p[1]
    raise KeyError(n)


def exact_rstar(strs):
    fx = np.array([float(x) for x, _ in strs])
    fy = np.array([float(y) for _, y in strs])
    coords = np.stack([fx, fy], axis=1)
    tree = cKDTree(coords)
    d2, _ = tree.query(coords, k=2)
    dmin = float(d2[:, 1].min())
    pairs = tree.query_pairs(r=dmin * (1 + 1e-9), output_type="ndarray")
    norms = np.hypot(fx, fy)
    nmax = float(norms.max())
    nidx = np.where(norms > nmax * (1 - 1e-9))[0]

    def P(i):
        return Decimal(strs[i][0]), Decimal(strs[i][1])

    hp_min = min(((P(i)[0] - P(j)[0]) ** 2 + (P(i)[1] - P(j)[1]) ** 2).sqrt() for i, j in pairs)
    hp_max = max((P(k)[0] ** 2 + P(k)[1] ** 2).sqrt() for k in nidx)
    return min(hp_min / 2, Decimal(1) - hp_max), len(pairs), len(nidx)


def sorted_multiset(path, chunk=256):
    a = np.loadtxt(path)
    if a.shape[1] >= 3:
        a = a[:, 1:3]
    out = []
    for i in range(0, len(a), chunk):
        d = a[i:i + chunk, None, :] - a[None, :, :]
        dist = np.hypot(d[..., 0], d[..., 1])
        rows = np.arange(i, i + d.shape[0])
        dist[np.arange(d.shape[0]), rows] = np.inf
        out.append(np.sort(dist[dist < np.inf].ravel()))
    return np.sort(np.concatenate(out))


def main():
    rt = Decimal(table_row(N))
    ours = load_xy_strings("attempts/symmetry/result/candidate_N3307.txt")
    print(f"our candidate: {len(ours)} centres (expected {N})")
    r_ours, npair, nnorm = exact_rstar(ours)
    print(f"OUR r* (decimal 60, from strings) = {r_ours}")
    print(f"  binding pairs {npair}, binding norms {nnorm}")
    print(f"table row {N}                      = {rt}")
    print(f"margin = {r_ours - rt}  (threshold 1e-11)")

    posted = load_xy_strings(f"data/cci{N}.txt")
    r_post, _, _ = exact_rstar(posted)
    print(f"POSTED cci{N} r* (string-exact)     = {r_post}  diff vs own row = {r_post - rt:.3e}")

    mo = sorted_multiset("attempts/symmetry/result/candidate_N3307.txt")
    mp = sorted_multiset(f"data/cci{N}.txt")
    assert mo.shape == mp.shape, "distance counts differ"
    frac = float((np.abs(mo - mp) > 1e-9).mean())
    print(f"isometry: max|multiset diff| = {float(np.abs(mo - mp).max()):.3e}, fraction>1e-9 = {frac:.4f}"
          f" -> {'NON-ISOMETRIC' if frac > 1e-6 else 'ISOMETRIC'}")
    ok = len(ours) == N and (r_ours - rt) >= Decimal("1e-11") and frac > 1e-6 and abs(r_post - rt) < Decimal("1e-20")
    print("VERIFY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
