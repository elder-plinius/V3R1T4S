#!/usr/bin/env python3
"""usage: diff_AB.py "A9_part*.txt" "B9_part*.txt"
Compare Program A (totA self) and Program B (totB.go) graph by graph for n = 9: same graph set, same per-graph
maximum, same histogram, same overall maximum; list every graph reaching the overall maximum."""
import glob, collections
def load(pat):
    d = {}
    for f in sorted(glob.glob(pat)):
        for l in open(f):
            if l.startswith('G '):
                _, g, m = l.split()
                assert g not in d, ('duplicate', g)
                d[g] = int(m)
    return d
import sys
A = load(sys.argv[1]); B = load(sys.argv[2])
print('A graphs', len(A), 'B graphs', len(B), 'same graph set', set(A) == set(B))
mism = [g for g in A if A.get(g) != B.get(g)]
print('per-graph mismatches', len(mism), mism[:5])
hA = collections.Counter(A.values()); hB = collections.Counter(B.values())
print('histograms identical', hA == hB)
M = max(A.values()); print('max A', M, 'max B', max(B.values()))
print('graphs reaching max', [g for g in A if A[g] == M])
print('top values', sorted(hA.items())[-8:])
