"""PREREG A3: S16 MH2 response relative to MH1 for every 1973 levent row and for the candidate.

usage: s16_mh2_response.py TOOLS_DIR LEVENT.csv OUT.jsonl
Frozen preprocessing (apollo_lib.preprocess, band 0.25-1.0 Hz, whitening 0.1 Hz, despike, dec 2) of each S16 day
(+ 2 h of the next day). For t0: E_sig = mean y^2 over [t0 - 60 s, t0 + 600 s]; E_noise = median of the mean y^2 of
the 60 s sub-windows of [t0 - 25 min, t0 - 5 min]; R = E_sig / E_noise; valid if both spans are >= 99% valid.
r2 = (R_MH2 - 1) / (R_MH1 - 1) when R_MH1 >= 1.5. One line per event (and one for the candidate).
Also, per hour of 1973 days 328-332, raw MH1/MH2 statistics (std of valid samples, fraction of valid samples equal to
the hour's median: a flat-line indicator).
"""
import sys, json, datetime as dt
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
import pandas as pd
from apollo_lib import load_span, load_day, preprocess, NS, RATE, day_start_ns
from evlib import FS

LEV, OUT = sys.argv[2], sys.argv[3]
BAND = (0.25, 1.0, 0.1)
cat = pd.read_csv(LEV, dtype=str)
cat = cat[cat['Y'] == '73'].copy()
cat['doy'] = cat['JD'].astype(int)
cand = dict(label='CANDIDATE', t0=int(np.datetime64('1973-11-26T07:46:28.641', 'ns').astype(np.int64)), doy=330)
fo = open(OUT, 'w')


def energies(y, v, i0):
    a = i0 - int(60 * FS); b = i0 + int(600 * FS)
    n0 = i0 - int(25 * 60 * FS); n1 = i0 - int(5 * 60 * FS)
    if n0 < 0 or b > len(y):
        return None
    vs, vn = v[a:b].mean(), v[n0:n1].mean()
    es = float(np.mean(y[a:b] ** 2))
    w = int(60 * FS)
    subs = [float(np.mean(y[k:k + w] ** 2)) for k in range(n0, n1 - w + 1, w)]
    en = float(np.median(subs))
    return dict(R=es / en if en > 0 else None, valid_sig=round(float(vs), 4), valid_noise=round(float(vn), 4))


for doy in range(1, 366):
    rows = cat[cat['doy'] == doy]
    evs = []
    for _, r in rows.iterrows():
        s = str(r['S']).strip().zfill(4)
        t0 = day_start_ns(1973, doy) + (int(s[:2]) * 3600 + int(s[2:]) * 60) * NS
        f = lambda c: '' if pd.isna(r[c]) else str(r[c])
        evs.append(dict(label='levent 73-%03d %s T2=%s N2=%s' % (doy, s, f('T2'), f('N2')),
                        t0=t0, doy=doy, T2=f('T2'), N2=f('N2').strip(), A4=f('A4'), grade=f('Grade'),
                        flags16=dict(LPX=f('16LPX'), LPY=f('16LPY'), LPZ=f('16LPZ'))))
    if doy == 330:
        evs.append(cand)
    if not evs:
        continue
    pre = {}
    for ch in ('mh1', 'mh2'):
        sp = load_span('s16', ch, 1973, doy, int(7200 * RATE))
        if sp is None:
            pre[ch] = None; continue
        x, v, _ = sp
        pre[ch] = preprocess(x, v, BAND, dec=2)
    for e in evs:
        i0 = int(round((e['t0'] - day_start_ns(1973, doy)) / NS * FS))
        out = dict(e)
        for ch in ('mh1', 'mh2'):
            out[ch] = None if pre[ch] is None else energies(pre[ch][0], pre[ch][1], i0)
        ok = all(out[c] is not None and out[c]['R'] is not None and out[c]['valid_sig'] >= 0.99 and out[c]['valid_noise'] >= 0.99
                 for c in ('mh1', 'mh2'))
        out['valid'] = ok
        if ok and out['mh1']['R'] >= 1.5:
            out['r2'] = round((out['mh2']['R'] - 1) / (out['mh1']['R'] - 1), 4)
        else:
            out['r2'] = None
        out['t0_iso'] = str(np.datetime64(e['t0'], 'ns'))[:19]
        fo.write(json.dumps(out) + '\n')
    fo.flush()
fo.close()

# raw hourly statistics around the candidate
st = []
for doy in range(328, 333):
    for ch in ('mh1', 'mh2'):
        r = load_day('s16', ch, 1973, doy)
        if r is None:
            continue
        x, v, _ = r
        for h in range(24):
            a, b = int(h * 3600 * RATE), int((h + 1) * 3600 * RATE)
            xv = x[a:b][v[a:b]].astype(float)
            if xv.size < 100:
                st.append(dict(doy=doy, hour=h, ch=ch, n=int(xv.size))); continue
            med = np.median(xv)
            st.append(dict(doy=doy, hour=h, ch=ch, n=int(xv.size), std=round(float(xv.std()), 3),
                           frac_at_median=round(float(np.mean(xv == med)), 4), median=float(med),
                           p01=float(np.percentile(xv, 1)), p99=float(np.percentile(xv, 99))))
json.dump(st, open(OUT.replace('.jsonl', '_rawhourly.json'), 'w'), indent=0)
print('done')
