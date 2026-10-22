"""Restriction (deletion) search: from an N-assignment, delete alternatives one at a time (beam over subsets),
counting the full domain of each restricted assignment by the exact subset DP (cdlib.count). Reports the best count
for every m < N down to 9 and saves the best restricted assignment per m.
Usage: python restrict.py N in.npy BEAM out_prefix"""
import sys, os, itertools
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdlib
N = int(sys.argv[1]); cond = np.load(sys.argv[2]); B = int(sys.argv[3]); outp = sys.argv[4]; MMIN = int(sys.argv[5]) if len(sys.argv) > 5 else 9
REC = {9: 492, 10: 1104, 11: 2452, 12: 5520, 13: 12182, 14: 27026, 15: 59430, 16: 131536, 17: 292015, 18: 649079,
       19: 1432836, 20: 3155366, 21: 6674931, 22: 15037178, 23: 33162136, 24: 73279872}
def restrict(S):
    S = sorted(S); m = len(S); out = np.empty(comb(m, 3), dtype=np.uint8)
    for (i, a), (j, b), (k, c) in itertools.combinations(enumerate(S), 3):
        out[comb(k, 3) + comb(j, 2) + i] = cond[comb(c, 3) + comb(b, 2) + a]
    return out
beam = [frozenset(range(N))]
print('source n', N, 'count', cdlib.count(N, cond), flush=True)
for m in range(N - 1, MMIN - 1, -1):
    cand = {}
    for S in beam:
        for x in S:
            T = S - {x}
            if T in cand: continue
            cand[T] = cdlib.count(m, restrict(T))
    beam = sorted(cand, key=lambda T: -cand[T])[:B]
    best = beam[0]; bv = cand[best]
    np.save(f'{outp}_m{m}.npy', restrict(best))
    print(f'm {m} best {bv} record {REC.get(m)} {"ABOVE" if bv > REC.get(m, 1 << 62) else ""} subset {sorted(best)}', flush=True)
