"""MBH with neighbour-list penalty. usage: python3 mbh2.py N seed seconds outdir [init.npy]"""
import sys, time, os
import numpy as np
from numba import njit
from scipy.optimize import minimize
from search import min_dist, project, slp, random_seed, r_of_D, penalty

FEAS = 1e-20


@njit(cache=True)
def build_pairs(x, cut2):
    n = x.shape[0]
    cnt = 0
    out = np.empty((n * 60, 2), dtype=np.int64)
    for i in range(n):
        for j in range(i + 1, n):
            s = 0.0
            for k in range(4):
                t = x[i, k] - x[j, k]
                s += t * t
            if s < cut2:
                if cnt >= out.shape[0]:
                    return out[:cnt], False
                out[cnt, 0] = i; out[cnt, 1] = j
                cnt += 1
    return out[:cnt], True


@njit(cache=True)
def pen_nl(xf, n, D2, pairs):
    x = xf.reshape(n, 4)
    g = np.zeros((n, 4))
    f = 0.0
    for p in range(pairs.shape[0]):
        i = pairs[p, 0]; j = pairs[p, 1]
        d0 = x[i, 0] - x[j, 0]; d1 = x[i, 1] - x[j, 1]
        d2 = x[i, 2] - x[j, 2]; d3 = x[i, 3] - x[j, 3]
        s = d0 * d0 + d1 * d1 + d2 * d2 + d3 * d3
        v = D2 - s
        if v > 0.0:
            f += v * v
            c = -4.0 * v
            g[i, 0] += c * d0; g[j, 0] -= c * d0
            g[i, 1] += c * d1; g[j, 1] -= c * d1
            g[i, 2] += c * d2; g[j, 2] -= c * d2
            g[i, 3] += c * d3; g[j, 3] -= c * d3
    for i in range(n):
        s = x[i, 0] ** 2 + x[i, 1] ** 2 + x[i, 2] ** 2 + x[i, 3] ** 2
        v = s - 1.0
        if v > 0.0:
            f += v * v
            c = 4.0 * v
            for k in range(4):
                g[i, k] += c * x[i, k]
    return f, g.reshape(-1)


def emin(x, D, iters=3000):
    n = x.shape[0]
    for _ in range(4):
        pairs, ok = build_pairs(x, (1.6 * D) ** 2)
        if not ok:
            f, _ = penalty(x.reshape(-1), n, D * D, 1.0)
            res = minimize(penalty, x.reshape(-1), args=(n, D * D, 1.0), jac=True, method="L-BFGS-B",
                           options={"maxiter": iters, "gtol": 1e-13, "ftol": 1e-20, "maxcor": 20})
            return res.x.reshape(n, 4), res.fun
        res = minimize(pen_nl, x.reshape(-1), args=(n, D * D, pairs), jac=True, method="L-BFGS-B",
                       options={"maxiter": iters, "gtol": 1e-13, "ftol": 1e-20, "maxcor": 20})
        y = res.x.reshape(n, 4)
        ftrue, _ = penalty(res.x, n, D * D, 1.0)
        if ftrue <= res.fun * (1 + 1e-9) + 1e-30:
            return y, ftrue
        x = y
    return y, ftrue


def sph(k, rng):
    v = rng.standard_normal((k, 4)); return v / np.linalg.norm(v, axis=1)[:, None]


def seed_conf(n, rng):
    frac = rng.uniform(0.78, 0.88)
    nout = int(round(frac * n))
    nc = int(rng.random() < 0.5)
    rho = rng.uniform(0.45, 0.6)
    parts = [sph(nout, rng), rho * sph(n - nout - nc, rng)]
    if nc:
        parts.append(0.02 * rng.standard_normal((1, 4)))
    return np.vstack(parts)


def initial(n, rng, Dtab):
    x = seed_conf(n, rng)
    for fac in [1.06, 1.03, 1.015, 1.005]:
        x, f = emin(x, Dtab * fac)
    D = Dtab * 0.995
    while True:
        x, f = emin(x, D)
        if f < FEAS:
            return project(x)
        D *= 0.998


def mbh(x, seconds, rng, verbose=False, maxfail=40):
    t0 = time.time()
    n = x.shape[0]
    xbest = project(x); Dbest = min_dist(xbest)
    step = 1e-3
    D = Dbest * (1 + step)
    xc, fc = emin(xbest, D)
    fails = 0
    nt = 0
    while time.time() - t0 < seconds:
        if fc < FEAS:
            Dn = min_dist(project(xc))
            if Dn > Dbest:
                Dbest, xbest = Dn, project(xc)
            if verbose:
                print("ok", r_of_D(Dbest), step, nt, round(time.time() - t0), flush=True)
            step = min(step * 1.5, 3e-3)
            D = Dbest * (1 + step)
            xc, fc = emin(xbest, D)
            fails = 0
            continue
        y = xc.copy()
        mode = rng.random()
        if mode < 0.25:
            # relocate the most stressed ball to a random spot
            i = rng.integers(n)
            y[i] = sph(1, rng)[0] * rng.uniform(0, 1) ** 0.25
        else:
            k = rng.integers(1, 8)
            i0 = rng.integers(n)
            dd = np.linalg.norm(y - y[i0], axis=1)
            idx = np.argsort(dd)[:k]
            y[idx] += rng.normal(0, 0.25 * D, (k, 4))
        y, fy = emin(y, D, iters=1200)
        nt += 1
        if fy < fc:
            xc, fc = y, fy
            fails = 0
        else:
            fails += 1
        if fails > maxfail:
            step *= 0.5
            if step < 2e-6:
                step = 1e-3
            D = Dbest * (1 + step)
            xc, fc = emin(xbest, D)
            fails = 0
    return xbest, Dbest


def table():
    tab = {}
    for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "../../../data/packomania.com_hsp4_txt_radius.txt")):
        p = line.split()
        if len(p) >= 2:
            tab[int(p[0])] = float(p[1])
    return tab


if __name__ == "__main__":
    n = int(sys.argv[1]); seed = int(sys.argv[2]); secs = float(sys.argv[3]); out = sys.argv[4]
    rT = table()[n]; Dtab = 2 * rT / (1 - rT)
    rng = np.random.default_rng(seed)
    t = time.time()
    x = np.load(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "-" else initial(n, rng, Dtab)
    x, D = mbh(x, secs, rng, verbose=os.environ.get("V") == "1")
    x2, D2 = slp(x, iters=80, delta=1e-4, tol=1e-15)
    if D2 > D:
        x, D = x2, D2
    os.makedirs(out, exist_ok=True)
    np.save(os.path.join(out, f"{n}_{seed}.npy"), x)
    r = r_of_D(D)
    print(f"{n} {seed} r={r:.15f} tab={rT:.12f} diff={r - rT:+.3e} t={time.time() - t:.0f}", flush=True)
