#!/usr/bin/env python3
"""Regenerate two diverse truncation candidates from the wide-search TOP20.

cand01: theta 7.5074 deg basin (-1.999e-05 raw).
cand02: theta 25.0394 deg basin (-2.051e-05 raw).
The other two polished candidates are saved directly by wide_search.py
(random_best.txt, theta 21.80 deg; refine_best.txt, theta 9.51 deg).
Run from how-we-built-it/ :  python3 gen_cands.py
Writes cand01.txt, cand02.txt into ./deep-polish-4153-output/ (created
by deep_polish.py) — or pass an output dir as argv[1].
"""
import numpy as np
import os
import sys

N = 4153
CANDS = [
    (7.5074, 0.02915287, 0.016191, 0.009265),
    (25.0394, 0.02915183, 0.018219, 0.000735),
]


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
    idx = np.argsort(rad)[:N]
    return P[idx]


OUT = sys.argv[1] if len(sys.argv) > 1 else './deep-polish-4153-output/'
os.makedirs(OUT, exist_ok=True)
for ci, (th, s, ox, oy) in enumerate(CANDS):
    Q = raw_trunc(th, ox, oy, s)
    with open(OUT + 'cand%02d.txt' % (ci + 1), 'w') as f:
        for i, (x, y) in enumerate(Q):
            f.write('%d %.30f %.30f\n' % (i + 1, x, y))
    print('cand%02d th=%.4f rows=%d' % (ci + 1, th, len(Q)))
