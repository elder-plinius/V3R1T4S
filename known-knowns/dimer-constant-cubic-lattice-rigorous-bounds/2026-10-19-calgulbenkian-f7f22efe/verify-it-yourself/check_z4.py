#!/usr/bin/env python3
"""Z^4 dimer upper bound at (m1,m2,m3) = (3,3,2): standard library only.

1  brute-force trace identity on the 4D quotient (2,2,2), l = 4 (546803712 perfect matchings)
2  property C on the full 4D matrices (2,2,2) and (3,2,2)
3  the shipped sector-9 certificate (v = (XY)^4 1, 1404 orbits): layer, group (36 elements) and orbits rebuilt from
   the definitions, every listed (XY v)_u recomputed, exact ratio and bound
4  p = 4 iterates from the all-ones vector for every sector 0..9 (about 5 minutes; CW_QUICK=1 skips this):
   sector 9 must be the largest and equal the shipped ratio
"""
import os, sys, time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import cwcheck as cw
from decimal import Decimal

claim = os.path.dirname(here)
ok_all = True


def report(name, ok, extra=''):
    global ok_all
    ok_all = ok_all and ok
    print('%s %s %s' % ('PASS' if ok else 'FAIL', name, extra), flush=True)


report('trace identity (2,2,2), l=4', cw.cmd_trace([2, 2, 2], 4))
report('property C (2,2,2)', cw.cmd_propc([2, 2, 2]))
report('property C (3,2,2)', cw.cmd_propc([3, 2, 2]))
t0 = time.time()
res = cw.cmd_cert([3, 3, 2], 9, os.path.join(claim, 'object', 'cert_4d_332.txt'))
exp = (4527733104115888037323625277988191910329450496, 3349983888759867418883092542107779072)
if res is None:
    report('certificate', False)
else:
    num, den, b = res
    report('sector 9 exact ratio equals the shipped one; l4 <= %s (ten places, rounded up), rounded up to six places %s' % ((b * 10 ** 10).to_integral_value(rounding='ROUND_CEILING') / 10 ** 10, cw.ceil6(b)),
           num * exp[1] == exp[0] * den and cw.ceil6(b) == Decimal('0.584015'), '%.0fs' % (time.time() - t0))
    if os.environ.get('CW_QUICK') != '1':
        best = cw.cmd_iter([3, 3, 2], 4)
        b4, sec, n4, d4 = best[4]
        report('all sectors at p=4: maximum %.10f in sector %d; equals the shipped ratio' % (b4, sec),
               sec == 9 and n4 * exp[1] == exp[0] * d4 and b4 == b)
print('ALL CHECKS PASS' if ok_all else 'SOME CHECK FAILED')
sys.exit(0 if ok_all else 1)
