"""Candidates from the frozen scan (PREREG R4-R6 and the candidate checks).

usage: candidates.py FROZEN.npz SCAN.jsonl CATALOG_DIR OUT_PREFIX
1. Null maxima over the full span: C0 = time-reversed data, C1..CN = phase-randomised templates.
2. Candidates = forward declustered detections with D above every control's full-span maximum.
3. For each: catalogue check (all PDS tables), best single-channel CC (R4), gap, glitch, thermal checks, and the
   anomalistic phase (M') for information.
"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
import datetime as dt
from apollo_lib import NS, RATE, load_day, ns_iso, day_start_ns, despike, DAY_SAMPLES
from evlib import FS, DayCache, event_block
from catalog_check import load_all, matches, UNPARSED
from ephem import solar_elevation_deg, mean_anomaly_deg, STATIONS
from scan import NDAY

npz = np.load(sys.argv[1]); theta = float(npz['theta'])
tm = list(npz['tm']); chans = [tuple(c.split('.')) for c in npz['chans']]
band = tuple(float(b) for b in npz['band'])
if len(band) > 2 and band[2] == 0:
    band = band[:2]
L = float(npz['L']); M = tm[0].size
days = [json.loads(l) for l in open(sys.argv[2])]
rows = load_all(sys.argv[3])
out = sys.argv[4]
c0 = max(d['rev_max'] for d in days if d.get('rev_max') is not None)
nctrl = max(len(d.get('ctrl_max', [])) for d in days)
ck = [max(d['ctrl_max'][k] for d in days if d.get('ctrl_max') and d['ctrl_max'][k] is not None) for k in range(nctrl)]
best_control = max([c0] + ck)
peaks = [(p[0], p[1], p[2], p[3]) for d in days for p in d.get('fwd_peaks', [])]
cands = [p for p in peaks if p[1] > best_control]
cache = DayCache(band)


def raw_window(sta, ch, t_ns, dur_s):
    """raw samples (6.625 Hz grid) and validity for [t, t+dur) possibly across midnight; disc indices inside."""
    xs, vs, ds = [], [], []
    t = t_ns; remaining = int(dur_s * RATE)
    while remaining > 0:
        d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t // NS)
        y, doy = d.year, d.timetuple().tm_yday
        t0 = day_start_ns(y, doy)
        i0 = int(round((t - t0) / NS * RATE))
        n = min(remaining, DAY_SAMPLES - i0)
        r = load_day(sta, ch, y, doy)
        if r is None:
            xs.append(np.zeros(n)); vs.append(np.zeros(n, bool))
        else:
            xs.append(r[0][i0:i0 + n].astype(float)); vs.append(r[1][i0:i0 + n])
            ds += [k for k in r[2] if i0 <= k < i0 + n]
        remaining -= n; t = t0 + 86400 * NS
    return np.concatenate(xs), np.concatenate(vs), ds


res = []
for (t, D, ccs, nv) in sorted(cands, key=lambda p: -p[1]):
    onset = t + 30 * NS
    cat = matches(rows, onset)
    ccs_f = [c for c in ccs if c is not None]
    best_cc = max(ccs_f) if ccs_f else None
    # gap check: [onset - 10 min, onset + L + 10 min]
    g_ok = True; g_info = {}
    for (sta, ch) in chans:
        x, v, ds = raw_window(sta, ch, onset - 600 * NS, L + 1200)
        g_info['%s.%s' % (sta, ch)] = dict(valid=round(float(v.mean()), 4), disc=len(ds))
        if v.mean() < 0.99 or ds:
            g_ok = False
    # glitch check
    gl_ok = True; gl_info = {}
    for k, (sta, ch) in enumerate(chans):
        x, v, _ = raw_window(sta, ch, t, L)
        xv = x[v] - np.median(x[v]) if v.any() else np.zeros(1)
        mad = np.median(np.abs(xv - np.median(xv)))
        big = bool(np.any(np.abs(xv) > 8 * max(mad, 0.5)))
        others = [c for j, c in enumerate(ccs) if j != k and c is not None]
        d_wo = float(np.mean(others)) if others else None
        gl_info['%s.%s' % (sta, ch)] = dict(spike_over_8mad=big, mad=float(mad), D_without=d_wo)
        if big and (d_wo is None or d_wo < theta):
            gl_ok = False
    # half-template CC (first and second halves) at the detection lag
    blk = event_block(cache, chans, t, M)
    halves = []
    for h in (slice(0, M // 2), slice(M // 2, M)):
        cs = []
        for (y, v), tt in zip(blk, tm):
            if y is None:
                continue
            a, b = tt[h] - tt[h].mean(), y[h] - y[h].mean()
            den = np.sqrt((a * a).sum() * (b * b).sum())
            cs.append(float((a * b).sum() / den) if den > 0 else 0.0)
        halves.append(float(np.mean(cs)) if cs else None)
    if any(hh is None or hh <= 0 for hh in halves):
        gl_ok = False
    elev = float(solar_elevation_deg(onset, *STATIONS['s12']))
    th_ok = abs(elev) > 12.0
    res.append(dict(window_start=ns_iso(t), onset=ns_iso(onset), D=D, ccs=ccs, best_single_cc=best_cc,
                    r4_cc_ge_0p6=bool(best_cc is not None and best_cc >= 0.6), catalogued=cat, new=not cat,
                    gap_ok=g_ok, gap=g_info, glitch_ok=gl_ok, glitch=gl_info, half_D=halves,
                    solar_elev_s12=elev, thermal_ok=th_ok, anomalistic_phase_deg=float(mean_anomaly_deg(onset))))
summary = dict(theta=theta, c0_time_reversed_max=c0, controls=nctrl, best_phase_random_max=max(ck) if ck else None,
               best_control=best_control, n_fwd_peaks=len(peaks), n_candidates=len(cands),
               n_new=sum(r['new'] for r in res),
               n_p1=sum(r['new'] and r['r4_cc_ge_0p6'] and r['gap_ok'] and r['glitch_ok'] and r['thermal_ok'] for r in res),
               unparsed_catalogue_rows=UNPARSED)
json.dump(dict(summary=summary, candidates=res, ctrl_full_span_max=[c0] + ck), open(out + '.json', 'w'), indent=1)
print(json.dumps(summary, indent=1))
for r in res:
    print(r['onset'], 'D=%.3f' % r['D'], 'bestCC=%s' % r['best_single_cc'], 'new=%s' % r['new'], r['catalogued'][:2],
          'gap', r['gap_ok'], 'glitch', r['glitch_ok'], 'elev %.0f' % r['solar_elev_s12'])
