#!/usr/bin/env python3
"""Standalone checker for one spherical-code cell (Python standard library only).

Definition (bank target spherical-codes-cohn-table):
  N vectors in R^d given to >= 20 digits; normalise each to unit length; c* is the
  maximum pairwise inner product of the normalised vectors (cosine of the minimal
  angle). The cell is beaten when table - c* >= 1e-10, where table is the 12-decimal
  cosine of row (d, N) in https://spherical-codes.org/plain. If 9 <= d <= 23 and
  c* <= 0.5 the configuration is a kissing configuration and is not counted.

Usage: python3 check_sph.py OBJECT_FILE d N TABLE_VALUE
Inner products and squared norms are exact (fractions.Fraction); the cosine
<x_i, x_j> / sqrt(|x_i|^2 |x_j|^2) is evaluated with decimal at 50 digits.
Last output line: PASS or FAIL.
"""
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50


def fail(msg):
    print("error: " + msg)
    print("FAIL")
    sys.exit(1)


def to_dec(q, prec=60):
    getcontext().prec = prec
    v = Decimal(q.numerator) / Decimal(q.denominator)
    getcontext().prec = 50
    return v


def main():
    if len(sys.argv) != 5:
        fail("usage: check_sph.py OBJECT_FILE d N TABLE_VALUE")
    path, d, n_expected, table_s = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    pts = []
    min_digits = None
    with open(path, encoding="ascii") as f:
        for ln, line in enumerate(f, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            toks = s.split()
            if len(toks) != d:
                fail("line %d: expected %d coordinates, found %d" % (ln, d, len(toks)))
            row = []
            for t in toks:
                try:
                    dv = Decimal(t)
                except Exception:
                    fail("line %d: token is not a decimal" % ln)
                if not dv.is_finite():
                    fail("line %d: token is not finite" % ln)
                nd = len(dv.as_tuple().digits)
                if dv != 0:
                    min_digits = nd if min_digits is None else min(min_digits, nd)
                row.append(Fraction(dv))
            pts.append(row)
    n = len(pts)
    if n != n_expected:
        fail("found %d vectors, expected N = %d" % (n, n_expected))
    norms2 = [sum(x * x for x in p) for p in pts]
    if any(q == 0 for q in norms2):
        fail("zero vector")
    cmax = None
    arg = None
    for i in range(n):
        a = pts[i]
        for j in range(i + 1, n):
            b = pts[j]
            dot = sum(a[k] * b[k] for k in range(d))
            num = to_dec(dot)
            den = to_dec(norms2[i] * norms2[j]).sqrt()
            c = num / den
            if cmax is None or c > cmax:
                cmax, arg = c, (i + 1, j + 1)
    table = Decimal(table_s)
    margin = table - cmax
    kissing = (9 <= d <= 23) and cmax <= Decimal("0.5")
    print("d = %d, N = %d, minimum significant digits per nonzero coordinate = %s" % (d, n, min_digits))
    print("c* = %s (pair %d, %d)" % (cmax, arg[0], arg[1]))
    print("minimal angle (degrees, float display) = %.13f" % math.degrees(math.acos(float(cmax))))
    print("table = %s" % table_s)
    print("table - c* = %s" % margin)
    print("margin >= 1e-10: %s; kissing range: %s; digits >= 20: %s" % (margin >= Decimal("1e-10"), kissing, (min_digits or 0) >= 20))
    ok = margin >= Decimal("1e-10") and not kissing and (min_digits or 0) >= 20
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
