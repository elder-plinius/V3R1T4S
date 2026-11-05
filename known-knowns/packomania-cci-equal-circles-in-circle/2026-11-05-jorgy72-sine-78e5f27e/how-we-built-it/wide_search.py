#!/usr/bin/env python3
"""Lens fresh-trunc-4153: systematic hex-truncation search at N=4153.

The 96,525-eval recipe from 2026-10-25/27, in one script: (1) full grid over
orientation (0-30 deg, 0.25 deg steps) x spacing (21 values around 2*r_table)
x lattice-cell offsets (5x5) = 63,525 evals; (2) 3,000 random refinements
around the grid best; (3) 30,000 full-cell random evals (theta uniform
[0,30), spacing ratio uniform [0.995, 1.001], offsets uniform over [0,s)^2).
Raw evaluator is the analytic one from 2026-10-24: feasible radius of a
perfect hex truncation is min(s/2, 1 - max radius of the innermost N points).
rng seed 20261105 (fresh; never used before). Checkpoint: top-20 list flushed
to wide_search.log as it is found; the best of each phase saved.
"""
import numpy as np, time, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import R_TABLE, save

N = 4153
rT = R_TABLE
OUT = './fresh-trunc-4153-output/'
import os as _os
_os.makedirs(OUT, exist_ok=True)
out = open(OUT + 'wide_search.log', 'w')


def raw_trunc(theta, ox, oy, s):
    th = np.radians(theta)
    a1 = s * np.array([np.cos(th), np.sin(th)])
    a2 = s * np.array([np.cos(th + np.pi / 3), np.sin(th + np.pi / 3)])
    m = int(2.4 / s) + 2
    ii, jj = np.meshgrid(np.arange(-m, m + 1), np.arange(-m, m + 1))
    P = ii[..., None] * a1 + jj[..., None] * a2 + np.array([ox, oy])
    P = P.reshape(-1, 2)
    rad = np.linalg.norm(P, axis=1)
    keep = rad <= 1.05
    P, rad = P[keep], rad[keep]
    if len(P) < N:
        return None, -1.0
    idx = np.argsort(rad)[:N]
    Q = P[idx]
    return Q, min(s / 2.0, 1.0 - rad[idx].max())


t0 = time.time()
top = []  # (F, theta, ox, oy, s)


def consider(F, th, ox, oy, s):
    if F <= -1.0:
        return
    top.append((F, th, ox, oy, s))
    top.sort(key=lambda z: -z[0])
    del top[20:]
    if len(top) == 1 or top[0][0] == F:
        out.write('NEW BEST F=%.15f margin=%+.3e th=%.3f s=%.8f ox=%.6f oy=%.6f t=%.0fs\n'
                  % (F, F - rT, th, s, ox, oy, time.time() - t0))
        out.flush()


thetas = np.arange(0.0, 30.01, 0.25)
ss = 2 * rT * np.linspace(0.9985, 1.0005, 21)
offs = [0.0, 0.2, 0.4, 0.6, 0.8]
n_eval = 0
for th in thetas:
    for s in ss:
        for a in offs:
            for b in offs:
                _, F = raw_trunc(float(th), a * s, b * s, float(s))
                consider(F, float(th), a * s, b * s, float(s))
                n_eval += 1
    out.write('grid theta %.2f done, evals=%d, best margin=%+.3e t=%.0fs\n'
              % (th, n_eval, top[0][0] - rT, time.time() - t0))
    out.flush()
out.write('GRID done: evals=%d best F=%.15f margin=%+.3e t=%.0fs\n'
          % (n_eval, top[0][0], top[0][0] - rT, time.time() - t0))
out.flush()
Q, _ = raw_trunc(top[0][1], top[0][2], top[0][3], top[0][4])
save(Q, OUT + 'wide_best.txt')

# random refinement around grid best
rng = np.random.default_rng(20261105)
bt, bo_x, bo_y, bs = top[0][1], top[0][2], top[0][3], top[0][4]
for it in range(3000):
    th = bt + rng.normal(0, 1.0)
    s = bs * (1 + rng.normal(0, 0.001))
    ox, oy = bo_x + rng.normal(0, bs * 0.05), bo_y + rng.normal(0, bs * 0.05)
    _, F = raw_trunc(float(th), float(ox), float(oy), float(s))
    consider(F, float(th), float(ox), float(oy), float(s))
out.write('REFINE done: evals=%d best F=%.15f margin=%+.3e t=%.0fs\n'
          % (n_eval + 3000, top[0][0], top[0][0] - rT, time.time() - t0))
out.flush()
Q, _ = raw_trunc(top[0][1], top[0][2], top[0][3], top[0][4])
save(Q, OUT + 'refine_best.txt')

# full-cell random phase
rand_best = (-1.0, None)
for it in range(30000):
    th = rng.random() * 30.0
    s = 2 * rT * (0.995 + rng.random() * 0.006)
    ox, oy = rng.random() * s, rng.random() * s
    _, F = raw_trunc(float(th), float(ox), float(oy), float(s))
    consider(F, float(th), float(ox), float(oy), float(s))
    if F > rand_best[0]:
        rand_best = (F, (float(th), float(ox), float(oy), float(s)))
    if it % 5000 == 4999:
        out.write('random it %d best margin=%+.3e t=%.0fs\n'
                  % (it, top[0][0] - rT, time.time() - t0))
        out.flush()
out.write('RANDOM done: evals=%d best F=%.15f margin=%+.3e t=%.0fs\n'
          % (n_eval + 33000, top[0][0], top[0][0] - rT, time.time() - t0))
out.write('RANDOM phase best F=%.15f margin=%+.3e spec th=%.4f s=%.8f ox=%.6f oy=%.6f\n'
          % (rand_best[0], rand_best[0] - rT, rand_best[1][0], rand_best[1][3],
             rand_best[1][1], rand_best[1][2]))
Q, _ = raw_trunc(rand_best[1][0], rand_best[1][1], rand_best[1][2], rand_best[1][3])
save(Q, OUT + 'random_best.txt')
out.write('TOP20:\n')
for F, th, ox, oy, s in top:
    out.write('  %+.6e th=%.4f s=%.8f ox=%.6f oy=%.6f\n' % (F - rT, th, s, ox, oy))
out.close()
print('grid+refine+random done, best margin %+.3e' % (top[0][0] - rT))
