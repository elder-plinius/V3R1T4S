#!/usr/bin/env python3
"""Deep polish: diverse raw truncations -> 8-ratchet smooth-max polish.
Saves each result. This is the main win attempt."""
import numpy as np, time, sys, shutil
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import R_TABLE, feasible_r, save, RUN
from polish import smooth_max_polish
from gen import hex_truncation

rT = R_TABLE
N = 3949
out = open(RUN + '/attempts/ring-graft/output/deep.log', 'w')
results = []


def raw_trunc(theta, ox, oy, s):
    Q0 = hex_truncation(theta, ox, oy, 1.05, s)
    if len(Q0) < N:
        return None
    rad = np.linalg.norm(Q0, axis=1)
    return Q0[np.argsort(rad)[:N]]


def deep_polish(Q, ratchets=8):
    fr = feasible_r(Q)
    r = fr
    for k in range(ratchets):
        Q, Emax = smooth_max_polish(Q, r, outer=10, maxiter=500, log=None)
        fr2 = feasible_r(Q)
        if fr2 <= r + 1e-13:
            break
        r = fr2
        fr = fr2
    return Q, fr


rng = np.random.default_rng(999)
cands = [(12.863, 0.001694, 0.007549, 0.02987721)]  # known good
for _ in range(5):
    cands.append((rng.random() * 30, rng.random() * 0.03, rng.random() * 0.03,
                  0.02987721 * (1 + rng.normal(0, 0.0012))))

t0 = time.time()
for ci, (th, ox, oy, s) in enumerate(cands):
    t = time.time()
    Q = raw_trunc(th, ox, oy, s)
    if Q is None:
        continue
    fr0 = feasible_r(Q)
    Qp, frp = deep_polish(Q)
    mg = frp - rT
    out.write('deep %d th=%.2f s=%.8f: raw %+.3e -> polished %+.3e t=%.0fs\n'
              % (ci, th, s, fr0 - rT, mg, time.time() - t))
    out.flush()
    save(Qp, RUN + '/attempts/ring-graft/output/deep%02d.txt' % ci)
    results.append((mg, ci))

results.sort(key=lambda x: -x[0])
out.write('\nRANKED:\n')
for mg, ci in results:
    out.write('  %+.3e  deep%02d\n' % (mg, ci))
shutil.copy(RUN + '/attempts/ring-graft/output/deep%02d.txt' % results[0][1],
            RUN + '/attempts/ring-graft/output/deep_best.txt')
out.write('best margin %+.3e total t=%.0fs\n' % (results[0][0], time.time() - t0))
out.close()
print(open(RUN + '/attempts/ring-graft/output/deep.log').read())
