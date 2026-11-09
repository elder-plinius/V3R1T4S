#!/usr/bin/env python3
"""H4b: self-contained (no Worley) deep search of f_k(m) = r f_k(n), every Lemma-A ratio r, X0 <= X <= XMAX.

Setting (see deep_cf.py): X = n + (k+1)/2, Y = m + (k+1)/2, rho = r^(1/k), c = (k^2-1)(rho^2-1)/(24 rho),
(p, q) = (Y, X) for odd k, (2Y, 2X) for even k (scale S = 1 or 4). margin_check.py --tight proves, for X >= X0,
c(1-eta) < X(rho X - Y(X)) < c(1+eta), hence every solution has  S c(1-eta) < q (q rho - p) < S c(1+eta) =: [L, U].
Enumeration of ALL integer pairs (p, q), 1 <= q <= QMAX, with 0 < q rho - p and q (q rho - p) < U:
let m >= 0 with q_m <= q < q_{m+1} (convergents p_m/q_m of rho). As (p_m,q_m),(p_{m+1},q_{m+1}) is a unimodular
basis, (p, q) = r (p_{m+1}, q_{m+1}) + s (p_m, q_m) with integers r, s. r = 0 gives multiples of a convergent.
For r != 0, r and s have opposite signs, so r d_{m+1} and s d_m (d_j = q_j rho - p_j, alternating signs) have the
same sign and q|q rho - p| >= q_m |s| |d_m| > q_m |s| / (q_{m+1}+q_m); together with the range of q this gives
|r| <= 2U + 1. For every (m, r) the admissible real s form an interval cut by a quadratic inequality; all integer
s there (with a safety margin of 2 on each side) are generated and re-checked in 1050-digit arithmetic.
Candidates with q(q rho - p) in (L, U) are mapped to (n, m) and tested exactly; X < X0 is inside the complete search.
usage: deep_rig.py KMIN KMAX DIGITS ETA X0 [validate]
"""
import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gmpy2
from gmpy2 import mpz
import mpmath
from deep_cf import admissible_r, cf_of_root, f, M

def convergents(pq):
    P = [mpz(1), mpz(pq[0])]; Q = [mpz(0), mpz(1)]
    for t in pq[1:]:
        P.append(t * P[-1] + P[-2]); Q.append(t * Q[-1] + Q[-2])
    return P[1:], Q[1:]     # p_0.., q_0..

