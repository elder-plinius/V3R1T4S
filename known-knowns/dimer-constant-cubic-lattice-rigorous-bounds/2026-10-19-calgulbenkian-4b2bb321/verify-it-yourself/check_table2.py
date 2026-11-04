#!/usr/bin/env python3
"""Reproduction of He's Table 2 (arXiv 2607.28810) with exact integer arithmetic; standard library only.

For every (m,n) with m>=n of the table except (5,5) this script rebuilds the layer, the symmetry group and the
blocks X, Y from the definitions, iterates v -> XY v from the all-ones vector in Python integers, takes the row
maximising the ratio by cross multiplication, and rounds the logarithm up to six places.  The (5,5) entry
(p = 2, 13 sectors, 35070 orbits in the largest) is done by the compiled program cwsec.c if a C compiler is found
(run_checks.sh does that); this script only parses and checks its output when given as argument 1.
Environment: CW_QUICK=1 skips (5,4), the slowest Python entry (about 8 minutes alone).
"""
import os, sys, time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import cwcheck as cw
from decimal import Decimal

HE = {(2, 2): '0.486478', (3, 2): '0.471408', (3, 3): '0.458558', (4, 2): '0.465970', (4, 3): '0.457380',
      (4, 4): '0.454673', (5, 2): '0.463401', (5, 3): '0.454663', (5, 4): '0.453365', (6, 2): '0.462010',
      (6, 3): '0.454618', (5, 5): '0.452130'}
ok_all = True


def report(name, ok, extra=''):
    global ok_all
    ok_all = ok_all and ok
    print('%s %s %s' % ('PASS' if ok else 'FAIL', name, extra), flush=True)


quick = os.environ.get('CW_QUICK') == '1'
for dims, l in (([2, 2], 4), ([3, 2], 4)):
    report('trace identity %s l=%d' % (dims, l), cw.cmd_trace(dims, l))
for (m, n), want in sorted(HE.items()):
    if (m, n) == (5, 5):
        continue
    if quick and (m, n) == (5, 4):
        print('SKIP (5,4) (CW_QUICK=1)')
        continue
    t0 = time.time()
    best = cw.cmd_iter([m, n], 4)
    b = best[4][0]
    got = cw.ceil6(b)
    report('(%d,%d) p=4: bound %.10f, rounded up %s, He %s' % (m, n, b, got, want), got == Decimal(want), '%.0fs' % (time.time() - t0))
if len(sys.argv) > 1:
    # output of: cwsec iter 5 5 2
    rows = {}
    for line in open(sys.argv[1]):
        t = line.split()
        if t and t[0] == 'ITER':
            d = dict(x.split('=') for x in t[1:5])
            if d['p'] == '2':
                num, den = d['ratio'].split('/')
                rows[int(d['sector'])] = (int(num), int(den), int(d['u']))
    bs = {i: cw.bound_from_ratio(n_, d_, 50) for i, (n_, d_, u) in rows.items()}
    mx = max(bs.values())
    arg = max(bs, key=lambda i: bs[i])
    report('(5,5) p=2: %d sectors, maximum %.10f in sector %d, rounded up %s, He %s' % (len(rows), mx, arg, cw.ceil6(mx), HE[(5, 5)]),
           len(rows) == 13 and cw.ceil6(mx) == Decimal(HE[(5, 5)]))
print('ALL CHECKS PASS' if ok_all else 'SOME CHECK FAILED')
sys.exit(0 if ok_all else 1)
