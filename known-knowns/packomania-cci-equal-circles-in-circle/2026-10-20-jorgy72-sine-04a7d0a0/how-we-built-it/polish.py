#!/usr/bin/env python3
"""Bottleneck polisher: minimize the smooth-max of overlaps via L-BFGS-B.

E_alpha = (1/alpha) * logsumexp(alpha * ov_c)  ->  max_c ov_c as alpha->inf.
Minimizing E_alpha directly maximizes the binding constraint (the true r*).
Fixed-skin neighbor lists, outer rebuilds.
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import feasible_r


def smooth_max_polish(P, r, freeze=None, alpha=3e5, outer=10, maxiter=500,
                      skin=1.3, log=None):
    P = P.copy()
    n = len(P)
    mv = ~freeze if freeze is not None else np.ones(n, dtype=bool)
    idx = np.where(mv)[0]
    for o in range(outer):
        tree = cKDTree(P)
        pairs = tree.query_pairs(r=2 * r * skin, output_type='ndarray')
        keep = mv[pairs[:, 0]] | mv[pairs[:, 1]]
        pairs = pairs[keep]
        A, B = pairs[:, 0], pairs[:, 1]
        npair = len(pairs)

        def fg(x):
            P[idx] = x.reshape(-1, 2)
            d = P[A] - P[B]
            dist = np.sqrt((d ** 2).sum(axis=1))
            ov = 2 * r - dist
            rad = np.sqrt((P ** 2).sum(axis=1))
            ovw = rad + r - 1.0
            allov = np.concatenate([ov, ovw])
            m = allov.max()
            # logsumexp with shift; gradient weights
            e = np.exp(np.clip(alpha * (allov - m), -50, 50))
            S = e.sum()
            E = m + np.log(S) / alpha
            w = e / S  # dE/d(ov_c)
            F = np.zeros_like(P)
            wp = w[:npair]
            # d(ov)/dx_i = -(d_vec/dist) for i=A, +(d_vec/dist) for i=B
            coef = (wp / np.maximum(dist, 1e-12))[:, None]
            np.add.at(F, A, -coef * d)
            np.add.at(F, B, coef * d)
            ww = w[npair:]
            F += (ww / np.maximum(rad, 1e-12))[:, None] * P
            return E, F[idx].ravel()

        res = minimize(fg, P[idx].ravel(), jac=True, method='L-BFGS-B',
                       options={'maxiter': maxiter, 'ftol': 1e-32,
                                'gtol': 1e-14})
        P[idx] = res.x.reshape(-1, 2)
        Emax = float(res.fun)
        if log:
            fr = feasible_r(P)
            log.write('  outer %d smoothmax=%.3e fr=%.15f\n' % (o, Emax, fr))
        if Emax < -1e-9:
            break
    return P, Emax
