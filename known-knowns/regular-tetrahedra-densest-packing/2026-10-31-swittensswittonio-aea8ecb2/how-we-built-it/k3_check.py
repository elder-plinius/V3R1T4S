"""K3 construction, randomised sanity test (NUMERICAL, not a proof input; the proof is REDUCTION_FULL.md section 4).
Random objects O = B_1 cap {n1.x<=s1} cap {n2.x<=s2} (n1.n2 = -1/3, any offsets; caps = second offset >= 1) with 0 not in int O, restricted to
the ball G = int B_s (s = 0.5).  Random families of (approximately) pairwise interior-disjoint objects are built from a pool by rejection.
The construction of section 4 is applied literally:
  objects with edge line meeting G (e < s) and caps are kept; every other object becomes the cap B_s cap H_j, H_j the half-space with 0 not in int H_j
  when both planes cut G ('middle' type) or the cut plane when only one does; nested ones are deleted (O' inside cl R^far(O)); then
  (i) members pairwise disjoint, (ii) every original point of G is covered by a member, (iii) member count/type bookkeeping.
Original families are made exactly disjoint (convex-programming test, interior_radius <= 1e-7) after a sample pre-filter; membership of the construction is tested on an independent sample set of 120000 points."""
import numpy as np, math, itertools
rng = np.random.default_rng(777)
kap = 1 / 3; sin = math.sqrt(8) / 3
s = 0.5
def pts(n):
    P = rng.normal(size=(n, 3)); P /= np.linalg.norm(P, axis=1)[:, None]
    return P * (s * rng.uniform(0, 1, size=n) ** (1 / 3))[:, None]
S1 = pts(60000); S2 = pts(120000)
def rand_obj():
    while True:
        n2 = rng.normal(size=3); n2 /= np.linalg.norm(n2)
        a = rng.normal(size=3); a -= a.dot(n2) * n2; a /= np.linalg.norm(a)
        n1 = -kap * n2 + sin * a
        s1 = rng.uniform(-0.9, 0.9) * rng.choice([1, 0.4]); s2 = rng.uniform(-0.9, 0.9) * rng.choice([1, 0.4])
        if rng.random() < 0.1: s2 = 5.0           # cap
        if s1 > 0 and s2 > 0: continue
        return (n1, n2, s1, s2)
from scipy.optimize import minimize
def planes(o):
    n1, n2, s1, s2 = o
    return [(n1, s1)] + ([(n2, s2)] if s2 < 5 else [])
def interior_radius(objs):
    """max t such that a point x has n.x + t <= s for all planes of all objects and |x| + t <= s (G ball): convex program; > 0 iff the objects have a common interior point in G"""
    pl = [p for o in objs for p in planes(o)]
    cons = [{'type': 'ineq', 'fun': (lambda v, n=n, sj=sj: sj - n @ v[:3] - v[3])} for n, sj in pl]
    cons.append({'type': 'ineq', 'fun': lambda v: (s - v[3]) ** 2 - v[:3] @ v[:3]})
    best = -9
    for t0 in (-0.5,):
        r = minimize(lambda v: -v[3], np.array([0, 0, 0, t0]), constraints=cons, method='SLSQP', options={'maxiter': 200, 'ftol': 1e-12})
        best = max(best, r.x[3] if r.success else -9)
    return best
def exactly_disjoint(o, fam):
    return all(interior_radius([o, o2]) <= 1e-7 for o2, _ in fam)
def member(o, P): return (P @ o[0] <= o[2]) & (P @ o[1] <= o[3])
def edge_dist(o):
    n1, n2, s1, s2 = o
    if s2 >= 5: return 9.0
    return math.sqrt((s1 * s1 + s2 * s2 + 2 * kap * s1 * s2) / (1 - kap * kap))
def targeted_mid():
    """object whose two planes both cut G and whose edge line misses G (the case flagged by an earlier reviewer)"""
    while True:
        n2 = rng.normal(size=3); n2 /= np.linalg.norm(n2)
        a = rng.normal(size=3); a -= a.dot(n2) * n2; a /= np.linalg.norm(a)
        n1 = -kap * n2 + sin * a
        s1 = -rng.uniform(0.0, 0.5 * s * 2); s2 = rng.uniform(0.0, s)
        o = (n1, n2, s1, s2)
        if abs(s1) < s and abs(s2) < s and edge_dist(o) >= s: return o
def mixed():
    return targeted_mid() if rng.random() < 0.6 else rand_obj()
