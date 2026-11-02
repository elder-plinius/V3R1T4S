import numpy as np, sys
from core import *
T = table(); rng = np.random.default_rng(8); N = 20; rt = T[N]
x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
x *= rng.random(N)[:, None] ** 0.25 * (1 - rt)
y, r = relax(x, rt, k0=0.3, kfac=1.5); print(r - rt)
for mi in [4000, 40000, 400000]:
    y2, r2 = relax(y, r, k0=1e3, kfac=10, maxit=mi); print(mi, r2 - rt)
y3, r3 = relax(y, r, k0=1e3, kfac=2, maxit=40000); print('kf2', r3 - rt)
