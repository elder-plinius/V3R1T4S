"""Sequential LP polish of the active contact set: maximise r subject to linearised
pair and container constraints with a shrinking trust region (HiGHS)."""
import numpy as np, sys
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from scipy.spatial.distance import pdist, squareform
from core import feasible_np

def slp(x, iters=60, delta=1e-4, tol_frac=0.02, verbose=False):
    x = x.copy(); n = len(x); r = feasible_np(x)
    for it in range(iters):
        Dm = squareform(pdist(x)); iu = np.triu_indices(n, 1)
        dij = Dm[iu]; sel = dij < 2 * r * (1 + tol_frac)
        I, J, dd = iu[0][sel], iu[1][sel], dij[sel]
        U = (x[I] - x[J]) / dd[:, None]
        nr = np.linalg.norm(x, axis=1); B = np.where(nr > 1 - r * (1 + tol_frac) - r * tol_frac)[0]
        nv = n * 4 + 1; rows, cols, vals = [], [], []; b = []
        for k in range(len(I)):
            for a in range(4):
                rows += [k, k]; cols += [I[k]*4+a, J[k]*4+a]; vals += [-U[k, a], U[k, a]]
            rows.append(k); cols.append(nv - 1); vals.append(2.0); b.append(dd[k] - 2 * r)
        m0 = len(I)
        for q, i in enumerate(B):
            v = x[i] / nr[i]
            for a in range(4): rows.append(m0+q); cols.append(i*4+a); vals.append(v[a])
            rows.append(m0+q); cols.append(nv-1); vals.append(1.0); b.append(1 - r - nr[i])
        A = coo_matrix((vals, (rows, cols)), shape=(m0 + len(B), nv)).tocsr()
        c = np.zeros(nv); c[-1] = -1
        # variables scaled by delta so solver tolerances act relative to the step
        bounds = [(-1, 1)] * (nv - 1) + [(None, None)]
        res = linprog(c, A_ub=A, b_ub=np.array(b) / delta, bounds=bounds, method='highs',
                      options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
        if res.status != 0: delta *= 0.3; continue
        res.x = res.x * delta
        y = x + res.x[:-1].reshape(n, 4); ry = feasible_np(y)
        if verbose: print(it, delta, res.x[-1], ry - r)
        if ry > r: x, r = y, ry
        else: delta *= 0.3
        if 0 < ry - r < 1e-16 * 0 + 1e-17: break
        if delta < 1e-15: break
    return x, r

if __name__ == '__main__':
    from run import load_best, save, T
    for N in map(int, sys.argv[1].split(',')):
        r0, x = load_best(N)
        y, r = slp(x, verbose=True)
        print(N, r0 - T[N], r - T[N], r - r0)
