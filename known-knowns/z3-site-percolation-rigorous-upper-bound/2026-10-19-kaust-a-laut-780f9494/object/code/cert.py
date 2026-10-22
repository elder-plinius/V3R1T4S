"""Exact side of the certificate (see cert/main.go for the model).

  python cert.py intervals <counts file> <pnum> <pden> <out>
      From the exact counts, r_f(T) = P_p(T meets the trace of G(eps') on the facing face opp(f)) as an exact
      rational, and pw[k] = p^k (1-p)^(n-k); writes each as the pair (largest float <= value, smallest float >= value).
  python cert.py check <counts file> <laws file> <pnum> <pden> <qnum> <qden>
      Root: r_f(full face) >= q exactly for every face f.
      Each entry face fin and nonempty U: with lo/hi the Go bounds, num_lo(x) = sum over T meeting U of lo[fin][T][x]
      (exact integers after scaling every float by 2^1100), likewise num_hi; Z_hi = sum_x num_hi(x);
      l(x) = floor(num_lo(x) 2^56 / Z_hi). Then for every up-set A of {0,1}^5 other than the empty and full sets,
      P_true(A) >= num_lo(A)/Z_hi >= sum_{x in A} l(x) / 2^56, and the check is sum_{x in A} l(x) >= ceil(Q_q(A) 2^56),
      in exact integers. (Those two hold trivially: both sides are 0, or both 1.)
"""
import math
import sys
from fractions import Fraction

import numpy as np

from upsets import upsets

OPP = [1, 0, 3, 2, 5, 4]
SCALE = 1100   # every finite float is an integer multiple of 2^-1074
PREC = 56


def read_counts(fn):
    C = {}
    for line in open(fn):
        w = line.split()
        if w[0] == "dims":
            n = int(w[w.index("n") + 1])
            fs = list(map(int, w[w.index("fsize") + 1:]))
        else:
            f, k, S, v = map(int, w[1:])
            C.setdefault(f, {})
            C[f][(k, S)] = C[f].get((k, S), 0) + v
    return n, fs, C


def exact_tables(n, fs, C, p):
    pw = [p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
    dist = []
    for g in range(6):
        d = [Fraction(0)] * (1 << fs[g])
        for (k, S), v in C[g].items():
            d[S] += v * pw[k]
        assert sum(d) == 1, "trace law of face %d does not sum to 1" % g
        dist.append(d)
    r = []
    for f in range(6):
        d = dist[OPP[f]]
        r.append([sum((d[S] for S in range(len(d)) if S & T), Fraction(0)) for T in range(1 << fs[f])])
    return pw, r


def enclose(x):
    """(lo, hi) floats with lo <= x <= hi, for an exact rational x >= 0."""
    f = float(x)
    lo = f if Fraction(f) <= x else math.nextafter(f, 0.0)
    hi = f if Fraction(f) >= x else math.nextafter(f, math.inf)
    return lo, hi


def to_int(s):
    num, den = float(s).as_integer_ratio()
    return num * ((1 << SCALE) // den)


def cmd_intervals(cfile, pn, pd, out):
    n, fs, C = read_counts(cfile)
    p = Fraction(pn, pd)
    pw, r = exact_tables(n, fs, C, p)
    with open(out, "w", newline="\n") as fo:
        fo.write("p %d/%d\n" % (pn, pd))
        for k in range(n + 1):
            lo, hi = enclose(pw[k])
            fo.write("pw %d %r %r\n" % (k, lo, hi))
        for f in range(6):
            for T in range(1 << fs[f]):
                rl, rh = enclose(r[f][T])
                sl, sh = enclose(1 - r[f][T])
                fo.write("r %d %d %r %r %r %r\n" % (f, T, rl, rh, sl, sh))
    print("intervals written:", out)


def zeta(rows, m):
    """rows[T] (lists of ints over x); returns S[V] = sum over T subset of V of rows[T]."""
    S = [list(r) for r in rows]
    for i in range(m):
        bit = 1 << i
        for V in range(1 << m):
            if V & bit:
                a, b = S[V], S[V ^ bit]
                S[V] = [u + v for u, v in zip(a, b)]
    return S


def cmd_check(cfile, lfile, pn, pd, qn, qd):
    n, fs, C = read_counts(cfile)
    p, q = Fraction(pn, pd), Fraction(qn, qd)
    pw, r = exact_tables(n, fs, C, p)
    ok = True
    for f in range(6):
        full = (1 << fs[f]) - 1
        if r[f][full] < q:
            ok = False
            print("ROOT FAIL face %d: r(full) = %s < q" % (f, float(r[f][full])))
    print("root: min r_f(full face) = %.12f (needs >= q = %s)" % (min(float(r[f][(1 << fs[f]) - 1]) for f in range(6)), q))
    lo = {}
    hi = {}
    for line in open(lfile):
        w = line.split()
        if w[0] != "L":
            continue
        fin, T = int(w[1]), int(w[2])
        vals = w[3:]
        lo[(fin, T)] = [to_int(vals[2 * x]) for x in range(32)]
        hi[(fin, T)] = [to_int(vals[2 * x + 1]) for x in range(32)]
    U5 = [A for A in upsets(5) if 0 < len(A) < 32]   # empty and full sets hold trivially
    M = np.zeros((len(U5), 32), np.int64)
    for i, A in enumerate(U5):
        M[i, list(A)] = 1
    Qhi = []
    for A in U5:
        QA = sum((q ** bin(x).count("1") * (1 - q) ** (5 - bin(x).count("1")) for x in A), Fraction(0))
        Qhi.append(-((-QA.numerator << PREC) // QA.denominator))   # ceil(QA * 2^PREC)
    Qhi = np.array(Qhi, dtype=np.int64)
    worst = None
    nlaws = 0
    for fin in range(6):
        m = fs[fin]
        full = (1 << m) - 1
        Llo = [lo[(fin, T)] for T in range(1 << m)]
        Lhi = [hi[(fin, T)] for T in range(1 << m)]
        Slo, Shi = zeta(Llo, m), zeta(Lhi, m)
        ell = np.zeros((1 << m, 32), np.int64)
        valid = np.zeros(1 << m, bool)
        for U in range(1, 1 << m):
            comp = full ^ U
            nlo = [a - b for a, b in zip(Slo[full], Slo[comp])]
            nhi = [a - b for a, b in zip(Shi[full], Shi[comp])]
            Z = sum(nhi)
            if Z == 0:
                continue
            valid[U] = True
            ell[U] = [(v << PREC) // Z for v in nlo]
        P = ell @ M.T                       # exact int64: entries < 2^56, at most 31 terms
        marg = P - Qhi[None, :]
        marg[~valid] = 1 << 62
        i, j = np.unravel_index(int(np.argmin(marg)), marg.shape)
        nlaws += int(valid.sum())
        mv = int(marg[i, j])
        if worst is None or mv < worst[0]:
            worst = (mv, fin, int(i), U5[j])
        if mv < 0:
            ok = False
            print("FAIL entry face %d U=%s up-set %s margin %.3e" % (fin, bin(i), U5[j], mv / 2 ** PREC))
    print("checked %d entry laws x %d up-sets; worst margin %.6e at entry face %d U=%s up-set %s"
          % (nlaws, len(U5), worst[0] / 2 ** PREC, worst[1], bin(worst[2]), worst[3]))
    print("CERTIFICATE: %s (p = %s, q = %s)" % ("PASS" if ok else "FAIL", p, q))


if __name__ == "__main__":
    if sys.argv[1] == "intervals":
        cmd_intervals(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    else:
        cmd_check(sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8]))
