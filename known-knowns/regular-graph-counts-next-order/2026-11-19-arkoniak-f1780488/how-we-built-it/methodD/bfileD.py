#!/usr/bin/env python3
"""Method D b-file lane: U(N) = sum_lambda F_3(lambda)/z_lambda over all cycle types of N (D.F_D for
< symL long cycles, Dsym.F_Dsym otherwise), connected counts by the inverse Euler transform (own code),
compared with b002851 (connected cubic, index n = N/2) and b005638 (all cubic, index n = N/2).
Checkpoint: one line 'N U C' per finished N in --out; restart resumes after the last N."""
import sys, os, argparse
from fractions import Fraction
from math import factorial
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import D, Dsym
ap = argparse.ArgumentParser(); ap.add_argument('--nmax', type=int); ap.add_argument('--out')
ap.add_argument('--symL', type=int, default=8); ap.add_argument('--bconn'); ap.add_argument('--ball')
ap.add_argument('--lane', type=int, default=0); ap.add_argument('--lanes', type=int, default=1)
ap.add_argument('--other', default='')  # out files of the other lanes, read for the final check
a = ap.parse_args(); D.set_degree(3)
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for k in range(min(n, mx), 0, -1):
        for r in parts(n - k, k): yield (k,) + r
def z(lam):
    z = 1
    for k, c in Counter(lam).items(): z *= k ** c * factorial(c)
    return z
def bfile(p):
    b = {}
    for ln in open(p):
        f = ln.split()
        if len(f) == 2 and not ln.startswith('#'): b[int(f[0])] = int(f[1])
    return b
U = {0: 1}
for fn in [a.out] + [x for x in a.other.split(',') if x]:
    if not os.path.exists(fn): continue
    for ln in open(fn):
        f = ln.split()
        if len(f) == 3: U[int(f[0])] = int(f[1])
with open(a.out, 'a') as fo:
    for N in range(2, a.nmax + 1, 2):
        if N in U or (N // 2) % a.lanes != a.lane: continue
        s = Fraction(0)
        for lam in parts(N):
            L = sum(1 for x in lam if x >= 3)
            v = Dsym.F_Dsym(lam) if L >= a.symL else D.F_D(lam)
            s += Fraction(v, z(lam))
        assert s.denominator == 1, N
        U[N] = int(s); fo.write(f'{N} {U[N]} 0\n'); fo.flush()
for fn in [x for x in a.other.split(',') if x]:
    if os.path.exists(fn):
        for ln in open(fn):
            f = ln.split()
            if len(f) == 3: U[int(f[0])] = int(f[1])
if any(N not in U for N in range(0, a.nmax + 1, 2)):
    print('lane', a.lane, 'done; other lanes unfinished, no check yet'); sys.exit(0)
# inverse Euler in n = N/2: U(x) = exp(sum_k C(x^k)/k) -> C by the standard recurrence
n = a.nmax // 2; u = [U[2 * i] for i in range(n + 1)]
# a = Euler-inverse: n*u_n = sum_{k=1..n} b_k u_{n-k}, b_k = sum_{d|k} d*c_d
b = [0] * (n + 1); c = [0] * (n + 1)
for k in range(1, n + 1):
    b[k] = k * u[k] - sum(b[j] * u[k - j] for j in range(1, k))
    c[k] = Fraction(b[k] - sum(dd * c[dd] for dd in range(1, k) if k % dd == 0), k)
    assert c[k].denominator == 1
bc, ba = bfile(a.bconn), bfile(a.ball); mism = chk = 0
for k in range(1, n + 1):
    for name, val, ref in (('connected', int(c[k]), bc), ('all', u[k], ba)):
        if k in ref:
            chk += 1
            if ref[k] != val: mism += 1; print(f'MISMATCH {name} N={2*k} bfile={ref[k]} D={val}')
    print(f'N={2*k} U={u[k]} C={int(c[k])}')
print(f'checked={chk} MISMATCH {mism}')
