#!/usr/bin/env python3
"""Standalone 50-digit feasible-radius checker (Python standard library only).

Reads a Packomania-format centers file (one `index x y` per line, 30 decimals),
computes r* = min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) at 50 decimal
digits using the decimal module (exact parse of the decimal strings, no binary
float anywhere), and compares against the Packomania cci table value for N=3949.

Prints PASS or FAIL as the last line.
Runtime: a few minutes (7.8M pair checks in decimal arithmetic).
"""
import sys
from decimal import Decimal, getcontext

getcontext().prec = 50

TABLE = Decimal('0.014965462848801963307763269064')  # live cci N=3949 value
NEED = Decimal('1e-11')                              # strict-improvement bar


def load(path):
    pts = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) >= 3:
                pts.append((Decimal(p[1]), Decimal(p[2])))
    return pts


def main():
    pts = load(sys.argv[1])
    n = len(pts)
    if n != 3949:
        print('expected 3949 centers, got %d' % n)
        print('FAIL')
        return
    max_r2 = Decimal(0)
    min_d2 = None
    for i, (x1, y1) in enumerate(pts):
        r2 = x1 * x1 + y1 * y1
        if r2 > max_r2:
            max_r2 = r2
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx = x1 - x2
            dy = y1 - y2
            d2 = dx * dx + dy * dy
            if min_d2 is None or d2 < min_d2:
                min_d2 = d2
    r_star = min(min_d2.sqrt() / 2, 1 - max_r2.sqrt())
    margin = r_star - TABLE
    print('centers: %d' % n)
    print('r*     = %s' % r_star)
    print('table  = %s' % TABLE)
    print('margin = %.3e  (need >= 1e-11)' % margin)
    print('PASS' if margin >= NEED else 'FAIL')


if __name__ == '__main__':
    main()
