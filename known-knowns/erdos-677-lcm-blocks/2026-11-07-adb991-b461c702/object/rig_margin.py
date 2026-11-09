#!/usr/bin/env python3
"""Rigorous (interval-arithmetic) proof of the R2 margin, written from the mathematics (see NOTES.md, "Task B").

For k >= 3, 1 < r rational, F(Z) = prod_{j=1..k} (Z + j - (k+1)/2) = sum_j e_j Z^j (e_j exact rationals),
rho = r^(1/k), c = (k^2-1)(rho^2-1)/(24 rho), asserted margin C_lo = c*CF*(1-eta), C_hi = c*CF*(1+eta) (CF = 1 is the
real claim; CF != 1 is only used for negative tests). Claim: for every real X >= X0 the unique real Y > (k-1)/2 with
F(Y) = r F(X) satisfies C_lo < X(rho X - Y) < C_hi.

Reduction (proved in NOTES.md). F is strictly increasing on [(k-1)/2, oo) with F((k-1)/2) = 0. If
rho X - C/X > (k-1)/2 for all X >= X0 (checked: C > 0 and rho X0 - C/X0 > (k-1)/2), then
  X(rho X - Y) < C  <=>  P_C(X) := X^k [r F(X) - F(rho X - C/X)] > 0.
With D = C rho = (k^2-1) CF (1 +- eta)(rho^2 - 1)/24 and e_j = 0 for j != k (mod 2) (asserted exactly),
  P_C(X) = sum_{t=0..k} a_t X^(2k-2t),  a_t = r e_{k-2t} - rho^(k-2t) sum_v e_{k-2t+2v} binom(k-2t+2v, v) (-D)^v
(sum over v >= 0 with 0 <= k-2t+2v <= k), and a_0 = r - rho^k = 0 exactly (dropped by the identity, not numerically).
Sufficient for P_C > 0 on [X0, oo):  a_1 > sum_{t>=2} |a_t| X0^(-2(t-1))  (then a_1 > 0 too).
Upper claim: P_{C_hi} > 0. Lower claim: -P_{C_lo} > 0. Every quantity is an mpmath.iv interval (outward rounding);
rho is enclosed by the dyadic bracket [A/2^P, (A+1)/2^P] with A^k den < num 2^(Pk) < (A+1)^k den checked in exact
integers. A decision is made only on interval endpoints; anything not decided is reported UNDECIDED (= failure).
usage: rig_margin.py KMIN KMAX X0 ETA_NUM ETA_DEN [CF_NUM CF_DEN] [--maxpairs N] [--out FILE]
"""
import sys, time, math, argparse
sys.dont_write_bytecode = True
DEEP = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
sys.path.insert(0, DEEP)
from fractions import Fraction
import mpmath
from mpmath import iv
from deep_cf import admissible_r

IVPREC = 320
PBITS = 256
iv.prec = IVPREC
mpmath.mp.prec = 420


def Fcoeffs(k):
    """exact e_0..e_k of F(Z) = prod_{j=1..k} (Z + j - (k+1)/2), by repeated multiplication"""
    co = [Fraction(1)]
    for j in range(1, k + 1):
        a = Fraction(2 * j - k - 1, 2)
        new = [Fraction(0)] * (len(co) + 1)
        for i, cc in enumerate(co):
            new[i] += cc * a
            new[i + 1] += cc
        co = new
    return co


def ivq(q):
    q = Fraction(q)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def rho_bracket(num, den, k):
    """dyadic interval containing r^(1/k), r = num/den, verified in exact integers"""
    approx = mpmath.root(mpmath.mpf(num) / den, k)
    A = int(mpmath.floor(approx * mpmath.mpf(2) ** PBITS))
    target = num * (1 << (PBITS * k))
    for _ in range(100):
        lo_ok = A ** k * den < target
        hi_ok = (A + 1) ** k * den > target
        if lo_ok and hi_ok:
            break
        A += -1 if not lo_ok else 1
    else:
        raise RuntimeError("bracket")
    lo = mpmath.mpf(A) * mpmath.mpf(2) ** (-PBITS)
    hi = mpmath.mpf(A + 1) * mpmath.mpf(2) ** (-PBITS)
    I = iv.mpf([lo, hi])
    # the interval endpoints must be exactly A/2^P and (A+1)/2^P (no rounding inward)
    assert int(mpmath.mpf(I.a) * mpmath.mpf(2) ** PBITS) == A and int(mpmath.mpf(I.b) * mpmath.mpf(2) ** PBITS) == A + 1
    assert mpmath.mpf(I.a) * mpmath.mpf(2) ** PBITS == A and mpmath.mpf(I.b) * mpmath.mpf(2) ** PBITS == A + 1
    return I


class KData:
    def __init__(self, k):
        self.k = k
        e = Fcoeffs(k)
        assert e[k] == 1 and e[k - 1] == 0
        for j in range(k + 1):
            if (k - j) % 2 == 1:
                assert e[j] == 0, (k, j)
        self.e = e
        # table: for t = 1..k: (e_{k-2t} as iv or None, [(v, b_tv iv)])
        self.tab = []
        for t in range(1, k + 1):
            j0 = k - 2 * t
            et = ivq(e[j0]) if 0 <= j0 <= k and e[j0] != 0 else None
            terms = []
            for v in range(0, k + 1):
                j = j0 + 2 * v
                if j < 0 or j > k or v > j:
                    continue
                if e[j] == 0:
                    continue
                terms.append((v, ivq(e[j] * math.comb(j, v))))
            self.tab.append((t, et, terms))
        self.kk1 = iv.mpf(k * k - 1)
        self.half = ivq(Fraction(k - 1, 2))


