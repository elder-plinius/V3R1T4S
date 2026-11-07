#!/usr/bin/env python3
"""H4: deep (CAPPED) search of the product curves f_k(m) = r * f_k(n) for small k, via Diophantine approximation.

By Lemma A every counterexample satisfies f_k(m) = r f_k(n) with r = prod_{p<k} p^{d_p}, |d_p| <= L_p(k) =
#{i >= 1 : p^i < k, p^i does not divide k}, and 1 < r <= R(k) = lcm(1..k)/k.
Put X = n + (k+1)/2, Y = m + (k+1)/2, F(Z) = prod_j (Z + j - (k+1)/2) = Z^k - s Z^(k-2) + ..., s = k(k^2-1)/24.
F(Y) = r F(X) gives Y = rho X - c/X + O(X^-3), rho = r^(1/k), c = (k^2-1)(rho^2-1)/(24 rho) > 0.
So with (p, q) = (Y, X) for odd k and (2Y, 2X) for even k:  0 < q rho - p < Cq / q  (Cq = C or 4C, C >= c with
margin; checked numerically for X >= X0 in this script). All such (p, q), q <= QMAX, are generated as g*(p', q')
with p'/q' reduced, and reduced p'/q' with |rho - p'/q'| < Cq/q'^2 are of the form
(a p_{i+1} +- b p_i)/(a q_{i+1} +- b q_i), a*b < 2 Cq (Worley 1981; also Dujella 2004), p_i/q_i convergents of rho.
Each candidate is tested exactly: f(m) * den(r) == num(r) * f(n), then lcm equality.
CAPPED: covers X0 <= X <= QMAX only (X < X0 lies inside the complete search range).
usage: deep_cf.py KMIN KMAX DIGITS [X0]
"""
import sys, math, itertools, time
from fractions import Fraction
import gmpy2
from gmpy2 import mpz, iroot
import mpmath

