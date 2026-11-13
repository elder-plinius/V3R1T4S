"""PREREG.v15 glitch check (PREREG.md rule) for lag-tolerant S14+S16 candidates: per channel, raw template-window
samples above 8 x MAD; if any, Dt recomputed without that channel must stay above the nest's null maximum; template
first and second halves must correlate positively at each station (station mean, at the station's own lag).
usage: glitch_check_1416.py NETS.npz CANDIDATES.json NEST ONSET_ISO"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
import datetime as dt
from apollo_lib import NS, RATE, load_day, day_start_ns, DAY_SAMPLES
from evlib import FS, DayCache, event_block
z = np.load(sys.argv[1]); nests = [str(n) for n in z['nests']]; nest = sys.argv[3]
tm = z['tm'][nests.index(nest)]; chans = [tuple(c.split('.')) for c in z['chans']]; M = tm.shape[1]
c = json.load(open(sys.argv[2])); best = c['summary'][nest]['best_control']
r = [x for x in c['candidates'][nest] if x['onset'] == sys.argv[4]][0]
t = int(np.datetime64(r['onset'][:-1], 'ns').astype(np.int64)) - 30 * NS
lags = {'s14': r['lag12_s'], 's16': r['lag14_s']}
ccs = r['ccs']


def raw(sta, ch, t_ns, n):
    d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t_ns // NS); y, doy = d.year, d.timetuple().tm_yday
    i0 = int(round((t_ns - day_start_ns(y, doy)) / NS * RATE)); x, v, _ = load_day(sta, ch, y, doy)
    return x[i0:i0 + n].astype(float), v[i0:i0 + n]


out = dict(onset=r['onset'], null_max=best, Dt=r['Dc'], ccs=ccs, lags=lags, channels={})
ok = True
for k, (sta, ch) in enumerate(chans):
    x, v = raw(sta, ch, t + int(lags[sta] * NS), int(450 * RATE))
    xv = x[v] - np.median(x[v]); mad = np.median(np.abs(xv - np.median(xv)))
    spike = bool(np.any(np.abs(xv) > 8 * max(mad, 0.5)))
    rest = [ccs[j] for j, (s2, _) in enumerate(chans) if s2 == sta and j != k and ccs[j] is not None]
    other = [ccs[j] for j, (s2, _) in enumerate(chans) if s2 != sta and ccs[j] is not None]
    dt_wo = min(np.mean(rest), np.mean(other)) if rest and other else None
    out['channels']['%s.%s' % (sta, ch)] = dict(spike_over_8mad=spike, mad=float(mad), Dt_without=dt_wo)
    if spike and (dt_wo is None or dt_wo <= best):
        ok = False
cache = DayCache((0.25, 1.0, 0.1))
halves = {}
for sta in ('s14', 's16'):
    idx = [k for k, c2 in enumerate(chans) if c2[0] == sta]
    blk = event_block(cache, [chans[k] for k in idx], t + int(lags[sta] * NS), M)
    hs = []
    for h in (slice(0, M // 2), slice(M // 2, M)):
        cs = []
        for (y, vv), k in zip(blk, idx):
            a, b = tm[k][h] - tm[k][h].mean(), y[h] - y[h].mean()
            cs.append(float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum())))
        hs.append(float(np.mean(cs)))
    halves[sta] = hs
    if min(hs) <= 0:
        ok = False
out['halves'] = halves; out['glitch_ok'] = ok
print(json.dumps(out, indent=1))
