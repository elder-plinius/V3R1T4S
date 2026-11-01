import numpy as np, sys, collections
from core import *
T = table(); rng = np.random.default_rng(9); N = int(sys.argv[1]); rt = T[N]
c = collections.Counter()
for s in range(int(sys.argv[2])):
    x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
    x *= rng.random(N)[:, None] ** 0.25 * (1 - rt)
    y, r = relax(x, rt*0.5, k0=float(sys.argv[3]), kfac=float(sys.argv[4]))
    c[round(r - rt, 6)] += 1
print(sorted(c.items(), reverse=True)[:8])
