"""All dated rows of the PDS Apollo seismic event catalogue tables as (start_ns, end_ns, label) intervals,
and a lookup for R6: a time is 'catalogued' if any row time is within +/- 5 min of it or it lies between a levent
row's start and stop (E; 9999 = continues to the next event)."""
import os
import numpy as np
import pandas as pd
from apollo_lib import day_start_ns, NS

MIN5 = 300 * NS
UNPARSED = []  # rows whose date field is malformed in the source table (reported, not silently dropped)


def _ymdhm(s):
    s = str(s).strip().split('.')[0].zfill(10)
    yy, mo, dd, hh, mi = int(s[0:2]), int(s[2:4]), int(s[4:6]), int(s[6:8]), int(s[8:10])
    import datetime as dt
    t = dt.datetime(1900 + yy, mo, dd, hh, mi)
    d = t - dt.datetime(1970, 1, 1)
    return (d.days * 86400 + d.seconds) * NS


def load_all(catdir):
    rows = []
    lv = pd.read_csv(os.path.join(catdir, 'levent.1008weber.csv'), dtype=str)
    starts = []
    for r in lv.itertuples():
        y = 1900 + int(r.Y); d = int(r.JD); s = str(r.S).strip().zfill(4)
        t = day_start_ns(y, d) + (int(s[:2]) * 3600 + int(s[2:]) * 60) * NS
        starts.append(t)
    starts = np.array(starts, dtype=np.int64)
    order = np.argsort(starts)
    for k, r in enumerate(lv.itertuples()):
        t = int(starts[k])
        e = str(r.E).strip() if isinstance(r.E, str) else ''
        if e == '9999':
            later = starts[starts > t]
            te = int(later.min()) if later.size else t
        elif e and e.isdigit():
            e = e.zfill(4)
            te = t - (t % (86400 * NS)) + (int(e[:2]) * 3600 + int(e[2:]) * 60) * NS
            if te < t:
                te += 86400 * NS
        else:
            te = t
        rows.append((t, te, 'levent %s-%s %s T2=%s N2=%s' % (r.Y, r.JD, r.S, r.T2, r.N2)))
    p = os.path.join(catdir, 'gagnepian_2006_catalog.csv')
    for r in pd.read_csv(p, dtype=str).itertuples():
        try:
            t = _ymdhm(r.Date)
        except ValueError:
            UNPARSED.append('gagnepian_2006 %s %s' % (r.Type, r.Date)); continue
        rows.append((t, t, 'gagnepian_2006 %s' % r.Type))
    p = os.path.join(catdir, 'lognonne_2003_catalog.csv')
    for r in pd.read_csv(p, dtype=str).itertuples():
        try:
            t = _ymdhm(r.Date) + int(float(r.Seconds or 0) * NS)
        except ValueError:
            UNPARSED.append('lognonne_2003 %s %s' % (r.Type, r.Date)); continue
        rows.append((t, t, 'lognonne_2003 %s' % r.Type))
    p = os.path.join(catdir, 'nakamura_1979_sm_locations.csv')
    for r in pd.read_csv(p, dtype=str).itertuples():
        t = day_start_ns(int(r.Year), int(r.Day)) + (int(r.H) * 3600 + int(r.M) * 60 + int(float(r.S))) * NS
        rows.append((t, t, 'nakamura_1979_sm'))
    p = os.path.join(catdir, 'nakamura_1983_ai_locations.csv')
    for r in pd.read_csv(p, dtype=str).itertuples():
        t = day_start_ns(1900 + int(r.Y), int(r.JD)) + (int(r.Hour) * 3600 + int(r.Min) * 60) * NS + int(float(r.Sec) * NS)
        rows.append((t, t, 'nakamura_1983_ai %s' % r.AI))
    for f in ('nakamura_1983_m_arrivals.csv', 'nakamura_1983_sm_arrivals.csv'):
        p = os.path.join(catdir, f)
        for r in pd.read_csv(p, dtype=str).itertuples():
            if not isinstance(r.Year, str) or not r.Year.strip():
                continue
            h = str(r.Hour).strip().zfill(4)
            t = day_start_ns(int(r.Year), int(r.Day)) + (int(h[:2]) * 3600 + int(h[2:]) * 60) * NS
            rows.append((t, t, f.replace('.csv', '')))
    return rows


def matches(rows, t_ns):
    out = []
    for (a, b, lab) in rows:
        if abs(a - t_ns) <= MIN5 or (a <= t_ns <= b) or abs(b - t_ns) <= MIN5 and b != a:
            out.append(lab)
    return out
