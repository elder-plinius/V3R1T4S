"""Score p2 on the frozen scan: recovery of catalogued A1 events of one year, false-alarm rate on the bank's
time-reversed null, chance recovery of shifted catalogue times, and a recall/false-alarm curve.

usage: score_p2.py FROZEN.npz SCAN.jsonl CATALOG.csv YEAR2 OUT_PREFIX
"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from apollo_lib import NS, day_start_ns, ns_iso
from evlib import load_nest_events

npz = np.load(sys.argv[1]); theta = float(npz['theta'])
days = [json.loads(l) for l in open(sys.argv[2])]
ev = load_nest_events(sys.argv[3], '1', [sys.argv[4]])
out = sys.argv[5]
ONSET = 30 * NS; TOL = 300 * NS
peaks = np.array([[p[0], p[1]] for d in days for p in d.get('fwd_peaks', [])], dtype=np.float64)
pt = peaks[:, 0].astype(np.int64) if len(peaks) else np.zeros(0, np.int64)
pv = peaks[:, 1] if len(peaks) else np.zeros(0)
order = np.argsort(pt); pt, pv = pt[order], pv[order]
cov = {}
for d in days:
    if d.get('coverage_per_min'):
        t0 = day_start_ns(d['year'], d['doy'])
        for k, c in enumerate(d['coverage_per_min']):
            cov[t0 // NS // 60 + k] = c
scanned_days = sum(d.get('scanned', 0.0) for d in days)
rev = np.array([v for d in days for v in d.get('rev_peaks', [])])


def best_near(tc):
    lo = np.searchsorted(pt, tc - TOL - ONSET); hi = np.searchsorted(pt, tc + TOL - ONSET, side='right')
    return float(pv[lo:hi].max()) if hi > lo else None


def scanned_near(tc):
    m0 = (tc - TOL - ONSET) // NS // 60; m1 = (tc + TOL - ONSET) // NS // 60
    return any(cov.get(m, 0.0) > 0 for m in range(int(m0), int(m1) + 1))


rows = []
for r in ev.itertuples():
    tc = int(r.t_ns)
    rows.append(dict(time=ns_iso(tc), Y=r.Y, JD=r.JD, S=r.S, A1=r.A1, A2=r.A2, scanned=scanned_near(tc),
                     best=best_near(tc)))
prim = [x for x in rows if x['scanned']]
rec_p = sum(1 for x in prim if x['best'] is not None and x['best'] >= theta)
rec_all = sum(1 for x in rows if x['best'] is not None and x['best'] >= theta)
far = float((rev >= theta).sum()) / scanned_days if scanned_days else None
# chance recovery: catalogue times shifted by random offsets of 1-10 days (either sign), 200 draws
rng = np.random.default_rng(20261112)
ch = []
for k in range(200):
    hits = 0; n = 0
    for x in rows:
        tc = int(np.datetime64(x['time'][:-1], 'ns').astype(np.int64))
        s = int(rng.uniform(1, 10) * 86400 * NS) * (1 if rng.random() < 0.5 else -1)
        t = tc + s
        if not scanned_near(t):
            continue
        n += 1
        b = best_near(t)
        hits += (b is not None and b >= theta)
    ch.append(hits / n if n else np.nan)
curve = []
for th in np.round(np.arange(0.06, 0.40, 0.01), 3):
    curve.append(dict(theta=float(th), recall_primary=sum(1 for x in prim if x['best'] is not None and x['best'] >= th) / len(prim),
                      far_per_day=float((rev >= th).sum()) / scanned_days))
res = dict(theta=theta, n_events=len(rows), n_primary=len(prim), recovered_primary=rec_p,
           recall_primary=rec_p / len(prim) if prim else None, recovered_all=rec_all, recall_all=rec_all / len(rows),
           scanned_day_equivalents=scanned_days, n_days=len(days), rev_detections_at_theta=int((rev >= theta).sum()),
           false_alarm_rate_per_day=far, chance_recovery_mean=float(np.nanmean(ch)), chance_recovery_max=float(np.nanmax(ch)),
           p2_met=bool(prim and rec_p / len(prim) >= 0.90))
json.dump(dict(result=res, events=rows, curve=curve), open(out + '.json', 'w'), indent=1)
with open(out + '.md', 'w') as f:
    f.write('# p2 scoring\n\n')
    for k, v in res.items():
        f.write('- %s: %s\n' % (k, v))
    f.write('\n| catalogued start (UTC) | A1 | A2 | scanned | best D within +/-5 min | recovered |\n|---|---|---|---|---|---|\n')
    for x in rows:
        f.write('| %s | %s | %s | %s | %s | %s |\n' % (x['time'], x['A1'], x['A2'], x['scanned'],
                'none' if x['best'] is None else '%.3f' % x['best'], x['best'] is not None and x['best'] >= theta))
    f.write('\n| theta | recall (primary) | false alarms per day (time-reversed) |\n|---|---|---|\n')
    for c in curve:
        f.write('| %.2f | %.3f | %.3f |\n' % (c['theta'], c['recall_primary'], c['far_per_day']))
print(json.dumps(res, indent=1))
