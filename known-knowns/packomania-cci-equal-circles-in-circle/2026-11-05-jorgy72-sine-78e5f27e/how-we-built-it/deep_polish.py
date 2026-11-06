#!/usr/bin/env python3
"""Lens deep-polish: smooth-max ratchet polish of the best raw candidates from
the ring-graft-wide and boundary-variants lenses (same 8-ratchet recipe as
2026-10-20/24: logsumexp bottleneck, L-BFGS-B, polish from raw, never deflate).
Candidate files are passed on the command line; results logged to deep_polish.log.
"""
import numpy as np, sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import R_TABLE, load, save, feasible_r
from polish import smooth_max_polish

OUT = './deep-polish-4153-output/'
import os as _os
_os.makedirs(OUT, exist_ok=True)
out = open(OUT + 'deep_polish.log', 'w')


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


results = []
for ci, path in enumerate(sys.argv[1:]):
    t = time.time()
    Q = load(path)
    fr0 = feasible_r(Q)
    Qp, frp = deep_polish(Q)
    mg = frp - R_TABLE
    out.write('cand %d %s: raw %+.3e -> polished %+.3e t=%.0fs\n'
              % (ci, path, fr0 - R_TABLE, mg, time.time() - t))
    out.flush()
    save(Qp, OUT + 'polished%02d.txt' % ci)
    results.append((mg, ci))
results.sort(key=lambda x: -x[0])
out.write('\nRANKED:\n')
for mg, ci in results:
    out.write('  %+.3e  polished%02d\n' % (mg, ci))
out.write('best margin %+.3e\n' % results[0][0])
out.close()
print('deep polish done, best margin %+.3e' % results[0][0])
