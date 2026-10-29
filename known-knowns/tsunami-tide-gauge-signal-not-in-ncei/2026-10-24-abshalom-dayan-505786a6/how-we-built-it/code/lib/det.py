"""Detector D5 (PREREG.md section 2) and the per-source runner used by the map, the positive control and the screen."""
import os, json, gzip, hashlib, subprocess, datetime as dt, math
import numpy as np, pandas as pd
from scipy import signal
import tt

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RUN, 'data')
IOC = os.path.join(DATA, 'ioc'); os.makedirs(IOC, exist_ok=True)
# raw windows saved by earlier runs (a claim bundle carries the used ones, gzipped, under data/ioc_old/)
_OLD_LOCAL = [os.path.join(DATA, 'ioc_old', k) for k in ('2026-10-24-0850', '2026-10-24-1501')]
OLD = _OLD_LOCAL if os.path.isdir(_OLD_LOCAL[0]) else \
    [os.path.join(RUN, '..', '2026-10-24-0850', 'data', 'ioc'), os.path.join(RUN, '..', '2026-10-24-1501', 'data', 'ioc')]


def _oldp(d, name):
    """Path of a non-empty saved window name (.json, or .json.gz in a bundle) in folder d, else None."""
    for p in (os.path.join(d, name), os.path.join(d, name + '.gz')):
        if os.path.exists(p) and os.path.getsize(p) > 0:
            return p
    return None
UA = 'V3R1T4S-research (honest client)'
SEA = {'rad', 'ra2', 'ras', 'prs', 'prt', 'prte', 'pr1', 'pr2', 'bub', 'bub1', 'flt', 'enc', 'en2', 'aqu', 'pwl', 'wls',
       'ecs', 'bwl', 'stp'}
TT_SEL = json.load(open(os.path.join(RUN, 'attempts', 'evaluator-first', 'out', 'tt_selected.json')))
DMIN, C = float(TT_SEL['dmin']), float(TT_SEL['c'])
CTRL = list(range(-7, 0)) + list(range(2, 9))
MAXKM, ETA_LO, ETA_HI = 1000.0, 10.0, 150.0
# PREREG.v6 implementation corrections (stuck rule on raw samples, gap bridging <= 30 min only, fake-origin stage-2
# window); off by default so the as-run v4/v5 outputs still reproduce; the v6 drivers set det.IMPL6 = True.
IMPL6 = False


class Blocked(RuntimeError):
    pass


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _trace(p):
    if os.environ.get('V3_TRACE'):
        with open(os.environ['V3_TRACE'], 'a') as f:
            f.write((p if p.startswith('OFFLINE_MISS') else os.path.relpath(os.path.abspath(p), RUN)) + '\n')


def _fetch(url, fn_gz):
    if os.environ.get('V3_OFFLINE'):
        _trace('OFFLINE_MISS ' + url)
        return 'offline', b''
    tmp = fn_gz + '.part'
    t = utc()
    r = subprocess.run(['curl', '-g', '-s', '--compressed', '-m', '180', '-A', UA, '-o', tmp, '-w', '%{http_code} %{size_download}', url],
                       capture_output=True, text=True)
    parts = (r.stdout.strip() or '000 0').split()
    code, nbytes = parts[0], parts[1] if len(parts) > 1 else '0'
    raw = open(tmp, 'rb').read() if os.path.exists(tmp) else b''
    h = hashlib.sha256(raw).hexdigest()
    with open(os.path.join(DATA, 'fetch_log.tsv'), 'a') as f:
        f.write(f'{url}\t{t}\t{code}\t{h}\t{len(raw)}\t{os.path.relpath(fn_gz, RUN)}\ttransfer={nbytes}\n')
    if code in ('401', '403', '429', '503'):
        raise Blocked(f'BLOCKED {code} {url}')
    if code == '200':
        with gzip.open(fn_gz, 'wb') as g:
            g.write(raw)
    if os.path.exists(tmp):
        os.remove(tmp)
    return code, raw


_OLDIDX = None


def _win(n):
    """(code, t0, t1) from a cache file name, or None."""
    b = n[:-3] if n.endswith('.gz') else n
    if not b.endswith('.json'):
        return None
    p = b[:-5].rsplit('_', 2)
    if len(p) != 3:
        return None
    try:
        return p[0], pd.Timestamp(dt.datetime.strptime(p[1], '%Y%m%d%H%M')), pd.Timestamp(dt.datetime.strptime(p[2], '%Y%m%d%H%M'))
    except ValueError:
        return None


