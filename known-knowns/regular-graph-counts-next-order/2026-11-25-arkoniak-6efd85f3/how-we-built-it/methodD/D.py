#!/usr/bin/env python3
"""Method D: hybrid exact counter for F_d(lambda), d=3 primary.

Decomposition of lambda's cycles into LONG (length>=3) and SHORT (length 1 = fixed
point, length 2 = two-cycle).

SHORT part: a CLOSED combinatorial formula via the configuration model expressed in
power sums.  The generating function (Eq 2.6 restricted to short nodes)

    prod_q (1+z_q)                       [2-cycle internal edge]
  * prod_{p<p'} (1+y_p y_{p'})           [fp-fp edge]
  * prod_{p,q} (1+y_p^2 z_q)             [fp-2cycle orbit]
  * prod_{q<q'} (1+z_q z_{q'})^2         [2cycle-2cycle, g=2 parallel orbits]

is symmetric in the fp variables y_p and in the 2-cycle variables z_q (one variable
per 2-cycle, since its two vertices always share the same degree).  Writing the log
of this product in the power sums Py_k=sum_p y_p^k, Pz_k=sum_q z_q^k and exponentiating,
the coefficient [prod y_p^d prod z_q^d] of any monomial in the power sums factors as
N(.;f)*N(.;m), where N(c_1,..,c_d;n) = number of ways to assign c_j distinguishable
"degree-j half-edge bundles" to n labeled nodes so each node's bundles sum to exactly d.
For d=3, N has a closed form (below).  This depends ONLY on the counts f, m (and the
injected residuals), never on a per-node or per-cycle DP, and is not method A/B.

LONG part: the few long cycles (<=~12) are handled by an exact method-B-style product
DP over their residual-degree vector (internal factors P_a, long-long pair factors).
The long<->short coupling uses the SAME general orbit rule: each long<->short pair
factor is expanded (in power sums on the short side) and injects, for each long DP
state, residual "half-edge bundles" Py_3 / Pz_2 / Pz_3 into the short counts, whose
closed short-part value is then multiplied in.

This file is self-contained; it imports nothing from method A or B.
"""
from math import gcd, comb, factorial, perm
from fractions import Fraction
from functools import lru_cache
from collections import Counter

DEG = 3
MODULAR = True  # exact while F < PMOD (N<=42); False = original Fraction path


def set_degree(d):
    global DEG
    DEG = d
    _Gy_cache.clear()
    _Gz_cache.clear()


