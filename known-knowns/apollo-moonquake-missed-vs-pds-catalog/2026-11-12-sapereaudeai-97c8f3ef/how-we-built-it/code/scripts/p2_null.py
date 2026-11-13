"""PREREG.v6 null test for p2: 400 shifted catalogues, same recall computation; writes null_test.md lines.

usage: p2_null.py FROZEN.npz SCAN.jsonl CATALOG.csv YEAR2 OUT.md
"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from apollo_lib import NS, day_start_ns
from evlib import load_nest_events

npz = np.load(sys.argv[1]); theta = float(npz['theta'])
days = [json.loads(l) for l in open(sys.argv[2])]
ev = load_nest_events(sys.argv[3], '1', [sys.argv[4]])
ONSET = 30 * NS; TOL = 300 * NS
pk = sorted((p[0], p[1]) for d in days for p in d.get('fwd_peaks', []))
pt = np.array([p[0] for p in pk], dtype=np.int64); pv = np.array([p[1] for p in pk])
cov = {}
for d in days:
    if d.get('coverage_per_min'):
        t0 = day_start_ns(d['year'], d['doy'])
        for k, c in enumerate(d['coverage_per_min']):
            cov[t0 // NS // 60 + k] = c


def scanned(tc):
    m0 = (tc - TOL - ONSET) // NS // 60; m1 = (tc + TOL - ONSET) // NS // 60
    return any(cov.get(m, 0.0) > 0 for m in range(int(m0), int(m1) + 1))


def hit(tc):
    lo = np.searchsorted(pt, tc - TOL - ONSET); hi = np.searchsorted(pt, tc + TOL - ONSET, side='right')
    return hi > lo and pv[lo:hi].max() >= theta


def recall(times):
    s = [t for t in times if scanned(t)]
    return (sum(hit(t) for t in s) / len(s)) if s else float('nan'), len(s)


real, nreal = recall([int(t) for t in ev['t_ns']])
ctrl = []
for k in range(1, 401):
    rng = np.random.default_rng(20261113 + k)
    sh = rng.uniform(1, 10, len(ev)) * 86400 * np.where(rng.random(len(ev)) < 0.5, -1, 1)
    r, n = recall([int(t) + int(s * NS) for t, s in zip(ev['t_ns'], sh)])
    ctrl.append(r)
ctrl = np.array(ctrl)
best = float(np.nanmax(ctrl))
lines = ['# null_test (p2, PREREG.v6): shifted-catalogue controls', '',
         'controls: %d' % int(np.sum(~np.isnan(ctrl))),
         'best_control: %.4f' % best,
         'real: %.4f' % real,
         'real_beats_all_controls: %s' % ('yes' if real > best else 'no'),
         'command: python -I attempts/evaluator-first/code/p2_null.py '
         'attempts/evaluator-first/frozen/A1_s12_dev1972_templates.npz attempts/evaluator-first/out/scan_1971/scan_s12_A1_1971.jsonl '
         'data/catalog/levent.1008weber.csv 71 null_test.md', '',
         'real recall over %d scanned catalogued 1971 A1 times; control recall mean %.4f, median %.4f, max %.4f.' % (
             nreal, float(np.nanmean(ctrl)), float(np.nanmedian(ctrl)), best),
         'theta (frozen) = %.6f' % theta]
open(sys.argv[5], 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
