#!/usr/bin/env python3
"""Standard-library comparison of a computed radius with the saved table records.
Prints the facts only (row value, largest row value at N' >= N, Moki-Julio manifest values,
Cohn spherical-code values converted to a ball packing); it does not judge them.

  python3 table_compare.py --n N --rstar R --radius table-record/radius.txt
        [--mj table-record/mj_rows.csv --shelf scu] [--cohn table-record/cohn_rows.txt]
Cohn conversion for balls in a ball: a code with cosine c has s = sqrt(2 - 2c) and r = s / (2 + s).
"""
import argparse, csv
from decimal import Decimal, getcontext
getcontext().prec = 50

ap = argparse.ArgumentParser()
ap.add_argument('--n', type=int, required=True)
ap.add_argument('--rstar', required=True)
ap.add_argument('--radius', required=True)
ap.add_argument('--mj')
ap.add_argument('--shelf')
ap.add_argument('--cohn')
a = ap.parse_args()
N = a.n
rs = Decimal(a.rstar)


def show(label, v, at=None):
    if v is None:
        print("%s: none" % label)
    else:
        print("%s: %s%s  r_star minus this = %s" % (label, format(v, '.14f'), '' if at is None else ' (at N=%d)' % at, format(rs - v, '.6e')))


rows = {}
for line in open(a.radius):
    if line.startswith('#') or not line.strip():
        continue
    t = line.split()
    rows[int(t[0])] = Decimal(t[1])
print("table rows read: %d (N from %d to %d)" % (len(rows), min(rows), max(rows)))
show("table row N=%d" % N, rows.get(N))
ge = {k: v for k, v in rows.items() if k >= N}
if ge:
    k = max(ge, key=lambda x: ge[x])
    show("largest table row at N' >= %d" % N, ge[k], k)
else:
    print("no table row at N' >= %d" % N)
if a.mj:
    mj = {}
    for r in csv.DictReader(open(a.mj)):
        if r['shelf'] == a.shelf:
            mj[int(r['N'])] = Decimal(r['new_radius'])
    show("Moki-Julio manifest N=%d" % N, mj.get(N))
    g = {k: v for k, v in mj.items() if k >= N}
    if g:
        k = max(g, key=lambda x: g[x])
        show("largest manifest value at N' >= %d" % N, g[k], k)
if a.cohn:
    co = {}
    for l in open(a.cohn):
        t = l.split(',', 3)
        if len(t) >= 3:
            c = Decimal(t[2])
            s = (2 - 2 * c).sqrt()
            co[int(t[1])] = s / (2 + s)
    show("Cohn table converted, N=%d" % N, co.get(N))
    g = {k: v for k, v in co.items() if k >= N}
    if g:
        k = max(g, key=lambda x: g[x])
        show("largest converted Cohn value at N' >= %d" % N, g[k], k)
print("RESULT facts printed")
