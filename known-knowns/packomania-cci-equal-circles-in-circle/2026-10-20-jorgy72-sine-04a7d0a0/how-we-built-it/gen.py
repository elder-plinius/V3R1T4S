#!/usr/bin/env python3
"""Side-effect-free generators: hex truncations, phyllotaxis."""
import numpy as np


def hex_truncation(theta_deg, ox, oy, bound, s):
    th = np.radians(theta_deg)
    a1 = s * np.array([np.cos(th), np.sin(th)])
    a2 = s * np.array([np.cos(th + np.pi / 3), np.sin(th + np.pi / 3)])
    pts = []
    m = int(2.4 / s) + 2
    for i in range(-m, m + 1):
        for j in range(-m, m + 1):
            p = i * a1 + j * a2 + np.array([ox, oy])
            if np.linalg.norm(p) <= bound:
                pts.append(p)
    return np.array(pts)


def trim_to_N(P, N, rT, seed=0):
    P = P.copy()
    if len(P) == N:
        return P
    if len(P) > N:
        # drop outermost
        rad = np.linalg.norm(P, axis=1)
        keep = np.argsort(rad)[:N]
        return P[keep]
    rng = np.random.default_rng(seed)
    extra = []
    while len(P) + len(extra) < N:
        a = rng.random() * 2 * np.pi
        rr = 1 - rT * (0.5 + rng.random())
        extra.append([rr * np.cos(a), rr * np.sin(a)])
    return np.vstack([P, np.array(extra)])


def phyllotaxis(N, div_deg, fill=0.972):
    c = fill / np.sqrt(N)
    i = np.arange(1, N + 1)
    rr = c * np.sqrt(i)
    th = np.radians(div_deg) * i
    return np.stack([rr * np.cos(th), rr * np.sin(th)], axis=1)
