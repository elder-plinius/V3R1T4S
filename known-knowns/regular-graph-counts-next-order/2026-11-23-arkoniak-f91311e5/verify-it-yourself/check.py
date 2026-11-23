#!/usr/bin/env python3
"""Standalone check of A006822(25) (connected unlabeled 6-regular graphs on 25 vertices).

Definition. U(N) = number of unlabeled 6-regular simple graphs on N vertices = (1/N!) sum_{g in S_N} Fix(g)
(Burnside), Fix(g) = number of labeled 6-regular graphs on {1..N} fixed by g, which depends only on the cycle type
lambda of g: U(N) = sum_lambda F(lambda)/z_lambda, z_lambda = prod_k k^{c_k} c_k!. Connected counts C(N) by the
inverse Euler transform: 1 + sum_N U(N) x^N = prod_N (1 - x^N)^(-C(N)).

Checks: (1) object/F_N25.txt has exactly one value per cycle type of 25 (all 1958 partitions);
(2) every value equals method A's F_A(lambda) recomputed here (how-we-built-it/methodA/engine.py, a few minutes);
(3) sum F/z_lambda is an integer U(25); (4) with the published A165627(1..24) (U(n), OEIS) the inverse Euler
transform gives C(25) equal to object/A006822_25.txt, and C(n) equal to the published A006822(1..24).
Last line PASS or FAIL."""
import sys, os
sys.dont_write_bytecode = True
from fractions import Fraction
from math import factorial
from collections import Counter
here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
# OEIS A165627 (n=1..24, all 6-regular graphs on n vertices) and A006822 (n=1..24, connected), as published
A165627 = [0, 0, 0, 0, 0, 0, 1, 1, 4, 21, 266, 7849, 367860, 21609301, 1470293676, 113314233813, 9799685588961, 945095823831333, 101114579937196179, 11945375659140003692, 1551593789610531820695, 220716215902794066709555, 34259321384370735003091907, 5782740798229835127025560294]
A006822 = [0, 0, 0, 0, 0, 0, 1, 1, 4, 21, 266, 7849, 367860, 21609300, 1470293675, 113314233808, 9799685588936, 945095823831036, 101114579937187980, 11945375659139626688, 1551593789610509806552, 220716215902792573134799, 34259321384370620122314325, 5782740798229825207562109439]
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
for ln in open(os.path.join(pkg, 'object', 'F_N25.txt')):
    p, v = ln.strip().split(';'); lam = tuple(map(int, p.split()))
    if lam in F: print('duplicate type', p); ok = False
    F[lam] = int(v)
allp = set(parts(25))
print(f'(1) types in object: {len(F)}, partitions of 25: {len(allp)}, equal sets: {set(F) == allp}'); ok &= set(F) == allp
sys.path.insert(0, os.path.join(pkg, 'how-we-built-it', 'methodA')); import engine as E
E.set_degree(6); bad = sum(1 for lam in allp if E.F_A(lam) != F.get(lam))
print(f'(2) types where method A differs from the object values: {bad}'); ok &= bad == 0
S = sum(Fraction(v, z(lam)) for lam, v in F.items())
print(f'(3) U(25) = {S} integer: {S.denominator == 1}'); ok &= S.denominator == 1
U = [0] * 26; U[0] = 1
for n in range(1, 25): U[n] = A165627[n - 1]
U[25] = int(S)
c = [0] * 26
for n in range(1, 26): c[n] = n * U[n] - sum(c[k] * U[n - k] for k in range(1, n))
def mu(n):
    r, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r
C = [0] * 26
for n in range(1, 26):
    s = sum(mu(n // d) * c[d] for d in range(1, n + 1) if n % d == 0); assert s % n == 0; C[n] = s // n
pub = all(C[n] == A006822[n - 1] for n in range(1, 25))
print(f'(4) C(n) == published A006822(1..24): {pub}'); ok &= pub
obj = [l.split() for l in open(os.path.join(pkg, 'object', 'A006822_25.txt')) if not l.startswith('#') and l.strip()]
val = int(obj[0][1]) if obj and obj[0][0] == '25' else None
print(f'    C(25) = {C[25]}, object A006822(25) = {val}, equal: {C[25] == val}'); ok &= C[25] == val
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
