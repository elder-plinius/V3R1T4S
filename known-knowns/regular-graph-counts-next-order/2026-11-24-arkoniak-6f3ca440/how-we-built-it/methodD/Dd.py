#!/usr/bin/env python3
"""Method D for general degree d: F_d(lambda) = number of labeled d-regular simple graphs fixed by a permutation of
cycle type lambda. Same decomposition as D.py (d=3), generalised:

SHORT part (fixed points y_p, 2-cycles z_q): the generating function
    prod_q (1+z_q) * prod_{p<p'} (1+y_p y_p') * prod_{p,q} (1+y_p^2 z_q) * prod_{q<q'} (1+z_q z_q')^2
does not depend on d. Its log in power sums Py_k, Pz_k: fp-fp and 2c-2c terms as in D.py, and the fp-2c cross term
    sum_{k: 2k<=d} (-1)^{k-1}/k Py_{2k} Pz_k        (d=3 keeps only Py_2 Pz_1).
[prod y_p^d prod z_q^d] of a monomial prod Py_j^{a_j} prod Pz_j^{b_j} = N(a; f) * N(b; m), N(c; n) = number of maps of
c_j distinguishable size-j bundles onto n labeled nodes with every node's sizes summing to d (general N_assign below:
sum over how many nodes take each partition of d).

LONG part: residual-degree DP over the long cycles (as D._long_Q). The long-short couplings inject Py_{a t} (a t <= d)
and Pz_{zexp} (zexp <= d) into the short counts; for d >= 4 these include partial fills (Py_3 with d = 4, ...).
Injection vector: (Py_1..Py_d, Pz_1..Pz_d).

Exact Fractions (gate version). Imports from D.py only the degree-independent helpers Ia, exp_poly, _fpfp_terms,
_twotwo_terms."""
import os, sys
from math import gcd, comb, factorial
from fractions import Fraction
from functools import lru_cache
from collections import Counter
sys.path.insert(0, os.environ.get('DPATH', os.path.dirname(os.path.abspath(__file__))))
import D

DEG = 3
MOD = True  # v3: long part and the final sum modulo the Mersenne prime PMOD (exact while F < PMOD/2)
PMOD = (1 << 521) - 1


def _m(x):
    x = Fraction(x)
    return x.numerator % PMOD * pow(x.denominator, -1, PMOD) % PMOD if MOD else x


def set_degree(d):
    global DEG, PARTS
    DEG = d
    PARTS = [Counter(p) for p in _parts(d)]
    N_assign.cache_clear(); _Gy.cache_clear(); _Gz.cache_clear(); _S.cache_clear()


def _parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0:
        yield (); return
    for k in range(min(n, mx), 0, -1):
        for r in _parts(n - k, k):
            yield (k,) + r


@lru_cache(maxsize=None)
def _nodes(idx, rem, n):
    """sum over n_mu (mu = PARTS[idx:]) with sum n_mu = n and sum n_mu m_j(mu) = rem_j of
    1/prod n_mu! * 1/prod_mu (prod_j m_j(mu)!)^{n_mu}   (as a Fraction)."""
    if idx == len(PARTS):
        return Fraction(1) if n == 0 and not any(rem) else Fraction(0)
    mu = PARTS[idx]; w = 1
    for j, c in mu.items():
        w *= factorial(c)
    tot = Fraction(0); k = 0; r = list(rem); fk = 1; wk = 1
    while k <= n and all(x >= 0 for x in r):
        tot += _nodes(idx + 1, tuple(r), n - k) / (fk * wk)
        k += 1; fk *= k; wk *= w
        for j, c in mu.items():
            r[j - 1] -= c
    return tot


@lru_cache(maxsize=None)
def N_assign(counts, n):
    d = DEG
    if any(c < 0 for c in counts) or sum((j + 1) * c for j, c in enumerate(counts)) != d * n:
        return 0
    v = _nodes(0, tuple(counts), n) * factorial(n)
    for c in counts:
        v *= factorial(c)
    assert v.denominator == 1
    return int(v)


@lru_cache(maxsize=None)
def _Gy(f):
    return tuple(D.exp_poly(D._fpfp_terms(DEG), DEG, DEG * f).items())


@lru_cache(maxsize=None)
def _Gz(m):
    return tuple(D.exp_poly(D._twotwo_terms(DEG), DEG, DEG * m).items())


@lru_cache(maxsize=None)
def _S(side, n, shift):
    """sum over G monomials A of coeff * N(A + shift; n)."""
    g = _Gy(n) if side == 0 else _Gz(n)
    tot = Fraction(0)
    for A, c in g:
        v = N_assign(tuple(a + s for a, s in zip(A, shift)), n)
        if v:
            tot += c * v
    return tot


