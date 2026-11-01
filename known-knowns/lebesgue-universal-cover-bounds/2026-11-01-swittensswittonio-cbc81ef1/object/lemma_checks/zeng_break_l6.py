# Numerical break attempts for the Zeng lemma layer (float64, NUMERICAL evidence).
import numpy as np, time
from common import *
from scipy.spatial import ConvexHull
rng = np.random.default_rng(20261101)
def rot(a): c, s = np.cos(a), np.sin(a); return np.array([[c, -s], [s, c]])
S0 = np.diag([1.0, -1.0])
Bd = lambda n, per=3000: boundary_points(n, 0.0, (0, 0), per)   # reference body R_n^0: vertex on the x-axis
DD = disc_points(20000)
t0 = time.time()

print("=== Z-L6c: turn criterion: all det(e_i,e_{i+1})>0 and total turn 2pi  <=>  convex (random polygons) ===")
def turn_data(P):
    E = np.roll(P, -1, 0) - P; E2 = np.roll(E, -1, 0)
    det = E[:, 0]*E2[:, 1] - E[:, 1]*E2[:, 0]; ang = np.arctan2(det, (E*E2).sum(1)); return det, ang
n_pos = 0; bad = 0; idx2 = 0; idx_other = 0
for _ in range(60000):
    m = int(rng.integers(3, 9)); P = rng.normal(size=(m, 2))
    det, ang = turn_data(P)
    if np.all(det > 0):
        n_pos += 1; tot = ang.sum()/(2*np.pi)
        hull = ConvexHull(P); hv = list(hull.vertices); convex = (len(hv) == m and any(hv == [(j+i) % m for i in range(m)] for j in range(m)))   # convex polygon IN THE GIVEN ORDER (ccw)
        k = int(round(tot))
        if k == 1 and not convex: bad += 1
        if k == 1 and convex: pass
        if k != 1 and convex: bad += 1
        if k == 2: idx2 += 1
        if k > 2: idx_other += 1
print(f"random polygons with all turns positive: {n_pos}; of these index 2 (non-convex, e.g. pentagram-like): {idx2}, index>2: {idx_other}; violations of 'index 1 <=> convex vertex-set in order': {bad}")
# pentagram: all dets > 0 but index 2
pent = np.array([[np.cos(4*np.pi*k/5), np.sin(4*np.pi*k/5)] for k in range(5)]); det, ang = turn_data(pent)
print("pentagram: min det =", det.min(), " total turn / 2pi =", ang.sum()/(2*np.pi), " (so 'all turns positive' alone does not give convexity)")
# homotopy statement: dets positive on the displacement-ball product at the centre-polygon margin
print("=== Z-L6d/e: perturbation and mean-value lower bounds for the shoelace ===")
def shoelace(P): return 0.5*np.sum(P[:, 0]*np.roll(P[:, 1], -1) - P[:, 1]*np.roll(P[:, 0], -1))
worst = 9; ident = 0
for _ in range(20000):
    m = int(rng.integers(3, 12)); ang = np.sort(rng.uniform(0, 2*np.pi, m)); R = rng.uniform(.4, .8, m); C = np.stack([R*np.cos(ang), R*np.sin(ang)], 1)
    eps = 10**rng.uniform(-6, -1, m)
    # adversarial-ish d_i: pick the displacement minimising the linear term, plus random
    Dn = np.roll(C, -1, 0) - np.roll(C, 1, 0)
    lin = np.stack([-Dn[:, 1], Dn[:, 0]], 1)                # grad of 1/2 det(d, Dn) wrt d = 1/2 (Dn_y, -Dn_x); minimise: d = -eps * that/|that|
    g = 0.5*np.stack([Dn[:, 1], -Dn[:, 0]], 1); dmin = -eps[:, None]*g/np.linalg.norm(g, axis=1)[:, None]
    ph = rng.uniform(0, 6.3, m); drand = np.stack([np.cos(ph), np.sin(ph)], 1)*(eps*rng.random(m))[:, None]
    for d in (dmin, drand):
        Z = C + d
        lhs = shoelace(Z); rhs = shoelace(C) - 0.5*np.sum(eps*np.linalg.norm(Dn, axis=1)) - 0.5*np.sum(eps*np.roll(eps, -1))
        worst = min(worst, lhs-rhs)
        dd = 0.5*np.sum(d[:, 0]*Dn[:, 1]-d[:, 1]*Dn[:, 0])+0.5*np.sum(d[:, 0]*np.roll(d[:, 1], -1)-d[:, 1]*np.roll(d[:, 0], -1))
        ident = max(ident, abs(lhs-shoelace(C)-dd))
print(f"min over trials of [S(z) - perturbation bound] = {worst:.3e} (>=0 required; ~0 for the adversarial displacement); max |expansion identity residual| = {ident:.2e}")
# mean-value bound on the real core parametrisation
V3 = corners(3); V5 = corners(5)
def core_poly(z, idx):  # polygon: subset of vertices of D(24-gon), R3, R5 by index list
    x3, y3, ps, x5, y5 = z
    pts = np.vstack([disc_points(24), V3+[x3, y3], V5@rot(ps).T+[x5, y5]]); return pts
worst_mv = 9; ntest = 0
for _ in range(300):
    c = np.array([rng.uniform(-.08, .08), rng.uniform(-.08, .08), rng.uniform(0, np.pi/5), rng.uniform(-.08, .08), rng.uniform(-.08, .08)])
    r = 10**rng.uniform(-4, -1.5, 5); r[2] = min(r[2], .1)
    pts = core_poly(c, None); H = ConvexHull(pts).vertices      # template = hull of centre configuration, ccw
    T = H
    def Sz(z): return shoelace(core_poly(z, None)[T])
    Sc = Sz(c)
    # derivative sup by dense sampling of the box (numerical gradient) -- NOT rigorous, tests the inequality only
    Gk = np.zeros(5)
    for _ in range(60):
        z = c + (rng.random(5)*2-1)*r
        for k in range(5):
            h = 1e-7*max(r[k], 1e-3)/1e-3*1e-3; e = np.zeros(5); e[k] = 1e-8
            Gk[k] = max(Gk[k], abs((Sz(z+e)-Sz(z-e))/(2e-8)))
    Gk *= 1.0000001
    for _ in range(40):
        z = c + (rng.random(5)*2-1)*r
        worst_mv = min(worst_mv, Sz(z) - (Sc - np.sum(Gk*r))); ntest += 1
print(f"mean-value bound S(z) >= S(c) - sum G_k r_k on {ntest} random z in 300 random core boxes (G_k sampled sup|dS/dz_k|): min(S(z) - bound) = {worst_mv:.3e} (>=0)")
print("elapsed", time.time()-t0)
