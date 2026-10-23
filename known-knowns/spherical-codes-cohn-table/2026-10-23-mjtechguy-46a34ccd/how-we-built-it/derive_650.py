#!/usr/bin/env python3
"""Derive a (25, 650) code from object/651.txt of package 2026-10-23-mjtechguy-23ad10a0 by deleting one point.
Candidates: every endpoint of the 20 largest pairwise inner products (float64 screen). Each candidate deletion is
scored by the max inner product over the remaining 650 points (float64 screen, then mpmath 50 digits on the top
pairs within 1e-7 of the float max). The deletion with the smallest mpmath maximum wins. The kept lines are copied
byte-for-byte from the 651 file. Usage: derive_650.py <651.txt> <out_650.txt>"""
import sys, json
import numpy as np
import mpmath as mp
mp.mp.dps = 50
src, out = sys.argv[1], sys.argv[2]
lines = [l.rstrip("\n") for l in open(src) if l.strip()]
X = np.array([[float(t) for t in l.split(",")] for l in lines])
X /= np.linalg.norm(X, axis=1, keepdims=True)
G = X @ X.T
iu = np.triu_indices(len(X), 1)
vals = G[iu]
order = np.argsort(-vals)[:20]
cands = sorted({int(iu[0][k]) for k in order} | {int(iu[1][k]) for k in order})
U = None
def mpunit(i):
    v = [mp.mpf(t) for t in lines[i].split(",")]
    n = mp.sqrt(mp.fsum(x * x for x in v))
    return [x / n for x in v]
cache = {}
def mpdot(i, j):
    for k in (i, j):
        if k not in cache: cache[k] = mpunit(k)
    return mp.fsum(a * b for a, b in zip(cache[i], cache[j]))
res = []
for k in cands:
    H = np.delete(np.delete(G, k, 0), k, 1)
    keep = [i for i in range(len(X)) if i != k]
    a, b = np.triu_indices(len(keep), 1)
    hv = H[a, b]
    fmax = hv.max()
    near = np.nonzero(hv >= fmax - 1e-7)[0]
    best = max(mpdot(keep[a[t]], keep[b[t]]) for t in near)
    res.append((best, k, float(fmax), len(near)))
res.sort()
best, k, fmax, nn = res[0]
with open(out, "w") as f:
    for i, l in enumerate(lines):
        if i != k: f.write(l + "\n")
print(json.dumps({"deleted_zero_based": k, "deleted_line_one_based": k + 1, "mp_max": mp.nstr(best, 50),
                  "float_max": fmax, "candidates": [(c, mp.nstr(b, 20)) for b, c, _, _ in res]}, indent=1))
