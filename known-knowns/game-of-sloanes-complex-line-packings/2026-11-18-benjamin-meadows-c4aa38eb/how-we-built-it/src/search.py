"""Lane sloanes: search for low-coherence packings of n lines in C^d.

Pipeline per restart:
  1. smoothed-max descent: L-BFGS on log-sum-exp of squared overlaps |<y_j,y_k>|^2
     of the normalised columns, with the sharpness p raised in stages;
  2. (some restarts) alternating projection onto the Gram constraints
     {|G_jk| <= mu, G_jj = 1} and {PSD, rank <= d};
  3. active-set polish: sequential linear programming on the near-maximal overlaps
     (minimise t subject to linearised |G_jk|^2 <= t, box trust region).
Writes the best packing found to out/<d>x<n>.txt in the Game of Sloanes layout.
"""
import json, os, sys, time
import numpy as np
from scipy.optimize import minimize, linprog
from scipy.sparse import coo_matrix

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def normalise(X):
    return X / np.linalg.norm(X, axis=0, keepdims=True)


def coherence(X):
    Y = normalise(X)
    G = np.abs(Y.conj().T @ Y)
    np.fill_diagonal(G, 0)
    return G.max()


def lse_obj(v, d, n, p):
    X = (v[: d * n] + 1j * v[d * n:]).reshape(d, n)
    nrm = np.linalg.norm(X, axis=0)
    Y = X / nrm
    G = Y.conj().T @ Y
    S = (G.real ** 2 + G.imag ** 2)
    np.fill_diagonal(S, -np.inf)
    m = S.max()
    E = np.exp(p * (S - m))
    Z = E.sum()
    f = m + np.log(Z) / p
    W = E / Z  # symmetric, zero diagonal
    gY = 2 * Y @ (W * G)  # column k: 2*sum_j W_jk G_jk y_j
    # Through normalisation: project out radial part, divide by norm
    gX = (gY - Y * np.real(np.sum(Y.conj() * gY, axis=0))) / nrm
    return f, np.concatenate([gX.real.ravel(), gX.imag.ravel()])


def descend(X, ps=(30, 100, 300, 1000, 3000, 1e4, 3e4), iters=400):
    d, n = X.shape
    for p in ps:
        v = np.concatenate([X.real.ravel(), X.imag.ravel()])
        r = minimize(lse_obj, v, args=(d, n, p), jac=True, method="L-BFGS-B",
                     options=dict(maxiter=iters, gtol=1e-12, ftol=1e-15))
        X = normalise((r.x[: d * n] + 1j * r.x[d * n:]).reshape(d, n))
    return X


def altproj(X, mu, iters=200):
    d, n = X.shape
    Y = normalise(X)
    for _ in range(iters):
        G = Y.conj().T @ Y
        a = np.abs(G)
        scale = np.where(a > mu, mu / np.maximum(a, 1e-300), 1.0)
        G = G * scale
        np.fill_diagonal(G, 1.0)
        w, V = np.linalg.eigh(G)
        w = np.clip(w[-d:], 0, None)
        Y = normalise((V[:, -d:] * np.sqrt(w)).conj().T)
    return Y


