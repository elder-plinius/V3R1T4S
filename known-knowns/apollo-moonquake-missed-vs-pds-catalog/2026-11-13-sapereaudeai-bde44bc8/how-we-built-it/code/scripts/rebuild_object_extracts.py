"""Rebuild the A38 object extracts from the PDS waveforms with the frozen run tools and compare them byte-for-byte with
the unsubmitted package's object/ files; write the two G2 input extracts for the rebuilt package.
usage: rebuild_object_extracts.py TOOLS_DIR A38.npz NULL.jsonl OLD_OBJECT_DIR OUT_DIR
Outputs in OUT_DIR: window_and_template.csv, null_full_span_maxima.csv, null_daily_maxima.csv (same code as the
original package builder), g2_raw_window.csv (raw S14 MH1/MH2 counts and valid flags, 2981 samples at 6.625 Hz from
the window start, exactly the samples glitch_gates_a38.py tests with the frozen glitch rule), g2_prepped_window_pm10s.csv
(prepped 3.3125 Hz series from 33 samples before to 33 samples after the 1491-sample window, the samples G2's lag search
uses), compare.txt."""
import sys, os, json, hashlib, datetime as dt
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from apollo_lib import NS, RATE, load_day, day_start_ns, DAY_SAMPLES
from evlib import FS
from scan import prep_day

NPZ, NULL, OLD, OUT = sys.argv[2:6]
os.makedirs(OUT, exist_ok=True)
WS = '1971-05-13T18:39:33.735'
L = 450.0
ws = int(np.datetime64(WS, 'ns').astype(np.int64))
z = np.load(NPZ); tm = z['tm']; M = tm.shape[1]
pp = prep_day(1971, 133, [('s14', 'mh1'), ('s14', 'mh2')], (0.25, 1.0, 0.1), M)
i0 = int(round((ws - day_start_ns(1971, 133)) / NS * FS))
blk = [(p[0][i0:i0 + M], p[1][i0:i0 + M]) for p in pp]
rep = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def put(name, text):
    b = text.encode()
    open(os.path.join(OUT, name), 'wb').write(b)
    return b


def cmp(name, b):
    old = os.path.join(OLD, name)
    o = open(old, 'rb').read() if os.path.isfile(old) else None
    rep.append('%s: rebuilt sha256 %s, package sha256 %s -> %s' % (name, sha(b), sha(o) if o is not None else '-', 'IDENTICAL' if o == b else ('not in the comparison folder' if o is None else 'DIFFERENT')))


lines = ['sample,template_mh1,template_mh2,data_mh1,data_mh2']
for i in range(M):
    lines.append('%d,%.9e,%.9e,%.9e,%.9e' % (i, tm[0, i], tm[1, i], blk[0][0][i], blk[1][0][i]))
cmp('window_and_template.csv', put('window_and_template.csv', '\n'.join(lines) + '\n'))
null = [json.loads(l) for l in open(NULL)]
c0 = max(d['rev_max'] for d in null if d.get('rev_max') is not None)
ck = [max(d['ctrl_max'][k] for d in null if d.get('ctrl_max') and d['ctrl_max'][k] is not None) for k in range(400)]
cmp('null_full_span_maxima.csv', put('null_full_span_maxima.csv', 'control,full_span_max\nC0_time_reversed,%.5f\n' % c0 + ''.join(
    'C%d_phase_randomised,%.5f\n' % (k + 1, v) for k, v in enumerate(ck))))
cmp('null_daily_maxima.csv', put('null_daily_maxima.csv', 'doy_1971,C0_time_reversed_max,best_phase_randomised_max\n' + ''.join(
    '%d,%.5f,%.5f\n' % (d['doy'], d['rev_max'], max(c for c in d['ctrl_max'] if c is not None)) for d in null)))


def ncc(t, w):
    w = w - w.mean()
    return float(np.dot(t, w) / np.sqrt(np.dot(w, w)) / np.sqrt(np.dot(t, t)))


