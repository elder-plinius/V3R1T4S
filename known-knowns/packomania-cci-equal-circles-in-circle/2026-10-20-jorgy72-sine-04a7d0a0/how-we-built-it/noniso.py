#!/usr/bin/env python3
"""Non-isometry check: compare sorted pairwise-distance multisets (float64)
of a candidate vs the posted seed. Differ -> non-isometric."""
import numpy as np, sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import load, RUN


def dist_multiset(P):
    n = len(P)
    ds = np.empty(n * (n - 1) // 2)
    k = 0
    bs = 700
    for i0 in range(0, n, bs):
        A = P[i0:i0 + bs]
        D = np.linalg.norm(A[:, None, :] - P[None, :, :], axis=2)
        for a, i in enumerate(range(i0, min(i0 + bs, n))):
            row = D[a, i + 1:]
            ds[k:k + len(row)] = row
            k += len(row)
    ds.sort()
    return ds


if __name__ == '__main__':
    cand_path = sys.argv[1]
    t = time.time()
    seed = load(RUN + '/data/cci3949.txt')
    cand = load(cand_path)
    assert len(seed) == len(cand) == 3949
    ms = dist_multiset(seed)
    mc = dist_multiset(cand)
    diff = np.abs(ms - mc)
    print('max|d_seed - d_cand| sorted = %.3e' % diff.max())
    print('mean abs diff = %.3e' % diff.mean())
    print('num pairs differing by >1e-9: %d / %d'
          % ((diff > 1e-9).sum(), len(diff)))
    print('NON-ISOMETRIC' if diff.max() > 1e-9 else 'ISOMETRIC (or too close)')
    print('time %.1fs' % (time.time() - t))
