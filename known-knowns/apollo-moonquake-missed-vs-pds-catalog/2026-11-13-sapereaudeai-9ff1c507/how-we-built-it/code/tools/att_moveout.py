"""PREREG.v5 R8: ATT-corrected inter-station arrival difference for a detection.

station_arrival(cache, tm, chans_of_station, t_window_start) -> best lag (s) within +/- 10 s (station-mean NCC)
true_time(sta, t_nominal_ns) -> Earth-received time (ns) from the station's ATT trace (frame-head timestamps, one per
    four LP samples): ATT value of the frame holding the sample, plus the sample's offset in the frame.
ATT files are read from wfcache/att/xa.<sta>..att.<year>.<doy>.0.mseed (fetched separately, one honest GET each).
"""
import os
import datetime as dt
import numpy as np
from mseed_steim2 import read_mseed
from evlib import event_block, FS
from apollo_lib import NS, RATE

ATT_DIR = __import__('os').environ.get('APOLLO_ATT', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'waveforms', 'att'))
_att = {}


def _load_att(sta, year, doy):
    k = (sta, year, doy)
    if k not in _att:
        p = os.path.join(ATT_DIR, 'xa.%s..att.%d.%03d.0.mseed' % (sta, year, doy))
        if not os.path.isfile(p):
            _att[k] = None
        else:
            recs = read_mseed(p)
            t_nom = np.concatenate([r['start'] + np.round(np.arange(len(r['data'])) / r['rate'] * 1e9).astype(np.int64) for r in recs])
            val = np.concatenate([r['data'] for r in recs])
            ok = val != -1.0
            _att[k] = (t_nom[ok], (val[ok] * 1e9).astype(np.int64))
    return _att[k]


def true_time(sta, t_ns):
    d = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t_ns // NS)
    a = _load_att(sta, d.year, d.timetuple().tm_yday)
    if a is None:
        return None
    t_nom, t_att = a
    j = int(np.searchsorted(t_nom, t_ns, side='right')) - 1
    if j < 0 or t_ns - t_nom[j] > 2 * NS:
        return None
    return int(t_att[j] + (t_ns - t_nom[j]))


def station_arrival(cache, tm_station, chans_station, t_ns, half_s=10.0):
    M = len(tm_station[0])
    k10 = int(half_s * FS)
    blk = event_block(cache, chans_station, t_ns - int(half_s * NS), M + 2 * k10 + 1)
    best = (None, -9.0)
    for s in range(0, 2 * k10 + 1):
        cs = []
        for (y, v), t in zip(blk, tm_station):
            if y is None:
                continue
            w = y[s:s + M]; w = w - w.mean(); n = np.sqrt((w * w).sum())
            if n > 0:
                cs.append(float((w * t).sum() / n))
        if cs and np.mean(cs) > best[1]:
            best = ((s - k10) / FS, float(np.mean(cs)))
    return best
