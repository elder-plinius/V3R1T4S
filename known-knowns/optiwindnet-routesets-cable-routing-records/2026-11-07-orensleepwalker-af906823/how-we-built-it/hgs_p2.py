"""Lens B: longer HGS-CVRP (radial) runs on p2 candidates. Own runs only; compares with the stored radial best."""
import argparse, json, pickle, sys, time, sqlite3
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import checks
from optiwindnet.db.model import open_database, RouteSet, NodeSet
from optiwindnet.db.storage import L_from_nodeset
from optiwindnet.api import HGSRouter
from optiwindnet.api_utils import parse_cables_input
from optiwindnet.mesh import make_planar_embedding
from optiwindnet.constraints import NetworkConstraints
ap = argparse.ArgumentParser(); ap.add_argument('--worklist', required=True); ap.add_argument('--time', type=float, default=240)
ap.add_argument('--seeds', default='1,2,3'); ap.add_argument('--deadline', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True); dl = datetime.fromisoformat(a.deadline).timestamp()
db = open_database('data/work.sqlite')
for line in open(a.worklist):
    nid_hex, cap = line.split()[:2]; cap = int(cap)
    ns = NodeSet.get(NodeSet.digest == bytes.fromhex(nid_hex))
    rows = [r for r in RouteSet.select().where((RouteSet.nodes == ns) & (RouteSet.capacity == cap)) if r.misc.get('topology') == 'radial']
    best = min(rows, key=lambda r: r.length)
    cons = NetworkConstraints(topology='radial', feeder_route='segmented', max_substation_feeders=tuple(best.feeders_per_root))
    for seed in [int(s) for s in a.seeds.split(',')]:
        if time.time() + a.time + 30 > dl: print(json.dumps({'event': 'deadline'}), flush=True); sys.exit(0)
        t = time.time()
        try:
            L = L_from_nodeset(ns); P, A = make_planar_embedding(L)
            _, G = HGSRouter(time_limit=a.time, seed=seed).route(P=P, A=A, cables=parse_cables_input(cap), cables_capacity=cap, constraints=cons)
        except Exception as e:
            print(json.dumps({'event': 'error', 'name': ns.name, 'cap': cap, 'seed': seed, 'err': str(e)[:200]}), flush=True); continue
        c = checks.full_check(G); fpr = [G.degree(r) for r in range(-G.graph['R'], 0)]
        hit = (c['length_euclid'] < best.length * (1 - 1e-6)) and not c['violations'] and not c['containment'] and all(f <= m for f, m in zip(fpr, best.feeders_per_root))
        rec = {'event': 'HIT' if hit else 'run', 'name': ns.name, 'T': ns.T, 'cap': cap, 'seed': seed, 'stored_radial_best': best.length, 'stored_id': best.id,
               'new_length': c['length_euclid'], 'delta_m': best.length - c['length_euclid'], 'feeders': fpr, 'cap_feeders': best.feeders_per_root,
               'violations': c['violations'], 'containment': c['containment'], 'seconds': round(time.time() - t, 1), 'utc': datetime.now(timezone.utc).isoformat()}
        print(json.dumps(rec, default=str), flush=True)
        if hit: pickle.dump(G, open(out / f'HIT-{ns.T}-{cap}-{seed}-{best.id}.pickle', 'wb'))
