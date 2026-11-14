"""PROVED-HERE (exact rational arithmetic + arb enclosure): each term g(x) = x exp(-b x^p) of pricing050 is concave on [0,10].
g''(x) = exp(-b x^p) * b p x^(p-1) * (b p x^p - (p+1)). The prefactor is >= 0 on [0,10]; b p x^p - (p+1) is increasing
in x >= 0, so its max on [0,10] is b p 10^p - (p+1), checked < 0 exactly with Fractions of the decimal strings.
Also: arb enclosure of g'' on 10000 subintervals of [0,10] has upper end <= 0 (independent numerical confirmation)."""
from fractions import Fraction as F
import json, sys
from flint import arb
M = json.load(open(sys.argv[1]))
types = sorted({(t['b'], t['p']) for r in M['rows'] for t in r['terms']})
for b, p in types:
    h = F(b) * p * F(10) ** p - (p + 1)
    print('type b=%s p=%d: max of b p x^p - (p+1) on [0,10] = %s = %.6g  -> %s' % (b, p, h, float(h), 'NEG (concave)' if h < 0 else 'NOT'))
    B = arb(b); worst = None
    for k in range(10000):
        lo, hi = arb(k) / 1000, arb(k + 1) / 1000
        X = arb((lo + hi) / 2, (hi - lo) / 2)
        g2 = (-(B * X ** p)).exp() * B * p * X ** (p - 1) * (B * p * X ** p - (p + 1)) if p > 1 else (-(B * X)).exp() * B * (B * X - 2)
        u = g2.upper()
        worst = u if worst is None or u > worst else worst
    print('   arb max upper end of g\'\' enclosure over 10000 cells:', worst.str(8, radius=False))
