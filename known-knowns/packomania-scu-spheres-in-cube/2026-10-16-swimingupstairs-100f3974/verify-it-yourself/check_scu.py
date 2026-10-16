#!/usr/bin/env python3
"""Standalone checker (Python standard library only), written from the definition:
r* = min( min_{i<j} |c_i - c_j| / 2 , 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ) for N centres in the cube [-1/2,1/2]^3.
Exact integer arithmetic over ALL pairs (coordinates scaled by 10^K), sqrt in 50-digit Decimal.
Usage: check_scu.py OBJECT N TABLE_RADIUS   -> prints r*, margin, and PASS iff N matches and r* - table >= 1e-11."""
import sys
from decimal import Decimal, getcontext
getcontext().prec = 60
path, N, table = sys.argv[1], int(sys.argv[2]), Decimal(sys.argv[3])
rows = [l.split() for l in open(path) if l.strip()]
ok = all(len(r) == 3 for r in rows)
K = max(len(t.split('.')[1]) if '.' in t else 0 for r in rows for t in r)
S = 10 ** K
def toint(t):
    d = Decimal(t); v = d * S
    assert v == v.to_integral_value(), t
    return int(v)
P = [tuple(toint(t) for t in r) for r in rows]
n = len(P)
distinct = len(set(P)) == n
m = min((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 for i, a in enumerate(P) for b in P[i+1:])
w = Decimal(S // 2 - max(abs(c) for p in P for c in p)) / S
pair = Decimal(m).sqrt() / 2 / S
r = min(pair, w)
margin = r - table
print('n=%d (expected %d) rows_ok=%s distinct=%s' % (n, N, ok, distinct))
print('half_min_pair=%s wall=%s' % (format(pair, '.25f'), format(w, '.25f')))
print('r*=%s table=%s margin=%s' % (format(r, '.25f'), table, format(margin, '.6e')))
print('PASS' if (ok and distinct and n == N and margin >= Decimal('1e-11')) else 'FAIL')
