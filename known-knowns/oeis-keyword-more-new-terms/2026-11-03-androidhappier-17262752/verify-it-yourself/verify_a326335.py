#!/usr/bin/env python3
"""Standalone checker for OEIS A326335, written for this package from the entry's definition (stdlib only).

A326335(n): number of set partitions of {1..n} whose blocks, joined by an edge whenever two blocks nest, form a
connected graph. Two blocks nest if they have the form {...x,y...} and {...z,t...} with x<z<t<y or z<x<y<t, where
x,y are consecutive elements of the first (sorted) block and z,t consecutive elements of the second. The empty
partition (n = 0) and one-block partitions count as connected.

usage: verify_a326335.py object/VALUE.txt   -> counts n = 0..11, compares a(0..10) with DATA and a(11) with the object
       verify_a326335.py --any-pairs        -> negative control: x,y and z,t any pairs; exits 1 if DATA is NOT reproduced
"""
import re
import sys

DATA = [1, 1, 1, 1, 2, 6, 21, 86, 394, 1974, 10696]  # OEIS A326335 DATA, n = 0..10 (offset 0)
N = 11


def pairs(block, consecutive):
    if consecutive:
        return [(block[i], block[i + 1]) for i in range(len(block) - 1)]
    return [(block[i], block[j]) for i in range(len(block)) for j in range(i + 1, len(block))]


def nest(pa, pb):
    for x, y in pa:
        for z, t in pb:
            if x < z < t < y or z < x < y < t:
                return True
    return False


def connected(blocks, consecutive):
    k = len(blocks)
    if k <= 1:
        return True
    pr = [pairs(b, consecutive) for b in blocks]
    seen = [False] * k
    seen[0] = True
    stack = [0]
    count = 1
    while stack:
        v = stack.pop()
        for w in range(k):
            if not seen[w] and nest(pr[v], pr[w]):
                seen[w] = True
                count += 1
                stack.append(w)
    return count == k


def count(n, consecutive):
    """Enumerate set partitions of {1..n} by inserting n, n-1, ... into blocks (blocks stay sorted ascending)."""
    total = 0

    def rec(m, blocks):
        nonlocal total
        if m > n:
            if connected(blocks, consecutive):
                total += 1
            return
        for b in blocks:
            b.append(m)
            rec(m + 1, blocks)
            b.pop()
        blocks.append([m])
        rec(m + 1, blocks)
        blocks.pop()

    rec(1, [])
    return total


def main():
    args = sys.argv[1:]
    if args == ["--any-pairs"]:
        got = [count(n, False) for n in range(10)]
        print("any-pairs control a(0..9): %s" % got)
        same = got == DATA[:10]
        print("control reproduces DATA: %s" % same)
        return 0 if same else 1   # exit 0 only if the wrong definition reproduced DATA (bad)
    if len(args) != 1:
        print(__doc__)
        print("FAIL")
        return 2
    m = re.fullmatch(r"\s*A326335\((\d+)\)\s*=\s*(\d+)\s*", open(args[0]).read())
    if not m or int(m.group(1)) != N:
        print("object is not of the form 'A326335(11) = <value>'")
        print("FAIL")
        return 1
    claimed = int(m.group(2))
    print("object claims A326335(%d) = %d" % (N, claimed))
    got = []
    for n in range(N + 1):
        got.append(count(n, True))
        print("%d %d" % (n, got[-1]))
        sys.stdout.flush()
    ok = True
    if got[:N] == DATA:
        print("a(0..10) equal OEIS DATA")
    else:
        print("a(0..10) differ from OEIS DATA")
        ok = False
    print("computed a(11) = %d" % got[N])
    if got[N] != claimed:
        print("computed value differs from the object")
        ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
