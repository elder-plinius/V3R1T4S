#!/usr/bin/env python3
"""Post-process wheel output: keep proven primes (deterministic MR, valid < 3.3e24), recompute the number of leading
primes that are QRs by Euler's criterion (not from the sieve), and report the least prime for each n >= 30.
Usage: analyze.py survivors.txt X bfile"""
import sys
sys.path.insert(0, sys.argv[4] if len(sys.argv) > 4 else '.')
from check_a002224 import is_prime, small_primes
P = small_primes(80)
X = int(sys.argv[2])
best = {}
nprime = 0
for line in open(sys.argv[1]):
    q = int(line.split()[0])
    if q > X or not is_prime(q):
        continue
    nprime += 1
    n = 0
    while n < len(P) and pow(P[n], (q - 1) // 2, q) == 1:
        n += 1                      # first n primes are QRs mod q
    for m in range(30, n + 1):
        if m not in best or q < best[m]:
            best[m] = q
bf = {int(a): int(b) for a, b in (l.split() for l in open(sys.argv[3]) if l.strip())}
print("primes among survivors:", nprime)
ok = True
for m in sorted(best):
    tag = ("bfile=%d %s" % (bf[m], "MATCH" if bf[m] == best[m] else "MISMATCH")) if m in bf else "NOT IN BFILE"
    if m in bf and bf[m] != best[m]: ok = False
    print("n=%d least_prime=%d %s" % (m, best[m], tag))
missing = [m for m in bf if m >= 30 and bf[m] <= X and m not in best]
print("bfile terms <= X not found:", missing)
print("CALIBRATION", "PASS" if ok and not missing else "FAIL")