def enum_pairs(rho, pq, U, QMAX, L=None):
    """(v2) if L is given, pairs whose double-precision g = q(q rho - p) is outside (L(1-1e-6), U(1+1e-6)) are skipped
    before the 1050-digit check (float relative error ~1e-15, so no pair with g in (L, U) is lost)."""
    p_, q_ = convergents(pq)
    out = set()
    R = int(2 * U) + 2
    ms = [i for i in range(len(q_) - 1) if q_[i] <= QMAX]
    if not ms:
        return out
    if q_[ms[-1] + 1] <= QMAX:
        raise RuntimeError("continued fraction too short for QMAX")
    Qn = np.array([float(mpmath.mpf(q_[i]) / q_[i + 1]) for i in ms])
    d = [q_[i] * rho - p_[i] for i in range(len(q_))]
    D0 = np.array([float(d[i] * q_[i + 1]) for i in ms])
    D1 = np.array([float(d[i + 1] * q_[i + 1]) for i in ms])
    amax = max(int(q_[i + 1] // q_[i]) for i in ms)
    if amax > 10 ** 12:
        raise RuntimeError("partial quotient too large for float stage")
    Uf = float(U)
    Lf = float(L) if L is not None else None
    jidx = {i: j for j, i in enumerate(ms)}
    def check_add(i, r, s):
        p = r * p_[i + 1] + s * p_[i]; q = r * q_[i + 1] + s * q_[i]
        if q < q_[i] or q >= q_[i + 1] or q > QMAX or q <= 0:
            return
        e = q * rho - p
        if e > 0 and q * e < U:
            out.add((int(p), int(q)))
    # r = 0: q = s q_m, s >= 1, need d_m > 0 and s^2 q_m d_m < U  (u = s Qn, w = s D0)
    for j, i in enumerate(ms):
        if D0[j] > 0:
            smax = int(math.sqrt(Uf / (Qn[j] * D0[j]))) + 2
            smax = min(smax, int(1 / Qn[j]) + 2)
            for s in range(1, smax + 1):
                if Lf is not None:
                    g = s * s * Qn[j] * D0[j]
                    if not (Lf * (1 - 1e-6) < g < Uf * (1 + 1e-6)):
                        continue
                check_add(i, 0, s)
    # r != 0, vectorised over (m, r): u = r + s Qn in [Qn, 1), w = r D1 + s D0 > 0, u w < U
    rr = np.array([x for x in range(-R, R + 1) if x != 0], dtype=np.float64)
    Qm, Rm = np.meshgrid(Qn, rr, indexing="ij"); D0m = np.meshgrid(D0, rr, indexing="ij")[0]; D1m = np.meshgrid(D1, rr, indexing="ij")[0]
    lo = (Qm - Rm) / Qm                      # u >= Qn
    hi = (1.0 - Rm) / Qm                     # u < 1
    # w > 0
    wb = -Rm * D1m / D0m
    lo = np.where(D0m > 0, np.maximum(lo, wb), lo)
    hi = np.where(D0m < 0, np.minimum(hi, wb), hi)
    # quadratic g(s) = A s^2 + B s + C0 < U
    A = Qm * D0m; B = Rm * (Qm * D1m + D0m); C0 = Rm * Rm * D1m - Uf
    disc = B * B - 4 * A * C0
    sq = np.sqrt(np.maximum(disc, 0.0))
    r1 = (-B - sq) / (2 * A); r2 = (-B + sq) / (2 * A)
    rmin = np.minimum(r1, r2); rmax = np.maximum(r1, r2)
    cand_cells = []
    pos = A > 0
    dpos = disc >= 0
    ivs = []
    # A > 0: g < U strictly between the roots
    x1 = np.maximum(lo, rmin); y1 = np.minimum(hi, rmax)
    ivs.append((pos & dpos & (y1 >= x1 - 4), x1, y1))
    # A <= 0, no real root: g < U everywhere on [lo, hi]
    ivs.append((~pos & ~dpos & (hi >= lo - 4), lo, hi))
    # A <= 0, real roots: g < U outside the roots
    x2 = lo; y2 = np.minimum(hi, rmin)
    ivs.append((~pos & dpos & (y2 >= x2 - 4), x2, y2))
    x3 = np.maximum(lo, rmax); y3 = hi
    ivs.append((~pos & dpos & (y3 >= x3 - 4), x3, y3))
    for mask, xs, ys in ivs:
        for j, t in zip(*np.nonzero(mask)):
            x, y = xs[j, t], ys[j, t]
            s0 = int(math.floor(x)) - 2; s1 = int(math.ceil(y)) + 2
            if s1 - s0 > 100000:
                raise RuntimeError("s-range too long at m-index %d r=%d: %d" % (ms[j], int(rr[t]), s1 - s0))
            cand_cells.append((ms[j], int(rr[t]), s0, s1))
    # exact u only where float cancellation could exceed 1e-9 relative (Qn small); see NOTES.md (run 2026-10-24-0818)
    exact_u = [bool(Qn[j] < 1e-4 or 3.4e-16 * (R + 1) / Qn[j] > 1e-9) for j in range(len(ms))]
    for (i, r, s0, s1) in cand_cells:
        j = jidx[i]
        for s in range(s0, s1 + 1):
            if s == 0 or (r > 0 and s > 0) or (r < 0 and s < 0):
                continue
            if Lf is not None:
                # u = q / q_{m+1} from the exact integer q (no cancellation: r and s have opposite signs, so the float
                # r + s*Qn can lose all relative accuracy when Qn = q_m/q_{m+1} is tiny); w = r D1 + s D0 has no
                # cancellation (both terms have the same sign). Patch of run 2026-10-24-0818, see NOTES.md.
                if exact_u[j]:
                    qq = r * q_[i + 1] + s * q_[i]
                    if qq <= 0:
                        continue
                    g = float(gmpy2.mpq(qq, q_[i + 1])) * (r * D1[j] + s * D0[j])
                else:
                    # float u = r + s Qn: absolute error <= 3 (|r|+1) 2^-53, relative <= 3.4e-16 (R+1)/Qn <= 1e-9
                    g = (r + s * Qn[j]) * (r * D1[j] + s * D0[j])
                if not (Lf * (1 - 1e-6) < g < Uf * (1 + 1e-6)):
                    continue
            check_add(i, r, s)
    return out

def brute_pairs(rho, U, QV):
    out = set()
    for q in range(1, QV + 1):
        p = int(mpmath.floor(q * rho))
        while p >= 1 and q * (q * rho - p) < U:
            if q * rho - p > 0:
                out.add((p, q))
            p -= 1
    return out

def main():
    KMIN, KMAX, DIG = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    ETA = mpmath.mpf(sys.argv[4]); X0 = int(sys.argv[5])
    validate = len(sys.argv) > 6 and sys.argv[6] == "validate"
    mpmath.mp.dps = DIG + 50
    QEXP = int(os.environ.get('QEXP', DIG // 2 - 5))   # QMAX = 10^QEXP; needs DIG comfortably above 2*QEXP
    QMAX = mpz(10) ** QEXP
    t0 = time.time()
    totc = tots = 0
    for k in range(KMIN, KMAX + 1):
        S = 1 if k % 2 else 4
        kc = ks = kp = 0
        for r in admissible_r(k):
            a, b = r.numerator, r.denominator
            rho = mpmath.root(mpmath.mpf(a) / b, k)
            c = (k * k - 1) * (rho * rho - 1) / (24 * rho)
            if validate:
                Uv = S * (2 * c + mpmath.mpf(1) / 10) * float(os.environ.get('UMULT', '1'))
                pq = cf_of_root(a, b, k, 120)
                mine = set(t for t in enum_pairs(rho, pq, Uv, mpz(4000)) if t[0] >= 1)   # p = Y or 2Y > 0
                br = set(t for t in brute_pairs(rho, Uv, 4000) if t[0] >= 1)
                status = "OK" if mine == br else "MISMATCH only_enum=%d only_brute=%d" % (len(mine - br), len(br - mine))
                print("validate k=%d r=%s pairs(q<=4000)=%d %s" % (k, r, len(br), status), flush=True)
                continue
            L = S * c * (1 - ETA); U = S * c * (1 + ETA)
            pq = cf_of_root(a, b, k, DIG)
            pairs = enum_pairs(rho, pq, U, QMAX, L=L if os.environ.get('WINDOW_PREFILTER', '1') == '1' else None)
            kp += len(pairs)
            for (p, q) in pairs:
                e = q * rho - p
                if not (q * e > L):
                    continue
                if k % 2:
                    n, m = q - (k + 1) // 2, p - (k + 1) // 2
                else:
                    if q % 2 == 0 or p % 2 == 0:
                        continue
                    n, m = (q - k - 1) // 2, (p - k - 1) // 2
                if n < 0 or m <= n or 2 * n + k + 1 < 2 * X0:
                    continue
                kc += 1
                if f(m, k) * b == a * f(n, k):
                    ks += 1
                    print("PRODUCT SOLUTION k=%d r=%s n=%d m=%d disjoint=%s lcm_equal=%s" % (k, r, n, m, m >= n + k, M(m, k) == M(n, k)), flush=True)
        if not validate:
            totc += kc; tots += ks
            print("k=%d admissible_r=%d enumerated_pairs(q(q rho-p)<U)=%d window_candidates=%d product_solutions=%d t=%.0fs" % (k, len(admissible_r(k)), kp, kc, ks, time.time() - t0), flush=True)
    if not validate:
        print("TOTAL window candidates=%d product solutions=%d (X0=%d, QMAX=10^%d)" % (totc, tots, X0, QEXP))

if __name__ == "__main__":
    main()
