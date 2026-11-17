"""Forward-only scan of one year of S12 LP with many nest templates (seed stage of lens 3). Resumable, one JSON
line per day: for each nest, declustered (+/- 5 min) peaks with D >= 0.15 or best single-channel CC >= 0.45,
with per-channel CC.

usage: multinest_scan.py TEMPLATES.npz YEAR DOY_FROM DOY_TO OUT.jsonl
"""
import sys, os, json, time
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from apollo_lib import NS, decluster, day_start_ns
from evlib import FS
from scan import prep_day, corr_channels, NDAY

z = np.load(sys.argv[1])
year, d0, d1, out = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
nests = list(z['nests']); TM = z['tm']; chans = [tuple(c.split('.')) for c in z['chans']]
band = tuple(float(b) for b in z['band']); M = TM.shape[2]
SEP = int(300 * FS)
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
    t0 = day_start_ns(year, doy)
    cache = {}
    rec['peaks'] = {}
    for n, tm in zip(nests, TM):
        D, ccs, nv = corr_channels(pp, list(tm), xf_cache=cache)
        best = np.nanmax(np.where(np.isnan(ccs), -1, ccs), axis=0)
        score = np.where(np.isnan(D), np.nan, np.maximum(D, best - 0.30))  # keep D >= 0.15 or best CC >= 0.45
        pk = decluster(score, SEP, 0.15)
        rec['peaks'][str(n)] = [[int(t0 + round(i / FS * 1e9)), round(float(D[i]), 4),
                                 [None if np.isnan(c) else round(float(c), 4) for c in ccs[:, i]]] for i in pk]
        rec.setdefault('scanned', float(np.mean(~np.isnan(D))))
    rec['seconds'] = round(time.time() - T, 1)
    fo.write(json.dumps(rec) + '\n'); fo.flush()
    print(year, doy, rec['seconds'], flush=True)
fo.close()
