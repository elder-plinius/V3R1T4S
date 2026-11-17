"""Claim run a100_1030, PREREG "S12 (third station)" (reported, not gated).

The frozen S12 + S14 A100 stack of lens lagtol-25nests-1973 (PREREG.v14), its statistic: S12 mean NCC over valid
S12 channels (>= 2 of MH1/MH2/MHZ), S14 mean over valid S14 channels (>= 1), each station's running maximum over
+/- 7 samples, Dt = min. Maximum within +/- 10 min of that lens's window start for the event; per-channel NCC at each
station's best lag. Run for 1973-10-30 (window start 02:26:50.264, that lens's peak) and, as a reproduction check of
that lens, for 1973-11-26 (window start 07:47:30.415). Waveforms: APOLLO_WF (the folder that lens read).

usage: s12_third_1030.py TOOLS_DIR NETS_S12S14.npz OUT.json LENS_CANDIDATES_STDOUT.txt
"""
import sys, json
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from scipy.ndimage import maximum_filter1d
from apollo_lib import NS, day_start_ns
from evlib import FS
from scan import prep_day, corr_channels

z = np.load(sys.argv[2]); nests = [str(n) for n in z['nests']]
tm = z['tm'][nests.index('100')]; chans = [tuple(c.split('.')) for c in z['chans']]
assert [c[0] for c in chans] == ['s12', 's12', 's12', 's14', 's14'], chans
M = tm.shape[1]; band = tuple(float(b) for b in z['band'])
import re
NULL = [float(m.group(1)) for m in (re.match(r'A100: null C0 [\d.]+, best shift [\d.]+, best control ([\d.]+)', l) for l in open(sys.argv[4])) if m][0]
print('S12 + S14 lens A100 null (best control, from its stdout):', NULL)


def runmax(x):
    y = np.where(np.isnan(x), -np.inf, x)
    m = maximum_filter1d(y, size=15, mode='nearest')
    return np.where(np.isinf(m), np.nan, m)


def smean(c, need):
    v = np.sum(~np.isnan(c), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        d = np.nansum(np.nan_to_num(c, nan=0.0), axis=0) / np.maximum(v, 1)
    return np.where(v >= need, d, np.nan)


res = {}
for lab, doy, ws in (('candidate_1973-10-30', 303, '1973-10-30T02:26:50.264'), ('first_claim_1973-11-26', 330, '1973-11-26T07:47:30.415')):
    pp = prep_day(1973, doy, chans, band, M)
    _, ccs, _ = corr_channels(pp, list(tm), min_comps=1)
    d12, d14 = smean(ccs[[0, 1, 2]], 2), smean(ccs[[3, 4]], 1)
    Dt = np.minimum(runmax(d12), runmax(d14))
    WS = int(np.datetime64(ws, 'ns').astype(np.int64))
    i_ws = int(round((WS - day_start_ns(1973, doy)) / NS * FS))
    K = int(round(600 * FS))
    seg = Dt[i_ws - K:i_ws + K + 1]; top = np.flatnonzero(seg >= np.nanmax(seg) - 1e-6)
    k = i_ws - K + int(top[len(top) // 2])  # middle of the plateau of the maximum (v2; v1 took its first index)
    j12 = k - 7 + int(np.nanargmax(d12[k - 7:k + 8])); j14 = k - 7 + int(np.nanargmax(d14[k - 7:k + 8]))
    r = dict(Dt=round(float(Dt[k]), 4), window_start=str(np.datetime64(day_start_ns(1973, doy) + int(round(k / FS * 1e9)), 'ns'))[:23] + 'Z',
             s12_lag_s=round((j12 - k) / FS, 3), s14_lag_s=round((j14 - k) / FS, 3),
             s12_ccs=[round(float(c), 4) for c in ccs[[0, 1, 2], j12]], s14_ccs=[round(float(c), 4) for c in ccs[[3, 4], j14]],
             s12_mean=round(float(d12[j12]), 4), s14_mean=round(float(d14[j14]), 4),
             lens_null_best_control=NULL, above_lens_null=bool(Dt[k] > NULL))
    res[lab] = r
    print(lab, json.dumps(r), flush=True)
json.dump(res, open(sys.argv[3], 'w'), indent=1)
