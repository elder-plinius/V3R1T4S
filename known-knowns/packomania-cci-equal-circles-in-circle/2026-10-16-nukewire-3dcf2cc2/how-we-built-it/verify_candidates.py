#!/usr/bin/env python
"""Exact verification of window candidates N=3307 and N=4141 against the bank criterion.

For each N:
  1. r* (mpmath, dps=50) of OUR candidate, computed from the saved coordinates alone
     (binding pairs/norms located in double, then recomputed at 50 digits).
  2. r* of the POSTED cciN.txt the same way, plus its margin vs the table row (integrity check).
  3. Isometry: sorted pairwise-distance multiset comparison (double precision; isometry-invariant).
  4. Table row read from data/radius.txt (fetched this run).

Usage (from the run root): python code/verify_candidates.py
"""
import sys
import numpy as np
from scipy.spatial import cKDTree
from mpmath import mp, mpf

mp.dps = 50


def load_xy(path):
    a = np.loadtxt(path)
    if a.shape[1] >= 3:
        a = a[:, 1:3]
    return a


def table_radius(n):
    for line in open("data/radius.txt"):
        p = line.split()
        if p and p[0] == str(n):
            return p[1]
    raise KeyError(n)


def exact_rstar(coords):
    """Feasible radius at dps=50: locate binding pairs/norms in double, confirm at 50 digits."""
    tree = cKDTree(coords)
    d2, _ = tree.query(coords, k=2)
    dmin = float(d2[:, 1].min())
    pairs = tree.query_pairs(r=dmin * (1 + 1e-9), output_type="ndarray")
    norms = np.hypot(coords[:, 0], coords[:, 1])
    nmax = float(norms.max())
    nidx = np.where(norms > nmax * (1 - 1e-9))[0]

    def P(i):
        return mpf(repr(float(coords[i][0]))), mpf(repr(float(coords[i][1])))

    hp_min = min(((P(i)[0] - P(j)[0]) ** 2 + (P(i)[1] - P(j)[1]) ** 2).sqrt() for i, j in pairs)
    hp_max = max((P(i)[0] ** 2 + P(i)[1] ** 2).sqrt() for i in nidx)
    return min(hp_min / 2, mpf(1) - hp_max), len(pairs), len(nidx)


def sorted_multiset(coords, chunk=256):
    N = len(coords)
    out = []
    for i in range(0, N, chunk):
        d = coords[i:i + chunk, None, :] - coords[None, :, :]
        dist = np.hypot(d[..., 0], d[..., 1])
        rows = np.arange(i, i + d.shape[0])
        dist[np.arange(d.shape[0]), rows] = np.inf
        out.append(np.sort(dist[dist < np.inf].ravel()))
    # merge chunks
    return np.sort(np.concatenate(out))


def main():
    ok = True
    for N in (3307, 4141):
        rt = mpf(table_radius(N))
        ours = load_xy(f"attempts/symmetry/candidate_N{N}.txt")
        post = load_xy(f"data/cci{N}.txt")
        r_ours, npair, nnorm = exact_rstar(ours)
        r_post, npair2, nnorm2 = exact_rstar(post)
        print(f"N={N}: table={mp.nstr(rt, 31)}")
        print(f"  OUR window   r*={mp.nstr(r_ours, 31)}  margin={mp.nstr(r_ours - rt, 4)} "
              f"({npair} binding pairs, {nnorm} binding norms)")
        print(f"  POSTED cci{N}  r*={mp.nstr(r_post, 31)}  margin_vs_table={mp.nstr(r_post - rt, 4)} "
              f"({npair2} binding pairs, {nnorm2} binding norms)")
        mo = sorted_multiset(ours)
        mp_ = sorted_multiset(post)
        if mo.shape != mp_.shape:
            print(f"  ISOMETRY: distance counts differ ({mo.shape[0]} vs {mp_.shape[0]}) -> NON-ISOMETRIC")
        else:
            dmax = float(np.abs(mo - mp_).max())
            frac = float((np.abs(mo - mp_) > 1e-9).mean())
            verdict = "ISOMETRIC" if frac < 1e-6 else "NON-ISOMETRIC"
            print(f"  ISOMETRY: max|multiset diff|={dmax:.3e}, fraction>1e-9: {frac:.4f} -> {verdict}")
        if not (r_ours - rt >= mpf("1e-11")):
            print("  FAIL: margin below 1e-11")
            ok = False
    print("VERIFY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
