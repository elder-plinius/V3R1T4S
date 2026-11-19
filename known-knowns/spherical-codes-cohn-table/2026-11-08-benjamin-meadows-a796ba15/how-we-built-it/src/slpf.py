"""Faster SLP polish: vectorized LP construction, capped active set."""
import numpy as np
import sys
sys.path.insert(0, '/work')
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack as svstack, csr_matrix


def slp_fast(X, max_iter=25, rho0=0.03, tol=1e-13, cap=1200, verbose=False):
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    N, d = X.shape
    rho = rho0
    cur = None
    iu = np.triu_indices(N, 1)
    for it in range(max_iter):
        G = X @ X.T
        np.fill_diagonal(G, -9)
        gmax = G.max()
        if cur is None:
            cur = gmax
        vals = G[iu]
        delta = max(3e-5, 8 * rho)
        act = np.where(vals > gmax - delta)[0]
        if len(act) > cap:
            thr = np.partition(vals[act], len(act) - cap)[len(act) - cap]
            act = act[vals[act] >= thr][:cap]
        pi = iu[0][act]; pj = iu[1][act]
        nA = len(act)
        nvar = N * d + 1
        # constraint rows: for pair (i,j): x_j.u_i + x_i.u_j <= t - g_ij
        # build sparse data
        rows = np.repeat(np.arange(nA), d)
        rows = np.concatenate([rows, rows])
        cols_i = np.repeat(pi * d, d) + np.tile(np.arange(d), nA)
        cols_j = np.repeat(pj * d, d) + np.tile(np.arange(d), nA)
        cols = np.concatenate([cols_i, cols_j])
        data = np.concatenate([X[pj].ravel(), X[pi].ravel()])
        A = coo_matrix((data, (rows, cols)), shape=(nA, nvar))
        # t column
        tcol = coo_matrix((-np.ones(nA), (np.arange(nA),
                                          np.zeros(nA, int) + nvar - 1)),
                          shape=(nA, nvar))
        A = A + tcol
        rhs = -G[pi, pj]
        # equalities: x_i.u_i = 0 for all i (keep on sphere)
        erow = np.repeat(np.arange(N), d)
        ecol = np.repeat(np.arange(N) * d, d) + np.tile(np.arange(d), N)
        edat = X.ravel()
        E = coo_matrix((edat, (erow, ecol)), shape=(N, nvar))
        c = np.zeros(nvar); c[-1] = 1.0
        bounds = [(-rho, rho)] * (N * d) + [(None, gmax)]
        res = linprog(c, A_ub=csr_matrix(A), b_ub=rhs,
                      A_eq=csr_matrix(E), b_eq=np.zeros(N),
                      bounds=bounds, method='highs-ipm',
                      options={'time_limit': 20.0,
                               'ipm_iteration_limit': 60})
        if not res.success:
            rho *= 0.5
            if rho < 1e-9:
                break
            continue
        u = res.x[:-1].reshape(N, d)
        Xn = X + u
        Xn /= np.linalg.norm(Xn, axis=1, keepdims=True)
        Gn = Xn @ Xn.T; np.fill_diagonal(Gn, -9)
        new = Gn.max()
        if verbose:
            print(f'  slpf {it}: {gmax:.12f} -> {new:.12f} nA={nA} rho={rho:.3g}',
                  flush=True)
        if new < cur - 1e-15:
            X = Xn
            cur = new
            rho = min(rho * 1.4, 0.2)
        else:
            rho *= 0.4
            if rho < 1e-11:
                break
    return X, cur
