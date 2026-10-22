"""f(p) via up-sets (fast; float guide). Same model and output as fmax.py, which uses LPs.
usage: python fmax2.py <gate3 table> [...]
"""
import sys

import numpy as np

from fmax import load
from upsets import matrix


def fvals(laws, m=5, tol=1e-6):
    U, M = matrix(m)
    Mf = M.astype(float)
    P = laws @ Mf.T
    k = np.array([bin(x).count("1") for x in range(1 << m)])
    lo = np.zeros(len(laws))
    hi = np.ones(len(laws))
    while (hi - lo).max() > tol:
        mid = (lo + hi) / 2
        Q = (mid[:, None] ** k[None, :] * (1 - mid[:, None]) ** (m - k[None, :])) @ Mf.T
        ok = (P >= Q - 1e-15).all(axis=1)
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    return lo


def main():
    for fn in sys.argv[1:]:
        head, laws = load(fn)
        keys = [k for k, _ in laws]
        L = np.array([l for _, l in laws])
        v = fvals(L)
        i = int(np.argmin(v))
        print("%s: f(p) = %.5f at entry %s" % (head, v[i], keys[i]))


if __name__ == "__main__":
    main()
