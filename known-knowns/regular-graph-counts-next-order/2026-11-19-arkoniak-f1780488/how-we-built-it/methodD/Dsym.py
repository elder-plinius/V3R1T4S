#!/usr/bin/env python3
"""Method D with a symmetric long-cycle part (d=3).

Same decomposition and same short part as D.py (closed power-sum formula for fixed points and
2-cycles, D.short_extract). Only the long part changes: instead of one residual degree per long
cycle (state (d+1)^L), cycles are added one at a time and the state keeps, per cycle length, how
many of the cycles added so far have each residual degree 0..d. All factors applied so far are
symmetric under permuting added cycles of equal length, so this loses nothing. When cycle c is
added, its pair factors with every earlier cycle are applied at once: c has at most d half-edges
of residual, so only a few earlier cycles are touched (a multinomial picks which ones).
Arithmetic is modulo PMOD (exact for N<=42: every F_3 value there is < 10^73).
"""
import os, sys
from math import gcd, comb, factorial
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import D

PMOD = D.PMOD
d = 3


def unary(a):
    """Options for one long cycle alone: list of (u, (e3,d2,d3), weight mod P): its internal
    factor P_a and its cross factors with the fixed points and 2-cycles (same rule as D.py)."""
    Iav = D.Ia(a, d)
    st = {}
    for u in range(d + 1):
        if Iav[u]:
            st[(u, (0, 0, 0))] = Iav[u] % PMOD
    crosses = []
    for t in range(1, d + 1):  # long <-> fixed point
        if a * t == d:
            crosses.append((t, 0, (-1) ** (t - 1) * pow(t, -1, PMOD) % PMOD))
    g = gcd(a, 2); w0 = 2 // g; z0 = a // g
    for t in range(1, d + 1):  # long <-> 2-cycle
        wexp, zexp = w0 * t, z0 * t
        if wexp > d or zexp > d:
            continue
        if zexp not in (2, 3):
            raise NotImplementedError
        crosses.append((wexp, 1 if zexp == 2 else 2, g * (-1) ** (t - 1) * pow(t, -1, PMOD) % PMOD))
    for wexp, idx, coeff in crosses:
        nxt = {}
        for (u, inj), c in st.items():
            k, ck, fk = 0, 1, 1
            while u + wexp * k <= d:
                ni = list(inj); ni[idx] += k
                key = (u + wexp * k, tuple(ni))
                nxt[key] = (nxt.get(key, 0) + c * ck * pow(fk, -1, PMOD)) % PMOD
                k += 1; ck = ck * coeff % PMOD; fk *= k
        st = nxt
    return [(u, inj, c) for (u, inj), c in st.items() if c]


def _touch(cnts, groups, a, gi, ri, room, out, wt, pend):
    """Distribute pair-factor edges from the new cycle (length a) to earlier cycles.
    cnts: per group, counts per residual, as before this cycle (read only); pend: chosen moves
    (gi, r_from, r_to, m), applied only at the end so a cycle is touched at most once.
    Walk (group gi, residual class ri); room = residual left on the new cycle."""
    while gi < len(groups) and ri > d:
        gi += 1; ri = 0
    if gi == len(groups):
        cl = [list(x) for x in cnts]
        for g_, r0, r1, m_ in pend:
            cl[g_][r0] -= m_; cl[g_][r1] += m_
        out.append((cl, d - room, wt))
        return
    b = groups[gi]; g = gcd(a, b); p = b // g; q = a // g  # k orbits: new +k*p, old +k*q
    n = cnts[gi][ri]
    ks = [k for k in range(1, g + 1) if ri + k * q <= d and k * p <= room]
    def rec(idx, left_n, room2, wt2, mv):
        if idx == len(ks):
            _touch(cnts, groups, a, gi, ri + 1, room2, out, wt2, pend + mv)
            return
        k = ks[idx]; m = 0
        while m <= left_n and m * k * p <= room2:
            w2 = wt2 * comb(left_n, m) * comb(g, k) ** m if m else wt2
            rec(idx + 1, left_n - m, room2 - m * k * p, w2, mv + ([(gi, ri, ri + k * q, m)] if m else []))
            m += 1
    rec(0, n, room, wt, [])


def long_Q(longs):
    longs = sorted(longs)
    groups = sorted(set(longs))
    gidx = {b: i for i, b in enumerate(groups)}
    zero = tuple(tuple([0] * (d + 1)) for _ in groups)
    S = {zero: {(0, 0, 0): 1}}  # count vectors -> {injection (e3,d2,d3): value}
    for a in longs:
        un = unary(a)
        nxt = {}
        for cn, injs in S.items():
            for u, dinj, c in un:
                out = []
                _touch(cn, groups, a, 0, 0, d - u, out, 1, [])
                for cn2, res, wt in out:
                    cl = cn2; cl[gidx[a]][res] += 1
                    dst = nxt.setdefault(tuple(tuple(x) for x in cl), {})
                    cw = c * wt % PMOD
                    for inj, val in injs.items():
                        ninj = (inj[0] + dinj[0], inj[1] + dinj[1], inj[2] + dinj[2])
                        dst[ninj] = (dst.get(ninj, 0) + val * cw) % PMOD
        S = nxt
    Q = {}
    for cn, injs in S.items():
        if all(sum(x[:d]) == 0 for x in cn):
            for inj, val in injs.items():
                Q[inj] = (Q.get(inj, 0) + val) % PMOD
    return Q


def F_Dsym(lam):
    lam = tuple(lam)
    N = sum(lam)
    if (d * N) % 2:
        return 0
    f = lam.count(1); m = lam.count(2)
    longs = [x for x in lam if x >= 3]
    Q = long_Q(longs) if longs else {(0, 0, 0): 1}
    total = 0
    for (e3, d2, d3), c in Q.items():
        if c == 0:
            continue
        s = D.short_extract(f, m, e3, d2, d3)
        if s:
            total = (total + c * (s.numerator % PMOD) * pow(s.denominator, -1, PMOD)) % PMOD
    return total