def short_extract(f, m, inj):
    d = DEG
    iy, iz = list(inj[:d]), list(inj[d:])
    ks = [k for k in range(1, d // 2 + 1)]
    total = Fraction(0)

    def rec(i, coef, sy, sz):
        nonlocal total
        if i == len(ks):
            a = _S(0, f, tuple(sy))
            if a:
                b = _S(1, m, tuple(sz))
                if b:
                    total += coef * a * b
            return
        k = ks[i]; c = Fraction((-1) ** (k - 1), k); j = 0; cj = Fraction(1); fj = 1
        sy2, sz2 = list(sy), list(sz)
        while sum((t + 1) * x for t, x in enumerate(sy2)) <= d * f and sum((t + 1) * x for t, x in enumerate(sz2)) <= d * m:
            rec(i + 1, coef * cj / fj, sy2, sz2)
            j += 1; cj *= c; fj *= j
            sy2 = list(sy2); sz2 = list(sz2); sy2[2 * k - 1] += 1; sz2[k - 1] += 1
    rec(0, Fraction(1), iy, iz)
    return total


def long_Q(longs):
    d = DEG; L = len(longs); zi = tuple([0] * (2 * d))
    S = {tuple([0] * L): {zi: _m(1)}}

    def step(trans):
        nonlocal S
        nxt = {}
        for w, inj in S.items():
            for nw, wt, di in trans(w):
                dst = nxt.setdefault(nw, {})
                for key, c in inj.items():
                    nk = tuple(x + y for x, y in zip(key, di)) if di else key
                    dst[nk] = (dst.get(nk, 0) + c * wt) % PMOD if MOD else dst.get(nk, 0) + c * wt
        S = nxt
    for i, a in enumerate(longs):
        Iav = D.Ia(a, d)
        step(lambda w, i=i, Iav=Iav: [(w[:i] + (w[i] + u,) + w[i + 1:], Iav[u], None)
                                      for u in range(d + 1) if Iav[u] and w[i] + u <= d])
    for i in range(L):
        for jx in range(i + 1, L):
            g = gcd(longs[i], longs[jx]); p = longs[jx] // g; q = longs[i] // g

            def tr(w, i=i, jx=jx, g=g, p=p, q=q):
                out = []
                for k in range(0, g + 1):
                    if w[i] + k * p > d or w[jx] + k * q > d:
                        break
                    nw = list(w); nw[i] += k * p; nw[jx] += k * q
                    out.append((tuple(nw), comb(g, k), None))
                return out
            step(tr)

    def cross(i, wexp, idx, coeff):
        def tr(w):
            out = []; k = 0; ck = Fraction(1); fk = 1
            while w[i] + wexp * k <= d:
                di = [0] * (2 * d); di[idx] = k
                out.append((w[:i] + (w[i] + wexp * k,) + w[i + 1:], _m(ck / fk), tuple(di)))
                k += 1; ck *= coeff; fk *= k
            return out
        step(tr)
    for i, a in enumerate(longs):
        for t in range(1, d + 1):  # long <-> fixed point: prod_p (1 + w_i y_p^a)
            if a * t <= d:
                cross(i, t, a * t - 1, Fraction((-1) ** (t - 1), t))
        g = gcd(a, 2)  # long <-> 2-cycle: prod_q (1 + w_i^{2/g} z_q^{a/g})^g
        for t in range(1, d + 1):
            wexp, zexp = (2 // g) * t, (a // g) * t
            if wexp <= d and zexp <= d:
                cross(i, wexp, d + zexp - 1, Fraction(g * (-1) ** (t - 1), t))
        # v2: the cross factors are the last ones touching cycle i, so only w[i] == d can reach the answer
        S = {w: inj for w, inj in S.items() if w[i] == d}
    return S.get(tuple([d] * L), {})


def F_D(lam):
    lam = tuple(lam); N = sum(lam); d = DEG
    if (d * N) % 2:
        return 0
    f = lam.count(1); m = lam.count(2)
    longs = tuple(sorted((a for a in lam if a >= 3), reverse=True))
    Q = long_Q(longs) if longs else {tuple([0] * (2 * d)): _m(1)}
    total = Fraction(0)
    for inj, c in Q.items():
        if c:
            total += c * short_extract(f, m, inj)
    if MOD:
        total = _m(total)
        assert total < PMOD // 2, (lam, 'residue too large: F >= PMOD/2?')
        return total
    assert total.denominator == 1, (lam, total)
    return int(total)
