"""Seed families for N between 2d and 3d."""
import numpy as np


def random_seed(rng, d, N):
    return rng.standard_normal((N, d))


def cross_plus(rng, d, N, eps=0.05):
    """+-e_i (2d points) plus N-2d random points, then a small perturbation."""
    k = N - 2 * d
    E = np.vstack([np.eye(d), -np.eye(d)])
    if k < 0:
        E = E[rng.permutation(2 * d)[:N]]
        k = 0
    X = np.vstack([E, rng.standard_normal((k, d)) / np.sqrt(d)])
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    return X + eps * rng.standard_normal(X.shape) / np.sqrt(d)


def proj_cross(rng, d, N):
    """Cross-polytope in R^m (2m >= N) projected to a random d-dim subspace, N points kept."""
    m = (N + 1) // 2
    Q, _ = np.linalg.qr(rng.standard_normal((m, m)))
    P = Q[:, :d]  # rows: images of e_i
    X = np.vstack([P, -P])
    return X[rng.permutation(2 * m)[:N]]


def simplex_pair(rng, d, N):
    """Two random rotated copies of a regular simplex-like frame (2(d+1) points), extras random."""
    m = d + 1
    S = np.eye(m) - 1.0 / m
    U, s, Vt = np.linalg.svd(S)
    B = U[:, :d] * s[:d]  # m points in R^d, regular simplex
    B /= np.linalg.norm(B, axis=1, keepdims=True)
    Q, _ = np.linalg.qr(rng.standard_normal((d, d)))
    X = np.vstack([B, -B, (B @ Q)])
    if len(X) < N:
        X = np.vstack([X, rng.standard_normal((N - len(X), d))])
    return X[rng.permutation(len(X))[:N]]


SEEDS = {"rand": random_seed, "cross": cross_plus, "proj": proj_cross, "simp": simplex_pair}
