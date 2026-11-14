import numpy as np, packlib, worker, time, sys, json, os

T = packlib.table()

def load_seed(m, n, N):
    """Return the best available seed: Sloane flat file or repo record cell,
    whichever has the larger min-distance (after re-orthonormalisation)."""
    cands = []
    p = f'grass/txts/grassc.{m}.{n}.{N}.txt'
    if os.path.exists(p):
        try:
            cands.append(packlib.orth(packlib.load_flat(p, m, n, N)))
        except Exception:
            pass
    q = f'packing-records/grassmannian/{m}-{n}-{N}.txt'
    if os.path.exists(q):
        try:
            a = np.loadtxt(q, delimiter=',', comments='#')
            U = a.reshape(N, n, m).transpose(2, 1, 0)
            cands.append(packlib.orth(U))
        except Exception:
            pass
    if not cands:
        return worker.orth_frames(np.random.default_rng(0).standard_normal((m, n, N))), 'rand'
    ds = [worker.mind(U) for U in cands]
    i = int(np.argmax(ds))
    return cands[i], ('sloane' if i == 0 and len(cands) > 1 or i == 0 else 'repo')


def run(m, n, N, budget=650):
    t0 = time.time()
    U0, src = load_seed(m, n, N)
    row = T.get((m, n, N))
    tv = row['val'] if row else None
    nv = N * n * (m - n) + 1
    sd = worker.mind(U0)

    os.makedirs('results', exist_ok=True)
    outp = f'results/{m}-{n}-{N}.pol.npy'
    logp = f'results/{m}-{n}-{N}.pol.json'

    def emit(stage, U):
        d = worker.mind(U)
        np.save(outp, U)
        rec = dict(m=m, n=n, N=N, seed=sd, src=src, d=d,
                   gain=None if tv is None else d - tv,
                   stage=stage, t=round(time.time() - t0, 1))
        json.dump(rec, open(logp, 'w'))
        print(json.dumps(dict(rec, d=round(d, 12),
                              gain=None if tv is None else round(d - tv, 10))),
              flush=True)
        return d

    if nv < 1200:
        it1, na1, it2, na2 = 25, 1600, 18, 2500
    elif nv < 2500:
        it1, na1, it2, na2 = 18, 1200, 10, 1200
    else:
        it1, na1, it2, na2 = 10, 700, 6, 700

    U = worker.lp_polish(U0, tol=1e-5, max_iter=it1, r0=0.06, n_active=na1,
                         deadline=t0 + budget * 0.5)
    d = emit('deep', U)
    gain = None if tv is None else d - tv

    if (gain is None or gain < 3e-7) and time.time() - t0 < budget:
        U2 = worker.lp_polish(U, tol=1e-6, max_iter=it2, r0=0.02, n_active=na2,
                              deadline=t0 + budget)
        if worker.mind(U2) > d:
            U = U2
        d = emit('extra', U)
        gain = None if tv is None else d - tv

    tied = gain is not None and gain <= 1e-10
    if tied and time.time() - t0 < budget:
        U2 = worker.lp_polish(U0, tol=1e-5, max_iter=20, r0=0.25,
                              deadline=t0 + budget * 0.7)
        U2 = worker.lp_polish(U2, tol=1e-6, max_iter=15, r0=0.03,
                              deadline=t0 + budget)
        if worker.mind(U2) > d:
            U = U2
        emit('bigR', U)

if __name__ == '__main__':
    m, n, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    budget = float(sys.argv[4]) if len(sys.argv) > 4 else 650
    run(m, n, N, budget)