viol = 0; fam_n = 0; mids = 0; dels = 0; maxov = 0.0; uncovered = 0
for trial in range(150):
    while True:                                    # rejection-sample a genuinely middle-type o0
        o0 = targeted_mid(); m0 = member(o0, S1)
        H1 = (S1 @ o0[0] <= o0[2]); H2 = (S1 @ o0[1] <= o0[3])
        if m0.sum() >= 100 and (H1 & ~H2).sum() > 100 and (H2 & ~H1).sum() > 100: break
    fam = [(o0, m0)]
    j0 = 0 if o0[2] <= 0 else 1
    fn, fs = (o0[1], o0[3]) if j0 == 0 else (o0[0], o0[2])
    farpts = S1[(S1 @ fn > fs)]
    for _ in range(1500):
        r = rng.random()
        if r < 0.5 and len(farpts) > 20:           # candidates placed inside R^far(o0): nested caps / nested wedges
            y = farpts[rng.integers(len(farpts))]
            if r < 0.15:
                o = (-fn, -fn, -(fn @ y) + rng.uniform(-0.1, 0.1), 5.0)      # a cap {fn.x >= fn.y - eta} beyond a plane through y (second half-space redundant)
            else:
                o2 = rand_obj(); o = (o2[0], o2[1], o2[0] @ y + rng.uniform(-0.12, 0.12), o2[1] @ y + rng.uniform(-0.12, 0.12))
                if o[2] > 0 and o[3] > 0: continue
        else:
            o = mixed()
        m = member(o, S1)
        if m.sum() > 100 and all((m & m2).sum() == 0 for _, m2 in fam) and exactly_disjoint(o, fam):
            fam.append((o, m))
        if len(fam) >= 5: break
    if len(fam) < 2: continue
    fam_n += 1
    # originals' mutual overlap on S2 (noise level)
    mem2 = [member(o, S2) for o, _ in fam]
    ov0 = max([(a & b).mean() for a, b in itertools.combinations(mem2, 2)] + [0])
    # construction
    info = []
    for (o, m), m2 in zip(fam, mem2):
        n1, n2, s1, s2 = o
        e = edge_dist(o)
        if e < s or s2 >= 5:
            info.append(dict(kind='keep', o=o)); continue
        d1 = abs(s1) < s; d2 = abs(s2) < s
        if not d1 and not d2: info.append(dict(kind='drop')); continue
        if d1 != d2:
            j = 0 if d1 else 1
            other = (s2 if d1 else s1)
            if other <= -s: info.append(dict(kind='drop')); continue
            info.append(dict(kind='cap', n=(n1, n2)[j], sj=(s1, s2)[j], o=o)); continue
        # both planes cut G: middle iff O cap G is neither cap
        H1 = (S1 @ n1 <= s1); H2 = (S1 @ n2 <= s2)
        if ((H1 & ~H2).sum() > 0 and (H2 & ~H1).sum() > 0) and m.sum() > 0:
            # middle type unless O cap G equals one of the caps; here O cap G = H1 cap H2 differs from both
            mids += 1
            j = 0 if s1 <= 0 else 1                          # 0 not in int H_j
            n = (n1, n2)[j]; sj = (s1, s2)[j]; far = (n2, s2) if j == 0 else (n1, s1)
            info.append(dict(kind='mid', n=n, sj=sj, far=far, o=o))
        else:
            # outer region: O cap G is a cap
            if (H1 & ~H2).sum() == 0 and m.sum() > 0: info.append(dict(kind='cap', n=n1, sj=s1, o=o))
            elif (H2 & ~H1).sum() == 0 and m.sum() > 0: info.append(dict(kind='cap', n=n2, sj=s2, o=o))
            else: info.append(dict(kind='drop'))
    # delete objects inside cl R^far of a middle type
    def far_region(P, d):
        n, sj = d['n'], d['sj']; fn, fs = d['far']
        return (P @ n <= sj) & ~(P @ fn <= fs)
    keep = []
    for i, d in enumerate(info):
        if d['kind'] == 'drop': continue
        mi = mem2[i]
        deleted = False
        for k, dk in enumerate(info):
            if k != i and dk['kind'] == 'mid':
                if mi.sum() > 0 and (mi & ~far_region(S2, dk)).mean() < 1e-5: deleted = True; break
        if deleted: dels += 1
        else: keep.append(i)
    # membership of the new family
    new = []
    for i in keep:
        d = info[i]
        if d['kind'] == 'keep': new.append(member(d['o'], S2))
        else: new.append((S2 @ d['n'] <= d['sj']))
    ov = max([(a & b).mean() for a, b in itertools.combinations(new, 2)] + [0])
    if ov > ov0 + 3e-5:
        viol += 1; print("OVERLAP in new family", ov, ov0)
    maxov = max(maxov, ov - ov0)
    cov = np.zeros(len(S2), bool)
    for a in new: cov |= a
    orig = np.zeros(len(S2), bool)
    for a in mem2: orig |= a
    if (orig & ~cov).mean() > 1e-4: uncovered += 1; print("UNCOVERED", (orig & ~cov).mean())
print("families tested %d, middle-type wedges encountered %d, nested deletions %d" % (fam_n, mids, dels))
print("violations (new overlap > original overlap + 3e-5): %d ; families with uncovered original volume: %d ; max (new-orig) overlap fraction %.2e" % (viol, uncovered, maxov))
