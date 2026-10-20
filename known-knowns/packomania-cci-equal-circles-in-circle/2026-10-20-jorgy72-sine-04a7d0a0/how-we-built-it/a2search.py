#!/usr/bin/env python3
"""A2 parameter search: F(theta,ox,oy,s) = min(s/2, 1-max|p|) over the 3949
smallest-|p| hex lattice points. O(N) per eval -> dense search. Then gentle
settle of the winner."""
import numpy as np, time, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import R_TABLE, feasible_r, save, RUN
from jam import jam
from gen import hex_truncation

N = 3949
rT = R_TABLE
out = open(RUN + '/attempts/ring-graft/output/a2search.log', 'w')


def F_of(theta, ox, oy, s):
    P = hex_truncation(theta, ox, oy, 1.05, s)  # generous bound
    if len(P) < N:
        return -1, None
    rad = np.linalg.norm(P, axis=1)
    idx = np.argsort(rad)[:N]
    P = P[idx]
    return min(s / 2.0, 1.0 - rad[idx].max()), P


t = time.time()
rng = np.random.default_rng(7)
best = (-1, None, None)
evals = 0
for it in range(12000):
    theta = rng.random() * 30.0
    s = 2 * rT * (0.985 + rng.random() * 0.02)
    ox = rng.random() * s
    oy = rng.random() * s
    f, _ = F_of(theta, ox, oy, s)
    evals += 1
    if f > best[0]:
        best = (f, (theta, ox, oy, s), None)
        out.write('it %d NEW BEST F=%.15f margin=%+.3e th=%.3f s=%.8f ox=%.6f oy=%.6f\n'
                  % (it, f, f - rT, theta, s, ox, oy))
        out.flush()
out.write('coarse: %d evals best F=%.15f margin=%+.3e t=%.1fs\n'
          % (evals, best[0], best[0] - rT, time.time() - t))
out.flush()

# refine around best
bt, bo, bs_ = best[1][0], (best[1][1], best[1][2]), best[1][3]
t = time.time()
for it in range(8000):
    theta = bt + rng.normal(0, 1.5)
    s = bs_ * (1 + rng.normal(0, 0.0012))
    ox = bo[0] + rng.normal(0, bs_ * 0.06)
    oy = bo[1] + rng.normal(0, bs_ * 0.06)
    f, _ = F_of(theta, ox, oy, s)
    evals += 1
    if f > best[0]:
        best = (f, (theta, ox, oy, s), None)
        out.write('refine %d NEW BEST F=%.15f margin=%+.3e th=%.3f s=%.8f ox=%.6f oy=%.6f\n'
                  % (it, f, f - rT, theta, s, ox, oy))
        out.flush()
out.write('refine done: %d evals best F=%.15f margin=%+.3e t=%.1fs\n'
          % (evals, best[0], best[0] - rT, time.time() - t))
out.flush()

# rebuild winner, verify with full O(N^2) feasible_r, gentle settle
f, params, _ = best
theta, ox, oy, s = params
_, Pwin = F_of(theta, ox, oy, s)
fr = feasible_r(Pwin)
out.write('winner full feasible_r=%.15f margin=%+.3e (F_est %.15f)\n'
          % (fr, fr - rT, f))
save(Pwin, RUN + '/attempts/ring-graft/output/a2raw_best.txt')
# gentle settle: jam just below current fr, then try nudging up
Q, E = jam(Pwin, fr * 0.99999, outer=6, maxiter=300)
fr2 = feasible_r(Q)
out.write('gentle settle: E=%.3e fr=%.15f margin=%+.3e\n' % (E, fr2, fr2 - rT))
save(Q, RUN + '/attempts/ring-graft/output/a2_best.txt')
out.close()
print(open(RUN + '/attempts/ring-graft/output/a2search.log').read())
