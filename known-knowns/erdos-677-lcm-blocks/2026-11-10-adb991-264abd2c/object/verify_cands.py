#!/usr/bin/env python3
"""Exact verification of candidate triples "k n m" written by search677 (comment lines start with #).
For each candidate computes M(n,k) and M(m,k) exactly (Python big ints) and reports:
  - exact equal-lcm pairs (with flag DISJOINT if m >= n + k, i.e. a counterexample),
  - for disjoint candidates that fail: which primes < k carry the mismatch (near-collision statistics, H7).
usage: verify_cands.py CANDFILE [--list-equal]
"""
import sys
from math import gcd
from collections import Counter

def M(x, k):
    v = 1
    for y in range(x + 1, x + k + 1):
        v = v // gcd(v, y) * y
    return v

def small_primes(k):
    return [p for p in range(2, k) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

def vp(x, p):
    e = 0
    while x % p == 0:
        x //= p; e += 1
    return e

def main():
    fn = sys.argv[1]
    list_equal = "--list-equal" in sys.argv
    n_c = n_eq = n_disj = n_disj_eq = 0
    mism = Counter()
    eq_pairs = []
    header = []
    for line in open(fn):
        if line.startswith("#"):
            header.append(line.rstrip()); continue
        k, n, m = map(int, line.split())
        n_c += 1
        a, b = M(n, k), M(m, k)
        disj = m >= n + k
        n_disj += disj
        if a == b:
            n_eq += 1
            eq_pairs.append((k, n, m))
            if disj:
                n_disj_eq += 1
                print("COUNTEREXAMPLE CANDIDATE (exact lcm equal, disjoint):", n, m, k, flush=True)
        elif disj:
            # large parts agree by construction (or hash collision); find mismatching primes
            g = a // gcd(a, b) * (b // gcd(a, b))
            bad = []
            for p in range(2, max(k, 3) + 1000):
                if g % p == 0:
                    bad.append(p)
                    while g % p == 0: g //= p
                if g == 1: break
            if g != 1:
                bad.append("LARGE(%d digits)" % len(str(g)))
            mism[tuple(bad)] += 1
    for h in header[:1] + header[-1:]:
        print(h)
    print("candidates:", n_c, "exact-equal:", n_eq, "disjoint candidates:", n_disj, "disjoint exact-equal:", n_disj_eq)
    if mism:
        print("mismatch prime-sets among disjoint non-equal candidates (top 15):")
        for key, c in mism.most_common(15):
            print("  ", key, c)
        large = sum(c for key, c in mism.items() if any(isinstance(x, str) for x in key))
        print("disjoint candidates whose mismatch involves a prime outside the small range (hash collision?):", large)
    if list_equal:
        for t in eq_pairs:
            print("EQ", *t)

if __name__ == "__main__":
    main()
