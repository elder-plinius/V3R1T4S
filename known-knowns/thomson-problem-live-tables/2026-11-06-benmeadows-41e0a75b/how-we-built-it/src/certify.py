# /// script
# dependencies = ["numpy", "scipy", "mpmath"]
# ///
"""Thomson claim check, following the V3R1T4S bank's verification method for thomson-problem-live-tables:
normalise in mpmath (dps 40), E* exactly; tangent-space Newton in mpmath until the tangent gradient norm < 1e-20 (Newton
direction from the float64 tangent Hessian, gradient and positions in mpmath); E* change < 1e-12; float64 Hessian with
rotations projected out has 2N-3 positive eigenvalues; each table's own point file polished the same way must end
>= 1e-6 above E*; table minimum - E* >= 1e-6.
usage: certify.py <ours.txt (x,y,z per line)> <table_min> <out_prefix> [<table point file> <fmt deeter|xyz> ...]"""
import sys, time
import numpy as np
from scipy.optimize import minimize
from mpmath import mp, mpf, sqrt, fsum

mp.dps = 40


def load(path, fmt):
    if fmt == 'deeter':
        v = [float(l) for l in open(path) if l.strip()]
        return np.array(v).reshape(-1, 3), None
    if fmt == 'xyz':
        rows = [l.split() for l in open(path)][2:]
        return np.array([[float(t) for t in r[1:4]] for r in rows if len(r) >= 4]), None
    rows = [l.strip().split(',') for l in open(path) if l.strip()]
    return np.array([[float(t) for t in r] for r in rows]), [[mpf(t) for t in r] for r in rows]


def e_grad_f(x):
    X = x.reshape(-1, 3); X = X / np.linalg.norm(X, axis=1, keepdims=True)
    D = X[:, None] - X[None]; r = np.linalg.norm(D, axis=2); np.fill_diagonal(r, np.inf)
    G = -np.sum(D / r[..., None] ** 3, axis=1); G -= np.sum(G * X, 1, keepdims=True) * X
    return 0.5 * np.sum(1 / r), G.ravel()


def mp_norm(P):
    return [[c / sqrt(fsum(c2 * c2 for c2 in p)) for c in p] for p in P]


def mp_energy_grad(P):
    N = len(P); E = []; G = [[mpf(0)] * 3 for _ in range(N)]
    for i in range(N):
        a = P[i]
        for j in range(i):
            b = P[j]; d = [a[k] - b[k] for k in range(3)]
            r2 = fsum(t * t for t in d); r = sqrt(r2); E.append(1 / r); w = 1 / (r2 * r)
            for k in range(3):
                G[i][k] -= d[k] * w; G[j][k] += d[k] * w
    T = []
    for i in range(N):
        dot = fsum(G[i][k] * P[i][k] for k in range(3))
        T.append([G[i][k] - dot * P[i][k] for k in range(3)])
    return fsum(E), T


def hessian_tangent(X):
    """float64 Hessian of E on the product of spheres in a 2N tangent basis (with the radial-force correction)."""
    N = len(X); D = X[:, None] - X[None]; r = np.linalg.norm(D, axis=2); np.fill_diagonal(r, np.inf)
    H = np.zeros((3 * N, 3 * N))
    for i in range(N):
        d = D[i]; ri = r[i]
        blk = 3 * d[:, :, None] * d[:, None, :] / ri[:, None, None] ** 5 - np.eye(3)[None] / ri[:, None, None] ** 3
        blk[i] = 0
        for j in range(N):
            if j != i:
                H[3 * i:3 * i + 3, 3 * j:3 * j + 3] = -blk[j]
        H[3 * i:3 * i + 3, 3 * i:3 * i + 3] = blk.sum(0)
    F = np.sum(D / r[..., None] ** 3, axis=1)  # -grad of E for each point
    B = np.zeros((3 * N, 2 * N))
    for i in range(N):
        n = X[i]; a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
        t1 = np.cross(n, a); t1 /= np.linalg.norm(t1); t2 = np.cross(n, t1)
        B[3 * i:3 * i + 3, 2 * i] = t1; B[3 * i:3 * i + 3, 2 * i + 1] = t2
        H[3 * i:3 * i + 3, 3 * i:3 * i + 3] += np.dot(F[i], n) * np.eye(3)  # -(grad E . n) on the sphere
    return B.T @ H @ B, B