def polish(X, rounds=200, tol_act=None, r0=1e-2, tmax=None):
    """Sequential LP on squared overlaps with a box trust region."""
    d, n = X.shape
    tstart = time.time()
    if tmax is None:
        tmax = 5 + 0.01 * d * n
    stall = 0
    Y = normalise(X)
    iu = np.triu_indices(n, 1)
    best = coherence(Y) ** 2
    r = r0
    for _ in range(rounds):
        if time.time() - tstart > tmax or stall > 25:
            break
        G = Y.conj().T @ Y
        S = np.abs(G) ** 2
        s = S[iu]
        m = s.max()
        thr = m - max(10 * r * 4, 1e-6) if tol_act is None else m - tol_act
        idx = np.nonzero(s >= thr)[0]
        J, K = iu[0][idx], iu[1][idx]
        nc = len(idx)
        # variables: dRe (d*n), dIm (d*n), t. Perturbation of y_k: dy_k.
        # dS_jk = 2 Re( conj(G_jk) * (dy_j^H y_k + y_j^H dy_k) )
        #       = 2 Re( conj(G_jk) conj(dy_j)^T y_k ) + 2 Re( conj(G_jk) y_j^H dy_k )
        # coefficient vectors: for dy_k: c = conj(G_jk) * conj(y_j)  -> 2Re(c.dy_k)
        #                      for dy_j: c' = G_jk * conj(y_k)       -> 2Re(c'.dy_j)
        nv = 2 * d * n + 1
        g = G[J, K]
        ck = (np.conj(g)[:, None] * np.conj(Y[:, J]).T)  # nc x d, coefficient on dy_k
        cj = (g[:, None] * np.conj(Y[:, K]).T)            # nc x d, coefficient on dy_j
        ar = np.arange(d)[None, :] * n
        R = np.repeat(np.arange(nc), d)
        rows = np.concatenate([R, R, R, R, np.arange(nc)])
        cols = np.concatenate([(ar + K[:, None]).ravel(), (ar + K[:, None]).ravel() + d * n,
                               (ar + J[:, None]).ravel(), (ar + J[:, None]).ravel() + d * n,
                               np.full(nc, nv - 1)])
        vals = np.concatenate([2 * ck.real.ravel(), -2 * ck.imag.ravel(),
                               2 * cj.real.ravel(), -2 * cj.imag.ravel(), -np.ones(nc)])
        A = coo_matrix((vals, (rows, cols)), shape=(nc, nv)).tocsr()
        b = -s[idx]
        er = np.repeat(np.arange(n), d)
        ec = (np.arange(d)[None, :] * n + np.arange(n)[:, None]).ravel()
        Aeq = coo_matrix((np.concatenate([Y.T.real.ravel(), Y.T.imag.ravel()]),
                          (np.concatenate([er, er]), np.concatenate([ec, ec + d * n]))),
                         shape=(n, nv)).tocsr()
        cost = np.zeros(nv); cost[-1] = 1
        bounds = [(-r, r)] * (2 * d * n) + [(None, None)]
        res = linprog(cost, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=np.zeros(n), bounds=bounds, method="highs",
                      options=dict(time_limit=max(1.0, 0.005 * d * n)))
        if res.status != 0:
            r *= 0.5
            if r < 1e-12:
                break
            continue
        dx = res.x[:-1]
        Yn = normalise(Y + (dx[: d * n] + 1j * dx[d * n:]).reshape(d, n))
        new = coherence(Yn) ** 2
        stall = stall + 1 if new > best - 1e-13 else 0
        if new < best - 1e-16:
            pred = m - res.x[-1]
            Y, best = Yn, new
            if pred > 0 and (m - new) > 0.5 * pred:
                r = min(r * 2, 0.05)
        else:
            r *= 0.3
            if r < 1e-12:
                break
    return Y


def random_start(d, n, rng):
    return normalise(rng.standard_normal((d, n)) + 1j * rng.standard_normal((d, n)))


def save(path, X, mu):
    Y = normalise(X)
    d, n = Y.shape
    with open(path, "w") as f:
        for k in range(n):
            for i in range(d):
                f.write(f"{Y[i, k].real:.20e}\n")
        for k in range(n):
            for i in range(d):
                f.write(f"{Y[i, k].imag:.20e}\n")


def run_cell(d, n, table, budget, seed=0, npolish=3):
    rng = np.random.default_rng(seed + 1000 * d + n)
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    pool, tries = [], 0
    while time.time() - t0 < 0.6 * budget:
        X = descend(random_start(d, n, rng))
        mu = coherence(X)
        if tries % 4 == 3:
            X2 = descend(altproj(X, mu * 0.99), ps=(1e3, 1e4, 3e4))
            m2 = coherence(X2)
            if m2 < mu:
                X, mu = X2, m2
        tries += 1
        pool.append((mu, X))
        pool.sort(key=lambda t: t[0])
        pool = pool[:npolish]
    best, bestX = np.inf, None
    for mu, X in pool:
        if time.time() - t0 > budget and bestX is not None:
            break
        Xp = polish(X, rounds=300)
        mp = coherence(Xp)
        if mp < best:
            best, bestX = mp, Xp
    bestX = polish(bestX, rounds=300, r0=1e-4, tmax=10 + 0.02 * d * n)
    best = coherence(bestX)
    path = os.path.join(OUT, f"{d}x{n}.txt")
    prev = None
    if os.path.exists(path):
        v = np.loadtxt(path)
        prev = coherence((v[: d * n].reshape(n, d) + 1j * v[d * n:].reshape(n, d)).T)
    if prev is None or best < prev:
        save(path, bestX, best)
    else:
        best = prev
    return dict(d=d, n=n, table=table, best=float(best), tries=tries,
                time=round(time.time() - t0, 1), gap=float(best - table))


if __name__ == "__main__":
    d, n, table, budget = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    print(json.dumps(run_cell(d, n, table, budget, seed)))
