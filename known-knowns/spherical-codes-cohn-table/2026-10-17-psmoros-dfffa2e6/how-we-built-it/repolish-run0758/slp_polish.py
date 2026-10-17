#!/usr/bin/env python3
"""Active-set sequential-LP trust-region polish for spherical codes (calibrator lens, own code).

Problem: minimise max_{i<j} <x_i, x_j> over unit vectors x_1..x_N in R^d.
Step: on the near-active pairs A = {(i,j): c_ij >= cmax - eps}, solve the LP (scaled by the trust radius r,
delta_i = r * u_i)
    minimise sigma  s.t.  x_j.u_i + x_i.u_j - sigma <= (cmax - c_ij) / r   for (i,j) in A
                          x_i.u_i = 0                                       (tangent step)
                          -1 <= u <= 1
then x_i <- (x_i + r u_i) / |x_i + r u_i|. Predicted decrease = -r*sigma; actual decrease is measured on the
neighbour list. Accept if actual > 0 and ratio > 1e-3; adapt r.
Neighbour list: pairs with c >= cmax_rebuild - W at the last rebuild (blockwise Gram, never a dense N x N per
iteration); |c_ij(X) - c_ij(X0)| <= |x_i - x0_i| + |x_j - x0_j|, so pairs outside the list stay below
cmax_rebuild - W + 2*Dmax; we rebuild whenever that bound reaches the current max (provably safe).
"""
import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog


def normalize(X):
    return X / np.linalg.norm(X, axis=1)[:, None]


def pairs_above(X, thr, block=1024):
    """All (i, j, c) with i < j and c = <x_i, x_j> >= thr; blockwise."""
    N = X.shape[0]
    I, J, C = [], [], []
    for s in range(0, N, block):
        G = X[s:s + block] @ X.T
        rows = np.arange(G.shape[0])
        mask = np.arange(N)[None, :] > (rows + s)[:, None]
        G = np.where(mask, G, -3.0)
        ii, jj = np.nonzero(G >= thr)
        I.append(ii + s)
        J.append(jj)
        C.append(G[ii, jj])
    return np.concatenate(I), np.concatenate(J), np.concatenate(C)


def max_ip(X, block=1024):
    N = X.shape[0]
    m = -3.0
    for s in range(0, N, block):
        G = X[s:s + block] @ X.T
        rows = np.arange(G.shape[0])
        mask = np.arange(N)[None, :] > (rows + s)[:, None]
        G = np.where(mask, G, -3.0)
        m = max(m, float(G.max()))
    return m


class NeighbourList:
    def __init__(self, X, W):
        self.W = W
        self.rebuild(X)

    def rebuild(self, X):
        self.X0 = X.copy()
        self.cfull = max_ip(X)
        self.I, self.J, _ = pairs_above(X, self.cfull - self.W)
        self.nrebuild = getattr(self, "nrebuild", 0) + 1

    def values(self, X):
        return np.einsum("ij,ij->i", X[self.I], X[self.J])

    def safe_max(self, X):
        """Exact float max over all pairs, using the list when provably safe, else rebuilding."""
        c = self.values(X)
        m = float(c.max())
        D = float(np.max(np.linalg.norm(X - self.X0, axis=1)))
        if self.cfull - self.W + 2.0 * D >= m - 1e-12:
            self.rebuild(X)
            c = self.values(X)
            m = float(c.max())
        return m, c


def lp_step(X, I, J, c, cmax, r, eps, tol=1e-10):
    sel = c >= cmax - eps
    Ia, Ja, ca = I[sel], J[sel], c[sel]
    P = np.unique(np.concatenate([Ia, Ja]))
    loc = -np.ones(X.shape[0], dtype=np.int64)
    loc[P] = np.arange(P.size)
    d = X.shape[1]
    nP = P.size
    nv = nP * d + 1
    m = Ia.size
    # inequality rows: x_j . u_i + x_i . u_j - sigma <= (cmax - c_ij)/r
    rows = np.repeat(np.arange(m), 2 * d + 1)
    li, lj = loc[Ia], loc[Ja]
    cols_i = (li[:, None] * d + np.arange(d)[None, :])
    cols_j = (lj[:, None] * d + np.arange(d)[None, :])
    cols = np.concatenate([cols_i, cols_j, np.full((m, 1), nv - 1)], axis=1).ravel()
    vals = np.concatenate([X[Ja], X[Ia], -np.ones((m, 1))], axis=1).ravel()
    A_ub = sp.csr_matrix((vals, (rows, cols)), shape=(m, nv))
    b_ub = (cmax - ca) / r
    # tangent equalities
    erows = np.repeat(np.arange(nP), d)
    ecols = (np.arange(nP)[:, None] * d + np.arange(d)[None, :]).ravel()
    evals = X[P].ravel()
    A_eq = sp.csr_matrix((evals, (erows, ecols)), shape=(nP, nv))
    b_eq = np.zeros(nP)
    cost = np.zeros(nv)
    cost[-1] = 1.0
    bounds = [(-1.0, 1.0)] * (nv - 1) + [(None, None)]
    res = linprog(cost, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs",
                  options={
                           "presolve": True})
    if res.status != 0:
        return None, None, m, nP
    U = np.zeros_like(X)
    U[P] = res.x[:-1].reshape(nP, d)
    return U, float(res.x[-1]), m, nP


def polish(X, time_cap=60.0, r0=1e-3, r_min=1e-13, W=0.05, eps_cap=0.02, max_iter=100000, log=None,
           stall_tol=1e-9):
    """Return (X_best, info). X is not modified."""
    t0 = time.process_time()
    X = normalize(np.array(X, dtype=np.float64))
    N, d = X.shape
    nl = NeighbourList(X, W)
    cmax, c = nl.safe_max(X)
    c_start = cmax
    r_max = eps_cap / (2.2 * np.sqrt(d))
    r = min(r0, r_max)
    it = acc = 0
    stall = 0
    status = "max_iter"
    hist = []
    while it < max_iter:
        if time.process_time() - t0 > time_cap:
            status = "time_cap"
            break
        if r < r_min:
            status = "r_min"
            break
        it += 1
        eps = min(eps_cap, 2.2 * r * np.sqrt(d) + 1e-13)
        U, sigma, m, nP = lp_step(X, nl.I, nl.J, c, cmax, r, eps)
        if U is None:
            r *= 0.5
            continue
        pred = -r * sigma
        if pred <= stall_tol * r:
            # LP sees no first-order descent at this radius
            stall += 1
            if stall >= 3:
                status = "stationary"
                break
            r *= 0.5
            continue
        stall = 0
        Xn = normalize(X + r * U)
        mn, cn = nl.safe_max(Xn)
        act = cmax - mn
        rho = act / pred
        if act > 0 and rho > 1e-3:
            X, cmax, c = Xn, mn, cn
            acc += 1
            if rho > 0.5 and np.max(np.abs(U)) > 0.99:
                r = min(2.0 * r, r_max)
            elif rho < 0.25:
                r *= 0.5
        else:
            r *= 0.3
        if log is not None and it % 25 == 0:
            log("it %d acc %d r %.2e cmax %.15f gain %.3e m %d nP %d t %.1f" % (
                it, acc, r, cmax, c_start - cmax, m, nP, time.process_time() - t0))
        hist.append((it, cmax))
    # final exact float max (full, not the list)
    cfinal = max_ip(X)
    info = dict(c_start=c_start, c_final=cfinal, gain_float=c_start - cfinal, iters=it, accepted=acc, r=r,
                status=status, secs=time.process_time() - t0, rebuilds=nl.nrebuild)
    return X, info
