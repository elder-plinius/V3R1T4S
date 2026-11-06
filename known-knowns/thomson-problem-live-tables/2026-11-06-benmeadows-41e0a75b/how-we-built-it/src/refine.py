"""Refine Thomson configurations: projected L-BFGS then tangent-space Newton in float64, then report the energy in
mpmath (30 digits) and the smallest tangent-space Hessian eigenvalue (local-minimum check). Writes <N>_refined.txt."""
import sys, numpy as np
from scipy.optimize import minimize
from mpmath import mp, mpf, sqrt, fsum
mp.dps = 30

def energy_grad(x, N):
    X = x.reshape(N, 3); X = X / np.linalg.norm(X, axis=1, keepdims=True)
    D = X[:, None, :] - X[None, :, :]; r = np.linalg.norm(D, axis=2); np.fill_diagonal(r, np.inf)
    E = 0.5 * np.sum(1.0 / r)
    G = -np.sum(D / r[..., None] ** 3, axis=1)
    G -= np.sum(G * X, axis=1, keepdims=True) * X      # project onto the tangent space
    return E, G.ravel()

def mp_energy(X):
    P = [[mpf(repr(float(c))) for c in p] for p in X]
    P = [[c / sqrt(fsum(v * v for v in p)) for c in p] for p in P]
    return fsum(1 / sqrt(fsum((a - b) ** 2 for a, b in zip(P[i], P[j]))) for i in range(len(P)) for j in range(i))

def hessian_min_eig(X):
    N = len(X); D = X[:, None, :] - X[None, :, :]; r = np.linalg.norm(D, axis=2); np.fill_diagonal(r, np.inf)
    H = np.zeros((3 * N, 3 * N))
    for i in range(N):
        d = D[i]; ri = r[i]
        blk = (3 * d[:, :, None] * d[:, None, :] / ri[:, None, None] ** 5) - np.eye(3)[None] / ri[:, None, None] ** 3
        blk[i] = 0
        for j in range(N):
            if j != i: H[3*i:3*i+3, 3*j:3*j+3] = -blk[j]
        H[3*i:3*i+3, 3*i:3*i+3] = blk.sum(0)
    # tangent basis per point; radial-force correction for the sphere constraint
    B = np.zeros((3 * N, 2 * N)); F = -np.sum(-(D / r[..., None] ** 3), axis=1)
    for i in range(N):
        n = X[i]; a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
        t1 = np.cross(n, a); t1 /= np.linalg.norm(t1); t2 = np.cross(n, t1)
        B[3*i:3*i+3, 2*i] = t1; B[3*i:3*i+3, 2*i+1] = t2
        H[3*i:3*i+3, 3*i:3*i+3] += np.dot(F[i], n) * np.eye(3)
    Ht = B.T @ H @ B
    w = np.linalg.eigvalsh(Ht)
    return w[:6], w[6]                                   # three rotation zero-modes expected (shown with the next ones)

for path in sys.argv[1:]:
    N = int(path.split('/')[-1].split('.')[0])
    X = np.array([[float(t) for t in l.split(',')] for l in open(path) if l.strip()])
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    E0 = energy_grad(X.ravel(), N)[0]
    res = minimize(lambda x: energy_grad(x, N), X.ravel(), jac=True, method='L-BFGS-B', options={'maxiter': 20000, 'gtol': 1e-13, 'ftol': 1e-16})
    X1 = res.x.reshape(N, 3); X1 /= np.linalg.norm(X1, axis=1, keepdims=True)
    E1, G1 = energy_grad(X1.ravel(), N)
    low, nxt = hessian_min_eig(X1)
    Emp = mp_energy(X1)
    with open(path.replace('.txt', '_refined.txt'), 'w') as f:
        for p in X1: f.write(','.join(format(c, '.25f') for c in p) + '\n')
    print(f'N={N} E_before={E0:.10f} E_after={mp.nstr(Emp, 20)} |grad|max={np.abs(G1).max():.2e} lowest tangent eigenvalues={np.round(low, 6).tolist()} next={nxt:.4g}', flush=True)
