#!/usr/bin/env python3
"""Fast jammer: L-BFGS-B on overlap energy with fixed-skin neighbor lists.

jam(P, r): minimize E = sum overlaps^2 (+ wall). E == 0 <=> feasible at r.
inflate_jam / basin-hop built on top.
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import overlap_energy


def jam(P, r, freeze=None, outer=8, maxiter=400, skin=1.25, log=None,
        etarget=1e-28):
    P = P.copy()
    n = len(P)
    mv = ~freeze if freeze is not None else np.ones(n, dtype=bool)
    idx = np.where(mv)[0]
    E = overlap_energy(P, r)
    for o in range(outer):
        if E <= etarget:
            break
        tree = cKDTree(P)
        pairs = tree.query_pairs(r=2 * r * skin, output_type='ndarray')
        keep = mv[pairs[:, 0]] | mv[pairs[:, 1]]
        pairs = pairs[keep]
        A, B = pairs[:, 0], pairs[:, 1]

        def fg(x):
            P[idx] = x.reshape(-1, 2)
            d = P[A] - P[B]
            dist = np.sqrt((d ** 2).sum(axis=1))
            ov = 2 * r - dist
            pos = ov > 0
            E_ = float((ov[pos] ** 2).sum()) if pos.any() else 0.0
            rad = np.sqrt((P ** 2).sum(axis=1))
            ovw = rad + r - 1.0
            posw = ovw > 0
            if posw.any():
                E_ += float((ovw[posw] ** 2).sum())
            F = np.zeros_like(P)
            if pos.any():
                w = -2.0 * ov[pos] / np.maximum(dist[pos], 1e-12)
                g = w[:, None] * d[pos]
                np.add.at(F, A[pos], g)
                np.add.at(F, B[pos], -g)
            if posw.any():
                F[posw] += (2.0 * ovw[posw] / np.maximum(rad[posw], 1e-12))[:, None] * P[posw]
            return E_, F[idx].ravel()

        res = minimize(fg, P[idx].ravel(), jac=True, method='L-BFGS-B',
                       options={'maxiter': maxiter, 'ftol': 1e-32,
                                'gtol': 1e-13})
        P[idx] = res.x.reshape(-1, 2)
        E = float(res.fun)
        if log:
            log.write('  outer %d E=%.3e npairs=%d nit=%d\n'
                      % (o, E, len(pairs), res.nit))
    return P, E


def inflate_jam(P0, r_target, freeze=None, stages=12, r_start=None, log=None):
    P = P0.copy()
    if r_start is None:
        r_start = r_target * 0.80
    E = 0.0
    for s in range(stages):
        r = r_start * (r_target / r_start) ** ((s + 1) / stages)
        P, E = jam(P, r, freeze=freeze, log=None)
        if log:
            log.write('stage %d/%d r=%.15f E=%.3e\n' % (s + 1, stages, r, E))
    return P, E


def basin_hop(P, r_test, movers, hops=12, kick=None, seed=0, log=None,
              ckpt=None):
    """Repeated kick + jam. Returns best (P, E). E->0 means feasible win."""
    rng = np.random.default_rng(seed)
    if kick is None:
        kick = r_test * 0.5
    bestP, bestE = jam(P, r_test,
                       freeze=~movers if movers is not None else None, log=None)
    if log:
        log.write('hop -1 (no kick) E=%.3e\n' % bestE)
    cur = bestP.copy()
    for h in range(hops):
        Q = cur.copy()
        Q[movers] += rng.normal(0, kick, size=(movers.sum(), 2))
        rad = np.linalg.norm(Q, axis=1)
        over = rad > 1.0
        Q[over] *= (0.999 / rad[over])[:, None]
        Q, E = jam(Q, r_test, freeze=~movers, log=None)
        if E < bestE:
            bestE, bestP = E, Q.copy()
            cur = Q.copy()
            if log:
                log.write('hop %d NEW BEST E=%.3e\n' % (h, E))
        elif log:
            log.write('hop %d E=%.3e\n' % (h, E))
        if ckpt and h % 4 == 0:
            np.save(ckpt, bestP)
        if bestE < 1e-28:
            break
    return bestP, bestE
