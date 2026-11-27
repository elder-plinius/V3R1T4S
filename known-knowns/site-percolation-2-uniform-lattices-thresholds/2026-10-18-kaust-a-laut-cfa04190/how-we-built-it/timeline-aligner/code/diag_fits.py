"""Report-only diagnostics of the MC crossings (NOT the frozen PREREG fit): weighted mean of sizes >= Lmin, and
one-term fits p_L = p + A L2^-w for fixed w in {2, 2.75, 4}, over L2 >= 16 and L2 >= 24. Compares with a reference.

usage: python diag_fits.py <mc dir> <reference value> <label>
"""
import io
import math
import os
import sys
import contextlib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_mc  # noqa: E402
import fss_mc  # noqa: E402


def main():
    d, ref, label = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    rows = []
    for (L1, L2), paths in sorted(fss_mc.sizes_in(d).items(), key=lambda t: t[0][1]):
        with contextlib.redirect_stdout(io.StringIO()):
            rows.append(analyze_mc.analyze(paths))
    L = np.array([r["L2"] for r in rows], float)
    p = np.array([r["p"] for r in rows])
    e = np.array([r["err"] for r in rows])
    print("%s: reference %.10f" % (label, ref))
    for r in rows:
        print("  L2 %4d  p_L - ref %+.2e  (%.2f sigma)" % (r["L2"], r["p"] - ref, (r["p"] - ref) / r["err"]))
    for lmin in (8, 16, 24, 48):
        m = L >= lmin
        w = 1 / e[m] ** 2
        mu = np.sum(w * p[m]) / np.sum(w)
        s = 1 / math.sqrt(np.sum(w))
        chi2 = float(np.sum(w * (p[m] - mu) ** 2))
        print("  weighted mean L2>=%-3d %.9f +- %.2e  chi2/dof %.2f/%d  minus ref %+.2e (%.2f sigma)" % (
            lmin, mu, s, chi2, m.sum() - 1, mu - ref, (mu - ref) / s))
    for wexp in (2.0, 2.75, 4.0):
        for lmin in (16, 24):
            m = L >= lmin
            pc, s, A, chi2, dof = fss_mc.wls(L[m], p[m], e[m], w_exp=wexp)
            print("  fit w=%.2f L2>=%d  %.9f +- %.2e  A %+.3g  chi2/dof %.2f/%d  minus ref %+.2e (%.2f sigma)" % (
                wexp, lmin, pc, s, A, chi2, dof, pc - ref, (pc - ref) / s))


if __name__ == "__main__":
    main()
