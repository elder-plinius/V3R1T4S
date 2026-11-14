"""Harmonic energy optimization on product of unit spheres.

E = sum_{i<j} |x_i - x_j|^{-p}, p = n-2, x_i unit vectors in R^n.
Free variables X in R^{N x n}; objective E(P(X)) with P row-normalization.
grad_X_i = (G_i - (G_i . y_i) y_i) / |x_i|  where G = ambient grad wrt Y.
"""
import numpy as np
from scipy.optimize import minimize


def energy_grad(Y, p):
    """Y (N,n) unit vectors. Returns E and ambient gradient G wrt Y."""
    N, n = Y.shape
    D = Y[:, None, :] - Y[None, :, :]
    r2 = np.einsum('ijk,ijk->ij', D, D)
    np.fill_diagonal(r2, np.inf)
    rp = r2 ** (-p / 2.0)
    np.fill_diagonal(rp, 0.0)
    E = rp.sum() / 2.0
    rm2 = r2 ** (-(p + 2) / 2.0)
    np.fill_diagonal(rm2, 0.0)
    G = -p * np.einsum('ij,ijk->ik', rm2, D)
    return E, G


def energy(Y, p):
    N, n = Y.shape
    E = 0.0
    for i in range(N - 1):
        d = Y[i + 1:] - Y[i]
        r2 = np.einsum('ij,ij->i', d, d)
        E += np.sum(r2 ** (-p / 2.0))
    return E


def minimize_energy(Y0, p, maxiter=3000, gtol=1e-9, ftol=1e-15, quiet=True):
    """L-BFGS-B on free variables with internal normalization."""
    X0 = Y0.copy()
    N, n = X0.shape

    def f(x):
        X = x.reshape(N, n)
        nrm = np.linalg.norm(X, axis=1)
        Y = X / nrm[:, None]
        E, G = energy_grad(Y, p)
        gy = np.einsum('ij,ij->i', G, Y)
        GX = (G - gy[:, None] * Y) / nrm[:, None]
        return E, GX.ravel()

    res = minimize(f, X0.ravel(), jac=True, method='L-BFGS-B',
                   options={'maxiter': maxiter, 'maxfun': maxiter * 4,
                            'ftol': ftol, 'gtol': gtol, 'maxcor': 20})
    X = res.x.reshape(N, n)
    Y = X / np.linalg.norm(X, axis=1)[:, None]
    return Y, res.fun, res


def basin_hop(Ybest, p, iters, rng, scale=0.3, kmove=0, min_kwargs=None):
    """Perturb-and-relax basin hopping. Ybest: unit (N,n).
    kmove>0: reinsert kmove worst-contributing points at random spots."""
    if min_kwargs is None:
        min_kwargs = {}
    N, n = Ybest.shape
    Ebest, _ = energy_grad(Ybest, p)
    Ebest = float(Ebest)
    hist = [Ebest]
    for it in range(iters):
        Y = Ybest.copy()
        if kmove:
            # move k random points to random locations
            idx = rng.choice(N, size=kmove, replace=False)
            Y[idx] = rng.normal(size=(kmove, n))
            Y += scale * 0.3 * rng.normal(size=Y.shape)
        else:
            Y += scale * rng.normal(size=Y.shape)
        Y /= np.linalg.norm(Y, axis=1)[:, None]
        Y, E, res = minimize_energy(Y, p, **min_kwargs)
        if E < Ebest - 1e-12:
            Ebest = E
            Ybest = Y
        hist.append(Ebest)
    return Ybest, Ebest, hist


# ---- high precision ----
def energy_mp(Y, p, dps=60):
    import mpmath as mp
    mp.mp.dps = dps
    N, n = Y.shape
    Ym = [[mp.mpf(repr(float(v))) for v in row] for row in Y]
    # renormalize in mp
    for i in range(N):
        s = mp.sqrt(sum(v * v for v in Ym[i]))
        Ym[i] = [v / s for v in Ym[i]]
    E = mp.mpf(0)
    for i in range(N):
        for j in range(i + 1, N):
            r2 = sum((Ym[i][k] - Ym[j][k]) ** 2 for k in range(n))
            E += r2 ** (-mp.mpf(p) / 2)
    return E, Ym


def write_cell(path, N, n, Y):
    """Write cell file: header + N lines of n comma-separated reals (30+ digits)."""
    import mpmath as mp
    mp.mp.dps = 50
    p = n - 2
    E, Ym = energy_mp(Y, p, dps=60)
    with open(path, 'w') as f:
        f.write(f"# cell {N}-{n} energy {mp.nstr(E, 45)}\n")
        for row in Ym:
            f.write(",".join(mp.nstr(v, 30) for v in row) + "\n")
    return E
