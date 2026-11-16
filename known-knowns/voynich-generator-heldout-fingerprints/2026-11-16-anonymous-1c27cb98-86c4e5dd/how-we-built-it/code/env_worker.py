#!/usr/bin/env python3
"""Envelope worker: one process per (stat, d, T). Reads the pickle preload,
runs B=4000 quire-bootstrap resamples, writes output/env_<stat>_<d>_<T>.json
with the 95% and 99.9% envelopes and the observed value.

Usage: env_worker.py <stat> <d> <T>
stats: S1 S2 S3 S4 S5 S6 S7 S8 S9 H1 H2 H3 H4
"""
from __future__ import annotations
import json, os, sys, time, random, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precompute import stat_pool

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN, 'output')
B = 4000
SEED = 20261116

def pct(vals, p):
    vs = sorted(vals)
    if not vs: return 0.0
    k = (len(vs)-1)*p/100.0
    f = int(k); c = min(f+1, len(vs)-1)
    return vs[f]*(c-k)+vs[c]*(k-f)

def main():
    stat, d, T = sys.argv[1], sys.argv[2], sys.argv[3]
    t0 = time.time()
    pl = pickle.load(open(os.path.join(OUT, f'preload_{d}_{T}.pkl'),'rb'))
    P, qorder, boundaries = pl['P'], pl['qorder'], pl['boundaries']
    n = len(qorder)
    rng = random.Random(SEED + 1000*ord(d) + 100*ord(T[0]) + len(stat))
    vals = []
    for b in range(B):
        keys = [rng.randrange(n) for _ in range(n)]
        v = stat_pool(stat, P, qorder, boundaries, keys)
        if isinstance(v, tuple):
            vals.append(v)
        else:
            vals.append(v)
    # envelopes per component
    out = {'stat':stat, 'd':d, 'T':T, 'B':B, 'n_quires':n, 'seed':SEED,
           'seconds': round(time.time()-t0,1)}
    if isinstance(vals[0], tuple):
        for i in range(len(vals[0])):
            comp_vals = [v[i] for v in vals]
            out[f'c{i}_mean'] = sum(comp_vals)/len(comp_vals)
            out[f'c{i}_95'] = [pct(comp_vals,2.5), pct(comp_vals,97.5)]
            out[f'c{i}_999'] = [pct(comp_vals,0.05), pct(comp_vals,99.95)]
    else:
        out['mean'] = sum(vals)/len(vals)
        out['envelope_95'] = [pct(vals,2.5), pct(vals,97.5)]
        out['envelope_999'] = [pct(vals,0.05), pct(vals,99.95)]
    json.dump(out, open(os.path.join(OUT, f'env_{stat}_{d}_{T}.json'),'w'), indent=1)
    print(f"env {stat}/{d}/{T} done in {out['seconds']}s", flush=True)

if __name__ == '__main__':
    main()
