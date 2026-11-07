"""Riesz-energy start with rising exponent: E_s = sum_{i<j} |x_i - x_j|^{-s}."""
import numpy as np
from scipy.optimize import minimize


def _E(y, N, d, s):
    Y = y.reshape(N, d)
    nr = np.linalg.norm(Y, axis=1, keepdims=True)
    Z = Y / nr
    G = Z @ Z.T
    D2 = np.maximum(2.0 - 2.0 * G, 1e-12)
    np.fill_diagonal(D2, 1.0)
    # scale to avoid overflow: relative to the minimum distance
    m = D2[~np.eye(N, dtype=bool)].min()
    R = (D2 / m) ** (-s / 2.0)
    np.fill_diagonal(R, 0.0)
    E = R.sum() / 2.0
    # dE/dG_ij = (-s/2) * R / D2 * (-2)  = s R / D2
    W = s * R / D2
    np.fill_diagonal(W, 0.0)
    gZ = W @ Z
    gY = (gZ - Z * np.sum(gZ * Z, axis=1, keepdims=True)) / nr
    return np.log(E), (gY / E).ravel()


def riesz(X, exps=(2, 8, 32, 128, 512), iters=500):
    N, d = X.shape
    y = X.ravel()
    for s in exps:
        y = minimize(_E, y, args=(N, d, s), jac=True, method="L-BFGS-B",
                     options={"maxiter": iters, "gtol": 1e-12, "ftol": 1e-15}).x
        Y = y.reshape(N, d)
        y = (Y / np.linalg.norm(Y, axis=1, keepdims=True)).ravel()
    return y.reshape(N, d)
