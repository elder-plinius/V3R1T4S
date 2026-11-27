"""LNS v2: same ruin-and-recreate moves as lns.py, with simulated-annealing acceptance (T0 -> 0 geometrically over the
time budget), k in 1..6, and a strictly-feasible global best checkpoint. Usage: lns2.py START.json PREFIX SEED SECONDS T0"""
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iea37 import aep, feas
from wflo import polish, strict_ok
from lns import turbine_energy, grid, insert_best
start, prefix, seed, secs, T0 = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
d = json.load(open(start)); x = np.array(d['x']); y = np.array(d['y']); n = len(x)
rng = np.random.default_rng(seed); GX, GY = grid(n, 50.0)
cur = aep(x, y); best = cur if strict_ok(x, y) else -1; bx, by = x, y
t_start = time.time(); log = open(prefix+'.log', 'a'); it = 0
print('start %.5f' % cur, file=log, flush=True)
while time.time()-t_start < secs:
    frac = (time.time()-t_start)/secs; T = T0*(0.001**frac)
    k = int(rng.integers(1, 7)); mode = rng.choice(['random', 'worst', 'cluster'])
    if mode == 'random': rem = rng.choice(n, k, replace=False)
    elif mode == 'worst': rem = np.argsort(turbine_energy(x, y))[:k]
    else:
        c = rng.integers(n); rem = np.argsort(np.hypot(x-x[c], y-y[c]))[:k]
    keep = np.setdiff1d(np.arange(n), rem); xx, yy = x[keep], y[keep]
    for _ in range(k):
        r = insert_best(xx, yy, GX, GY, n)
        if r is None: break
        xx, yy = r
    it += 1
    if len(xx) != n: continue
    xx, yy = polish(xx, yy, maxiter=400, ftol=1e-11)
    if not strict_ok(xx, yy): continue
    a = aep(xx, yy)
    if a > cur or rng.random() < np.exp((a-cur)/max(T, 1e-9)):
        cur, x, y = a, xx, yy
    if a > best + 1e-6:
        best, bx, by = a, xx, yy
        json.dump(dict(x=list(map(float, bx)), y=list(map(float, by)), aep=best), open(prefix+'_best.json', 'w'))
    print(it, mode, k, 'T %.1f' % T, 'cand %.5f cur %.5f best %.5f' % (a, cur, best), file=log, flush=True)
