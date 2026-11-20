#!/usr/bin/env python3
"""Regenerate the rotation basins for N=4357, standalone.
raw_trunc is copied verbatim from wide_search.py (do NOT import that
module: importing it re-runs the whole search).

NOTE 2026-11-20: spacing/offsets below are PLACEHOLDERS carried from
2026-11-19 (N=4345). MUST be replaced with tonight's own grid best
before running (the 2026-11-19 lesson).
"""
import numpy as np
import sys
sys.path.insert(0, '.')
from common import save, R_TABLE

N = 4357


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
Q, F = raw_trunc(15.0, 0.000000, 0.017087, 0.02847898)
print('basin15 F=%.15f margin=%+.3e' % (F, F - R_TABLE))
save(Q, 'fresh-trunc-4357-output/basin15.txt')
Q, F = raw_trunc(25.0, 0.000000, 0.017087, 0.02847898)
print('basin25 F=%.15f margin=%+.3e' % (F, F - R_TABLE))
save(Q, 'fresh-trunc-4357-output/basin25.txt')
