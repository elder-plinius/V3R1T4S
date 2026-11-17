"""Claim run a100_1030, PREREG D1 (reported, not gated): the other decimation phase.

The frozen pipeline keeps raw samples 0, 2, 4, ... after filtering (apollo_lib.preprocess: y[::2]). Here the same
preprocessing keeps raw samples 1, 3, 5, ... (y[1::2]); the A100 S14 + S16 stack is rebuilt on that grid with the
frozen builder logic (net25_build_1416.py, nest 100 only, 1973 events, same reference rule, same drop rule), and the
candidate is scored on that grid: frozen Dt (station means, +/- 7 samples per station, min), maximum over common lags
within +/- 10 s of the window start, per-channel NCC at each station's best lag. Control: the same code on the
frozen grid (phase 0) with a stack rebuilt the same way must give the frozen numbers. Reported for the first claimed
event (1973-11-26) as well, for information only.

usage: decphase_1030.py TOOLS_DIR LEVENT.csv FROZEN_A100.npz OUT.json
"""
import sys, json
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
import pandas as pd
from scipy import signal
from scipy import fft as sfft
from scipy.ndimage import maximum_filter1d
import apollo_lib, evlib, scan
from apollo_lib import NS, RATE, despike, day_start_ns
from evlib import FS, load_nest_events, DayCache, event_block
import nesttemplates2
from nesttemplates2 import build, _clean

LEV, FROZEN, OUT = sys.argv[2], sys.argv[3], sys.argv[4]
_orig = apollo_lib.preprocess


def make_pp(phase):
    def pp(x, valid, band, dec=2, pad_s=20.0, do_despike=True):
        # identical to apollo_lib.preprocess except for the decimation phase of the last line
        if do_despike:
            x, _ = despike(x, valid)
        x = x.astype(float).copy()
        if valid.any():
            x[valid] -= np.median(x[valid])
        x[~valid] = 0.0
        if len(band) > 2 and band[2]:
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
        return y[phase::dec].copy(), (~inv)[phase::dec].copy()
    return pp


def use_phase(phase):
    f = make_pp(phase)
    apollo_lib.preprocess = f; evlib.preprocess = f; scan.preprocess = f


band = (0.25, 1.0, 0.1); L = 450.0; M = int(round(L * FS))
chans = [('s14', 'mh1'), ('s14', 'mh2'), ('s16', 'mh1'), ('s16', 'mh2')]


def build_a100():
    cache = DayCache(band)
    ev = load_nest_events(LEV, '100', ['73'])
    amp = ev['A1n'].clip(lower=0).fillna(0) + ev['A2n'].clip(lower=0).fillna(0) + pd.to_numeric(ev['A4'], errors='coerce').clip(lower=0).fillna(0)
    clean = []
    for i, r in ev.iterrows():
        blk = event_block(cache, chans, int(r['t_ns']), M)
        clean.append(all(y is not None and v.mean() > 0.95 and _clean(y) for y, v in blk))
    ref = int(amp.where(clean, -1).idxmax())
    b = build(ev, chans, band, L, ref, cache=cache)
    g = [round(float(np.abs(t).max() / t.std()), 1) for t in b['tm']]
    members = [str(np.datetime64(int(ev.loc[i, 't_ns']), 'ns'))[:16] for i in b['members']]
    return np.array(b['tm']), dict(members=members, n_members=len(members), onset_rel_s=b['onset_rel_s'], glitchiness=g)


def runmax(x):
    y = np.where(np.isnan(x), -np.inf, x)
    m = maximum_filter1d(y, size=15, mode='nearest')
    return np.where(np.isinf(m), np.nan, m)


def smean(c):
    v = np.sum(~np.isnan(c), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        d = np.nansum(np.nan_to_num(c, nan=0.0), axis=0) / np.maximum(v, 1)
    return np.where(v >= 1, d, np.nan)


def score(tm, doy, ws_iso):
    pp = scan.prep_day(1973, doy, chans, band, M)
    _, ccs, _ = scan.corr_channels(pp, list(tm), min_comps=1)
    d14, d16 = smean(ccs[[0, 1]]), smean(ccs[[2, 3]])
    Dt = np.minimum(runmax(d14), runmax(d16))
    WS = int(np.datetime64(ws_iso, 'ns').astype(np.int64))
    i_ws = int(round((WS - day_start_ns(1973, doy)) / NS * FS))
    K = int(round(10 * FS))
    seg = Dt[i_ws - K:i_ws + K + 1]; top = np.flatnonzero(seg >= np.nanmax(seg) - 1e-6)
    k = i_ws - K + int(top[len(top) // 2])  # middle of the plateau of the maximum (v2; v1 took its first index)
    j14 = k - 7 + int(np.nanargmax(d14[k - 7:k + 8])); j16 = k - 7 + int(np.nanargmax(d16[k - 7:k + 8]))
    return dict(Dt=round(float(Dt[k]), 4), common_lag_offset_samples=k - i_ws,
                s14_lag_s=round((j14 - k) / FS, 3), s16_lag_s=round((j16 - k) / FS, 3),
                ccs=[round(float(c), 4) for c in list(ccs[[0, 1], j14]) + list(ccs[[2, 3], j16])],
                s14_best=round(float(np.nanmax(ccs[[0, 1], j14])), 4), s16_best=round(float(np.nanmax(ccs[[2, 3], j16])), 4),
                R7=bool(np.nanmax(ccs[[0, 1], j14]) >= 0.5 and np.nanmax(ccs[[2, 3], j16]) >= 0.5))


res = {}
z = np.load(FROZEN); tmF = z['tm'][0]
use_phase(0)
res['phase0_frozen_stack'] = dict(candidate=score(tmF, 303, '1973-10-30T02:25:21.509'), first_claim=score(tmF, 330, '1973-11-26T07:45:58.641'))
print('phase 0, frozen stack:', json.dumps(res['phase0_frozen_stack']), flush=True)
tm0, info0 = build_a100()
res['phase0_rebuilt'] = dict(stack=info0, identical_to_frozen=bool(np.allclose(tm0, tmF, atol=1e-9)),
                             max_abs_diff=float(np.abs(tm0 - tmF).max()))
print('phase 0 rebuilt stack identical to frozen:', res['phase0_rebuilt']['identical_to_frozen'], res['phase0_rebuilt']['max_abs_diff'], info0, flush=True)
use_phase(1)
tm1, info1 = build_a100()
res['phase1_rebuilt'] = dict(stack=info1, candidate=score(tm1, 303, '1973-10-30T02:25:21.509'),
                             first_claim=score(tm1, 330, '1973-11-26T07:45:58.641'))
print('phase 1 rebuilt stack:', info1, flush=True)
print('phase 1 candidate:', json.dumps(res['phase1_rebuilt']['candidate']), flush=True)
print('phase 1 first claimed event (reported only):', json.dumps(res['phase1_rebuilt']['first_claim']), flush=True)
use_phase(0)
json.dump(res, open(OUT, 'w'), indent=1)
