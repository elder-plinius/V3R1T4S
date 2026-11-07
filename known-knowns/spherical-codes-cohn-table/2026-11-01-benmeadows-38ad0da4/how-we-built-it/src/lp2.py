"""Sequential LP polish with a narrow active window and a trust region.
Vectorised constraint assembly; HiGHS dual simplex."""
import time
import numpy as np
from scipy.optimize import linprog
from scipy import sparse


def normalize(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def maxcos(X):
    G = X @ X.T
    np.fill_diagonal(G, -2.0)
    return G.max()


def lp_step(X, c, r, window, method="highs-ds"):
    N, d = X.shape
    G = X @ X.T
    I, J = np.triu_indices(N, 1)
    g = G[I, J]
    act = g > c - window
    I, J, g = I[act], J[act], g[act]
    m = len(I)
    nv = N * d + 1
    ar = np.arange(d)
    rows = np.repeat(np.arange(m), 2 * d + 1)
    cols = np.concatenate([(I[:, None] * d + ar), (J[:, None] * d + ar), np.full((m, 1), N * d)], axis=1).ravel()
    vals = np.concatenate([X[J], X[I], -np.ones((m, 1))], axis=1).ravel()
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(m, nv))
    Aeq = sparse.csr_matrix((X.ravel(), (np.repeat(np.arange(N), d), np.arange(N * d))), shape=(N, nv))
    cobj = np.zeros(nv); cobj[-1] = 1.0
    lb = np.full(nv, -r); ub = np.full(nv, r); lb[-1] = -1; ub[-1] = 1
    res = linprog(cobj, A_ub=A, b_ub=-g, A_eq=Aeq, b_eq=np.zeros(N),
                  bounds=np.column_stack([lb, ub]), method=method)
    if res.status != 0:
        return None, m
    return normalize(X + res.x[:-1].reshape(N, d)), m


def polish(X, r=1e-3, rounds=300, deadline=None, verbose=False):
    X = normalize(X)
    c = maxcos(X)
    for k in range(rounds):
        if deadline and time.time() > deadline:
            break
        window = max(4 * r, 1e-9)
        t = time.time()
        Xn, m = lp_step(X, c, r, window)
        if Xn is None:
            r *= 0.5
            continue
        cn = maxcos(Xn)
        if verbose:
            print(f"  r={r:.1e} m={m} c={cn:.15f} dt={time.time()-t:.2f}", flush=True)
        if cn < c - 1e-16:
            X, c = Xn, cn
            r = min(r * 2, 1e-2)
        else:
            r *= 0.25
            if r < 1e-12:
                break
    return X, c