def _cached_windows(code):
    global _OLDIDX
    if _OLDIDX is None:
        _OLDIDX = {}
        for d in OLD:
            for n in os.listdir(d):
                w = _win(n)
                if w and os.path.getsize(os.path.join(d, n)) > 0:
                    _OLDIDX.setdefault(w[0], []).append((w[1], w[2], os.path.join(d, n)))
    c = list(_OLDIDX.get(code, []))
    for n in os.listdir(IOC):
        if n.startswith(code + '_') and n.endswith('.json.gz'):
            w = _win(n)
            if w and w[0] == code:
                c.append((w[1], w[2], os.path.join(IOC, n)))
    return c


def _load(p):
    _trace(p)
    raw = gzip.open(p, 'rb').read() if p.endswith('.gz') else open(p, 'rb').read()
    try:
        d = json.loads(raw)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def ioc_raw(code, t0, t1, compose_only=False):
    """Raw JSON list for [t0, t1] (PREREG.v4 data access): an exact cached window; else, if saved windows of the same
    code (this run or earlier runs) cover >= 25 % of it, those plus one GET per uncovered gap, rows cut to [t0, t1];
    else one GET."""
    name = f'{code}_{t0:%Y%m%d%H%M}_{t1:%Y%m%d%H%M}.json'
    if compose_only or not os.path.exists(os.path.join(IOC, name + '.gz')) and not any(_oldp(d, name) for d in OLD):
        cand = [c for c in _cached_windows(code) if c[0] < t1 and c[1] > t0 and not (compose_only and c[0] == t0 and c[1] == t1)]
        if cand:
            cur, use, gaps = t0, [], []
            while cur < t1:
                cov = [c for c in cand if c[0] <= cur < c[1]]
                if cov:
                    b = max(cov, key=lambda c: c[1]); use.append(b[2]); cur = min(b[1], t1)
                else:
                    nxt = min([c[0] for c in cand if c[0] > cur] + [t1]); gaps.append((cur, nxt)); cur = nxt
            covered = 1 - sum((b - a).total_seconds() for a, b in gaps) / (t1 - t0).total_seconds()
            if covered >= 0.25 and len(gaps) <= 3:
                rows = []
                for p in use:
                    rows += _load(p)
                for a, b in gaps:
                    rows += ioc_raw(code, a, b)
                lo, hi = f'{t0:%Y-%m-%d %H:%M:%S}', f'{t1:%Y-%m-%d %H:%M:%S}'
                return [r for r in rows if isinstance(r, dict) and lo <= str(r.get('stime', '')) <= hi]
    return _ioc_raw_exact(code, t0, t1)


def _ioc_raw_exact(code, t0, t1):
    """Raw JSON list for [t0, t1]: this run's gzip cache, else an earlier run's identical window, else one GET."""
    name = f'{code}_{t0:%Y%m%d%H%M}_{t1:%Y%m%d%H%M}.json'
    fn = os.path.join(IOC, name + '.gz')
    raw = None
    if os.path.exists(fn):
        raw = gzip.open(fn, 'rb').read(); _trace(fn)
    else:
        for d in OLD:
            p = _oldp(d, name)
            if p:
                raw = gzip.open(p, 'rb').read() if p.endswith('.gz') else open(p, 'rb').read(); _trace(p); break
    if raw is None:
        url = (f'https://www.ioc-sealevelmonitoring.org/service.php?query=data&code={code}'
               f'&timestart={t0:%Y-%m-%dT%H:%M:%S}&timestop={t1:%Y-%m-%dT%H:%M:%S}&format=json')
        c, raw = _fetch(url, fn)
        if c != '200':
            return []
    try:
        d = json.loads(raw)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def floor_h(t):
    return t.floor('h')


def ceil_h(t):
    return t.ceil('h')


def raw_window(code, t0, t1, alt_split=None):
    """Raw rows for [t0, t1]; if an earlier run cached [alt_split, t1] exactly, use it plus [t0, alt_split]."""
    if alt_split is not None:
        name = f'{code}_{alt_split:%Y%m%d%H%M}_{t1:%Y%m%d%H%M}.json'
        if any(_oldp(d, name) for d in OLD) \
                and not os.path.exists(os.path.join(IOC, f'{code}_{t0:%Y%m%d%H%M}_{t1:%Y%m%d%H%M}.json.gz')):
            return ioc_raw(code, t0, alt_split) + ioc_raw(code, alt_split, t1)
    return ioc_raw(code, t0, t1)


