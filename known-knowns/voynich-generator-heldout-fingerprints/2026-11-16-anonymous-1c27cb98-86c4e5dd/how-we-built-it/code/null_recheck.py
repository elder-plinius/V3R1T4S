#!/usr/bin/env python3
"""Re-check the falsifier's null (H1 vs 4000 quire-bootstrap controls x 4 cells).
Prints per-cell minima/quantiles and whether the pooled Naibbe H1 beats all controls.
Usage: python3 code/null_recheck.py  (expects output/preload_*.pkl + attempts/falsifier/output/naibbe_batch.json)
"""
import json, os, pickle, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from precompute import stat_pool
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN, 'output')
B, SEED = 4000, 20261116
def main():
    mins = {}
    for d in ('A','B'):
        for T in ('ZL3b','IT2a'):
            pl = pickle.load(open(os.path.join(OUT, f'preload_{d}_{T}.pkl'),'rb'))
            P,qo,bd = pl['P'], pl['qorder'], pl['boundaries']
            n = len(qo); rng = random.Random(SEED + 1000*ord(d) + 100*ord(T[0]) + len('H1'))
            vs = sorted(stat_pool('H1', P, qo, bd, [rng.randrange(n) for _ in range(n)]) for _ in range(B))
            mins[f'{d}_{T}'] = vs
    batch = json.load(open(os.path.join(RUN,'attempts','falsifier','output','naibbe_batch.json')))
    real = {'A': batch['pooled']['A']['stats']['H1'], 'B': batch['pooled']['B']['stats']['H1']}
    ok = True
    for d in ('A','B'):
        cellmin = min(mins[f'{d}_{T}'][0] for T in ('ZL3b','IT2a'))
        print(f"real {d} H1 = {real[d]:.4f}   min Voynich bootstrap ({d}) = {cellmin:.4f}   beats-all-controls = {real[d] < cellmin}")
        ok &= real[d] < cellmin
    print("RESULT:", "PASS (real beats all 16,000 controls)" if ok else "FAIL")
    sys.exit(0 if ok else 1)
if __name__ == '__main__':
    main()
