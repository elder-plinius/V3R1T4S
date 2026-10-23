#!/usr/bin/env python3
"""Short active-set LP minimax polish of a spherical code (float64), crash-safe.
Usage: polish_650.py <in.txt> <outdir> <seconds>
Each LP step linearizes every pair within 3r of the current maximum, moves points by at most r per coordinate in
the tangent space, and minimizes the linearized maximum (scipy HiGHS). A step is kept only if the true float64
maximum drops. The best file is written atomically to <outdir>/polished_650.txt with a status JSON."""
import os, sys, time, json
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

def load(path):
    X = np.array([[float(t) for t in l.split(",")] for l in open(path) if l.strip()])
    return X / np.linalg.norm(X, axis=1, keepdims=True)

def gram_max(X):
    G = X @ X.T; np.fill_diagonal(G, -2.0); m = G.max()
    return G, m, int((np.triu(G, 1) >= m - 1e-10).sum())

def lp_step(X, G, m, r, maxpairs=10000):
    N, d = X.shape
    iu = np.triu_indices(N, 1); g = G[iu]
    sel = np.nonzero(g >= m - 3 * r)[0]
    if len(sel) > maxpairs: sel = sel[np.argsort(-g[sel])[:maxpairs]]
    I, J, gv = iu[0][sel], iu[1][sel], g[sel]
    P = len(sel); nv = N * d + 1
    rows = np.repeat(np.arange(P), 2 * d)
    cols = np.concatenate([(I[:, None] * d + np.arange(d)), (J[:, None] * d + np.arange(d))], 1).ravel()
    vals = np.concatenate([X[J], X[I]], 1).ravel()
    A = sp.csr_matrix((np.concatenate([vals, -np.ones(P)]),
                       (np.concatenate([rows, np.arange(P)]), np.concatenate([cols, np.full(P, nv - 1)]))), shape=(P, nv))
    b = -(gv - m) / r
    Aeq = sp.csr_matrix((X.ravel(), (np.repeat(np.arange(N), d), np.arange(N * d))), shape=(N, nv))
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=np.zeros(N), bounds=[(-1, 1)] * (N * d) + [(None, None)],
                  method="highs-ipm", options={"time_limit": 150.0})
    if res.status != 0: return None, P
    Y = X + r * res.x[:-1].reshape(N, d)
    return Y / np.linalg.norm(Y, axis=1, keepdims=True), P

def save(outdir, X, m, ties, base, it, t):
    tmp = os.path.join(outdir, "polished_650.txt.tmp")
    with open(tmp, "w") as f:
        for r in X: f.write(",".join("%.20e" % v for v in r) + "\n")
    os.replace(tmp, os.path.join(outdir, "polished_650.txt"))
    json.dump(dict(start=repr(base), best=repr(m), gain=repr(base - m), ties=ties, iterations=it, seconds=round(t, 1)),
              open(os.path.join(outdir, "polish_status.json"), "w"))

def main():
    src, outdir, tlimit = sys.argv[1], sys.argv[2], float(sys.argv[3])
    os.makedirs(outdir, exist_ok=True)
    X = load(src); G, m, ties = gram_max(X); base = m
    r = 1e-4; t0 = time.time(); it = 0
    print("start c=%r ties=%d" % (m, ties), flush=True)
    while time.time() - t0 < tlimit and r > 1e-16:
        it += 1
        Y, P = lp_step(X, G, m, r)
        if Y is None: r *= 0.3; continue
        G2, m2, t2 = gram_max(Y)
        print("it=%d r=%.1e pairs=%d c=%r ties=%d t=%.0f" % (it, r, P, m2, t2, time.time() - t0), flush=True)
        if m2 < m:
            X, G, m, ties = Y, G2, m2, t2; r = min(r * 2, 3e-2)
            save(outdir, X, m, ties, base, it, time.time() - t0)
        else:
            r *= 0.25
    print("DONE start=%r best=%r gain=%.6e ties=%d" % (base, m, base - m, ties), flush=True)

if __name__ == "__main__":
    main()
