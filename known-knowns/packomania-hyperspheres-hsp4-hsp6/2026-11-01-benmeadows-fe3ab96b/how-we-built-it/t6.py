import numpy as np, sys
from core import *
T = table(); rng = np.random.default_rng(7)
for N in [20, 40, 60, 100]:
    rt = T[N]; best = 0
    for s in range(12):
        x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
        x *= rng.random(N)[:, None] ** 0.25 * (1 - rt)
        y, r = relax(x, rt, k0=0.3, kfac=1.5); best = max(best, r)
    print(N, rt, best - rt, flush=True)