# ---------------------------------------------------------------------------
# Internal-edge polynomial  I_a[u] = [x^u] P_a(x),  P_a=(1+x^2)^floor((a-1)/2)(1+x)^[a even]
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def Ia(a, d):
    poly = [1]

    def mul(p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i, ci in enumerate(p):
            if ci:
                for j, cj in enumerate(q):
                    r[i + j] += ci * cj
        return r
    for _ in range((a - 1) // 2):
        poly = mul(poly, [1, 0, 1])
    if a % 2 == 0:
        poly = mul(poly, [1, 1])
    return tuple(poly[u] if u < len(poly) else 0 for u in range(d + 1))


# ---------------------------------------------------------------------------
# N(c_1,...,c_d ; n): assign c_j distinguishable degree-j bundles to n labeled nodes,
# each node's bundles summing to exactly d.  Closed form for d=3.
#   groups summing to 3 : {1,1,1}(alpha), {2,1}(beta), {3}(gamma)
#   A1=c_1, A2=c_2, A3=c_3 ;  g_beta=A2, g_gamma=A3, g_alpha=n-A2-A3
#   valid iff A1+2A2+3A3 = 3n and A2+A3<=n
#   N = P(n,A3) * P(n-A3,A2) * A1!/(6^{g_alpha})
# ---------------------------------------------------------------------------
def N_assign(counts, n):
    d = DEG
    if d != 3:
        raise NotImplementedError("N_assign closed form implemented for d=3 only")
    A1, A2, A3 = counts  # counts of degree-1,2,3 bundles
    if A1 < 0 or A2 < 0 or A3 < 0:
        return 0
    if A1 + 2 * A2 + 3 * A3 != 3 * n:
        return 0
    if A2 + A3 > n:
        return 0
    g_alpha = n - A2 - A3
    # A1 must equal 3*g_alpha + A2 (implied by weight==3n); guard anyway
    if A1 != 3 * g_alpha + A2:
        return 0
    val = perm(n, A3) * perm(n - A3, A2) * (factorial(A1) // (6 ** g_alpha))
    return val


# ---------------------------------------------------------------------------
# Power-sum log-expansion of the short generating function (per species).
# Returns list of (Fraction coeff, exponent-tuple over Py_1..Py_d) etc.
# ---------------------------------------------------------------------------
def _fpfp_terms(d):
    """log prod_{p<p'}(1+y_p y_{p'}) in power sums Py_1..Py_d (truncate idx>d)."""
    terms = {}

    def add(vec, c):
        terms[vec] = terms.get(vec, Fraction(0)) + c
    for k in range(1, d + 1):
        c = Fraction((-1) ** (k - 1), 2 * k)
        # Py_k^2
        v = [0] * d
        v[k - 1] += 2
        add(tuple(v), c)
        # - Py_{2k}
        if 2 * k <= d:
            v = [0] * d
            v[2 * k - 1] += 1
            add(tuple(v), -c)
    return [(c, vec) for vec, c in terms.items() if c != 0]


def _twotwo_terms(d):
    """log [ prod_q(1+z_q) * prod_{q<q'}(1+z_q z_{q'})^2 ] in Pz_1..Pz_d."""
    terms = {}

    def add(vec, c):
        terms[vec] = terms.get(vec, Fraction(0)) + c
    # internal: log prod_q(1+z_q) = sum_j (-1)^{j-1}/j Pz_j
    for j in range(1, d + 1):
        v = [0] * d
        v[j - 1] += 1
        add(tuple(v), Fraction((-1) ** (j - 1), j))
    # 2cycle-2cycle: 2 * sum_{k} (-1)^{k-1}/(2k)(Pz_k^2 - Pz_{2k})
    for k in range(1, d + 1):
        c = Fraction((-1) ** (k - 1), k)  # = 2 * (-1)^{k-1}/(2k)
        v = [0] * d
        v[k - 1] += 2
        add(tuple(v), c)
        if 2 * k <= d:
            v = [0] * d
            v[2 * k - 1] += 1
            add(tuple(v), -c)
    return [(c, vec) for vec, c in terms.items() if c != 0]


def exp_poly(terms, dim, max_weight):
    """exp of a polynomial (list of (Fraction coeff, exp-tuple over power sums
    Pow_1..Pow_dim)) as a dict exp-tuple -> Fraction, truncated to
    weight = sum_k k*exp_k <= max_weight (weight = total variable-degree)."""
    result = {tuple([0] * dim): Fraction(1)}
    for c, vec in terms:
        wv = sum((i + 1) * e for i, e in enumerate(vec))
        if wv == 0 or wv > max_weight:
            # wv==0 impossible for nonconstant term; skip if too heavy alone
            if wv > max_weight:
                continue
        # series sum_{k>=0} c^k/k! * (k*vec)
        series = []
        k = 0
        ck = Fraction(1)
        fk = 1
        while k * wv <= max_weight:
            series.append((k, ck / fk))
            k += 1
            ck *= c
            fk *= k
        nxt = {}
        for base, bc in result.items():
            bw = sum((i + 1) * e for i, e in enumerate(base))
            for k, coef in series:
                if bw + k * wv > max_weight:
                    break
                ne = list(base)
                for i, e in enumerate(vec):
                    ne[i] += k * e
                key = tuple(ne)
                nxt[key] = nxt.get(key, Fraction(0)) + bc * coef
        result = nxt
    return result


_Gy_cache = {}
_Gz_cache = {}


def _Gy(f):
    """exp(log prod fp-fp) as dict (A1,A2,A3)->Fraction, weight<=3f."""
    key = (f, DEG)
    if key in _Gy_cache:
        return _Gy_cache[key]
    g = exp_poly(_fpfp_terms(DEG), DEG, DEG * f)
    _Gy_cache[key] = g
    return g


def _Gz(m):
    key = (m, DEG)
    if key in _Gz_cache:
        return _Gz_cache[key]
    g = exp_poly(_twotwo_terms(DEG), DEG, DEG * m)
    _Gz_cache[key] = g
    return g


def _SY(f, j, e3):
    """sum over Gy monomials of coeff * N_y(A1, A2+j, A3+e3; f)."""
    g = _Gy(f)
    tot = Fraction(0)
    for (A1, A2, A3), c in g.items():
        v = N_assign((A1, A2 + j, A3 + e3), f)
        if v:
            tot += c * v
    return tot


def _SZ(m, j, d2, d3):
    """sum over Gz monomials of coeff * N_z(B1+j, B2+d2, B3+d3; m)."""
    g = _Gz(m)
    tot = Fraction(0)
    for (B1, B2, B3), c in g.items():
        v = N_assign((B1 + j, B2 + d2, B3 + d3), m)
        if v:
            tot += c * v
    return tot


def short_extract(f, m, e3=0, d2=0, d3=0):
    """[prod y^d prod z^d] exp(E_short) * Py_3^{e3} Pz_2^{d2} Pz_3^{d3}.

    exp(E_short) = Gy(y)*Gz(z)*exp(Py_2 Pz_1); the last couples via j:
      exp(Py_2 Pz_1) = sum_j (1/j!) Py_2^j Pz_1^j.
    (d=3: the only fp-2cycle cross term is Py_2 Pz_1.)
    """
    if DEG != 3:
        raise NotImplementedError
    jmax_f = (3 * f) // 2 if f > 0 else 0
    jmax_m = 3 * m if m > 0 else 0
    jmax = min(jmax_f, jmax_m)
    total = Fraction(0)
    fj = 1
    for j in range(0, jmax + 1):
        if j > 0:
            fj *= j
        sy = _SY(f, j, e3)
        if sy == 0:
            continue
        sz = _SZ(m, j, d2, d3)
        if sz == 0:
            continue
        total += (sy * sz) / fj
    return total


# ---------------------------------------------------------------------------
# LONG part + long<->short coupling.
# Dlong: dict  w-degree-tuple (over long cycles) -> dict( (e3,d2,d3) -> Fraction ).
# ---------------------------------------------------------------------------
def _long_Q(longs):
    """Return Q: dict (e3,d2,d3)->Fraction = [prod w_i^d] of
    (long internal * long-long pairs * exp(long<->short cross))."""
    d = DEG
    L = len(longs)
    if L == 0:
        return {(0, 0, 0): Fraction(1)}
    zero_w = tuple([0] * L)
    D = {zero_w: {(0, 0, 0): Fraction(1)}}

    def mul_w_only(transform):
        """transform(state_w) -> list of (new_w, int_weight). injections unchanged."""
        nonlocal D
        nxt = {}
        for w, inj in D.items():
            for nw, wt in transform(w):
                dst = nxt.setdefault(nw, {})
                for key, c in inj.items():
                    dst[key] = dst.get(key, Fraction(0)) + c * wt
        D = nxt

    # internal factors
    for i, a in enumerate(longs):
        Iav = Ia(a, d)

        def tr(w, i=i, Iav=Iav):
            out = []
            for u in range(0, d + 1):
                if Iav[u] and w[i] + u <= d:
                    nw = list(w)
                    nw[i] += u
                    out.append((tuple(nw), Iav[u]))
            return out
        mul_w_only(tr)

    # long-long pair factors
    for i in range(L):
        for jx in range(i + 1, L):
            ai, aj = longs[i], longs[jx]
            g = gcd(ai, aj)
            p = aj // g
            q = ai // g

            def tr(w, i=i, jx=jx, g=g, p=p, q=q):
                out = []
                kmax = min(g, (d - w[i]) // p if p else g, (d - w[jx]) // q if q else g)
                for k in range(0, kmax + 1):
                    nw = list(w)
                    nw[i] += k * p
                    nw[jx] += k * q
                    out.append((tuple(nw), comb(g, k)))
                return out
            mul_w_only(tr)

    # long<->short cross factors (inject into short counts)
    def mul_cross(i, wexp, inj_index, coeff):
        """multiply by exp(coeff * w_i^{wexp} * P_short) as a series in connections k.
        inj_index: 0->e3, 1->d2, 2->d3.  coeff: Fraction."""
        nonlocal D
        # series over k>=0: term coeff^k/k! , w_i += wexp*k , inj[inj_index]+=k
        nxt = {}
        for w, inj in D.items():
            k = 0
            ck = Fraction(1)
            fk = 1
            while w[i] + wexp * k <= d:
                nw = list(w)
                nw[i] += wexp * k
                nwt = tuple(nw)
                dst = nxt.setdefault(nwt, {})
                factor = ck / fk
                for key, c in inj.items():
                    nkey = list(key)
                    nkey[inj_index] += k
                    nk = tuple(nkey)
                    dst[nk] = dst.get(nk, Fraction(0)) + c * factor
                k += 1
                ck *= coeff
                fk *= k
        D = nxt

    for i, a in enumerate(longs):
        # long <-> fixed point : factor prod_p (1 + w_i^1 y_p^a)
        #   log term t: w_i^t * y^{a t}; keep a*t<=d, t<=d; inject Py_{a t}
        for t in range(1, d + 1):
            yexp = a * t
            if yexp > d or t > d:
                continue
            if yexp == d:  # fills a fp -> inject Py_d  (d=3 -> e3)
                coeff = Fraction((-1) ** (t - 1), t)
                mul_cross(i, t, 0, coeff)
            # (yexp<d would need a partial-fp injection; impossible for a>=3,d=3)
        # long <-> 2-cycle : factor prod_q (1 + w_i^{2/g} z_q^{a/g})^g
        g = gcd(a, 2)
        wexp0 = 2 // g
        zexp0 = a // g
        for t in range(1, d + 1):
            wexp = wexp0 * t
            zexp = zexp0 * t
            if wexp > d or zexp > d:
                continue
            coeff = Fraction(g * (-1) ** (t - 1), t)
            if zexp == 2:
                mul_cross(i, wexp, 1, coeff)
            elif zexp == 3:
                mul_cross(i, wexp, 2, coeff)
            elif zexp == 1:
                # would inject Pz_1 (partial); not reachable for a>=3
                raise NotImplementedError("unexpected zexp=1 coupling")

    # extract w == (d,d,...,d)
    full = tuple([d] * L)
    return D.get(full, {})


PMOD = (1 << 521) - 1  # Mersenne prime; every F_3 value at N<=42 is < 10^73 << PMOD


def _long_Q_mod(longs):
    """_long_Q with integers modulo the prime PMOD instead of Fraction (same recurrence)."""
    """Return Q: dict (e3,d2,d3)->Fraction = [prod w_i^d] of
    (long internal * long-long pairs * exp(long<->short cross))."""
    d = DEG
    L = len(longs)
    if L == 0:
        return {(0, 0, 0): 1}
    zero_w = tuple([0] * L)
    D = {zero_w: {(0, 0, 0): 1}}

    def mul_w_only(transform):
        """transform(state_w) -> list of (new_w, int_weight). injections unchanged."""
        nonlocal D
        nxt = {}
        for w, inj in D.items():
            for nw, wt in transform(w):
                dst = nxt.setdefault(nw, {})
                for key, c in inj.items():
                    dst[key] = (dst.get(key, 0) + c * wt) % PMOD
        D = nxt

    # internal factors
    for i, a in enumerate(longs):
        Iav = Ia(a, d)

        def tr(w, i=i, Iav=Iav):
            out = []
            for u in range(0, d + 1):
                if Iav[u] and w[i] + u <= d:
                    nw = list(w)
                    nw[i] += u
                    out.append((tuple(nw), Iav[u]))
            return out
        mul_w_only(tr)

    # long-long pair factors
    for i in range(L):
        for jx in range(i + 1, L):
            ai, aj = longs[i], longs[jx]
            g = gcd(ai, aj)
            p = aj // g
            q = ai // g

            def tr(w, i=i, jx=jx, g=g, p=p, q=q):
                out = []
                kmax = min(g, (d - w[i]) // p if p else g, (d - w[jx]) // q if q else g)
                for k in range(0, kmax + 1):
                    nw = list(w)
                    nw[i] += k * p
                    nw[jx] += k * q
                    out.append((tuple(nw), comb(g, k)))
                return out
            mul_w_only(tr)

    # long<->short cross factors (inject into short counts)
    def mul_cross(i, wexp, inj_index, coeff):
        """multiply by exp(coeff * w_i^{wexp} * P_short) as a series in connections k.
        inj_index: 0->e3, 1->d2, 2->d3.  coeff: Fraction."""
        nonlocal D
        # series over k>=0: term coeff^k/k! , w_i += wexp*k , inj[inj_index]+=k
        nxt = {}
        for w, inj in D.items():
            k = 0
            ck = 1
            fk = 1
            while w[i] + wexp * k <= d:
                nw = list(w)
                nw[i] += wexp * k
                nwt = tuple(nw)
                dst = nxt.setdefault(nwt, {})
                factor = ck * pow(fk, -1, PMOD) % PMOD
                for key, c in inj.items():
                    nkey = list(key)
                    nkey[inj_index] += k
                    nk = tuple(nkey)
                    dst[nk] = (dst.get(nk, 0) + c * factor) % PMOD
                k += 1
                ck = ck * coeff % PMOD
                fk *= k
        D = nxt

    for i, a in enumerate(longs):
        # long <-> fixed point : factor prod_p (1 + w_i^1 y_p^a)
        #   log term t: w_i^t * y^{a t}; keep a*t<=d, t<=d; inject Py_{a t}
        for t in range(1, d + 1):
            yexp = a * t
            if yexp > d or t > d:
                continue
            if yexp == d:  # fills a fp -> inject Py_d  (d=3 -> e3)
                coeff = (-1) ** (t - 1) * pow(t, -1, PMOD) % PMOD
                mul_cross(i, t, 0, coeff)
            # (yexp<d would need a partial-fp injection; impossible for a>=3,d=3)
        # long <-> 2-cycle : factor prod_q (1 + w_i^{2/g} z_q^{a/g})^g
        g = gcd(a, 2)
        wexp0 = 2 // g
        zexp0 = a // g
        for t in range(1, d + 1):
            wexp = wexp0 * t
            zexp = zexp0 * t
            if wexp > d or zexp > d:
                continue
            coeff = g * (-1) ** (t - 1) * pow(t, -1, PMOD) % PMOD
            if zexp == 2:
                mul_cross(i, wexp, 1, coeff)
            elif zexp == 3:
                mul_cross(i, wexp, 2, coeff)
            elif zexp == 1:
                # would inject Pz_1 (partial); not reachable for a>=3
                raise NotImplementedError("unexpected zexp=1 coupling")

    # extract w == (d,d,...,d)
    full = tuple([d] * L)
    return D.get(full, {})


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------
def F_D(lam):
    lam = tuple(lam)
    N = sum(lam)
    if (DEG * N) % 2 != 0:
        return 0
    cnt = Counter(lam)
    f = cnt.get(1, 0)
    m = cnt.get(2, 0)
    longs = tuple(sorted((a for a in lam if a >= 3), reverse=True))
    if MODULAR:
        Q = _long_Q_mod(longs)
        total = 0
        for (e3, d2, d3), c in Q.items():
            if c == 0:
                continue
            s = short_extract(f, m, e3, d2, d3)
            if s:
                total = (total + c * (s.numerator % PMOD) * pow(s.denominator, -1, PMOD)) % PMOD
        return total
    Q = _long_Q(longs)
    total = Fraction(0)
    for (e3, d2, d3), c in Q.items():
        if c == 0:
            continue
        s = short_extract(f, m, e3, d2, d3)
        if s:
            total += c * s
    if total.denominator != 1:
        raise ValueError("non-integer result %s for lam=%s" % (total, lam))
    return int(total)


if __name__ == "__main__":
    import sys
    tests = [((1, 1), 0), ((1, 1, 1, 1), 1), ((2, 2), 1), ((1, 1, 2), 1),
             ((2, 2, 2), 20), ((1,) * 6, 70), ((3, 3), 4), ((3, 1), 1),
             ((3, 2), 0), ((4, 2), 2), ((6,), 2), ((2, 2, 2, 2), 451),
             ((1, 1, 2, 2), 6)]
    for lam, exp in tests:
        got = F_D(lam)
        print(lam, got, exp, "OK" if got == exp else "**MISMATCH**")
