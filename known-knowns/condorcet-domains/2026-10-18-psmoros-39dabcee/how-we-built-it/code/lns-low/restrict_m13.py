"""Exhaustive restrictions to every m-subset for small m (13, 12, 11) from the best n = 14, 15, 16 domains of this
lens and the best wave-1 restriction sources (n = 17 300388, n = 18 658240). One process."""
import sys, os, itertools
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdlib
L = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = {11: 2452, 12: 5520, 13: 12182}
srcs = [(14, 'rec/n14_27040.npy'), (15, 'rec/n15_60956.npy'), (16, 'rec/n16_135072.npy'), (16, 'rec/n16_131745_ls.npy'),
        (15, 'rec/n15_60154.npy'), (18, '../local-search/out/chain17/n18_lns.npy')]
for N, path in srcs:
    cond = np.load(os.path.join(L, path)); C3 = np.array([comb(v, 3) for v in range(N)]); C2 = np.array([comb(v, 2) for v in range(N)])
    out = []
    for m in (13, 12, 11):
        if comb(N, m) > 40000: out.append(f'{m}:skip'); continue
        P = np.array(list(itertools.combinations(range(m), 3)), dtype=np.int64)
        key = np.array([comb(k, 3) + comb(j, 2) + i for i, j, k in P]); P = P[np.argsort(key)]
        bv = max(cdlib.count(m, np.ascontiguousarray(cond[C3[S[P[:, 2]]] + C2[S[P[:, 1]]] + S[P[:, 0]]], dtype=np.uint8))
                 for S in map(np.array, itertools.combinations(range(N), m)))
        out.append(f'{m}:{bv}(rec {REC[m]})')
    print(N, path, ' '.join(out), flush=True)
