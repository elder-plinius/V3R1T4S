"""Seeded optimization via high-beta L-BFGS continuation + SLP.
Never goes to low beta (which unwinds good seeds)."""
import numpy as np, sys, time
sys.path.insert(0, '/work')
import sph
from scipy.optimize import minimize


def lbfgs_b(X0, beta, maxiter=120, maxls=8, verbose=False, tag=''):
    """L-BFGS on (1/beta) logsumexp(beta*g_ij), scale-invariant objective."""
    N, d = X0.shape
    iu = np.triu_indices(N, 1)
    calls = [0]

    def fg(y):
        X = y.reshape(N, d)
        X = X / np.linalg.norm(X, axis=1, keepdims=True)
        G = X @ X.T
        v = G[iu]
        m = v.max()
        e = np.exp(beta * (v - m))
        s = e.sum()
        f = m + np.log(s) / beta
        w = e / s
        W = np.zeros((N, N))
        W[iu] = w
        W += W.T
        grad = W @ X
        grad -= (grad * X).sum(1, keepdims=True) * X
        calls[0] += 1
        return f, grad.ravel()

    res = minimize(fg, X0.ravel(), jac=True, method='L-BFGS-B',
                   options={'maxiter': maxiter, 'maxls': maxls,
                            'ftol': 1e-19, 'gtol': 1e-12})
    X = res.x.reshape(N, d)
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    if verbose:
        G = X @ X.T; np.fill_diagonal(G, -9)
        print(f'    {tag} beta={beta:g} it={res.nit} calls={calls[0]} '
              f'maxip={G.max():.12f}', flush=True)
    return X


def seeded(core_X, newpts, betas=(1e4, 3e4, 1e5, 3e5, 1e6, 3e6),
           iters=150, slp_iter=50, verbose=True):
    X = np.vstack([core_X] + [p[None, :] for p in newpts])
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    for b in betas:
        t0 = time.time()
        X = lbfgs_b(X, b, iters, verbose=verbose, tag='seed')
    if slp_iter:
        X, g = sph.slp_polish(X, max_iter=slp_iter)
    else:
        G = X @ X.T; np.fill_diagonal(G, -9); g = G.max()
    if verbose:
        print(f'    SLP -> {g:.12f}', flush=True)
    return g, X
