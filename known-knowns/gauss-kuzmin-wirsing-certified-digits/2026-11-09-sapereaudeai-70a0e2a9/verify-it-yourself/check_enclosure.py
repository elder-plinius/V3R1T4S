#!/usr/bin/env python3
"""Re-certify the enclosure of lambda_2 and check the object files. Run from the package folder:
    python verify-it-yourself/check_enclosure.py            (or: python verify-it-yourself/check_enclosure.py --write)
Needs python-flint 0.9.0. Steps:
 1. joins object/v_N2800.part1.txt ... object/v_N2800.part4.txt (split only to keep each file under 1 MB) and requires
    the sha256 of the joined bytes to be cc6beb453558cfead1420c2d3cb5f4c54f83106c8417129e2bd09e08be17882a;
 2. runs the rigorous certifier verify-it-yourself/gkw_cert.py (Arb ball arithmetic; proof in object/PROOF.md) on that
    vector and object/mu_N2800.txt at 3900 bits (K 80, J 11200, r0 0.01, rho 0.2, Q2 64, Qrho 256);
 3. requires isolation_ok (exactly 80 eigenvalue balls of the section, 1 inside |z - mu| = r0, 2 outside |z| = rho)
    and D >= 842;
 4. recomputes the outward-rounded decimal endpoints (860 places) of C_83 = -lambda_2 and requires them to equal
    object/C83_enclosure.txt exactly;
 5. requires |(-mu) - Nisoli's 175-digit centre| <= radius + 10^-175 (the-record-we-beat/nisoli_centre_175.txt).
Last line: PASS or FAIL. With --write it (re)writes object/C83_enclosure.txt instead of comparing (author's use only)."""
import os, sys, json, re, hashlib, tempfile
from decimal import Decimal

here = os.path.dirname(os.path.abspath(__file__))
pkg = os.path.dirname(here)
sys.path.insert(0, here)
D_CLAIM = 842
P = 860
V_SHA = 'cc6beb453558cfead1420c2d3cb5f4c54f83106c8417129e2bd09e08be17882a'


def fail(msg):
    print('problem:', msg)
    print('FAIL')
    sys.exit(1)


try:
    from flint import arb, fmpq, ctx
    import gkw_cert
except Exception as e:  # noqa
    fail('python-flint not available (%s)' % e)

tmp = tempfile.mkdtemp(prefix='gkw_recert_')
parts = [os.path.join(pkg, 'object', 'v_N2800.part%d.txt' % i) for i in (1, 2, 3, 4)]
try:
    data = b''.join(open(p, 'rb').read() for p in parts)
except OSError as e:
    fail('cannot read the vector parts: %s' % e)
if hashlib.sha256(data).hexdigest() != V_SHA:
    fail('joined vector sha256 differs from %s' % V_SHA)
vfile = os.path.join(tmp, 'v_N2800.txt')
open(vfile, 'wb').write(data)
mufile = os.path.join(pkg, 'object', 'mu_N2800.txt')
out = os.path.join(tmp, 'recert_S1.json')
try:
    gkw_cert.cmd_certify(vfile, mufile, 80, 3900, 11200, '0.01', '0.2', 64, 256, out)
except SystemExit as e:
    fail('certifier stopped: %s' % e)
except Exception as e:  # noqa
    fail('certifier error: %r' % e)
cert = json.load(open(out))
if not cert.get('isolation_ok') or cert.get('n_eig_total') != 80:
    fail('isolation/counting not certified')
D = cert['certified_D']
if D < D_CLAIM:
    fail('certified decimals %d < %d' % (D, D_CLAIM))
ctx.prec = cert['prec']
mu = arb(open(mufile).read().split()[0]).mid()
man, ex = mu.man_exp()
man, ex = int(man), int(ex)
muq = fmpq(man) * fmpq(2) ** ex if ex >= 0 else fmpq(man, 2 ** (-ex))
m = re.match(r'\[([0-9.e+-]+) \+/- ([0-9.e+-]+)\]', cert['radius'])
if not m:
    fail('cannot parse radius %s' % cert['radius'])
rad = (fmpq(*Decimal(m.group(1)).as_integer_ratio()) + fmpq(*Decimal(m.group(2)).as_integer_ratio())) * fmpq(1001, 1000)
if not rad < fmpq(1, 10 ** D_CLAIM):
    fail('radius not below 10^-%d' % D_CLAIM)
lo_s = '0.' + str(((-muq - rad) * 10 ** P).floor()).rjust(P, '0')
hi_s = '0.' + str(((-muq + rad) * 10 ** P).floor() + 1).rjust(P, '0')
encl = os.path.join(pkg, 'object', 'C83_enclosure.txt')
if '--write' in sys.argv:
    with open(encl, 'w', newline='\n') as f:
        f.write('lower %s\nupper %s\ncertified_decimals %d\n' % (lo_s, hi_s, D_CLAIM))
    print('wrote', encl)
obj = {}
for line in open(encl):
    p = line.split()
    if len(p) == 2:
        obj[p[0]] = p[1]
if obj.get('lower') != lo_s or obj.get('upper') != hi_s:
    fail('object/C83_enclosure.txt endpoints differ from the recomputed certified enclosure')
if obj.get('certified_decimals') != str(D_CLAIM):
    fail('object/C83_enclosure.txt certified_decimals is not %d' % D_CLAIM)
lo, hi = fmpq(int(lo_s[2:]), 10 ** P), fmpq(int(hi_s[2:]), 10 ** P)
if not (hi - lo < fmpq(2, 10 ** D_CLAIM)):
    fail('object endpoints are not within 2 x 10^-%d of each other' % D_CLAIM)
nis = open(os.path.join(pkg, 'the-record-we-beat', 'nisoli_centre_175.txt')).read().split()[0]
nq = fmpq(int(nis[2:]), 10 ** (len(nis) - 2))
if not abs(-muq - nq) <= rad + fmpq(1, 10 ** 175):
    fail("centre does not agree with Nisoli's 175-digit centre within the two radii")
print('certified: |lambda_2 - mu| <= %s, D = %d; endpoints match object/C83_enclosure.txt; Nisoli centre agrees'
      % (cert['radius'], D))
print('PASS')