def primes_below(k):
    return [p for p in range(2, k) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

def admissible_r(k):
    ps = primes_below(k)
    lev = []
    for p in ps:
        L = 0; q = p
        while q < k:
            if k % q:
                L += 1
            q *= p
        lev.append(L)
    lcm = 1
    for x in range(1, k + 1):
        lcm = lcm * x // math.gcd(lcm, x)
    Rk = Fraction(lcm, k)
    out = set()
    for ds in itertools.product(*[range(-L, L + 1) for L in lev]):
        r = Fraction(1)
        for p, d in zip(ps, ds):
            r *= Fraction(p) ** d
        if 1 < r <= Rk:
            out.add(r)
    return sorted(out)

def f(x, k):
    v = mpz(1)
    for j in range(1, k + 1):
        v *= (x + j)
    return v

def M(x, k):
    v = mpz(1)
    for j in range(1, k + 1):
        v = gmpy2.lcm(v, x + j)
    return v

def cf_of_root(a, b, k, digits):
    """continued fraction partial quotients of rho = (a/b)^(1/k), exact up to the common prefix of two bounds"""
    S = mpz(10) ** digits
    Z = mpz(a) * mpz(b) ** (k - 1) * S ** k
    T, exact = iroot(Z, k)           # floor(b * rho * S)
    lo = Fraction(int(T), int(b) * int(S))         # rho in [lo, hi)
    hi = Fraction(int(T) + 1, int(b) * int(S))
    def cf(fr):
        out = []
        n, d = fr.numerator, fr.denominator
        while d:
            q = n // d
            out.append(q)
            n, d = d, n - q * d
        return out
    c1, c2 = cf(lo), cf(hi)
    pref = []
    for u, v in zip(c1, c2):
        if u != v:
            break
        pref.append(u)
    return pref[:-1] if len(pref) > 1 else pref   # drop last (may be truncated)

def gen_cands(k, r, DIG, QMAX=None):
    """all (p, q) = g*(p', q') with 0 < q rho - p < Cq/q, q <= QMAX (via convergents + Worley's theorem)"""
    a, b = r.numerator, r.denominator
    rho = mpmath.root(mpmath.mpf(a) / b, k)
    c = (k * k - 1) * (rho * rho - 1) / (24 * rho)
    C = 2 * c + mpmath.mpf(1) / 10        # margin, validated by validate_deep.py
    Cq = C if k % 2 else 4 * C
    pq = cf_of_root(a, b, k, DIG)
    P = [mpz(1), mpz(pq[0])]; Q = [mpz(0), mpz(1)]
    for t in pq[1:]:
        P.append(t * P[-1] + P[-2]); Q.append(t * Q[-1] + Q[-2])
    if QMAX is None:
        QMAX = mpz(10) ** (DIG // 2 - 5)
    reduced = set()
    AB = int(2 * Cq) + 1
    for i in range(len(P) - 1):
        if Q[i] > QMAX:
            break
        p0, q0, p1, q1 = P[i], Q[i], P[i + 1], Q[i + 1]
        for aa in range(0, AB + 1):
            for bb in range(0, AB + 1):
                if aa * bb >= 2 * Cq and not (aa == 0 or bb == 0):
                    continue
                if (aa == 0 and bb != 1) or (bb == 0 and aa != 1):
                    continue
                for sg in (1, -1):
                    pp = aa * p1 + sg * bb * p0; qq = aa * q1 + sg * bb * q0
                    if qq <= 0 or pp <= 0:
                        continue
                    g = gmpy2.gcd(pp, qq)
                    pp //= g; qq //= g
                    reduced.add((int(pp), int(qq)))
    cands = []
    for (pp, qq) in reduced:
        delta = qq * rho - pp
        if not (delta > 0 and qq * delta < Cq):
            continue
        g = 1
        while g * g * qq * delta < Cq and g * qq <= QMAX:
            cands.append((g * pp, g * qq))
            g += 1
    return cands, Q

import numpy as np

def gen_cands_fast(k, r, DIG, QMAX=None):
    """same output set as gen_cands, but the Worley (a, b) grid is pre-filtered in normalised double precision:
    for q = a q_{i+1} + s b q_i, q*(q rho - p) = (a + s b Qn)(a D1 + s b D0) with Qn = q_i/q_{i+1},
    D_j = delta_j * q_{i+1}, delta_j = q_j rho - p_j (all O(1)); survivors (with margin) are checked exactly."""
    a, b = r.numerator, r.denominator
    rho = mpmath.root(mpmath.mpf(a) / b, k)
    c = (k * k - 1) * (rho * rho - 1) / (24 * rho)
    C = 2 * c + mpmath.mpf(1) / 10
    Cq = C if k % 2 else 4 * C
    Cqf = float(Cq)
    pq = cf_of_root(a, b, k, DIG)
    P = [mpz(1), mpz(pq[0])]; Q = [mpz(0), mpz(1)]
    for t in pq[1:]:
        P.append(t * P[-1] + P[-2]); Q.append(t * Q[-1] + Q[-2])
    if QMAX is None:
        QMAX = mpz(10) ** (DIG // 2 - 5)
    AB = int(2 * Cq) + 1
    A_, B_ = np.meshgrid(np.arange(0, AB + 1, dtype=np.float64), np.arange(0, AB + 1, dtype=np.float64), indexing="ij")
    keep = (A_ * B_ < 2 * Cqf) | ((A_ == 1) & (B_ == 0)) | ((A_ == 0) & (B_ == 1))
    keep &= ~((A_ == 0) & (B_ != 1)) & ~((B_ == 0) & (A_ != 1))
    Af, Bf = A_[keep], B_[keep]
    reduced = set()
    for i in range(len(P) - 1):
        if Q[i] > QMAX:
            break
        p0, q0, p1, q1 = P[i], Q[i], P[i + 1], Q[i + 1]
        d0 = q0 * rho - p0; d1 = q1 * rho - p1
        Qn = float(mpmath.mpf(q0) / q1); D0 = float(d0 * q1); D1 = float(d1 * q1)
        for sg in (1, -1):
            qn = Af + sg * Bf * Qn
            val = qn * (Af * D1 + sg * Bf * D0)
            sel = (qn > 0) & (val > -1e-6) & (val < Cqf + 1e-6)
            for aa, bb in zip(Af[sel], Bf[sel]):
                aa = int(aa); bb = int(bb)
                pp = aa * p1 + sg * bb * p0; qq = aa * q1 + sg * bb * q0
                if qq <= 0 or pp <= 0:
                    continue
                g = gmpy2.gcd(pp, qq)
                reduced.add((int(pp // g), int(qq // g)))
    cands = []
    for (pp, qq) in reduced:
        delta = qq * rho - pp
        if not (delta > 0 and qq * delta < Cq):
            continue
        g = 1
        while g * g * qq * delta < Cq and g * qq <= QMAX:
            cands.append((g * pp, g * qq))
            g += 1
    return cands, Q

def main():
    KMIN, KMAX, DIG = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    X0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    mpmath.mp.dps = DIG + 50
    t0 = time.time()
    tot_cand = tot_sol = 0
    for k in range(KMIN, KMAX + 1):
        rs = admissible_r(k)
        kc = 0; ks = 0; maxq_digits = 0
        for r in rs:
            a, b = r.numerator, r.denominator
            cands, Q = gen_cands_fast(k, r, DIG)
            for (p, q) in cands:
                if k % 2:
                    X, Y = q, p
                    n, m = X - (k + 1) // 2, Y - (k + 1) // 2
                else:
                    if q % 2 == 0 or p % 2 == 0:
                        continue
                    n, m = (q - k - 1) // 2, (p - k - 1) // 2
                if n < 0 or m <= n:
                    continue
                if X0 and (2 * n + k + 1) < 2 * X0:
                    continue
                kc += 1
                if f(m, k) * b == a * f(n, k):
                    ks += 1
                    eq = M(m, k) == M(n, k)
                    print("PRODUCT SOLUTION k=%d r=%s n=%d m=%d disjoint=%s lcm_equal=%s" % (k, r, n, m, m >= n + k, eq), flush=True)
            maxq_digits = max(maxq_digits, len(str(int(min(Q[-1], mpz(10) ** (DIG // 2 - 5))))))
        tot_cand += kc; tot_sol += ks
        print("k=%d admissible_r=%d candidates_tested=%d product_solutions=%d max_q_digits=%d t=%.0fs" % (k, len(rs), kc, ks, maxq_digits, time.time() - t0), flush=True)
    print("TOTAL candidates=%d product_solutions=%d" % (tot_cand, tot_sol))

if __name__ == "__main__":
    main()