cc = [ncc(tm[c].astype(float), blk[c][0].astype(float)) for c in (0, 1)]
rep.append('NCC MH1 %.6f MH2 %.6f D %.6f (rounded %.4f %.4f %.4f); null C0 %.5f, best phase-randomised %.5f, controls %d, best of all %.5f' % (
    cc[0], cc[1], sum(cc) / 2, cc[0], cc[1], sum(cc) / 2, c0, max(ck), 1 + len(ck), max([c0] + ck)))
rep.append('prepped valid fraction in window: MH1 %.4f MH2 %.4f; window index i0 %d, M %d' % (blk[0][1].mean(), blk[1][1].mean(), i0, M))


# G2 inputs: raw window exactly as glitch_gates_a38.py reads it (same function body)
def raw_window(sta, ch, t_ns, dur_s):
    xs, vs = [], []
    t = t_ns; remaining = int(dur_s * RATE)
    while remaining > 0:
        d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t // NS)
        y, doy = d.year, d.timetuple().tm_yday
        t0 = day_start_ns(y, doy); j0 = int(round((t - t0) / NS * RATE)); n = min(remaining, DAY_SAMPLES - j0)
        r = load_day(sta, ch, y, doy)
        xs.append(r[0][j0:j0 + n].astype(float)); vs.append(r[1][j0:j0 + n])
        remaining -= n; t = t0 + 86400 * NS
    return np.concatenate(xs), np.concatenate(vs)


raw = [raw_window('s14', ch, ws, L) for ch in ('mh1', 'mh2')]
for x, v in raw:
    assert np.all(x == np.round(x)), 'raw samples not integral'
lines = ['k,raw_mh1,valid_mh1,raw_mh2,valid_mh2']
for k in range(len(raw[0][0])):
    lines.append('%d,%d,%d,%d,%d' % (k, raw[0][0][k], raw[0][1][k], raw[1][0][k], raw[1][1][k]))
b = put('g2_raw_window.csv', '\n'.join(lines) + '\n'); cmp('g2_raw_window.csv', b)
rep.append('g2_raw_window.csv: %d samples per channel, valid MH1 %d MH2 %d, sha256 %s' % (len(raw[0][0]), raw[0][1].sum(), raw[1][1].sum(), sha(b)))
for c, (x, v) in enumerate(raw):
    xv = x - np.median(x[v]); mad = np.median(np.abs(xv[v] - np.median(xv[v])))
    flag = np.where(v & (np.abs(xv) > 8 * max(mad, 0.5)))[0]
    rep.append('frozen glitch rule on MH%d raw window: MAD %.3f, threshold %.3f, max |x - median| %.1f, flagged samples %d' % (
        c + 1, mad, 8 * max(mad, 0.5), np.abs(xv[v]).max(), len(flag)))
LAG = 33
lines = ['offset,data_mh1,data_mh2']
for k in range(-LAG, M + LAG):
    lines.append('%d,%.9e,%.9e' % (k, pp[0][0][i0 + k], pp[1][0][i0 + k]))
b = put('g2_prepped_window_pm10s.csv', '\n'.join(lines) + '\n'); cmp('g2_prepped_window_pm10s.csv', b)
rep.append('g2_prepped_window_pm10s.csv: offsets %d..%d, sha256 %s' % (-LAG, M + LAG - 1, sha(b)))
# central rows must equal the window file's data columns
w = [l.split(',') for l in open(os.path.join(OUT, 'window_and_template.csv')).read().split('\n')[1:-1]]
e = [l.split(',') for l in '\n'.join(lines).split('\n')[1 + LAG:1 + LAG + M]]
rep.append('central prepped rows equal window_and_template.csv data columns: %s' % all(a[3:5] == b2[1:3] for a, b2 in zip(w, e)))
open(os.path.join(OUT, 'compare.txt'), 'w', newline='\n').write('\n'.join(rep) + '\n')
print('\n'.join(rep))
