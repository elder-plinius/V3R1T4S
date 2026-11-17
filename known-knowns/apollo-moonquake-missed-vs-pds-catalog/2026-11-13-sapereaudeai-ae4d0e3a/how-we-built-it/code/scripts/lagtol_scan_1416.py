"""PREREG.v15 (S14 + S16 variant of the PREREG.v14 scan) lag-tolerant coincidence scan: Dt = min(runmax_{+/-2 s} D12, runmax_{+/-2 s} D14).
(derived from the fast variant: identical results; shared reversed-data FFTs, shared circular spectra and norms, rolls by slicing)
PREREG.v8 coincidence scan: several nests at once on S12 (MH1/MH2/MHZ) + S14 (MH1/MH2), statistic
Dc = min(mean S12 NCC, mean S14 NCC); forward, C0 time-reversed, C1..C400 S14 rolled by 3600 + 180 k s (exact, via
circular correlation). One JSON line per day; resumable; waits for files listed in the PDS inventory.

usage: coinc_scan.py NETS.npz YEAR DOY_FROM DOY_TO OUT.jsonl N_SHIFTS
NETS.npz: nests (k), tm (k x 5 x M), chans (5), band, L
"""
import sys, os, re, json, time
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from apollo_lib import NS, decluster, day_start_ns
from evlib import FS
from scan import prep_day, corr_channels, reverse_prepped, NDAY

z = np.load(sys.argv[1])
year, d0, d1, out, NSH = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
nests = [str(n) for n in z['nests']]; TM = z['tm']; chans = [tuple(c.split('.')) for c in z['chans']]
band = tuple(float(b) for b in z['band']); M = TM.shape[2]
i12 = [k for k, c in enumerate(chans) if c[0] == 's14']; i14 = [k for k, c in enumerate(chans) if c[0] == 's16']  # PREREG.v15: first S14, rolled S16
SEP = int(300 * FS)
CACHE = __import__('os').environ.get('APOLLO_WF', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'waveforms'))
INV = set(re.findall(r'(xa\.s1[0-9]\.00\.mh[12z]\.\d{4}\.\d{3})\.0', open(
    __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'data', 'pse', 'collection_data_seed_inventory.csv')).read()))


