"""Parallel checkpointed basin-hopping hunt for Thomson minima.
usage: hunt.py OUTDIR MINUTES N1 N2 ... [--hops H] [--workers W]
Resume: rerun same command; finished chain ids in OUTDIR/chains.jsonl are skipped, best_*.npy reloaded."""
import sys, os, json, time, argparse
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMBA_NUM_THREADS"): os.environ.setdefault(_v,"1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fastpol as F
from multiprocessing import Pool
ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('minutes', type=float); ap.add_argument('N', type=int, nargs='+')
ap.add_argument('--hops', type=int, default=120); ap.add_argument('--workers', type=int, default=os.cpu_count())
ap.add_argument('--data', default='data'); ap.add_argument('--table', required=True)
ap.add_argument('--T', type=float, default=2e-3); ap.add_argument('--ref', nargs='*', default=[], help='N=E overrides/extra reference energies')
a = ap.parse_args()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from thomson_check import parse_table
REF = {int(k): float(v) for k, v in parse_table(open(a.table).read()).items()}
for kv in a.ref: k, v = kv.split('='); REF[int(k)] = float(v)
SEEDS = ['warm', 'warm', 'warm', 'minus1', 'plus1', 'spiral', 'rsz', 'random']
def deeter(n):
    f = f'{a.data}/e.{n}.txt'; return F.load_pts(f) if os.path.exists(f) else None
def task(cid):
    n = a.N[cid % len(a.N)]; st = SEEDS[(cid // len(a.N)) % len(SEEDS)]; return cid, n, st
def seed(n, st, rng):
    if st == 'warm':
        P = deeter(n); 
        if P is None: st = 'spiral'
        else: return F.defect_kick(P, rng), st
    if st == 'minus1':   # from N+1, remove a point
        P = deeter(n+1); 
        if P is not None: return F.remove_point(P, rng), st
        st = 'plus1'
    if st == 'plus1':    # from N-1, add a point
        P = deeter(n-1)
        if P is not None: return F.add_point(P, rng), st
        st = 'spiral'
    if st == 'spiral': return F.spiral(n, offset=rng.uniform(0.2, 0.8), rng=rng, jitter=0.01), st
    if st == 'rsz': return F.norm(F.rsz_spiral(n)@np.linalg.qr(rng.normal(size=(3, 3)))[0] + rng.normal(scale=0.01, size=(n, 3))), st
    return F.random_pts(n, rng), st
DEADLINE = None
def chain(args):
    cid, n, st0, deadline = args; rng = np.random.default_rng(1000003*cid + 7)
    t0 = time.time(); P0, st = seed(n, st0, rng); P, E, _ = F.polish(P0); E0 = E; bestE, bestP = E, P; opts = 1; acc = 0
    for h in range(a.hops):
        if time.time() > deadline: break
        Q, En, _ = F.polish(F.defect_kick(P, rng)); opts += 1
        if En < E or rng.random() < np.exp(-(En-E)/a.T): P, E = Q, En; acc += 1
        if En < bestE: bestE, bestP = En, Q
    return dict(cid=cid, N=n, seed=st, opts=opts, acc=acc, E_start=E0, E_best=bestE, gap=bestE-REF.get(n, np.inf), secs=time.time()-t0), bestP
if __name__ == '__main__':
    os.makedirs(a.out, exist_ok=True); L = f'{a.out}/chains.jsonl'
    done = set(); best = {}
    if os.path.exists(L):
        for l in open(L): done.add(json.loads(l)['cid'])
    for n in a.N:
        f = f'{a.out}/best_{n}.npy'
        if os.path.exists(f): Q = np.load(f); best[n] = (F.energy(Q), Q)
    print(f'nproc={os.cpu_count()} workers={a.workers} resume_done={len(done)}', flush=True)
    deadline = time.time() + 60*a.minutes
    def handle(res, log):
        rec, Q = res; log.write(json.dumps(rec)+'\n'); log.flush(); n = rec['N']
        if n not in best or rec['E_best'] < best[n][0]:
            best[n] = (rec['E_best'], Q); np.save(f'{a.out}/best_{n}.tmp.npy', Q); os.replace(f'{a.out}/best_{n}.tmp.npy', f'{a.out}/best_{n}.npy')
        print(f"chain {rec['cid']} N={n} seed={rec['seed']} opts={rec['opts']} gap={rec['gap']:.3e} secs={rec['secs']:.1f}", flush=True)
    with Pool(a.workers) as pool, open(L, 'a') as log:
        pending = []; cid = 0
        while True:
            pending = [p for p in pending if not (p.ready() and (handle(p.get(), log) or True))]
            if time.time() < deadline - 2 and len(pending) < a.workers:
                if cid not in done: c, n, st = task(cid); pending.append(pool.apply_async(chain, ((c, n, st, deadline),)))
                cid += 1; continue
            if not pending and time.time() >= deadline - 2: break
            time.sleep(0.05)
    print('HUNT_DONE', flush=True)
