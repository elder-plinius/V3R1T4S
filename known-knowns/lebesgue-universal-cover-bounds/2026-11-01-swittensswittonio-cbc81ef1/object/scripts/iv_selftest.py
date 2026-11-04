import sys
from fractions import Fraction as F
from mpmath import mp, mpf, sin, cos, sqrt
mp.dps = 60
bad = 0; n = 0; byop = {}
for line in open(sys.argv[1]):
    op, *v = line.split(); v = [float(x) for x in v]; n += 1
    al, ah, bl, bh, rl, rh = v
    A = [F(al), F(ah)]; B = [F(bl), F(bh)]; ok = True
    if op in ('add', 'sub', 'mul'):
        f = {'add': lambda p, q: p + q, 'sub': lambda p, q: p - q, 'mul': lambda p, q: p * q}[op]
        vals = [f(p, q) for p in A for q in B]; ok = F(rl) <= min(vals) and F(rh) >= max(vals)
    elif op == 'sqr':
        lo = min(abs(A[0]), abs(A[1])) ** 2 if A[0] * A[1] > 0 else F(0); hi = max(abs(A[0]), abs(A[1])) ** 2
        ok = F(rl) <= lo and F(rh) >= hi
    elif op == 'div':
        vals = [p / q for p in A for q in B]; ok = F(rl) <= min(vals) and F(rh) >= max(vals)
    elif op == 'sqrt':
        ok = (rl <= 0 or F(rl) ** 2 <= A[0]) and F(rh) ** 2 >= A[1]
    elif op in ('sin', 'cos'):
        t = (sin if op == 'sin' else cos)(mpf(al)); ok = mpf(rl) <= t <= mpf(rh) and (float(rh) - float(rl)) < 1e-13
    elif op in ('sinI', 'cosI'):
        g = sin if op == 'sinI' else cos
        ts = [g(mpf(al)), g(mpf(ah))]; ok = mpf(rl) <= min(ts) and mpf(rh) >= max(ts)
    byop[op] = byop.get(op, 0) + 1
    if not ok: bad += 1; print('VIOLATION', line.strip())
print('checked', n, 'violations', bad, byop)
