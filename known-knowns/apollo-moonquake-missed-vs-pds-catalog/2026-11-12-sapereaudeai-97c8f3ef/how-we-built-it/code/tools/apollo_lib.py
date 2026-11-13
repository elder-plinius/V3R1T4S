"""Shared helpers for this run: day loading on a uniform grid, preprocessing, normalised cross-correlation.

All times are integer nanoseconds since 1970-01-01 (UTC as recorded in the PDS MiniSEED, i.e. Earth-received time).
"""
import os
import datetime as dt
import numpy as np
from scipy import signal
from scipy import fft as sfft

from mseed_steim2 import read_mseed

RATE = 6.625
NS = 1_000_000_000
DAY_SAMPLES = int(round(86400 * RATE))  # 572400
CACHE = __import__('os').environ.get('APOLLO_WF', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'waveforms'))
PDS = 'https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/data/xa/continuous_waveform'
COMPS = ('mh1', 'mh2', 'mhz')


def day_start_ns(year, doy):
    t = dt.datetime(year, 1, 1) + dt.timedelta(days=doy - 1)
    d = t - dt.datetime(1970, 1, 1)
    return (d.days * 86400 + d.seconds) * NS


def fname(sta, ch, year, doy, loc='00'):
    return 'xa.%s.%s.%s.%d.%03d.0.mseed' % (sta, loc, ch, year, doy)


def url(sta, ch, year, doy, loc='00'):
    return '%s/%s/%d/%03d/%s' % (PDS, sta, year, doy, fname(sta, ch, year, doy, loc))


def load_day(sta, ch, year, doy, loc='00', cache=CACHE):
    """Return (x float64[DAY_SAMPLES], valid bool[DAY_SAMPLES], disc list of sample indices with timing
    discontinuities) or None if the file is absent. Samples placed by record start time on a grid from 00:00:00."""
    p = os.path.join(cache, sta, fname(sta, ch, year, doy, loc))
    if not os.path.isfile(p) or os.path.getsize(p) == 0:
        return None
    recs = read_mseed(p)
    t0 = day_start_ns(year, doy)
    x = np.zeros(DAY_SAMPLES)
    valid = np.zeros(DAY_SAMPLES, bool)
    disc = []
    prev_end = None
    for r in recs:
        d = r['data']
        if len(d) == 0:
            continue
        i0 = int(round((r['start'] - t0) / NS * RATE))
        if prev_end is not None:
            expect = prev_end
            if abs(i0 - expect) >= 1:
                disc.append(i0)
        prev_end = i0 + len(d)
        a, b = max(i0, 0), min(i0 + len(d), DAY_SAMPLES)
        if b <= a:
            continue
        seg = d[a - i0:b - i0]
        x[a:b] = seg
        valid[a:b] = seg != -1
    return x, valid, disc


def load_span(sta, ch, year, doy, extra_samples, loc='00'):
    """Day (year, doy) plus the first extra_samples of the next day. Returns (x, valid, disc) or None if day absent."""
    a = load_day(sta, ch, year, doy, loc)
    if a is None:
        return None
    nd = dt.date(year, 1, 1) + dt.timedelta(days=doy)  # next day (doy is 1-based)
    b = load_day(sta, ch, nd.year, nd.timetuple().tm_yday, loc)
    if b is None:
        bx = np.zeros(extra_samples); bv = np.zeros(extra_samples, bool); bd = []
    else:
        bx, bv, bd = b[0][:extra_samples], b[1][:extra_samples], [i + DAY_SAMPLES for i in b[2] if i < extra_samples]
    return (np.concatenate([a[0], bx]), np.concatenate([a[1], bv]), a[2] + bd)


def despike(x, valid, floor=3.0, nmad=5.0, k=7):
    """Hampel filter: samples with |x - med_k| > max(floor, nmad * 1.4826 * MAD_k) are replaced by med_k.
    Returns (x_clean, n_replaced)."""
    from scipy.ndimage import median_filter
    xf = x.astype(float).copy()
    if valid.any():
        xf[~valid] = np.median(xf[valid])
    med = median_filter(xf, size=k, mode='nearest')
    r = np.abs(xf - med)
    mad = median_filter(r, size=k, mode='nearest')
    bad = (r > np.maximum(floor, nmad * 1.4826 * mad)) & valid
    out = x.astype(float).copy()
    out[bad] = med[bad]
    return out, int(bad.sum())


