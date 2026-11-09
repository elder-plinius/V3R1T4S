#!/usr/bin/env python3
"""H10 falsify-first: numerical sanity check of the frozen spec's map
   x = (h, g, a) in SU(3) x SU(2) x U(1)  |->  M(x) = blockdiag(a^3 g, a^-2 h)   (2x2 block first)
 - M(x) unitary, det M(x) = 1, M(xy) = M(x) M(y) (componentwise product) on random elements;
 - the six elements gaugeGroupZ6OfRoot(alpha) = (alpha^2 I3, conj(alpha)^3 I2, alpha), alpha^6 = 1, map to I5;
 - conversely M(x) = I5 forces g = a^-3 I2, h = a^2 I3, and these lie in SU(2) x SU(3) iff a^6 = 1:
   scan a over a fine grid of the circle and count where det conditions hold.
"""
import numpy as np

rng = np.random.default_rng(20261014)


def rand_su(n):
    z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    q = q @ np.diag(np.diag(r) / np.abs(np.diag(r)))
    d = np.linalg.det(q)
    return q / d ** (1.0 / n)          # det becomes 1 (principal n-th root of det)


def rand_u1():
    return np.exp(1j * rng.uniform(0, 2 * np.pi))


def M(x):
    h, g, a = x
    out = np.zeros((5, 5), dtype=complex)
    out[:2, :2] = a ** 3 * g
    out[2:, 2:] = a ** -2 * h
    return out


def mul(x, y):
    return (x[0] @ y[0], x[1] @ y[1], x[2] * y[2])


worst = {"unitary": 0.0, "det": 0.0, "hom": 0.0, "su_in": 0.0}
for _ in range(2000):
    x = (rand_su(3), rand_su(2), rand_u1())
    y = (rand_su(3), rand_su(2), rand_u1())
    worst["su_in"] = max(worst["su_in"], abs(np.linalg.det(x[0]) - 1), abs(np.linalg.det(x[1]) - 1))
    m = M(x)
    worst["unitary"] = max(worst["unitary"], np.abs(m @ m.conj().T - np.eye(5)).max())
    worst["det"] = max(worst["det"], abs(np.linalg.det(m) - 1))
    worst["hom"] = max(worst["hom"], np.abs(M(mul(x, y)) - M(x) @ M(y)).max())
print("random checks (2000 pairs), worst errors:", {k: float("%.3g" % v) for k, v in worst.items()})

print("sixth roots: alpha, ||M(gaugeGroupZ6OfRoot alpha) - I||_max, det(alpha^2 I3), det(conj(alpha)^3 I2)")
for k in range(6):
    al = np.exp(2j * np.pi * k / 6)
    x = (al ** 2 * np.eye(3), np.conj(al) ** 3 * np.eye(2), al)
    print("  k=%d  %.3g  %.3g  %.3g" % (k, np.abs(M(x) - np.eye(5)).max(),
                                       abs(np.linalg.det(x[0]) - 1), abs(np.linalg.det(x[1]) - 1)))

# converse: M(x) = I forces g = a^-3 I2, h = a^2 I3; which a on a fine grid give det g = det h = 1?
N = 600000
hits = []
for j in range(N):
    a = np.exp(2j * np.pi * j / N)
    if abs(a ** -6 - 1) < 1e-9 and abs(a ** 6 - 1) < 1e-9:     # det(a^-3 I2) = a^-6, det(a^2 I3) = a^6
        hits.append(j)
print("grid points (N=%d) where the forced kernel candidate lies in SU(3)xSU(2):" % N, hits,
      "-> angles/(2pi) =", [h / N for h in hits])

# random non-identity elements are not in the kernel (smoke test)
nonid = sum(np.abs(M((rand_su(3), rand_su(2), rand_u1())) - np.eye(5)).max() < 1e-6 for _ in range(1000))
print("random elements mapping to I5 (expect 0):", int(nonid))
