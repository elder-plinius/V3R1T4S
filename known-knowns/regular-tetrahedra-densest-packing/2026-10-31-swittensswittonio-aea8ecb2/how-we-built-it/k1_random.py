"""K1 sanity (NUMERICAL, not a proof input): random B-wedges (any offsets, 10% caps); surface fraction by Monte Carlo (400000 sphere points each)
versus a(r) with r = dist(c, W) (the smallest radius with W meeting B_r).  Claim: fraction >= a(r) - noise."""
import numpy as np, math
rng = np.random.default_rng(99)
def a(e):
    return (math.atan(math.sqrt((1 - e * e) / 2)) - e / math.sqrt(3) * math.acos(e * math.sqrt(2) / math.sqrt(3 - e * e))) / math.pi
kap = 1 / 3; sin = math.sqrt(8) / 3
P = rng.normal(size=(400000, 3)); P /= np.linalg.norm(P, axis=1)[:, None]
def dist_to_wedge(n1, n2, s1, s2):
    ins = lambda x: n1 @ x <= s1 + 1e-12 and n2 @ x <= s2 + 1e-12
    if ins(np.zeros(3)): return 0.0
    cands = []
    for n, s in ((n1, s1), (n2, s2)):
        x = n * s                                   # projection of 0 onto the plane n.x = s
        if ins(x): cands.append(np.linalg.norm(x))
    # edge line
    A = np.array([n1, n2]); sol = np.linalg.lstsq(A, np.array([s1, s2]), rcond=None)[0]
    cands.append(np.linalg.norm(sol))
    return min(cands)
worst = 9; n = 0
for _ in range(300):
    n2 = rng.normal(size=3); n2 /= np.linalg.norm(n2)
    t = rng.normal(size=3); t -= t.dot(n2) * n2; t /= np.linalg.norm(t)
    n1 = -kap * n2 + sin * t
    s1 = rng.uniform(-0.5, 0.95); s2 = rng.uniform(-0.5, 0.95)
    if rng.random() < 0.1: s2 = 5.0
    r = dist_to_wedge(n1, n2, s1, s2)
    if r >= 0.97: continue
    frac = np.mean((P @ n1 <= s1) & (P @ n2 <= s2))
    n += 1
    worst = min(worst, frac - a(r))
print("random wedges with dist < 0.97: %d ; smallest (MC fraction - a(dist)) = %.5f (MC noise ~ 0.0008)" % (n, worst))
