"""Search for spherical codes: smoothed max-cosine (log-sum-exp) descent with
rising sharpness, then sequential-LP polish of the active set.
Usage: python opt.py d N seconds seed outdir [table_value]
Writes outdir/<d>_<N>.txt with the best code found (one point per line)."""
import sys, time, os
import numpy as np
from scipy.optimize import minimize, linprog
from scipy import sparse


def normalize(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def maxcos(X):
    G = X @ X.T
    np.fill_diagonal(G, -2.0)
    return G.max()


def lse_descent(X, betas, iters=400):
    N, d = X.shape
    iu = np.triu_indices(N, 1)

    def f(y, beta):
        Y = y.reshape(N, d)
        nr = np.linalg.norm(Y, axis=1, keepdims=True)
        Z = Y / nr
        G = Z @ Z.T
        g = G[iu]
        m = g.max()
        e = np.exp(beta * (g - m))
        s = e.sum()
        val = m + np.log(s) / beta
        W = np.zeros((N, N))
        W[iu] = e / s
        W = W + W.T
        gZ = W @ Z
        # gradient through normalization
        gY = (gZ - Z * np.sum(gZ * Z, axis=1, keepdims=True)) / nr
        return val, gY.ravel()

    y = X.ravel().copy()
    for b in betas:
        r = minimize(f, y, args=(b,), jac=True, method="L-BFGS-B",
                     options={"maxiter": iters, "gtol": 1e-12, "ftol": 1e-15})
        y = normalize(r.x.reshape(N, d)).ravel()
    return y.reshape(N, d)


def lp_polish(X, rounds=200, tol=1e-15):
    N, d = X.shape
    X = normalize(X)
    c = maxcos(X)
    r = 1e-2
    delta = 1e-2
    for _ in range(rounds):
        G = X @ X.T
        I, J = np.triu_indices(N, 1)
        g = G[I, J]
        act = g > c - max(delta, 4 * r)
        I, J, g = I[act], J[act], g[act]
        m = len(I)
        nv = N * d + 1
        rows, cols, vals = [], [], []
        for k in range(m):
            i, j = I[k], J[k]
            rows += [k] * (2 * d + 1)
            cols += list(range(i * d, i * d + d)) + list(range(j * d, j * d + d)) + [N * d]
            vals += list(X[j]) + list(X[i]) + [-1.0]
        A = sparse.csr_matrix((vals, (rows, cols)), shape=(m, nv))
        rows, cols, vals = [], [], []
        for i in range(N):
            rows += [i] * d
            cols += list(range(i * d, i * d + d))
            vals += list(X[i])
        Aeq = sparse.csr_matrix((vals, (rows, cols)), shape=(N, nv))
        cobj = np.zeros(nv); cobj[-1] = 1.0
        bounds = [(-r, r)] * (N * d) + [(None, None)]
        res = linprog(cobj, A_ub=A, b_ub=-g, A_eq=Aeq, b_eq=np.zeros(N),
                      bounds=bounds, method="highs")
        if res.status != 0:
            r *= 0.5
            if r < 1e-14:
                break
            continue
        Xn = normalize(X + res.x[:-1].reshape(N, d))
        cn = maxcos(Xn)
        if cn < c - tol:
            gain = c - cn
            X, c = Xn, cn
            if gain < 1e-14:
                break
            r = min(r * 1.5, 5e-2)
        else:
            r *= 0.3
            if r < 1e-13:
                break
    return X, c


def run(d, N, seconds, seed, outdir, table=None):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    best, bestc = None, 9.0
    nres = 0
    betas = [10, 30, 100, 300, 1000, 3000, 10000]
    while time.time() - t0 < seconds:
        X = normalize(rng.standard_normal((N, d)))
        X = lse_descent(X, betas)
        c0 = maxcos(X)
        if best is not None and c0 > bestc + 5e-3:
            nres += 1
            continue
        X, c = lp_polish(X)
        nres += 1
        if c < bestc:
            best, bestc = X, c
    os.makedirs(outdir, exist_ok=True)
    fn = os.path.join(outdir, f"{d}_{N}.txt")
    # keep the better of an existing file and this run
    prev = None
    if os.path.exists(fn):
        P = np.loadtxt(fn, comments="#")
        prev = maxcos(normalize(P))
    if prev is None or bestc < prev:
        with open(fn, "w") as fh:
            fh.write(f"# d={d} N={N} c_float={bestc:.17g} table={table}\n")
            for row in best:
                fh.write(" ".join(f"{v:.20e}" for v in row) + "\n")
    print(f"{d} {N} best={bestc:.15f} table={table} restarts={nres} "
          f"diff={(float(table) - bestc) if table else 'na'}", flush=True)
    return bestc


if __name__ == "__main__":
    d, N, sec, seed = map(int, sys.argv[1:5])
    out = sys.argv[5]
    tab = sys.argv[6] if len(sys.argv) > 6 else None
    run(d, N, sec, seed, out, tab)
