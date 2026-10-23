#!/usr/bin/env python3
"""mpmath 50-digit score of a code file: every pair, after unit normalization. Usage: score.py <file>"""
import sys
import mpmath as mp
mp.mp.dps = 50
L = [l.split(",") for l in open(sys.argv[1]) if l.strip()]
U = []
for r in L:
    v = [mp.mpf(t) for t in r]; n = mp.sqrt(mp.fsum(x * x for x in v)); U.append([x / n for x in v])
best = mp.mpf(-2); arg = None
for i in range(len(U)):
    ui = U[i]
    for j in range(i + 1, len(U)):
        d = mp.fdot(ui, U[j])
        if d > best: best, arg = d, (i, j)
print("N=%d d=%s c*=%s pair=%s" % (len(U), {len(r) for r in L}, mp.nstr(best, 50), arg))
