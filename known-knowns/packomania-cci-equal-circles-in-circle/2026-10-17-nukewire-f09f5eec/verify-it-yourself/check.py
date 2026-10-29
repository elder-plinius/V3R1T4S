#!/usr/bin/env python
"""Standalone checker for the packaged N=3307 claim. Python 3.8+, standard library only.

Checks: object sha256 (LF or CRLF-materialised form), exactly 3307 centres, and
r* = min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) at 60 significant digits from the
coordinate strings, exceeding the recorded table value by at least 1e-11.

Run from the package folder:  python verify-it-yourself/check.py
Last line: PASS or FAIL.
"""
import hashlib
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60

N = 3307
OBJECT = "object/candidate_N3307.txt"
OBJECT_SHA = "f09f5eecbb7b14f10607e97c3a74829129931cc0e0285e4372a5b4c4f61b0194"
TABLE = "0.016314899796158766989004378524"  # live radius.txt row 3307, fetched 2026-10-17T09:45:15Z
THRESH = Decimal("1e-11")


def main():
    raw = open(OBJECT, "rb").read()
    # line-ending tolerance: recorded hash is of the LF bytes; a CRLF checkout also passes
    h = hashlib.sha256(raw).hexdigest()
    h_lf = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
    if OBJECT_SHA not in (h, h_lf):
        print(f"FAIL: {OBJECT} sha256 {h} (lf-form {h_lf}) != recorded {OBJECT_SHA}")
        return 1
    pts = []
    for line in raw.decode().splitlines():
        s = line.split()
        if len(s) >= 2:
            pts.append((s[-2], s[-1]))
    if len(pts) != N:
        print(f"FAIL: expected {N} centres, found {len(pts)}")
        return 1
    fx = [float(x) for x, _ in pts]
    fy = [float(y) for _, y in pts]
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
    print(f"object sha256 ok ({OBJECT_SHA[:16]}...)")
    print(f"N = {len(pts)}")
    print(f"r* (60-digit decimal, from coordinate strings) = {r_star}")
    print(f"table value (cell N=3307)                        = {table}")
    print(f"margin = {margin}  (threshold {THRESH})")
    ok = margin >= THRESH
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
