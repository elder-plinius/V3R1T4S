"""Build a seed for N from the best found packing of N+1 (delete one ball) or N-1 (insert one ball).

usage: python3 chain.py N resultsdir seed out.npy
"""
import sys, glob, os
import numpy as np


def best_for(n, d):
    best, bx = -1, None
    for f in glob.glob(os.path.join(d, f"{n}_*.npy")):
        x = np.load(f)
        dif = x[:, None] - x[None]
        dd = np.sqrt((dif ** 2).sum(-1)); dd[np.diag_indices(len(x))] = 9
        D = dd.min()
        if D > best:
            best, bx = D, x
    return bx, best


n = int(sys.argv[1]); d = sys.argv[2]; seed = int(sys.argv[3]); out = sys.argv[4]
rng = np.random.default_rng(seed)
up, Du = best_for(n + 1, d)
dn, Dd = best_for(n - 1, d)
ru = Du / (2 + Du) if up is not None else -1
rd = Dd / (2 + Dd) if dn is not None else -1
use_up = up is not None and (dn is None or rng.random() < 0.6)
if use_up:
    i = rng.integers(len(up))
    x = np.delete(up, i, axis=0)
else:
    # insert at the probe point farthest from all centres
    p = rng.standard_normal((20000, 4))
    p /= np.linalg.norm(p, axis=1)[:, None]
    p *= rng.uniform(0, 1, (20000, 1)) ** 0.25
    dist = np.sqrt(((p[:, None] - dn[None]) ** 2).sum(-1)).min(1)
    k = int(os.environ.get('HOLE_TOPK', '1'))
    top = np.argsort(dist)[::-1][:k]
    x = np.vstack([dn, p[rng.choice(top)]])
np.save(out, x)
print("from", "N+1" if use_up else "N-1", ru if use_up else rd)
