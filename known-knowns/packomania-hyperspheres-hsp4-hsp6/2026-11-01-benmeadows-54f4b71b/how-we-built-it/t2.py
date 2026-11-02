import numpy as np, time, sys
from core import *
T = table(); N = int(sys.argv[1]); rng = np.random.default_rng(2)
for (k0, kf) in [(1e0, 10), (1e0, 3), (1e1, 2), (3e-1, 1.5)]:
    rs = []; t = time.time()
    for s in range(4):
        x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
        x *= rng.random(N)[:, None] ** 0.25 * (1 - T[N])
        y, r = relax(x, T[N], k0=k0, kfac=kf)
        rs.append(r - T[N])
    print(k0, kf, np.round(rs, 5), round((time.time() - t)/4, 2))
