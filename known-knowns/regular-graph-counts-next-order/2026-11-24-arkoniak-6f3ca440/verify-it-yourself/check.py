#!/usr/bin/env python3
"""Standalone check of A006821(15) (connected unlabeled 5-regular graphs on 30 vertices; OEIS index n = vertices/2).

Definition. U(N) = number of unlabeled 5-regular simple graphs on N vertices = (1/N!) sum_{g in S_N} Fix(g)
(Burnside), Fix(g) = number of labeled 5-regular graphs on {1..N} fixed by g, which depends only on the cycle type
lambda of g: U(N) = sum_lambda F(lambda)/z_lambda, z_lambda = prod_k k^{c_k} c_k!. With a(n) = U(2n) (A165626) the
connected counts C(n) (A006821) follow by the inverse Euler transform: 1 + sum_n a(n) x^n = prod_n (1 - x^n)^(-C(n)).

Checks: (1) object/F_N30.txt (method D) has exactly one value per cycle type of 30 (all 5604 partitions);
(2) sum F/z_lambda is an integer U(30); (3) method A (how-we-built-it/methodA: C histogram recurrence, CRT), built
and run here (about 4 min on one core), gives the same U(30); (4) with the published A165626(0..14) the inverse
Euler transform gives C(n) == published A006821(1..14) and C(15) == object/A006821_15.txt. Last line PASS or FAIL."""
import sys, os, subprocess, tempfile
sys.dont_write_bytecode = True
from fractions import Fraction
from math import factorial
from collections import Counter
here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
# OEIS A165626 (n=0..14: all 5-regular graphs on 2n vertices) and A006821 (n=0..14, connected), as published
A165626 = [1, 0, 0, 1, 3, 60, 7849, 3459386, 2585136741, 2807105258926, 4221456120848125, 8516994772686533749, 22470883220896245217626, 75883288448434648617038134, 322040154712674550886226182668]
A006821 = [1, 0, 0, 1, 3, 60, 7848, 3459383, 2585136675, 2807105250897, 4221456117363365, 8516994770090547979, 22470883218081146186209, 75883288444204588922998674, 322040154704144697047052726990]
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for k in range(min(n, mx), 0, -1):
        for r in parts(n - k, k): yield (k,) + r
def z(lam):
    r = 1
    for k, c in Counter(lam).items(): r *= k ** c * factorial(c)
    return r
ok = True
F = {}
for ln in open(os.path.join(pkg, 'object', 'F_N30.txt')):
    p, v = ln.strip().split(';'); lam = tuple(map(int, p.split()))
    if lam in F: print('duplicate type', p); ok = False
    F[lam] = int(v)
allp = set(parts(30))
print(f'(1) types in object: {len(F)}, partitions of 30: {len(allp)}, equal sets: {set(F) == allp}'); ok &= set(F) == allp
S = sum(Fraction(v, z(lam)) for lam, v in F.items())
print(f'(2) U_D(30) = {S} integer: {S.denominator == 1}'); ok &= S.denominator == 1
mA = os.path.join(pkg, 'how-we-built-it', 'methodA')
with tempfile.TemporaryDirectory() as td:
    subprocess.run(['gcc', '-O2', '-o', os.path.join(td, 'cubic'), os.path.join(mA, 'cubic.c')], check=True)
    out = subprocess.run([sys.executable, '-I', os.path.join(mA, 'driver.py'), '--bin', os.path.join(td, 'cubic'), '--deg', '5',
                          '--nmax', '30', '--nprimes', '8', '--pivot', 'max', '--dumpU'], capture_output=True, text=True).stdout
UA = None
for l in out.splitlines():
    f = l.split()
    if len(f) >= 2 and f[0] == '30' and f[1].isdigit(): UA = int(f[1])
print(f'(3) U_A(30) by method A = {UA}, equal to U_D(30): {UA == S}'); ok &= UA == S
a = A165626[:] + [int(S)]
c = [0] * 16
for n in range(1, 16): c[n] = n * a[n] - sum(c[k] * a[n - k] for k in range(1, n))
def mu(n):
    r, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r
C = [0] * 16
for n in range(1, 16):
    s = sum(mu(n // d) * c[d] for d in range(1, n + 1) if n % d == 0); assert s % n == 0; C[n] = s // n
pub = all(C[n] == A006821[n] for n in range(1, 15))
print(f'(4) C(n) == published A006821(1..14): {pub}'); ok &= pub
obj = [l.split() for l in open(os.path.join(pkg, 'object', 'A006821_15.txt')) if not l.startswith('#') and l.strip()]
val = int(obj[0][1]) if obj and obj[0][0] == '15' else None
print(f'    C(15) = {C[15]}, object A006821(15) = {val}, equal: {C[15] == val}'); ok &= C[15] == val
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
