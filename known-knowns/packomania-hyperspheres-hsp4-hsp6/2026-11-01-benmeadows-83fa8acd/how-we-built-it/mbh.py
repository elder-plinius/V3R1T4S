"""Monotonic basin hopping on the feasibility penalty, then SLP polish.

usage: python3 mbh.py N seed seconds outdir
Writes outdir/N_seed.npy (best points in unit ball, D-form) and prints r.
"""
import sys, time, os
import numpy as np
from scipy.optimize import minimize
from search import penalty, min_dist, project, slp, random_seed, d4_seed, r_of_D

FEAS = 1e-22


def emin(x, D, iters=5000):
    n = x.shape[0]
    res = minimize(penalty, x.reshape(-1), args=(n, D * D, 1.0), jac=True,
                   method="L-BFGS-B",
                   options={"maxiter": iters, "gtol": 1e-13, "ftol": 1e-20, "maxcor": 20})
    return res.x.reshape(n, 4), res.fun


def feasible_D(x):
    return min_dist(project(x))


def mbh(n, seed, seconds, Dtab, verbose=False):
    rng = np.random.default_rng(seed)
    t0 = time.time()
    x = d4_seed(n, rng) if seed % 3 == 0 else random_seed(n, rng)
    # coarse compression from low density
    D = 0.8 * Dtab
    x, f = emin(x, D)
    for fac in np.linspace(0.85, 0.99, 8):
        x, f = emin(x, Dtab * fac)
    # find a feasible point by decreasing D until energy ~0
    D = Dtab * 0.99
    while True:
        x, f = emin(x, D)
        if f < FEAS:
            break
        D *= 0.997
    Dbest = feasible_D(x)
    xbest = project(x)
    step = 2e-3
    fails = 0
    D = Dbest * (1 + step)
    xc, fc = emin(xbest, D)
    while time.time() - t0 < seconds:
        if fc < FEAS:
            Dn = feasible_D(xc)
            if Dn > Dbest:
                Dbest, xbest = Dn, project(xc)
            if verbose:
                print("ok", r_of_D(Dbest), step, time.time() - t0, flush=True)
            step = min(step * 1.3, 5e-3)
            D = Dbest * (1 + step)
            xc, fc = emin(xbest, D)
            fails = 0
            continue
        # perturb: move a few balls by noise of size ~ sigma*D
        y = xc.copy()
        k = rng.integers(1, 6)
        idx = rng.choice(n, k, replace=False)
        if rng.random() < 0.3:
            # relocate one ball into a random position
            y[idx[0]] = random_seed(1, rng)[0]
        y[idx] += rng.normal(0, 0.3 * D, (k, 4))
        y += rng.normal(0, 0.01 * D, y.shape)
        y, fy = emin(y, D)
        if fy < fc:
            xc, fc = y, fy
            fails = 0
        else:
            fails += 1
        if fails > 60:
            step *= 0.5
            D = Dbest * (1 + step)
            xc, fc = emin(xbest, D)
            fails = 0
    x, Dp = slp(xbest, iters=300, delta=1e-3, tol=1e-15)
    if Dp > Dbest:
        xbest, Dbest = x, Dp
    return xbest, Dbest


if __name__ == "__main__":
    n = int(sys.argv[1]); seed = int(sys.argv[2]); secs = float(sys.argv[3]); out = sys.argv[4]
    tab = {}
    for line in open(os.path.join(os.path.dirname(__file__), "../../../data/packomania.com_hsp4_txt_radius.txt")):
        p = line.split()
        if len(p) >= 2:
            tab[int(p[0])] = float(p[1])
    rT = tab[n]
    Dtab = 2 * rT / (1 - rT)
    x, D = mbh(n, seed, secs, Dtab, verbose=len(sys.argv) > 5)
    os.makedirs(out, exist_ok=True)
    np.save(os.path.join(out, f"{n}_{seed}.npy"), x)
    r = r_of_D(D)
    print(f"{n} {seed} r={r:.15f} tab={rT:.12f} diff={r - rT:+.3e}", flush=True)
