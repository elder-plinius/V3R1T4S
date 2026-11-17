"""Lens 3 seed triage (PREREG.v3): per nest, forward peaks whose best single-channel CC >= 0.6 at the D peak,
then R6 (all PDS tables) and the Onodera SP list. Writes per-nest npz files for the null stage of nests with
surviving seeds, and a summary.

usage: multinest_seeds.py TEMPLATES.npz SCAN.jsonl CATALOG_DIR LIT_DIR OUT_DIR
"""
import sys, os, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from apollo_lib import NS, ns_iso
from catalog_check import load_all, matches
import onodera_check

z = np.load(sys.argv[1]); days = [json.loads(l) for l in open(sys.argv[2])]
rows = load_all(sys.argv[3]); ono = onodera_check.load(sys.argv[4]); od = sys.argv[5]
os.makedirs(od, exist_ok=True)
nests = [str(n) for n in z['nests']]
summary = {}
surv = {}
for k, n in enumerate(nests):
    pk = [p for d in days for p in d.get('peaks', {}).get(n, [])]
    best_new = None; seeds = []
    for t, D, ccs in pk:
        onset = t + 30 * NS
        bc = max([c for c in ccs if c is not None] or [-1])
        cat = matches(rows, onset)
        if not cat:
            if best_new is None or bc > best_new[1]:
                best_new = (ns_iso(onset), bc, D)
            if bc >= 0.6:
                seeds.append(dict(onset=ns_iso(onset), t=t, D=D, ccs=ccs, best_cc=bc, onodera=onodera_check.matches(ono, onset)))
    summary[n] = dict(n_peaks=len(pk), n_new_cc_ge_0p6=len(seeds), best_new=best_new, seeds=seeds)
    if seeds:
        surv[n] = k
        np.savez(os.path.join(od, 'nest_A%s_templates.npz' % n), tm=z['tm'][k], chans=z['chans'], band=z['band'], L=z['L'],
                 theta=0.10897762490606308)
    print('A%s peaks %d, new seeds with CC>=0.6: %d, best new %s' % (n, len(pk), len(seeds), best_new))
json.dump(summary, open(os.path.join(od, 'seeds_summary.json'), 'w'), indent=1)
print('nests with seeds:', list(surv))
