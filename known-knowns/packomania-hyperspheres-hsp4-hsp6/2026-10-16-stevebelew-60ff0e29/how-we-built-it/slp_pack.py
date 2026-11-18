"""Sequential-linear-programming maximiser of the feasible radius of N equal balls in the unit d-ball.
Variables: displacements dx (n*d) and r. Pair distances and norms are linearised at the current point; a trust region
|dx_k| <= delta bounds the step; the TRUE r* (float64) is evaluated after every step and a step is kept only if it improves.
Pair linearisation under-estimates distances (norm is convex) so included pairs stay safe; wall steps are checked by the true r*.
"""
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

def rstar(X):
    diff = X[:, None, :] - X[None, :, :]
    D = np.sqrt((diff * diff).sum(-1))
    np.fill_diagonal(D, np.inf)
    nrm = np.linalg.norm(X, axis=1)
    return min(D.min() / 2.0, 1.0 - nrm.max()), D, nrm

def slp(X, delta=0.02, iters=400, tol=1e-15, delta_min=1e-13, margin=None):
    X = np.array(X, dtype=float)
    n, d = X.shape
    r, D, nrm = rstar(X)
    for _ in range(iters):
        reach = 2 * delta * np.sqrt(d) + (margin if margin is not None else 0.05 * r)
        I, J = np.where(np.triu(D < 2 * r + reach, 1))
        rows, cols, vals, b = [], [], [], []
        k = 0
        for i, j in zip(I, J):
            u = (X[i] - X[j]) / D[i, j]
            # constraint: -(u.dxi) + (u.dxj) + 2 r_new <= D0   (from D0 + u.(dxi - dxj) >= 2 r_new)
            for c in range(d):
                rows += [k, k]; cols += [i * d + c, j * d + c]; vals += [-u[c], u[c]]
            rows.append(k); cols.append(n * d); vals.append(2.0); b.append(D[i, j]); k += 1
        for i in range(n):
            if nrm[i] > 1 - r - reach:
                v = X[i] / max(nrm[i], 1e-300)
                for c in range(d):
                    rows.append(k); cols.append(i * d + c); vals.append(v[c])
                rows.append(k); cols.append(n * d); vals.append(1.0); b.append(1.0 - nrm[i]); k += 1
        A = coo_matrix((vals, (rows, cols)), shape=(k, n * d + 1)).tocsr()
        cobj = np.zeros(n * d + 1); cobj[-1] = -1.0
        bounds = [(-delta, delta)] * (n * d) + [(0.0, 1.0)]
        res = linprog(cobj, A_ub=A, b_ub=np.array(b), bounds=bounds, method='highs')
        if res.status != 0:
            delta *= 0.5
            if delta < delta_min: break
            continue
        Xn = X + res.x[:n * d].reshape(n, d)
        rn, Dn, nn = rstar(Xn)
        if rn > r + tol:
            X, r, D, nrm = Xn, rn, Dn, nn
            delta = min(delta * 1.5, 0.05)
        else:
            delta *= 0.5
            if delta < delta_min: break
    return X, r

def slack(X, r):
    _, D, nrm = rstar(X)
    s_pair = D.min(axis=1) / 2.0 - r
    s_wall = (1.0 - nrm) - r
    return np.minimum(s_pair, s_wall), s_pair, s_wall

def kick(X, r, rng, k=3, amp=1.0):
    """Move the k loosest balls (largest slack) by a random vector of size amp*r; re-project inside the container."""
    s, _, _ = slack(X, r)
    idx = np.argsort(-s)[:k]
    Xn = X.copy()
    for i in idx:
        v = rng.normal(size=X.shape[1]); v /= np.linalg.norm(v)
        Xn[i] = Xn[i] + amp * r * rng.uniform(0.5, 1.5) * v
        nn = np.linalg.norm(Xn[i])
        if nn > 1 - r: Xn[i] *= (1 - r) / nn
    return Xn

def basin_hop(X, rng, hops=20, k=3, amp=1.0, deadline=None, time=None):
    X, r = slp(X)
    best_X, best_r = X.copy(), r
    for h in range(hops):
        if deadline is not None and time() > deadline: break
        Xk = kick(best_X, best_r, rng, k=k, amp=amp)
        Xk, rk = slp(Xk, delta=0.02)
        if rk > best_r + 1e-14:
            best_X, best_r = Xk, rk
    return best_X, best_r

def write_coords(path, X, header=None):
    with open(path, 'w') as f:
        if header: f.write(header.rstrip('\n') + '\n')
        for row in X:
            f.write(' '.join('%.17g' % v for v in row) + '\n')
