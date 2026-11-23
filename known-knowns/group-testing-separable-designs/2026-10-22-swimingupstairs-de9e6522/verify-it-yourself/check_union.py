"""check_union.py FILE n k  (Python 3 standard library only)
FILE: binary vectors, one per line, characters 0/1 only (blank lines allowed). Any other character -> INVALID.
Checks: every vector has length n, all vectors distinct, and the bitwise ORs of all unordered k-subsets of distinct
vectors are pairwise distinct (k=2: OEIS A054961; k=3: OEIS A290492). Prints VALID or INVALID on the last line."""
import sys, itertools
f, n, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
txt = open(f).read()
bad = sorted(set(c for c in txt if c not in '01\n'))
V = [l for l in txt.split('\n') if l != '']
ok = all(len(v) == n for v in V)
X = [int(v, 2) for v in V] if not bad else []
m = len(V); distinct = len(set(X)) == m; seen = {}; clash = None
if not bad:
    for c in itertools.combinations(range(m), k):
        u = 0
        for i in c: u |= X[i]
        if u in seen: clash = (seen[u], c); break
        seen[u] = c
print('n=%d k=%d m=%d stray_chars=%r lengths_ok=%s distinct=%s clash=%s' % (n, k, m, bad, ok, distinct, clash))
print('VALID' if not bad and ok and distinct and clash is None else 'INVALID')
