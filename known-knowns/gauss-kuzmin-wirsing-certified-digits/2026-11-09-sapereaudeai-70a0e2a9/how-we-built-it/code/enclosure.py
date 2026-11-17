#!/usr/bin/env python3
"""Outward-rounded decimal enclosure of C_83 = -lambda_2 from one or more certify JSONs (run with python -I).
usage: enclosure.py MUFILE NDEC CERT1.json [CERT2.json ...]
For each run: centre -mu with mu = arb(mu_str).mid() at that run's precision (exact dyadic), radius parsed
conservatively ("[x +/- y]" -> (x + y) * 1.001). Prints the hull of all run enclosures, floor/ceil to NDEC decimals."""
import sys, json, re
from decimal import Decimal
from flint import arb, fmpq, fmpz, ctx

mu_str = open(sys.argv[1]).read().split()[0]
nd = int(sys.argv[2])
los, his, Ds, rads = [], [], [], []
for fn in sys.argv[3:]:
    c = json.load(open(fn))
    ctx.prec = c['prec']
    man, ex = arb(mu_str).mid().man_exp()
    mu = fmpq(int(man)) * (fmpq(2) ** int(ex) if int(ex) >= 0 else fmpq(1, 2 ** (-int(ex))))
    m = re.match(r'\[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]', c['radius'])
    rad = (fmpq(*Decimal(m.group(1)).as_integer_ratio()) + fmpq(*Decimal(m.group(2)).as_integer_ratio())) * fmpq(1001, 1000)
    assert rad < fmpq(1, 10 ** c['certified_D']) and c['isolation_ok'] and c.get('n_eig_total', 80) == 80
    los.append(-mu - rad); his.append(-mu + rad); Ds.append(c['certified_D']); rads.append(rad)
lo, hi = min(los), max(his)
S = fmpz(10) ** nd
lo_i = (lo * S).floor(); hi_i = (hi * S).ceil()
def fmt(i):
    s = str(int(i)).rjust(nd, '0')
    return '0.' + s
k = 0
a, b = fmt(lo_i)[2:], fmt(hi_i)[2:]
while k < nd and a[k] == b[k]:
    k += 1
print('C_83 = |lambda_2| of the Gauss-Kuzmin-Wirsing operator; certified enclosure (outward-rounded decimal endpoints, hull of %d runs):' % len(Ds))
print('lower =', fmt(lo_i))
print('upper =', fmt(hi_i))
width = (hi - lo) / 2
print('half-width of the hull <= %s < 10^-%d' % ((arb(width.p) / arb(width.q)).str(8), min(Ds)))
print('certified decimals D = %d (min over the runs: %s)' % (min(Ds), ', '.join(str(d) for d in Ds)))
print('the two endpoints agree on the first %d decimals: 0.%s' % (k, a[:k]))
