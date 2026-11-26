#!/usr/bin/env python3
"""Sum method-D values F_3(lambda)/z_lambda from runD lane files into U(N) (all cubic graphs on N
vertices) and compare with method A's U(N) (C engine terms file 'N U C'). Prints one verdict line."""
import sys
from fractions import Fraction
from math import factorial
from collections import Counter
N = int(sys.argv[1]); aterms = sys.argv[2]; lanes = sys.argv[3:]
def z(lam):
    r = 1
    for k, c in Counter(lam).items(): r *= k ** c * factorial(c)
    return r
seen = {}; bad = 0
for fn in lanes:
    for ln in open(fn):
        f = ln.strip().split(';')
        if len(f) < 4: continue
        if f[3] in ('TIMEOUT', 'ERR', 'MISMATCH'):
            if f[0] not in seen: bad += 1
            continue
        seen[f[0]] = int(f[1])
def np_(n, m=None):
    m = n if m is None else m
    if n == 0: return 1
    return sum(np_(n - k, k) for k in range(1, min(n, m) + 1))
need = np_(N)
UA = None
for ln in open(aterms):
    f = ln.split()
    if len(f) == 3 and f[0] == str(N): UA = int(f[1])
if len(seen) < need:
    print(f'N={N} INCOMPLETE types_done={len(seen)}/{need}'); sys.exit(0)
s = sum(Fraction(v, z(tuple(map(int, p.split())))) for p, v in seen.items())
ok = s.denominator == 1 and int(s) == UA
print(f'N={N} types={len(seen)} U_D={s} U_A={UA} {"AGREE" if ok else "DISAGREE"}')
sys.exit(0 if ok else 4)
