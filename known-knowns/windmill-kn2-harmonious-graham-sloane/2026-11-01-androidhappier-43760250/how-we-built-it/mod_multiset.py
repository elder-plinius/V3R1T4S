#!/usr/bin/env python3
"""mod_multiset.py d  -- does the mod-d obstruction need the Sidon (distinct-sums) property at all?
Reduce labels mod d (d | 56). Each residue class mod d holds 56/d labels of Z_56, and the 56 edge sums must hit each
class mod d exactly 56/d times. Enumerate all multisets X (clique A incl. the shared label 0) and Y (clique B incl. 0)
of size 8 over Z_d with class multiplicity <= 56/d, combined X[r]+Y[r] <= 56/d (+1 for r = 0, the shared vertex counted
in both), and test whether their pair-sum class counts add to 56/d in every class."""
import sys, itertools
from collections import defaultdict
d = int(sys.argv[1]); q = 56; cap = q // d
def multisets(size, d, cap):
    def rec(r, left, cur):
        if r == d - 1:
            if left <= cap: yield cur + [left]
            return
        for c in range(min(cap, left) + 1):
            yield from rec(r + 1, left - c, cur + [c])
    yield from rec(0, size, [])
def sumvec(X):
    v = [0]*d
    for a in range(d):
        if X[a] >= 2: v[(2*a) % d] += X[a]*(X[a]-1)//2
        for b in range(a+1, d):
            v[(a+b) % d] += X[a]*X[b]
    return tuple(v)
Ms = [X for X in multisets(8, d, cap) if X[0] >= 1]
by = defaultdict(list)
for X in Ms: by[sumvec(X)].append(X)
pairs = 0
for X in Ms:
    need = tuple(cap - x for x in sumvec(X))
    for Y in by.get(need, ()):
        if all(X[r] + Y[r] <= cap + (1 if r == 0 else 0) for r in range(d)):
            pairs += 1
print(f"d={d}: multisets with 0 = {len(Ms)}, compatible ordered pairs (no Sidon condition) = {pairs}")
