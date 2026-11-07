"""Exact-objective polish by sequential linear programming (search only; the two checkers decide).
At each step: active pairs (cosine within 4*rad of the max), tangent steps rad*y with |y|_inf <= 1, linearised
normalised inner products <= c + rad*s, minimise s (HiGHS); accept if the true max cosine drops, else shrink rad.
Usage: slp_polish.py infile d N table_cos outfile seconds
Prints the max cosine every 10 steps and at the end; writes the best code with 25 significant digits."""
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
X = normalize(np.array([[float(x) for x in l.replace(",", " ").split()] for l in open(inp) if l.strip()]))
c = maxcos(X); c0 = c
rad, t0, it = 1e-4, time.time(), 0
while rad > 1e-15 and time.time() - t0 < secs:
    it += 1
    G = X @ X.T
    np.fill_diagonal(G, -2.0)
    I, J = np.nonzero(np.triu(G > c - max(4 * rad, 1e-12), 1))
    m = len(I)
    nv = N * d + 1
    # d<x_i,x_j> for unit vectors moved in the tangent space: <x_i, y_j> + <y_i, x_j> (y_i orthogonal to x_i)
    rows = np.repeat(np.arange(m), 2 * d + 1)
    cols = np.hstack([J[:, None] * d + np.arange(d), I[:, None] * d + np.arange(d), np.full((m, 1), N * d)]).ravel()
    vals = np.hstack([X[I], X[J], -np.ones((m, 1))]).ravel()
    A = coo_matrix((vals, (rows, cols)), shape=(m, nv)).tocsr()
    Aeq = coo_matrix((X.ravel(), (np.repeat(np.arange(N), d), np.arange(N * d))), shape=(N, nv)).tocsr()
    obj = np.zeros(nv); obj[-1] = 1.0
    res = linprog(obj, A_ub=A, b_ub=(c - G[I, J]) / rad, A_eq=Aeq, b_eq=np.zeros(N),
                  bounds=[(-1.0, 1.0)] * (N * d) + [(-10.0, 10.0)], method="highs", options={"time_limit": 20.0})
    if res.x is None:
        rad /= 3
        continue
    Xn = normalize(X + rad * res.x[:-1].reshape(N, d))
    cn = maxcos(Xn)
    if cn < c:
        X, c = Xn, cn
        rad = min(rad * 2, 1e-2)
    else:
        rad /= 3
    if it % 10 == 0:
        print("step %d rad %.1e active %d max cos %.16f gain_vs_table %.3e t %.0f" % (it, rad, m, c, ctab - c, time.time() - t0), flush=True)
with open(out, "w") as f:
    for p in X:
        f.write(" ".join("%.25e" % x for x in p) + "\n")
print("cell (%d,%d) start %.16f final %.16f table %.12f gain_vs_table %.3e steps %d" % (d, N, c0, c, ctab, ctab - c, it))
