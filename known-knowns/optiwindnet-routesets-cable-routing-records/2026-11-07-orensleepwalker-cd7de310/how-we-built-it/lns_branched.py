"""Fix-and-optimise large-neighbourhood search for branched cable routing (Claude Code, 2026-11-06).
Incumbent = the instance's stored best (or our own improved set). Each iteration: build optiwindnet's MILP model
(ortools CP-SAT) warm-started from the incumbent; pin the outgoing link of every turbine outside a window of k nearby
turbines; solve briefly; route detours; accept only if the final Euclidean length (detours included) is shorter and
the result passes validate_routeset and the border/obstacle checks. Seeds: own RNG; no external solutions are used."""
import argparse, json, math, pickle, sys, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np, networkx as nx
sys.path.insert(0, str(Path(__file__).resolve().parent)); import checks
from optiwindnet.db.model import open_database, RouteSet, NodeSet
from optiwindnet.db.storage import G_from_routeset, L_from_nodeset
from optiwindnet.converting import S_from_G
from optiwindnet.mesh import make_planar_embedding
from optiwindnet.MILP import solver_factory
from optiwindnet.constraints import NetworkConstraints

ap = argparse.ArgumentParser(); ap.add_argument('--name'); ap.add_argument('--cap', type=int); ap.add_argument('--k', type=int, default=14)
ap.add_argument('--sub-time', type=float, default=20); ap.add_argument('--deadline'); ap.add_argument('--seed', type=int, default=1); ap.add_argument('--out'); ap.add_argument('--start-from-shortest', action='store_true')
a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True); rng = np.random.default_rng(a.seed)
dl = datetime.fromisoformat(a.deadline).timestamp()
open_database('data/work.sqlite'); ns = NodeSet.get(NodeSet.name == a.name)
rows = list(RouteSet.select().where((RouteSet.nodes == ns) & (RouteSet.capacity == a.cap)).order_by(RouteSet.length))
best_any = rows[0]; br = [r for r in rows if r.misc.get('topology') == 'branched']; best_br = min(br, key=lambda r: r.length)
fcap = tuple(best_any.feeders_per_root)                       # criterion: <= the shortest stored set's feeders
cons = NetworkConstraints(topology='branched', feeder_route='segmented', max_substation_feeders=fcap)
L = L_from_nodeset(ns); P, A = make_planar_embedding(L); T, R = L.graph['T'], L.graph['R']; VC = L.graph['VertexC']
G = G_from_routeset(best_any if a.start_from_shortest else best_br); S = S_from_G(G); cur = checks.euclid_length(G); target = best_any.length
print(json.dumps({'event': 'start', 'name': a.name, 'cap': a.cap, 'start_len': cur, 'stored_best_any': target, 'stored_best_topology': best_any.misc.get('topology'), 'feeder_cap': fcap, 'utc': datetime.now(timezone.utc).isoformat()}), flush=True)
def parents(S):
    par = {}
    for r in range(-R, 0):
        for u, v in nx.bfs_edges(S, r): par[v] = u
    return par
it = 0
while time.time() + a.sub_time + 15 < dl:
    it += 1; par = parents(S); seed_t = int(rng.integers(T)); d = np.hypot(*(VC[:T] - VC[seed_t]).T)
    k = int(rng.integers(max(6, a.k - 6), a.k + 7)); W = set(np.argsort(d)[:k].tolist())
    t0 = time.time()
    try:
        solver = solver_factory('ortools.cp_sat')
        solver.set_problem(P, A, constraints=cons, capacity=a.cap, warmstart=S)
        lk = solver.metadata.link_; fixed = 0
        for t in range(T):
            if t in W: continue
            key = (t, par[t])
            if key in lk: lk[key].lower_bound = 1; fixed += 1
        solver.solve(time_limit=a.sub_time, mip_gap=0.0, options={'num_workers': 1})
        S2, G2 = solver.get_solution()
    except Exception as e:
        print(json.dumps({'event': 'error', 'it': it, 'err': str(e)[:200]}), flush=True); continue
    new = checks.euclid_length(G2)
    rec = {'event': 'iter', 'it': it, 'k': k, 'fixed': fixed, 'len': new, 'cur': cur, 'sec': round(time.time() - t0, 1)}
    if new < cur - 1e-6:
        c = checks.full_check(G2); fpr = [G2.degree(r) for r in range(-R, 0)]
        if not c['violations'] and not c['containment'] and all(f <= m for f, m in zip(fpr, fcap)):
            cur, S, G = new, S2, G2; rec['event'] = 'IMPROVED'; rec['feeders'] = fpr
            pickle.dump(G, open(out / 'best.pickle', 'wb')); json.dump({'len': cur, 'it': it, 'utc': datetime.now(timezone.utc).isoformat()}, open(out / 'best.json', 'w'))
            if cur < target * (1 - 1e-6): rec['event'] = 'RECORD'
        else:
            rec['event'] = 'rejected'; rec['why'] = (c['violations'][:2], c['containment'][:2], fpr)
    print(json.dumps(rec, default=str), flush=True)
print(json.dumps({'event': 'complete', 'iters': it, 'final': cur, 'stored_best_any': target, 'utc': datetime.now(timezone.utc).isoformat()}), flush=True)
