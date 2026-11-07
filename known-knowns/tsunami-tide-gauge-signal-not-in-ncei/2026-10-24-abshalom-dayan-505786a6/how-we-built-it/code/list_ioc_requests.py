"""List every IOC SLSMF request behind the p3 maps: one row per quake, gauge code and window read, with the gauge's
model arrival time (ETA), the sensor scored, and the saved IOC responses (URL, UTC fetch time, sha256) that supply the
window. Written 2026-11-07; Python 3 standard library only. Run from the package folder:

    python3 how-we-built-it/code/list_ioc_requests.py > how-we-built-it/ioc_requests.csv

Inputs: object/quakes/*.json (gauges in scope, ETAs, tied sensors, per-sensor results), how-we-built-it/ioc_windows_1.tsv
and _2.tsv (every saved response, with its sha256 at fetch time). Which saved responses supply a window is reconstructed
with lib/det.py's own rules (ioc_raw, raw_window: the exact saved window if there is one; else, PREREG.v4, saved windows
of the same code covering >= 25 % of it with at most 3 gaps; stage 1 may also be an earlier run's [o-25 h, o+7 h] window
plus [o-31 h, o-25 h]) over the full set of saved responses. A piece no saved response covers is listed as GAP.

Columns: stage 1 is the [floor_h(o-31 h), ceil_h(o+7 h)] window read for the real and both fake origins; stage 2 is the
control-day window [floor_h(oo-8 d-1 h), ceil_h(oo+9 d)] of the origins named (real origin oo = o; fake origins o-5 h, o-7 h).
used_by says which map read it (v4: the headline map; v5: the sensitivity map). tied_sensors are the sea-level sensors
sharing the largest sample count in the stage-1 window; sensor_v4 is the first of them, the one the v4 code scores (for
stage 2 the v4 code takes the sensor with the most samples in that window; in the re-fetched windows it was the same
sensor, how-we-built-it/refetch_stage1_check.tsv and object/v4_ctrl_refetch.json). responses: one entry per saved IOC
response read, as T:L:sha256, where L is the line of how-we-built-it/ioc_windows_T.tsv that holds its URL (station and
UTC window), UTC fetch time and HTTP status, and sha256 is that of the raw JSON as fetched. An IOC response holds every
sensor of the station; the scored sensor is picked from it."""
import csv, glob, json, os, sys, datetime as dt

H = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(os.path.dirname(H))
HOUR = dt.timedelta(hours=1)


def floor_h(t):
    return t.replace(minute=0, second=0, microsecond=0)


def ceil_h(t):
    f = floor_h(t)
    return f if f == t else f + HOUR


def win(name):
    b = name[:-3] if name.endswith('.gz') else name
    p = b[:-5].rsplit('_', 2)
    return p[0], dt.datetime.strptime(p[1], '%Y%m%d%H%M'), dt.datetime.strptime(p[2], '%Y%m%d%H%M')


OLD, NEW, BYCODE = {}, {}, {}
for T in (1, 2):
    for L, r in enumerate(csv.DictReader(open(os.path.join(PKG, 'how-we-built-it', f'ioc_windows_{T}.tsv')), delimiter='\t'), 2):
        r['ref'] = f'{T}:{L}'
        name = os.path.basename(r['file'])
        c, a, b = win(name)
        key = (c, a, b)
        (OLD if '/ioc_old/' in r['file'] else NEW).setdefault(key, r)
        BYCODE.setdefault(c, {})[key] = r


def exact(c, a, b):
    return NEW.get((c, a, b)) or OLD.get((c, a, b))


def ioc_raw(c, a, b):
    """List of responses (table rows, or ('GAP', c, a, b)) that det.ioc_raw would read for [a, b]."""
    e = exact(c, a, b)
    if e:
        return [e]
    cand = [k for k in BYCODE.get(c, {}) if k[1] < b and k[2] > a]
    if cand:
        cur, use, gaps = a, [], []
        while cur < b:
            cov = [k for k in cand if k[1] <= cur < k[2]]
            if cov:
                k = max(cov, key=lambda k: k[2]); use.append(BYCODE[c][k]); cur = min(k[2], b)
            else:
                nxt = min([k[1] for k in cand if k[1] > cur] + [b]); gaps.append((cur, nxt)); cur = nxt
        covered = 1 - sum((y - x).total_seconds() for x, y in gaps) / (b - a).total_seconds()
        if covered >= 0.25 and len(gaps) <= 3:
            out = list(use)
            for x, y in gaps:
                out += ioc_raw(c, x, y)
            return out
    return [('GAP', c, a, b)]


def raw_window(c, t0, t1, split):
    if OLD.get((c, split, t1)) and not NEW.get((c, t0, t1)):
        return ioc_raw(c, t0, split) + ioc_raw(c, split, t1)
    return ioc_raw(c, t0, t1)


def fmt(t):
    return t.strftime('%Y-%m-%dT%H:%M:%SZ')


w = csv.writer(sys.stdout, lineterminator='\n')
w.writerow(['quake', 'stage', 'origin', 'code', 'site', 'eta_min', 'tied_sensors', 'sensor_v4', 'window_start_utc',
            'window_stop_utc', 'used_by', 'n_responses', 'responses'])
H5 = {'real': 0, 'fake5': 5, 'fake7': 7}
for f in sorted(glob.glob(os.path.join(PKG, 'object', 'quakes', '*.json'))):
    q = json.load(open(f))
    o = dt.datetime.strptime(q['origin'][:19], '%Y-%m-%d %H:%M:%S')
    t0, t1, sp = floor_h(o - 31 * HOUR), ceil_h(o + 7 * HOUR), floor_h(o - 25 * HOUR)
    for g in q['gauges']:
        tied = g.get('tied', []); per = g.get('res_by_sensor', {})
        s4 = tied[0] if tied and tied[0] in per else ''
        rows = [('1', 'real;fake5;fake7', t0, t1, 'v4;v5', raw_window(g['code'], t0, t1, sp))]
        st2 = {}
        for nm, h in H5.items():
            oo = o - h * HOUR
            W = (floor_h(oo - dt.timedelta(days=8, hours=1)), ceil_h(oo + dt.timedelta(days=9)))
            v4 = bool(s4) and per[s4][nm].get('detects')
            v5 = any('ctrl' in v[nm] for v in per.values())
            if v4 or v5:
                st2.setdefault(W, [set(), set()])
                st2[W][0].add(nm)
                st2[W][1].update(['v4'] if v4 else [])
                st2[W][1].update(['v5'] if v5 else [])
        for W, (nms, by) in st2.items():
            rows.append(('2', ';'.join(n for n in H5 if n in nms), W[0], W[1], ';'.join(sorted(by)), ioc_raw(g['code'], *W)))
        for stage, nms, a, b, by, resp in rows:
            parts = []
            for r in resp:
                if isinstance(r, tuple):
                    parts.append(f'GAP {fmt(r[2])}..{fmt(r[3])}')
                else:
                    parts.append(f"{r['ref']}:{r['sha256_of_raw_json']}")
            w.writerow([q['label'], stage, nms, g['code'], g['site'], g['eta'], ';'.join(tied), s4, fmt(a), fmt(b), by,
                        len(resp), ' '.join(parts)])
