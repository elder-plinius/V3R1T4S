"""PREREG A1 (every stacked nest) and A2 (moveout) for the A100-like candidate of 1973-11-26.

usage: attrib_a1a2.py TOOLS_DIR NETS12.npz LAGTOL_STDOUT.txt NAKAMURA_2005_DM_ARRIVALS.csv OUT.json
A1: each of the 12 frozen S14 + S16 stacks, frozen Dt (station means, running max +/- 7 samples, min), maximum over
window starts within +/- 10 min of 07:45:58.641; per-channel NCC at each station's best lag; R7; own null maximum.
A2a: Delta = 16S - 14S (Nakamura 2005) per nest; nests within 2 s / 5 s of A100. A2b: A100 station means over
+/- 30 s of the common lag: location of the maximum vs the maximum within +/- 7 samples (C2).
"""
import sys, json, re, csv
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from scipy.ndimage import maximum_filter1d
from apollo_lib import NS, day_start_ns
from evlib import FS
from scan import prep_day, corr_channels

NPZ, STDOUT, NAK, OUT = sys.argv[2:6]
z = np.load(NPZ)
nests = [str(n) for n in z['nests']]; TMS = z['tm']
CH = [tuple(c.split('.')) for c in z['chans']]
M = TMS.shape[2]
WS = int(np.datetime64('1973-11-26T07:45:58.641', 'ns').astype(np.int64))
pp = prep_day(1973, 330, CH, (0.25, 1.0, 0.1), M)
i_ws = int(round((WS - day_start_ns(1973, 330)) / NS * FS))
K10 = int(round(600 * FS)); K30 = int(round(30 * FS)); KLAG = 7

nullmax = {}
for ln in open(STDOUT):
    m = re.match(r'A(\d+): null C0 ([\d.]+), best shift ([\d.]+), best control ([\d.]+)', ln)
    if m:
        nullmax[m.group(1)] = dict(C0=float(m.group(2)), best_control=float(m.group(4)))


def runmax(x):
    y = np.where(np.isnan(x), -np.inf, x)
    m = maximum_filter1d(y, size=2 * KLAG + 1, mode='nearest')
    return np.where(np.isinf(m), np.nan, m)


def smean(c):
    v = np.sum(~np.isnan(c), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        d = np.nansum(np.nan_to_num(c, nan=0.0), axis=0) / np.maximum(v, 1)
    return np.where(v >= 1, d, np.nan)


i14 = [k for k, c in enumerate(CH) if c[0] == 's14']; i16 = [k for k, c in enumerate(CH) if c[0] == 's16']
res = dict(A1={}, A2={})
xf = {}
for n, tm in zip(nests, TMS):
    _, ccs, _ = corr_channels(pp, list(tm), min_comps=1, xf_cache=xf)
    d14, d16 = smean(ccs[i14]), smean(ccs[i16])
    Dt = np.minimum(runmax(d14), runmax(d16))
    a, b = i_ws - K10, i_ws + K10 + 1
    k = a + int(np.nanargmax(Dt[a:b]))
    lo, hi = k - KLAG, k + KLAG + 1
    j14 = lo + int(np.nanargmax(d14[lo:hi])); j16 = lo + int(np.nanargmax(d16[lo:hi]))
    c14 = [round(float(x), 4) for x in ccs[i14, j14]]; c16 = [round(float(x), 4) for x in ccs[i16, j16]]
    nm = nullmax.get(n, {}).get('best_control')
    rec = dict(Dt=round(float(Dt[k]), 4), window_start_offset_s=round((k - i_ws) / FS, 3),
               onset=str(np.datetime64(WS + int(round((k - i_ws) / FS * 1e9)) + 30 * NS, 'ns'))[:23] + 'Z',
               s14_lag_s=round((j14 - k) / FS, 3), s16_lag_s=round((j16 - k) / FS, 3), s14_ccs=c14, s16_ccs=c16,
               s14_mean=round(float(d14[j14]), 4), s16_mean=round(float(d16[j16]), 4),
               Dt_at_A100_window=round(float(Dt[i_ws]), 4), null_max=nm,
               above_null=None if nm is None else bool(Dt[k] > nm),
               R7=bool(max(c14) >= 0.5 and max(c16) >= 0.5))
    res['A1']['A' + n] = rec
    if n == '100':
        # A2b: station means over +/- 30 s around the common lag of the claim (window start i_ws)
        a, b = i_ws - K30, i_ws + K30 + 1
        prof = {}
        for sta, d, idx in (('s14', d14, i14), ('s16', d16, i16)):
            seg = d[a:b]
            kk = int(np.nanargmax(seg)) - K30
            seg7 = d[i_ws - KLAG:i_ws + KLAG + 1]
            k7 = int(np.nanargmax(seg7)) - KLAG
            # best channel profile too
            chbest = []
            for j in idx:
                sj = ccs[j, a:b]
                chbest.append(dict(ch=CH[j][1], max_pm30s=round(float(np.nanmax(sj)), 4),
                                   lag_of_max_s=round((int(np.nanargmax(sj)) - K30) / FS, 3)))
            top = np.argsort(-np.nan_to_num(seg, nan=-9))[:6]
            prof[sta] = dict(max_pm30s=round(float(np.nanmax(seg)), 4), lag_of_max_samples=kk,
                             lag_of_max_s=round(kk / FS, 3), max_pm7=round(float(np.nanmax(seg7)), 4), lag_pm7_samples=k7,
                             top6_lags_s=[round((int(t) - K30) / FS, 3) for t in top],
                             top6_vals=[round(float(seg[t]), 4) for t in top], channels=chbest)
            prof[sta]['C2_contradiction'] = bool(abs(kk) > KLAG and float(np.nanmax(seg)) > float(np.nanmax(seg7)) + 0.05)
        res['A2']['lag_robustness'] = prof
# A2a
nak = {}
for r in csv.DictReader(open(NAK)):
    try:
        s14, s16 = float(r['14S']), float(r['16S'])
    except (ValueError, TypeError):
        continue
    nak[r['A'].strip()] = (s14, s16, s16 - s14)
dA = nak['100'][2]
res['A2']['nakamura_A100'] = dict(S14=nak['100'][0], S16=nak['100'][1], delta_16S_minus_14S=dA)
res['A2']['nests_with_both_S_picks'] = len(nak)
res['A2']['within_2s'] = sorted([(n, v[2]) for n, v in nak.items() if abs(v[2] - dA) <= 2 and n != '100'], key=lambda x: abs(x[1] - dA))
res['A2']['within_5s'] = sorted([(n, v[2]) for n, v in nak.items() if abs(v[2] - dA) <= 5 and n != '100'], key=lambda x: abs(x[1] - dA))
res['A2']['stacked_nests_delta'] = {('A' + n): (nak[n][2] if n in nak else None) for n in nests}
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(res, indent=1))
