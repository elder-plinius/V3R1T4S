"""Calibrate the frozen extrapolation rule (extrapolate.py, PREREG method A) on a series with a known limit.

For n_max = lo..hi: run the rule on the series truncated at n_max and print p_TM, sigma_TM, the true error and
whether |error| <= sigma_TM (honest bar) and <= 3 sigma_TM.

usage: python calib_rule.py <series file> <exact value> <nmax lo> <nmax hi>
"""
import io
import os
import sys
import contextlib
from mpmath import mp, mpf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extrapolate  # noqa: E402

mp.dps = 40


def main():
    path, exact, lo, hi = sys.argv[1], mpf(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    print("series %s, exact %s" % (os.path.basename(path), mp.nstr(exact, 16)))
    print("n_max  local_exp  p_TM                 sigma_TM    error        |err|/sigma")
    for nmax in range(lo, hi + 1):
        vals = extrapolate.read_series(path, nmax)
        if max(vals) < nmax:
            break
        with contextlib.redirect_stdout(io.StringIO()):
            med, sig, eloc, ests = extrapolate.extrapolate(vals)
        err = med - exact
        print("%5d  %8.4f  %s  %.3e  %+.3e  %6.2f" % (nmax, eloc or float("nan"), mp.nstr(med, 17), float(sig),
                                                     float(err), float(abs(err) / sig) if sig else float("inf")))


if __name__ == "__main__":
    main()
