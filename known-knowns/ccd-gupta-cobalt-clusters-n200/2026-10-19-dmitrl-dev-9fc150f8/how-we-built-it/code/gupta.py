"""Gupta (second-moment tight-binding) potential in reduced units (r in units of r0), numpy implementation used by the
SEARCH (part B). The confirmatory checker (part C) is a separate implementation.

E = sum_i [ sum_{j!=i} A exp(-p (r_ij - 1)) - sqrt( sum_{j!=i} xi^2 exp(-2 q (r_ij - 1)) ) ]   (eV; r in units of r0)
Cleri-Rosato (1993) cobalt: A = 0.0950 eV, xi = 1.4880 eV, p = 11.604, q = 2.286, r0 = 2.497 A.
"""
import numpy as np

CO = dict(A=0.0950, xi=1.4880, p=11.604, q=2.286)


def energy_grad(x, A=CO["A"], xi=CO["xi"], p=CO["p"], q=CO["q"], grad=True):
    X = np.asarray(x, dtype=float).reshape(-1, 3)
    n = len(X)
    d = X[:, None, :] - X[None, :, :]
    r = np.sqrt((d ** 2).sum(-1))
    np.fill_diagonal(r, 1.0)
    rep = A * np.exp(-p * (r - 1.0))
    att = xi * xi * np.exp(-2.0 * q * (r - 1.0))
    np.fill_diagonal(rep, 0.0)
    np.fill_diagonal(att, 0.0)
    rho = att.sum(1)
    sr = np.sqrt(rho)
    e = rep.sum() - sr.sum()
    if not grad:
        return e
    # dE/dr_ij for the pair (i, j), counting both i-sum and j-sum terms
    # repulsive: d/dr [A e^{-p(r-1)}] = -p * rep; appears twice (i and j sums)
    # attractive: -sqrt(rho_i): d/dr = -(1/(2 sqrt(rho_i))) * (-2q) att_ij = q att_ij / sqrt(rho_i); plus the j term
    inv = np.where(sr > 0, 1.0 / sr, 0.0)
    dEdr = -2.0 * p * rep + q * att * (inv[:, None] + inv[None, :])
    np.fill_diagonal(dEdr, 0.0)
    rr = r.copy()
    np.fill_diagonal(rr, np.inf)
    fac = dEdr / rr
    g = (fac[:, :, None] * d).sum(1)
    return e, g.ravel()


def energy(x, **kw):
    return energy_grad(x, grad=False, **kw)
