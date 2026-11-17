#!/usr/bin/env python3
"""Falsify-first numeric check of PatiSalam.inclSM_ker under the frozen spec's conventions.

x = (h, g, a) in SU(3) x SU(2) x U(1);  f(x) = (blockdiag(a h, a^-3), g, diag(a^3, a^-3)).
Physlib's Z3 subgroup: gaugeGroupZ3OfRoot b = gaugeGroupZ6OfRoot (incl b) = (b^2 1_3, conj(b)^3 1_2, b), b^3 = 1.
Physlib's Z6 subgroup: (z^2 1_3, conj(z)^3 1_2, z), z^6 = 1.

Checks:
 1. f lands in SU(4) x SU(2) x SU(2) (unitary, det 1) on random inputs.
 2. f is multiplicative on random pairs.
 3. f kills every Z3 element; for Z6 elements, f(x) = 1 exactly when z^3 = 1.
 4. Kernel solve: f(x) = 1 forces g = 1, a^3 = 1 (entry (3,3) / third component), h = a^-1 1_3.
    For a on a fine grid of the circle, the candidate h = a^-1 1_3 lies in SU(3) iff a^3 = 1; then x equals the
    Z3 element with b = a (b^2 = b^-1). Count kernel elements found this way and compare with the Z3 set.
 5. Perturbation probe: random small perturbations of kernel / Z6 elements keep ||f(x) - 1|| > 0 unless the
    perturbation is zero (no extra kernel near the Z6 points).
 6. Convention contrast: with the WRONG reading b 1_3 (instead of b^2 1_3) the Z3 set is not killed (shows the
    test can fail).
Deterministic seed. Prints a summary line `NUMERIC: ...`.
"""
import numpy as np

rng = np.random.default_rng(20261014)
TOL = 1e-10


def haar_unitary(n):
    z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    return q * (d / np.abs(d))


def haar_special_unitary(n):
    u = haar_unitary(n)
    det = np.linalg.det(u)
    return u / det ** (1.0 / n)


def rand_x():
    h = haar_special_unitary(3)
    g = haar_special_unitary(2)
    a = np.exp(1j * rng.uniform(0, 2 * np.pi))
    return h, g, a


def f(x):
    h, g, a = x
    m4 = np.zeros((4, 4), dtype=complex)
    m4[:3, :3] = a * h
    m4[3, 3] = (1 / a) ** 3
    mr = np.diag([a ** 3, (1 / a) ** 3])
    return m4, g, mr


def mul(x, y):
    return x[0] @ y[0], x[1] @ y[1], x[2] * y[2]


def dist_to_one(fx):
    m4, g, mr = fx
    return max(np.abs(m4 - np.eye(4)).max(), np.abs(g - np.eye(2)).max(), np.abs(mr - np.eye(2)).max())


def is_su(m):
    n = m.shape[0]
    return np.abs(m.conj().T @ m - np.eye(n)).max() < 1e-9 and abs(np.linalg.det(m) - 1) < 1e-9


def z6_elem(z, wrong=False):
    h = (z if wrong else z ** 2) * np.eye(3)
    g = np.conj(z) ** 3 * np.eye(2)
    return h, g, z


def main():
    fails = 0
    # 1, 2
    n_rand = 2000
    in_su = 0
    hom_ok = 0
    for _ in range(n_rand):
        x, y = rand_x(), rand_x()
        fx = f(x)
        if is_su(fx[0]) and is_su(fx[1]) and is_su(fx[2]):
            in_su += 1
        fxy = f(mul(x, y))
        fxfy = mul(f(x), f(y))
        if max(np.abs(fxy[0] - fxfy[0]).max(), np.abs(fxy[1] - fxfy[1]).max(), np.abs(fxy[2] - fxfy[2]).max()) < 1e-9:
            hom_ok += 1
    print("1. f(x) in SU(4)xSU(2)xSU(2): %d/%d random x" % (in_su, n_rand))
    print("2. f(xy) = f(x)f(y): %d/%d random pairs" % (hom_ok, n_rand))
    fails += (in_su != n_rand) + (hom_ok != n_rand)

    # 3
    cube = [np.exp(2j * np.pi * k / 3) for k in range(3)]
    sixth = [np.exp(2j * np.pi * k / 6) for k in range(6)]
    z3_killed = sum(dist_to_one(f(z6_elem(b))) < TOL for b in cube)
    print("3a. Z3 elements with f = 1: %d/3" % z3_killed)
    rows = []
    for k, z in enumerate(sixth):
        d = dist_to_one(f(z6_elem(z)))
        rows.append((k, abs(z ** 3 - 1) < TOL, d < TOL))
    print("3b. Z6 elements (k, z^3=1, f=1): %s" % rows)
    fails += (z3_killed != 3) + sum(r[1] != r[2] for r in rows)

    # 4: kernel solve on a grid of the circle
    N = 3 * 200000
    found = []
    for k in range(N):
        a = np.exp(2j * np.pi * k / N)
        h = (1 / a) * np.eye(3)  # forced by a h = 1_3
        if abs(np.linalg.det(h) - 1) < 1e-9 and abs(a ** 3 - 1) < 1e-9:
            x = (h, np.eye(2), a)
            if dist_to_one(f(x)) < TOL:
                found.append(a)
    match = 0
    for a in found:
        zx = z6_elem(a)
        if np.abs(zx[0] - (1 / a) * np.eye(3)).max() < TOL and np.abs(zx[1] - np.eye(2)).max() < TOL:
            match += 1
    print("4. grid of %d points on U(1): kernel elements found = %d, equal to the Z3 element with b = a: %d"
          % (N, len(found), match))
    fails += (len(found) != 3) + (match != 3)

    # 5: perturbation probe around Z6 points (and random points): f(x) = 1 only at the exact Z3 points
    min_d = []
    for z in sixth:
        base = z6_elem(z)
        ds = []
        for _ in range(200):
            eps = 10 ** rng.uniform(-6, -2)
            # small SU(3) perturbation: exp(i eps H) approximated via eigen-decomposition of a random Hermitian
            H = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
            H = (H + H.conj().T) / 2
            H -= np.trace(H) / 3 * np.eye(3)
            w, v = np.linalg.eigh(H)
            U = v @ np.diag(np.exp(1j * eps * w)) @ v.conj().T
            x = (base[0] @ U, base[1], base[2] * np.exp(1j * eps * rng.normal()))
            ds.append(dist_to_one(f(x)))
        min_d.append(min(ds))
    print("5. min ||f(x)-1|| over perturbed Z6 points (eps in [1e-6,1e-2]): %s"
          % ["%.2e" % d for d in min_d])
    fails += sum(d < TOL for d in min_d)

    # 6: wrong convention contrast (should NOT be killed for b != 1)
    wrong_killed = sum(dist_to_one(f(z6_elem(b, wrong=True))) < TOL for b in cube)
    print("6. contrast: with h = b 1_3 (wrong reading) f = 1 for %d/3 cube roots (expect 1: only b = 1)" % wrong_killed)
    fails += (wrong_killed != 1)

    print("NUMERIC: %s (failures=%d)" % ("CONSISTENT with kernel = Z3" if fails == 0 else "INCONSISTENT", fails))


if __name__ == "__main__":
    main()
