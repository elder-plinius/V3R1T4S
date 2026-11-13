"""Run PREREG (this run): rebuild the S14 nest templates on the phase-1 decimation grid (every series starts one
6.625 Hz sample later) with the same builder and members rule, and find the best D within +/- 10 min of each seed;
report the per-channel CC at that peak next to the phase-0 values.
usage: phase1_check.py OUT.json"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import threadcap  # noqa: F401
import numpy as np
import apollo_lib
_orig = apollo_lib.preprocess


def preprocess_phase1(x, valid, band, dec=2, pad_s=20.0, do_despike=True):
    y, v = _orig(x, valid, band, dec=1, pad_s=pad_s, do_despike=do_despike)
    return (y[1::dec].copy(), v[1::dec].copy()) if dec > 1 else (y, v)


apollo_lib.preprocess = preprocess_phase1
import evlib  # noqa: E402  (binds the phase-1 preprocess)
from evlib import load_nest_events, DayCache, event_block, best_lag, FS  # noqa: E402
from nesttemplates2 import build, _clean  # noqa: E402
from apollo_lib import NS, ns_iso  # noqa: E402
assert evlib.preprocess is preprocess_phase1
CAT = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'data', 'catalog', 'levent.1008weber.csv')
band = (0.25, 1.0, 0.1); L = 450.0; M = int(round(L * FS)); chans = [('s14', 'mh1'), ('s14', 'mh2')]
cache = DayCache(band)
seeds = {'201': ('1971-08-17T05:55:22.566', [0.5642, 0.7036], 0.6339), '39': ('1971-09-05T01:25:44.150', [0.5952, 0.6925], 0.6439)}
res = {}
for n, (ws, cc0, d0) in seeds.items():
    ev = load_nest_events(CAT, n, ['71'])
    amp = ev['A1n'].clip(lower=0).fillna(0) + ev['A2n'].clip(lower=0).fillna(0)
    clean = []
    for i, r in ev.iterrows():
        blk = event_block(cache, chans, int(r['t_ns']), M)
        clean.append(all(y is not None and v.mean() > 0.95 and _clean(y) for y, v in blk))
    ref = int(amp.where(clean, -1).idxmax())
    b = build(ev, chans, band, L, ref, cache=cache)
    t = int(np.datetime64(ws, 'ns').astype(np.int64))
    p = best_lag(cache, chans, b['tm'], t - 600 * NS, t + 600 * NS)
    res[n] = dict(seed_window_start_phase0=ws, phase0_ccs=cc0, phase0_D=d0, phase1_members=len(b['members']),
                  phase1_D=round(p[0], 4), phase1_window_start=ns_iso(p[1]), phase1_ccs=[round(float(c), 4) for c in p[2]],
                  phase1_offset_s=round((p[1] - t) / NS, 2))
    r = res[n]
    r['min_best_cc_over_phases'] = round(min(max(cc0), max(r['phase1_ccs'])), 4)
    print('A%s: phase 0 CC %s (D %.3f); phase 1 (%d members) CC %s (D %.3f) at %+.2f s; min over phases of best CC %.4f' % (
        n, cc0, d0, r['phase1_members'], r['phase1_ccs'], r['phase1_D'], r['phase1_offset_s'], r['min_best_cc_over_phases']), flush=True)
q = [n for n in res if res[n]['min_best_cc_over_phases'] >= 0.6]
choice = max(q, key=lambda n: res[n]['min_best_cc_over_phases']) if q else None
print('declared rule -> claimed seed:', 'A' + choice if choice else 'none (no seed >= 0.6 under both phases)')
json.dump(dict(results=res, choice=choice), open(sys.argv[1], 'w'), indent=1)
