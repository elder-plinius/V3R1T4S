#!/usr/bin/env python3
"""Final squeeze on deep00: analyze binding constraints, aggressive polish
with higher alpha and more ratchets."""
import numpy as np, time, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import load, R_TABLE, feasible_r, save, RUN
from polish import smooth_max_polish
from scipy.spatial import cKDTree

rT = R_TABLE
out = open(RUN + '/attempts/ring-graft/output/squeeze.log', 'w')
P = load(RUN + '/attempts/ring-graft/output/deep00.txt')
fr0 = feasible_r(P)
out.write('start fr=%.15f margin=%+.3e\n' % (fr0, fr0 - rT))

# binding constraint analysis
tree = cKDTree(P)
d, _ = tree.query(P, k=2)
d1 = np.sort(d[:, 1])
out.write('min pair/2 = %.15f (margin %+.3e)\n' % (d1[0] / 2, d1[0] / 2 - rT))
rad = np.linalg.norm(P, axis=1)
wm = 1 - rad
out.write('min wall = %.15f (margin %+.3e)\n' % (wm.min(), wm.min() - rT))
out.write('num pairs within 1e-9 of min: %d\n' % (np.sum(d[:, 1] < d1[0] + 2e-9)))
out.write('num wall within 1e-9 of min: %d\n' % (np.sum(wm < wm.min() + 1e-9)))
out.flush()

# aggressive polish: higher alpha, more outers, more ratchets
import polish as pm
orig = pm.smooth_max_polish

Q = P.copy()
r = fr0
t = time.time()
for k in range(12):
    Q, Emax = smooth_max_polish(Q, r, alpha=1e6, outer=12, maxiter=600, log=None)
    fr2 = feasible_r(Q)
    out.write('sq %d: Emax=%.3e fr=%.15f margin=%+.3e\n'
              % (k, Emax, fr2, fr2 - rT))
    out.flush()
    if fr2 <= r + 5e-14:
        break
    r = fr2
save(Q, RUN + '/attempts/ring-graft/output/squeeze_best.txt')
out.write('squeeze done t=%.0fs\n' % (time.time() - t))
out.close()
print(open(RUN + '/attempts/ring-graft/output/squeeze.log').read())
