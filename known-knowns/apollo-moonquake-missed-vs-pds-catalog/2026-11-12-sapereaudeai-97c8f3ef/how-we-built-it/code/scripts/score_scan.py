"""FROZEN SCAN of one year with frozen templates: forward data, time-reversed data (bank null C0) and N
phase-randomised template controls (C1..CN). One JSON line per day, resumable (days already in OUT are skipped).

usage: score_scan.py FROZEN.npz YEAR DOY_FROM DOY_TO OUT.jsonl N_CONTROLS SEED_BASE
"""
import sys, os, json, time
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from apollo_lib import NS, decluster, day_start_ns
from evlib import FS
from scan import prep_day, corr_channels, reverse_prepped, phase_randomise, NDAY

npz = np.load(sys.argv[1])
year, d0, d1, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
NC, SEED = int(sys.argv[6]), int(sys.argv[7])
tm = list(npz['tm']); chans = [tuple(c.split('.')) for c in npz['chans']]
band = tuple(float(b) for b in npz['band'])
if len(band) > 2 and band[2] == 0:
    band = band[:2]
M = tm[0].size
SEP = int(300 * FS)
FLOOR = 0.05
controls = [phase_randomise(tm, SEED + k) for k in range(1, NC + 1)]
import re
CACHE = __import__('os').environ.get('APOLLO_WF', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'waveforms'))
INV = set(re.findall(r'(xa\.s1[0-9]\.00\.mh[12z]\.\d{4}\.\d{3})\.0', open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'data', 'pse', 'collection_data_seed_inventory.csv')).read()))
done = set()
if os.path.isfile(out):
    for line in open(out):
        try:
            done.add(json.loads(line)['doy'])
        except Exception:
            pass
fo = open(out, 'a')
for doy in range(d0, d1 + 1):
    if doy in done:
        continue
    # all of this day's (and the next day's) files listed in the PDS inventory must be in the cache before scanning;
    # otherwise skip without writing, so the day is scanned on a later pass (resumable)
    need = []
    for (sta, ch) in chans:
        for (yy, dd) in ((year, doy), (year + (doy == (366 if year % 4 == 0 else 365)), 1 if doy == (366 if year % 4 == 0 else 365) else doy + 1)):
            stem = 'xa.%s.00.%s.%d.%03d' % (sta, ch, yy, dd)
            if stem in INV and not os.path.isfile(os.path.join(CACHE, sta, stem + '.0.mseed')):
                need.append(stem)
    if need:
        print('skip (not yet downloaded):', doy, need[:3], flush=True)
        continue
    T = time.time()
    rec = dict(year=year, doy=doy)
    pp = prep_day(year, doy, chans, band, M)
    rec['channels_present'] = [('%s.%s' % c) for c, p in zip(chans, pp) if p is not None]
    if sum(p is not None for p in pp) < 2:
        rec['scanned'] = 0.0
        fo.write(json.dumps(rec) + '\n'); fo.flush(); continue
    t0 = day_start_ns(year, doy)
    cache = {}
    D, ccs, nv = corr_channels(pp, tm, xf_cache=cache)
    ok = ~np.isnan(D)
    rec['scanned'] = float(ok.mean())
    # coverage per minute (fraction of window starts with D defined)
    per_min = int(60 * FS)
    cov = [float(ok[i:i + per_min].mean()) for i in range(0, NDAY, per_min)]
    rec['coverage_per_min'] = [round(c, 3) for c in cov]
    pk = decluster(D, SEP, FLOOR)
    rec['fwd_peaks'] = [[int(t0 + round(i / FS * 1e9)), round(float(D[i]), 5),
                         [None if np.isnan(c) else round(float(c), 4) for c in ccs[:, i]], int(nv[i])] for i in pk]
    rec['fwd_max'] = float(np.nanmax(D)) if ok.any() else None
    # discontinuities (sample index in 6.625 Hz grid of the day span) per channel
    rec['disc'] = {('%s.%s' % c): (p[2][:50] if p is not None else None) for c, p in zip(chans, pp)}
    # bank null C0: time-reversed data
    Dr, _, _ = corr_channels(reverse_prepped(pp), tm)
    pr = decluster(Dr, SEP, FLOOR)
    rec['rev_peaks'] = [round(float(Dr[i]), 5) for i in pr]
    rec['rev_max'] = float(np.nanmax(Dr)) if np.any(~np.isnan(Dr)) else None
    # controls C1..CN: phase-randomised templates on forward data
    cm = []
    for tk in controls:
        Dk, _, _ = corr_channels(pp, tk, xf_cache=cache)
        cm.append(round(float(np.nanmax(Dk)), 5) if np.any(~np.isnan(Dk)) else None)
    rec['ctrl_max'] = cm
    rec['seconds'] = round(time.time() - T, 1)
    fo.write(json.dumps(rec) + '\n'); fo.flush()
    print(year, doy, 'scanned %.3f fwd_max %.3f rev_max %.3f ctrl_max %.3f  %.1fs' % (
        rec['scanned'], rec['fwd_max'] or -1, rec['rev_max'] or -1, max(c for c in cm if c is not None) if cm else -1,
        rec['seconds']), flush=True)
fo.close()
