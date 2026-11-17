"""PREREG (fullwin_panel) gates G1 and G2 for the A100-like candidate on S14 + S16, Liu, Xiao and Li 2025 catalogue.

usage: glitch_gates_1416.py TOOLS_DIR A100.npz LIT_ACC_DIR OUT.json
G1: catalogued Spike / Step-Up / Step-Down intervals on S14 and S16 (MH1, MH2; MHZ reported) overlapping each
station's template window [ws + lag, + 450 s]. Coverage: entries per station in 1973 and nearest entries to the onset.
G2: mute +/- 5 s around every overlapping catalogued interval (used channels) and every raw sample flagged by the
frozen rule (|x - median| > 8 max(MAD, 0.5)) on all channels of that station, template and data at the same samples;
NCC over unmuted samples; each station's best lag (station mean) within +/- 7 samples of the common lag (and, reported,
+/- 10 s). Pass: best single-channel NCC >= 0.5 at S14 and at S16 and Dt = min(station means) > 0.1906.
"""
import sys, os, json, csv, bisect, datetime as dt
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from apollo_lib import NS, RATE, load_day, day_start_ns
from evlib import FS
from scan import prep_day

NPZ, ACCDIR, OUT = sys.argv[2], sys.argv[3], sys.argv[4]
WS = int(np.datetime64('1973-11-26T07:45:58.641', 'ns').astype(np.int64))
ONSET = WS + 30 * NS
L = 450.0
NULLMAX = 0.1906
LAGS = {'s14': 5, 's16': 7}          # samples at FS (1.509 s, 2.113 s)
CH = [('s14', 'mh1'), ('s14', 'mh2'), ('s16', 'mh1'), ('s16', 'mh2')]
z = np.load(NPZ); TM = z['tm'][0] if z['tm'].ndim == 3 else z['tm']
assert [str(c) for c in z['chans']] == ['s14.mh1', 's14.mh2', 's16.mh1', 's16.mh2']
M = TM.shape[1]


def T(s):
    s = s.strip()
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


def tns(d):
    return int((d - dt.datetime(1970, 1, 1)).total_seconds() * 1e9)


acc = {}
cov = {}
for sta in ('S14', 'S16'):
    rows = []
    for typ in ('Spike', 'Step-Up', 'Step-Down'):
        for comp in ('MH1', 'MH2', 'MHZ'):
            p = os.path.join(ACCDIR, '%s_ACC-%s_%s_all.csv' % (sta, typ, comp))
            n73 = 0; n = 0; first = last = None
            for r in csv.DictReader(open(p, newline='')):
                a, b = tns(T(r['Start time'])), tns(T(r['End time']))
                rows.append((a, b, typ, comp, r['Mode'], r['Similarity'], r['Amplitude Range']))
                n += 1
                if 1973 == T(r['Start time']).year:
                    n73 += 1
                first = a if first is None else min(first, a); last = b if last is None else max(last, b)
            cov['%s %s %s' % (sta, typ, comp)] = dict(rows=n, rows_1973=n73,
                                                       first=str(np.datetime64(first, 'ns'))[:19],
                                                       last=str(np.datetime64(last, 'ns'))[:19])
    rows.sort()
    acc[sta.lower()] = rows

res = dict(window_start='1973-11-26T07:45:58.641Z', onset='1973-11-26T07:46:28.641Z', coverage=cov, G1={}, G2={})
day330 = (tns(dt.datetime(1973, 11, 26)), tns(dt.datetime(1973, 11, 27)))
for sta, rows in acc.items():
    w0 = WS + int(round(LAGS[sta] / FS * 1e9)); w1 = w0 + int(L * 1e9)
    ov = [r for r in rows if r[1] >= w0 and r[0] <= w1]
    used = [r for r in ov if r[3] in ('MH1', 'MH2')]
    st = np.array([r[0] for r in rows], dtype=np.int64)
    i = int(np.searchsorted(st, ONSET))
    near = sorted(rows[max(0, i - 40):i + 40], key=lambda r: abs(r[0] - ONSET))[:6]
    on_day = sum(1 for r in rows if day330[0] <= r[0] < day330[1])
    res['G1'][sta] = dict(window=[str(np.datetime64(w0, 'ns'))[:23] + 'Z', L],
                          overlapping_all=[[round((r[0] - ONSET) / 1e9, 2), round((r[1] - ONSET) / 1e9, 2)] + list(r[2:]) for r in ov],
                          overlapping_used_channels=len(used),
                          entries_on_1973_330=on_day,
                          nearest_to_onset=[[round((r[0] - ONSET) / 1e9, 2), round((r[1] - ONSET) / 1e9, 2)] + list(r[2:]) for r in near])


