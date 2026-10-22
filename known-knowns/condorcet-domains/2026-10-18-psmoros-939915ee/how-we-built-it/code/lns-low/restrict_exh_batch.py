"""Exhaustive restrictions (every m-subset, m = 14, 15, 16) of selected wave-1 sources (one process).
Sources: all n = 18 and n = 19 entries of out/restrict/sources.txt, and the top 4 by count for n = 20 and 21.
Saves the global best per m as out/restrict/exh_best_m<m>.npy; prints one line per (source, m)."""
import sys, os, itertools
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdlib
L = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srcs = [l.split() for l in open(os.path.join(L, 'out/restrict/sources.txt'))]
sel = [s for s in srcs if s[0] in ('18', '19')]
for n in ('20', '21'): sel += sorted([s for s in srcs if s[0] == n], key=lambda s: -int(s[1]))[:4]
best = {}
for n, c, path in sel:
    N = int(n); cond = np.load(os.path.join(L, '..', path))
    C3 = np.array([comb(v, 3) for v in range(N)]); C2 = np.array([comb(v, 2) for v in range(N)])
    out = []
    for m in (16, 15, 14):
        P = np.array(list(itertools.combinations(range(m), 3)), dtype=np.int64)
        key = np.array([comb(k, 3) + comb(j, 2) + i for i, j, k in P]); P = P[np.argsort(key)]
        bv, bS = -1, None
        for S in itertools.combinations(range(N), m):
            S = np.array(S); r = np.ascontiguousarray(cond[C3[S[P[:, 2]]] + C2[S[P[:, 1]]] + S[P[:, 0]]], dtype=np.uint8)
            v = cdlib.count(m, r)
            if v > bv: bv, bS = v, S
        out.append(f'{m}:{bv}')
        if bv > best.get(m, (0,))[0]:
            best[m] = (bv, path, tuple(bS.tolist()))
            np.save(os.path.join(L, f'out/restrict/exh_best_m{m}.npy'), np.ascontiguousarray(cond[C3[bS[P[:, 2]]] + C2[bS[P[:, 1]]] + bS[P[:, 0]]], dtype=np.uint8))
    print(n, c, path, ' '.join(out), flush=True)
print('GLOBAL BEST', best, flush=True)
