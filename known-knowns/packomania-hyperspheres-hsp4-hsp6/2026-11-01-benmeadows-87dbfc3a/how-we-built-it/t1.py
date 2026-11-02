import numpy as np, time, sys
from core import *
T = table(); N = int(sys.argv[1]); rng = np.random.default_rng(1)
for s in range(4):
    t = time.time()
    x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
    x *= rng.random(N)[:, None] ** 0.25 * (1 - T[N])
    y, r = relax(x, T[N] * 0.9)
    print(s, r, T[N], r - T[N], feasible_np(y), round(time.time() - t, 2))
