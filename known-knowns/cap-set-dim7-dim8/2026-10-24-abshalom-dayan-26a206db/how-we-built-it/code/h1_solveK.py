"""Exact max cap inside K = F_3^n \\ -(X + M X) for given sign diagonals / monomials (from h1_monomial output)."""
import numpy as np, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framelib import *
n = int(sys.argv[1])
X = load(RUN + ('/checker/record_512_n8.txt' if n == 8 else '/checker/record_236_n7.txt'), n)
for spec in sys.argv[2:]:
    if spec.startswith('diag'):
        M = np.diag([int(c) for c in spec[4:]])
    else:
        p, s = spec[4:].split('s'); p = [int(c) for c in p]; s = [int(c) for c in s]
        M = np.zeros((n, n), np.int64); M[np.arange(n), p] = s
    Y = (X @ M.T) % 3
    K = np.flatnonzero(K_of(X, Y))
    st, sz, bnd, ch = maxcap_in(K, n, time_limit=120, workers=2)
    # weights of K points and their structure
    V = dec(K, n)
    w = (V != 0).sum(1)
    print(spec, '|K|=', len(K), 'maxcap', st, sz, 'bound', bnd, 'weights', dict(zip(*np.unique(w, return_counts=True))), flush=True)
    print('  frame total', 2 * len(X), '+', sz, '=', 2 * len(X) + sz, flush=True)
