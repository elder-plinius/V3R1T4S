"""Exhaustive restriction: for an N-assignment and target m, count the full domain of the restriction to EVERY
m-subset of alternatives (exact DP, cdlib.count), report the best few and save the best restriction.
Usage: python restrict_exh.py N in.npy m out.npy [MAXSUBSETS]"""
import sys, os, itertools
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdlib
N = int(sys.argv[1]); cond = np.load(sys.argv[2]); m = int(sys.argv[3]); outp = sys.argv[4]
mx = int(sys.argv[5]) if len(sys.argv) > 5 else 200000
if comb(N, m) > mx: print('too many subsets', comb(N, m)); sys.exit(1)
P = np.array(list(itertools.combinations(range(m), 3)), dtype=np.int64)  # positions i<j<k, in colex order? sort below
key = np.array([comb(k, 3) + comb(j, 2) + i for i, j, k in P]); P = P[np.argsort(key)]
C3 = np.array([comb(v, 3) for v in range(N)]); C2 = np.array([comb(v, 2) for v in range(N)])
res = []
for S in itertools.combinations(range(N), m):
    S = np.array(S); a, b, c = S[P[:, 0]], S[P[:, 1]], S[P[:, 2]]
    r = np.ascontiguousarray(cond[C3[c] + C2[b] + a], dtype=np.uint8)
    res.append((cdlib.count(m, r), tuple(S.tolist())))
res.sort(reverse=True)
print('source N', N, 'm', m, 'subsets', len(res), 'best', res[0][0], 'top5', [v for v, _ in res[:5]], 'subset', res[0][1], flush=True)
S = np.array(res[0][1]); np.save(outp, np.ascontiguousarray(cond[C3[S[P[:, 2]]] + C2[S[P[:, 1]]] + S[P[:, 0]]], dtype=np.uint8))