def station_means(ccs):
    v12 = np.sum(~np.isnan(ccs[i12]), axis=0); v14 = np.sum(~np.isnan(ccs[i14]), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        d12 = np.nansum(np.nan_to_num(ccs[i12], nan=0.0), axis=0) / np.maximum(v12, 1)
        d14 = np.nansum(np.nan_to_num(ccs[i14], nan=0.0), axis=0) / np.maximum(v14, 1)
    return np.where(v12 >= 1, d12, np.nan), np.where(v14 >= 1, d14, np.nan)


def coinc(ccs):
    v12 = np.sum(~np.isnan(ccs[i12]), axis=0); v14 = np.sum(~np.isnan(ccs[i14]), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        d12 = np.nansum(np.nan_to_num(ccs[i12], nan=0.0), axis=0) / np.maximum(v12, 1)
        d14 = np.nansum(np.nan_to_num(ccs[i14], nan=0.0), axis=0) / np.maximum(v14, 1)
    Dc = np.minimum(d12, d14).astype(np.float32)
    Dc[(v12 < 2) | (v14 < 1)] = np.nan
    return Dc


KLAG = int(round(2.0 * FS))


def runmax(x, wrap=False):
    from scipy.ndimage import maximum_filter1d
    y = np.where(np.isnan(x), -np.inf, x)
    m = maximum_filter1d(y, size=2 * KLAG + 1, mode='wrap' if wrap else 'nearest')
    return np.where(np.isinf(m), np.nan, m)


def circ_prep(y, v):
    """circular correlation through a linear correlation of the wrapped series (fast FFT length, data FFT shared)"""
    from scipy import fft as sfft
    from apollo_lib import window_norms
    N = len(y)
    ye = np.concatenate([y, y[:M - 1]]); ve = np.concatenate([v, v[:M - 1]])
    nf = sfft.next_fast_len(len(ye) + M)
    Xe = sfft.rfft(ye, nf)
    nrm, frac = window_norms(ye, ve, M)
    return Xe, nf, nrm, frac, N


def circ_ncc_fast(prep, t):
    from scipy import fft as sfft
    Xe, nf, nrm, frac, N = prep
    Tf = sfft.rfft(t[::-1], nf)
    raw = sfft.irfft(Xe * Tf, nf)[M - 1:M - 1 + N]
    c = raw / nrm; c[frac < 0.9] = np.nan
    return c


def roll_max_all(d12, d14c, shifts):
    """Exact max over m < NDAY of min(d12[m], roll(d14c, sh)[m]) for every shift: evaluate only the samples with
    d12 >= q (q = 99.5th percentile of d12); if the best value there is >= q it is the exact maximum (all other
    samples give min < q); otherwise fall back to the full computation for that shift."""
    N = len(d14c)
    d = d12[:NDAY]
    ok = ~np.isnan(d)
    if not ok.any():
        return [None] * len(shifts)
    q = float(np.percentile(d[ok], 99.5))
    H = np.flatnonzero(ok & (d >= q))
    dh = d[H]
    out = []
    for sh in shifts:
        x = np.minimum(dh, d14c[(H - sh) % N]).astype(np.float32)
        b = float(np.nanmax(x)) if np.any(~np.isnan(x)) else -np.inf
        if not (b >= q):
            b = roll_max(d12, d14c, sh)
        out.append(round(b, 5) if np.isfinite(b) else None)
    return out


def roll_max(d12, d14c, sh):
    """nanmax over m < NDAY of min(d12[m], roll(d14c, sh)[m]) without building the rolled array."""
    N = len(d14c); sh %= N
    best = -np.inf
    # roll(d14c, sh)[m] = d14c[m - sh] for m >= sh, d14c[N - sh + m] for m < sh
    a = min(sh, NDAY)
    if a > 0:
        x = np.minimum(d12[:a], d14c[N - sh:N - sh + a]).astype(np.float32)
        if np.any(~np.isnan(x)):
            best = max(best, float(np.nanmax(x)))
    if NDAY > sh:
        x = np.minimum(d12[sh:NDAY], d14c[:NDAY - sh]).astype(np.float32)
        if np.any(~np.isnan(x)):
            best = max(best, float(np.nanmax(x)))
    return best


done = set()
if os.path.isfile(out):
    done = {json.loads(l)['doy'] for l in open(out)}
fo = open(out, 'a')
last = 366 if year % 4 == 0 else 365
for doy in range(d0, d1 + 1):
    if doy in done:
        continue
    need = []
    for (sta, ch) in chans:
        for (yy, dd) in ((year, doy), (year + (doy == last), 1 if doy == last else doy + 1)):
            stem = 'xa.%s.00.%s.%d.%03d' % (sta, ch, yy, dd)
            if stem in INV and not os.path.isfile(os.path.join(CACHE, sta, stem + '.0.mseed')):
                need.append(stem)
    if need:
        continue
    T = time.time()
    rec = dict(year=year, doy=doy, nests={})
    pp = prep_day(year, doy, chans, band, M)
    t0 = day_start_ns(year, doy)
    xf = {}
    xfr = {}
    ppr = reverse_prepped(pp)
    cprep = {j: circ_prep(pp[j][0], pp[j][1]) for j in i14 if pp[j] is not None}
    for n, tm in zip(nests, TM):
        tm = list(tm)
        _, ccs, _ = corr_channels(pp, tm, min_comps=1, xf_cache=xf)
        d12r, d14r = station_means(ccs)
        D12m, D14m = runmax(d12r), runmax(d14r)
        Dc = np.minimum(D12m, D14m).astype(np.float32)
        ok = ~np.isnan(Dc)
        r = dict(scanned=float(ok.mean()))
        pk = decluster(Dc, SEP, 0.05)
        pl = []
        for i in pk:
            a, b = max(0, i - KLAG), min(NDAY, i + KLAG + 1)
            j12 = a + int(np.nanargmax(np.where(np.isnan(d12r[a:b]), -np.inf, d12r[a:b])))
            j14 = a + int(np.nanargmax(np.where(np.isnan(d14r[a:b]), -np.inf, d14r[a:b])))
            pl.append([int(t0 + round(i / FS * 1e9)), round(float(Dc[i]), 5),
                       [None if np.isnan(c) else round(float(c), 4) for c in ccs[i12, j12]] +
                       [None if np.isnan(c) else round(float(c), 4) for c in ccs[i14, j14]],
                       round((j12 - i) / FS, 3), round((j14 - i) / FS, 3)])
        r['fwd_peaks'] = pl
        _, ccr, _ = corr_channels(ppr, tm, min_comps=1, xf_cache=xfr)
        a12, a14 = station_means(ccr)
        Dr = np.minimum(runmax(a12), runmax(a14))
        r['rev_max'] = float(np.nanmax(Dr)) if np.any(~np.isnan(Dr)) else None
        circ = {j: circ_ncc_fast(cprep[j], tm[j]) for j in cprep}
        # exact speed-up: rolling every S14 channel by the same shift and then averaging equals averaging the circular
        # S14 correlations first and rolling the average (and its valid-channel count) once per shift
        d12 = D12m
        if circ:
            C = np.array([circ[j] for j in sorted(circ)])
            vc = np.sum(~np.isnan(C), axis=0)
            with np.errstate(invalid='ignore', divide='ignore'):
                d14c = np.nansum(np.nan_to_num(C, nan=0.0), axis=0) / np.maximum(vc, 1)
            d14c = runmax(np.where(vc >= 1, d14c, np.nan), wrap=True)
        shifts = [int(round((3600 + 180 * k) * FS)) for k in range(NSH)]
        sm = roll_max_all(d12, d14c, shifts) if circ else [None] * NSH
        r['shift_max'] = sm
        rec['nests'][n] = r
    rec['seconds'] = round(time.time() - T, 1)
    fo.write(json.dumps(rec) + '\n'); fo.flush()
    print(year, doy, ' '.join('A%s fwd %.3f rev %.3f sh %.3f' % (
        n, max([p[1] for p in rec['nests'][n]['fwd_peaks']] or [-1]), rec['nests'][n]['rev_max'] or -1,
        max([s for s in rec['nests'][n]['shift_max'] if s is not None] or [-1])) for n in nests), '%.1fs' % rec['seconds'], flush=True)
fo.close()
