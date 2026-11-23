#!/usr/bin/env python3
"""Standalone checker for OEIS A326336 (standard library only).

Definition (OEIS A326336, Gus Wiseman): a(n) is the number of set partitions of {1..n} whose blocks, joined by an
edge when they capture, form a connected graph. Two blocks capture if they are of the form {...x...y...} and
{...z...t...} with x<z<t<y or z<x<y<t. The empty partition (n = 0) and one-block partitions count.

Usage:
  verify_a326336.py OBJECT     count n = 0..11, compare a(0..10) with OEIS DATA and a(11) with OBJECT's value
  verify_a326336.py --crossing negative control: crossing edges (x<z<y<t or z<x<t<y) instead of capturing;
                               exits 0 only if it (wrongly) reproduces DATA for n = 0..9
The fast capture test (A captures B iff at least two elements of B lie strictly between min A and max A) is checked
against the literal any-pair test on every block pair for n <= 8 before it is used.
"""
import itertools, re, sys

DATA = [1, 1, 1, 1, 2, 7, 24, 100, 458, 2279, 12270]   # OEIS A326336, n = 0..10, offset 0


def partitions(n):
    """All set partitions of {1..n} as lists of sorted blocks (insert n, n-1, ... recursively)."""
    def rec(k):
        if k == 0:
            yield []
            return
        for p in rec(k - 1):
            for i in range(len(p)):
                yield p[:i] + [p[i] + [k]] + p[i + 1:]
            yield p + [[k]]
    return rec(n)


def cap_literal(A, B):
    return any(x < z < t < y or z < x < y < t
               for x, y in itertools.combinations(A, 2) for z, t in itertools.combinations(B, 2))


def cap_fast(A, B):
    def inside(P, Q):
        lo, hi = P[0], P[-1]
        return sum(1 for v in Q if lo < v < hi) >= 2
    return inside(A, B) or inside(B, A)


def cross(A, B):
    return any(x < z < y < t or z < x < t < y
               for x, y in itertools.combinations(A, 2) for z, t in itertools.combinations(B, 2))


def connected(p, rel):
    if len(p) <= 1:
        return True
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in range(len(p)):
            if w not in seen and rel(p[v], p[w]):
                seen.add(w)
                stack.append(w)
    return len(seen) == len(p)


def count(n, rel):
    return sum(1 for p in partitions(n) if connected(p, rel))


def main(argv):
    if len(argv) == 2 and argv[1] == "--crossing":
        vals = [count(n, cross) for n in range(10)]
        print("crossing control a(0..9):", vals)
        return 0 if vals == DATA[:10] else 1
    if len(argv) != 2:
        print(__doc__)
        return 2
    m = re.fullmatch(r"\s*A326336\(11\) = (\d+)\s*", open(argv[1]).read())
    if not m:
        print("object file not of the form 'A326336(11) = N'")
        return 1
    claimed = int(m.group(1))
    for n in range(9):
        for p in partitions(n):
            for A, B in itertools.combinations(p, 2):
                if cap_literal(A, B) != cap_fast(A, B):
                    print("fast capture test disagrees with the literal test at", A, B)
                    return 1
    print("fast capture test equals the literal any-pair test on every block pair, n <= 8")
    vals = []
    for n in range(12):
        vals.append(count(n, cap_fast))
        print(n, vals[-1])
        sys.stdout.flush()
    ok = True
    if vals[:11] == DATA:
        print("a(0..10) equal OEIS DATA")
    else:
        print("a(0..10) DIFFER from OEIS DATA")
        ok = False
    print("computed a(11) = %d; object says %d" % (vals[11], claimed))
    if vals[11] != claimed:
        ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
