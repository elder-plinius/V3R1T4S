import numpy as np, sys, time
from core import *
T = table(); N = int(sys.argv[1]); rt = T[N]
for p0, p1, pf in [(4, 64, 2), (2, 128, 2), (8, 256, 1.5), (12, 48, 2)]:
    rs = []; t = time.time()
    for s in range(4):
        rng = np.random.default_rng(s)
        x, _ = random_feasible(N, rng)
        x = riesz(x, p0, p1, pf); r1 = feasible_np(x)
        y, r2 = relax(x, r1, k0=1e3, kfac=10)
        rs.append((round(r1 - rt, 5), round(r2 - rt, 5)))
    print(p0, p1, pf, rs, round((time.time()-t)/4, 1), flush=True)
