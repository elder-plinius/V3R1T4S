import numpy as np, time, sys
from core import *
T = table(); N = int(sys.argv[1]); rng = np.random.default_rng(int(sys.argv[3])); rt = T[N]
k0 = float(sys.argv[4]); dl = float(sys.argv[5])
x = rng.normal(size=(N, 4)); x /= np.linalg.norm(x, axis=1)[:, None]
x *= rng.random(N)[:, None] ** 0.25 * (1 - rt)
bx, br = relax(x, rt, k0=0.3, kfac=1.5)
t0 = time.time(); it = 0
while time.time() - t0 < float(sys.argv[2]):
    it += 1
    y = bx + rng.uniform(-dl, dl, size=bx.shape) * br
    y, r = relax(y, br, k0=k0, kfac=10)
    if r > br + 1e-12:
        br, bx = r, y
        print(it, round(time.time() - t0), br - rt, flush=True)
print('end', it, br - rt)
