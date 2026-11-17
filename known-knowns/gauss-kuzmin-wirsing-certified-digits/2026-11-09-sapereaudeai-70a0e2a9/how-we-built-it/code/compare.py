#!/usr/bin/env python3
"""Exact comparison of a certified enclosure with the reference digit strings (run with python -I).
usage: compare.py CERT.json MUFILE REFS.json OLD649.txt
C_83 enclosure = [-mu - rad, -mu + rad] with mu the exact dyadic used by gkw_cert.py (arb(mu_str).mid()).
Checks, in exact rationals: (1) |(-mu) - Nisoli centre| <= rad + 10^-175 (bank rule: agree within the two radii);
(2) the 649-decimal non-certified value of run 2026-11-08-1936 lies in the enclosure up to its own truncation 10^-649;
(3) OEIS b-file 382 decimals (truncated) lie within rad + 10^-382; prints the certified decimals."""
import sys, json, re
from flint import arb, fmpq, fmpz, ctx

cert = json.load(open(sys.argv[1]))
mu_str = open(sys.argv[2]).read().split()[0]
refs = json.load(open(sys.argv[3]))
old = re.search(r'0\.(\d+)', open(sys.argv[4]).read()).group(1)

ctx.prec = cert['prec']
mu = arb(mu_str).mid()
man, ex = mu.man_exp()
mu_q = fmpq(int(man)) * (fmpq(2) ** int(ex) if int(ex) >= 0 else fmpq(1, 2 ** (-int(ex))))
c83 = -mu_q
# radius upper bound: parse "[x +/- y]" conservatively as x + y, rounded up in decimal
rs = cert['radius']
m = re.match(r'\[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]', rs)
if m:
    from decimal import Decimal
    rad = fmpq(*Decimal(m.group(1)).as_integer_ratio()) + fmpq(*Decimal(m.group(2)).as_integer_ratio())
    rad = rad * fmpq(1001, 1000)   # absorb decimal printing of the arb radius
else:
    from decimal import Decimal
    rad = fmpq(*Decimal(rs).as_integer_ratio()) * fmpq(1001, 1000)
D = cert['certified_D']
assert rad < fmpq(1, 10 ** D), 'radius not < 10^-D'


def dec(s):
    return fmpq(int(s), 10 ** len(s))


nis = dec(refs['nisoli_centre_digits'])
oeis = dec(refs['oeis_b038517_digits'])
o649 = dec(old)
d_nis = abs(c83 - nis)
ok_nis = d_nis <= rad + fmpq(1, 10 ** 175)
ok_649 = abs(c83 - o649) <= rad + fmpq(1, 10 ** 649)
ok_oeis = abs(c83 - oeis) <= rad + fmpq(1, 10 ** 382)
print('certified D =', D, ' radius <=', (arb(rad.p) / arb(rad.q)).str(6))
print('Nisoli 175-digit centre within rad + 1e-175:', ok_nis, ' |diff| =', (arb(d_nis.p) / arb(d_nis.q)).str(3))
print('old 649-decimal value within rad + 1e-649:', ok_649)
print('OEIS b-file 382 decimals within rad + 1e-382:', ok_oeis)
# certified decimal string: digits of -mu that are the same at both ends of the enclosure
lo, hi = c83 - rad, c83 + rad
k = 0
s_lo = str(int(lo * 10 ** (D + 5)))
s_hi = str(int(hi * 10 ** (D + 5)))
while k < len(s_lo) and s_lo[k] == s_hi[k]:
    k += 1
print('enclosure endpoints share the first %d digits after "0.":' % k)
print('C_83 = 0.' + s_lo[:k] + '...')
print('ALL_CHECKS', 'PASS' if (ok_nis and ok_649 and ok_oeis) else 'FAIL')
