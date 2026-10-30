"""Shared tsunami-detector library (frozen with PREREG.md).

Data: IOC SLSMF API v1 (service.php, keyless), USGS ComCat, NCEI HazEL, ETOPO1 (ERDDAP / THREDDS).
Every fetch writes the raw bytes as fetched under RAW_DIR so a skeptic can re-check.
"""
import datetime as dt
import gzip
import hashlib
import json
import math
import os
import time
import urllib.parse
import urllib.request

import numpy as np
from scipy import signal
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

UA = {"User-Agent": "V3R1T4S-research-agent (python urllib; non-commercial research)"}
RAW_DIR = os.environ.get("RAW_DIR", os.path.join(os.environ.get("JOB_OUT", "."), "raw"))
G = 9.81
R_EARTH = 6371.0088e3
PAUSE = float(os.environ.get("FETCH_PAUSE", "0.7"))

# ---------- fetching ----------

def _cache_name(url):
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def fetch(url, tag="", timeout=120, cache=True):
    """One honest GET. Raw bytes saved gzip-compressed with the URL; no retry on 4xx/5xx."""
    os.makedirs(RAW_DIR, exist_ok=True)
    fn = os.path.join(RAW_DIR, (tag + "_" if tag else "") + _cache_name(url) + ".gz")
    if cache and os.path.exists(fn):
        with gzip.open(fn, "rb") as f:
            return f.read()
    time.sleep(PAUSE)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        status = r.status
        body = r.read()
    with gzip.open(fn, "wb") as f:
        f.write(body)
    with open(os.path.join(RAW_DIR, "FETCHLOG.tsv"), "a") as f:
        f.write("%s\t%s\t%d\t%d\t%s\t%s\n" % (
            dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), url, status, len(body),
            hashlib.sha256(body).hexdigest(), os.path.basename(fn)))
    return body


def ioc_stationlist():
    b = fetch("https://www.ioc-sealevelmonitoring.org/service.php?query=stationlist&showall=all", "stationlist")
    return json.loads(b)


def ioc_data(code, start, stop):
    """start/stop datetime (UTC). Max 30 days per call."""
    q = urllib.parse.urlencode({"query": "data", "code": code, "timestart": start.strftime("%Y-%m-%dT%H:%M"),
                                "timestop": stop.strftime("%Y-%m-%dT%H:%M"), "format": "json"})
    b = fetch("https://www.ioc-sealevelmonitoring.org/service.php?" + q, "ioc_" + code)
    try:
        return json.loads(b)
    except Exception:
        return []


def ioc_data_long(code, start, stop):
    out, s = [], start
    while s < stop:
        e = min(stop, s + dt.timedelta(days=29))
        out += ioc_data(code, s, e)
        s = e
    return out


# ---------- geometry ----------

