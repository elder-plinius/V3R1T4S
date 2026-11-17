"""Claim run a100_1030, A6b (descriptive, written AFTER the PREREG freeze and after seeing A6; gates nothing):
the A6 specificity count extended from catalogued deep moonquakes (T2 = A) to every 1973 levent row of any type
(impacts, shallow events, unclassified), streaming the A100 forward peaks of the N0 rerun.
Same scoring as A6: the A100 forward peak with onset in [start - 5 min, start + 10 min]; pass = Dt above the N0 A100
best control, best channel >= 0.5 at S14 and at S16 (R7), and phase in the A100 interval (R9).

usage: a6b_all_types.py TOOLS_DIR SCAN12.jsonl LEVENT.csv N0.json
"""
import sys, json
sys.path.insert(0, sys.argv[1])
import numpy as np
import pandas as pd
from ephem import mean_anomaly_deg

NS = 1_000_000_000
n0 = json.load(open(sys.argv[4])); best = n0['N0']['best_control']; iv = n0['A6']['phase_interval']
inv = (lambda p: iv[0] <= p <= iv[1]) if iv[0] <= iv[1] else (lambda p: p >= iv[0] or p <= iv[1])
pk = []
for l in open(sys.argv[2]):
    d = json.loads(l)
    pk += [p for p in d['nests']['100']['fwd_peaks']]
pt = np.array([p[0] + 30 * NS for p in pk], dtype=np.int64); o = np.argsort(pt); pt = pt[o]; pk = [pk[i] for i in o]
cat = pd.read_csv(sys.argv[3], dtype=str)
c = cat[cat['Y'] == '73'].copy()
day0 = np.datetime64('1973-01-01T00:00', 'ns').astype(np.int64)
c['t'] = [int(day0 + ((int(r.JD) - 1) * 86400 + int(str(r.S).zfill(4)[:2]) * 3600 + int(str(r.S).zfill(4)[2:]) * 60) * NS) for r in c.itertuples()]
c['T2'] = c['T2'].fillna('?').str.strip()
out = {}
for r in c.itertuples():
    a = np.searchsorted(pt, r.t - 300 * NS); b = np.searchsorted(pt, r.t + 600 * NS, side='right')
    rec = out.setdefault(r.T2, dict(n=0, scored=0, above_null=0, above_null_R7=0, passes=0, hits=[]))
    rec['n'] += 1
    if b <= a:
        continue
    k = a + int(np.argmax([pk[j][1] for j in range(a, b)])); p = pk[k]
    rec['scored'] += 1
    s14 = max([x for x in p[2][:2] if x is not None] or [-1]); s16 = max([x for x in p[2][2:] if x is not None] or [-1])
    ph = float(mean_anomaly_deg(p[0] + 30 * NS))
    if p[1] > best:
        rec['above_null'] += 1
        rec['hits'].append('73-%s %s T2=%s N2=%s Dt %.4f S14 %.3f S16 %.3f R9 %s' % (r.JD, str(r.S).zfill(4), r.T2, str(r.N2).strip(), p[1], s14, s16, inv(ph)))
        if s14 >= 0.5 and s16 >= 0.5:
            rec['above_null_R7'] += 1
            if inv(ph):
                rec['passes'] += 1
for t2, rec in sorted(out.items()):
    print('T2=%s: rows %d, with a forward peak %d, above the A100 null %d, + R7 %d, + R9 %d %s' % (
        t2, rec['n'], rec['scored'], rec['above_null'], rec['above_null_R7'], rec['passes'], rec['hits'] if t2 != 'A' or rec['above_null'] < 8 else '(A100 rows listed in n0_stdout)'))
