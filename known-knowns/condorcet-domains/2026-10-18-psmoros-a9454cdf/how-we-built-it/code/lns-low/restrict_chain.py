"""Exhaustive restrictions (every m-subset, m = 14, 15, 16, if at most 60000 subsets) of every assignment written by
this lens's chains (out/chain*/n<N>_*.npy, N >= 15). Prints per file; saves global best per m to
out/restrict/chain_best_m<m>.npy."""
import sys, os, itertools, glob, re
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdlib
L = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
best = {}
files = sorted(glob.glob(os.path.join(L, 'out/chain*/n*_*.npy')))
for path in files:
    N = int(re.match(r'n(\d+)_', os.path.basename(path)).group(1))
    if N < 15: continue
    cond = np.load(path); C3 = np.array([comb(v, 3) for v in range(N)]); C2 = np.array([comb(v, 2) for v in range(N)])
    out = [f'self:{cdlib.count(N, cond)}']
    for m in (16, 15, 14):
        if m >= N or comb(N, m) > 60000: continue
        P = np.array(list(itertools.combinations(range(m), 3)), dtype=np.int64)
        key = np.array([comb(k, 3) + comb(j, 2) + i for i, j, k in P]); P = P[np.argsort(key)]
        bv, bS = -1, None
        for S in itertools.combinations(range(N), m):
            S = np.array(S); v = cdlib.count(m, np.ascontiguousarray(cond[C3[S[P[:, 2]]] + C2[S[P[:, 1]]] + S[P[:, 0]]], dtype=np.uint8))
            if v > bv: bv, bS = v, S
        out.append(f'{m}:{bv}')
        if bv > best.get(m, (0,))[0]:
            best[m] = (bv, os.path.relpath(path, L), tuple(bS.tolist()))
            np.save(os.path.join(L, f'out/restrict/chain_best_m{m}.npy'), np.ascontiguousarray(cond[C3[bS[P[:, 2]]] + C2[bS[P[:, 1]]] + bS[P[:, 0]]], dtype=np.uint8))
    print(os.path.relpath(path, L), ' '.join(out), flush=True)
print('GLOBAL BEST', best, flush=True)
