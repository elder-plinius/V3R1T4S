#!/usr/bin/env python3
"""Short part of method D by a vertex DP (replacement candidate for Dd._S, whose memo grows ~x2.3 per +2 fixed points).

_S(side, n, shift) = [prod_p x_p^d]  G(x) * prod_j P_j^{shift_j}  over n labelled vertices, where
  side 0 (fixed points): G = prod_{p<p'} (1 + x_p x_p')            (pair orbits g = 1, no self term)
  side 1 (2-cycles):     G = prod_q (1 + x_q) prod_{q<q'} (1 + x_q x_q')^2   (g = 2, one optional self orbit)
and P_j = sum_p x_p^j is a bundle of j stubs on one vertex (shift_j distinguishable bundles).
Vertices are added one at a time; the state keeps, for the vertices added so far, how many still need r more pair
orbits from later vertices (r = 1..d), and how many bundles of each size are left. The new vertex takes bundles,
its optional self orbit, k orbits with some earlier vertices (comb(g, k) each, chosen by a multinomial over residual
classes); what it still needs becomes its residual. Exact integers."""
from math import comb
from functools import lru_cache


def S(d, side, n, shift):
    g = 1 if side == 0 else 2
    selfopt = side == 1
    shift = tuple(shift)
    if sum((j + 1) * c for j, c in enumerate(shift)) > d * n:
        return 0
    # state: (R tuple len d: R[r-1] = #added vertices needing r more, B tuple bundles left) -> ways
    st = {(tuple([0] * d), shift): 1}
    for v in range(n):
        left = n - v - 1  # vertices after this one
        nxt = {}
        for (R, B), w in st.items():
            # bundle choices for the new vertex
            for load, bw, B2 in _bundles(B, d):
                for so in ((0, 1) if selfopt else (0,)):
                    need = d - load - so
                    if need < 0:
                        continue
                    for R2, used, ew in _edges(R, need, g, d):
                        res = need - used
                        if res > left * g:
                            continue
                        R3 = list(R2)
                        if res:
                            R3[res - 1] += 1
                        # prune: every earlier vertex needs at most g per later vertex
                        if any(R3[r - 1] for r in range(left * g + 1, d + 1)):
                            continue
                        if sum(r * x for r, x in enumerate(R3, 1)) > left * d:
                            continue  # v2: later vertices have at most left*d stubs for the open residual
                        if sum((j + 1) * c for j, c in enumerate(B2)) > d * left:
                            continue
                        key = (tuple(R3), B2)
                        nxt[key] = nxt.get(key, 0) + w * bw * ew
        st = nxt
    return st.get((tuple([0] * d), tuple([0] * d)), 0)


def _bundles(B, d):
    """(load, weight, B_left): the new vertex takes c_j of the B_j remaining j-bundles, sum j c_j <= d."""
    out = []

    def rec(j, load, wt, Bl):
        if j == len(B):
            out.append((load, wt, tuple(Bl))); return
        size = j + 1; c = 0
        while c <= B[j] and load + c * size <= d:
            Bl2 = list(Bl); Bl2[j] -= c
            rec(j + 1, load + c * size, wt * comb(B[j], c), Bl2)
            c += 1
    rec(0, 0, 1, list(B))
    return out


@lru_cache(maxsize=4000)
def _edges(R, need, g, d):
    """(R_after, orbits used by the new vertex, weight): for each residual class r, choose m_k earlier vertices
    taking k orbits (k = 1..min(g, r)); they move to residual r - k."""
    out = []

    def rec(r, Rl, used, wt):
        if r > d:
            out.append((tuple(Rl), used, wt)); return
        n_r = R[r - 1]
        ks = [k for k in range(1, g + 1) if k <= r]

        def rk(i, avail, Rl2, used2, wt2):
            if i == len(ks):
                rec(r + 1, Rl2, used2, wt2); return
            k = ks[i]; m = 0
            while m <= avail and used2 + m * k <= need:
                Rl3 = list(Rl2)
                if m:
                    Rl3[r - 1] -= m
                    if r - k:
                        Rl3[r - k - 1] += m
                rk(i + 1, avail - m, Rl3, used2 + m * k, wt2 * comb(avail, m) * comb(g, k) ** m)
                m += 1
        rk(0, n_r, Rl, used, wt)
    rec(1, list(R), 0, 1)
    return tuple(out)


def S_all(d, side, n, shifts, P=None):
    """{shift: S(d, side, n, shift)} for every shift in `shifts` from ONE vertex DP: bundles are emitted by the
    vertices instead of consumed (state B = bundles emitted so far, capped by the per-size maximum over `shifts`),
    with weight 1/prod c_j! per vertex; at the end S(shift) = value[shift] * prod shift_j!. Modulo P if given, else Fraction."""
    from fractions import Fraction
    from math import factorial
    g = 1 if side == 0 else 2
    selfopt = side == 1
    shifts = [tuple(s) for s in shifts]
    cap = [max((s[j] for s in shifts), default=0) for j in range(d)]
    capw = max((sum((j + 1) * c for j, c in enumerate(s)) for s in shifts), default=0)
    inv = (lambda x: pow(x, -1, P)) if P else (lambda x: Fraction(1, x))
    red = (lambda x: x % P) if P else (lambda x: x)
    st = {(tuple([0] * d), tuple([0] * d)): 1}
    for v in range(n):
        left = n - v - 1
        nxt = {}
        for (R, B), w in st.items():
            bw0 = sum((j + 1) * c for j, c in enumerate(B))
            for load, bw, B2 in _emit(B, cap, d, capw - bw0, inv):
                for so in ((0, 1) if selfopt else (0,)):
                    need = d - load - so
                    if need < 0:
                        continue
                    for R2, used, ew in _edges(R, need, g, d):
                        res = need - used
                        if res > left * g:
                            continue
                        R3 = list(R2)
                        if res:
                            R3[res - 1] += 1
                        if any(R3[r - 1] for r in range(left * g + 1, d + 1)):
                            continue
                        if sum(r * x for r, x in enumerate(R3, 1)) > left * d:
                            continue  # v2: later vertices have at most left*d stubs for the open residual
                        key = (tuple(R3), B2)
                        nxt[key] = red(nxt.get(key, 0) + w * bw * ew)
        st = nxt
    out = {}
    z = tuple([0] * d)
    for s in shifts:
        val = st.get((z, s), 0)
        for c in s:
            val = red(val * factorial(c))
        out[s] = val
    return out


def _emit(B, cap, d, wleft, inv):
    """(load, weight, B_after): the new vertex carries c_j new j-bundles (sum j c_j <= min(d, wleft), B_j + c_j <= cap_j),
    weight 1/prod c_j!."""
    from math import factorial
    out = []

    def rec(j, load, cs, Bl):
        if j == d:
            wt = 1
            for c in cs:
                if c > 1:
                    wt = wt * inv(factorial(c))
            out.append((load, wt, tuple(Bl))); return
        size = j + 1; c = 0
        while B[j] + c <= cap[j] and load + c * size <= min(d, wleft):
            Bl2 = list(Bl); Bl2[j] += c
            rec(j + 1, load + c * size, cs + [c], Bl2)
            c += 1
    rec(0, 0, [], list(B))
    return out
