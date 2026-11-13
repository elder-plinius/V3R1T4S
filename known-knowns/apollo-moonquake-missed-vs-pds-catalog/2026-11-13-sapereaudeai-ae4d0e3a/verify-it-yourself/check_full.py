"""Standalone checker for the full-criterion candidate (Python standard library only). From object/:
- sha256 of the object files;
- NCC of the saved preprocessed S14 and S16 windows with the saved A100 stack (template zero-mean, unit-norm;
  NCC = sum t (w - mean w) / sqrt(sum (w - mean w)^2)) at every lag within +/- 7 samples; each station takes the lag
  of its best station mean; Dt = min of the two station means (the frozen statistic at the claimed window start);
- R7: best single-channel NCC >= 0.5 at S14 and at S16;
- null: Dt above the full-span maximum of every one of the 401 controls;
- R8: ATT-corrected S16 - S14 arrival difference (station lags + saved ATT offsets) within 2 s of the median of the
  saved reference values;
- R9: anomalistic phase (Meeus mean anomaly) of the onset inside the shortest circular interval holding 95% of the
  catalogued A100 event times;
- thermal: |solar elevation| > 12 deg at both stations (low-precision ephemeris);
- R6 (saved): no catalogue row within +/- 5 min.
Last line: PASS or FAIL."""
import csv, datetime as dt, hashlib, json, math, os, sys

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); obj = os.path.join(root, 'object')
ok = True


def fail(m):
    global ok
    ok = False; print('mismatch:', m)


for line in open(os.path.join(here, 'OBJECT_SHA256.txt')):
    h, name = line.split(); p = os.path.join(obj, name)
    if not os.path.isfile(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != h:
        fail('sha256 of object/' + name)
cand = json.load(open(os.path.join(obj, 'candidate.json')))
rows = list(csv.DictReader(open(os.path.join(obj, 'window_and_template.csv'))))
K = int(cand['lag_tolerance_samples']); FS = float(cand['sample_rate_hz'])
cols = ['s14_mh1', 's14_mh2', 's16_mh1', 's16_mh2']
tm = {c: [float(r['template_' + c]) for r in rows if r['template_' + c] != ''] for c in cols}
dat = {c: [float(r['data_' + c]) for r in rows] for c in cols}
M = len(tm[cols[0]])
for c in cols:
    if abs(sum(tm[c])) > 1e-6 or abs(math.sqrt(sum(x * x for x in tm[c])) - 1) > 1e-6:
        fail('template %s not zero-mean unit-norm' % c)


def ncc(t, w):
    mw = sum(w) / len(w); wd = [x - mw for x in w]
    return sum(a * b for a, b in zip(t, wd)) / math.sqrt(sum(x * x for x in wd))


best = {}
for sta in ('s14', 's16'):
    cs = [c for c in cols if c.startswith(sta)]
    b = None
    for d in range(-K, K + 1):
        v = [ncc(tm[c], dat[c][K + d:K + d + M]) for c in cs]
        m = sum(v) / len(v)
        if b is None or m > b[0]:
            b = (m, d, v)
    best[sta] = b
Dt = min(best['s14'][0], best['s16'][0])
print('S14 lag %+d samples NCC %s mean %.4f | S16 lag %+d samples NCC %s mean %.4f | Dt %.4f' % (
    best['s14'][1], [round(x, 4) for x in best['s14'][2]], best['s14'][0],
    best['s16'][1], [round(x, 4) for x in best['s16'][2]], best['s16'][0], Dt))
fz = cand['frozen_scan_peak']
if abs(Dt - fz['Dt']) > 2e-4 or any(abs(a - b) > 2e-4 for a, b in zip(best['s14'][2] + best['s16'][2], fz['ccs'])):
    fail('recomputed NCC differ from candidate.json')
if abs(best['s14'][1] / FS - fz['lag_s14_s']) > 0.01 or abs(best['s16'][1] / FS - fz['lag_s16_s']) > 0.01:
    fail('station lags differ from candidate.json')
r7 = max(best['s14'][2]) >= 0.5 and max(best['s16'][2]) >= 0.5
print('R7 best single channel S14 %.4f, S16 %.4f: %s' % (max(best['s14'][2]), max(best['s16'][2]), r7))
if not r7:
    fail('R7')
ctrl = [float(r['full_span_max']) for r in csv.DictReader(open(os.path.join(obj, 'null_full_span_maxima.csv')))]
print('null: %d controls, best %.5f, Dt above all: %s' % (len(ctrl), max(ctrl), all(Dt > c for c in ctrl)))
if len(ctrl) != 401 or not all(Dt > c for c in ctrl):
    fail('null')
r8 = cand['r8']
diff = (best['s16'][1] / FS + r8['att_offset_s16_s']) - (best['s14'][1] / FS + r8['att_offset_s14_s'])
refs = sorted(r8['reference_values_s']); n = len(refs)
med = refs[n // 2] if n % 2 else (refs[n // 2 - 1] + refs[n // 2]) / 2
print('R8 S16 - S14 %.3f s, reference median %.3f s (n %d): %s' % (diff, med, n, abs(diff - med) <= 2.0))
if abs(diff - r8['candidate_s16_minus_s14_s']) > 0.01 or abs(diff - med) > 2.0:
    fail('R8')


def t_ns(iso):
    d = dt.datetime.strptime(iso.rstrip('Z')[:23], '%Y-%m-%dT%H:%M:%S.%f')
    return (d - dt.datetime(1970, 1, 1)).total_seconds() * 1e9


def T(tn):
    return (tn - 946728000e9) / 1e9 / 86400.0 / 36525.0


def mean_anomaly(tn):
    t = T(tn)
    return (134.9633964 + 477198.8675055 * t + 0.0087414 * t * t + t ** 3 / 69699.0) % 360.0


def elongation(tn):
    t = T(tn)
    return (297.8501921 + 445267.1114034 * t - 0.0018819 * t * t + t ** 3 / 545868.0) % 360.0


on = t_ns(cand['onset_utc'])
ph = mean_anomaly(on)
cat = sorted(mean_anomaly(t_ns(r['utc'])) for r in csv.DictReader(open(os.path.join(obj, 'a100_catalogue_times.csv'))))
k = math.ceil(0.95 * len(cat)); bw = None
for i in range(len(cat)):
    j = (i + k - 1) % len(cat); w = (cat[j] - cat[i]) % 360
    if bw is None or w < bw[0]:
        bw = (w, cat[i], cat[j])
inside = ((ph - bw[1]) % 360) <= bw[0]
print('R9 phase %.2f deg, 95%% interval of %d events [%.2f, %.2f]: %s' % (ph, len(cat), bw[1], bw[2], inside))
if not inside or abs(ph - cand['r9']['anomalistic_phase_deg']) > 0.01:
    fail('R9')
st = {'s14': (-3.6445, -17.47753), 's16': (-8.97577, 15.49649)}
lam = 180.0 - elongation(on)
el = {s: math.degrees(math.asin(math.cos(math.radians(la)) * math.cos(math.radians(lo - lam)))) for s, (la, lo) in st.items()}
print('thermal: solar elevation S14 %.1f, S16 %.1f deg' % (el['s14'], el['s16']))
if any(abs(e) <= 12 for e in el.values()):
    fail('thermal')
near = cand['nearest_catalogue_rows_min']
print('R6 (saved): nearest catalogue row %.1f min (%s)' % (near[0][0], near[0][1]))
if any(abs(r[0]) <= 5 for r in near):
    fail('R6')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
