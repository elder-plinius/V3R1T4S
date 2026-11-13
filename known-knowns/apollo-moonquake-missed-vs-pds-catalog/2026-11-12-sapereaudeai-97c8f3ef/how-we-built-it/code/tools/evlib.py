"""Event-window helpers: preprocessed day cache, event windows, alignment and stacking (network templates)."""
import datetime as dt
import numpy as np
import pandas as pd
from apollo_lib import (load_span, preprocess, RATE, NS, DAY_SAMPLES, day_start_ns, cat_time_ns, norm_template,
                        station_ncc)

DEC = 2
FS = RATE / DEC  # 3.3125 Hz


class DayCache:
    def __init__(self, band, extra_s=7200):
        self.band = band
        self.extra = int(extra_s * RATE)
        self.c = {}

    def get(self, sta, ch, year, doy):
        k = (sta, ch, year, doy)
        if k not in self.c:
            r = load_span(sta, ch, year, doy, self.extra)
            if r is None:
                self.c[k] = None
            else:
                x, v, disc = r
                y, vd = preprocess(x, v, self.band, dec=DEC)
                self.c[k] = (y, vd, disc)
            if len(self.c) > 400:
                self.c.pop(next(iter(self.c)))
        return self.c[k]


def window(cache, sta, ch, t_ns, nsamp):
    """Decimated preprocessed samples from t_ns for nsamp samples (and valid mask). None if day missing."""
    d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t_ns // NS)
    year, doy = d.year, d.timetuple().tm_yday
    r = cache.get(sta, ch, year, doy)
    if r is None:
        return None
    y, vd, _ = r
    i0 = int(round((t_ns - day_start_ns(year, doy)) / NS * FS))
    if i0 < 0 or i0 + nsamp > len(y):
        return None
    return y[i0:i0 + nsamp], vd[i0:i0 + nsamp]


def load_nest_events(csv, nest='1', years=None):
    cat = pd.read_csv(csv, dtype=str)
    a = cat[(cat['T2'] == 'A') & (cat['N2'].str.strip() == nest)].copy()
    if years is not None:
        a = a[a['Y'].isin(years)]
    a['t_ns'] = [cat_time_ns(r.Y, r.JD, r.S) for r in a.itertuples()]
    a['A1n'] = pd.to_numeric(a['A1'], errors='coerce')
    a['A2n'] = pd.to_numeric(a['A2'], errors='coerce')
    return a.reset_index(drop=True)


def event_block(cache, chans, t0_ns, nsamp):
    """Return list over chans of (y, v) or (None, None)."""
    out = []
    for sta, ch in chans:
        w = window(cache, sta, ch, t0_ns, nsamp)
        out.append(w if w is not None else (None, None))
    return out


def best_lag(cache, chans, tmpls, t_lo_ns, t_hi_ns, min_comps=2):
    """Scan window starts from t_lo to t_hi (ns); return (best D, best start ns, ccs at best, D series)."""
    M = len(tmpls[0])
    n = int((t_hi_ns - t_lo_ns) / NS * FS) + M + 1
    blk = event_block(cache, chans, t_lo_ns, n)
    ys = [b[0] for b in blk]; vs = [b[1] for b in blk]
    if sum(y is not None for y in ys) < min_comps:
        return None
    ys2 = [y if y is not None else np.zeros(n) for y in ys]
    vs2 = [v if v is not None else np.zeros(n, bool) for v in vs]
    D, ccs = station_ncc(ys2, vs2, tmpls, min_comps=min_comps)
    if np.all(np.isnan(D)):
        return None
    k = int(np.nanargmax(D))
    return float(D[k]), t_lo_ns + int(k / FS * NS), ccs[:, k], D


def stack_events(cache, chans, starts_ns, M):
    """Per channel: mean of unit-norm windows (only events with that channel fully valid). Returns templates
    (unit-norm, zero-mean) and per-channel counts."""
    sums = [np.zeros(M) for _ in chans]
    cnt = [0 for _ in chans]
    for t in starts_ns:
        blk = event_block(cache, chans, t, M)
        for i, (y, v) in enumerate(blk):
            if y is None or v.mean() < 0.95:
                continue
            y = y - y.mean()
            n = np.sqrt((y * y).sum())
            if n == 0:
                continue
            sums[i] += y / n
            cnt[i] += 1
    tm = [norm_template(s) if c > 0 else None for s, c in zip(sums, cnt)]
    return tm, cnt
