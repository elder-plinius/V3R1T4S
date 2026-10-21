"""Portable deterministic replay. Copy beside ddlib.py, sa2.py, constructor.py and covers.py."""
import argparse
import hashlib
import json
import time
from pathlib import Path

from constructor import build
from ddlib import adj_to_edges, edges_to_adj, exact_cost, load_edges_file_order, write_edges
from sa2 import sa2_run

ap = argparse.ArgumentParser()
ap.add_argument('plan',type=Path)
ap.add_argument('--out',type=Path,default=Path('rebuilt'))
ap.add_argument('--max-seconds',type=float,default=10800)
args = ap.parse_args()
plan = json.loads(args.plan.read_text())
base = args.plan.parent/'seed6631.edges'
assert hashlib.sha256(base.read_bytes()).hexdigest() == plan['baseline_sha256']
args.out.mkdir(exist_ok=False)
started = time.monotonic()
state, best_cost = build(base,13,4,args.out/'seed0',0)
valid = base
stale = 0
rounds = 0
for row in plan['trajectory']:
    assert time.monotonic()-started < args.max_seconds, 'Replay time limit'
    seed = row['seed']
    assert seed == 1000+rounds
    n, edges = load_edges_file_order(state)
    assert n == row['n'] and best_cost == row['start_cost']
    a,d = edges_to_adj(n,edges,13)
    best,aa,dd,*_ = sa2_run(a,d,n,4,13,5000,row['T0'],row['T1'],seed,.6,0.,.2,10**12,0)
    actual = int(exact_cost(aa,dd,n,4)[0])
    assert int(best) == actual == row['best_cost'], (seed,actual,row['best_cost'])
    if actual < best_cost:
        state = args.out/f'best_n{n}_s{seed}_c{actual}.edges'
        write_edges(state,adj_to_edges(aa,dd),f'local bounded annealing; N={n}; bad_pairs={actual}; seed={seed}')
        best_cost = actual
        stale = 0
    else:
        stale += 1
    rounds += 1
    print(json.dumps(dict(seed=seed,n=n,cost=actual,matches_measured=True)),flush=True)
    if actual == 0:
        valid = state
        if n == plan['target_n']:
            break
        state,best_cost = build(valid,13,4,args.out/f'reinsert{n+1}_s{seed+1}',seed+1)
        stale = 0
    elif stale >= 24 and seed+1 in plan['restart_seeds']:
        new,c = build(valid,13,4,args.out/f'restart_s{seed+1}',seed+1)
        if c < best_cost or rounds%96 == 0:
            state,best_cost = new,c
        stale = 0
sha = hashlib.sha256(valid.read_bytes()).hexdigest()
assert n == plan['target_n'] and best_cost == 0 and sha == plan['object_sha256']
receipt = dict(rebuild='PASS',n=n,seeds_checked=rounds,sha256=sha,seconds=time.monotonic()-started)
(args.out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt),flush=True)
