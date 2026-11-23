# Independent checker for A326336 from OEIS definition.
# Blocks A,B capture iff exist x<y in one, z<t in other, x<z<t<y or z<x<y<t.
# Fast form: A captures B iff |B ∩ (minA,maxA)| >= 2 (or vice versa).
import sys, itertools
from itertools import combinations
def partitions(n):
    # restricted growth strings
    def rec(i, rgs, m):
        if i == n:
            yield rgs[:]; return
        for b in range(m+1):
            rgs.append(b); yield from rec(i+1, rgs, max(m, b+1)); rgs.pop()
    if n == 0: yield []; return
    yield from rec(0, [], 0)
def blocks_of(rgs):
    bl = {}
    for i, b in enumerate(rgs): bl.setdefault(b, []).append(i+1)
    return list(bl.values())
def cap_fast(A, B):
    lo, hi = A[0], A[-1]
    if sum(1 for z in B if lo < z < hi) >= 2: return True
    lo, hi = B[0], B[-1]
    return sum(1 for z in A if lo < z < hi) >= 2
def cap_literal(A, B):
    for x, y in combinations(A, 2):
        for z, t in combinations(B, 2):
            if x < z < t < y or z < x < y < t: return True
    return False
def connected(bl, cap):
    k = len(bl)
    if k <= 1: return True
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for v in range(k):
            if v not in seen and cap(bl[u], bl[v]):
                seen.add(v); st.append(v)
    return len(seen) == k
def a(n, cap):
    return sum(1 for r in partitions(n) if connected(blocks_of(r), cap))
N = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else 'fast'
cap = cap_fast if mode == 'fast' else cap_literal
for n in range(N+1): print(n, a(n, cap), flush=True)
