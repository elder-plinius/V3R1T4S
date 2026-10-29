"""Flat-ocean check of lib/tt.py (bank pitfall: check the solver against the analytic time before scoring)."""
import sys, os, math, time, resource
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'lib'))
import numpy as np, tt
for lat0 in (0.0, 30.0, 60.0):
    t0 = time.time()
    f = tt.FMM(lat0, 150.0, radius_km=1700, flat_depth=4000.0)
    c = math.sqrt(9.81 * 4000) * 60 / 1000
    errs = []
    for az in np.arange(0, 360, 7.5):
        for dist in (200.0, 800.0, 1500.0):
            # destination point on the sphere
            p0, l0, b, d = math.radians(lat0), math.radians(150.0), math.radians(az), dist / tt.RE
            p = math.asin(math.sin(p0) * math.cos(d) + math.cos(p0) * math.sin(d) * math.cos(b))
            l = l0 + math.atan2(math.sin(b) * math.sin(d) * math.cos(p0), math.cos(d) - math.sin(p0) * math.sin(p))
            T, sd, h = f.eta(math.degrees(p), math.degrees(l), dmin=20)
            errs.append((dist, az, (T - dist / c) / (dist / c) * 100))
    e = np.array(errs)
    for dist in (200.0, 800.0, 1500.0):
        m = e[e[:, 0] == dist][:, 2]
        print(f'lat0 {lat0:4.0f} dist {dist:6.0f} km: error % min {m.min():+.2f} max {m.max():+.2f} mean {m.mean():+.2f}')
    print(f'  grid {f.T.shape}, {time.time() - t0:.1f} s')
print('peak RSS MB', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20)
