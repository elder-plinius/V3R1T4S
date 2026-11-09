"""Finite-size fit of the Monte Carlo crossings (PREREG.md, method B).

Primary: weighted least squares p_L = p_MC + A * L2^-4 over all sizes with L2 >= 16; sigma_MC from the covariance,
times sqrt(chi2/dof) if chi2/dof > 1. Stability: the same fit over L2 >= 24 must agree within one sigma_MC.
Report only: free-exponent fit p_L = p + A L2^-w over L2 >= 8.

usage: python fss_mc.py <dir with *.hist files> [--min-blocks 20] [--exact VALUE]
"""
import sys
import os
import glob
import math
import re
import numpy as np
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_mc  # noqa: E402


def sizes_in(d):
    groups = {}
    for p in sorted(glob.glob(os.path.join(d, "*.hist"))):
        m = re.search(r"_L(\d+)x(\d+)_s(\d+)_b(\d+)\.hist$", p)
        if m:
            groups.setdefault((int(m.group(1)), int(m.group(2))), []).append(p)
    return groups


def wls(L, p, e, w_exp=4.0):
    X = np.vstack([np.ones_like(L), L ** (-w_exp)]).T
    W = 1.0 / e ** 2
    A = X.T @ (W[:, None] * X)
    b = X.T @ (W * p)
    cov = np.linalg.inv(A)
    beta = cov @ b
    r = p - X @ beta
    chi2 = float(np.sum(W * r ** 2))
    dof = len(L) - 2
    s = math.sqrt(cov[0, 0])
    if dof > 0 and chi2 / dof > 1:
        s *= math.sqrt(chi2 / dof)
    return beta[0], s, beta[1], chi2, dof


def main():
    d = sys.argv[1]
    minb = 20
    exact = None
    if "--min-blocks" in sys.argv:
        minb = int(sys.argv[sys.argv.index("--min-blocks") + 1])
    if "--exact" in sys.argv:
        exact = float(sys.argv[sys.argv.index("--exact") + 1])
    rows = []
    for (L1, L2), paths in sorted(sizes_in(d).items(), key=lambda t: t[0][1]):
        if len(paths) < 2:
            continue
        r = analyze_mc.analyze(paths)
        r["ok_blocks"] = len(paths) >= minb
        rows.append(r)
    sel = [r for r in rows if r["ok_blocks"]]
    print("sizes with >= %d blocks: %s" % (minb, [(r["L1"], r["L2"]) for r in sel]))
    L = np.array([r["L2"] for r in sel], float)
    p = np.array([r["p"] for r in sel])
    e = np.array([r["err"] for r in sel])
    out = {}
    for lmin, label in [(16, "primary L2>=16"), (24, "stability L2>=24")]:
        m = L >= lmin
        if m.sum() >= 3:
            pc, s, A, chi2, dof = wls(L[m], p[m], e[m])
            out[label] = (pc, s)
            print("%-18s p_MC %.9f +- %.9f  A %.4g  chi2/dof %.2f/%d" % (label, pc, s, A, chi2, dof))
            if exact is not None:
                print("                   minus exact: %+.3e (%.2f sigma)" % (pc - exact, (pc - exact) / s))
    if "primary L2>=16" in out and "stability L2>=24" in out:
        (a, sa), (b, sb) = out["primary L2>=16"], out["stability L2>=24"]
        print("stability: |diff| %.3e vs sigma_MC %.3e -> %s" % (abs(a - b), sa, "STABLE" if abs(a - b) <= sa else "UNSTABLE"))
    m = L >= 8
    if m.sum() >= 4:
        try:
            f = lambda x, pc, A, w: pc + A * x ** (-w)
            popt, pcov = curve_fit(f, L[m], p[m], p0=[p[m][-1], 0.0, 4.0], sigma=e[m], absolute_sigma=True, maxfev=20000)
            print("free exponent (report only): p %.9f +- %.9f, w %.2f +- %.2f" % (
                popt[0], math.sqrt(pcov[0, 0]), popt[2], math.sqrt(pcov[2, 2])))
        except Exception as ex:  # noqa: BLE001
            print("free exponent fit failed: %s" % ex)


if __name__ == "__main__":
    main()
