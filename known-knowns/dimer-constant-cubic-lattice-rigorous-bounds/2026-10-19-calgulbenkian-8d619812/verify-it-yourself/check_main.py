#!/usr/bin/env python3
"""Claim check for the l3 upper bound at (5,5): standard library only.

Steps (each prints PASS or FAIL):
  1 reassemble the object from its parts and compare sha256 of every part and of the whole
  2 trace identity tr(T^l) = number of perfect matchings (brute force) on small quotients
  3 property C on the full matrices for (3,3)
  4 sector 12: rebuild the layer from the definition and recompute the exact ratio for the shipped vector
  5 sectors 0..11: same, for the builder-generated vectors in sectors/ (opt-in: CW_SMALL=1; default run checks sector 12 only)
  6 the maximum over the 13 sectors, rounded outward, against the claimed 0.452010
Environment: CW_PROCS = worker processes (default: number of CPUs).
"""
import os, sys, hashlib, tempfile, time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import cwcheck as cw
from decimal import Decimal

claim = os.path.dirname(here)
obj = os.path.join(claim, 'object')
procs = int(os.environ.get('CW_PROCS', os.cpu_count() or 1))
skip_small = os.environ.get('CW_SMALL') != '1'
ok_all = True


def report(name, ok, extra=''):
    global ok_all
    ok_all = ok_all and ok
    print('%s %s %s' % ('PASS' if ok else 'FAIL', name, extra), flush=True)


tmp = tempfile.mkdtemp()
out = os.path.join(tmp, 'cert_he_55_converged_sector12.txt')
try:
    # 1
    whole = hashlib.sha256()
    good = True
    with open(out, 'wb') as fo:
        for line in open(os.path.join(obj, 'PARTS.sha256')):
            t = line.split()
            if len(t) >= 2 and t[1].startswith('cert_he_55_converged_sector12.txt.part'):
                data = open(os.path.join(obj, t[1]), 'rb').read()
                good = good and hashlib.sha256(data).hexdigest() == t[0] and len(data) <= 900000
                fo.write(data)
                whole.update(data)
    want = '8d6198121bb490e8f44f352114144556fd75cc33aa98b4f698335ca274342661'
    report('object parts and whole sha256', good and whole.hexdigest() == want, whole.hexdigest())
    # 2 and 3
    t2 = all([cw.cmd_trace(d, l) for d, l in (([2, 2], 4), ([3, 2], 4), ([2, 2], 6))])
    report('trace identity tr(T^l) = matchings of the quotient graph', t2)
    report('property C on the full (3,3) matrices', cw.cmd_propc([3, 3]))
    # 4
    t0 = time.time()
    res = cw.cmd_certfull([5, 5], 12, out, procs)
    bounds = {}
    exp = (68004910275217693829986, 10405826313374)
    if res is None:
        report('sector 12 exact ratio', False)
    else:
        num, den, b = res
        report('sector 12 exact ratio equals 68004910275217693829986/10405826313374',
               num * exp[1] == exp[0] * den, '%.0fs' % (time.time() - t0))
        bounds[12] = b
    # 5
    if not skip_small:
        for i in range(11, -1, -1):
            r = cw.cmd_certfull([5, 5], i, os.path.join(here, 'sectors', 'vec_55_s%d.txt' % i), procs)
            if r is None:
                report('sector %d' % i, False)
            else:
                bounds[i] = r[2]
                report('sector %d exact ratio computed, bound %.10f' % (i, r[2]), True)
    # 6
    if len(bounds) == 13:
        mx = max(bounds.values())
        c6 = cw.ceil6(mx)
        report('maximum over 13 sectors %.10f, rounded up %s, claimed 0.452010; margin to He 0.452130 is %.7f'
               % (mx, c6, 0.452130 - float(mx)), c6 <= Decimal('0.452010') and bounds[12] == mx)
    else:
        print('NOTE default run: sectors 0..11 NOT checked in Python (set CW_SMALL=1, or use the C program, see REPRODUCE.md); sector 12 alone gives %.10f' % bounds.get(12, 0))
finally:
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
print('ALL CHECKS PASS' if ok_all else 'SOME CHECK FAILED')
sys.exit(0 if ok_all else 1)
