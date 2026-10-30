"""SLP polish v2 (search only; the two checkers decide). Same step as slp_polish.py (tangent steps rad*y with
|y|_inf <= 1, linearised normalised inner products <= c + rad*s over the active pairs, minimise s, accept if the
true max cosine drops), with three changes aimed at codes whose first LP never finished under the old settings:
  - start radius rad0 and a ceiling radmax on the trust radius (the old code started at 1e-4 and grew to 1e-2);
  - the active set is the pairs within 4*rad of the max, capped at the K largest (K = kfac*N*d/2);
  - HiGHS method selectable (highs-ds dual simplex, highs-ipm interior point).
Usage: slp_v2.py in d N c_table out seconds rad0 radmax lp_limit kfac method
Prints the max cosine every 10 steps and a final "cell" line with LP counts (solved, capped/failed)."""
import sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

def normalize(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)

def maxcos(X):
    G = X @ X.T
    np.fill_diagonal(G, -2.0)
    return G.max()

inp, d, N, ctab, out, secs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], float(sys.argv[6])
rad0, radmax, lplim, kfac, method = float(sys.argv[7]), float(sys.argv[8]), float(sys.argv[9]), float(sys.argv[10]), sys.argv[11]
X = normalize(np.array([[float(x) for x in l.replace(",", " ").split()] for l in open(inp) if l.strip()]))
c = maxcos(X); c0 = c
K = max(int(kfac * N * d / 2), 10)
rad, t0, it, nsolved, nfail, nacc = rad0, time.time(), 0, 0, 0, 0
while rad > 1e-15 and time.time() - t0 < secs:
    it += 1
    G = X @ X.T
    np.fill_diagonal(G, -2.0)
    I, J = np.nonzero(np.triu(G > c - max(4 * rad, 1e-12), 1))
    if len(I) > K:
        keep = np.argsort(-G[I, J])[:K]
        I, J = I[keep], J[keep]
    m = len(I)
    nv = N * d + 1
    rows = np.repeat(np.arange(m), 2 * d + 1)
    cols = np.hstack([J[:, None] * d + np.arange(d), I[:, None] * d + np.arange(d), np.full((m, 1), N * d)]).ravel()
    vals = np.hstack([X[I], X[J], -np.ones((m, 1))]).ravel()
    A = coo_matrix((vals, (rows, cols)), shape=(m, nv)).tocsr()
    Aeq = coo_matrix((X.ravel(), (np.repeat(np.arange(N), d), np.arange(N * d))), shape=(N, nv)).tocsr()
    obj = np.zeros(nv); obj[-1] = 1.0
    res = linprog(obj, A_ub=A, b_ub=(c - G[I, J]) / rad, A_eq=Aeq, b_eq=np.zeros(N),
                  bounds=[(-1.0, 1.0)] * (N * d) + [(-10.0, 10.0)], method=method, options={"time_limit": lplim})
    if res.x is None:
        nfail += 1
        rad /= 3
        continue
    nsolved += 1
    Xn = normalize(X + rad * res.x[:-1].reshape(N, d))
    cn = maxcos(Xn)
    if cn < c:
        X, c = Xn, cn
        nacc += 1
        rad = min(rad * 2, radmax)
    else:
        rad /= 3
    if it % 10 == 0:
        print("step %d rad %.1e active %d max cos %.16f gain_vs_table %.3e t %.0f" % (it, rad, m, c, ctab - c, time.time() - t0), flush=True)
with open(out, "w") as f:
    for p in X:
        f.write(" ".join("%.25e" % x for x in p) + "\n")
print("cell (%d,%d) start %.16f final %.16f table %.12f gain_vs_table %.3e steps %d lp_solved %d lp_failed %d accepted %d t %.0f"
      % (d, N, c0, c, ctab, ctab - c, it, nsolved, nfail, nacc, time.time() - t0))
