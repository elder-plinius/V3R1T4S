#!/usr/bin/env python3
"""Compare per-graph maxima of Program A and Program B part files; print totals, mismatches, global max and argmax."""
import sys, glob
def load(pat):
    d = {}
    for f in sorted(glob.glob(pat)):
        for line in open(f):
            p = line.split()
            if len(p) == 2 and not line.startswith(('n=', 'hist')):
                assert p[0] not in d, ('duplicate', p[0]); d[p[0]] = int(p[1])
    return d
A = load(sys.argv[1]); B = load(sys.argv[2])
print('graphs_A', len(A), 'graphs_B', len(B), 'same_keys', set(A) == set(B))
mm = [g for g in A if A[g] != B.get(g)]
print('mismatches', len(mm), mm[:5])
M = max(A.values()); print('max_A', M, 'max_B', max(B.values()))
print('argmax_A', [g for g in A if A[g] == M], 'argmax_B', [g for g in B if B[g] == max(B.values())])
top = sorted(set(A.values()))[-6:]; print('top values', top, 'counts', [sum(1 for v in A.values() if v == t) for t in top])
