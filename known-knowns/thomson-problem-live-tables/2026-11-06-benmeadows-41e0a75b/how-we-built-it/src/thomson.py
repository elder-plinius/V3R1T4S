"""Thomson problem tools: energy, gradient, L-BFGS, basin hopping."""
import numpy as np
from math import fsum
from scipy.optimize import minimize
from scipy.spatial import ConvexHull, distance
from numba import njit


@njit(cache=True, fastmath=False)
def _nb_eg(x, g):
    n = x.shape[0]
    E = 0.0
    g[:] = 0.0
    for i in range(n - 1):
        xi = x[i, 0]; yi = x[i, 1]; zi = x[i, 2]
        gxi = 0.0; gyi = 0.0; gzi = 0.0
        for j in range(i + 1, n):
            dx = xi - x[j, 0]; dy = yi - x[j, 1]; dz = zi - x[j, 2]
            r2 = dx * dx + dy * dy + dz * dz
            inv_r = 1.0 / np.sqrt(r2)
            E += inv_r
            f = inv_r / r2
            gxi -= dx * f; gyi -= dy * f; gzi -= dz * f
            g[j, 0] += dx * f; g[j, 1] += dy * f; g[j, 2] += dz * f
        g[i, 0] += gxi; g[i, 1] += gyi; g[i, 2] += gzi
    return E


def energy_grad_fast(y):
    """Numba energy + gradient wrt x on unit sphere (input already |.|=1)."""
    x = np.ascontiguousarray(y, dtype=np.float64)
    g = np.empty_like(x)
    E = _nb_eg(x, g)
    return E, g


