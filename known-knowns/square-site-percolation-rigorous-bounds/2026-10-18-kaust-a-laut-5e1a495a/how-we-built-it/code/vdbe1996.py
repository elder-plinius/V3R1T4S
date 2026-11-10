"""Exact reproduction of van den Berg and Ermakov (1996), Random Structures Algorithms 8, 199-212: p_c^site(Z^2) > 0.556.

Written from the paper's definitions (Sections 3-4), exact rational arithmetic only (fractions.Fraction).

Notation: eps(v) = (upper, lower) states of (v,1) and (v,0) in L; P(open) = p each, independent.
eps-adjacency of neighbours v, w of S (min = smaller coordinate sum): upper-upper, lower-lower, or
upper(min)-lower(max) (the paper's ((1,*),(1,*)), ((*,1),(*,1)), ((1,*),(*,1)) with top entry = upper).

Part A (brute force, Proposition 4.2 as stated): for configurations I and II of Fig. 2 and each of the 48 events
E in M, the exact conditional law of (eta(a1), eta(a2), eta(a3)) given E, checked for stochastic domination of
pi_{1-p} on every increasing event of {0,1}^3; also min_E P(eps(c) = (1,*) | E) against Lemma 4.5's r0(p).
Part B (the paper's route): mu_hat of (10), the p. 210 table at p = 0.444, and the largest root.

usage: python vdbe1996.py
"""
from fractions import Fraction as F
from itertools import product

STATES = [(1, 0), (0, 1), (0, 0), (1, 1)]  # (upper, lower)


def w(s, p):
    q = 1 - p
    return (p if s[0] else q) * (p if s[1] else q)


def adj(sv, sw, v, w_):
    """eps-adjacency of neighbouring sites v, w (coordinates) with states sv, sw."""
    if sum(v) < sum(w_):
        smin, smax = sv, sw
    else:
        smin, smax = sw, sv
    return (smin[0] and smax[0]) or (smin[1] and smax[1]) or (smin[0] and smax[1])


# Fig. 2 coordinates (x right, y up); b2 at the origin, c to its left.
CONF = {
    "I": dict(d=(-2, 0), c=(-1, 0), b1=(-1, 1), b3=(-1, -1), b2=(0, 0), a1=(0, 1), a2=(1, 0), a3=(0, -1)),
    "II": dict(d=(-1, 1), c=(-1, 0), b1=(-2, 0), b3=(-1, -1), b2=(0, 0), a1=(0, 1), a2=(1, 0), a3=(0, -1)),
}
# Every site appears once; the children a_i of b2 and brothers b_i of c are distinct sites (checked below).

UP = []  # all increasing events of {0,1}^3 other than empty and full
pts = list(product((0, 1), repeat=3))
for mask in range(1, 2 ** 8 - 1):
    A = {pts[i] for i in range(8) if mask >> i & 1}
    if all(tuple(max(a, b) for a, b in zip(x, y)) in A for x in A for y in pts if all(yy >= xx for xx, yy in zip(x, y))):
        UP.append(frozenset(A))


def pi(A, lam):
    return sum((lam if x[0] else 1 - lam) * (lam if x[1] else 1 - lam) * (lam if x[2] else 1 - lam) for x in A)


def events():
    """The 48 events of M: (E_d, E_b1, E_b3); E_d is eps(d) in {(1,0),(0,1),(1,1)}; E_b is ('0',) or ('1', state)."""
    Eb = [("0",)] + [("1", s) for s in [(1, 0), (0, 1), (1, 1)]]
    return [(sd, e1, e3) for sd in [(1, 0), (0, 1), (1, 1)] for e1 in Eb for e3 in Eb]


def cond_law(conf, E, p):
    """P((eta(a1), eta(a2), eta(a3)) = x | E) for all x, and P(eps(c) = (1,*) | E), exactly."""
    C = CONF[conf]
    sd, e1, e3 = E
    law = {x: F(0) for x in pts}
    tot = F(0)
    c_up = F(0)
    for sc, sb1, sb2, sb3 in product(STATES, repeat=4):
        if not adj(sb2, sc, C["b2"], C["c"]) or not adj(sc, sd, C["c"], C["d"]):
            continue
        ok = True
        for e, sb, name in ((e1, sb1, "b1"), (e3, sb3, "b3")):
            a = adj(sb, sc, C[name], C["c"])
            if e[0] == "0":
                ok &= not a
            else:
                ok &= bool(a) and sb == e[1]
        if not ok:
            continue
        wt = w(sd, p) * w(sc, p) * w(sb1, p) * w(sb2, p) * w(sb3, p)
        tot += wt
        if sc[0]:
            c_up += wt
        # children: independent given eps(b2)
        pa = []
        for name in ("a1", "a2", "a3"):
            pa.append(sum(w(sa, p) for sa in STATES if adj(sa, sb2, C[name], C["b2"])))
        for x in pts:
            pr = wt
            for xi, pi_ in zip(x, pa):
                pr *= pi_ if xi else 1 - pi_
            law[x] += pr
    # P(E) includes the weight of eps(d) only as a constant factor; it cancels.
    return {x: law[x] / tot for x in pts}, c_up / tot


def dominates(law, lam):
    worst = None
    for A in UP:
        m = sum(law[x] for x in A) - pi(A, lam)
        if worst is None or m < worst[0]:
            worst = (m, A)
    return worst


def r0(p):
    q = 1 - p
    return (1 - q * q) / (2 - q * q)


