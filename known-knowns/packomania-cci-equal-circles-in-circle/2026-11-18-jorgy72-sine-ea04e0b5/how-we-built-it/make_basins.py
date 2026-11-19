#!/usr/bin/env python3
"""Regenerate the rotation basins for N=4339, standalone.
raw_trunc is copied verbatim from wide_search.py (do NOT import that
module: importing it re-runs the whole search).

NOTE 2026-11-17: at this row orientation CARRIES signal in the raw
evaluator, unlike 4303/4267. The grid best is th=0, s=0.02853229,
ox=0.011413, oy=0, margin -1.576e-05 (top-20 all th~0 or th~30). Rotating
to th=15/25 with the grid-best offsets gives far-off basins
(-5.721e-04 / -8.508e-04); with ox=oy=0 they are worse still
(-1.872e-03). The basins below carry the grid-best offsets, as the 4303
recipe intended (there the grid best itself sat at ox=oy=0). They are
polished anyway: prior nights show far-off candidates can recover
several e-04 under the ratchet (e.g. 2026-11-08: -1.198e-03 -> -1.947e-05).
"""
import numpy as np
import sys
sys.path.insert(0, '.')
from common import save, R_TABLE

N = 4339


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


# rotation basins at th=15 and th=25, grid-best spacing 0.02853229 and
# grid-best offsets ox=0.011413, oy=0
Q, F = raw_trunc(15.0, 0.011413, 0.0, 0.02853229)
print('basin15 F=%.15f margin=%+.3e' % (F, F - R_TABLE))
save(Q, 'fresh-trunc-4339-output/basin15.txt')
Q, F = raw_trunc(25.0, 0.011413, 0.0, 0.02853229)
print('basin25 F=%.15f margin=%+.3e' % (F, F - R_TABLE))
save(Q, 'fresh-trunc-4339-output/basin25.txt')
