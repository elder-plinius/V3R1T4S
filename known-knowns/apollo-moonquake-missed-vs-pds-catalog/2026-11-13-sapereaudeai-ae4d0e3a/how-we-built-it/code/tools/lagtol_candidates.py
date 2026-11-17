"""(lag-tolerant variant for PREREG.v14: peaks carry per-station lags; R7 uses each station's CC at its own best lag)
Candidates of a coincidence scan (PREREG.v8 / v10): per nest, null maxima (C0 reversed, C1..C400 shifts),
forward peaks above every control, then R6 (all PDS tables + Onodera list), R7 (best single-channel CC >= 0.5 at
both stations), p1 (>= 0.6 at one station), R9 (nest phase interval), gap and thermal checks. R8 (ATT moveout) is
done separately for any candidate that passes the rest.

usage: coinc_candidates.py NETS.npz SCAN.jsonl CATALOG_DIR LIT_DIR OUT_PREFIX
"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
import datetime as dt
from apollo_lib import NS, RATE, ns_iso, load_day, day_start_ns, DAY_SAMPLES
from evlib import load_nest_events
from catalog_check import load_all, matches
import onodera_check
from ephem import solar_elevation_deg, mean_anomaly_deg, STATIONS

z = np.load(sys.argv[1]); nests = [str(n) for n in z['nests']]; chans = [tuple(c.split('.')) for c in z['chans']]
L = float(z['L'])
days = [json.loads(l) for l in open(sys.argv[2])]
rows = load_all(sys.argv[3]); ono = onodera_check.load(sys.argv[4]); out = sys.argv[5]
stations = []
for c in chans:
    if c[0] not in stations:
        stations.append(c[0])
idx = {s: [k for k, c in enumerate(chans) if c[0] == s] for s in stations}


def phase_interval(nest):
    ev = load_nest_events(sys.argv[3] + '/levent.1008weber.csv', nest)
    ph = np.sort(mean_anomaly_deg(ev['t_ns'].values.astype(np.int64)))
    n = len(ph); k = int(np.ceil(0.95 * n))
    ext = np.concatenate([ph, ph + 360]); w = ext[k - 1:k - 1 + n] - ext[:n]; i = int(np.argmin(w))
    return float(ext[i] % 360), float(ext[i + k - 1] % 360)


def in_iv(p, iv):
    a, b = iv
    return (a <= p <= b) if a <= b else (p >= a or p <= b)


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


summary = {}
cands = {}
for n in nests:
    dd = [d['nests'][n] for d in days if n in d.get('nests', {})]
    c0 = max(d['rev_max'] for d in dd if d.get('rev_max') is not None)
    nsh = max(len(d.get('shift_max', [])) for d in dd)
    ck = [max(d['shift_max'][k] for d in dd if d.get('shift_max') and d['shift_max'][k] is not None) for k in range(nsh)]
    best = max([c0] + ck)
    peaks = sorted([(p[0], p[1], p[2], p[3], p[4]) for d in dd for p in d.get('fwd_peaks', [])], key=lambda p: -p[1])
    iv = phase_interval(n)
    res = []
    for (t, D, ccs, lag12, lag14) in peaks[:60]:
        onset = t + 30 * NS
        cat = matches(rows, onset); on = onodera_check.matches(ono, onset)
        bc = {s: max([ccs[i] for i in idx[s] if ccs[i] is not None] or [None], key=lambda x: -9 if x is None else x) for s in stations}
        ph = float(mean_anomaly_deg(onset))
        g_ok = True
        for (sta, ch) in chans:
            x, v, ds = raw_window(sta, ch, onset - 600 * NS, L + 1200)
            if v.mean() < 0.99 or ds:
                g_ok = False
        el = {s: float(solar_elevation_deg(onset, *STATIONS[s])) for s in stations}
        res.append(dict(onset=ns_iso(onset), Dc=D, above_null=D > best, ccs=ccs, best_cc=bc, lag12_s=lag12, lag14_s=lag14,
                        r7=all(bc[s] is not None and bc[s] >= 0.5 for s in stations),
                        p1_cc=any(bc[s] is not None and bc[s] >= 0.6 for s in stations),
                        catalogued=cat, onodera=on, new=not cat, phase=ph, r9=in_iv(ph, iv), gap_ok=g_ok,
                        elev=el, thermal_ok=all(abs(e) > 12 for e in el.values())))
    summary[n] = dict(c0=c0, best_shift=max(ck) if ck else None, best_control=best, n_peaks=len(peaks),
                      n_above=sum(p[1] > best for p in peaks), phase_interval=iv,
                      n_above_new=sum(r['above_null'] and r['new'] for r in res))
    cands[n] = res
    print('A%s: null C0 %.3f, best shift %.3f, best control %.3f; peaks above: %d (new %d); phase interval %s' % (
        n, c0, max(ck) if ck else -1, best, summary[n]['n_above'], summary[n]['n_above_new'], iv))
    for r in [x for x in res if x['above_null'] and x['new']] + res[:5]:
        print('   ', r['onset'], 'Dc=%.3f' % r['Dc'], 'ABOVE' if r['above_null'] else '-', 'bestcc', r['best_cc'],
              'new' if r['new'] else r['catalogued'][:1], 'onodera' if r['onodera'] else '', 'r9' if r['r9'] else 'r9-fail',
              'gap' if r['gap_ok'] else 'gap-fail', 'elev', {k: round(v) for k, v in r['elev'].items()})
json.dump(dict(summary=summary, candidates=cands), open(out + '.json', 'w'), indent=1)
