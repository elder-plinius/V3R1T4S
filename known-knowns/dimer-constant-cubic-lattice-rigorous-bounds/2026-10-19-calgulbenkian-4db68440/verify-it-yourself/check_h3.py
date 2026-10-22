#!/usr/bin/env python3
"""Monomer-dimer entropy h3 upper bound from a Collatz-Wielandt vector.  Python 3.8+ standard library plus the C compiler
(cc) for the one heavy step.  Usage:  python3 -I check_h3.py M N certfile [expected_num expected_den]

1. trace identity tests of the monomer-dimer matrix definition (cwcheck.py, independent brute force on small quotient graphs);
2. the certificate (one value per orbit under all translations of Z/M x Z/N, plus the coordinate swap when M = N) is checked to be a
   genuine partition of all 2^(MN) states into orbits and expanded to every state;
3. mdlayer.c applies the FULL monomer-dimer matrix to the expanded vector (all 2^(MN) rows, no symmetry used);
4. a handful of rows are recomputed by a separate pure-Python permanent expansion;
5. max_U (T x)_U / x_U is found by exact cross multiplication; the bound is log(ratio)/(M N), rounded UP.
"""
import os, sys, struct, subprocess, random, time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import cwcheck as cw
from decimal import Decimal, getcontext

M, N = int(sys.argv[1]), int(sys.argv[2])
certpath = sys.argv[3]
exp = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else None
V = M * N
NS = 1 << V
ok_all = True
t0 = time.time()


def report(name, ok, extra=''):
    global ok_all
    ok_all = ok_all and ok
    print('%s %s %s' % ('PASS' if ok else 'FAIL', name, extra), flush=True)


report('trace identity: tr(TMD^l) = number of ALL matchings of the quotient graph, (2,2,4) (3,2,4) (2,2,6)',
       all([cw.cmd_trace(d, l) for d, l in (([2, 2], 4), ([3, 2], 4), ([2, 2], 6))]))

# ---- certificate: orbits and expansion
perms = []
for sw in ([False, True] if M == N else [False]):
    for tx in range(M):
        for ty in range(N):
            p = []
            for a in range(M):
                for b in range(N):
                    aa, bb = (b, a) if sw else (a, b)
                    p.append(((aa + tx) % M) * N + (bb + ty) % N)
            perms.append(p)


def image(mask, p):
    r = 0
    v = 0
    while mask:
        if mask & 1:
            r |= 1 << p[v]
        mask >>= 1
        v += 1
    return r


x = [0] * NS
lines = [l.split() for l in open(certpath) if l.strip() and not l.startswith('#')]
good = True
prev = -1
for k, (idn, mask, xv) in enumerate(lines):
    idn, mask, xv = int(idn), int(mask), int(xv)
    orb = set(image(mask, p) for p in perms)
    if idn != k or mask != min(orb) or mask <= prev or xv <= 0:
        good = False
        print('bad line', k, idn, mask)
        break
    prev = mask
    for o in orb:
        if x[o]:
            good = False
            print('orbit overlap at', o)
            break
        x[o] = xv
    if not good:
        break
good = good and all(v > 0 for v in x)
report('certificate lines are exactly the orbits of the %d-element group (canonical = minimum mask), cover all %d states, all values positive; %d orbits' % (len(perms), NS, len(lines)), good)
if not good:
    print('SOME CHECK FAILED')
    sys.exit(1)

# ---- heavy step in C
tmp = os.environ.get('H3_TMP', os.path.join(here, '_tmp'))
os.makedirs(tmp, exist_ok=True)
xbin, outbin, exe = [os.path.join(tmp, n) for n in ('x.bin', 'tx.bin', 'mdlayer')]
with open(xbin, 'wb') as f:
    f.write(struct.pack('<%dQ' % NS, *x))
subprocess.check_call(['cc', '-O2', '-o', exe, os.path.join(here, 'mdlayer.c')])
t1 = time.time()
subprocess.check_call([exe, str(M), str(N), xbin, outbin])
t_c = time.time() - t1
raw = open(outbin, 'rb').read()
w = struct.unpack('<%dQ' % (2 * NS), raw)
tx = [w[2 * i] | (w[2 * i + 1] << 64) for i in range(NS)]
os.remove(xbin); os.remove(outbin); os.remove(exe)
try:
    os.rmdir(tmp)
except OSError:
    pass

# ---- independent pure-Python rows
def tgt(u):
    a, b = divmod(u, N)
    return (u, ((a + 1) % M) * N + b, a * N + (b + 1) % N)


def row_py(U):
    comp = [v for v in range(V) if not U >> v & 1]
    total = 0
    for sm in range(1 << len(comp)):
        S = [comp[j] for j in range(len(comp)) if sm >> j & 1]
        def rec(i, used):
            if i == len(S):
                return x[used]
            s = 0
            for t in tgt(S[i]):
                if not used >> t & 1:
                    s += rec(i + 1, used | 1 << t)
            return s
        total += rec(0, 0)
    return total


random.seed(1)
rows = [NS - 1]
while len(rows) < 40:
    k = random.randint(0, 7)
    U = NS - 1
    for v in random.sample(range(V), k):
        U &= ~(1 << v)
    rows.append(U)
report('40 sampled rows (including the all-ones state) agree with a separate pure-Python expansion of the permanent definition',
       all(row_py(U) == tx[U] for U in rows))

# ---- exact Collatz-Wielandt maximum
bu = 0
for U in range(1, NS):
    if tx[U] * x[bu] > tx[bu] * x[U]:
        bu = U
num, den = tx[bu], x[bu]
g = 1
a, b2 = num, den
while b2:
    a, b2 = b2, a % b2
num //= a; den //= a
print('RESULT mdcert dims=%d,%d states=%d orbits=%d argmax_state=%d ratio=%d/%d' % (M, N, NS, len(lines), bu, num, den))
getcontext().prec = 60
r = Decimal(num) / Decimal(den)
b = r.ln() / V
# outward rounding of the (approximate) logarithm: widen by 1e-40, then ceil
up7 = ((b + Decimal(10) ** -40) * 10 ** 7).to_integral_value(rounding='ROUND_CEILING') / 10 ** 7
print('ratio decimal (15 places) = %s' % str(r.quantize(Decimal(10) ** -15)))
print('log(ratio)/%d = %s   (12 places, rounded up: %s; 7 places, rounded up: %s)' % (V, str(b)[:20], ((b + Decimal(10) ** -40) * 10 ** 12).to_integral_value(rounding='ROUND_CEILING') / 10 ** 12, up7))
if exp:
    report('exact ratio %d/%d' % exp, num * exp[1] == exp[0] * den)
if len(sys.argv) > 6:
    report('claimed 7-place bound %s' % sys.argv[6], up7 == Decimal(sys.argv[6]))
fk = Decimal('0.7862023450')
report('h3 <= %s is below FKLM %s by %s (needed: at least 1e-6)' % (up7, fk, fk - up7), fk - up7 >= Decimal('0.000001'))
print('elapsed seconds: total %.1f, of which C matrix-vector step %.1f' % (time.time() - t0, t_c))
print('ALL CHECKS PASS' if ok_all else 'SOME CHECK FAILED')
sys.exit(0 if ok_all else 1)
