import numpy as np, itertools
from core import relax
def d4_points(R=4):
    g = np.array(list(itertools.product(range(-R, R + 1), repeat=4)), float)
    return g[(g.sum(1) % 2) == 0]
def a4_points(R=4):
    # A4 in R^5 (sum zero) projected to an orthonormal basis of the hyperplane
    g = np.array(list(itertools.product(range(-R, R + 1), repeat=5)), float)
    g = g[g.sum(1) == 0]
    B = np.linalg.qr(np.vstack([np.ones(5), np.eye(5)[:4]]).T)[0][:, 1:5]
    return g @ B
D4 = d4_points(); A4 = a4_points(3)
def lattice_cut(L, N, c, rng, jitter=0.0):
    d = np.linalg.norm(L - c, axis=1)
    idx = np.argsort(d + rng.random(len(d)) * jitter)[:N]
    P = L[idx] - c
    # random rotation
    Q = np.linalg.qr(rng.normal(size=(4, 4)))[0]
    P = P @ Q
    return P / (np.linalg.norm(P, axis=1).max() + 0.7)
