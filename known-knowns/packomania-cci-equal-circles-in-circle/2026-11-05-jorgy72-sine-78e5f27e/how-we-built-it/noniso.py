#!/usr/bin/env python3
"""Non-isometry check: compare sorted pairwise-distance multisets of the
candidate against the posted seed (numpy, float64).

Usage: python3 noniso.py candidate.txt seed.txt
Prints sizes, max/mean abs difference of the sorted multisets, and whether
they are identical. A max difference far above 1e-9 rules out any isometry
(rotation, reflection, translation, relabelling).
"""
import sys
import numpy as np


def load(path):
    pts = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) >= 3:
                pts.append((float(p[1]), float(p[2])))
    return np.array(pts)


def multiset(P):
    n = len(P)
    out = []
    for i0 in range(0, n, 500):
        A = P[i0:i0 + 500]
        D = np.sqrt(((A[:, None, :] - P[None, :, :]) ** 2).sum(axis=2))
        for k, i in enumerate(range(i0, min(i0 + 500, n))):
            out.append(D[k, i + 1:])
    return np.sort(np.concatenate(out))


a = multiset(load(sys.argv[1]))
b = multiset(load(sys.argv[2]))
print('sizes: %d %d' % (len(a), len(b)))
print('max abs multiset diff: %.6e' % np.max(np.abs(a - b)))
print('mean abs diff: %.6e' % np.mean(np.abs(a - b)))
print('identical multisets:', bool(np.array_equal(a, b)))
