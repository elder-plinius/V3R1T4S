import numpy as np, sys, time
from core import *
T = table(); N = int(sys.argv[1]); rt = T[N]
for ns, g in [(2000, 0.3), (10000, 0.3), (10000, 0.05), (40000, 0.05)]:
    rs = []; t = time.time()
    for s in range(3):
        rng = np.random.default_rng(s)
        x, r0 = random_feasible(N, rng)
        x, r, rate = mc(x, r0, ns, g, seed=s)
        y, r2 = relax(x, r, k0=1e4, kfac=10)
        rs.append((round(r - rt, 5), round(r2 - rt, 5)))
    print(ns, g, rs, round((time.time()-t)/3, 1), flush=True)
