#!/usr/bin/env python3
"""Batch: diverse raw truncations -> smooth-max ratchet polish -> keep best.
Saves every polished config + margin. Kill-fast: drop candidates that are
hopeless after 2 ratchets."""
import numpy as np, time, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import R_TABLE, feasible_r, save, RUN
from polish import smooth_max_polish
from gen import hex_truncation

rT = R_TABLE
N = 3949
out = open(RUN + '/attempts/ring-graft/output/batch.log', 'w')
results = []


def raw_trunc(theta, ox, oy, s):
    Q0 = hex_truncation(theta, ox, oy, 1.05, s)
    if len(Q0) < N:
        return None
    rad = np.linalg.norm(Q0, axis=1)
    return Q0[np.argsort(rad)[:N]]


def polish_ratchet(Q, ratchets=5):
    fr = feasible_r(Q)
    r = fr
    for k in range(ratchets):
        Q, Emax = smooth_max_polish(Q, r, outer=8, maxiter=400, log=None)
        fr2 = feasible_r(Q)
        if fr2 <= r + 1e-13:
            break
        r = fr2
        fr = fr2
    return Q, fr


rng = np.random.default_rng(123)
cands = []
# seed the batch with the known-good it-240 params + jittered copies
cands.append((12.863, 0.001694, 0.007549, 0.02987721))
for _ in range(4):
    cands.append((rng.random() * 30, rng.random() * 0.03, rng.random() * 0.03,
                  0.02987721 * (1 + rng.normal(0, 0.0008))))
# + fully random diverse
for _ in range(8):
    cands.append((rng.random() * 30, rng.random() * 0.03, rng.random() * 0.03,
                  2 * rT * (0.995 + rng.random() * 0.008)))

t0 = time.time()
for ci, (th, ox, oy, s) in enumerate(cands):
    t = time.time()
    Q = raw_trunc(th, ox, oy, s)
    if Q is None:
        out.write('cand %d: too few points, skip\n' % ci)
        continue
    fr0 = feasible_r(Q)
    # quick kill: if raw is worse than -6e-5, polish is unlikely to reach table
    # (best observed gain +2.7e-5). Actually keep it simple: polish all, but
    # only 5 ratchets.
    Qp, frp = polish_ratchet(Q, ratchets=5)
    mg = frp - rT
    out.write('cand %d th=%.2f s=%.8f: raw %+.3e -> polished %+.3e t=%.0fs\n'
              % (ci, th, s, fr0 - rT, mg, time.time() - t))
    out.flush()
    save(Qp, RUN + '/attempts/ring-graft/output/batch_cand%02d.txt' % ci)
    results.append((mg, ci))
    # checkpoint best
    results.sort(key=lambda x: -x[0])
    out.write('  best so far: cand %d %+.3e\n' % (results[0][1], results[0][0]))
    out.flush()

results.sort(key=lambda x: -x[0])
out.write('\nFINAL RANKED:\n')
for mg, ci in results:
    out.write('  %+.3e  cand %d\n' % (mg, ci))
best_ci = results[0][1]
# copy best to batch_best.txt
import shutil
shutil.copy(RUN + '/attempts/ring-graft/output/batch_cand%02d.txt' % best_ci,
            RUN + '/attempts/ring-graft/output/batch_best.txt')
out.write('best: cand %d margin %+.3e total t=%.0fs\n'
          % (best_ci, results[0][0], time.time() - t0))
out.close()
print(open(RUN + '/attempts/ring-graft/output/batch.log').read())
