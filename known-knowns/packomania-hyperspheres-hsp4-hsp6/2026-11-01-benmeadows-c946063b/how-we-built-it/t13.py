import numpy as np, sys, time
from core import *
T = table(); N = int(sys.argv[1]); rt = T[N]; mode = sys.argv[2]; dl = float(sys.argv[3]); seed = int(sys.argv[4])
rng = np.random.default_rng(seed)
best = (-1, None)
for s in range(6):
    x, _ = random_feasible(N, rng); x = riesz(x, 4, 64, 2); y, r = relax(x, feasible_np(x), k0=1e3)
    if r > best[0]: best = (r, y)
br, bx = best; print('start', br - rt, flush=True); t0 = time.time(); it = 0
while time.time() - t0 < 150:
    it += 1
    y = bx + rng.normal(size=bx.shape) * dl * br
    nr = np.linalg.norm(y, axis=1); y[nr > 0.99] *= (0.99 / nr[nr > 0.99])[:, None]
    if mode == 'r': y = riesz(y, 16, 64, 2)
    y, r = relax(y, feasible_np(y) if mode == 'r' else br, k0=1e3 if mode == 'r' else 1e2)
    if r > br + 1e-12: br, bx = r, y; print(it, round(time.time()-t0), br - rt, flush=True)
print('end', it, br - rt)
