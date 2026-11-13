"""PREREG (claim run a100_1030) A3 / C3 decision and the descriptive 1973 time series of S16 MH2 response.

usage: a3_decide.py S16_RESPONSE.jsonl
"""
import sys, json
import numpy as np

rows = [json.loads(l) for l in open(sys.argv[1])]
cand = [r for r in rows if r['label'] == 'CANDIDATE'][0]
ev = [r for r in rows if r['label'] != 'CANDIDATE']
H = 3600 * 10 ** 9
tc = cand['t0']
print('candidate: R_MH1 %.3f R_MH2 %.3f r2 %s' % (cand['mh1']['R'], cand['mh2']['R'], cand['r2']))


def refs(span_h):
    return [r for r in ev if r['r2'] is not None and abs(r['t0'] - tc) <= span_h * H]


state = {}
for side in ('before', 'after'):
    for span in (12, 48):
        rr = [r for r in refs(span) if (r['t0'] < tc if side == 'before' else r['t0'] > tc)]
        if rr:
            r = min(rr, key=lambda r: abs(r['t0'] - tc))
            state[side] = dict(event=r['label'], t0=r['t0_iso'], R1=round(r['mh1']['R'], 3), R2=round(r['mh2']['R'], 3),
                               r2=r['r2'], window_h=span)
            break
print('nearest reference before:', state.get('before'))
print('nearest reference after:', state.get('after'))
print('all reference events within +/- 12 h (R_MH1 >= 1.5, valid):')
for r in sorted(refs(12), key=lambda r: r['t0']):
    print('   %s %s R1 %.2f R2 %.2f r2 %.3f flags16 %s' % (r['t0_iso'], r['label'], r['mh1']['R'], r['mh2']['R'], r['r2'], r.get('flags16')))
b, a = state.get('before'), state.get('after')
if b is None or a is None:
    verdict = 'inconclusive (no reference on a side within 48 h)'
elif b['r2'] <= 0.25 and a['r2'] <= 0.25:
    verdict = 'S16 MH2 unresponsive at the candidate time: its S16 MH2 null is explained, no contradiction (C3 does not hold)'
elif b['r2'] >= 0.5 and a['r2'] >= 0.5 and (cand['r2'] is not None and cand['r2'] < 0.25 or cand['r2'] is None and cand['mh2']['R'] < 1.2):
    verdict = 'C3 holds (S16 MH2 responsive around the candidate but not for it)'
else:
    verdict = 'inconclusive'
print('A3 verdict:', verdict)

# descriptive: monthly medians of r2 over 1973 and the other new detections
print('\nr2 of 1973 levent rows with R_MH1 >= 1.5 (valid), by 30-day block: n, median, fraction r2 <= 0.25')
day0 = np.datetime64('1973-01-01T00:00', 'ns').astype(np.int64)
good = [r for r in ev if r['r2'] is not None]
for k in range(0, 365, 30):
    rr = [r['r2'] for r in good if k <= (r['t0'] - day0) / 86400e9 < k + 30]
    if rr:
        print('   days %3d-%3d: n %3d median %6.3f frac<=0.25 %.2f' % (k + 1, k + 30, len(rr), np.median(rr), np.mean(np.array(rr) <= 0.25)))
for lab, iso in (('1973-01-30 23:06 (new, A100-like)', '1973-01-30T23:06:52'), ('1973-10-30 02:25 (candidate of this run)', '1973-10-30T02:25:51'),
                 ('1973-11-26 07:46 (first claimed event)', '1973-11-26T07:46:28')):
    t = int(np.datetime64(iso, 'ns').astype(np.int64))
    rr = sorted([r for r in good if abs(r['t0'] - t) <= 24 * H], key=lambda r: r['t0'])
    print('%s: reference events within +/- 24 h: n %d, r2 values %s' % (lab, len(rr), [round(r['r2'], 2) for r in rr]))
a100 = sorted([r for r in ev if r.get('N2') == '100' and r.get('T2') == 'A'], key=lambda r: r['t0'])
print('\ncatalogued 1973 A100 events: R_MH1, R_MH2, r2, and the median r2 of reference events within +/- 24 h')
for r in a100:
    rr = [x['r2'] for x in good if abs(x['t0'] - r['t0']) <= 24 * H and x is not r]
    print('   %s R1 %s R2 %s r2 %s | nearby median r2 %s (n %d)' % (
        r['t0_iso'], None if not r['mh1'] or r['mh1']['R'] is None else round(r['mh1']['R'], 2), None if not r['mh2'] or r['mh2']['R'] is None else round(r['mh2']['R'], 2),
        r['r2'], None if not rr else round(float(np.median(rr)), 3), len(rr)))
