"""Step 5 self-break check, independent of tools/ljfast.py and of the dry-run checker's Hessian code.

Reads a coordinate file, computes the gradient with a plain pair loop, builds the Hessian by central finite
differences of that gradient, takes its eigenvalues, and recomputes E_sp. Then it probes the minimum: 2000 random
displacements of size 1e-3 must all raise E_LJ (a necessary sign of a local minimum, given zero modes aside).
Usage: python -I selfcheck.py COORDS BAR_NE
"""
import sys, math, random
import numpy as np


def read(path):
    pts = []
    for line in open(path):
        t = line.split()
        if len(t) >= 3:
            try:
                pts.append([float(v.replace("D", "e").replace("d", "e")) for v in t[-3:]])
            except ValueError:
                pass
    return np.array(pts)


def e_and_g(x):
    n = len(x); e = 0.0; g = np.zeros_like(x)
    for i in range(n):
        for j in range(i + 1, n):
            d = x[i] - x[j]; r2 = float(d @ d); s6 = 1.0 / r2 ** 3
            e += 4.0 * (s6 * s6 - s6)
            dvdr_over_r = (-48.0 * s6 * s6 + 24.0 * s6) / r2
            g[i] += dvdr_over_r * d; g[j] -= dvdr_over_r * d
    return e, g


x = read(sys.argv[1]); bar = float(sys.argv[2]); n = len(x)
e, g = e_and_g(x)
print("N = %d, E_LJ = %.10f, |grad| = %.3e" % (n, e, np.sqrt((g * g).sum())))
h = 1e-5
H = np.zeros((3 * n, 3 * n))
for k in range(3 * n):
    a = x.copy().ravel(); a[k] += h
    b = x.copy().ravel(); b[k] -= h
    H[:, k] = (e_and_g(a.reshape(-1, 3))[1].ravel() - e_and_g(b.reshape(-1, 3))[1].ravel()) / (2 * h)
H = 0.5 * (H + H.T)
lam = np.sort(np.linalg.eigvalsh(H))
idx = np.argsort(np.abs(lam))
zero, nz = lam[idx[:6]], lam[idx[6:]]
print("six smallest |lambda| (finite-difference Hessian): " + " ".join("%.1e" % v for v in sorted(zero)))
print("lowest nonzero eigenvalue: %.6f ; negative nonzero eigenvalues: %d" % (nz.min(), int((nz < 0).sum())))
s = float(np.sqrt(nz).sum())
for sp, q in (("Xe", 0.01), ("Ar", 0.03), ("Ne", 0.095)):
    print("E_%s = %.6f" % (sp, e + 0.5 * q * s))
ene = e + 0.5 * 0.095 * s
print("bar_Ne - E_Ne = %.6f (need >= 5e-4)" % (bar - ene))
random.seed(1)
rises = 0
for t in range(2000):
    dx = np.array([[random.gauss(0, 1) for _ in range(3)] for _ in range(n)])
    dx -= dx.mean(0)
    dx *= 1e-3 / np.sqrt((dx * dx).sum())
    if e_and_g(x + dx)[0] > e:
        rises += 1
print("random 1e-3 displacements that raise E_LJ: %d / 2000" % rises)
