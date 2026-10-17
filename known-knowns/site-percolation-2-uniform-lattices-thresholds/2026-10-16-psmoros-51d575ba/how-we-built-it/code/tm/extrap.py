#!/usr/bin/env python3
"""PREREG rule 4 extrapolation of p(W) sequences (rules fixed in NOTES.md at 03:45Z before any 2-uniform data).

usage: extrap.py TSV [REF] [--parity even|odd] [--wmin N]
  E1 = exact 3-point solve p(n) = pc + a n^-D (D free) on the last three sizes
  E2 = same on the three sizes before the last
  E3 = exact solve p(n) = pc + A n^-4 + B n^-6 + C n^-8 on the last four sizes
  sigma_B = max(|E1-E2|, |E1-E3|) if the last 4 sizes are monotone with strictly decreasing |differences|,
  else max |p(n)-p(n')| over the last 3 sizes.
All arithmetic on the printed decimal values with Fractions (exact), bisection for D in high precision Decimal.
"""
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 50


def load(path, parity=None, wmin=0):
    pts = []
    for ln in open(path):
        if ln.startswith("#") or not ln.strip():
            continue
        a = ln.split()
        w = int(a[0])
        if w < wmin:
            continue
        if parity == "even" and w % 2:
            continue
        if parity == "odd" and w % 2 == 0:
            continue
        pts.append((w, Decimal(a[1])))
    pts.sort()
    seen, out = set(), []
    for w, p in pts:  # duplicate W lines (two drivers) are identical runs; keep one
        if w not in seen:
            seen.add(w); out.append((w, p))
    return out


def three_point(pts):
    (n1, p1), (n2, p2), (n3, p3) = pts
    d1, d2 = p2 - p1, p3 - p2
    if d1 == 0 or d2 / d1 <= 0:
        return None, None
    q = d2 / d1
    n1, n2, n3 = Decimal(n1), Decimal(n2), Decimal(n3)

    def g(D):
        a, b, c = n1 ** (-D), n2 ** (-D), n3 ** (-D)
        return (c - b) / (b - a) - q

    lo, hi = Decimal("0.01"), Decimal("40")
    glo, ghi = g(lo), g(hi)
    if glo * ghi > 0:
        return None, None
    for _ in range(200):
        mid = (lo + hi) / 2
        gm = g(mid)
        if gm * glo > 0:
            lo, glo = mid, gm
        else:
            hi = mid
    D = (lo + hi) / 2
    a = d2 / (n3 ** (-D) - n2 ** (-D))
    return p3 - a * n3 ** (-D), D


def solve(M, y):
    n = len(y)
    M = [row[:] + [yy] for row, yy in zip(M, y)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * z for x, z in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def richardson468(pts):
    M, y = [], []
    for n, p in pts:
        n = F(n)
        M.append([F(1), n ** -4, n ** -6, n ** -8])
        y.append(F(str(p)))
    x = solve(M, y)[0]
    return Decimal(x.numerator) / Decimal(x.denominator)


def richardson_n(pts, exps):
    M, y = [], []
    for n, p in pts:
        n = F(n)
        M.append([F(1)] + [n ** -e for e in exps])
        y.append(F(str(p)))
    x = solve(M, y)[0]
    return Decimal(x.numerator) / Decimal(x.denominator)


def main():
    path = sys.argv[1]
    ref = None
    parity, wmin = None, 0
    refsig = None
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--parity":
            parity = args[i + 1]; i += 2
        elif args[i] == "--refsig":
            refsig = Decimal(args[i + 1]); i += 2
        elif args[i] == "--wmin":
            wmin = int(args[i + 1]); i += 2
        else:
            ref = Decimal(args[i]); i += 1
    pts = load(path, parity, wmin)
    print("# file %s parity=%s wmin=%d  n=%d sizes" % (path, parity, wmin, len(pts)))
    print("# W  p(W)  diff  D_eff(3pt ending here)  pc_3pt" + ("  p(W)-ref" if ref is not None else ""))
    for k, (w, p) in enumerate(pts):
        diff = p - pts[k - 1][1] if k else None
        pc3, D = three_point(pts[k - 2:k + 1]) if k >= 2 else (None, None)
        s = "%3d  %s  %s  %s  %s" % (w, p, ("%.3e" % diff) if diff is not None else "-",
                                     ("%.4f" % D) if D is not None else "-", ("%.15f" % pc3) if pc3 is not None else "-")
        if ref is not None:
            s += "  %.3e" % (p - ref)
        print(s)
    print("# diagnostic (not the rule-4 estimate): sliding 4-point Richardson with exponents 4,6,8 and 5-point with 4,6,8,10")
    for k in range(3, len(pts)):
        r4 = richardson468(pts[k - 3:k + 1])
        s = "#   window W=%d..%d  E3=%.15f" % (pts[k - 3][0], pts[k][0], r4)
        if k >= 4:
            s += "  R5=%.15f" % richardson_n(pts[k - 4:k + 1], [4, 6, 8, 10])
        if ref is not None:
            s += "  E3-ref=%.3e" % (r4 - ref)
        print(s)
    if len(pts) < 4:
        print("fewer than 4 sizes: rule 4 not applicable")
        return
    E1, D1 = three_point(pts[-3:])
    E2, D2 = three_point(pts[-4:-1])
    E3 = richardson468(pts[-4:])
    last4 = pts[-4:]
    ds = [last4[i + 1][1] - last4[i][1] for i in range(3)]
    smooth = (all(d > 0 for d in ds) or all(d < 0 for d in ds)) and abs(ds[0]) > abs(ds[1]) > abs(ds[2])
    if smooth and E1 is not None and E2 is not None:
        sig = max(abs(E1 - E2), abs(E1 - E3))
        rule = "rule4-main"
    else:
        l3 = [p for _, p in pts[-3:]]
        sig = max(l3) - min(l3)
        rule = "rule4-fallback(not smooth)"
    print("E1 = %s (D=%s)" % (("%.15f" % E1) if E1 is not None else "None", ("%.4f" % D1) if D1 is not None else "-"))
    print("E2 = %s (D=%s)" % (("%.15f" % E2) if E2 is not None else "None", ("%.4f" % D2) if D2 is not None else "-"))
    print("E3 = %.15f (fixed exponents 4,6,8 on last four)" % E3)
    pcB = E1 if (E1 is not None and smooth) else pts[-1][1]
    print("RESULT pc_B = %.15f sigma_B = %.3e [%s] sizes W=%d..%d" % (pcB, sig, rule, pts[0][0], pts[-1][0]))
    if ref is not None:
        print("pc_B - ref = %.3e  (= %.2f sigma_B)" % (pcB - ref, float((pcB - ref) / sig) if sig else float("inf")))
        if refsig is not None:
            comb = (sig * sig + refsig * refsig).sqrt()
            print("combined sigma = %.3e ; |pc_B - ref| / combined = %.2f" % (comb, float(abs(pcB - ref) / comb)))


if __name__ == "__main__":
    main()