def newton_mp(P, log, tol=mpf('1e-20'), max_it=12):
    """Tangent-space Newton: positions and gradient in mpmath, step from the float64 tangent Hessian (rotation modes
    removed by a pseudo-inverse); each update moves along the step and renormalises in mpmath."""
    P = mp_norm(P)
    for it in range(max_it):
        E, T = mp_energy_grad(P)
        gn = sqrt(fsum(c * c for t in T for c in t))
        log('  newton %d  E=%s  |grad|=%s' % (it, mp.nstr(E, 25), mp.nstr(gn, 5)))
        if gn < tol:
            return P, E, gn
        X = np.array([[float(c) for c in p] for p in P])
        Ht, B = hessian_tangent(X)
        g = B.T @ np.array([float(c) for t in T for c in t])
        w, V = np.linalg.eigh(Ht)
        keep = np.abs(w) > 1e-6 * np.abs(w).max()
        step = -(V[:, keep] @ ((V[:, keep].T @ g) / w[keep]))
        S = B @ step
        P = mp_norm([[P[i][k] + mpf(S[3 * i + k]) for k in range(3)] for i in range(len(P))])
    E, T = mp_energy_grad(P)
    return P, E, sqrt(fsum(c * c for t in T for c in t))


def certify(P, log):
    X = np.array([[float(c) for c in p] for p in P])
    Ht, _ = hessian_tangent(X)
    w = np.linalg.eigvalsh(Ht)
    N = len(P)
    pos = int((w > 1e-8).sum()); zero = int((np.abs(w) <= 1e-8).sum())
    log('  hessian: %d positive (need %d), %d near zero, lowest %s' % (pos, 2 * N - 3, zero, np.round(w[:6], 6).tolist()))
    return pos == 2 * N - 3, w


def polish(path, fmt, log):
    X, _ = load(path, fmt)
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    res = minimize(e_grad_f, X.ravel(), jac=True, method='L-BFGS-B', options={'maxiter': 50000, 'gtol': 1e-14, 'ftol': 1e-17})
    P = [[mpf(float(c)) for c in p] for p in res.x.reshape(-1, 3)]
    return newton_mp(P, log)


if __name__ == '__main__':
    ours, tmin, out = sys.argv[1], mpf(sys.argv[2]), sys.argv[3]
    tables = list(zip(sys.argv[4::2], sys.argv[5::2]))
    lines = []
    def log(s):
        print(s, flush=True); lines.append(s)
    t0 = time.time()
    _, Pm = load(ours, 'ours')
    E0, _ = mp_energy_grad(mp_norm(Pm))
    log('ours: N=%d  E*(as given)=%s' % (len(Pm), mp.nstr(E0, 25)))
    P, E1, gn = newton_mp(Pm, log)
    log('ours after Newton: E*=%s  change=%s  |grad|=%s' % (mp.nstr(E1, 25), mp.nstr(E1 - E0, 5), mp.nstr(gn, 5)))
    ok_h, _ = certify(P, log)
    ok = gn < mpf('1e-20') and abs(E1 - E0) < mpf('1e-12') and ok_h
    ok_t = tmin - E1 >= mpf('1e-6')
    log('table min %s - E* = %s  (need >= 1e-6): %s' % (mp.nstr(tmin, 15), mp.nstr(tmin - E1, 10), ok_t))
    ok = ok and ok_t
    for path, fmt in tables:
        log('table file %s (%s): polishing' % (path, fmt))
        _, Et, gt = polish(path, fmt, log)
        d = Et - E1
        log('  polished E=%s  minus E* = %s  (need >= 1e-6): %s' % (mp.nstr(Et, 20), mp.nstr(d, 10), d >= mpf('1e-6')))
        ok = ok and d >= mpf('1e-6')
    with open(out + '_certified.txt', 'w') as f:
        for p in P:
            f.write(','.join(mp.nstr(c, 30, strip_zeros=False) for c in p) + '\n')
    log('ALL CHECKS PASS' if ok else 'SOME CHECK FAILED')
    log('elapsed %.0fs' % (time.time() - t0))
    open(out + '_report.txt', 'w').write('\n'.join(lines) + '\n')
