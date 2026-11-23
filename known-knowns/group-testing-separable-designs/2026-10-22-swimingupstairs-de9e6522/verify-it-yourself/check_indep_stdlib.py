#!/usr/bin/env python3
"""Independent checker written at close-out from the OEIS A054961 wording:
"Maximal number of binary vectors of length n such that the unions (or bitwise ORs) of any 2 distinct vectors are all distinct."
Usage: check_indep_stdlib.py FILE n   (one vector per line, characters 0/1 only, each of length n)
Vectors are read as subsets of {0..n-1} (frozensets); the union of every unordered pair of distinct lines is formed
and all C(m,2) unions must differ. Last line: PASS or FAIL."""
import sys
from itertools import combinations
path, n = sys.argv[1], int(sys.argv[2])
lines = open(path, 'rb').read().decode('ascii').splitlines()
if not lines or any(len(l) != n or set(l) - {'0', '1'} for l in lines):
    print('format error'); print('FAIL'); sys.exit(1)
fam = [frozenset(i for i, c in enumerate(l) if c == '1') for l in lines]
if len(set(fam)) != len(fam):
    print('m=%d duplicate vectors' % len(fam)); print('FAIL'); sys.exit(1)
seen = {}
for a, b in combinations(range(len(fam)), 2):
    u = fam[a] | fam[b]
    if u in seen:
        print('m=%d collision: lines %s and %s have the same union' % (len(fam), seen[u], (a, b))); print('FAIL'); sys.exit(1)
    seen[u] = (a, b)
print('n=%d m=%d pairs=%d distinct_unions=%d' % (n, len(fam), len(fam) * (len(fam) - 1) // 2, len(seen)))
print('PASS')
