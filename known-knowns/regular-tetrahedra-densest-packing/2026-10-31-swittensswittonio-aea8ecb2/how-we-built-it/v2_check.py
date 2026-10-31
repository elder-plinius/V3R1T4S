"""Lemma V2 sanity (NUMERICAL, not a proof input).  Needs python-flint (fullchain) and numpy.
 (a) the slice formula  vol(W)/vol(B) = (1/vol B) int_{-1}^{min(s2,1)} R^2 bracket(clip(y)) dx0   (y = (s1+kappa x0)/(R sin theta))
     against a Monte-Carlo volume of W = {n1.x<=s1, n2.x<=s2} cap B for random wedges;
 (b) for 6000 random wedges with c not interior, vol(W)/vol(B) - alpha <= E_up(e) with e = exact distance of the edge line to c;
     prints the largest ratio (excess)/E_up.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from flint import arb
import fullchain as F
rng = np.random.default_rng(2024)
kap = 1 / 3; sin = math.sqrt(8) / 3; alpha = math.acos(1 / 3) / (2 * math.pi)
gx, gw = np.polynomial.legendre.leggauss(400)
def vol_frac(s1, s2):
    hi = min(s2, 1.0)
    if hi <= -1: return 0.0
    x0 = (gx + 1) / 2 * (hi + 1) - 1
    w = gw * (hi + 1) / 2
    R2 = 1 - x0 ** 2
    y = np.clip((s1 + kap * x0) / (np.sqrt(R2) * sin), -1, 1)
    br = math.pi - np.arccos(y) + y * np.sqrt(1 - y * y)
    return float(np.sum(w * R2 * br)) * 3 / (4 * math.pi)
def random_wedge():
    n2 = rng.normal(size=3); n2 /= np.linalg.norm(n2)
    a = rng.normal(size=3); a -= a.dot(n2) * n2; a /= np.linalg.norm(a)
    n1 = -kap * n2 + sin * a
    return n1, n2
# (a)
P = rng.uniform(-1, 1, size=(6_000_000, 3)); P = P[np.einsum('ij,ij->i', P, P) <= 1]
for _ in range(6):
    n1, n2 = random_wedge()
    s1 = -rng.uniform(0, 0.8); s2 = rng.uniform(-0.3, 0.9)
    mc = np.mean((P @ n1 <= s1) & (P @ n2 <= s2))
    print("MC %.5f   slice formula %.5f   (s1=%.3f s2=%.3f)" % (mc, vol_frac(s1, s2), s1, s2))
# (b)
worst = 0.0; viol = 0; n = 0
for _ in range(6000):
    t = rng.uniform(0, 0.89) ** 1.5; s1 = -t
    s2 = rng.uniform(0, 0.89)
    d2 = (s2 * s2 + t * t - 2 * kap * t * s2) / (1 - kap * kap); e = math.sqrt(d2)
    if e > F.EMAX: continue
    ex = vol_frac(s1, s2) - alpha
    ub = float(F.E_up(arb(e).upper()))
    n += 1
    if ex > ub: viol += 1
    worst = max(worst, ex / ub)
print("random wedges tested: %d, violations of excess <= E_up(e): %d, largest excess/E_up: %.4f" % (n, viol, worst))
