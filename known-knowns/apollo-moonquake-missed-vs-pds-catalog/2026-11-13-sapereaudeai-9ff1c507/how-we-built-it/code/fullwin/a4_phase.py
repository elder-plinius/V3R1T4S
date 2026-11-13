"""PREREG A4 (descriptive): anomalistic phases (Meeus mean anomaly M') of the catalogued A100 events and the candidate;
1973 A100 sequence with spacings; shortest circular interval holding 95% of all A100 events (R9 as fixed).
usage: a4_phase.py TOOLS_DIR LEVENT.csv"""
import sys
sys.path.insert(0, sys.argv[1])
import numpy as np, pandas as pd
from ephem import mean_anomaly_deg
from apollo_lib import cat_time_ns
cat = pd.read_csv(sys.argv[2], dtype=str)
a = cat[(cat['T2'] == 'A') & (cat['N2'].str.strip() == '100')]
t = np.array([cat_time_ns(r.Y, r.JD, r.S) for r in a.itertuples()], dtype=np.int64)
ph = mean_anomaly_deg(t)
c = int(np.datetime64('1973-11-26T07:46:28.641', 'ns').astype(np.int64)); c2 = int(np.datetime64('1973-10-30T02:25:51.509', 'ns').astype(np.int64))
print('catalogued A100 events:', len(t))
s = np.sort(ph); n = len(s); k = int(np.ceil(0.95 * n))
best = None
for i in range(n):
    j = (i + k - 1) % n
    w = (s[j] - s[i]) % 360
    if best is None or w < best[0]:
        best = (w, s[i], s[j])
print('shortest 95%% interval: [%.2f, %.2f] width %.1f deg (k=%d of %d)' % (best[1], best[2], best[0], k, n))
pc = float(mean_anomaly_deg(c)); pc2 = float(mean_anomaly_deg(c2))
print('candidate phase %.2f deg; second candidate %.2f deg' % (pc, pc2))
h, e = np.histogram(ph, bins=12, range=(0, 360))
print('A100 phase histogram (30 deg bins):', dict(zip([int(x) for x in e[:-1]], [int(x) for x in h])))
z = np.mean(np.exp(1j * np.radians(ph)))
print('circular mean %.1f deg, resultant length %.3f; candidate offset from mean %.1f deg' % (
    np.degrees(np.angle(z)) % 360, abs(z), (pc - np.degrees(np.angle(z)) + 180) % 360 - 180))
print('events within +/- 20 deg of the candidate phase: %d of %d (uniform expectation %.1f)' % (
    int(np.sum(np.abs((ph - pc + 180) % 360 - 180) <= 20)), n, n * 40 / 360))
y73 = sorted([(int(tt), float(p)) for tt, p, y in zip(t, ph, a['Y']) if y == '73'] + [(c, pc), (c2, pc2)])
prev = None
for tt, p in y73:
    lab = 'NEW' if tt in (c, c2) else 'cat'
    d = (tt - prev) / 86400e9 if prev else float('nan')
    print('  %s %s phase %6.1f  dt %6.2f d' % (str(np.datetime64(tt, 'ns'))[:16], lab, p, d))
    prev = tt
