"""PREREG.v15 R8 (S14 + S16 variant): ATT-corrected S16-minus-S14 arrival difference of a candidate vs the
median over the nest's catalogued events whose Dt exceeds the null maximum (else Dt >= 0.2).
Needs wfcache/att/xa.s12..att.<y>.<doy>.0.mseed and xa.s14..att... for the days involved (list printed if missing).

usage: att_check.py CANDIDATES.json SCAN.jsonl NEST ONSET_ISO
"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
import datetime as dt
from apollo_lib import NS, ns_iso
from att_moveout import true_time
from catalog_check import load_all, matches

cand = json.load(open(sys.argv[1])); nest = sys.argv[3]
days = [json.loads(l) for l in open(sys.argv[2])]
best = cand['summary'][nest]['best_control']
rows = load_all(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'data', 'catalog'))
peaks = [p for d in days for p in d['nests'][nest].get('fwd_peaks', [])]
target = int(np.datetime64(sys.argv[4].rstrip('Z'), 'ns').astype(np.int64))


def diff(p):
    t, D, ccs, l12, l14 = p
    a = true_time('s14', t + int(l12 * NS)); b = true_time('s16', t + int(l14 * NS))
    if a is None or b is None:
        d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t // NS)
        return None, 'missing ATT for %d-%03d' % (d.year, d.timetuple().tm_yday)
    return (b - a) / NS, None


cat = [p for p in peaks if [l for l in matches(rows, p[0] + 30 * NS) if ('N2=%s' % nest) in l]]
ref = [p for p in cat if p[1] > best] or [p for p in cat if p[1] >= 0.2]
vals, missing = [], []
for p in ref:
    v, m = diff(p)
    if v is None:
        missing.append(m)
    else:
        vals.append(v)
c = [p for p in peaks if abs(p[0] + 30 * NS - target) <= 60 * NS]
print('nest A%s: reference events %d (above null: %s), ATT-corrected S14-S12 differences: %s' % (
    nest, len(ref), bool([p for p in cat if p[1] > best]), [round(v, 2) for v in vals]))
print('missing ATT:', sorted(set(missing)))
if vals and c:
    v, m = diff(c[0])
    med = float(np.median(vals))
    print('candidate %s: S14-S12 = %s s; nest median %.2f s; within 2 s: %s' % (
        ns_iso(c[0][0] + 30 * NS), None if v is None else round(v, 2), med, None if v is None else abs(v - med) <= 2.0))
    if m:
        print('candidate', m)
