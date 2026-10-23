#!/usr/bin/env python3
"""Collect the best verified result per format over all sweep passes -> sweep.csv (+ best.json index)."""
import json, glob, os, csv
A = '[addcomp]/'
T = json.load(open(A + 'data/targets.json'))
best = {}
for s in glob.glob(A + 'work/*/*_m*/summary.json'):
    d = json.load(open(s))
    if not d.get('valid'): continue
    k = (d['format'], d['rank'])
    secs = d.get('secs', 0)
    b = best.setdefault(k, dict(ours=10**9, secs_total=0, dir=None, perminov=d['perminov']))
    b['secs_total'] += secs
    if d['ours'] < b['ours']:
        b.update(ours=d['ours'], dir=os.path.dirname(s), maps=d['ours_maps'], pmaps=d['perminov_maps'], source=d.get('source'))
rows = []
for t in sorted(T, key=lambda t: (max(t['fmt']), t['rank'])):
    f = 'x'.join(map(str, t['fmt'])); k = (f, t['rank']); b = best.get(k)
    if b is None:
        rows.append([f, t['rank'], t['cr'], '', '', '', 'excluded: claimed by PR #149 (calibration run gave 470, see NOTES.md)' if f == '4x6x7' else 'not searched: Perminov count equals the simple per-map lower bound']); continue
    rows.append([f, t['rank'], t['cr'], b['ours'], t['cr'] - b['ours'], round(b['secs_total']), '%s U%d V%d W%d (Perminov U%d V%d W%d)' % (
        os.path.relpath(b['dir'], A), *b['maps'], *b['pmaps'])])
with open(A + 'sweep.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['format', 'rank', 'perminov_cr_min', 'ours', 'margin', 'seconds', 'note'])
    w.writerows(rows)
json.dump({'%s_m%d' % k: v for k, v in best.items()}, open(A + 'work/best_index.json', 'w'), indent=1)
for r in rows: print(r[:6])
