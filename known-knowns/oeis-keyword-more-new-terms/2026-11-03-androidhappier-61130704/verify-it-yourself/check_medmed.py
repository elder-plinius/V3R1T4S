#!/usr/bin/env python3
"""Standalone checker for OEIS A361864, written from the definition (Python standard library only).

Definition (OEIS A361864): number of set partitions of {1..n} whose block-medians have integer median.
The median of a multiset of even size is the mean of its two middle elements (entry comment).
The outer median is taken over the multiset of block medians (with repetition).

Usage: python3 check_medmed.py N_MAX        -> prints "n a(n)" for n = 1..N_MAX
Exact arithmetic: every median is kept as a Fraction.
"""
import sys
from fractions import Fraction


def median(xs):
    s = sorted(xs)
    k = len(s)
    if k % 2:
        return Fraction(s[k // 2])
    return Fraction(s[k // 2 - 1] + s[k // 2], 2)


def count(n):
    # build partitions by placing 1..n in turn into an existing block or a new block
    blocks = []
    total = 0

    def rec(i):
        nonlocal total
        if i > n:
            m = median([median(b) for b in blocks])
            if m.denominator == 1:
                total += 1
            return
        for b in blocks:
            b.append(i)
            rec(i + 1)
            b.pop()
        blocks.append([i])
        rec(i + 1)
        blocks.pop()

    rec(1)
    return total


if __name__ == "__main__":
    nmax = int(sys.argv[1])
    for n in range(1, nmax + 1):
        print(n, count(n), flush=True)
