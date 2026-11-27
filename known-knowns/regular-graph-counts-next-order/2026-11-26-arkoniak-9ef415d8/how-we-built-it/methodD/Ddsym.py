#!/usr/bin/env python3
"""Method D at general degree d with a symmetric long-cycle part (Dsym.py's count-vector state, generalised to d).

Same short part and same factors as Dd.py: only the long part changes. Instead of one residual degree per long
cycle (state (d+1)^L), cycles are added one at a time (sorted by length) and the state keeps, per cycle length,
how many of the cycles added so far have each residual 0..d. Every factor applied so far is symmetric under
permuting added cycles of equal length, so nothing is lost. When cycle c is added: its own factor Ia and its cross
factors with fixed points / 2-cycles (Dd.py's rules: Py_{a t} for a t <= d, Pz_{zexp} for wexp, zexp <= d), then its
pair factors with every earlier cycle at once (_touch: a multinomial picks which earlier cycles take k orbits).
Injection key = Dd's (Py_1..Py_d, Pz_1..Pz_d). Arithmetic modulo Dd.PMOD (exact while F < PMOD/2, asserted).
"""
import os, sys
from math import gcd, comb
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import Dd
D = Dd.D


def _ok(inj, d, f, m):
    """short_extract is 0 unless the injected degree fits: sum j*Py_j <= d*f and sum j*Pz_j <= d*m (it only grows)."""
    return (sum((j + 1) * x for j, x in enumerate(inj[:d])) <= d * f
            and sum((j + 1) * x for j, x in enumerate(inj[d:])) <= d * m)


def unary(a, f=10**9, m=10**9):
    d = Dd.DEG; P = Dd.PMOD
    Iav = D.Ia(a, d)
    zi = tuple([0] * (2 * d))
    st = {(u, zi): Iav[u] % P for u in range(d + 1) if Iav[u]}
    crosses = []
    for t in range(1, d + 1):  # long <-> fixed point: prod_p (1 + w y_p^a)
        if a * t <= d:
            crosses.append((t, a * t - 1, Fraction((-1) ** (t - 1), t)))
    g = gcd(a, 2)  # long <-> 2-cycle: prod_q (1 + w^{2/g} z_q^{a/g})^g
    for t in range(1, d + 1):
        wexp, zexp = (2 // g) * t, (a // g) * t
        if wexp <= d and zexp <= d:
            crosses.append((wexp, d + zexp - 1, Fraction(g * (-1) ** (t - 1), t)))
    for wexp, idx, coeff in crosses:
        nxt = {}
        for (u, inj), c in st.items():
            k, ck, fk = 0, Fraction(1), 1
            while u + wexp * k <= d:
                ni = list(inj); ni[idx] += k
                if not _ok(ni, d, f, m):
                    break
                key = (u + wexp * k, tuple(ni))
                nxt[key] = (nxt.get(key, 0) + c * Dd._m(ck / fk)) % P
                k += 1; ck *= coeff; fk *= k
        st = nxt
    return [(u, inj, c) for (u, inj), c in st.items() if c]


def _touch(cnts, groups, a, slots, si, room, out, wt, pend, d):
    """As Dsym._touch: distribute pair-factor orbits from the new cycle (length a) to earlier cycles. cnts read
    only; pend = moves (group, r_from, r_to, m) applied at the end, so each earlier cycle is touched at most once.
    2026-11-21: walks only `slots`, the nonzero (group, residual < d) entries (was every slot, most of them empty)."""
    if si == len(slots):
        cl = [list(x) for x in cnts]
        for g_, r0, r1, m_ in pend:
            cl[g_][r0] -= m_; cl[g_][r1] += m_
        out.append((cl, d - room, wt))
        return
    gi, ri = slots[si]
    b = groups[gi]; g = gcd(a, b); p = b // g; q = a // g  # k orbits: new +k*p, old +k*q
    n = cnts[gi][ri]
    ks = [k for k in range(1, g + 1) if ri + k * q <= d and k * p <= room]

    def rec(idx, left_n, room2, wt2, mv):
        if idx == len(ks):
            _touch(cnts, groups, a, slots, si + 1, room2, out, wt2, pend + mv, d)
            return
        k = ks[idx]; m = 0
        while m <= left_n and m * k * p <= room2:
            w2 = wt2 * comb(left_n, m) * comb(g, k) ** m if m else wt2
            rec(idx + 1, left_n - m, room2 - m * k * p, w2, mv + ([(gi, ri, ri + k * q, m)] if m else []))
            m += 1
    rec(0, n, room, wt, [])


def _reach(rest, b, d):
    """Degrees a cycle of length b can still gain from the cycles in `rest`: sums of k * a'/gcd(a', b), 0 <= k <= gcd(a', b),
    one term per later cycle a' (each later cycle touches it at most once), capped at d."""
    R = {0}
    for a2 in rest:
        g = gcd(a2, b); q = a2 // g
        R = {s + k * q for s in R for k in range(g + 1) if s + k * q <= d}
    return R


def long_Q(longs, f=10**9, m=10**9):
    d = Dd.DEG; P = Dd.PMOD
    longs = sorted(longs)
    groups = sorted(set(longs))
    gidx = {b: i for i, b in enumerate(groups)}
    zero = tuple(tuple([0] * (d + 1)) for _ in groups)
    S = {zero: {tuple([0] * (2 * d)): 1}}
    last = len(longs) - 1
    # 2026-11-21 prune: after step, a cycle of group gi at residual r survives only if d - r is reachable from the later cycles
    reach = [[_reach(longs[st + 1:], b, d) for b in groups] for st in range(len(longs))]
    for step, a in enumerate(longs):
        rch = reach[step]
        un = unary(a, f, m)
        nxt = {}
        for cn, injs in S.items():
            for u, dinj, c in un:
                out = []
                slots = [(gi, ri) for gi in range(len(groups)) for ri in range(d) if cn[gi][ri]]
                _touch(cn, groups, a, slots, 0, d - u, out, 1, [], d)
                for cl, res, wt in out:
                    cl[gidx[a]][res] += 1
                    if step == last and any(sum(x[:d]) for x in cl):
                        continue  # after the last cycle only count vectors with every residual == d reach Q
                    if any(x[r] and (d - r) not in rch[gi] for gi, x in enumerate(cl) for r in range(d)):
                        continue  # some cycle can no longer reach degree d
                    dst = nxt.setdefault(tuple(tuple(x) for x in cl), {})
                    cw = c * wt % P
                    for inj, val in injs.items():
                        ninj = tuple(x + y for x, y in zip(inj, dinj))
                        if not _ok(ninj, d, f, m):
                            continue
                        dst[ninj] = (dst.get(ninj, 0) + val * cw) % P
        S = nxt
    Q = {}
    for cn, injs in S.items():
        if all(sum(x[:d]) == 0 for x in cn):
            for inj, val in injs.items():
                Q[inj] = (Q.get(inj, 0) + val) % P
    return Q


def F_D(lam):
    lam = tuple(lam); N = sum(lam); d = Dd.DEG; P = Dd.PMOD
    if (d * N) % 2:
        return 0
    f = lam.count(1); m = lam.count(2)
    longs = [x for x in lam if x >= 3]
    Q = long_Q(longs, f, m) if longs else {tuple([0] * (2 * d)): 1}
    total = 0
    for inj, c in Q.items():
        if c:
            s = Dd.short_extract(f, m, inj)
            if s:
                total = (total + c * Dd._m(s)) % P
    assert total < P // 2, (lam, 'residue too large: F >= PMOD/2?')
    return total


def set_degree(d):
    Dd.set_degree(d)