def mu_hat(p):
    q = 1 - p
    r = r0(p)
    c1 = r * p / (1 + q) + (1 - r) * (1 - q * (2 + q) / (1 + q))
    c2 = q / (1 + q)
    c3 = r * q / (1 + q) + (1 - r) * q
    law = {}
    for x in pts:
        v = F(0)
        for c, ps in ((c1, (1 - q * q,) * 3), (c2, (1 - q * q, 1 - q * q, p)), (c3, (p, p, 1 - q * q))):
            t = c
            for xi, pp in zip(x, ps):
                t *= pp if xi else 1 - pp
            v += t
        law[x] = v
    return law


def bisect(fn, lo, hi, iters=60):
    """fn(lo) false (fails), fn(hi) true (holds); returns the threshold bracket."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if fn(mid):
            hi = mid
        else:
            lo = mid
    return lo, hi


def main():
    p0 = F(444, 1000)
    print("increasing events of {0,1}^3 (non-trivial):", len(UP))
    # sanity: sites distinct
    for k, C in CONF.items():
        assert len(set(C.values())) == 8, k
    # ---- Part A
    print("== Part A: brute force over the 2 x 48 local events (Proposition 4.2)")
    allok = True
    minr = {}
    worst_overall = None
    for conf in ("I", "II"):
        mr = None
        for E in events():
            law, cu = cond_law(conf, E, p0)
            assert sum(law.values()) == 1
            m, A = dominates(law, 1 - p0)
            allok &= m > 0
            if worst_overall is None or m < worst_overall[0]:
                worst_overall = (m, conf, E, A)
            mr = cu if mr is None else min(mr, cu)
        minr[conf] = mr
        print("  conf %s: min_E P(eps(c)=(1,*) | E) = %s ~ %.6f" % (conf, mr, float(mr)))
    print("  r0(0.444) = %s ~ %.6f (Lemma 4.5: equals the conf I minimum; conf II larger)" % (r0(p0), float(r0(p0))))
    print("  all %d inequalities hold at p = 0.444: %s; smallest margin %.3e (conf %s, E = %s)"
          % (2 * 48 * len(UP), allok, float(worst_overall[0]), worst_overall[1], worst_overall[2]))

    def holds_all(p):
        return all(dominates(cond_law(conf, E, p)[0], 1 - p)[0] > 0 for conf in ("I", "II") for E in events())

    lo, hi = bisect(holds_all, F(40, 100), F(444, 1000), iters=40)
    print("  per-event route: domination holds for p >= %.10f; bound 1 - p = %.10f" % (float(hi), 1 - float(hi)))
    # ---- Part B
    print("== Part B: mu_hat of (10), table p. 210 at p = 0.444")
    names = {
        "A1": {x for x in pts if x[0]}, "A3": {x for x in pts if x[2]},
        "A1nA2": {x for x in pts if x[0] and x[1]}, "A1nA3": {x for x in pts if x[0] and x[2]},
        "A1nA2nA3": {x for x in pts if all(x)}, "A1uA2": {x for x in pts if x[0] or x[1]},
        "A1uA3": {x for x in pts if x[0] or x[2]}, "A1u(A2nA3)": {x for x in pts if x[0] or (x[1] and x[2])},
        "(A1nA2)uA3": {x for x in pts if (x[0] and x[1]) or x[2]},
        "(A1nA2)u(A1nA3)": {x for x in pts if x[0] and (x[1] or x[2])},
        "(A1nA3)u(A2nA3)": {x for x in pts if x[2] and (x[0] or x[1])},
        "A1uA2uA3": {x for x in pts if any(x)},
        "maj": {x for x in pts if sum(x) >= 2},
    }
    paper = [0.573647, 0.602653, 0.344268, 0.335370, 0.195740, 0.803026, 0.840930, 0.713277, 0.751181, 0.483898,
             0.475001, 0.930678, 0.623529]
    paper_pi = [0.556000, 0.556000, 0.309136, 0.309136, 0.171880, 0.802864, 0.802864, 0.693256, 0.693256, 0.446392,
                0.446392, 0.912472, 0.583649]
    mh = mu_hat(p0)
    assert sum(mh.values()) == 1
    bad = 0
    for (nm, A), pv, ppi in zip(names.items(), paper, paper_pi):
        a, b = float(sum(mh[x] for x in A)), float(pi(A, 1 - p0))
        same = abs(a - pv) < 6e-7 and abs(b - ppi) < 6e-7
        bad += not same
        print("  %-17s mu_hat %.6f (paper %.6f)  pi %.6f (paper %.6f)  %s" % (nm, a, pv, b, ppi, "ok" if same else "DIFF"))
    print("  table rows reproduced: %d of 13" % (13 - bad))
    m, A = dominates(mh, 1 - p0)
    print("  mu_hat dominates pi_0.556 on all %d increasing events at p = 0.444: %s (min margin %.6e)"
          % (len(UP), m > 0, float(m)))

    def holds_mu(p):
        return dominates(mu_hat(p), 1 - p)[0] > 0

    lo, hi = bisect(holds_mu, F(40, 100), F(444, 1000))
    print("  mu_hat route: holds for p >= %.12f, so p_c > 1 - p = %.12f" % (float(hi), 1 - float(hi)))
    print("CERTIFIED (exact rational check at p = 444/1000): p_c^site(Z^2) >= 0.556:", allok and m > 0)


if __name__ == "__main__":
    main()
