"""Run restrict.py logic on every source in out/restrict/sources.txt (n count path), beam B, down to m = 14;
one process (imports restrict functions inline). Prints best per (source, m) and the global best per m; saves the
global best restricted assignment per m to out/restrict/batch_best_m<m>.npy."""
import sys, os, itertools
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdlib
B = int(sys.argv[1]); L = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srcs = [l.split() for l in open(os.path.join(L, 'out/restrict/sources.txt'))]
best = {}
for n, c, path in srcs:
    N = int(n); cond = np.load(os.path.join(L, '..', path) if not path.startswith('/') else path)
    def restrict(S):
        S = sorted(S); m = len(S); out = np.empty(comb(m, 3), dtype=np.uint8)
        for (i, a), (j, b), (k, cc) in itertools.combinations(enumerate(S), 3):
            out[comb(k, 3) + comb(j, 2) + i] = cond[comb(cc, 3) + comb(b, 2) + a]
        return out
    beam = [frozenset(range(N))]; line = []
    for m in range(N - 1, 13, -1):
        cand = {}
        for S in beam:
            for x in S:
                T = S - {x}
                if T not in cand: cand[T] = cdlib.count(m, restrict(T))
        beam = sorted(cand, key=lambda T: -cand[T])[:B]; bv = cand[beam[0]]
        if m <= 17: line.append(f'{m}:{bv}')
        if bv > best.get(m, (0,))[0]:
            best[m] = (bv, path); np.save(os.path.join(L, f'out/restrict/batch_best_m{m}.npy'), restrict(beam[0]))
    print(n, c, path, ' '.join(line), flush=True)
print('GLOBAL BEST', {m: best[m] for m in sorted(best)}, flush=True)
