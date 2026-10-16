#!/usr/bin/env python3
"""PREREG.v2 error bar for a transfer-matrix root sequence (main session, run 2026-10-16-0245).

usage: sigma_v2.py TSV SIGMA_B_RULE4 [REF]
  TSV: lines "W p ..." (first two columns used; duplicate W keep the first).
  Prints E1(W_max) for every W_max >= 4 (exact three-point solve p = pc + a W^-D, D free, on the last three sizes),
  drift_3 = max_k=1..3 |E1(W_max) - E1(W_max - k)|, and
  sigma_v2 = max(sigma_B_rule4, drift_3, 2.87 * sigma_B_rule4)
  where 2.87 is the worst ratio of true error to rule-4 sigma measured on lattices with known thresholds at comparable
  widths (runs/2026-10-16-0607/attempts/statistician/report.md, square site n_max 21, BSTD1 variant).
  Written after the step-5 lenses found rule-4 sigma under-covering; it only widens the error bar (PREREG.v2.md).
"""
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60
FACTOR = Decimal("2.87")


def load(path):
    seen, pts = set(), []
    for ln in open(path):
        if not ln.strip() or ln.startswith("#"):
            continue
        a = ln.split()
        try:
            w, p = int(a[0]), Decimal(a[1])
        except (ValueError, IndexError):
            continue
        if w not in seen:
            seen.add(w)
            pts.append((w, p))
    return sorted(pts)


def e1(three):
    (n1, p1), (n2, p2), (n3, p3) = three
    d1, d2 = p2 - p1, p3 - p2
    if d1 == 0 or d2 / d1 <= 0:
        return None
    q = d2 / d1
    N1, N2, N3 = Decimal(n1), Decimal(n2), Decimal(n3)
    g = lambda D: (N3 ** (-D) - N2 ** (-D)) / (N2 ** (-D) - N1 ** (-D)) - q
    lo, hi = Decimal("0.01"), Decimal("40")
    if g(lo) * g(hi) > 0:
        return None
    for _ in range(220):
        mid = (lo + hi) / 2
        if g(mid) * g(lo) > 0:
            lo = mid
        else:
            hi = mid
    D = (lo + hi) / 2
    a = (p3 - p2) / (N3 ** (-D) - N2 ** (-D))
    return p3 - a * N3 ** (-D), D


def main():
    pts = load(sys.argv[1])
    sb = Decimal(sys.argv[2])
    ref = Decimal(sys.argv[3]) if len(sys.argv) > 3 else None
    est = {}
    for i in range(2, len(pts)):
        r = e1(pts[i - 2:i + 1])
        wmax = pts[i][0]
        if r:
            est[wmax] = r
            print("W_max %2d  E1 %.15f  D %.4f%s" % (wmax, r[0], r[1], ("  E1-ref %+.3e" % (r[0] - ref)) if ref else ""))
        else:
            print("W_max %2d  E1 none (non-monotone window)" % wmax)
    wm = pts[-1][0]
    if wm not in est:
        print("last window has no E1; sigma_v2 undefined"); return
    drifts = [abs(est[wm][0] - est[wm - k][0]) for k in (1, 2, 3) if (wm - k) in est]
    d3 = max(drifts) if drifts else Decimal(0)
    sv2 = max(sb, d3, FACTOR * sb)
    print("W_max %d: E1 %.15f; sigma_B(rule 4) %.3e; drift_3 %.3e; 2.87*sigma_B %.3e; sigma_v2 %.3e"
          % (wm, est[wm][0], sb, d3, FACTOR * sb, sv2))
    if ref is not None:
        print("E1 - ref = %+.3e = %.2f sigma_v2" % (est[wm][0] - ref, abs(est[wm][0] - ref) / sv2))


if __name__ == "__main__":
    main()
