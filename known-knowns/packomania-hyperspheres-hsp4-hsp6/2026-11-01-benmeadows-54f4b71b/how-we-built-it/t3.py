import numpy as np, time, sys
from core import *
T = table(); N = int(sys.argv[1]); rng = np.random.default_rng(3); rt = T[N]
def sph(n):
    x = rng.normal(size=(n, 4)); return x / np.linalg.norm(x, axis=1)[:, None]
for nout in range(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])):
    rs = []; t = time.time()
    for s in range(3):
        nin = N - nout
        xo = sph(nout) * (1 - rt)
        xi = sph(nin) * rng.random(nin)[:, None] ** 0.25 * (1 - 3 * rt)
        y, r = relax(np.vstack([xo, xi]), rt, k0=1e1, kfac=3)
        rs.append(r - rt)
    print(nout, np.round(rs, 5), round((time.time() - t)/3, 2), flush=True)
