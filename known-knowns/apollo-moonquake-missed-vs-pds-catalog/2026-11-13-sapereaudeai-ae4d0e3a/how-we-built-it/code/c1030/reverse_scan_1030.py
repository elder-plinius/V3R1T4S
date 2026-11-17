"""PREREG A5 (reverse search): the candidate's own preprocessed window as a template, scanned over 1973 on S14 + S16.

Template: frozen pipeline (scan.prep_day, band 0.25-1.0 Hz, whitening 0.1 Hz, dec 2), candidate day 1973-303 (second candidate, claim run a100_1030),
window start 02:25:21.509 UTC; S14 MH1/MH2 cut at -1.509 s (-5 samples), S16 MH1/MH2 at -0.906 s (-3 samples), L = 450 s.
Statistic (frozen Dt): station mean NCC (valid channels >= 1), running max over +/- 7 samples per station, min of the
two stations. Variant a: S16 mean of MH1 + MH2. Variant b: S16 = MH1 alone. Declustered peaks (+/- 5 min), Dt >= 0.10.
One JSON line per day, resumable.

usage: reverse_scan.py TOOLS_DIR DOY_FROM DOY_TO OUT.jsonl
"""
import sys, os, json, time
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from scipy.ndimage import maximum_filter1d
from apollo_lib import NS, decluster, day_start_ns, norm_template
from evlib import FS
from scan import prep_day, corr_channels, NDAY

YEAR = 1973
d0, d1, OUT = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
CH = [('s14', 'mh1'), ('s14', 'mh2'), ('s16', 'mh1'), ('s16', 'mh2')]
BAND = (0.25, 1.0, 0.1)
M = int(round(450.0 * FS))
WS = int(np.datetime64('1973-10-30T02:25:21.509', 'ns').astype(np.int64))
LAG = {'s14': -5, 's16': -3}
KLAG = 7
SEP = int(300 * FS)
THR = 0.10

pp0 = prep_day(YEAR, 303, CH, BAND, M)
i_ws = int(round((WS - day_start_ns(YEAR, 303)) / NS * FS))
TM = []
for (sta, ch), p in zip(CH, pp0):
    i = i_ws + LAG[sta]
    y, v = p[0][i:i + M], p[1][i:i + M]
    assert v.mean() > 0.99, (sta, ch, v.mean())
    TM.append(norm_template(y.astype(float)))
TM = np.array(TM)
del pp0


def runmax(x):
    y = np.where(np.isnan(x), -np.inf, x)
    m = maximum_filter1d(y, size=2 * KLAG + 1, mode='nearest')
    return np.where(np.isinf(m), np.nan, m)


def smean(ccs, idx):
    c = ccs[idx]
    v = np.sum(~np.isnan(c), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        d = np.nansum(np.nan_to_num(c, nan=0.0), axis=0) / np.maximum(v, 1)
    return np.where(v >= 1, d, np.nan)


done = set()
if os.path.isfile(OUT):
    done = {json.loads(l)['doy'] for l in open(OUT)}
fo = open(OUT, 'a')
for doy in range(d0, d1 + 1):
    if doy in done:
        continue
    T = time.time()
    pp = prep_day(YEAR, doy, CH, BAND, M)
    t0 = day_start_ns(YEAR, doy)
    _, ccs, _ = corr_channels(pp, list(TM), min_comps=1)
    s14 = smean(ccs, [0, 1])
    rec = dict(year=YEAR, doy=doy, scanned14=float(np.mean(~np.isnan(s14))))
    for var, idx16 in (('a', [2, 3]), ('b', [2])):
        s16 = smean(ccs, idx16)
        Dt = np.minimum(runmax(s14), runmax(s16)).astype(np.float32)
        pk = decluster(Dt, SEP, THR)
        pl = []
        for i in pk:
            a, b = max(0, i - KLAG), min(NDAY, i + KLAG + 1)
            j14 = a + int(np.nanargmax(np.where(np.isnan(s14[a:b]), -np.inf, s14[a:b])))
            j16 = a + int(np.nanargmax(np.where(np.isnan(s16[a:b]), -np.inf, s16[a:b])))
            pl.append([int(t0 + round(i / FS * 1e9)), round(float(Dt[i]), 4),
                       [None if np.isnan(c) else round(float(c), 4) for c in ccs[[0, 1], j14]] +
                       [None if np.isnan(c) else round(float(c), 4) for c in ccs[[2, 3], j16]],
                       round((j14 - i) / FS, 3), round((j16 - i) / FS, 3)])
        rec['peaks_' + var] = pl
        rec['scanned_' + var] = float(np.mean(~np.isnan(Dt)))
    rec['seconds'] = round(time.time() - T, 1)
    fo.write(json.dumps(rec) + '\n'); fo.flush()
    print(doy, len(rec['peaks_a']), len(rec['peaks_b']), rec['seconds'], flush=True)
fo.close()
