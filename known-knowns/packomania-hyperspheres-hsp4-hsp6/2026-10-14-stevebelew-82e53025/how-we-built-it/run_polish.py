"""Lens warm-polish: start from the POSTED coordinates of row N, SLP-polish, then basin-hop with kicks of the loosest balls.
Usage: run_polish.py <deadline_seconds> <workers> N1 N2 ...   (output: output/polish_<N>.txt and output/log.txt)"""
import sys, os, time, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from slp_pack import rstar, slp, basin_hop, write_coords
from multiprocessing import Pool
RUN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
TABLE = {int(l.split()[0]): float(l.split()[1]) for l in open(os.path.join(RUN, 'data/hsp4_radius.txt')) if l.strip()}
T0 = time.time(); DEADLINE = T0 + float(sys.argv[1])

def posted(N):
    rows = [l.split() for l in open(os.path.join(RUN, 'data/coords/hsp4-%d.txt' % N)) if len(l.split()) >= 4]
    return np.array([[float(v) for v in r[-4:]] for r in rows])

def work(N):
    if time.time() > DEADLINE: return (N, 'skipped: deadline')
    rng = np.random.default_rng(1000 + N)
    X0 = posted(N); r0, _, _ = rstar(X0); rt = TABLE[N]
    X1, r1 = slp(X0.copy())
    per_N = min(240.0, max(30.0, (DEADLINE - time.time()) / 4))
    X2, r2 = basin_hop(X1, rng, hops=10 ** 6, k=max(2, N // 40), amp=1.0, deadline=min(DEADLINE, time.time() + per_N), time=time.time)
    best_r, best_X = (r2, X2) if r2 >= r1 else (r1, X1)
    gain = best_r - rt
    write_coords(os.path.join(OUT, 'polish_%d.txt' % N), best_X, header='# N=%d r_float=%.17g table=%.12f gain=%.3e' % (N, best_r, rt, gain))
    tag = 'CANDIDATE' if gain >= 1e-10 else ('near-miss' if gain > 1e-12 else 'no gain')
    return (N, 'table=%.12f posted_r=%.15f polished=%.15f hopped=%.15f gain=%.3e %s' % (rt, r0, r1, r2, gain, tag))

if __name__ == '__main__':
    Ns = [int(a) for a in sys.argv[3:]]
    with Pool(int(sys.argv[2])) as p:
        for N, msg in p.imap_unordered(work, Ns):
            with open(os.path.join(OUT, 'log.txt'), 'a') as f: f.write('%s N=%d %s\n' % (time.strftime('%H:%M:%S', time.gmtime()), N, msg))
            print(N, msg, flush=True)
    print('POLISH_DONE elapsed=%.0fs' % (time.time() - T0), flush=True)
