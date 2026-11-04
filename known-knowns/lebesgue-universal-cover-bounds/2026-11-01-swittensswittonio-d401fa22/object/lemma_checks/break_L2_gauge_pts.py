# L2 gauge reduction, point-set version with fine sampling (inner-hull error ~1e-9 per body).
import numpy as np
from common import *
rng = np.random.default_rng(78)
def rot(a): c, s = np.cos(a), np.sin(a); return np.array([[c, -s], [s, c]])
S = np.diag([1.0, -1.0])
worst = 0; worst_ref = 0
for trial in range(200):
    mots = []
    for i in range(3):
        a = rng.uniform(0, 2*np.pi); e = int(rng.integers(0, 2))
        mots.append((rot(a) @ (S if e else np.eye(2)), rng.uniform(-.4, .4, 2), a, e))
    bodies = [disc_points(20000), boundary_points(3, 0, (0, 0), 3000), boundary_points(5, 0, (0, 0), 3000)]
    A0 = hull_area(np.vstack([b @ m[0].T + m[1] for b, m in zip(bodies, mots)]))
    a2, a3 = mots[1][2], mots[2][2]
    t3 = rot(-a2) @ (mots[1][1]-mots[0][1]); t5 = rot(-a2) @ (mots[2][1]-mots[0][1]); rho = (a3-a2) % (2*np.pi/5)
    A1 = hull_area(np.vstack([bodies[0], boundary_points(3, 0, tuple(t3), 3000), boundary_points(5, rho, tuple(t5), 3000)]))
    worst = max(worst, abs(A0-A1))
    if any(m[3] for m in mots): worst_ref = max(worst_ref, abs(A0-A1))
print("max |area(original, arbitrary motions incl. reflections) - area(reduced placement)| over 200 trials, fine sampling:", worst, "(trials with >=1 reflection:", worst_ref, ")")
