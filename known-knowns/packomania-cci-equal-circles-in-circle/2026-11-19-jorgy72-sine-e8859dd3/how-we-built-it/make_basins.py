#!/usr/bin/env python3
"""Regenerate the rotation basins for N=4345, standalone.
raw_trunc is copied verbatim from wide_search.py (do NOT import that
module: importing it re-runs the whole search).

NOTE 2026-11-19: tonight's grid best is th=11.5, s=0.02851791,
ox=0.011407, oy=0.011407, margin -1.427e-05; top-20 ties at -1.427e-05
span th 11.5-18.5, so orientation carries LITTLE signal in the raw
evaluator here, like 4339 (unlike 4315). Rotating to th=15/25 with the
grid-best spacing and offsets gives far-off basins; they are polished
anyway: prior nights show far-off candidates can recover several e-04
under the ratchet (e.g. 2026-11-08: -1.198e-03 -> -1.947e-05, and
2026-11-18 basin25: -3.570e-04 -> +8.345e-06).
"""
import numpy as np
import sys
sys.path.insert(0, '.')
from common import save, R_TABLE

N = 4345


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


# rotation basins at th=15 and th=25, grid-best spacing 0.02851791 and
# grid-best offsets ox=0.011407, oy=0.011407
Q, F = raw_trunc(15.0, 0.011407, 0.011407, 0.02851791)
print('basin15 F=%.15f margin=%+.3e' % (F, F - R_TABLE))
save(Q, 'fresh-trunc-4345-output/basin15.txt')
Q, F = raw_trunc(25.0, 0.011407, 0.011407, 0.02851791)
print('basin25 F=%.15f margin=%+.3e' % (F, F - R_TABLE))
save(Q, 'fresh-trunc-4345-output/basin25.txt')
