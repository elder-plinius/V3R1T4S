"""PREREG (run 2026-11-13-0552) gates G1, G2 and descriptive G3 for the confirmed A38 object of 1971-05-13 (lens a38-glitch-check) (S14 MH1/MH2).
usage: glitch_gates.py TOOLS_DIR FROZEN_A39.npz LEVENT.csv ACC_MH1.csv ACC_MH2.csv OUT.json
G1: catalogued ACC-Spike intervals overlapping the 450 s window. G2: NCC with catalogued spikes overlapping the window
and raw samples flagged by the frozen glitch rule (|x - median| > 8 max(MAD, 0.5)) muted +/- 5 s in the prepped series,
template and data muted at the same samples, best lag within +/- 10 s; pass if best CC >= 0.6 and D > 0.2868.
G3: fraction of catalogued A39 / A201 / all type-A events with a catalogued spike in [start - 60 s, start + 450 s],
and the base rate for 20,000 uniform random times (seed 20261113)."""
import sys, json, csv, bisect, datetime as dt
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from apollo_lib import NS, RATE, load_day, day_start_ns, DAY_SAMPLES
from evlib import FS
from scan import prep_day

NPZ, LEV, ACC1, ACC2, OUT = sys.argv[2:7]
WS = '1971-05-13T18:39:33.735'
NULLMAX = 0.2868
L = 450.0
ws = int(np.datetime64(WS, 'ns').astype(np.int64))
we = ws + int(L * 1e9)
z = np.load(NPZ); tm = z['tm']; M = tm.shape[1]


def T(s):
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


def tns(d):
    return int((d - dt.datetime(1970, 1, 1)).total_seconds() * 1e9)


acc = []
for p, ch in ((ACC1, 'MH1'), (ACC2, 'MH2')):
    for r in csv.DictReader(open(p, newline='')):
        acc.append((tns(T(r['Start time'])), tns(T(r['End time'])), ch, r['Mode'], r['Similarity'], r['Amplitude Range']))
acc.sort()
starts = np.array([a[0] for a in acc], dtype=np.int64)
ends = np.array([a[1] for a in acc], dtype=np.int64)
maxdur = int((ends - starts).max())


def overlapping(t0, t1):
    i0 = bisect.bisect_left(starts, t0 - maxdur); i1 = bisect.bisect_right(starts, t1)
    return [acc[i] for i in range(i0, i1) if acc[i][1] >= t0 and acc[i][0] <= t1]


res = {}
# G1
ov = overlapping(ws, we)
res['G1'] = dict(window=[WS + 'Z', L], overlapping=[[(a[0] - ws) / 1e9, (a[1] - ws) / 1e9, a[2], a[3], a[4], a[5]] for a in ov],
                 pass_=len(ov) == 0)
i = bisect.bisect_left(starts, ws)
near = sorted([acc[j] for j in range(max(0, i - 20), min(len(acc), i + 20))], key=lambda a: abs(a[0] - (ws + 30 * NS)))[:4]
res['G1']['nearest_spike_starts_s_from_onset'] = [[round((a[0] - ws - 30 * NS) / 1e9, 3), a[2]] for a in near]


# G2
def raw_window(sta, ch, t_ns, dur_s):
    xs, vs = [], []
    t = t_ns; remaining = int(dur_s * RATE)
    while remaining > 0:
        d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t // NS)
        y, doy = d.year, d.timetuple().tm_yday
        t0 = day_start_ns(y, doy); i0 = int(round((t - t0) / NS * RATE)); n = min(remaining, DAY_SAMPLES - i0)
        r = load_day(sta, ch, y, doy)
        xs.append(r[0][i0:i0 + n].astype(float)); vs.append(r[1][i0:i0 + n])
        remaining -= n; t = t0 + 86400 * NS
    return np.concatenate(xs), np.concatenate(vs)


