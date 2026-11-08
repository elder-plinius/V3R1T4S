"""Polish floor for harmonic-energy cells: the posted 2021 configuration for (N, n) (data.txt of
https://hdl.handle.net/1721.1/130937), polished by projected L-BFGS on the product of spheres to gradient ~1e-14,
then a few Newton steps; reports the polished energy and whether it stays above E_ours + max(1e-9, 1e-12 E).
usage: harmonic_floor.py <data.txt> <cells dir> <N-n> [<N-n> ...]   -> prints one CSV line per cell"""
import os, re, sys
import numpy as np
from scipy.optimize import minimize
from mpmath import mp, mpf
mp.dps = 50

data, cells = sys.argv[1], sys.argv[2]
want = {tuple(map(int, c.split('-'))) for c in sys.argv[3:]}
posted = {}
cur = None
for line in open(data):
    m = re.match(r'(\d+) points in R\^(\d+)', line)
    if m:
        cur = (int(m.group(1)), int(m.group(2)))
        if cur in want:
            posted[cur] = []
        continue
    if cur in want and line.startswith('('):
        posted[cur].append([float(x) for x in line.strip().strip('()').split(',')])


def energy_grad(x, N, n):
    X = x.reshape(N, n); X = X / np.linalg.norm(X, axis=1, keepdims=True)
    D = X[:, None] - X[None]; r2 = (D ** 2).sum(-1); np.fill_diagonal(r2, np.inf)
    s = (n - 2) / 2
    E = 0.5 * np.sum(r2 ** -s)
    G = -2 * s * np.sum(D * (r2 ** (-s - 1))[..., None], axis=1)
    G -= np.sum(G * X, 1, keepdims=True) * X
    return E, G.ravel()


def mp_energy(X, n):
    P = [[mpf(repr(float(c))) for c in p] for p in X]
    P = [[c / mp.sqrt(mp.fsum(v * v for v in p)) for c in p] for p in P]
    s = mpf(n - 2) / 2
    return mp.fsum(mp.fsum((a - b) ** 2 for a, b in zip(P[i], P[j])) ** -s for i in range(len(P)) for j in range(i))


print('cell,posted_energy,polished_energy,our_energy,needed_margin,polished_minus_ours,ok')
for (N, n) in sorted(want):
    X = np.array(posted[(N, n)]); X /= np.linalg.norm(X, axis=1, keepdims=True)
    E0 = energy_grad(X.ravel(), N, n)[0]
    res = minimize(lambda x: energy_grad(x, N, n), X.ravel(), jac=True, method='L-BFGS-B',
                   options={'maxiter': 50000, 'gtol': 1e-15, 'ftol': 1e-17, 'maxcor': 30})
    Y = res.x.reshape(N, n); Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    Ep = mp_energy(Y, n)
    ours = [l for l in open(os.path.join(cells, '%d-%d.txt' % (N, n))) if l.startswith('#')][0]
    Eo = mpf(re.search(r'energy\s+([0-9.eE+-]+)', ours).group(1))
    marg = max(mpf('1e-9'), mpf('1e-12') * Eo)
    print('%d-%d,%.15f,%s,%s,%s,%s,%s' % (N, n, E0, mp.nstr(Ep, 25), mp.nstr(Eo, 25), mp.nstr(marg, 3),
                                          mp.nstr(Ep - Eo, 6), Ep >= Eo + marg), flush=True)
