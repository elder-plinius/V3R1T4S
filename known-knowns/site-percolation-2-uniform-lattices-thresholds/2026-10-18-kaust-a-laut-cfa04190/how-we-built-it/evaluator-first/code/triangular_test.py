"""PREREG.v2 addition 2: the crossing estimator on the self-matching triangular lattice must give p_L = 1/2.

For each size in the folder: p_L and its jackknife sigma (analyze_mc.py, the same code as for every lattice), the
deviation from 1/2, and PASS if |p_L - 1/2| <= 3 sigma_L. Also checks the exact microcanonical symmetry in
distribution: R_0D(n) = R_2D(M - n), by comparing the pooled histograms of n1 and M - n2 + 1 (two-sample
Kolmogorov-Smirnov distance, reported only).

usage: python triangular_test.py <mc folder> [expected blocks per size]
"""
import io
import math
import os
import sys
import contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "timeline-aligner", "code"))
import analyze_mc  # noqa: E402
import fss_mc  # noqa: E402


def main():
    d = sys.argv[1]
    want = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    allpass = True
    for (L1, L2), paths in sorted(fss_mc.sizes_in(d).items(), key=lambda t: t[0][1]):
        with contextlib.redirect_stdout(io.StringIO()):
            r = analyze_mc.analyze(paths)
        dev = r["p"] - 0.5
        ok = abs(dev) <= 3 * r["err"] and len(paths) >= want
        allpass &= ok
        metas, hs, M = analyze_mc.load(paths)
        H1 = sum(h[0] for h in hs)
        H2 = sum(h[1] for h in hs)
        # R_0D(n) = P(n1 > n) and R_2D(M - n) = P(n2 <= M - n) = P(M - n2 >= n); n1 > n  <=>  n1 >= n + 1
        c1 = np.cumsum(H1[::-1])[::-1] / H1.sum()            # P(n1 >= k)
        mirrored = np.zeros(M + 2)
        for k in range(M + 1):
            if H2[k]:
                mirrored[M - k + 1] += H2[k]                  # n2 = k  ->  M - n2 + 1
        c2 = np.cumsum(mirrored[::-1])[::-1][:M + 1] / H2.sum()   # P(M - n2 + 1 >= k)
        ks = float(np.max(np.abs(c1 - c2)))
        print("L %3dx%-3d blocks %2d samples %10d  p_L %.9f +- %.2e  p_L - 1/2 %+.2e (%+.2f sigma)  KS(n1, M-n2+1) %.2e  %s" % (
            L1, L2, len(paths), r["samples"], r["p"], r["err"], dev, dev / r["err"], ks, "PASS" if ok else "FAIL"))
    print("TRIANGULAR ESTIMATOR TEST: %s" % ("PASS" if allpass else "FAIL"))


if __name__ == "__main__":
    main()