spans = [(a[0] - 5 * NS, a[1] + 5 * NS, 'catalogued ' + a[2]) for a in ov]
for ch in ('mh1', 'mh2'):
    x, v = raw_window('s14', ch, ws, L)
    xv = x - np.median(x[v])
    mad = np.median(np.abs(xv[v] - np.median(xv[v])))
    flag = np.where(v & (np.abs(xv) > 8 * max(mad, 0.5)))[0]
    for k in flag:
        t = ws + int(k / RATE * 1e9)
        spans.append((t - 5 * NS, t + 5 * NS, 'rule-flagged %s sample %+.1f s' % (ch.upper(), k / RATE)))
pp = prep_day(1971, 133, [('s14', 'mh1'), ('s14', 'mh2')], (0.25, 1.0, 0.1), M)
i0 = int(round((ws - day_start_ns(1971, 133)) / NS * FS))


def ncc(t, w):
    w = w - w.mean()
    return float(np.dot(t, w) / np.sqrt(np.dot(w, w)) / np.sqrt(np.dot(t, t)))


best = {}
for mode in ('both_muted', 'data_only'):
    b = None
    for lag in range(-33, 34):
        tt = ws + (lag + np.arange(M)) * (NS / FS)
        mute = np.zeros(M, bool)
        for s0, s1, _ in spans:
            mute |= (tt >= s0) & (tt <= s1)
        cc = []
        for c in (0, 1):
            w = pp[c][0][i0 + lag:i0 + lag + M].astype(float)
            t = tm[c].astype(float)
            if mode == 'both_muted':
                cc.append(ncc(t[~mute], w[~mute]))
            else:
                w = w.copy(); w[mute] = 0.0
                cc.append(ncc(t, w))
        D = sum(cc) / 2
        rec = dict(lag_s=round(lag / FS, 3), ccs=[round(c, 4) for c in cc], D=round(D, 4), muted_samples=int(mute.sum()))
        if lag == 0:
            best[mode + '_lag0'] = rec
        if b is None or D > b['D']:
            b = rec
    best[mode + '_best'] = b
unm = [ncc(tm[c].astype(float), pp[c][0][i0:i0 + M].astype(float)) for c in (0, 1)]
g2 = best['both_muted_best']
res['G2'] = dict(spans=[[round((s0 - ws) / 1e9, 2), round((s1 - ws) / 1e9, 2), lab] for s0, s1, lab in spans],
                 unmuted_ccs=[round(c, 4) for c in unm], **best,
                 pass_=bool(max(g2['ccs']) >= 0.6 and g2['D'] > NULLMAX))

# G3
import pandas as pd  # noqa: E402
cat = pd.read_csv(LEV, dtype=str)


def cat_ns(y, jd, s):
    y = 1900 + int(y); jd = int(jd); s = str(s).zfill(4)
    return tns(dt.datetime(y, 1, 1) + dt.timedelta(days=jd - 1, hours=int(s[:2]), minutes=int(s[2:])))


s14_on = tns(dt.datetime(1971, 2, 5)); s14_off = tns(dt.datetime(1977, 9, 30))
g3 = {}
for lab, sel in (('A39', (cat['T2'] == 'A') & (cat['N2'].str.strip() == '39')),
                 ('A201', (cat['T2'] == 'A') & (cat['N2'].str.strip() == '201')),
                 ('all type A', cat['T2'] == 'A')):
    n = hit = 0
    for r in cat[sel].itertuples():
        try:
            t = cat_ns(r.Y, r.JD, r.S)
        except Exception:
            continue
        if not (s14_on <= t <= s14_off):
            continue
        n += 1
        if overlapping(t - 60 * NS, t + int(L * 1e9)):
            hit += 1
    g3[lab] = dict(events=n, with_spike=hit, fraction=round(hit / n, 4) if n else None)
rng = np.random.default_rng(20261113)
rt = rng.integers(s14_on, s14_off, 20000)
hit = sum(1 for t in rt if overlapping(int(t) - 60 * NS, int(t) + int(L * 1e9)))
g3['random times'] = dict(events=20000, with_spike=hit, fraction=round(hit / 20000, 4))
res['G3'] = g3
res['note'] = 'G3 counts any catalogued S14 MH1/MH2 ACC-Spike (all modes) overlapping [start - 60 s, start + 450 s]; levent start times are minute-resolution.'
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(res, indent=1))
