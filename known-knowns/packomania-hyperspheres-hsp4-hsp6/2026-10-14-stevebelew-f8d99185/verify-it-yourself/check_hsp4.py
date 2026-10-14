#!/usr/bin/env python3
"""Standalone checker, Python standard library only (decimal at 50 digits), written from the V3R1T4S bank definition:
r* = min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| ) for N equal balls in the unit 4-ball centred at the origin.
Usage: check_hsp4.py <candidate.txt> <table_value> [<posted.txt>]
Prints r*, the gain over the table value, the non-isometry test (sorted pairwise distances vs the posted file) and PASS/FAIL."""
import sys
from decimal import Decimal, getcontext
getcontext().prec = 50

def load(path):
    pts = []
    for line in open(path):
        parts = line.split()
        if line.startswith('#') or len(parts) < 4: continue
        pts.append([Decimal(p) for p in parts[-4:]])
    return pts

def dists(pts):
    return sorted(sum((a - b) * (a - b) for a, b in zip(p, q)).sqrt() for i, p in enumerate(pts) for q in pts[i + 1:])

def rstar(pts):
    d = dists(pts)
    return min(d[0] / 2, 1 - max(sum(c * c for c in p).sqrt() for p in pts)), d

cand = load(sys.argv[1]); table = Decimal(sys.argv[2])
r, dc = rstar(cand)
ok = len(cand) == 35 and r - table >= Decimal('1e-10')
print('N =', len(cand)); print('r* =', r); print('table =', table); print('gain =', r - table)
if len(sys.argv) > 3:
    posted = load(sys.argv[3]); rp, dp = rstar(posted)
    print('posted r* =', rp, '(reproduces table within 1e-11:', abs(rp - table) < Decimal('1e-11'), ')')
    mx = max(abs(a - b) for a, b in zip(dc, dp)) if len(dc) == len(dp) else Decimal('inf')
    print('max |sorted distance difference| vs posted =', mx)
    ok = ok and mx > Decimal('1e-8') and abs(rp - table) < Decimal('1e-11')
print('PASS' if ok else 'FAIL')
