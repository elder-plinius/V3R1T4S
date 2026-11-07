#!/usr/bin/env python3
"""compare_values.py CHECKER_OUTPUT VALUES_FILE [NMIN NMAX]
Reads the lines of ros_cert_check.py's output ("n<k>.json: n=k ... P000=num/den ... PASS") and compares every
P000 with the line "k num/den" of VALUES_FILE, for k in [NMIN, NMAX] (default 16..30). Exit 0 iff every term in
the range is present, PASSed, and equal (as reduced fractions)."""
import sys, re
from fractions import Fraction
out, vals = sys.argv[1], sys.argv[2]
nmin = int(sys.argv[3]) if len(sys.argv) > 3 else 16
nmax = int(sys.argv[4]) if len(sys.argv) > 4 else 30
expected = {}
for line in open(vals):
    p = line.split()
    if len(p) == 2 and '/' in p[1]:
        expected[int(p[0])] = Fraction(p[1])
got = {}
for line in open(out):
    m = re.match(r"n(\d+)\.json: n=(\d+) positions_checked=(\d+) P000=(\d+)/(\d+).*\bPASS\b", line.strip())
    if m:
        n = int(m.group(2)); got[n] = (Fraction(int(m.group(4)), int(m.group(5))), int(m.group(3)))
ok = True
for n in range(nmin, nmax + 1):
    if n not in got:
        print("n=%d: no PASS line in checker output" % n); ok = False; continue
    v, cnt = got[n]
    if cnt != n * n * (n + 1) // 2:
        print("n=%d: positions_checked %d != n^2(n+1)/2" % (n, cnt)); ok = False
    if n not in expected or expected[n] != v:
        print("n=%d: P000 differs from values file" % n); ok = False
    else:
        print("n=%d: PASS, P000 equals values file (%d digits / %d digits)" % (n, len(str(v.numerator)), len(str(v.denominator))))
print("compare_values: %s" % ("ALL_EQUAL" if ok else "MISMATCH"))
sys.exit(0 if ok else 1)