def series(rows, t0, t1, sensor=None):
    """1-min series of the best sea-level sensor (gaps <= 5 min filled, longer NaN, v5 spikes NaN); (None, reason) if none.
    sensor: score this sensor instead of the one with the most samples (PREREG.v5 rule 2)."""
    if not rows:
        return None, 'no data'
    df = pd.DataFrame(rows)
    if 'sensor' not in df or 'slevel' not in df or df.empty:
        return None, 'no data'
    df = df[df.sensor.isin(SEA)]
    if df.empty:
        return None, 'no sea-level sensor'
    if sensor is None:
        sensor = df.sensor.value_counts().idxmax()
    df = df[df.sensor == sensor].drop_duplicates('stime')
    v = pd.to_numeric(df.slevel, errors='coerce')
    s = pd.Series(v.values, index=pd.to_datetime(df.stime)).sort_index().dropna()
    s = s[~s.index.duplicated()]
    s0_index = s.index
    raw = s.copy() if IMPL6 else None
    if len(s) < 60:
        return None, f'{sensor}: too few samples'
    idx = pd.date_range(t0, t1, freq='1min')
    s = s.reindex(s.index.union(idx)).interpolate(method='time', limit=5, limit_area='inside').reindex(idx)
    # minutes farther than 5 min from a real sample on either side stay NaN
    rt = pd.Series(1.0, index=pd.DatetimeIndex(s0_index).sort_values())
    pos = rt.index.searchsorted(idx)
    prev_t = rt.index[np.clip(pos - 1, 0, len(rt) - 1)]
    next_t = rt.index[np.clip(pos, 0, len(rt) - 1)]
    exact = rt.index[np.clip(pos, 0, len(rt) - 1)] == idx
    dprev = (idx - prev_t).total_seconds().values / 60.0
    dnext = (next_t - idx).total_seconds().values / 60.0
    ok = exact | ((pos > 0) & (pos < len(rt)) & (dprev <= 5) & (dnext <= 5))
    s[~ok] = np.nan
    # spike rule v5: isolated one-sample excursions
    m = s.rolling(11, center=True, min_periods=6).median()
    a = (s - m).abs()
    sc = (a.rolling(11, center=True, min_periods=6).median() * 1.4826).clip(lower=0.003)
    big = a > 8 * sc
    small = a < 3 * sc
    spike = big & small.shift(1, fill_value=False) & small.shift(-1, fill_value=False)
    s[spike] = np.nan
    s.attrs['sensor'] = sensor
    s.attrs['n_spikes'] = int(spike.sum())
    if IMPL6:
        s.attrs['raw'] = raw
    return s, sensor


def _bridge(s, limit):
    """PREREG.v6 item 3: fill runs of at most `limit` missing minutes between two present minutes; longer runs stay NaN."""
    na = s.isna().values
    if not na.any():
        return s
    full = s.interpolate(limit_area='inside')
    e = np.flatnonzero(np.diff(np.r_[0, na.astype(int), 0]))
    keep = np.zeros(len(s), bool)
    for i0, i1 in zip(e[::2], e[1::2]):
        if i1 - i0 <= limit:
            keep[i0:i1] = True
    return s.where(~(na & keep), full)


def _fill(s, limit):
    return _bridge(s, limit) if IMPL6 else s.interpolate(limit=limit, limit_area='inside')


def highpass(s, cutoff_cpm=1 / 120.0, order=4, min_seg=360, fill_for_filter=30):
    b, a = signal.butter(order, cutoff_cpm / 0.5, btype='highpass')
    out = pd.Series(np.nan, index=s.index)
    orig_nan = s.isna().values
    sf = _fill(s, fill_for_filter)
    ok = sf.notna().values
    edges = np.flatnonzero(np.diff(np.r_[0, ok.astype(int), 0]))
    for i0, i1 in zip(edges[::2], edges[1::2]):
        if i1 - i0 >= min_seg:
            out.iloc[i0:i1] = signal.filtfilt(b, a, sf.values[i0:i1])
    out[orig_nan] = np.nan
    out[out.abs() > 10.0] = np.nan
    return out


