"""Claim run a100_1030, PREREG R6: the PDS tables as fetched in this run (16:15-16:16Z) and the Onodera SP windows
against the candidate onset 1973-10-30 02:25:51.509 and window start 02:25:21.509.

usage: r6_check_1030.py TOOLS_DIR CATALOG_DIR LIT_DIR
Rule: no row within +/- 5 min of either time (rows are minute-resolution, so +59 s is allowed in the reported
distance) and neither time inside a levent start-stop span (9999 = to the next event); also no Onodera window
within +/- 5 min of, or containing, either time. Also reported: the nearest rows, every levent row of 1973 days
302-304, unparsed rows, and the nearest row to the first claimed event (1973-11-26 07:46:28.641) for comparison.
"""
import sys
sys.path.insert(0, sys.argv[1])
import numpy as np
import catalog_check
import onodera_check

NS = 1_000_000_000
rows = catalog_check.load_all(sys.argv[2])
ono = onodera_check.load(sys.argv[3])
T = {'onset': int(np.datetime64('1973-10-30T02:25:51.509', 'ns').astype(np.int64)),
     'window_start': int(np.datetime64('1973-10-30T02:25:21.509', 'ns').astype(np.int64))}
print('dated rows loaded: %d; unparsed (malformed in the source): %s' % (len(rows), catalog_check.UNPARSED))
ok = True
for lab, t in T.items():
    hits = catalog_check.matches(rows, t)
    oh = onodera_check.matches(ono, t)
    near = sorted(rows, key=lambda r: min(abs(r[0] - t), abs(r[1] - t)))[:4]
    print('%s %s: catalogue rows within +/- 5 min or spanning it: %d %s; Onodera windows: %d %s' % (
        lab, str(np.datetime64(t, 'ns'))[:23], len(hits), hits, len(oh), oh))
    for a, b, l in near:
        print('   nearest: %s (start %+.1f min, stop %+.1f min) %s' % (str(np.datetime64(a, 'ns'))[:16], (a - t) / 60e9, (b - t) / 60e9, l))
    on = sorted(ono, key=lambda r: min(abs(r[0] - t), abs(r[1] - t)))[:2]
    for a, b, l in on:
        print('   nearest Onodera: %s-%s (%+.1f min) %s' % (str(np.datetime64(a, 'ns'))[:16], str(np.datetime64(b, 'ns'))[11:16], (a - t) / 60e9, l))
    if hits or oh:
        ok = False
d0 = int(np.datetime64('1973-10-29T00:00', 'ns').astype(np.int64)); d1 = int(np.datetime64('1973-11-01T00:00', 'ns').astype(np.int64))
print('levent and other rows on 1973 days 302-304:')
for a, b, l in sorted(r for r in rows if d0 <= r[0] < d1):
    print('   %s -> %s %s' % (str(np.datetime64(a, 'ns'))[:16], str(np.datetime64(b, 'ns'))[:16], l))
print('R6 pass:', ok)
