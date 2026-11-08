import numpy as np, packlib, worker, time, sys, json, os
from polsweep3 import load_seed
from lptrac import lp_trace
T = packlib.table()

def run(m, n, N, budget=260):
    t0 = time.time()
    U0, src = load_seed(m, n, N)
    if U0 is None:
        print(json.dumps(dict(m=m, n=n, N=N, err='noseed')), flush=True); return
    tv = T[(m, n, N)]['val']
    sd = worker.mind(U0)
    nv = N * n * (m - n)
    outp = f'results/{m}-{n}-{N}.pol.npy'
    logp = f'results/{m}-{n}-{N}.pol.json'
    na = 2500 if nv < 3000 else 2000
    U, tr = lp_trace(U0, tol=5e-4, max_iter=60, r0=1e-3, n_active=na,
                     deadline=t0 + budget * 0.92, early=8,
                     gapor_stop=8e-5, noacc_stop=18,
                     method='highs-ipm', lp_time=90, max_r=0.05,
                     dstop=n - tv - 1e-8)
    d = worker.mind(U)
    accs = sum(1 for t in tr if t[3])
    gor = 0.0
    if len(tr) >= 3:
        g = [t[1] - t[2] for t in tr[:3]]
        rr = [t[4] for t in tr[:3]]
        gor = sorted(g[i] / rr[i] for i in range(3))[1]
    stage = 're5fix' if accs == 0 else 're5'
    if d > sd and (not os.path.exists(outp) or d > worker.mind(np.load(outp))):
        np.save(outp, U)
    rec = dict(m=m, n=n, N=N, seed=sd, src='re5', d=d, gain=d - tv,
               stage=stage, acc=accs, gor=float(gor), iters=len(tr),
               t=round(time.time() - t0, 1))
    json.dump(rec, open(logp, 'w'))
    print(json.dumps(dict(rec, d=round(d, 12), gain=round(d - tv, 10),
                          gor='%.1e' % gor)), flush=True)

if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]),
        float(sys.argv[4]) if len(sys.argv) > 4 else 260)