def highpass_causal(s, cutoff_cpm=1 / 120.0, order=4, min_seg=360, fill_for_filter=30):
    """PREREG.v2: the same Butterworth run forward only (no output before the input changes), for the arrival pick."""
    b, a = signal.butter(order, cutoff_cpm / 0.5, btype='highpass')
    zi0 = signal.lfilter_zi(b, a)
    out = pd.Series(np.nan, index=s.index)
    orig_nan = s.isna().values
    sf = _fill(s, fill_for_filter)
    ok = sf.notna().values
    edges = np.flatnonzero(np.diff(np.r_[0, ok.astype(int), 0]))
    for i0, i1 in zip(edges[::2], edges[1::2]):
        if i1 - i0 >= min_seg:
            x = sf.values[i0:i1]
            out.iloc[i0:i1] = signal.lfilter(b, a, x, zi=zi0 * x[0])[0]
    out[orig_nan] = np.nan
    out[out.abs() > 10.0] = np.nan
    return out


def stuck(s, o):
    if IMPL6 and s.attrs.get('raw') is not None:   # PREREG.v6 item 2: raw samples of the scored sensor
        src = s.attrs['raw']
    else:
        src = s
    pre = src[o - pd.Timedelta(hours=24):o - pd.Timedelta(minutes=1)].dropna().values
    if len(pre) < 60:
        return False
    runs = np.diff(np.flatnonzero(np.r_[True, np.diff(pre) != 0, True]))
    return bool(runs.max() >= 60)


def tied_sensors(rows):
    """Sea-level sensors sharing the largest raw sample count, in value_counts order (the first is series()'s choice)."""
    if not rows:
        return []
    df = pd.DataFrame(rows)
    if 'sensor' not in df or 'slevel' not in df:
        return []
    vc = df[df.sensor.isin(SEA)].sensor.value_counts()
    return [k for k, v in vc.items() if v == vc.iloc[0]] if len(vc) else []


def stat(s, bp, o, eta, bpc=None):
    """PREREG section 2 per-origin statistic (arrival on the causal filter bpc, PREREG.v2); usable flag always present."""
    pre = bp[o - pd.Timedelta(hours=24):o - pd.Timedelta(minutes=1)]
    W = bp[o + pd.Timedelta(minutes=eta - 10):o + pd.Timedelta(minutes=eta + 120)]
    covp = float(pre.notna().mean()) if len(pre) else 0.0
    covw = float(W.notna().mean()) if len(W) else 0.0
    st = stuck(s, o)
    rms = float(np.sqrt(np.nanmean(pre.values ** 2))) if pre.notna().any() else float('nan')
    usable = bool(covp >= 0.8 and covw >= 0.5 and not st and rms > 0)
    d = dict(usable=usable, cov_pre=round(covp, 3), cov_w=round(covw, 3), stuck=st)
    if not usable:
        return d
    peak = float(np.nanmax(np.abs(W.values)))
    if bpc is None:
        bpc = highpass_causal(s)
    prec = bpc[o - pd.Timedelta(hours=24):o - pd.Timedelta(minutes=1)]
    rmsc = float(np.sqrt(np.nanmean(prec.values ** 2))) if prec.notna().any() else float('nan')
    aw = bpc[o + pd.Timedelta(minutes=eta - 30):o + pd.Timedelta(minutes=eta + 60)]
    ex = aw[np.abs(aw) > 3 * rmsc]
    arr = None if ex.empty else (ex.index[0] - o).total_seconds() / 60.0
    r = peak / rms
    d.update(r=round(r, 3), peak=round(peak, 4), rms24=round(rms, 5), arrival=None if arr is None else round(arr, 2),
             detects=bool(r > 5 and arr is not None and abs(arr - eta) <= 10))
    return d


_ST = None
def stations():
    global _ST
    if _ST is None:
        d = json.load(open(os.path.join(DATA, 'ioc_stationlist.json')))
        rows, seen = [], set()
        for x in d:
            if x.get('Lat') is None or x.get('sensor') not in SEA or x['Code'] in seen:
                continue
            if 'DART' in (x.get('Location') or '').upper():
                continue
            seen.add(x['Code'])
            rows.append(dict(code=x['Code'], name=x['Location'], country=x.get('country'), lat=float(x['Lat']), lon=float(x['Lon'])))
        _ST = pd.DataFrame(rows)
    return _ST


def sites_of(gs):
    """Group codes within 2 km into sites (greedy, by distance order)."""
    site = {}
    reps = []
    for g in gs:
        for k, (la, lo) in enumerate(reps):
            if tt.gc_km(la, lo, g['lat'], g['lon']) <= 2.0:
                site[g['code']] = k; break
        else:
            site[g['code']] = len(reps); reps.append((g['lat'], g['lon']))
    return site


