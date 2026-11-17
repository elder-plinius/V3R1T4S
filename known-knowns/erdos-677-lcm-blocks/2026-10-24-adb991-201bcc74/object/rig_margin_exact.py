#!/usr/bin/env python3
"""Second, independent-arithmetic proof of the R2 margin: same reduction as rig_margin.py (NOTES.md, Task B), but
every quantity is an interval with EXACT rational endpoints (fractions.Fraction; no floating point, no mpmath).
rho is enclosed by [A/2^P, (A+1)/2^P], A = floor((num 2^(Pk) / den)^(1/k)) by exact integer k-th root (bisection-free
Newton on Python ints), verified A^k den <= num 2^(Pk) < (A+1)^k den. Decisions are exact comparisons of rationals.
usage: rig_margin_exact.py KMIN KMAX X0 ETA_NUM ETA_DEN [CF_NUM CF_DEN] [--pbits P] [--out FILE]
"""
import sys, time, math, argparse
sys.dont_write_bytecode = True
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from fractions import Fraction as Q
from deep_cf import admissible_r


class I:
    """closed interval [lo, hi], exact rationals"""
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = Q(lo); self.hi = Q(lo if hi is None else hi)
        assert self.lo <= self.hi

    def __add__(s, o):
        o = o if isinstance(o, I) else I(o)
        return I(s.lo + o.lo, s.hi + o.hi)
    __radd__ = __add__

    def __neg__(s):
        return I(-s.hi, -s.lo)

    def __sub__(s, o):
        return s + (-(o if isinstance(o, I) else I(o)))

    def __mul__(s, o):
        o = o if isinstance(o, I) else I(o)
        p = (s.lo * o.lo, s.lo * o.hi, s.hi * o.lo, s.hi * o.hi)
        return I(min(p), max(p))
    __rmul__ = __mul__

    def inv(s):
        assert s.lo > 0 or s.hi < 0
        return I(1 / s.hi, 1 / s.lo)

    def absI(s):
        if s.lo >= 0:
            return I(s.lo, s.hi)
        if s.hi <= 0:
            return I(-s.hi, -s.lo)
        return I(0, max(-s.lo, s.hi))


def iroot(x, k):
    """floor(x^(1/k)) for int x >= 0"""
    if x < 2:
        return x
    y = 1 << ((x.bit_length() + k - 1) // k)   # >= true root
    while True:
        z = ((k - 1) * y + x // y ** (k - 1)) // k
        if z >= y:
            break
        y = z
    while y ** k > x:
        y -= 1
    while (y + 1) ** k <= x:
        y += 1
    return y


def Fcoeffs(k):
    co = [Q(1)]
    for j in range(1, k + 1):
        a = Q(2 * j - k - 1, 2)
        new = [Q(0)] * (len(co) + 1)
        for i, cc in enumerate(co):
            new[i] += cc * a
            new[i + 1] += cc
        co = new
    return co


def check(k, e, tab, r, X0, eta, CF, P):
    num, den = r.numerator, r.denominator
    A = iroot(num * (1 << (P * k)) // den, k)
    assert A ** k * den <= num * (1 << (P * k)) < (A + 1) ** k * den
    rho = I(Q(A, 1 << P), Q(A + 1, 1 << P))
    w = rho * rho - 1
    rinv = rho.inv()
    c = Q(k * k - 1, 24) * w * rinv
    rp = {0: I(1)}
    for p in range(1, k + 1):
        rp[p] = rp[p - 1] * rho
        rp[-p] = rp[-(p - 1)] * rinv
    out = []
    for sgn in (1, -1):
        fac = CF * (1 + sgn * eta)
        C = c * fac
        D = Q(k * k - 1, 24) * fac * w
        dom = C.lo > 0 and (rho * X0 - C * Q(1, X0) - Q(k - 1, 2)).lo > 0
        mDp = [I(1)]
        for v in range(1, k + 1):
            mDp.append(mDp[-1] * (-D))
        lead = None; tail = I(0); xf = Q(1)
        for t, et, terms in tab:
            S = I(0)
            for v, b in terms:
                S = S + mDp[v] * b
            a = -(rp[k - 2 * t] * S)
            if et:
                a = a + r * et
            if t == 1:
                lead = a
            else:
                xf = xf / (X0 * X0)
                tail = tail + a.absI() * xf
        L = lead if sgn == 1 else -lead
        if dom and L.lo - tail.hi > 0:
            st = "PROVED"
        elif L.hi < 0:
            st = "FAIL"
        else:
            st = "UNDECIDED"
        out.append((st, (L.lo - tail.hi) / L.lo if L.lo > 0 else None))
    sts = [o[0] for o in out]
    status = "PROVED" if sts == ["PROVED", "PROVED"] else ("FAIL" if "FAIL" in sts else "UNDECIDED")
    rel = min(o[1] for o in out) if status == "PROVED" else None
    return status, rel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kmin", type=int); ap.add_argument("kmax", type=int); ap.add_argument("X0", type=int)
    ap.add_argument("eta_num", type=int); ap.add_argument("eta_den", type=int)
    ap.add_argument("cf_num", type=int, nargs="?", default=1); ap.add_argument("cf_den", type=int, nargs="?", default=1)
    ap.add_argument("--pbits", type=int, default=96)
    ap.add_argument("--maxpairs", type=int, default=0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    eta = Q(a.eta_num, a.eta_den); CF = Q(a.cf_num, a.cf_den)
    print("rig_margin_exact: k=%d..%d X0=%d eta=%s CF=%s rho_bits=%d (exact rational intervals)" %
          (a.kmin, a.kmax, a.X0, eta, CF, a.pbits), flush=True)
    outf = open(a.out, "a") if a.out else None
    G = [0, 0, 0]
    for k in range(a.kmin, a.kmax + 1):
        t0 = time.time()
        e = Fcoeffs(k)
        assert e[k] == 1 and e[k - 1] == 0 and all(e[j] == 0 for j in range(k + 1) if (k - j) % 2)
        assert e[k - 2] == -Q(k * (k * k - 1), 24)
        tab = []
        for t in range(1, k + 1):
            j0 = k - 2 * t
            et = e[j0] if 0 <= j0 <= k else Q(0)
            terms = [(v, e[j0 + 2 * v] * math.comb(j0 + 2 * v, v)) for v in range(k + 1)
                     if 0 <= j0 + 2 * v <= k and v <= j0 + 2 * v and e[j0 + 2 * v] != 0]
            tab.append((t, et, terms))
        rs = admissible_r(k)
        if a.maxpairs:
            rs = rs[:a.maxpairs]
        npv = nf = nu = 0; worst = None; wr = None
        for r in rs:
            st, rel = check(k, e, tab, r, a.X0, eta, CF, a.pbits)
            if st == "PROVED":
                npv += 1
                if worst is None or rel < worst:
                    worst, wr = rel, r
            elif st == "FAIL":
                nf += 1
            else:
                nu += 1
            if st != "PROVED" and nf + nu <= 3:
                print("  %s k=%d r=%s" % (st, k, r), flush=True)
        line = "k=%d pairs=%d proved=%d failures=%d undecided=%d time_s=%.1f worst_rel_margin_lower_bound=%s at r=%s" % (
            k, len(rs), npv, nf, nu, time.time() - t0, "%.8f" % worst if worst is not None else "-", wr)
        print(line, flush=True)
        if outf:
            outf.write(line + "\n"); outf.flush()
        G[0] += len(rs); G[1] += nf; G[2] += nu
    print("TOTAL pairs=%d failures=%d undecided=%d" % tuple(G), flush=True)


if __name__ == "__main__":
    main()
