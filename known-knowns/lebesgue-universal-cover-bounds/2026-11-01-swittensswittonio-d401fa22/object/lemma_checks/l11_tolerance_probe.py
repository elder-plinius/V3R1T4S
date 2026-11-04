# L11 remark: is "cap D(V_j, rho+theta) lies within theta of cap D(V_j, rho)" true?  (paper Sec 5.4 treats retained points as within eps0~theta of C_n)
# Exact computation of the Hausdorff excess  max_{p in C(rho+th)} dist(p, C(rho))  for the B3/B5 corner sets.
import numpy as np
from common import *
from scipy.optimize import minimize
def boundary(V, r, nang=20000):
    base = V.mean(0); ang = np.linspace(0, 2*np.pi, nang, endpoint=False); U = np.stack([np.cos(ang), np.sin(ang)], 1)
    s = np.full(nang, np.inf)
    for v in V:
        b = U@(base-v); c = np.sum((base-v)**2)-r**2; s = np.minimum(s, -b+np.sqrt(np.maximum(b*b-c, 0)))
    return base + s[:, None]*U
for n in (3, 5):
    V = corners(n)
    for delta in (0.0, 0.1, 0.3, 0.4, 0.42, 0.4226):
        rho = 1-delta
        if rho <= Rn(n): continue
        for th in (1e-12, 1e-9, 1e-6):
            Bo = boundary(V, rho+th); Bi = boundary(V, rho)
            # distance from outer boundary pts to inner convex set: inner set = polygon of fine boundary pts; use distance to inner boundary pts (outer pts lie outside inner set)
            from scipy.spatial import cKDTree
            d, _ = cKDTree(Bi).query(Bo)
            print(f"n={n} delta={delta:.4f} rho-R_n={rho-Rn(n):.3e} theta={th:.0e}: max dist/theta = {d.max()/th:.4f}")
