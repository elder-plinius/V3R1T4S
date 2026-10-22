#!/usr/bin/env python
"""Standalone stdlib checker for the N=4141 claim (no third-party packages).

Definition (from the bank criterion): r* = min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ),
computed at >= 50 significant digits directly from the submitted coordinates. Two passes:
double-precision math locates the binding pairs and norms, then decimal (60 digits) recomputes
exactly those quantities from the coordinate strings.

Usage (from this claim folder): python verify_standalone.py
Last line: PASS or FAIL.
"""
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

N = 4141
TABLE = "0.014601755763187308074373236782"  # row 4141 of radius.txt in this folder
THRESH = Decimal("1e-11")


def load(path):
    pts = []
    with open(path) as f:
        for line in f:
            s = line.split()
            if len(s) >= 2:
                pts.append((s[0], s[1]))  # keep the STRINGS for exact decimal input
    return pts


def main():
    pts = load("candidate_N4141.txt")
    if len(pts) != N:
        print(f"FAIL: expected {N} centres, found {len(pts)}")
        return 1
    fx = [float(x) for x, _ in pts]
    fy = [float(y) for _, y in pts]
    # double pass: binding pairs (near-min distance) and binding norms (near-max)
    dmin = min((fx[i] - fx[j]) ** 2 + (fy[i] - fy[j]) ** 2
               for i in range(N) for j in range(i)) ** 0.5
    pairs = [(i, j) for i in range(N) for j in range(i)
             if ((fx[i] - fx[j]) ** 2 + (fy[i] - fy[j]) ** 2) ** 0.5 < dmin * (1 + 1e-9)]
    nmax = max((x * x + y * y) ** 0.5 for x, y in zip(fx, fy))
    nidx = [k for k in range(N) if (fx[k] ** 2 + fy[k] ** 2) ** 0.5 > nmax * (1 - 1e-9)]

    hp_min = min(((Decimal(pts[i][0]) - Decimal(pts[j][0])) ** 2 +
                  (Decimal(pts[i][1]) - Decimal(pts[j][1])) ** 2).sqrt() for i, j in pairs)
    hp_max = max((Decimal(pts[k][0]) ** 2 + Decimal(pts[k][1]) ** 2).sqrt() for k in nidx)
    r_star = min(hp_min / 2, Decimal(1) - hp_max)
    table = Decimal(TABLE)
    margin = r_star - table
    print(f"N = {len(pts)}")
    print(f"r* (60-digit decimal, from coordinate strings) = {r_star}")
    print(f"table value (radius.txt row {N})                 = {table}")
    print(f"margin = {margin}  (threshold {THRESH})")
    ok = margin >= THRESH
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
