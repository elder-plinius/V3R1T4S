"""Claim run a100_1030, PREREG M4 (descriptive): every uncatalogued detection above its own nest's null in the N0 rerun
(all 12 nests), with R7, R9, gap, thermal and Onodera flags, and the Onodera rows that match any of them.

usage: m4_list.py CAND12.json LIT_DIR TOOLS_DIR
"""
import sys, json
sys.path.insert(0, sys.argv[3])
import numpy as np
import onodera_check

c = json.load(open(sys.argv[1]))
ono = onodera_check.load(sys.argv[2])
NS = 1_000_000_000
rows = []
for n, lst in c['candidates'].items():
    for r in lst:
        if r['above_null'] and r['new']:
            rows.append((n, r))
rows.sort(key=lambda x: -x[1]['Dc'])
print('uncatalogued detections above their nest null (N0 rerun, 12 nests): %d' % len(rows))
for n, r in rows:
    t = int(np.datetime64(r['onset'].rstrip('Z'), 'ns').astype(np.int64))
    print('A%-4s %s Dt %.4f best %s ccs %s R7 %s R9 %s gap %s thermal %s elev %s onodera %s' % (
        n, r['onset'], r['Dc'], r['best_cc'], r['ccs'], r['r7'], r['r9'], r['gap_ok'], r['thermal_ok'],
        {k: round(v, 1) for k, v in r['elev'].items()}, onodera_check.matches(ono, t)))
k7 = [(n, r) for n, r in rows if r['r7']]
print('of these meeting R7 (best single channel >= 0.5 at both stations): %d -> %s' % (len(k7), [(('A' + n), r['onset']) for n, r in k7]))
full = [(n, r) for n, r in k7 if r['r9'] and r['gap_ok'] and r['thermal_ok'] and not r['onodera']]
print('meeting R7, R9, gap, thermal and outside Onodera SP windows: %d -> %s' % (len(full), [(('A' + n), r['onset']) for n, r in full]))
