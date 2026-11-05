#!/usr/bin/env python3
"""Spherical-code cosine checker.

Normalize each vector to unit length in mpmath at 50 decimal digits.
c* is the maximum pairwise inner product. Smaller is better.
An improvement over a table cosine requires c_table - c* >= margin (default 1e-10).
"""
import argparse
import sys
from mpmath import mp, mpf, sqrt, nstr, acos, pi

mp.dps = 50


def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rows.append([mpf(x) for x in line.replace(" ", ",").split(",") if x != ""])
    if not rows:
        raise SystemExit("empty coordinate file")
    d = len(rows[0])
    if any(len(r) != d for r in rows):
        raise SystemExit("ragged coordinate file")
    return rows


def digit_count(tok):
    mant = tok.lower().split("e")[0].replace("-", "").replace("+", "").replace(".", "")
    return len(mant)


def min_digits(path):
    worst = 10**9
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for tok in line.replace(" ", ",").split(","):
                if tok:
                    worst = min(worst, digit_count(tok))
    return worst


def normalize(rows):
    out = []
    for r in rows:
        s = sqrt(sum(x * x for x in r))
        if s == 0:
            raise SystemExit("zero vector")
        out.append([x / s for x in r])
    return out


def max_inner(rows):
    n = len(rows)
    best = mpf("-inf")
    pair = (0, 1)
    for i in range(n):
        ri = rows[i]
        for j in range(i + 1, n):
            ip = sum(a * b for a, b in zip(ri, rows[j]))
            if ip > best:
                best = ip
                pair = (i, j)
    return best, pair


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--table", default=None)
    ap.add_argument("--margin", default="1e-10")
    ap.add_argument("--min-digits", type=int, default=0)
    args = ap.parse_args()
    if args.min_digits:
        got = min_digits(args.path)
        print(f"min_digits={got}")
        if got < args.min_digits:
            print("DIGIT_FAIL")
            return 1
    rows = normalize(load(args.path))
    c, pair = max_inner(rows)
    print(f"N={len(rows)} d={len(rows[0])}")
    print("c*=" + nstr(c, 50, strip_zeros=False))
    ang = acos(c) * 180 / pi
    print("min_angle_deg=" + nstr(ang, 20, strip_zeros=False))
    print(f"pair={pair[0]},{pair[1]}")
    if args.table is None:
        print("NO_TABLE")
        return 0
    delta = mpf(args.table) - c
    print("c_table=" + str(args.table))
    print("delta=" + nstr(delta, 21, strip_zeros=False))
    ok = delta >= mpf(args.margin)
    print("IMPROVEMENT" if ok else "NO_IMPROVEMENT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
