"""Full-day network template scan.

scan_day(year, doy, chans, tmpls, band, modes) -> dict mode -> result
modes: 'fwd' (real data), 'rev' (each channel's day span reversed in time; bank null), 'shiftNNNN' (channels of the
second station circularly shifted by NNNN seconds within the day span; bank null), ('pr', k, tmpls_k) phase-randomised
templates on forward data.
Each result: dict(D=array of the statistic per window start (decimated samples from 00:00 of the day), ccs=per-channel
NCC array) - only for 'fwd' and 'rev' the full arrays are kept; for controls only the max is kept.
"""
import numpy as np
from scipy import fft as sfft
from apollo_lib import load_span, preprocess, window_norms, RATE, DAY_SAMPLES
from evlib import DEC, FS

NDAY = DAY_SAMPLES // DEC  # 286200 window starts per day


def prep_day(year, doy, chans, band, M):
    """Per channel: (y, valid) of length NDAY + M (day plus head of next day), or None."""
    out = []
    extra = (M + 10) * DEC
    for sta, ch in chans:
        r = load_span(sta, ch, year, doy, extra)
        if r is None:
            out.append(None); continue
        x, v, disc = r
        y, vd = preprocess(x, v, band, dec=DEC)
        n = NDAY + M - 1
        if len(y) < n:
            y = np.concatenate([y, np.zeros(n - len(y))]); vd = np.concatenate([vd, np.zeros(n - len(vd), bool)])
        out.append((y[:n], vd[:n], disc))
    return out


def corr_channels(prepped, tmpls, min_valid=0.9, min_comps=2, xf_cache=None):
    """Return (D, ccs) for window starts 0..NDAY-1. tmpls aligned with prepped (None = skip channel)."""
    M = len(next(t for t in tmpls if t is not None))
    ccs = np.full((len(prepped), NDAY), np.nan, dtype=np.float32)
    for i, (p, t) in enumerate(zip(prepped, tmpls)):
        if p is None or t is None:
            continue
        y, v = p[0], p[1]
        nf = sfft.next_fast_len(len(y) + M)
        key = (i, nf)
        if xf_cache is not None and key in xf_cache:
            Xf, nrm, frac = xf_cache[key]
        else:
            Xf = sfft.rfft(y, nf, workers=4)
            nrm, frac = window_norms(y, v, M)
            if xf_cache is not None:
                xf_cache[key] = (Xf, nrm, frac)
        Tf = sfft.rfft(t[::-1], nf, workers=4)
        raw = sfft.irfft(Xf * Tf, nf, workers=4)[M - 1:M - 1 + NDAY]
        c = raw / nrm[:NDAY]
        c[frac[:NDAY] < min_valid] = np.nan
        ccs[i] = c
    nvalid = np.sum(~np.isnan(ccs), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        D = np.nansum(np.nan_to_num(ccs, nan=0.0), axis=0) / np.maximum(nvalid, 1)
    D = D.astype(np.float32)
    D[nvalid < min_comps] = np.nan
    return D, ccs, nvalid


def reverse_prepped(prepped):
    return [None if p is None else (p[0][::-1].copy(), p[1][::-1].copy(), []) for p in prepped]


def shift_prepped(prepped, chans, station, shift_s):
    k = int(round(shift_s * FS))
    out = []
    for p, (sta, ch) in zip(prepped, chans):
        if p is None or sta != station:
            out.append(p); continue
        out.append((np.roll(p[0], k), np.roll(p[1], k), []))
    return out


def phase_randomise(tmpls, seed):
    """Same random phase per frequency applied to every channel's template spectrum; amplitudes kept."""
    M = len(next(t for t in tmpls if t is not None))
    rng = np.random.default_rng(seed)
    nfreq = M // 2 + 1
    ph = rng.uniform(0, 2 * np.pi, nfreq)
    ph[0] = 0.0
    if M % 2 == 0:
        ph[-1] = 0.0
    out = []
    for t in tmpls:
        if t is None:
            out.append(None); continue
        F = np.fft.rfft(t)
        r = np.fft.irfft(np.abs(F) * np.exp(1j * (np.angle(F) + ph)), M)
        r = r - r.mean(); r /= np.sqrt((r * r).sum())
        out.append(r)
    return out
