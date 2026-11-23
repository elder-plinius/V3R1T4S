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

OUT = 'deep-polish-4405-output/'
out = open(OUT + 'deep_polish.log', 'w')


def deep_polish(Q, ratchets=8):
    fr = feasible_r(Q)
    r = fr
    Q_inc = Q.copy()
    for k in range(ratchets):
        Q, Emax = smooth_max_polish(Q, r, outer=10, maxiter=500, log=None)
        fr2 = feasible_r(Q)
        if fr2 < fr - 1e-13:
            # FIX 2026-11-08 (2026-11-07 polished03 lesson): a ratchet
            # can DEGADE Q far below the incumbent (-7.015e-04 ->
            # -1.410323e-02); the old loop broke keeping the degraded
            # state. Revert to the incumbent and stop.
            Q = Q_inc
            fr2 = fr
            break
        if fr2 <= r + 1e-13:
            break
        r = fr2
        fr = fr2
        Q_inc = Q.copy()
    # FIX 2026-11-06 (2026-10-30 prescription, finally applied to
    # deep_polish.py itself): the tracked fr can be stale when the final
    # ratchet degrades Q — the loop breaks keeping the pre-ratchet fr
    # while Q is already the degraded state (read 1.2e-07–2.2e-07
    # optimistic on 2026-11-05). Recompute from the returned Q.
    fr = feasible_r(Q)
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
