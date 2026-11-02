#!/usr/bin/env python3
"""Standalone checker for one hsp4 cell (Python standard library only).

Definition (bank target packomania-hyperspheres-hsp4-hsp6):
  N centres c_1..c_N in R^4, unit container ball centred at the origin,
  feasible radius r* = min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| ),
  computed directly from the coordinate strings with no tolerance.
  The cell is beaten when r* - table >= 1e-10, where table is the 12-decimal
  value of row N in https://packomania.com/hsp4/txt/radius.txt.

Usage: python3 check_hsp4.py OBJECT_FILE N TABLE_VALUE
Coordinates are read as exact decimals; squared distances and squared norms are
exact (fractions.Fraction); square roots are taken with decimal at 50 digits.
Last output line: PASS or FAIL.
"""
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50


def fail(msg):
    print("error: " + msg)
    print("FAIL")
    sys.exit(1)


def frac_sqrt(q):
    """sqrt of a non-negative Fraction, correctly rounded to 50 significant digits."""
    getcontext().prec = 60
    v = (Decimal(q.numerator) / Decimal(q.denominator))
    getcontext().prec = 50
    return +v.sqrt()


def main():
    if len(sys.argv) != 4:
        fail("usage: check_hsp4.py OBJECT_FILE N TABLE_VALUE")
    path, n_expected, table_s = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    pts = []
    with open(path, encoding="ascii") as f:
        for ln, line in enumerate(f, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            toks = s.split()
            if len(toks) != 4:
                fail("line %d: expected 4 coordinates, found %d" % (ln, len(toks)))
            try:
                row = [Fraction(Decimal(t)) for t in toks]
            except Exception:
                fail("line %d: token is not a finite decimal" % ln)
            pts.append(row)
    n = len(pts)
    if n != n_expected:
        fail("found %d centres, expected N = %d" % (n, n_expected))
    min_d2 = None
    arg = None
    for i in range(n):
        a = pts[i]
        for j in range(i + 1, n):
            b = pts[j]
            d2 = sum((a[k] - b[k]) ** 2 for k in range(4))
            if min_d2 is None or d2 < min_d2:
                min_d2, arg = d2, (i + 1, j + 1)
    max_n2 = max(sum(x * x for x in p) for p in pts)
    half_min = frac_sqrt(min_d2) / 2
    wall = Decimal(1) - frac_sqrt(max_n2)
    r = min(half_min, wall)
    table = Decimal(table_s)
    gain = r - table
    print("N = %d" % n)
    print("half min pair distance = %s (pair %d, %d)" % (half_min, arg[0], arg[1]))
    print("1 - max norm = %s" % wall)
    print("r* = %s" % r)
    print("table = %s" % table_s)
    print("gain = %s" % gain)
    ok = (max_n2 <= 1) and gain >= Decimal("1e-10")
    print("gain >= 1e-10: %s" % (gain >= Decimal("1e-10")))
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
