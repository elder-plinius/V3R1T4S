import numpy as np, sys, time
from core import *
T = table(); N = int(sys.argv[1]); rt = T[N]; p0 = float(sys.argv[2]); pf = float(sys.argv[3]); p1 = float(sys.argv[4])
rs = []; t = time.time()
for s in range(10):
    rng = np.random.default_rng(100 + s)
    x, _ = random_feasible(N, rng)
    x = riesz(x, p0, p1, pf); r1 = feasible_np(x)
    y, r2 = relax(x, r1, k0=1e3, kfac=10)
    rs.append(r2 - rt)
print(N, p0, pf, p1, round(max(rs), 6), round(np.median(rs), 6), round((time.time()-t)/10, 1), flush=True)
