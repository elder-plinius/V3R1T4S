#!/usr/bin/env python3
"""Shared fast double-precision tools for ring-graft lens."""
import numpy as np
from scipy.spatial import cKDTree

R_TABLE = 0.014965462848801963307763269064
# NOTE (packager): the original absolute run path was redacted for publication;
# point SEED at a local copy of the posted Packomania cci3949.txt seed if needed.
RUN = '<WORKDIR>/runs/2026-10-20-0858'
SEED = RUN + '/data/cci3949.txt'


def load(path):
    pts = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) >= 3:
                pts.append((float(p[1]), float(p[2])))
    return np.array(pts)


def save(P, path):
    with open(path, 'w') as f:
        for i, (x, y) in enumerate(P):
            f.write('%d %.30f %.30f\n' % (i + 1, x, y))


def feasible_r(P):
    """Fast double-precision feasible radius. ~2s at N=3949."""
    n = len(P)
    dmin = np.inf
    bs = 700
    for i0 in range(0, n, bs):
        A = P[i0:i0 + bs]
        D = np.linalg.norm(A[:, None, :] - P[None, :, :], axis=2)
        for k, i in enumerate(range(i0, min(i0 + bs, n))):
            D[k, i] = np.inf
        m = D.min()
        if m < dmin:
            dmin = m
    wall = 1.0 - np.linalg.norm(P, axis=1).max()
    return min(dmin / 2.0, wall)


def contacts(P, r, tol=1.001):
    """Undirected contact count and per-circle neighbor counts."""
    tree = cKDTree(P)
    pairs = tree.query_pairs(r=2 * r * tol, output_type='ndarray')
    nn = np.zeros(len(P), dtype=int)
    if len(pairs):
        np.add.at(nn, pairs[:, 0], 1)
        np.add.at(nn, pairs[:, 1], 1)
    return pairs, nn


def overlap_energy(P, r, freeze=None):
    """Sum of squared overlaps (pairs + wall). 0.0 <=> feasible at r."""
    tree = cKDTree(P)
    pairs = tree.query_pairs(r=2 * r * 1.02, output_type='ndarray')
    E = 0.0
    if len(pairs):
        d = P[pairs[:, 0]] - P[pairs[:, 1]]
        dist = np.linalg.norm(d, axis=1)
        ov = 2 * r - dist
        m = ov > 0
        E += float((ov[m] ** 2).sum())
    rad = np.linalg.norm(P, axis=1)
    ovw = rad + r - 1.0
    m = ovw > 0
    E += float((ovw[m] ** 2).sum())
    return E


def cavity_map(P, r, grid_step=None):
    """Grid sample of clearance: max over grid of (min dist to centers).
    Returns (best_points, best_clearance). A point fits a new circle of
    radius r iff clearance >= 2r and |p| <= 1-r."""
    if grid_step is None:
        grid_step = r * 0.7
    xs = np.arange(-1, 1, grid_step)
    X, Y = np.meshgrid(xs, xs)
    G = np.stack([X.ravel(), Y.ravel()], axis=1)
    G = G[np.linalg.norm(G, axis=1) <= 1 - r]
    tree = cKDTree(P)
    d, _ = tree.query(G, k=1)
    order = np.argsort(d)[::-1]
    return G[order], d[order]


def margin(P):
    return feasible_r(P) - R_TABLE
