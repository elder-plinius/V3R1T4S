#!/usr/bin/env python3
"""Property checker written from the OEIS A002224 definition:
'Smallest prime p of form p = 8k+1 such that first n primes (p_1=2, ..., p_n) are quadratic residues mod p.'
This checks the PROPERTY of one q (not minimality). Usage: check_a002224.py q n"""
import sys

def small_primes(k):
    out, c = [], 2
    while len(out) < k:
        if all(c % d for d in range(2, int(c**0.5) + 1)):
            out.append(c)
        c += 1
    return out

def is_prime(n):
    # Deterministic Miller-Rabin: bases = first 13 primes is proven correct for n < 3.317e24 (Sorenson-Webster 2015).
    if n < 2:
        return False
    B = small_primes(13)
    for p in B:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in B:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def least_qnr(q):
    p = 2
    while True:
        if all(p % d for d in range(2, int(p**0.5) + 1)) and pow(p, (q - 1) // 2, q) != 1:
            return p
        p += 1

def has_property(q, n):
    assert q < 3317044064679887385961981
    if q % 8 != 1 or not is_prime(q):
        return False
    return all(pow(p, (q - 1) // 2, q) == 1 for p in small_primes(n))   # Euler's criterion

if __name__ == "__main__":
    q, n = int(sys.argv[1]), int(sys.argv[2])
    ok = has_property(q, n)
    print("q=%d n=%d prime=%s q%%8=%d least_qnr=%d property=%s" % (q, n, is_prime(q), q % 8, least_qnr(q), ok))
