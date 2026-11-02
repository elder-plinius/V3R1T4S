"""hsp4-b search: N equal balls in the unit 4-ball.

Reformulation: points x_i in the closed unit ball, maximise D = min |x_i - x_j|.
Ball centres c_i = (1 - r) x_i with r = D / (2 + D).

Pipeline per start: random or D4-lattice-cut seed -> penalty inflation with
L-BFGS -> sequential LP polish (HiGHS) on the near-active constraint set.
"""
import sys, os, time, json
import numpy as np
from numba import njit
from scipy.optimize import minimize, linprog
from scipy.sparse import coo_matrix

DIM = 4


@njit(cache=True)
def penalty(xf, n, D2, wb):
    x = xf.reshape(n, 4)
    g = np.zeros((n, 4))
    f = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            d0 = x[i, 0] - x[j, 0]
            d1 = x[i, 1] - x[j, 1]
            d2 = x[i, 2] - x[j, 2]
            d3 = x[i, 3] - x[j, 3]
            s = d0 * d0 + d1 * d1 + d2 * d2 + d3 * d3
            v = D2 - s
            if v > 0.0:
                f += v * v
                c = -4.0 * v
                g[i, 0] += c * d0; g[j, 0] -= c * d0
                g[i, 1] += c * d1; g[j, 1] -= c * d1
                g[i, 2] += c * d2; g[j, 2] -= c * d2
                g[i, 3] += c * d3; g[j, 3] -= c * d3
        s = x[i, 0] ** 2 + x[i, 1] ** 2 + x[i, 2] ** 2 + x[i, 3] ** 2
        v = s - 1.0
        if v > 0.0:
            f += wb * v * v
            c = 4.0 * wb * v
            for k in range(4):
                g[i, k] += c * x[i, k]
    return f, g.reshape(-1)


@njit(cache=True)
def min_dist(x):
    n = x.shape[0]
    m = 1e300
    for i in range(n):
        for j in range(i + 1, n):
            s = 0.0
            for k in range(4):
                t = x[i, k] - x[j, k]
                s += t * t
            if s < m:
                m = s
    return np.sqrt(m)


def project(x):
    nr = np.linalg.norm(x, axis=1)
    over = nr > 1.0
    x = x.copy()
    x[over] /= nr[over, None]
    return x


def relax(x, D, iters=3000):
    n = x.shape[0]
    res = minimize(penalty, x.reshape(-1), args=(n, D * D, 4.0), jac=True,
                   method="L-BFGS-B", options={"maxiter": iters, "gtol": 1e-14, "ftol": 1e-16})
    return res.x.reshape(n, 4)


def inflate(x, D0, rounds=40):
    """Penalty inflation: push target D up while relaxed packing remains near-feasible."""
    best = project(x)
    bestD = min_dist(best)
    D = max(D0, bestD)
    step = 0.02
    for _ in range(rounds):
        y = relax(best if bestD > 0 else x, D * (1 + step))
        y = project(y)
        dy = min_dist(y)
        if dy > bestD:
            best, bestD = y, dy
            D = dy
            step = min(step * 1.5, 0.05)
        else:
            step *= 0.5
            if step < 1e-5:
                break
    return best, bestD


