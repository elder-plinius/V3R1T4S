"""Extrapolate a p_c(n) series to n -> infinity by the rule frozen in PREREG.md (method A).

Ansatz p_c(n) = p_c + sum_{k=1..K} A_k n^(-e_k).
Exponents: local exponent e_loc from the three largest n (solving d(n)/d(n-1) for e, d(n) = p(n) - p(n-1));
  if e_loc is within 0.5 of an even integer >= 4: e_k = 2(k+1) = 4, 6, 8, ...;
  otherwise e_k = round(e_loc) + (k - 1).
Fit family: K = 1..4, j = 0, 1, 2, only n >= 4. PREREG says "each solved exactly on the K+1+j largest available n".
That phrase has two readings, and both are computed here; sigma_TM uses the union of both families (the more
conservative choice, fixed before any extrapolation was run):
  reading W (windows): exact solve on the K+1 consecutive n ending at n_max - j;
  reading S (sets):    least squares on the K+1+j largest n (exact when j = 0).
p_TM = median of the union; sigma_TM = max |estimate - p_TM| over the union.

usage: python extrapolate.py <series file> [--nmax N]
"""
import sys
import math
import numpy as np
from mpmath import mp, mpf, matrix, lu_solve

mp.dps = 40


def read_series(path, nmax=None):
    vals = {}
    for line in open(path):
        t = line.split()
        if len(t) > 5 and t[0] == "n":
            n = int(t[1])
            if nmax is None or n <= nmax:
                vals[n] = mpf(t[t.index("pc") + 1])
    return vals


def local_exponent(vals):
    ns = sorted(vals)
    n = ns[-1]
    if not (n - 1 in vals and n - 2 in vals):
        return None
    d1 = vals[n] - vals[n - 1]
    d0 = vals[n - 1] - vals[n - 2]
    r = d1 / d0

    def g(e):
        e = mpf(e)
        return (mpf(n) ** -e - mpf(n - 1) ** -e) / (mpf(n - 1) ** -e - mpf(n - 2) ** -e) - r
    lo, hi = mpf("0.5"), mpf("30")
    if g(lo) * g(hi) > 0:
        return None
    for _ in range(200):
        m = (lo + hi) / 2
        if g(lo) * g(m) <= 0:
            hi = m
        else:
            lo = m
    return float((lo + hi) / 2)


def exponents(e_loc, K):
    if e_loc is not None:
        near = round(e_loc / 2) * 2
        if near >= 4 and abs(e_loc - near) <= 0.5:
            return [2 * (k + 1) for k in range(1, K + 1)], "even"
        e1 = int(round(e_loc))
        return [e1 + k for k in range(K)], "integer from %d" % e1
    return [2 * (k + 1) for k in range(1, K + 1)], "even (no local exponent)"


def fit(vals, ns, exps):
    """least squares (exact when len(ns) == len(exps) + 1) for p_c and amplitudes, in 40-digit arithmetic"""
    rows = len(ns)
    cols = len(exps) + 1
    A = matrix(rows, cols)
    b = matrix(rows, 1)
    for i, n in enumerate(ns):
        A[i, 0] = 1
        for k, e in enumerate(exps):
            A[i, k + 1] = mpf(n) ** (-e)
        b[i] = vals[n]
    if rows == cols:
        x = lu_solve(A, b)
    else:
        At = A.T
        x = lu_solve(At * A, At * b)
    return x[0]


def extrapolate(vals, verbose=True):
    ns_all = sorted(n for n in vals if n >= 4)
    nmax = ns_all[-1]
    e_loc = local_exponent(vals)
    exps4, fam = exponents(e_loc, 4)
    ests = []
    for K in range(1, 5):
        exps = exps4[:K]
        for j in range(3):
            # reading W: window of K+1 consecutive n ending at nmax - j
            win = [n for n in range(nmax - j - K, nmax - j + 1)]
            if all(n in vals and n >= 4 for n in win):
                ests.append(("W", K, j, fit(vals, win, exps)))
            # reading S: the K+1+j largest n
            st = ns_all[-(K + 1 + j):]
            if len(st) == K + 1 + j and st[0] >= 4:
                ests.append(("S", K, j, fit(vals, st, exps)))
    est_vals = sorted(e[3] for e in ests)
    m = len(est_vals)
    med = est_vals[m // 2] if m % 2 else (est_vals[m // 2 - 1] + est_vals[m // 2]) / 2
    sig = max(abs(v - med) for v in est_vals)
    if verbose:
        print("n_max %d, local exponent %.4f, family %s, exponents %s" % (nmax, e_loc if e_loc else float("nan"), fam, exps4))
        for (r, K, j, v) in ests:
            print("  %s K=%d j=%d  %s" % (r, K, j, mp.nstr(v, 16)))
        print("p_TM %s  sigma_TM %s  (%d estimates)" % (mp.nstr(med, 14), mp.nstr(sig, 3), m))
    return med, sig, e_loc, ests


if __name__ == "__main__":
    path = sys.argv[1]
    nmax = None
    if "--nmax" in sys.argv:
        nmax = int(sys.argv[sys.argv.index("--nmax") + 1])
    extrapolate(read_series(path, nmax))
