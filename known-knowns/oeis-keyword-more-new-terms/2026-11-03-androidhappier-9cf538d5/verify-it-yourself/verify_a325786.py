#!/usr/bin/env python3
"""Standalone checker for A325786(21), written from the OEIS definition (Python 3 standard library only).

OEIS A325786: number of complete necklace compositions of n.
- composition of n: sequence of positive integers summing to n;
- necklace: lexicographically <= every one of its cyclic rotations (ties allowed, = Mathematica neckQ via OrderedQ);
- complete: every integer 1..n is the sum of some circular subsequence (consecutive parts, wrapping around).

Method (different from the authors' programs): compositions of n are enumerated as (n-1)-bit cut masks; the
necklace test compares the part tuple with its rotations; completeness is checked with a bitmask of circular block
sums built from prefix sums of the doubled part list. Usage:
    python3 verify_a325786.py object/VALUE.txt [--no-necklace]
--no-necklace is a negative control (drops the necklace test); it must not reproduce DATA.
"""
import re, sys

DATA = [1, 1, 2, 2, 4, 7, 12, 19, 41, 71, 141, 255, 509, 924, 1882, 3395, 6838, 12715, 25233, 47049]  # n = 1..20


def count(n, necklace=True):
    full = (1 << (n + 1)) - 2  # bits 1..n
    total = 0
    for m in range(1 << (n - 1)):
        parts, last = [], 0
        for i in range(1, n):
            if m >> (i - 1) & 1:
                parts.append(i - last)
                last = i
        parts.append(n - last)
        k = len(parts)
        if necklace:
            t = tuple(parts)
            if any(t[r:] + t[:r] < t for r in range(1, k)):
                continue
        # circular block sums: start s, length L = 1..k
        d = parts + parts
        seen = 0
        for s in range(k):
            acc = 0
            for L in range(k):
                acc += d[s + L]
                seen |= 1 << acc
        if seen & full == full:
            total += 1
    return total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    neck = "--no-necklace" not in sys.argv
    if not neck:
        got = [count(n, necklace=False) for n in range(1, 10)]
        print("no-necklace control a(1..9):", got)
        ok = got != DATA[:9]
        print("control differs from DATA:", ok)
        print("FAIL" if ok else "PASS")  # a control that reproduces DATA would be a broken checker
        return 1 if ok else 0
    text = open(args[0]).read()
    m = re.fullmatch(r"\s*A325786\((\d+)\)\s*=\s*(\d+)\s*", text)
    if not m:
        print("object is not of the form 'A325786(n) = v'")
        print("FAIL")
        return 1
    idx, val = int(m.group(1)), int(m.group(2))
    print("object claims A325786(%d) = %d" % (idx, val))
    ok = True
    if idx != len(DATA) + 1:
        print("index %d is not the first index beyond DATA (%d)" % (idx, len(DATA) + 1))
        ok = False
    vals = []
    for n in range(1, 22):
        vals.append(count(n))
        print(n, vals[-1], flush=True)
    if vals[:20] == DATA:
        print("a(1..20) equal OEIS DATA")
    else:
        print("a(1..20) DIFFER from OEIS DATA")
        ok = False
    print("computed a(21) = %d" % vals[20])
    if idx != 21 or val != vals[20]:
        print("object value does not match the computed a(%d)" % idx)
        ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
