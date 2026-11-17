"""Checks for given single-station seeds (PREREG.v9/v12 rules): gap, glitch (spike > 8 MAD flags per channel; the
'D without that channel above the null maximum' part is applied when the null maximum is given), both template
halves positive, thermal (|solar elevation| > 12 deg), R6 (all PDS tables) and Onodera windows, anomalistic phase.

usage: seed_checks.py SEEDS_SUMMARY.json PER_NEST_DIR CATALOG_DIR LIT_DIR OUT.json [NULLMAX_JSON]
"""
import sys, json, os
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
import datetime as dt
from apollo_lib import NS, RATE, load_day, ns_iso, day_start_ns, DAY_SAMPLES
from evlib import FS, DayCache, event_block
from catalog_check import load_all, matches
import onodera_check
from ephem import solar_elevation_deg, mean_anomaly_deg, STATIONS

seeds = json.load(open(sys.argv[1])); pnd = sys.argv[2]
rows = load_all(sys.argv[3]); ono = onodera_check.load(sys.argv[4]); out = sys.argv[5]
nullmax = json.load(open(sys.argv[6])) if len(sys.argv) > 6 else {}
cache = DayCache((0.25, 1.0, 0.1))


def raw_window(sta, ch, t_ns, dur_s):
    xs, vs, ds = [], [], []
    t = t_ns; remaining = int(dur_s * RATE)
    while remaining > 0:
        d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t // NS)
        y, doy = d.year, d.timetuple().tm_yday
        t0 = day_start_ns(y, doy); i0 = int(round((t - t0) / NS * RATE)); n = min(remaining, DAY_SAMPLES - i0)
        r = load_day(sta, ch, y, doy)
        if r is None:
            xs.append(np.zeros(n)); vs.append(np.zeros(n, bool))
        else:
            xs.append(r[0][i0:i0 + n].astype(float)); vs.append(r[1][i0:i0 + n]); ds += [k for k in r[2] if i0 <= k < i0 + n]
        remaining -= n; t = t0 + 86400 * NS
    return np.concatenate(xs), np.concatenate(vs), ds


res = {}
for n, v in seeds.items():
    if not v.get('seeds'):
        continue
    z = np.load(os.path.join(pnd, 's14_A%s_1971_templates.npz' % n))
    tm = list(z['tm']); chans = [tuple(c.split('.')) for c in z['chans']]; L = float(z['L']); M = tm[0].size
    sta = chans[0][0]
    for sd in v['seeds']:
        t = int(sd['t']); onset = t + 30 * NS
        g = {}; g_ok = True
        for (s, ch) in chans:
            x, vv, ds = raw_window(s, ch, onset - 600 * NS, L + 1200)
            g['%s.%s' % (s, ch)] = dict(valid=round(float(vv.mean()), 4), disc=len(ds))
            if vv.mean() < 0.99 or ds:
                g_ok = False
        spikes = {}
        for k, (s, ch) in enumerate(chans):
            x, vv, _ = raw_window(s, ch, t, L)
            xv = x[vv] - np.median(x[vv]) if vv.any() else np.zeros(1)
            mad = np.median(np.abs(xv - np.median(xv)))
            others = [c for j, c in enumerate(sd['ccs']) if j != k and c is not None]
            spikes['%s.%s' % (s, ch)] = dict(spike_over_8mad=bool(np.any(np.abs(xv) > 8 * max(mad, 0.5))), mad=float(mad),
                                             D_without=float(np.mean(others)) if others else None)
        nm = nullmax.get(n)
        gl_ok = True
        for k, sp in spikes.items():
            if sp['spike_over_8mad'] and (nm is None or sp['D_without'] is None or sp['D_without'] <= nm):
                gl_ok = False if nm is not None else gl_ok
        blk = event_block(cache, chans, t, M)
        halves = []
        for h in (slice(0, M // 2), slice(M // 2, M)):
            cs = []
            for (y, vv), tt in zip(blk, tm):
                if y is None:
                    continue
                a, b = tt[h] - tt[h].mean(), y[h] - y[h].mean()
                den = np.sqrt((a * a).sum() * (b * b).sum())
                cs.append(float((a * b).sum() / den) if den > 0 else 0.0)
            halves.append(float(np.mean(cs)) if cs else None)
        if any(hh is None or hh <= 0 for hh in halves):
            gl_ok = False
        el = float(solar_elevation_deg(onset, *STATIONS[sta]))
        res.setdefault(n, []).append(dict(onset=ns_iso(onset), window_start=ns_iso(t), D=sd['D'], ccs=sd['ccs'],
                                          best_cc=sd['best_cc'], catalogued=matches(rows, onset),
                                          onodera=onodera_check.matches(ono, onset), gap_ok=g_ok, gap=g,
                                          spikes=spikes, half_D=halves, glitch_ok=gl_ok,
                                          glitch_rule_applied_with_null_max=nm is not None,
                                          elev=el, thermal_ok=abs(el) > 12, phase=float(mean_anomaly_deg(onset))))
        r = res[n][-1]
        print('A%s %s D %.3f best %.3f cat %s ono %s gap %s glitch %s halves %s spikes %s elev %.0f' % (
            n, r['onset'], r['D'], r['best_cc'], bool(r['catalogued']), bool(r['onodera']), r['gap_ok'], r['glitch_ok'],
            [round(h, 3) for h in halves], [k for k, s in spikes.items() if s['spike_over_8mad']], el))
json.dump(res, open(out, 'w'), indent=1)
