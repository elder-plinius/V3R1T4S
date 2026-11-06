"""Production search for hsp4, one N per task: Riesz-annealed random starts,
then monotonic basin hopping (Gaussian jitter + penalty descent)."""
import numpy as np, sys, time, os
from multiprocessing import Pool
from core import *
T = table()
HERE = os.path.dirname(os.path.abspath(__file__))

def load_best(N):
    f = os.path.join(HERE, 'best', f'hsp4-{N}.txt')
    if not os.path.exists(f): return -1.0, None
    x = np.loadtxt(f, comments='#')
    return feasible_np(x), x

def save(N, x, r):
    f = os.path.join(HERE, 'best', f'hsp4-{N}.txt')
    with open(f + '.tmp', 'w') as fh:
        fh.write(f'# hsp4 N={N} r_float={r!r} table={T[N]:.12f}\n')
        for row in x: fh.write(' '.join(repr(float(v)) for v in row) + '\n')
    os.replace(f + '.tmp', f)

def seeds600(N, rng):
    # 600-cell vertices on radius 1-r plus N-120 interior balls
    import itertools
    phi = (1 + 5 ** .5) / 2; V = []
    for s in itertools.product([-1, 1], repeat=4): V.append(np.array(s) * .5)
    for i in range(4):
        for s in [-1, 1]: e = np.zeros(4); e[i] = s; V.append(e)
    base = np.array([phi, 1, 1 / phi, 0]) / 2
    even = [p for p in itertools.permutations(range(4)) if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0]
    for p in even:
        for s in itertools.product([-1, 1], repeat=3):
            v = np.zeros(4); vals = base * np.array(list(s) + [1])
            for k in range(4): v[p[k]] = vals[k]
            V.append(v)
    V = np.unique(np.round(np.array(V), 12), axis=0); assert len(V) == 120
    r = T[120]; X = V * (1 - r)
    k = N - 120
    if k > 0: X = np.vstack([X, rng.normal(size=(k, 4)) * 0.1])
    return X

def work(args):
    N, budget, seed = args
    rng = np.random.default_rng(seed); rt = T[N]; t0 = time.time()
    br, bx = load_best(N)
    if os.environ.get('FRESH'): br, bx = -1.0, None
    log = open(os.path.join(HERE, 'logs', f'{N}.log'), 'a')
    def upd(y, r, tag):
        nonlocal br, bx
        if r > br + 1e-13:
            br, bx = r, y
            if r > load_best(N)[0] + 1e-13: save(N, y, r)
            print(f'{N} {tag} t={time.time()-t0:.0f} r={r:.13f} diff={r-rt:+.3e}', file=log, flush=True)
    nst = 8 if bx is None else 2
    for s in range(nst):
        x, _ = random_feasible(N, rng); x = riesz(x, 4, 64, 2)
        y, r = relax(x, feasible_np(x), k0=1e3); upd(y, r, 'riesz')
    if 120 <= N <= 135:
        for s in range(3):
            y, r = relax(seeds600(N, rng), T[120] * 0.95, k0=1e2); upd(y, r, '600cell')
    it = 0
    while time.time() - t0 < budget:
        it += 1
        dl = rng.choice([0.05, 0.1, 0.1, 0.15, 0.2])
        y = bx + rng.normal(size=bx.shape) * dl * br
        nr = np.linalg.norm(y, axis=1); m = nr > 0.99
        y[m] *= (0.99 / nr[m])[:, None]
        y, r = relax(y, br, k0=1e2); upd(y, r, f'mbh{dl}')
    print(f'{N} done it={it} best={br:.13f} diff={br-rt:+.3e}', file=log, flush=True)
    return N, br, br - rt

if __name__ == '__main__':
    Ns = [int(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [n for n in range(120, 211) if n != 170]
    budget = float(sys.argv[1])
    tasks = [(N, budget, 1000 * N + int(time.time()) % 1000) for N in Ns]
    with Pool(4) as p:
        for N, br, d in p.imap_unordered(work, tasks):
            print(N, f'{br:.13f}', f'{d:+.3e}', flush=True)
