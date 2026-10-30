"""Large-neighbourhood search imported from vehicle-routing / facility-location practice (ruin and recreate):
remove k turbines (random, worst-producing, or spatial cluster), re-insert each greedily at the best point of a
dense candidate grid that respects the constraints, then SLSQP-polish; accept if strictly better (else keep).
Usage: lns.py START.json OUT_PREFIX SEED ITERS"""
import sys, os, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iea37 import aep, feas, RADIUS, dir_power, frames, U, D, K, CT, FREQ, CI, RWS, RP, CO
from wflo import polish, strict_ok

def turbine_energy(x, y):
    """Per-turbine expected energy (for 'worst' removal)."""
    fx, fy = frames(x, y)
    dx = fx[:, :, None]-fx[:, None, :]; dy = fy[:, :, None]-fy[:, None, :]; m = dx > 0
    sig = K*np.where(m, dx, 1.)+D/np.sqrt(8.); la = np.where(m, (1-np.sqrt(1-CT/(8*sig**2/D**2)))*np.exp(-0.5*(dy/sig)**2), 0.)
    v = U*(1-np.sqrt((la**2).sum(2)))
    p = np.where((CI <= v) & (v < RWS), RP*((v-CI)/(RWS-CI))**3, np.where((RWS <= v) & (v < CO), RP, 0.))
    return (FREQ[:, None]*p).sum(0)

def grid(n, h):
    R = RADIUS[n]-1e-6; g = np.arange(-R, R+h, h); X, Y = np.meshgrid(g, g); X = X.ravel(); Y = Y.ravel()
    keep = np.hypot(X, Y) <= R
    th = np.linspace(0, 2*np.pi, int(2*np.pi*R/(h/2)), endpoint=False)   # boundary ring, denser
    return np.concatenate([X[keep], R*np.cos(th)]), np.concatenate([Y[keep], R*np.sin(th)])

def insert_best(x, y, GX, GY, n):
    ok = np.ones(len(GX), bool)
    for xi, yi in zip(x, y): ok &= np.hypot(GX-xi, GY-yi) >= 2*D+1e-6
    idx = np.nonzero(ok)[0]
    if len(idx) == 0: return None
    best, bv = None, -1
    # evaluate AEP for each candidate (vectorised in chunks)
    for c in np.array_split(idx, max(1, len(idx)//400)):
        for i in c:
            v = aep(np.append(x, GX[i]), np.append(y, GY[i]))
            if v > bv: bv, best = v, i
    return np.append(x, GX[best]), np.append(y, GY[best])

if __name__ == '__main__':
    start, prefix, seed, iters = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    d = json.load(open(start)); x = np.array(d['x']); y = np.array(d['y']); n = len(x)
    rng = np.random.default_rng(seed); GX, GY = grid(n, 50.0)
    best = aep(x, y); log = open(prefix+'.log', 'a')
    print('start', best, feas(x, y), file=log, flush=True)
    for it in range(iters):
        k = int(rng.integers(1, 5)); mode = rng.choice(['random', 'worst', 'cluster'])
        if mode == 'random': rem = rng.choice(n, k, replace=False)
        elif mode == 'worst': rem = np.argsort(turbine_energy(x, y))[:k]
        else:
            c = rng.integers(n); rem = np.argsort(np.hypot(x-x[c], y-y[c]))[:k]
        keep = np.setdiff1d(np.arange(n), rem); xx, yy = x[keep], y[keep]
        for _ in range(k):
            r = insert_best(xx, yy, GX, GY, n)
            if r is None: break
            xx, yy = r
        if len(xx) != n: continue
        xx, yy = polish(xx, yy, maxiter=400, ftol=1e-11)
        a = aep(xx, yy)
        if strict_ok(xx, yy) and a > best + 1e-6:
            best, x, y = a, xx, yy
            json.dump(dict(x=list(map(float, x)), y=list(map(float, y)), aep=best), open(prefix+'_best.json', 'w'))
        print(it, mode, k, '%.5f' % a, 'best %.5f' % best, file=log, flush=True)
