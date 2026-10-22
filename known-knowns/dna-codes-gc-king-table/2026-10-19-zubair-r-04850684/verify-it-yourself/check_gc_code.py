#!/usr/bin/env python3
"""Checker for A_4^GC(n,d,w) codes (King 2003; King's table at rambutan.umassmed.edu/king/dnacodes.html).

A code is admissible iff every word has length n over {A,C,G,T}, exactly w = floor(n/2) letters in {G,C},
all words are distinct, and every pair is at Hamming distance >= d.
Usage: check_gc_code.py CODEFILE n d [table_value]   (one codeword per line; blank lines and '#' ignored)
Prints VALID size=<m> (and BEATS/NOT_BEATS table) or INVALID <reason>; exit code 0 only when VALID.
"""
import sys
from itertools import combinations

def load(path):
    with open(path) as f:
        return [l.strip().upper() for l in f if l.strip() and not l.lstrip().startswith("#")]

def check(words, n, d):
    w = n // 2
    for x in words:
        if len(x) != n: return "word %r has length %d, not %d" % (x, len(x), n)
        if set(x) - set("ACGT"): return "word %r uses letters outside ACGT" % x
        gc = sum(c in "GC" for c in x)
        if gc != w: return "word %r has GC count %d, not %d" % (x, gc, w)
    if len(set(words)) != len(words): return "duplicate words"
    for a, b in combinations(words, 2):
        h = sum(p != q for p, q in zip(a, b))
        if h < d: return "words %r and %r at distance %d < %d" % (a, b, h, d)
    return None

if __name__ == "__main__":
    path, n, d = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    words = load(path); err = check(words, n, d)
    if err: print("INVALID", err); sys.exit(1)
    msg = "VALID size=%d" % len(words)
    if len(sys.argv) > 4:
        tv = int(sys.argv[4]); msg += " table=%d %s" % (tv, "BEATS" if len(words) > tv else "NOT_BEATS")
    print(msg)
