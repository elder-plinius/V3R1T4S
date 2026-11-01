"""Pass 2: neighbour seeding (best(N+1) minus one ball, best(N-1) plus one ball at a deep hole),
followed by basin hopping. Writes improvements into best/."""
import numpy as np, sys, time, os
from multiprocessing import Pool
from scipy.spatial import cKDTree
from core import *
from run import load_best, save, T, HERE

def deep_holes(x, rng, k=5, m=40000):
    p = rng.normal(size=(m, 4)); p /= np.linalg.norm(p, axis=1)[:, None]
    p *= rng.random(m)[:, None] ** 0.25
    d, _ = cKDTree(x).query(p)
    clear = np.minimum(d, 1 - np.linalg.norm(p, axis=1) + 0.0)
    return p[np.argsort(-clear)[:k]]

def contacts(x, r, tol=1e-6):
    t = cKDTree(x); pairs = t.query_pairs(2 * r * (1 + tol), output_type='ndarray')
    c = np.bincount(pairs.ravel(), minlength=len(x))
    c += (np.linalg.norm(x, axis=1) > 1 - r * (1 + tol)).astype(int)
    return c

def work(args):
    N, budget, seed = args
    rng = np.random.default_rng(seed); t0 = time.time(); rt = T[N]
    br, bx = load_best(N)
    log = open(os.path.join(HERE, 'logs', f'{N}.log'), 'a')
    def upd(y, r, tag):
        nonlocal br, bx
        if r > br + 1e-13:
            br, bx = r, y; save(N, y, r)
            print(f'{N} {tag} t={time.time()-t0:.0f} r={r:.13f} diff={r-rt:+.3e}', file=log, flush=True)
    rp, xp = load_best(N + 1)
    if xp is not None and len(xp) == N + 1:
        c = contacts(xp, rp); order = np.argsort(c + rng.random(N + 1))
        for i in order[:6]:
            y = np.delete(xp, i, axis=0); y, r = relax(y, rp, k0=1e3); upd(y, r, 'from+1')
    rm, xm = load_best(N - 1)
    if xm is not None and len(xm) == N - 1:
        for h in deep_holes(xm, rng):
            y = np.vstack([xm, h]); y, r = relax(y, rm * 0.98, k0=1e2); upd(y, r, 'from-1')
    it = 0
    while time.time() - t0 < budget:
        it += 1
        if rng.random() < 0.15:
            # remove 1-3 low-contact balls, reinsert at deep holes
            c = contacts(bx, br); k = rng.integers(1, 4)
            idx = np.argsort(c + rng.random(N))[:k]
            y = np.delete(bx, idx, axis=0); y = np.vstack([y, deep_holes(y, rng, k)])
            y, r = relax(y, br * 0.98, k0=1e2); upd(y, r, f'rr{k}')
        else:
            dl = rng.choice([0.03, 0.05, 0.1, 0.1, 0.15])
            y = bx + rng.normal(size=bx.shape) * dl * br
            nr = np.linalg.norm(y, axis=1); m = nr > 0.99
            y[m] *= (0.99 / nr[m])[:, None]
            y, r = relax(y, br, k0=1e2); upd(y, r, f'mbh{dl}')
    print(f'{N} pass2 done it={it} best={br:.13f} diff={br-rt:+.3e}', file=log, flush=True)
    return N, br, br - rt

if __name__ == '__main__':
    budget = float(sys.argv[1]); Ns = [int(a) for a in sys.argv[2].split(',')]
    tasks = [(N, budget, 7919 * N + int(time.time()) % 1000) for N in Ns]
    with Pool(4) as p:
        for N, br, d in p.imap_unordered(work, tasks):
            print(N, f'{br:.13f}', f'{d:+.3e}', flush=True)
