"""Fast, exact re-implementation of score_scan.py's null (C0 time-reversed data; C1..CN phase-randomised templates)
for one template set, with overlap-save block correlation and precomputed control-template spectra. Output: one
JSON line per day with rev_max and ctrl_max (same definitions as score_scan.py), resumable.

usage: fast_null.py TEMPLATES.npz YEAR DOY_FROM DOY_TO OUT.jsonl N_CONTROLS SEED_BASE
"""
import sys, os, json, time
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from scipy import fft as sfft
from apollo_lib import window_norms
from scan import prep_day, corr_channels, reverse_prepped, phase_randomise, NDAY

z = np.load(sys.argv[1])
year, d0, d1, out, NC, SEED = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
tm = list(z['tm']); chans = [tuple(c.split('.')) for c in z['chans']]
band = tuple(float(b) for b in z['band'])
if len(band) > 2 and band[2] == 0:
    band = band[:2]
M = tm[0].size
controls = [phase_randomise(tm, SEED + k) for k in range(1, NC + 1)]
NB = 8192
STEP = NB - M + 1
nblk = int(np.ceil(NDAY / STEP))
# control template spectra (reversed templates), complex64, shape (NC, nch, NB//2+1)
TF = np.array([[sfft.rfft(t[::-1], NB) for t in ctl] for ctl in controls]).astype(np.complex64)
done = set()
if os.path.isfile(out):
    done = {json.loads(l)['doy'] for l in open(out)}
fo = open(out, 'a')
for doy in range(d0, d1 + 1):
    if doy in done:
        continue
    T = time.time()
    pp = prep_day(year, doy, chans, band, M)
    rec = dict(year=year, doy=doy)
    if sum(p is not None for p in pp) < 2:
        rec['scanned'] = 0.0; fo.write(json.dumps(rec) + '\n'); fo.flush(); continue
    # C0 exactly as score_scan.py
    Dr, _, _ = corr_channels(reverse_prepped(pp), tm)
    rec['rev_max'] = float(np.nanmax(Dr)) if np.any(~np.isnan(Dr)) else None
    # per channel: normalisation and validity (as corr_channels), data block spectra
    norm, okc, XB = [], [], []
    for p in pp:
        if p is None:
            norm.append(None); okc.append(None); XB.append(None); continue
        y, v = p[0], p[1]
        nrm, frac = window_norms(y, v, M)
        norm.append(nrm[:NDAY]); okc.append(frac[:NDAY] >= 0.9)
        L = nblk * STEP + M - 1
        yy = np.zeros(L); yy[:len(y)] = y[:L]
        blocks = np.lib.stride_tricks.sliding_window_view(yy, NB)[::STEP][:nblk]
        XB.append(sfft.rfft(blocks, axis=1).astype(np.complex64))
    ch_ok = [k for k in range(len(pp)) if pp[k] is not None]
    valid_n = np.sum([okc[k] for k in ch_ok], axis=0)
    good = valid_n >= 2
    inv = {k: np.where(okc[k], 1.0 / norm[k], 0.0).astype(np.float32) for k in ch_ok}
    wgt = np.where(good, 1.0 / np.maximum(valid_n, 1), np.nan).astype(np.float32)
    cm = []
    for kc in range(NC):
        acc = np.zeros(NDAY, np.float32)
        for k in ch_ok:
            r = sfft.irfft(XB[k] * TF[kc, k][None, :], NB, axis=1)[:, M - 1:M - 1 + STEP].reshape(-1)[:NDAY]
            acc += r * inv[k]
        D = acc * wgt
        cm.append(round(float(np.nanmax(D)), 5) if good.any() else None)
    rec['ctrl_max'] = cm
    rec['seconds'] = round(time.time() - T, 1)
    fo.write(json.dumps(rec) + '\n'); fo.flush()
    print(year, doy, 'rev %.3f ctrl %.3f %.1fs' % (rec['rev_max'] or -1, max(c for c in cm if c is not None), rec['seconds']), flush=True)
fo.close()
