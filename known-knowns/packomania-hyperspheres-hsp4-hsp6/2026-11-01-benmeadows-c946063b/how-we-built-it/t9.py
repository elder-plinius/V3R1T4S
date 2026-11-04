import numpy as np, sys, time
from core import *
T = table(); rng = np.random.default_rng(10); N = int(sys.argv[1]); rt = T[N]
for r0f, k0, kf, rad in [(0.5, 1e2, 10, 1), (0.5, 1e3, 10, 1), (0.2, 1e2, 10, 1), (0.5, 1e2, 10, 0.5), (0.5, 1e1, 10, 1), (0.5,1e2,3,1)]:
    rs = []; t = time.time()
    for s in range(8):
        x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
        x *= rng.random(N)[:, None] ** 0.25 * (1 - rt) * rad
        y, r = relax(x, rt*r0f, k0=k0, kfac=kf); rs.append(r - rt)
    print(r0f, k0, kf, rad, round(max(rs), 5), round(np.median(rs), 5), round((time.time()-t)/8, 2), flush=True)
