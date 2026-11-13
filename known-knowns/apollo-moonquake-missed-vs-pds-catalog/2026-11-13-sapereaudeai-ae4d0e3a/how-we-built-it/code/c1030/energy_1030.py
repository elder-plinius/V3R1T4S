"""Claim run a100_1030 (descriptive, written AFTER the PREREG freeze; gates nothing): how far above the noise is the
candidate on each channel? A3's energy ratio R = E_sig / E_noise (frozen preprocessing; E_sig = mean y^2 over
[t0 - 60 s, t0 + 600 s]; E_noise = median of the 60 s sub-window means over [t0 - 25 min, t0 - 5 min]) for S14 and S16
MH1/MH2 at the candidate onset, its percentile among 400 random onsets on the same day (seed 20261113, >= 30 min from
the candidate), and the raw counts in the template window (std, MAD, fraction of samples equal to the median).
Same for the first claimed event (1973-11-26) for comparison.

usage: energy_1030.py TOOLS_DIR
"""
import sys
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from apollo_lib import load_span, load_day, preprocess, NS, RATE, day_start_ns
from evlib import FS

BAND = (0.25, 1.0, 0.1)


def R(y, v, i0):
    a = i0 - int(60 * FS); b = i0 + int(600 * FS); n0 = i0 - int(25 * 60 * FS); n1 = i0 - int(5 * 60 * FS)
    if n0 < 0 or b > len(y) or v[a:b].mean() < 0.99 or v[n0:n1].mean() < 0.99:
        return None
    w = int(60 * FS)
    en = np.median([np.mean(y[k:k + w] ** 2) for k in range(n0, n1 - w + 1, w)])
    return float(np.mean(y[a:b] ** 2) / en) if en > 0 else None


rng = np.random.default_rng(20261113)
for lab, doy, onset, lags in (('candidate 1973-10-30', 303, '1973-10-30T02:25:51.509', {'s14': -1.509, 's16': -0.906}),
                              ('first claim 1973-11-26', 330, '1973-11-26T07:46:28.641', {'s14': 1.509, 's16': 2.113})):
    t0 = int(np.datetime64(onset, 'ns').astype(np.int64)); d0 = day_start_ns(1973, doy)
    ic = int(round((t0 - d0) / NS * FS))
    rnd = []
    while len(rnd) < 400:
        k = int(rng.integers(int(30 * 60 * FS), int(86400 * FS) - int(700 * FS)))
        if abs(k - ic) > int(1800 * FS):
            rnd.append(k)
    print(lab)
    for sta in ('s14', 's16'):
        for ch in ('mh1', 'mh2'):
            sp = load_span(sta, ch, 1973, doy, int(7200 * RATE))
            y, v = preprocess(sp[0], sp[1], BAND, dec=2)
            rc = R(y, v, ic)
            rr = np.array([x for x in (R(y, v, k) for k in rnd) if x is not None])
            x, vv, _ = load_day(sta, ch, 1973, doy)
            w0 = int(round((t0 - 30 * NS + int(lags[sta] * NS) - d0) / NS * RATE)); seg = x[w0:w0 + int(450 * RATE)][vv[w0:w0 + int(450 * RATE)]].astype(float)
            n0 = w0 - int(1500 * RATE); nseg = x[n0:n0 + int(1200 * RATE)][vv[n0:n0 + int(1200 * RATE)]].astype(float)
            med = np.median(seg); mad = np.median(np.abs(seg - med))
            print('  %s %s: R %.3f, percentile among %d random onsets of the day %.1f (random median %.3f); raw window std %.3f DU, MAD %.1f, frac at median %.3f; raw 20-min noise std %.3f DU' % (
                sta.upper(), ch.upper(), rc if rc is not None else float('nan'), len(rr), 100 * np.mean(rr < rc) if rc is not None else float('nan'),
                np.median(rr), seg.std(), mad, np.mean(seg == med), nseg.std()))
