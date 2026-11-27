"""Basin hopping from the posted minimum: surface-atom relocation moves + small global shakes; Metropolis at kT."""
import sys, os, time, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from common import *
def coordination(X, rc):
    d = np.linalg.norm(X[:, None] - X[None], axis=2); return (d < rc).sum(1) - 1
def bh(metal, n, seconds, seed, kT=0.15):
    rng = np.random.default_rng(seed); t0 = time.time()
    E, X = relax(metal, posted(metal, n), gtol=1e-8); best = (E, X.copy()); cur = (E, X.copy()); steps = 0
    rc = 3.3 if metal == 'Al' else 4.1
    while time.time() - t0 < seconds:
        Y = cur[1].copy(); steps += 1
        if rng.random() < 0.7:
            cn = coordination(Y, rc); m = rng.integers(1, 4)
            idx = rng.choice(np.argsort(cn)[:max(8, n // 5)], m, replace=False)
            for i in idx:
                Z = np.delete(Y, i, 0); site = surface_sites(Z, 1, rng, d0=2.8 if metal == 'Al' else 3.5)[0]; Y[i] = site
        else:
            Y += rng.normal(scale=0.35, size=Y.shape)
        e, Y = relax(metal, Y)
        if e < cur[0] or rng.random() < np.exp(-(e - cur[0]) / kT): cur = (e, Y)
        if e < best[0] - 1e-7: best = (e, Y.copy())
        if steps % 200 == 0: cur = (best[0], best[1].copy())
    return best, steps
if __name__ == '__main__':
    metal, n, sec, seed, outdir = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    tab = table(metal); (E, X), steps = bh(metal, n, sec, seed)
    np.savetxt(os.path.join(outdir, f'{metal}_{n}_best.xyz'), X, fmt='%.12f')
    print(json.dumps({'metal': metal, 'N': n, 'E_best': E, 'E_table': tab[n], 'dE': E - tab[n], 'steps': steps}), flush=True)
