"""Build the package object files for the second A100 full-criterion candidate, 1973-10-30 (claim run a100_1030; run only after a CONFIRMED gate).

usage: build_object.py CLAIM_DIR OUT_OBJECT_DIR
Writes candidate.json, window_and_template.csv, null_full_span_maxima.csv, null_daily_maxima.csv,
a100_catalogue_times.csv and r8_reference.csv from the claim's frozen files and waveforms (frozen pipeline).
"""
import sys, os, json, csv
CLAIM, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(CLAIM, 'code', 'tools'))
import threadcap  # noqa: F401
import numpy as np
import pandas as pd
from apollo_lib import NS, day_start_ns, ns_iso, cat_time_ns
from evlib import FS
from scan import prep_day
from att_moveout import true_time
from catalog_check import load_all, matches
from ephem import mean_anomaly_deg, solar_elevation_deg, STATIONS

os.makedirs(OUT, exist_ok=True)
WS = int(np.datetime64('1973-10-30T02:25:21.509', 'ns').astype(np.int64))
z = np.load(os.path.join(CLAIM, 'frozen', 'nets25_1973_A100.npz'))
TM = z['tm'][0]; CH = [tuple(c.split('.')) for c in z['chans']]; M = TM.shape[1]
pp = prep_day(1973, 303, CH, (0.25, 1.0, 0.1), M)
i_ws = int(round((WS - day_start_ns(1973, 303)) / NS * FS))
K = 7
cols = ['s14_mh1', 's14_mh2', 's16_mh1', 's16_mh2']
data = [pp[k][0][i_ws - K:i_ws + K + M].astype(float) for k in range(4)]
valid = [pp[k][1][i_ws - K:i_ws + K + M] for k in range(4)]
assert all(v.mean() == 1.0 for v in valid)
with open(os.path.join(OUT, 'window_and_template.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['sample'] + ['template_' + c for c in cols] + ['data_' + c for c in cols])
    for i in range(M + 2 * K):
        j = i - K
        tr = ['%.9e' % TM[k][j] if 0 <= j < M else '' for k in range(4)]
        w.writerow([j] + tr + ['%.9e' % data[k][i] for k in range(4)])

# null maxima from the frozen full-year A100 scan
days = []
for _l in open(os.path.join(CLAIM, 'results', 'scan12_1973.jsonl')):  # stream: keep only the A100 entry of each day
    _d = json.loads(_l); _d['nests'] = {'100': _d['nests']['100']}; days.append(_d)
rev = max(d['nests']['100']['rev_max'] for d in days if d['nests']['100']['rev_max'] is not None)
sh = np.full(400, -np.inf)
for d in days:
    s = d['nests']['100']['shift_max']
    for k, v in enumerate(s):
        if v is not None:
            sh[k] = max(sh[k], v)
with open(os.path.join(OUT, 'null_full_span_maxima.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['control', 'shift_s', 'full_span_max'])
    w.writerow(['C0_time_reversed', '', '%.5f' % rev])
    for k in range(400):
        w.writerow(['C%d_S16_rolled' % (k + 1), 3600 + 180 * k, '%.5f' % sh[k]])
with open(os.path.join(OUT, 'null_daily_maxima.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['doy', 'forward_max', 'reversed_max', 'best_shift_max'])
    for d in days:
        n = d['nests']['100']
        fm = max([p[1] for p in n['fwd_peaks']] or [float('nan')])
        sm = max([v for v in n['shift_max'] if v is not None] or [float('nan')])
        w.writerow([d['doy'], '%.5f' % fm, '%.5f' % (n['rev_max'] if n['rev_max'] is not None else float('nan')), '%.5f' % sm])

# A100 catalogue times (R9) and R8 references
cat = pd.read_csv(os.path.join(CLAIM, 'data', 'catalog', 'levent.1008weber.csv'), dtype=str)
a = cat[(cat['T2'] == 'A') & (cat['N2'].str.strip() == '100')]
with open(os.path.join(OUT, 'a100_catalogue_times.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['levent_Y', 'JD', 'S', 'utc'])
    for r in a.itertuples():
        w.writerow([r.Y, r.JD, r.S, ns_iso(cat_time_ns(r.Y, r.JD, r.S))])
cj = json.load(open(os.path.join(CLAIM, 'results', 'cand12.json')))
best = cj['summary']['100']['best_control']
rows = load_all(os.path.join(CLAIM, 'data', 'catalog'))
peaks = [p for d in days for p in d['nests']['100'].get('fwd_peaks', [])]
refs = [p for p in peaks if p[1] > best and [l for l in matches(rows, p[0] + 30 * NS) if 'N2=100' in l]]
with open(os.path.join(OUT, 'r8_reference.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['window_start_utc', 'Dt', 'lag_s14_s', 'lag_s16_s', 'att_s16_minus_s14_s'])
    vals = []
    for p in refs:
        t, D, _, l14, l16 = p
        aa = true_time('s14', t + int(l14 * NS)); bb = true_time('s16', t + int(l16 * NS))
        v = (bb - aa) / NS
        vals.append(v)
        w.writerow([ns_iso(t), D, l14, l16, '%.4f' % v])
c = [p for p in peaks if abs(p[0] - WS) <= 60 * NS][0]
t, D, ccs, l14, l16 = c
a14 = true_time('s14', t + int(l14 * NS)); a16 = true_time('s16', t + int(l16 * NS))
cand_diff = (a16 - a14) / NS
off14 = (a14 - (t + int(l14 * NS))) / NS; off16 = (a16 - (t + int(l16 * NS))) / NS
on = WS + 30 * NS
cand = dict(
    target_id='apollo-moonquake-missed-vs-pds-catalog', claim='full success criterion (deep moonquake, nest A100)',
    nest='A100 (levent.1008weber.csv T2 = A, N2 = 100)', stations=['S14', 'S16'],
    channels={'S14': ['MH1', 'MH2'], 'S16': ['MH1', 'MH2']}, location='00',
    time_base='MiniSEED (Earth-received, nominal-rate) times of the PDS restoration',
    window_start_utc=ns_iso(WS), onset_utc=ns_iso(on), window_s=450.0, sample_rate_hz=FS,
    lag_tolerance_samples=K, frozen_scan_peak=dict(Dt=D, ccs=ccs, lag_s14_s=l14, lag_s16_s=l16),
    null_controls=401, null_span='1973 days 1-365 (all of 1973)', null_c0_time_reversed_full_span_max=round(float(rev), 5),
    null_best_shift_full_span_max=round(float(sh.max()), 5),
    r8=dict(att_offset_s14_s=round(off14, 4), att_offset_s16_s=round(off16, 4), candidate_s16_minus_s14_s=round(cand_diff, 4),
            reference_values_s=[round(v, 4) for v in vals], reference_median_s=round(float(np.median(vals)), 4), tolerance_s=2.0),
    r9=dict(anomalistic_phase_deg=round(float(mean_anomaly_deg(on)), 3), interval_deg=[round(x, 3) for x in cj['summary']['100']['phase_interval']],
            definition='shortest circular interval holding 95% of the 62 catalogued A100 events (Meeus mean anomaly)'),
    thermal=dict(solar_elevation_deg={s: round(float(solar_elevation_deg(on, *STATIONS[s])), 1) for s in ('s14', 's16')}, rule='|elevation| > 12 deg'),
    nearest_catalogue_rows_min=[[round((r[0] - on) / 60e9, 1), r[2]] for r in sorted(rows, key=lambda r: abs(r[0] - on))[:3]],
)
json.dump(cand, open(os.path.join(OUT, 'candidate.json'), 'w'), indent=1)
print(json.dumps(cand, indent=1))
