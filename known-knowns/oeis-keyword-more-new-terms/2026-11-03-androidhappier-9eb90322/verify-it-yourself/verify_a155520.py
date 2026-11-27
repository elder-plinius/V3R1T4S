#!/usr/bin/env python3
"""Standalone checker for OEIS A155520 row 6 (Python 3 standard library only), written from the entry's definition.

A155520: A(n,k) = number of ordered trees with n edges having k drawings. A drawing of T (n edges) is a sequence of
trees (T_0, ..., T_n) with T_n = T and T_{i-1} obtained from T_i by deleting a leaf. Sequences are sequences of
TREES, so two leaf deletions that give the same tree give the same step.

Representation used here (different from the authors' Dyck words and the reproduce skeptic's nested tuples): an
ordered tree with n edges is its preorder depth sequence (d_0, ..., d_n) with d_0 = 0 and 1 <= d_{i+1} <= d_i + 1.
Vertex i is a leaf iff i = n or d_{i+1} <= d_i; deleting it removes d_i from the sequence (the result is again a valid
depth sequence). D(T) = sum of D(T') over the DISTINCT T' from one leaf deletion; D(single vertex) = 1.
Row n = histogram of D over all Catalan(n) trees, k = 1..max D, zeros kept.

usage: verify_a155520.py OBJECT_ROW_FILE [PAIRS_FILE]   -> exit 0 iff rows 1..5 = DATA, checksums hold and row 6 = object
       verify_a155520.py --seq                           -> negative control (count deletion sequences, leaves
                                                            distinguished); exit 0 iff it reproduces DATA (it must not)
"""
import sys
from functools import lru_cache
from collections import Counter

DATA = [1, 2, 3, 2, 4, 2, 6, 1, 1, 5, 2, 6, 9, 1, 4, 4, 4, 2, 1, 2, 2]   # OEIS A155520 DATA, rows 1..5
CATALAN = [1, 1, 2, 5, 14, 42, 132, 429]
A014307 = [1, 1, 2, 7, 35, 226, 1787, 16717]                           # total drawings (Klazar's w12), offset 0


def trees(n):
    out = []
    def g(seq):
        if len(seq) == n + 1:
            out.append(tuple(seq)); return
        for d in range(1, seq[-1] + 2):
            seq.append(d); g(seq); seq.pop()
    g([0])
    return out


def leaves(t):
    n = len(t) - 1
    return [i for i in range(1, n + 1) if i == n or t[i + 1] <= t[i]]


@lru_cache(None)
def D(t):
    if len(t) == 1:
        return 1
    return sum(D(s) for s in {t[:i] + t[i + 1:] for i in leaves(t)})


@lru_cache(None)
def S(t):   # negative control: deletion sequences, positions distinguished
    if len(t) == 1:
        return 1
    return sum(S(t[:i] + t[i + 1:]) for i in leaves(t))


def row(n, f):
    c = Counter(f(t) for t in trees(n))
    return [c.get(k, 0) for k in range(1, max(c) + 1)], c


def main(a):
    if a and a[0] == "--seq":
        flat = []
        for n in range(1, 6):
            flat += row(n, S)[0]
        print("control (deletion sequences) rows 1..5:", flat[:21])
        return 0 if flat == DATA else 1
    ok = True
    flat = []
    for n in range(1, 7):
        r, c = row(n, D)
        s, w = sum(r), sum(k * v for k, v in c.items())
        print("%d sum=%d wsum=%d row: %s" % (n, s, w, ",".join(map(str, r))))
        if s != CATALAN[n] or w != A014307[n]:
            print("checksum mismatch at n=%d" % n); ok = False
        if n <= 5:
            flat += r
        else:
            row6 = r
    if flat == DATA:
        print("rows 1..5 equal OEIS DATA (21 terms)")
    else:
        print("rows 1..5 DIFFER from DATA"); ok = False
    obj = [int(x) for x in open(a[0]).read().strip().split(",")]
    if obj == row6:
        print("row 6 (%d values) equals %s; A(6,1) = %d" % (len(row6), a[0], row6[0]))
    else:
        print("row 6 DIFFERS from %s" % a[0]); ok = False
    if len(a) > 1:
        pairs = [tuple(map(int, l.split())) for l in open(a[1]) if l.strip() and not l.startswith("#")]
        if pairs == list(enumerate(row6, 1)):
            print("pairs file equals row 6 (k, A(6,k)) for k = 1..%d" % len(row6))
        else:
            print("pairs file DIFFERS"); ok = False
    # %e: of the 5 trees with 3 edges, UDUUDD and UUDDUD have 2 drawings, the other three 1
    m = {t: D(t) for t in trees(3)}
    e = sorted(m.values())
    print("%e n = 3 drawing counts (multiset):", e, "ok" if e == [1, 1, 1, 2, 2] else "MISMATCH")
    ok = ok and e == [1, 1, 1, 2, 2]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
