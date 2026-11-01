# NUMERICAL (not a proof): dense-polygon estimate of A(z)=area conv(D u R3(z) u R5(z)); inscribed polygon => estimate <= true area.
import numpy as np, math, sys
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
rng = np.random.default_rng(20261031)
S = 1500
def disk(): t = np.linspace(0, 2 * math.pi, S, endpoint=False); return 0.5 * np.c_[np.cos(t), np.sin(t)]
def reul(n):
    R = 1 / (2 * math.sin((n // 2) * math.pi / n)); cs = [(R * math.cos(2 * math.pi * j / n), R * math.sin(2 * math.pi * j / n)) for j in range(n)]
    pts = []
    for c in cs:
        t = np.linspace(0, 2 * math.pi, 6 * S, endpoint=False); P = np.c_[c[0] + np.cos(t), c[1] + np.sin(t)]
        ok = np.all([((P[:, 0] - d[0]) ** 2 + (P[:, 1] - d[1]) ** 2) <= 1 + 1e-13 for d in cs], axis=0); pts.append(P[ok])
    return np.vstack(pts)
D, R3, R5 = disk(), reul(3), reul(5)
def A(z):
    x3, y3, psi, x5, y5 = z; c, s = math.cos(psi), math.sin(psi)
    P5 = R5 @ np.array([[c, s], [-s, c]]) + [x5, y5]
    return ConvexHull(np.vstack([D, R3 + [x3, y3], P5])).volume
lo = np.array([-.08, -.08, 0, -.08, -.08]); hi = np.array([.08, .08, math.pi / 5, .08, .08])
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
Z = lo + (hi - lo) * rng.random((N, 5)); vals = np.array([A(z) for z in Z])
print('random core samples', N, 'min A =', vals.min(), ' (> 0.834:', vals.min() > 0.834, ')')
best = Z[np.argsort(vals)[:6]]; mins = []
for z0 in best:
    r = minimize(lambda z: A(np.clip(z, lo, hi)), z0, method='Nelder-Mead', options={'xatol': 1e-9, 'fatol': 1e-13, 'maxiter': 4000})
    mins.append((r.fun, np.clip(r.x, lo, hi).tolist()))
mins.sort(key=lambda t: t[0])
print('Nelder-Mead local minima (best 3):'); [print('  A=%.9f at z=%s' % (m[0], np.round(m[1], 5).tolist())) for m in mins[:3]]
print('=> numeric minimum of A over the core box ~ %.7f ; certified threshold 0.834 ; gap %.2e' % (mins[0][0], mins[0][0] - 0.834))
