"""Monotonic basin hopping from a saved code: perturb (relocate a few points
and/or add global noise), loose descent, accept if max cosine decreases.
Final full descent on the incumbent. Saves to outdir."""
import sys, time, os
import numpy as np
from pen import normalize, descend, save, maxcos

d, N, sec, seed, infile, outdir, table = (int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]),
                                          int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7])
rng = np.random.default_rng(seed)
t0 = time.time()
X = normalize(np.loadtxt(infile, comments="#"))
c = maxcos(X)
c_start = c
acc = tries = 0
while time.time() - t0 < 0.9 * sec:
    tries += 1
    Y = X.copy()
    mode = rng.integers(3)
    if mode == 0:  # relocate 1-3 points
        idx = rng.choice(N, rng.integers(1, 4), replace=False)
        Y[idx] = rng.standard_normal((len(idx), d))
    elif mode == 1:  # global noise
        Y = Y + rng.choice([0.01, 0.03, 0.1]) * rng.standard_normal(Y.shape) / np.sqrt(d)
    else:  # relocate the point with most near-contacts plus small noise
        G = Y @ Y.T; np.fill_diagonal(G, -2)
        i = np.argmax((G > c - 1e-3).sum(1))
        Y[i] = rng.standard_normal(d)
        Y = Y + 0.01 * rng.standard_normal(Y.shape) / np.sqrt(d)
    Y, cy = descend(normalize(Y), step=1e-3, minstep=1e-8, iters=600)
    if cy < c - 1e-12:
        X, c = Y, cy
        acc += 1
        print(f"{d} {N} t={time.time()-t0:.0f}s try={tries} mode={mode} c={c:.12f}", flush=True)
X, c = descend(X, step=1e-7, minstep=1e-14, iters=4000, deadline=t0 + sec)
os.makedirs(outdir, exist_ok=True)
save(os.path.join(outdir, f"{d}_{N}.txt"), X, c, d, N, table)
print(f"{d} {N} MBH-FINAL start={c_start:.12f} best={c:.15f} table={table} margin={float(table)-c:.3e} tries={tries} acc={acc}", flush=True)