def normalize(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def energy_exact(x):
    """Compensated-sum energy of unit-normalized points."""
    x = normalize(np.asarray(x, dtype=np.float64).reshape(-1, 3))
    d = distance.pdist(x)
    return fsum((1.0 / d).tolist())


def energy_grad(y):
    """E and projected gradient wrt y (x = y/|y| rowwise). y:(N,3)."""
    n = np.linalg.norm(y, axis=1, keepdims=True)
    x = y / n
    d = x[:, None, :] - x[None, :, :]
    r2 = np.einsum('ijk,ijk->ij', d, d)
    np.fill_diagonal(r2, np.inf)
    inv_r = 1.0 / np.sqrt(r2)
    E = 0.5 * np.sum(inv_r)
    inv_r3 = inv_r / r2
    np.fill_diagonal(inv_r3, 0.0)
    g = -np.einsum('ij,ijk->ik', inv_r3, d)
    gx = np.einsum('ij,ij->i', g, x)
    gy = (g - x * gx[:, None]) / n
    return E, gy


def _fg_flat(yflat):
    y = yflat.reshape(-1, 3)
    n = np.linalg.norm(y, axis=1, keepdims=True)
    x = y / n
    E, g = energy_grad_fast(x)
    gx = np.einsum('ij,ij->i', g, x)
    gy = (g - x * gx[:, None]) / n
    return E, gy.ravel()


def local_min(y, maxiter=2500, ftol=1e-16, gtol=1e-9):
    y = normalize(y)
    res = minimize(_fg_flat, y.ravel(), jac=True, method='L-BFGS-B',
                   options={'maxiter': maxiter, 'ftol': ftol, 'gtol': gtol,
                            'maxfun': maxiter * 4})
    x = normalize(res.x.reshape(-1, 3))
    E, _ = energy_grad_fast(x)
    return x, E


def per_point_energy(x):
    d = x[:, None, :] - x[None, :, :]
    r2 = np.einsum('ijk,ijk->ij', d, d)
    np.fill_diagonal(r2, np.inf)
    return np.sum(1.0 / np.sqrt(r2), axis=1)  # = 2 * contribution


def holes(x):
    """Voronoi-vertex-like hole candidates: normalized face centroids of the
    convex hull triangulation, with radius = min dist to the 3 face points."""
    try:
        h = ConvexHull(x)
    except Exception:
        return np.empty((0, 3)), np.empty(0)
    tri = x[h.simplices]                      # (M,3,3)
    c = normalize(tri.mean(axis=1))
    # radius: min distance from hole to the 3 defining points
    dd = np.linalg.norm(tri - c[:, None, :], axis=2)
    rad = dd.min(axis=1)
    # also need distance to ALL points to avoid landing on an existing point
    return c, rad


def dist_to_set(c, x):
    d = distance.cdist(c, x)
    return d.min(axis=1)


def move_swap(x, rng, k=None, local=False):
    """Relocate k hottest points to the k largest distinct holes.
    local=True: each hot point goes to the largest hole NEAR it (defect glide)."""
    N = len(x)
    if k is None:
        k = rng.choice([1, 1, 1, 2, 2, 3, 4, 6, 8])
    k = min(k, N)
    pp = per_point_energy(x)
    hot = np.argsort(pp)[::-1][:k]
    c, rad = holes(x)
    if len(c) == 0:
        return move_kick(x, rng, 0.3, 0.4)
    true_rad = dist_to_set(c, x)
    y = x.copy()
    placed = []
    if local:
        used = set()
        for h in hot:
            near = np.where((c @ x[h]) > 0.75)[0]
            pool = near if len(near) else np.arange(len(c))
            best = None
            for idx in pool[np.argsort(true_rad[pool])[::-1]]:
                if idx in used:
                    continue
                if any(np.dot(c[idx], p) > 0.995 for p in placed):
                    continue
                best = idx
                break
            if best is not None:
                used.add(best)
                placed.append(c[best])
                y[h] = c[best] + 0.02 * rng.standard_normal(3)
        return normalize(y)
    order = np.argsort(true_rad)[::-1]
    ci = 0
    for idx in order:
        if ci >= k:
            break
        if any(np.dot(c[idx], p) > 0.995 for p in placed):
            continue
        y[hot[ci]] = c[idx] + 0.02 * rng.standard_normal(3)
        placed.append(c[idx])
        ci += 1
    return normalize(y)


def move_cap_refresh(x, rng, cap_cos=None):
    """Delete a random spherical cap of points and greedily refill it.
    Reorganizes a whole patch (defect layout can change)."""
    N = len(x)
    c = rng.standard_normal(3)
    c /= np.linalg.norm(c)
    if cap_cos is None:
        # cap of ~6-14% of the sphere: cos(theta) s.t. (1-cos)/2 ~ frac
        frac = rng.uniform(0.05, 0.14)
        cap_cos = 1.0 - 2.0 * frac
    mask = x @ c > cap_cos
    m = int(mask.sum())
    if m < 2:
        return move_kick(x, rng, 0.2, 0.3)
    keep = ~mask
    y = x[keep]
    # candidate refill sites: gaussian directions around cap center, filtered
    # to the cap; greedy farthest-first insertion wrt kept + chosen sites
    sig = np.sqrt(2.0 * (1.0 - cap_cos)) * 1.2
    cand = np.empty((0, 3))
    tries = 0
    while len(cand) < 30 * m and tries < 6:
        tries += 1
        cc = normalize(c[None, :] + sig * rng.standard_normal((60 * m, 3)))
        cc = cc[cc @ c > cap_cos - 0.02]
        cand = np.vstack([cand, cc])
    if len(cand) < m:
        extra = normalize(c[None, :] + 0.3 * rng.standard_normal((4 * m, 3)))
        cand = np.vstack([cand, extra])
    chosen = []
    # start from the hole farthest from kept points inside cap
    dmin = distance.cdist(cand, y).min(axis=1)
    order = np.argsort(dmin)[::-1]
    chosen.append(cand[order[0]])
    dmin2 = np.linalg.norm(cand - chosen[0], axis=1)
    dmin = np.minimum(dmin, dmin2)
    for _ in range(m - 1):
        i = int(np.argmax(dmin))
        chosen.append(cand[i])
        dmin = np.minimum(dmin, np.linalg.norm(cand - cand[i], axis=1))
        dmin[i] = -1
    y2 = np.vstack([y, np.array(chosen) + 0.015 * rng.standard_normal((len(chosen), 3))])
    return normalize(y2)


def move_kick(x, rng, frac=0.15, sigma=0.25):
    N = len(x)
    m = max(1, int(frac * N))
    idx = rng.choice(N, size=m, replace=False)
    y = x.copy()
    y[idx] += sigma * rng.standard_normal((m, 3))
    return normalize(y)


def move_caprot(x, rng, cap_cos=None, ang=None):
    """Rotate a random spherical cap about its axis."""
    N = len(x)
    c = rng.standard_normal(3)
    c /= np.linalg.norm(c)
    cosang = x @ c
    if cap_cos is None:
        cap_cos = rng.uniform(0.7, 0.95)
    mask = cosang > cap_cos
    if mask.sum() < 2:
        return move_kick(x, rng, 0.15, 0.25)
    if ang is None:
        ang = rng.uniform(-0.8, 0.8)
    # Rodrigues rotation about c
    K = np.array([[0, -c[2], c[1]], [c[2], 0, -c[0]], [-c[1], c[0], 0]])
    R = np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)
    y = x.copy()
    y[mask] = y[mask] @ R.T
    return normalize(y)


def basin_hop(x0, rng, n_iter, t_start=None, verbose=True, time_limit=None):
    import time
    t0 = time.time()
    x, E = local_min(x0)
    best_x, best_E = x.copy(), E
    if verbose:
        print(f"  start E={E:.9f}", flush=True)
    fails = 0
    for it in range(n_iter):
        r = rng.random()
        if r < 0.62:
            # escalate swap size after failures
            k = rng.choice([1, 1, 2, 2, 3, 4, 6, 8]) + (fails // 12)
            xt = move_swap(x, rng, k)
        elif r < 0.82:
            xt = move_caprot(x, rng)
        else:
            xt = move_kick(x, rng, frac=rng.uniform(0.05, 0.4),
                           sigma=rng.uniform(0.05, 0.4) + 0.03 * (fails // 12))
        xt, Et = local_min(xt)
        if Et < E - 1e-9:
            d = E - Et
            x, E = xt, Et
            fails = 0
            if Et < best_E - 1e-10:
                best_x, best_E = xt.copy(), Et
            if verbose:
                print(f"  it {it}: E={E:.9f} (-{d:.6f})", flush=True)
        else:
            fails += 1
        if time_limit and time.time() - t0 > time_limit:
            break
    # final polish of best
    best_x, best_E = local_min(best_x, maxiter=4000)
    return best_x, best_E
