#!/usr/bin/env python3
"""Compare lens independent-recheck primes (q, n by Euler criterion) with lens sieve-first survivors (primality and
Euler criterion recomputed here). Usage: compare.py recheck_primes.txt sieve_survivors.txt bfile checker_dir"""
import sys
sys.path.insert(0, sys.argv[4])
from check_a002224 import is_prime, small_primes
P = small_primes(60)
def lead(q):
    n = 0
    while n < len(P) and pow(P[n], (q - 1) // 2, q) == 1: n += 1
    return n
A = {}
for l in open(sys.argv[1]):
    q, n = map(int, l.split()); A[q] = n
B = {}
for l in open(sys.argv[2]):
    q = int(l.split()[0])
    if is_prime(q): B[q] = lead(q)
print("recheck primes:", len(A), " sieve-first primes:", len(B))
print("identical sets:", set(A) == set(B), " identical n values:", A == B)
only_a = sorted(set(A) - set(B)); only_b = sorted(set(B) - set(A))
print("only in recheck:", only_a[:10], " only in sieve-first:", only_b[:10])
bf = {int(a): int(b) for a, b in (l.split() for l in open(sys.argv[3]) if l.strip())}
for m in range(30, 46):
    c = [q for q in A if A[q] >= m]
    v = min(c) if c else None
    print("recheck n=%d least=%s %s" % (m, v, ("bfile=%d %s" % (bf[m], "MATCH" if bf[m] == v else "MISMATCH")) if m in bf else ""))