def gc_dist(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(np.asarray(lon2) - lon1)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R_EARTH * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


# ---------- series handling (frozen rules, see PREREG.md) ----------

def parse_series(rows):
    """rows: IOC json list. Returns {sensor: (t_seconds array, level array)} with -999/None dropped."""
    by = {}
    for r in rows:
        try:
            v = float(r["slevel"])
        except (TypeError, ValueError, KeyError):
            continue
        if v <= -999 or not math.isfinite(v):
            continue
        t = dt.datetime.strptime(r["stime"].strip()[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
        by.setdefault(r.get("sensor", "?"), []).append((t.timestamp(), v))
    out = {}
    for s, lst in by.items():
        lst.sort()
        a = np.array(lst)
        _, idx = np.unique(a[:, 0], return_index=True)
        a = a[idx]
        out[s] = (a[:, 0], a[:, 1])
    return out


def pick_sensor(series, t_lo, t_hi):
    """Sensor with native median interval <= 60 s and most samples inside [t_lo, t_hi]."""
    best = None
    for s, (t, v) in series.items():
        m = (t >= t_lo) & (t <= t_hi)
        if m.sum() < 10:
            continue
        d = np.median(np.diff(t[m]))
        if d > 61:
            continue
        if best is None or m.sum() > best[1]:
            best = (s, m.sum(), d)
    return best


def max_level_run(v):
    """Longest run of identical consecutive raw values."""
    if len(v) == 0:
        return 0
    ch = np.flatnonzero(np.diff(v) != 0)
    edges = np.concatenate(([-1], ch, [len(v) - 1]))
    return int(np.max(np.diff(edges)))


def to_minute_grid(t, v, t_lo, t_hi):
    """Average native samples into 1-min bins on [t_lo, t_hi). Returns grid times and values (NaN = missing)."""
    n = int(round((t_hi - t_lo) / 60))
    tg = t_lo + 60 * np.arange(n)
    m = (t >= t_lo) & (t < t_hi)
    k = ((t[m] - t_lo) // 60).astype(int)
    s = np.bincount(k, weights=v[m], minlength=n)[:n]
    c = np.bincount(k, minlength=n)[:n]
    with np.errstate(invalid="ignore", divide="ignore"):
        g = np.where(c > 0, s / np.maximum(c, 1), np.nan)
    return tg, g


def despike(x):
    """Frozen: residual from 7-min running median; spike if |r| > max(10*robust sigma, 0.05 m)."""
    y = x.copy()
    ok = np.isfinite(y)
    if ok.sum() < 20:
        return y, 0
    yi = np.interp(np.arange(len(y)), np.flatnonzero(ok), y[ok])
    med = signal.medfilt(yi, 7)
    r = yi - med
    sig = 1.4826 * np.median(np.abs(r[ok]))
    bad = ok & (np.abs(r) > max(10 * sig, 0.05))
    y[bad] = np.nan
    return y, int(bad.sum())


TIDE_PERIODS_H = [12.4206012, 12.0, 12.65834751, 11.96723606, 23.93447213, 25.81933871, 24.06588766,
                  26.868350, 6.210300601, 6.103339, 4.140200401, 3.105150301]


def detide_bandpass(tg, x):
    """Frozen: least-squares harmonic tide (12 constituents + mean + linear trend) over the whole window,
    then zero-phase 4th-order Butterworth high-pass at 120 min (1-min data: the 2-120 min band of the
    criterion; periods < 2 min are not representable at 1-min sampling).  Gaps <= 10 min interpolated."""
    ok = np.isfinite(x)
    tt = (tg - tg[0]) / 3600.0
    cols = [np.ones_like(tt), tt / max(tt[-1], 1)]
    for P in TIDE_PERIODS_H:
        w = 2 * np.pi / P
        cols += [np.cos(w * tt), np.sin(w * tt)]
    A = np.vstack(cols).T
    coef, *_ = np.linalg.lstsq(A[ok], x[ok], rcond=None)
    res = x - A @ coef
    resi = np.interp(np.arange(len(res)), np.flatnonzero(ok), res[ok])
    sos = signal.butter(4, 1.0 / 120.0, btype="highpass", fs=1.0, output="sos")
    bp = signal.sosfiltfilt(sos, resi)
    return res, bp


def gap_mask(x, max_gap=10):
    """True where a sample sits inside a gap longer than max_gap minutes."""
    bad = ~np.isfinite(x)
    out = np.zeros_like(bad)
    i = 0
    n = len(x)
    while i < n:
        if bad[i]:
            j = i
            while j < n and bad[j]:
                j += 1
            if j - i > max_gap:
                out[i:j] = True
            i = j
        else:
            i += 1
    return out


def prepare_gauge(rows, t0, pre_h=36, post_h=12):
    """Build the band-passed 1-min series on [t0-pre_h, t0+post_h]. Returns dict or None with a reason."""
    series = parse_series(rows)
    t_lo, t_hi = t0 - pre_h * 3600, t0 + post_h * 3600
    ps = pick_sensor(series, t0 - 24 * 3600, t0 + 4 * 3600)
    if ps is None:
        return {"ok": False, "why": "no sensor <=60s with data"}
    sensor = ps[0]
    t, v = series[sensor]
    m = (t >= t0 - 24 * 3600) & (t <= t0 + 4 * 3600)
    run = max_level_run(v[m])
    native_dt = float(ps[2])
    run_minutes = run * native_dt / 60.0
    tg, x = to_minute_grid(t, v, t_lo, t_hi)
    x, nspk = despike(x)
    core = (tg >= t0 - 24 * 3600) & (tg < t0 + 4 * 3600)
    miss = float(np.mean(~np.isfinite(x[core])))
    long_gap = bool(gap_mask(x)[core].any())
    info = {"ok": True, "sensor": sensor, "native_dt": native_dt, "level_run_min": run_minutes,
            "missing_frac": miss, "long_gap": long_gap, "spikes": nspk}
    if run_minutes >= 30:
        info.update(ok=False, why="level run >= 30 min")
    elif miss > 0.10:
        info.update(ok=False, why="missing > 10%")
    elif long_gap:
        info.update(ok=False, why="gap > 10 min in core window")
    if not info["ok"]:
        return info
    res, bp = detide_bandpass(tg, x)
    info.update(tg=tg, bp=bp, res=res)
    return info


def score(tg, bp, t0, eta_s=None, win=(0, 4 * 3600)):
    """Frozen statistic.
    RMS24 = rms of bp on [t0-24h, t0).
    With eta_s (travel time, s): onset = first minute in [t0+eta-30min, t0+eta+60min] (not before t0) with
    |bp| >= 3*RMS24; peak = max |bp| on [onset, onset+180 min]; R = peak/RMS24; dt_arr = onset-(t0+eta).
    Without eta_s (stage-1 screen): R = max|bp| on [t0+win0, t0+win1] / RMS24."""
    pre = (tg >= t0 - 24 * 3600) & (tg < t0)
    rms = float(np.sqrt(np.mean(bp[pre] ** 2)))
    if eta_s is None:
        w = (tg >= t0 + win[0]) & (tg <= t0 + win[1])
        pk = float(np.max(np.abs(bp[w])))
        it = int(np.argmax(np.abs(bp[w])))
        return {"rms24": rms, "peak": pk, "R": pk / rms, "t_peak": float(tg[w][it] - t0)}
    lo = max(t0, t0 + eta_s - 1800)
    hi = t0 + eta_s + 3600
    w = (tg >= lo) & (tg <= hi) & (np.abs(bp) >= 3 * rms)
    if not w.any():
        return {"rms24": rms, "onset": None, "R": 0.0, "peak": 0.0, "dt_arr": None}
    onset = float(tg[np.flatnonzero(w)[0]])
    w2 = (tg >= onset) & (tg <= onset + 180 * 60)
    pk = float(np.max(np.abs(bp[w2])))
    return {"rms24": rms, "onset": onset - t0, "peak": pk, "R": pk / rms, "dt_arr": (onset - (t0 + eta_s)) / 60.0}


def detect(sc):
    """Frozen per-gauge detection: onset exists, |dt_arr| <= 10 min, R > 5."""
    return sc.get("onset") is not None and abs(sc["dt_arr"]) <= 10.0 and sc["R"] > 5.0


# ---------- bathymetry and travel times ----------

def etopo_box(lat0, lat1, lon0, lon1, stride=2):
    """ETOPO1 (1 arcmin) subset at `stride` arcmin via NCEI THREDDS OPeNDAP ascii (grid-registered gmt4)."""
    # ETOPO1_Ice_g_gmt4: x = -180..180 (21601), y = -90..90 (10801), 1 arcmin
    i0 = int(math.floor((lat0 + 90) * 60)); i1 = int(math.ceil((lat1 + 90) * 60))
    j0 = int(math.floor((lon0 + 180) * 60)); j1 = int(math.ceil((lon1 + 180) * 60))
    i0, i1 = max(0, i0), min(10800, i1)
    j0, j1 = max(0, j0), min(21600, j1)
    url = ("https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO1_Ice_g_gmt4.nc.ascii?z[%d:%d:%d][%d:%d:%d]"
           % (i0, stride, i1, j0, stride, j1))
    b = fetch(url, "etopo", timeout=300).decode()
    rows = []
    for line in b.splitlines():
        if line.startswith("[") and "]," in line:
            rows.append([float(v) for v in line.split("],", 1)[1].split(",")])
    z = np.array(rows)
    lats = -90 + np.arange(i0, i1 + 1, stride) / 60.0
    lons = -180 + np.arange(j0, j1 + 1, stride) / 60.0
    z = z[: len(lats), : len(lons)]
    return lats[: z.shape[0]], lons[: z.shape[1]], z


OFFS = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if (a, b) != (0, 0) and math.gcd(abs(a), abs(b)) == 1]


def travel_time_grid(lats, lons, z, src_ij, hmin=10.0):
    """First-arrival times (s) from src cell; water = z < 0; speed sqrt(g*max(depth,hmin)).
    Graph on the lat/lon grid with the 32 coprime offsets |di|,|dj|<=3, edge length = great-circle distance
    between cell centres, cost = length * mean slowness over 5 points sampled along the edge; an edge is
    usable only if every sampled cell is water."""
    ny, nx = z.shape
    water = z < 0
    slow = np.where(water, 1.0 / np.sqrt(G * np.maximum(-z, hmin)), np.inf)
    idx = np.arange(ny * nx).reshape(ny, nx)
    LAT, LON = np.meshgrid(lats, lons, indexing="ij")
    rows_, cols_, w_ = [], [], []
    for di, dj in OFFS:
        i_a = slice(max(0, -di), ny - max(0, di)); i_b = slice(max(0, di), ny - max(0, -di))
        j_a = slice(max(0, -dj), nx - max(0, dj)); j_b = slice(max(0, dj), nx - max(0, -dj))
        ia, ja = np.meshgrid(np.arange(ny)[i_a], np.arange(nx)[j_a], indexing="ij")
        ssum = np.zeros(ia.shape)
        okm = np.ones(ia.shape, bool)
        for f in (0, 0.25, 0.5, 0.75, 1.0):
            ii = np.rint(ia + f * di).astype(int); jj = np.rint(ja + f * dj).astype(int)
            s = slow[ii, jj]
            okm &= np.isfinite(s)
            ssum += np.where(np.isfinite(s), s, 0)
        L = gc_dist(LAT[i_a, j_a], LON[i_a, j_a], LAT[i_b, j_b], LON[i_b, j_b])
        cost = L * ssum / 5.0
        rows_.append(idx[i_a, j_a][okm]); cols_.append(idx[i_b, j_b][okm]); w_.append(cost[okm])
    M = csr_matrix((np.concatenate(w_), (np.concatenate(rows_), np.concatenate(cols_))), shape=(ny * nx, ny * nx))
    d = dijkstra(M, directed=True, indices=idx[src_ij])
    return d.reshape(ny, nx)


def snap(lats, lons, z, lat, lon, min_depth, max_km):
    """Nearest cell with depth >= min_depth within max_km, or None."""
    LAT, LON = np.meshgrid(lats, lons, indexing="ij")
    d = gc_dist(lat, lon, LAT, LON)
    cand = (z <= -min_depth) & (d <= max_km * 1000)
    if not cand.any():
        return None
    k = np.argmin(np.where(cand, d, np.inf))
    return np.unravel_index(k, z.shape)


def flat_ocean_check():
    """Solver error on a flat 4000 m ocean (lat/lon grid at 2 arcmin, equator and 45N) against analytic."""
    out = []
    for latc in (0.0, 45.0):
        lats = latc + np.arange(-120, 121) / 30.0
        lons = np.arange(-120, 121) / 30.0
        z = -4000.0 * np.ones((len(lats), len(lons)))
        T = travel_time_grid(lats, lons, z, (120, 120))
        LAT, LON = np.meshgrid(lats, lons, indexing="ij")
        D = gc_dist(latc, 0.0, LAT, LON)
        Ta = D / math.sqrt(G * 4000)
        m = D > 200e3
        rel = (T[m] - Ta[m]) / Ta[m]
        out.append((latc, float(rel.min()), float(rel.max())))
    return out


# ---------- catalogues ----------

def ncei_events(min_year):
    items, page = [], 1
    while True:
        b = fetch("https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events?minYear=%d&page=%d"
                  % (min_year, page), "ncei_events", cache=False)
        d = json.loads(b)
        items += d["items"]
        if page >= d.get("totalPages", 1):
            break
        page += 1
    return items


def ncei_event_time(e):
    y, mo, d = e.get("year"), e.get("month"), e.get("day")
    if not (y and mo and d):
        return None
    return dt.datetime(y, mo, d, e.get("hour") or 12, e.get("minute") or 0, tzinfo=dt.timezone.utc).timestamp()


def ncei_conflict(events, t0, lat, lon, days=1.0, km=3000.0):
    """Frozen conservative match: any NCEI event (any validity, any cause) with date within +/-`days`
    (by calendar date if the time is missing) and either within `km` or with no coordinates."""
    hits = []
    for e in events:
        y, mo, d = e.get("year"), e.get("month"), e.get("day")
        if not (y and mo and d):
            continue
        day = dt.datetime(y, mo, d, tzinfo=dt.timezone.utc).timestamp()
        if abs(day + 43200 - t0) > days * 86400 + 43200:
            continue
        if e.get("latitude") is None or e.get("longitude") is None:
            hits.append(e)
            continue
        if gc_dist(lat, lon, e["latitude"], e["longitude"]) <= km * 1000:
            hits.append(e)
    return hits


def comcat(start, end, minmag=6.0, maxdepth=70):
    url = ("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=%s&endtime=%s"
           "&minmagnitude=%.1f&maxdepth=%d&orderby=time-asc" % (start, end, minmag, maxdepth))
    return json.loads(fetch(url, "comcat", timeout=600))["features"]