def preprocess(x, valid, band, dec=2, pad_s=20.0, do_despike=True):
    """Despike (Hampel), demean (median of valid), zero invalid, zero-phase Butterworth band-pass (4 poles),
    re-zero invalid samples dilated by pad_s, decimate by dec. Returns (y, valid_dec)."""
    if do_despike:
        x, _ = despike(x, valid)
    x = x.astype(float).copy()
    if valid.any():
        x[valid] -= np.median(x[valid])
    x[~valid] = 0.0
    if len(band) > 2 and band[2]:
        # spectral whitening of the whole span: divide by the running mean (width band[2] Hz) of |X|
        from scipy.ndimage import uniform_filter1d
        X = sfft.rfft(x)
        df = RATE / len(x)
        w = max(3, int(float(band[2]) / df))
        A = uniform_filter1d(np.abs(X), w, mode='nearest')
        A[A <= 0] = 1.0
        x = sfft.irfft(X / A, len(x))
        x[~valid] = 0.0
        band = band[:2]
    sos = signal.butter(4, band, btype='bandpass', fs=RATE, output='sos')
    y = signal.sosfiltfilt(sos, x)
    pad = int(pad_s * RATE)
    inv = ~valid
    if inv.any():
        k = np.ones(2 * pad + 1)
        inv = np.convolve(inv.astype(float), k, mode='same') > 0
    y[inv] = 0.0
    return y[::dec].copy(), (~inv)[::dec].copy()


def ncc_fft(y, Xf, nfft, tmpl):
    """Raw correlation sum_j tmpl[j] * y[k+j] for k = 0..len(y)-len(tmpl), via precomputed rfft Xf of y."""
    M = len(tmpl)
    Tf = sfft.rfft(tmpl[::-1], nfft)
    c = sfft.irfft(Xf * Tf, nfft, workers=4)
    return c[M - 1:len(y)]


def window_norms(y, valid, M):
    """For each start k: sqrt(sum y^2 - (sum y)^2/M) over y[k:k+M], and valid fraction."""
    cs = np.concatenate([[0.0], np.cumsum(y)])
    cs2 = np.concatenate([[0.0], np.cumsum(y * y)])
    cv = np.concatenate([[0], np.cumsum(valid.astype(np.int64))])
    s = cs[M:] - cs[:-M]
    s2 = cs2[M:] - cs2[:-M]
    var = s2 - s * s / M
    var[var < 1e-12] = np.inf
    frac = (cv[M:] - cv[:-M]) / M
    return np.sqrt(var), frac


def norm_template(t):
    t = t - t.mean()
    n = np.sqrt((t * t).sum())
    return t / n if n > 0 else t


def station_ncc(ys, valids, tmpls, Xfs=None, nfft=None, min_valid=0.9, min_comps=2):
    """ys, valids: lists per component (same length). tmpls: list of unit-norm zero-mean templates (same length M).
    Returns (D, ccs) where ccs is (ncomp, L) array of single-channel NCC (nan where component invalid) and D the
    mean over valid components (nan where fewer than min_comps valid)."""
    M = len(tmpls[0])
    L = len(ys[0]) - M + 1
    ccs = np.full((len(ys), L), np.nan)
    for i, (y, v, t) in enumerate(zip(ys, valids, tmpls)):
        if y is None:
            continue
        if Xfs is None:
            nf = sfft.next_fast_len(len(y) + M)
            Xf = sfft.rfft(y, nf)
        else:
            Xf, nf = Xfs[i], nfft
        raw = ncc_fft(y, Xf, nf, t)
        nrm, frac = window_norms(y, v, M)
        c = raw / nrm
        c[frac < min_valid] = np.nan
        ccs[i] = c
    nvalid = np.sum(~np.isnan(ccs), axis=0)
    with np.errstate(invalid='ignore'):
        D = np.nanmean(np.where(np.isnan(ccs), np.nan, ccs), axis=0) if len(ys) else None
    D[nvalid < min_comps] = np.nan
    return D, ccs


def decluster(D, sep, thr):
    """Indices of local maxima of D >= thr, greedy by height, at least sep samples apart."""
    Dn = np.where(np.isnan(D), -np.inf, D)
    idx = np.flatnonzero(Dn >= thr)
    if idx.size == 0:
        return np.array([], int)
    # local maxima only
    order = idx[np.argsort(-Dn[idx])]
    taken = []
    blocked = np.zeros(len(D), bool)
    for i in order:
        if blocked[i]:
            continue
        taken.append(i)
        blocked[max(0, i - sep):i + sep + 1] = True
    return np.array(sorted(taken), int)


def ns_iso(t):
    return str(np.datetime64(int(t), 'ns'))[:23] + 'Z'


def cat_time_ns(Y, JD, S):
    y = 1900 + int(Y); d = int(JD); hhmm = str(S).strip().zfill(4)
    return day_start_ns(y, d) + (int(hhmm[:2]) * 3600 + int(hhmm[2:]) * 60) * NS
