"""Spherical-code search: coarse log-sum-exp descent, then a descending
threshold schedule. For a threshold t we minimise F = sum_{i<j} max(0, <x_i,x_j> - t)^2
over unit vectors (L-BFGS on unnormalised coordinates); if the result has
max cosine <= t (to 1e-15) the threshold is accepted and lowered, otherwise the
step is halved."""
import sys, time, os
import numpy as np
from scipy.optimize import minimize


def normalize(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def maxcos(X):
    G = X @ X.T
    np.fill_diagonal(G, -2.0)
    return G.max()


def _lse(y, N, d, beta, iu):
    Y = y.reshape(N, d)
    nr = np.linalg.norm(Y, axis=1, keepdims=True)
    Z = Y / nr
    G = Z @ Z.T
    g = G[iu]
    m = g.max()
    e = np.exp(beta * (g - m))
    s = e.sum()
    W = np.zeros((N, N))
    W[iu] = e / s
    W = W + W.T
    gZ = W @ Z
    gY = (gZ - Z * np.sum(gZ * Z, axis=1, keepdims=True)) / nr
    return m + np.log(s) / beta, gY.ravel()


def _pen(y, N, d, t):
    Y = y.reshape(N, d)
    nr = np.linalg.norm(Y, axis=1, keepdims=True)
    Z = Y / nr
    G = Z @ Z.T
    np.fill_diagonal(G, -2.0)
    E = np.maximum(G - t, 0.0)
    F = 0.5 * np.sum(E * E)  # each pair counted twice -> 0.5 gives sum over pairs
    gZ = 2.0 * (E @ Z)
    gY = (gZ - Z * np.sum(gZ * Z, axis=1, keepdims=True)) / nr
    return F, gY.ravel()


def coarse(X, betas=(10, 30, 100, 300), iters=300):
    N, d = X.shape
    iu = np.triu_indices(N, 1)
    y = X.ravel()
    for b in betas:
        y = minimize(_lse, y, args=(N, d, b, iu), jac=True, method="L-BFGS-B",
                     options={"maxiter": iters, "gtol": 1e-12, "ftol": 1e-15}).x
        y = normalize(y.reshape(N, d)).ravel()
    return y.reshape(N, d)


def descend(X, step=1e-3, minstep=1e-13, iters=2000, deadline=None):
    N, d = X.shape
    X = normalize(X)
    c = maxcos(X)
    while step > minstep:
        if deadline and time.time() > deadline:
            break
        t = c - step
        r = minimize(_pen, X.ravel(), args=(N, d, t), jac=True, method="L-BFGS-B",
                     options={"maxiter": iters, "gtol": 1e-20, "ftol": 1e-30, "maxcor": 30})
        Xn = normalize(r.x.reshape(N, d))
        cn = maxcos(Xn)
        if cn < c:
            # accept whatever progress was made
            gain = c - cn
            X, c = Xn, cn
            if cn <= t + 1e-15:
                step *= 1.5
            else:
                step = max(min(step, gain) * 0.5, step * 0.25)
        else:
            step *= 0.25
    return X, c


def save(fn, X, c, d, N, table):
    with open(fn, "w") as fh:
        fh.write(f"# d={d} N={N} c_float={c:.17g} table={table}\n")
        for row in X:
            fh.write(" ".join(f"{v:.20e}" for v in row) + "\n")


def run(d, N, seconds, seed, outdir, table=None, nquick=None):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    best, bestc = None, 9.0
    nres = 0
    os.makedirs(outdir, exist_ok=True)
    fn = os.path.join(outdir, f"{d}_{N}.txt")
    while time.time() - t0 < seconds:
        X = normalize(rng.standard_normal((N, d)))
        X = coarse(X)
        # quick screen with a loose descent, full descent only if promising
        X, c = descend(X, minstep=1e-7, iters=500)
        nres += 1
        if best is not None and c > bestc + 1e-4:
            continue
        X, c = descend(X, step=1e-6, minstep=1e-14, iters=3000,
                       deadline=t0 + seconds + 60)
        if c < bestc:
            best, bestc = X, c
    prev = None
    if os.path.exists(fn):
        prev = maxcos(normalize(np.loadtxt(fn, comments="#")))
    if best is not None and (prev is None or bestc < prev):
        save(fn, best, bestc, d, N, table)
    fin = min(bestc, prev) if prev is not None else bestc
    diff = (float(table) - fin) if table else float("nan")
    print(f"{d} {N} run_best={bestc:.15f} file_best={fin:.15f} table={table} "
          f"restarts={nres} margin={diff:.3e}", flush=True)
    return bestc


if __name__ == "__main__":
    d, N, sec, seed = map(int, sys.argv[1:5])
    run(d, N, sec, seed, sys.argv[5], sys.argv[6] if len(sys.argv) > 6 else None)
