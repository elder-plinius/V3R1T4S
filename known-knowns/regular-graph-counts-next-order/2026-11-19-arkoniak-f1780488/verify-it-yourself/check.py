#!/usr/bin/env python3
"""Standalone check of A002851(21) (connected unlabeled cubic graphs on 42 vertices).

Definition. U(N) = number of unlabeled 3-regular simple graphs on N vertices = (1/N!) sum_{g in S_N} Fix(g)
(Burnside), Fix(g) = number of labeled cubic graphs on {1..N} fixed by g, which depends only on the cycle type
lambda of g: U(N) = sum_lambda F(lambda)/z_lambda, z_lambda = prod_k k^{c_k} c_k!. Connected counts C(N) by the
inverse Euler transform: 1 + sum_N U(N) x^N = prod_N (1 - x^N)^(-C(N)).

Checks: (1) object/F_N42_part*.txt has exactly one value per cycle type of 42 (all 53174 partitions);
(2) every value equals method A's F_A(lambda) recomputed here (how-we-built-it/methodA/engine.py, ~15 s);
(3) sum F/z_lambda is an integer U(42); (4) with the published A005638(1..20) (U(2n), n<=20, OEIS) the inverse Euler
transform gives C(42) equal to object/A002851_21.txt, and C(2n) equal to the published A002851(1..20).
Last line PASS or FAIL."""
import sys, os, glob
sys.dont_write_bytecode = True
from fractions import Fraction
from math import factorial
from collections import Counter
here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
# OEIS A005638 (n=1..20, all cubic graphs on 2n vertices) and A002851 (n=1..20, connected), as published
A005638 = [0, 1, 2, 6, 21, 94, 540, 4207, 42110, 516344, 7373924, 118573592, 2103205738, 40634185402, 847871397424, 18987149095005, 454032821688754, 11544329612485981, 310964453836198311, 8845303172513781271]
A002851 = [0, 1, 2, 5, 19, 85, 509, 4060, 41301, 510489, 7319447, 117940535, 2094480864, 40497138011, 845480228069, 18941522184590, 453090162062723, 11523392072541432, 310467244165539782, 8832736318937756165]
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
for fn in sorted(glob.glob(os.path.join(pkg, 'object', 'F_N42_part*.txt'))):
    for ln in open(fn):
        p, v = ln.strip().split(';'); lam = tuple(map(int, p.split()))
        if lam in F: print('duplicate type', p); ok = False
        F[lam] = int(v)
allp = set(parts(42))
print(f'(1) types in object: {len(F)}, partitions of 42: {len(allp)}, equal sets: {set(F) == allp}'); ok &= set(F) == allp
sys.path.insert(0, os.path.join(pkg, 'how-we-built-it', 'methodA')); import engine as E
E.set_degree(3); bad = sum(1 for lam in allp if E.F_A(lam) != F.get(lam))
print(f'(2) types where method A differs from the object values: {bad}'); ok &= bad == 0
S = sum(Fraction(v, z(lam)) for lam, v in F.items())
print(f'(3) U(42) = {S} integer: {S.denominator == 1}'); ok &= S.denominator == 1
U = [0] * 43; U[0] = 1
for n in range(1, 21): U[2 * n] = A005638[n - 1]
U[42] = int(S)
c = [0] * 43
for n in range(1, 43): c[n] = n * U[n] - sum(c[k] * U[n - k] for k in range(1, n))
def mu(n):
    r, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r
C = [0] * 43
for n in range(1, 43):
    s = sum(mu(n // d) * c[d] for d in range(1, n + 1) if n % d == 0); assert s % n == 0; C[n] = s // n
pub = all(C[2 * n] == A002851[n - 1] for n in range(1, 21)) and all(C[n] == 0 for n in range(1, 43, 2))
print(f'(4) C(2n) == published A002851(1..20): {pub}'); ok &= pub
obj = [l.split() for l in open(os.path.join(pkg, 'object', 'A002851_21.txt')) if not l.startswith('#') and l.strip()]
val = int(obj[0][1]) if obj and obj[0][0] == '21' else None
print(f'    C(42) = {C[42]}, object A002851(21) = {val}, equal: {C[42] == val}'); ok &= C[42] == val
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