def slp(x, iters=200, delta=0.02, tol=1e-15, cut=1.15, verbose=False):
    """Sequential LP: maximise t s.t. linearised |xi-xj| >= t, |xi| <= 1, |dx|_inf <= delta."""
    n = x.shape[0]
    x = project(x)
    D = min_dist(x)
    for it in range(iters):
        diff = x[:, None, :] - x[None, :, :]
        dist = np.linalg.norm(diff, axis=2)
        iu, ju = np.triu_indices(n, 1)
        dd = dist[iu, ju]
        sel = dd < D * cut + 2 * delta
        iu, ju, dd = iu[sel], ju[sel], dd[sel]
        u = (x[iu] - x[ju]) / dd[:, None]
        nr = np.linalg.norm(x, axis=1)
        bsel = np.where(nr > 1 - 2 * delta - 0.05)[0]
        nv = n * DIM + 1
        m1 = len(iu)
        # pair rows: -(u.(dxi - dxj)) + t <= dd
        rows = np.repeat(np.arange(m1), 2 * DIM + 1)
        cols = np.concatenate([
            (iu[:, None] * DIM + np.arange(DIM)[None, :]),
            (ju[:, None] * DIM + np.arange(DIM)[None, :]),
            np.full((m1, 1), n * DIM)], axis=1).reshape(-1)
        vals = np.concatenate([-u, u, np.ones((m1, 1))], axis=1).reshape(-1)
        # boundary rows: xhat.dx <= 1 - |x|
        m2 = len(bsel)
        xh = x[bsel] / nr[bsel, None]
        rows2 = np.repeat(np.arange(m2) + m1, DIM)
        cols2 = (bsel[:, None] * DIM + np.arange(DIM)[None, :]).reshape(-1)
        vals2 = xh.reshape(-1)
        A = coo_matrix((np.concatenate([vals, vals2]),
                        (np.concatenate([rows, rows2]), np.concatenate([cols, cols2]))),
                       shape=(m1 + m2, nv)).tocsr()
        b = np.concatenate([dd, 1 - nr[bsel]])
        c = np.zeros(nv); c[-1] = -1.0
        bounds = [(-delta, delta)] * (n * DIM) + [(None, None)]
        res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
        if res.status != 0:
            delta *= 0.5
            if delta < 1e-12:
                break
            continue
        dx = res.x[:-1].reshape(n, DIM)
        y = project(x + dx)
        Dy = min_dist(y)
        if Dy > D:
            gain = Dy - D
            x, D = y, Dy
            if verbose:
                print(it, D, delta, gain)
            if gain < tol:
                break
            # step size control based on predicted vs actual
            if np.abs(dx).max() < 0.5 * delta:
                delta = max(np.abs(dx).max() * 1.5, 1e-12)
        else:
            delta *= 0.3
            if delta < 1e-13:
                break
    return x, D


def d4_seed(n, rng):
    """N points of a randomly scaled, shifted, rotated D4 lattice closest to the origin."""
    a = rng.uniform(0.9, 1.6)
    rngp = np.arange(-6, 7)
    g = np.array(np.meshgrid(rngp, rngp, rngp, rngp, indexing="ij")).reshape(4, -1).T
    g = g[g.sum(1) % 2 == 0].astype(float)
    shift = rng.uniform(-1, 1, 4) * rng.choice([0.0, 0.5, 1.0])
    g = g + shift
    nr = np.linalg.norm(g, axis=1) + 1e-9 * rng.standard_normal(len(g))
    pts = g[np.argsort(nr)[:n]]
    pts = pts / np.linalg.norm(pts, axis=1).max()
    q, _ = np.linalg.qr(rng.standard_normal((4, 4)))
    return pts @ q + 1e-3 * rng.standard_normal(pts.shape)


def random_seed(n, rng):
    v = rng.standard_normal((n, 4))
    v /= np.linalg.norm(v, axis=1)[:, None]
    rad = rng.uniform(0, 1, n) ** 0.25
    return v * rad[:, None]


def r_of_D(D):
    return D / (2 + D)


def run(n, seed, kind):
    rng = np.random.default_rng(seed)
    x0 = d4_seed(n, rng) if kind == "d4" else random_seed(n, rng)
    x, D = inflate(x0, 0.3)
    x, D = slp(x, iters=60, delta=0.01, tol=1e-12)
    return x, D


if __name__ == "__main__":
    n = int(sys.argv[1]); seed = int(sys.argv[2]); kind = sys.argv[3]
    t = time.time()
    x, D = run(n, seed, kind)
    print(n, seed, kind, r_of_D(D), time.time() - t)
