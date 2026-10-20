#!/usr/bin/env python3
"""Resume the screened annealing sa2.sa2_run (unchanged) from a saved near-miss state at LOW temperature, one seed
after the other; stop at cost 0 and write the graph. The state is read in FILE order (ddlib.load_edges_file_order).
Each seed writes OUT_PREFIX_s<seed>_c<cost>.edges; if a seed lowers the cost, the next seed starts from its state.

The (13,4) N=6630 graph (deterministic, about 2.5-3.5 minutes on one core):
  sa2_resume.py near_c134_N6630_s13064_c2.edges 13 4 OUT/sa2c2 --iters 250000 --T0 0.12 --T1 0.02 --seeds 101
  -> OUT/sa2c2_s101_c0.edges, sha256 7c44e128901d6dd6b64e0574b90ff8aa21872462338fd267bab466cb268e10a4
     (the header line names the input file's basename, so name the input exactly as above for a byte-identical file)
"""
import os, sys, time, argparse, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ddlib import load_edges_file_order, edges_to_adj, adj_to_edges, exact_cost
from sa2 import sa2_run


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def write_edges(path, E, header=None):
    with open(path, 'w') as f:
        if header:
            f.write('# ' + header + '\n')
        for a, b in E:
            f.write(f'{int(a)} {int(b)}\n')
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('state'); ap.add_argument('Delta', type=int); ap.add_argument('D', type=int); ap.add_argument('out')
ap.add_argument('--iters', type=int, default=300000); ap.add_argument('--T0', type=float, default=0.15)
ap.add_argument('--T1', type=float, default=0.02); ap.add_argument('--seeds', default='101,102,103,104,105,106')
ap.add_argument('--p_target', type=float, default=0.6); ap.add_argument('--p_free', type=float, default=0.2)
a = ap.parse_args()
n, E = load_edges_file_order(a.state)
adj0, deg0 = edges_to_adj(n, E, a.Delta)
c0 = int(exact_cost(adj0, deg0, n, a.D)[0])
log(f'start {os.path.basename(a.state)}: N={n} cost={c0} free={int(a.Delta * n - deg0.sum())}')
cur_E = E
for s in [int(x) for x in a.seeds.split(',')]:
    adj, deg = edges_to_adj(n, cur_E, a.Delta)
    t0 = time.time()
    best, badj, bdeg, acc, nfull, nscr = sa2_run(adj, deg, n, a.D, a.Delta, a.iters, a.T0, a.T1, s, a.p_target, 0.0, a.p_free, int(1e12), 0)
    E2 = adj_to_edges(badj, bdeg)
    a2, d2 = edges_to_adj(n, E2, a.Delta)
    c2 = int(exact_cost(a2, d2, n, a.D)[0])
    log(f'seed {s}: sa2 best {best} (fresh re-eval {c2}) acc {acc} full {nfull} screened {nscr} maxdeg {bdeg.max()} '
        f'free {int(a.Delta*n - bdeg.sum())} {time.time()-t0:.0f}s')
    sha = write_edges(a.out + f'_s{s}_c{c2}.edges', E2, f'({a.Delta},{a.D}) N={n} cost={c2}; sa2_resume seed {s} from {os.path.basename(a.state)}')
    if c2 == 0:
        log(f'VALID N={n} -> {a.out}_s{s}_c0.edges sha256 {sha}')
        break
    if c2 < c0:
        cur_E = E2; c0 = c2
        log(f'  warm start moved to cost {c2}')
log('done')
