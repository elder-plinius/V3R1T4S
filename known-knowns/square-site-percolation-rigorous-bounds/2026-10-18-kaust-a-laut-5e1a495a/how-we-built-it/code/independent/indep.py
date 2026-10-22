"""Independent re-implementation (skeptic 1). Written from the paper's definitions, not from window.py.

Differences from window.py on purpose:
  * edges are explicit displacement vectors in Z^2 (E, N, W, S), not min/max orientation labels; eps-adjacency is
    evaluated from coordinates (paper p. 203: min = smaller coordinate sum; patterns upper-upper, lower-lower,
    upper(min)-lower(max));
  * no symmetry reduction (4 directions everywhere);
  * cones are kept EXACT (no outward rounding), pruned by an exact gift-wrapping hull in projective coordinates,
    with a self-check that every discarded generator lies in the hull of the kept ones;
  * increasing events are generated as up-closures of antichains.

usage: python indep.py margins <k_max> <p>        exact worst margins for depths 0..k_max at p
       python indep.py bisect <k> <lo> <hi>       smallest p (to 1e-9) at which the exact depth-k check passes
       python indep.py brute1 <p>                 depth 1 WITHOUT any pruning (float, numpy), all generator tuples
"""
import sys
from fractions import Fraction as F
from itertools import product, combinations

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
ALLS = [(u, l) for u in (0, 1) for l in (0, 1)]  # (upper, lower)
OPENS = [s for s in ALLS if s != (0, 0)]


def neg(d):
    return (-d[0], -d[1])


def eadj(v, sv, w, sw):
    """paper p. 203: v, w neighbours in S; min = smaller coordinate sum."""
    if v[0] + v[1] < w[0] + w[1]:
        mn, mx = sv, sw
    else:
        mn, mx = sw, sv
    return bool((mn[0] and mx[0]) or (mn[1] and mx[1]) or (mn[0] and mx[1]))


def E(d, sp, sc):
    """edge indicator for parent at origin in state sp and child at d in state sc."""
    return 1 if eadj((0, 0), sp, d, sc) else 0


def upsets(n):
    pts = list(product((0, 1), repeat=n))
    leq = lambda x, y: all(a <= b for a, b in zip(x, y))
    res = set()
    # all antichains (n <= 4: 16 points, brute force over subsets is 65536)
    for r in range(0, len(pts) + 1):
        pass
    for mask in range(1 << len(pts)):
        S = [pts[i] for i in range(len(pts)) if mask >> i & 1]
        if any(leq(a, b) and a != b for a in S for b in S):
            continue
        up = frozenset(y for y in pts if any(leq(a, y) for a in S))
        res.add(up)
    res.discard(frozenset())
    res.discard(frozenset(pts))
    return sorted(res, key=lambda s: (len(s), sorted(s)))


UP3 = upsets(3)