def check_pair(kd, r, X0, eta, CF):
    """returns (status, info). status in PROVED / FAIL / UNDECIDED"""
    k = kd.k
    rho = rho_bracket(r.numerator, r.denominator, k)
    riv = ivq(r)
    w = rho * rho - 1
    c = kd.kk1 * w / (24 * rho)
    X0iv = iv.mpf(X0)
    invX02 = 1 / (X0iv * X0iv)
    # powers of rho from -k .. k
    rpow = {0: iv.mpf(1)}
    for p in range(1, k + 1):
        rpow[p] = rpow[p - 1] * rho
    rinv = 1 / rho
    for p in range(1, k + 1):
        rpow[-p] = rpow[-(p - 1)] * rinv
    res = {}
    for side, sgn in (("hi", 1), ("lo", -1)):
        fac = ivq(CF * (1 + sgn * eta))
        C = c * fac
        D = kd.kk1 * fac * w / 24
        # domain: C > 0 and rho X0 - C/X0 > (k-1)/2
        dom = (C.a > 0) and ((rho * X0iv - C / X0iv - kd.half).a > 0)
        mD = -D
        mDp = [iv.mpf(1)]
        for v in range(1, k + 1):
            mDp.append(mDp[-1] * mD)
        lead = None
        tail = iv.mpf(0)
        Xfac = iv.mpf(1)
        for t, et, terms in kd.tab:
            S = iv.mpf(0)
            for v, b in terms:
                S = S + b * mDp[v]
            a = -(rpow[k - 2 * t] * S)
            if et is not None:
                a = a + riv * et
            if t == 1:
                lead = a
            else:
                Xfac = Xfac * invX02
                tail = tail + abs(a) * Xfac
        L = lead if sgn == 1 else -lead
        diff = L - tail
        if dom and diff.a > 0:
            st = "PROVED"
        elif L.b < 0:
            st = "FAIL"            # leading coefficient has the wrong sign: claim false for large X
        else:
            st = "UNDECIDED"
        rel = diff / L if L.a > 0 else None
        res[side] = (st, dom, L, tail, rel)
    sts = [res[s][0] for s in ("hi", "lo")]
    if all(s == "PROVED" for s in sts):
        status = "PROVED"
    elif "FAIL" in sts:
        status = "FAIL"
    else:
        status = "UNDECIDED"
    return status, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kmin", type=int); ap.add_argument("kmax", type=int); ap.add_argument("X0", type=int)
    ap.add_argument("eta_num", type=int); ap.add_argument("eta_den", type=int)
    ap.add_argument("cf_num", type=int, nargs="?", default=1); ap.add_argument("cf_den", type=int, nargs="?", default=1)
    ap.add_argument("--maxpairs", type=int, default=0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    eta = Fraction(args.eta_num, args.eta_den)
    CF = Fraction(args.cf_num, args.cf_den)
    print("rig_margin: k=%d..%d X0=%d eta=%s CF=%s ivprec=%d rho_bits=%d" %
          (args.kmin, args.kmax, args.X0, eta, CF, IVPREC, PBITS), flush=True)
    outf = open(args.out, "a") if args.out else None
    gtot = gbad = gund = 0
    for k in range(args.kmin, args.kmax + 1):
        t0 = time.time()
        kd = KData(k)
        rs = admissible_r(k)
        if args.maxpairs:
            rs = rs[:args.maxpairs]
        npr = nf = nu = 0
        worst = None; worst_r = None
        for r in rs:
            st, res = check_pair(kd, r, args.X0, eta, CF)
            if st == "PROVED":
                npr += 1
                m = min(mpmath.mpf(res[s][4].a) for s in ("hi", "lo"))
                if worst is None or m < worst:
                    worst, worst_r = m, r
            else:
                if st == "FAIL":
                    nf += 1
                else:
                    nu += 1
                if nf + nu <= 5:
                    info = {s: (res[s][0], res[s][1], mpmath.nstr(mpmath.mpf(res[s][2].a), 5),
                                mpmath.nstr(mpmath.mpf(res[s][2].b), 5), mpmath.nstr(mpmath.mpf(res[s][3].b), 5))
                            for s in ("hi", "lo")}
                    print("  %s k=%d r=%s  {side: (status, domain_ok, lead_lo, lead_hi, tail_hi)} %s" %
                          (st, k, r, info), flush=True)
        dt = time.time() - t0
        line = ("k=%d pairs=%d proved=%d failures=%d undecided=%d time_s=%.1f worst_rel_margin_lower_bound=%s at r=%s"
                % (k, len(rs), npr, nf, nu, dt, mpmath.nstr(worst, 8) if worst is not None else "-", worst_r))
        print(line, flush=True)
        if outf:
            outf.write(line + "\n"); outf.flush()
        gtot += len(rs); gbad += nf; gund += nu
    print("TOTAL pairs=%d failures=%d undecided=%d" % (gtot, gbad, gund), flush=True)


if __name__ == "__main__":
    main()
