"""Checker self-test from the definition (paper eq. 2): the pinball form used in p3_reproduce.py equals the interval form
1/(2N+1) * (|y - m| + sum_k alpha_k * IS_alpha_k), N = 3, alpha = 0.5, 0.2, 0.05; known positive (point forecast ->
WIS = |y - m|), known negative (a 1/(N+1) normalisation differs)."""
import numpy as np
TAU = np.array([0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975])
def wis_pinball(Q, y):
    y = np.asarray(y, float)[:, None]
    return np.mean(2 * ((y < Q).astype(float) - TAU[None, :]) * (Q - y), axis=1)
def wis_interval(Q, y):
    y = np.asarray(y, float); tot = np.abs(y - Q[:, 3])
    for k, a in enumerate([0.05, 0.2, 0.5]):
        l, u = Q[:, k], Q[:, 6 - k]
        IS = (u - l) + 2 / a * (l - y) * (y < l) + 2 / a * (y - u) * (y > u)
        tot = tot + a * IS
    return tot / 7.0
rng = np.random.default_rng(7)
Q = np.sort(rng.normal(100, 20, (5000, 7)), axis=1); y = rng.normal(100, 35, 5000)
d = np.max(np.abs(wis_pinball(Q, y) - wis_interval(Q, y)))
P = np.full((3, 7), 50.0); yy = np.array([40.0, 50.0, 80.0])
pos = np.allclose(wis_pinball(P, yy), np.abs(yy - 50))
neg = np.max(np.abs(wis_pinball(Q, y) * 7 / 4 - wis_interval(Q, y))) > 1e-6
print("max |pinball - interval| =", d); print("known positive (point forecast WIS = |y-m|):", pos)
print("known negative (wrong normalisation differs):", neg)
print("SELFTEST", "PASS" if (d < 1e-9 and pos and neg) else "FAIL")