def run_source(label, origin, lat, lon, fakes=(), do_stage2=True, maxkm=MAXKM, log=None):
    """Stage 1 (+ stage 2 for detecting codes) at the real origin and at fake origins (hours before)."""
    o = pd.Timestamp(origin)
    if o.tzinfo is not None:
        o = o.tz_convert(None)
    o = o.floor('s')
    st = stations().copy()
    st['km'] = tt.gc_km(lat, lon, st.lat.values, st.lon.values)
    st = st[st.km <= maxkm].sort_values('km')
    res = dict(label=label, origin=str(o), lat=lat, lon=lon, alt=int(tt.alt_at(lat, lon)), dmin=DMIN, c=C, fakes=list(fakes))
    try:
        f = tt.FMM(lat, lon, radius_km=1700)
        res['src_snap_km'] = f.src_snap_km
    except RuntimeError as ex:
        res['error'] = f'tt: {ex}'; res['gauges'] = []; return res
    gs = []
    for _, g in st.iterrows():
        t, sd, h = f.eta(g.lat, g.lon, dmin=DMIN)
        if not np.isfinite(t):
            continue
        eta = t + C
        if ETA_LO <= eta <= ETA_HI:
            gs.append(dict(code=g.code, name=g['name'], country=g.country, lat=g.lat, lon=g.lon, km=round(float(g.km), 1),
                           eta=round(float(eta), 2), snap_km=round(sd, 2), snap_depth=h))
    site = sites_of(gs)
    for g in gs:
        g['site'] = site[g['code']]
    t0 = floor_h(o - pd.Timedelta(hours=31)); t1 = ceil_h(o + pd.Timedelta(hours=7)); split = floor_h(o - pd.Timedelta(hours=25))
    T0 = floor_h(o - pd.Timedelta(days=8, hours=1)); T1 = ceil_h(o + pd.Timedelta(days=9))
    origins = [('real', o)] + [(f'fake{h}', o - pd.Timedelta(hours=h)) for h in fakes]
    for g in gs:
        rows = raw_window(g['code'], t0, t1, alt_split=split)
        s, info = series(rows, t0, t1)
        if s is None:
            g['status'] = info; continue
        g['sensor'] = info; g['n_spikes'] = s.attrs.get('n_spikes')
        bp = highpass(s); bpc = highpass_causal(s)
        g['res'] = {nm: stat(s, bp, oo, g['eta'], bpc) for nm, oo in origins}
        need = [nm for nm, oo in origins if g['res'][nm].get('detects')]
        if need and do_stage2:
            win = {}
            for nm, oo in origins:
                if nm not in need:
                    continue
                W2 = (floor_h(oo - pd.Timedelta(days=8, hours=1)), ceil_h(oo + pd.Timedelta(days=9))) \
                    if IMPL6 and nm != 'real' else (T0, T1)
                if W2 not in win:
                    rows2 = ioc_raw(g['code'], *W2)
                    s2, info2 = series(rows2, *W2)
                    win[W2] = (s2, highpass(s2) if s2 is not None else None, highpass_causal(s2) if s2 is not None else None)
                s2, bp2, bpc2 = win[W2]
                ctrl = []
                for k in CTRL:
                    if bp2 is None:
                        ctrl.append(None); continue
                    c = stat(s2, bp2, oo + pd.Timedelta(days=k), g['eta'], bpc2)
                    ctrl.append(dict(day=k, r=c.get('r'), detects=c.get('detects')) if c['usable'] else None)
                valid = [c for c in ctrl if c is not None]
                R = g['res'][nm]
                R['ctrl_n'] = len(valid); R['ctrl_any_detect'] = any(c['detects'] for c in valid)
                R['ctrl_max_r'] = max([c['r'] for c in valid], default=None)
                R['passes'] = bool(len(valid) >= 10 and not R['ctrl_any_detect'])
                R['undecided'] = bool(len(valid) < 10)
        if log:
            log(g)
    res['gauges'] = gs
    summ = {}
    for nm, _ in origins:
        us = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('usable')}
        de = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('detects')}
        pa = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('passes')}
        und = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('undecided')
               and not g['res'][nm].get('ctrl_any_detect')}
        if not gs:
            cls = 'NO_GAUGE'
        elif not us:
            cls = 'NO_DATA'
        elif pa:
            cls = 'SIGNAL'
        elif und:
            cls = 'SIGNAL_UNDECIDED'
        else:
            cls = 'NO_SIGNAL'
        summ[nm] = dict(cls=cls, n_sites=len(set(site.values())), n_usable=len(us), n_detect=len(de), n_pass=len(pa))
    res['summary'] = summ
    return res
