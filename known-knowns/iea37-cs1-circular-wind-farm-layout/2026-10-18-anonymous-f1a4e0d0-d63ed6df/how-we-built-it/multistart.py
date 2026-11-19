"""Multistart WEC + SLSQP from random feasible layouts. Usage: multistart.py N_TURB N_STARTS SEED0 OUT.jsonl NPROC"""
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iea37 import aep, feas, RADIUS
from wflo import wec_run, polish, strict_ok
from multiprocessing import Pool

def rand_layout(n, rng):
    R = RADIUS[n]; pts = []
    while len(pts) < n:
        r = R*np.sqrt(rng.random()); t = 2*np.pi*rng.random(); p = np.array([r*np.cos(t), r*np.sin(t)])
        if all(np.hypot(*(p-q)) >= 270 for q in pts): pts.append(p)
    P = np.array(pts); return P[:, 0], P[:, 1]

def one(args):
    n, seed = args
    rng = np.random.default_rng(seed); t0 = time.time()
    x, y = rand_layout(n, rng)
    x, y = wec_run(x, y, xis=(3.0, 2.5, 2.0, 1.5, 1.25, 1.0), maxiter=300, ftol=1e-9)
    x, y = polish(x, y, xi=1.0, maxiter=1000, ftol=1e-12)
    return dict(seed=seed, aep=aep(x, y), feas=list(map(float, feas(x, y))), ok=bool(strict_ok(x, y)),
                secs=time.time()-t0, x=list(map(float, x)), y=list(map(float, y)))

if __name__ == '__main__':
    n, ns, s0, out, npr = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
    with Pool(npr) as pool, open(out, 'a') as f:
        for res in pool.imap_unordered(one, [(n, s0+i) for i in range(ns)]):
            f.write(json.dumps(res)+'\n'); f.flush()