def norm(v):
    s = sum(v)
    return tuple(x / s for x in v)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def in_hull(pt, H):
    """exact: is 2D point pt in the convex polygon H (vertices in ccw order, possibly degenerate)?"""
    if len(H) == 1:
        return pt == H[0]
    if len(H) == 2:
        a, b = H
        if cross(a, b, pt) != 0:
            return False
        return min(a[0], b[0]) <= pt[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= pt[1] <= max(a[1], b[1])
    return all(cross(H[i], H[(i + 1) % len(H)], pt) >= 0 for i in range(len(H)))


def prune(vecs):
    """Extreme rays of the cone of nonnegative 3-vectors, exact. Gift wrapping on (v0, v1)/sum."""
    pts = {}
    for v in vecs:
        assert min(v) >= 0
        if sum(v) == 0:
            continue
        nv = norm(v)
        pts[(nv[0], nv[1])] = nv
    P = list(pts)
    if len(P) <= 2:
        return [pts[x] for x in P]
    start = min(P)
    H = [start]
    cur = start
    while True:
        cand = None
        for q in P:
            if q == cur:
                continue
            if cand is None:
                cand = q
                continue
            c = cross(cur, cand, q)
            d2 = lambda a: (a[0] - cur[0]) ** 2 + (a[1] - cur[1]) ** 2
            if c < 0 or (c == 0 and d2(q) > d2(cand)):
                cand = q
        cur = cand
        if cur == start:
            break
        H.append(cur)
        assert len(H) <= len(P)
    # gift wrapping with "c < 0 -> switch" produces clockwise order; make ccw for in_hull
    if len(H) >= 3 and cross(H[0], H[1], H[2]) < 0:
        H = H[::-1]
    # drop collinear middle points
    if len(H) >= 3:
        H2 = [H[i] for i in range(len(H)) if cross(H[i - 1], H[i], H[(i + 1) % len(H)]) != 0]
        H = H2 if len(H2) >= 2 else H
    for x in P:  # self-check: nothing outside
        assert in_hull(x, H), "hull self-check failed"
    return [pts[x] for x in H]


class M:
    def __init__(self, p):
        self.p = p
        q = 1 - p
        self.pi = {s: (p if s[0] else q) * (p if s[1] else q) for s in ALLS}
        self.one = (F(1),) * 3

    def leaf0(self, d):
        return tuple(sum(self.pi[s] * (1 - E(d, g, s)) for s in ALLS) for g in OPENS)

    def child_msg(self, d, slotmsgs):
        """eta = 1 child at direction d, whose own child slots send slotmsgs (3-vectors over the child's OPENS)."""
        out = []
        for g in OPENS:
            t = F(0)
            for i, s in enumerate(OPENS):
                if E(d, g, s):
                    f = self.pi[s]
                    for m in slotmsgs:
                        f *= m[i]
                    t += f
            out.append(t)
        return tuple(out)

    def par_msg(self, d, parmsg, slotmsgs):
        """message into x = y + d from y (x's state g), y's factors: parent-side parmsg, other child slots."""
        out = []
        for g in OPENS:
            t = F(0)
            for i, s in enumerate(OPENS):
                if E(d, s, g):
                    f = self.pi[s] * parmsg[i]
                    for m in slotmsgs:
                        f *= m[i]
                    t += f
            out.append(t)
        return tuple(out)

    def D0(self, d):
        return prune([self.one, self.leaf0(d)] + [tuple(F(E(d, g, s)) for g in OPENS) for s in OPENS])

    def U0(self, d):
        return prune([tuple(F(E(d, s, g)) for g in OPENS) for s in OPENS])

    def Dk(self, Dp):
        out = {}
        for d in DIRS:
            gens = [self.one, self.leaf0(d)]
            slots = [e for e in DIRS if e != neg(d)]
            for ms in product(*[Dp[e] for e in slots]):
                gens.append(self.child_msg(d, ms))
            out[d] = prune(gens)
        return out

    def Uk(self, Up, Dp):
        out = {}
        for d in DIRS:
            gens = []
            # y is the root: other slots all directions != d
            for ms in product(*[Dp[e] for e in DIRS if e != d]):
                gens.append(self.par_msg(d, self.one, ms))
            for e in DIRS:  # y = z + e, z is y's parent
                if e == neg(d):
                    continue
                slots = [f for f in DIRS if f != d and f != neg(e)]
                for mp in Up[e]:
                    for ms in product(*[Dp[f] for f in slots]):
                        gens.append(self.par_msg(d, mp, ms))
            out[d] = prune(gens)
        return out

    def check(self, U, D, detail=False):
        lam = 1 - self.p
        worst = None
        for d in DIRS:  # b2 = c + d
            kids = [e for e in DIRS if e != neg(d)]
            pk = {b: [sum(self.pi[a] for a in ALLS if E(e, b, a)) for e in kids] for b in OPENS}
            coef = []
            for B in UP3:
                piB = F(0)
                for x in B:
                    t = F(1)
                    for xi in x:
                        t *= lam if xi else 1 - lam
                    piB += t
                row = []
                for b in OPENS:
                    nb = F(0)
                    for x in B:
                        t = F(1)
                        for xi, pp in zip(x, pk[b]):
                            t *= pp if xi else 1 - pp
                        nb += t
                    row.append(nb - piB)
                coef.append(row)
            cases = [("root", self.one, [e for e in DIRS if e != d], None)]
            for e in DIRS:
                if e != neg(d):
                    cases.append(("par" + str(e), None, [f for f in DIRS if f != d and f != neg(e)], e))
            for name, fixed, slots, e in cases:
                pars = [fixed] if fixed is not None else U[e]
                for mp in pars:
                    for ms in product(*[D[f] for f in slots]):
                        mu = []
                        for i, g in enumerate(OPENS):
                            t = self.pi[g] * mp[i]
                            for m in ms:
                                t *= m[i]
                            mu.append(t)
                        w = [self.pi[b] * sum(mu[i] for i, g in enumerate(OPENS) if E(d, g, b)) for b in OPENS]
                        sw = sum(w)
                        assert sw > 0
                        for row in coef:
                            m = sum(wi * ci for wi, ci in zip(w, row)) / sw
                            if worst is None or m < worst[0]:
                                worst = (m, d, name, mp, ms)
        return worst


def run_levels(p, kmax):
    m = M(p)
    D = {d: m.D0(d) for d in DIRS}
    U = {d: m.U0(d) for d in DIRS}
    yield 0, m, U, D
    for k in range(1, kmax + 1):
        U, D = m.Uk(U, D), m.Dk(D)
        yield k, m, U, D


def margin(p, k):
    for kk, m, U, D in run_levels(p, k):
        if kk == k:
            return m.check(U, D), {d: len(U[d]) for d in DIRS}, {d: len(D[d]) for d in DIRS}


def brute1(p):
    """Depth 1 with NO hull pruning at all: every generator tuple, float numpy."""
    import numpy as np
    m = M(p)
    D0 = {d: [m.one, m.leaf0(d)] + [tuple(F(E(d, g, s)) for g in OPENS) for s in OPENS] for d in DIRS}
    U0 = {d: [tuple(F(E(d, s, g)) for g in OPENS) for s in OPENS] for d in DIRS}
    D1 = {}
    U1 = {}
    for d in DIRS:
        gens = [m.one, m.leaf0(d)]
        for ms in product(*[D0[e] for e in DIRS if e != neg(d)]):
            gens.append(m.child_msg(d, ms))
        D1[d] = np.array([[float(x) for x in g] for g in gens])
        gens = []
        for ms in product(*[D0[e] for e in DIRS if e != d]):
            gens.append(m.par_msg(d, m.one, ms))
        for e in DIRS:
            if e == neg(d):
                continue
            for mp in U0[e]:
                for ms in product(*[D0[f] for f in DIRS if f != d and f != neg(e)]):
                    gens.append(m.par_msg(d, mp, ms))
        U1[d] = np.array([[float(x) for x in g] for g in gens])
    pi = np.array([float(m.pi[g]) for g in OPENS])
    lam = 1 - float(p)
    worst = np.inf
    ntup = 0
    for d in DIRS:
        kids = [e for e in DIRS if e != neg(d)]
        pk = {b: [float(sum(m.pi[a] for a in ALLS if E(e, b, a))) for e in kids] for b in OPENS}
        C = np.zeros((len(UP3), 3))
        for j, B in enumerate(UP3):
            piB = sum(np.prod([lam if xi else 1 - lam for xi in x]) for x in B)
            for i, b in enumerate(OPENS):
                C[j, i] = sum(np.prod([pp if xi else 1 - pp for xi, pp in zip(x, pk[b])]) for x in B) - piB
        Ad = np.array([[E(d, g, b) for b in OPENS] for g in OPENS], dtype=float)  # [g, b]
        cases = [(np.ones((1, 3)), [D1[e] for e in DIRS if e != d])]
        for e in DIRS:
            if e != neg(d):
                cases.append((U1[e], [D1[f] for f in DIRS if f != d and f != neg(e)]))
        for MP, slots in cases:
            # mu[n, g] over all tuples, built by broadcasting
            mu = pi[None, :] * MP
            for S in slots:
                mu = (mu[:, None, :] * S[None, :, :]).reshape(-1, 3)
            ntup += mu.shape[0]
            w = (mu @ Ad) * pi[None, :]
            sw = w.sum(1, keepdims=True)
            marg = (w @ C.T) / sw
            worst = min(worst, marg.min())
    return worst, ntup


def main():
    cmd = sys.argv[1]
    if cmd == "margins":
        k, p = int(sys.argv[2]), F(sys.argv[3])
        print("increasing events of {0,1}^3:", len(UP3))
        for kk, m, U, D in run_levels(p, k):
            w = m.check(U, D)
            print("depth %d at p=%s: exact worst margin %.9e  (b2 dir %s, case %s) |U| %s |D| %s"
                  % (kk, p, float(w[0]), w[1], w[2], [len(U[d]) for d in DIRS], [len(D[d]) for d in DIRS]),
                  flush=True)
    elif cmd == "bisect":
        k, lo, hi = int(sys.argv[2]), F(sys.argv[3]), F(sys.argv[4])
        N = 10 ** 9
        a, b = int(lo * N), int(hi * N)
        assert margin(F(b, N), k)[0][0] > 0
        assert margin(F(a, N), k)[0][0] <= 0
        while b - a > 1:
            c = (a + b) // 2
            if margin(F(c, N), k)[0][0] > 0:
                b = c
            else:
                a = c
        print("depth %d: exact check passes at p = %d/1e9, fails at %d/1e9; bound 1-p = %.9f"
              % (k, b, a, 1 - b / N))
    elif cmd == "brute1":
        p = F(sys.argv[2])
        w, n = brute1(p)
        print("depth 1 unpruned (float): %d generator tuples, worst margin %.9e" % (n, w))


if __name__ == "__main__":
    main()
