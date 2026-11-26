#!/usr/bin/env python3
"""Inverse Euler check of method-D sums: read 'd=D N=.. types=.. U_D=X ...' lines from Dsum_check files, take U_D(N) for
every N the degree allows (N*D even, N > D; U=1 at N=0, 0 elsewhere below), compute the connected counts by the inverse
Euler transform and compare with a b-file of the connected sequence (index = N, or N/2 with --half for odd D).
Usage: dbfcheck.py D NMAX BFILE [--half] CHECKFILE..."""
import sys, re
from fractions import Fraction
D, NMAX, BF = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
half = '--half' in sys.argv; files = [x for x in sys.argv[4:] if x != '--half']
step = 2 if half else 1
UD = {}
for fn in files:
    for ln in open(fn):
        m = re.match(rf'd={D} N=(\d+) types=\d+ U_D=(\d+) ', ln)
        if m: UD[int(m.group(1))] = int(m.group(2))
need = [N for N in range(step, NMAX + 1, step) if (N * D) % 2 == 0 and N > D]
miss = [N for N in need if N not in UD]
if miss:
    print(f'd={D} bfile INCOMPLETE missing N={miss}'); sys.exit(0)
n = NMAX // step
u = [1] + [UD.get(step * i, 0) for i in range(1, n + 1)]
b = [0] * (n + 1); c = [0] * (n + 1)
for k in range(1, n + 1):
    b[k] = k * u[k] - sum(b[j] * u[k - j] for j in range(1, k))
    c[k] = Fraction(b[k] - sum(e * c[e] for e in range(1, k) if k % e == 0), k)
    assert c[k].denominator == 1
ref = {}
for ln in open(BF):
    f = ln.split()
    if len(f) == 2 and not ln.startswith('#'): ref[int(f[0])] = int(f[1])
chk = mism = 0
for k in range(1, n + 1):
    if k in ref:
        chk += 1
        if ref[k] != int(c[k]): mism += 1; print(f'MISMATCH N={step*k} bfile={ref[k]} D={int(c[k])}')
print(f'd={D} NMAX={NMAX} C_D(N={step*n})={int(c[n])} bfile_checked={chk} MISMATCH {mism}')
sys.exit(0 if mism == 0 else 5)