def raw_window(sta, ch, t_ns, n):
    d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t_ns // NS)
    y, doy = d.year, d.timetuple().tm_yday
    i0 = int(round((t_ns - day_start_ns(y, doy)) / NS * RATE))
    x, v, _ = load_day(sta, ch, y, doy)
    return x[i0:i0 + n].astype(float), v[i0:i0 + n]


spans = {'s14': [], 's16': []}
for sta in ('s14', 's16'):
    w0 = WS + int(round(LAGS[sta] / FS * 1e9))
    for r in acc[sta]:
        if r[3] in ('MH1', 'MH2') and r[1] >= w0 and r[0] <= w0 + int(L * 1e9):
            spans[sta].append((r[0] - 5 * NS, r[1] + 5 * NS, 'catalogued %s %s' % (r[2], r[3])))
    for ch in ('mh1', 'mh2'):
        x, v = raw_window(sta, ch, w0, int(L * RATE))
        xv = x - np.median(x[v])
        mad = np.median(np.abs(xv[v] - np.median(xv[v])))
        flag = np.where(v & (np.abs(xv) > 8 * max(mad, 0.5)))[0]
        res['G2'].setdefault('flagged', {})['%s.%s' % (sta, ch)] = dict(n=int(flag.size), mad=float(mad),
            first_s=None if flag.size == 0 else round(flag[0] / RATE, 2), last_s=None if flag.size == 0 else round(flag[-1] / RATE, 2))
        for k in flag:
            t = w0 + int(k / RATE * 1e9)
            spans[sta].append((t - 5 * NS, t + 5 * NS, 'rule %s' % ch))

pp = prep_day(1973, 330, CH, (0.25, 1.0, 0.1), M)
i_ws = int(round((WS - day_start_ns(1973, 330)) / NS * FS))


def ncc(t, w):
    t = t - t.mean(); w = w - w.mean()
    return float(np.dot(t, w) / np.sqrt(np.dot(w, w) * np.dot(t, t)))


def station(sta, maxlag, mute_on=True):
    idx = [k for k, c in enumerate(CH) if c[0] == sta]
    best = None
    for d in range(-maxlag, maxlag + 1):
        tt = WS + ((d + np.arange(M)) / FS * 1e9).astype(np.int64)
        mute = np.zeros(M, bool)
        if mute_on:
            for s0, s1, _ in spans[sta]:
                mute |= (tt >= s0) & (tt <= s1)
        cc = []
        for k in idx:
            w = pp[k][0][i_ws + d:i_ws + d + M].astype(float); t = TM[k].astype(float)
            cc.append(ncc(t[~mute], w[~mute]))
        rec = dict(lag_samples=d, lag_s=round(d / FS, 3), ccs=[round(c, 4) for c in cc], mean=round(float(np.mean(cc)), 4),
                   muted=int(mute.sum()))
        if best is None or rec['mean'] > best['mean']:
            best = rec
    return best


for lab, ml, mute in (('unmuted_pm7', 7, False), ('muted_pm7', 7, True), ('muted_pm10s', 33, True)):
    b = {sta: station(sta, ml, mute) for sta in ('s14', 's16')}
    b['Dt'] = round(min(b['s14']['mean'], b['s16']['mean']), 4)
    b['R7'] = bool(max(b['s14']['ccs']) >= 0.5 and max(b['s16']['ccs']) >= 0.5)
    res['G2'][lab] = b
g = res['G2']['muted_pm7']
res['G2']['spans'] = {sta: [[round((s0 - WS) / 1e9, 2), round((s1 - WS) / 1e9, 2), lab] for s0, s1, lab in spans[sta]][:200]
                      for sta in spans}
res['G2']['n_spans'] = {sta: len(spans[sta]) for sta in spans}
res['G2']['pass'] = bool(g['R7'] and g['Dt'] > NULLMAX)
res['G1']['pass_no_overlap_used_channels'] = all(res['G1'][s]['overlapping_used_channels'] == 0 for s in ('s14', 's16'))
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(dict(G1={s: dict(n_overlap_all=len(res['G1'][s]['overlapping_all']),
                                   n_overlap_used=res['G1'][s]['overlapping_used_channels'],
                                   on_day=res['G1'][s]['entries_on_1973_330'],
                                   nearest=res['G1'][s]['nearest_to_onset'][:3]) for s in ('s14', 's16')},
                      flagged=res['G2']['flagged'], n_spans=res['G2']['n_spans'],
                      unmuted=res['G2']['unmuted_pm7'], muted=res['G2']['muted_pm7'], muted10=res['G2']['muted_pm10s'],
                      G2_pass=res['G2']['pass']), indent=1))
