#!/usr/bin/env python3
"""Compare sweep outputs with Catagolue cost tables. Prints IMPROVE / UNTAB candidates."""
import sys, glob, os, re
D = os.path.join(os.path.dirname(__file__), '..', 'data')
tab = {}
for fn in glob.glob(os.path.join(D, '*-synthesis-costs.txt')):
    cls = os.path.basename(fn).split('-')[0]
    if os.path.getsize(fn) < 100: continue
    d = {}
    for l in open(fn):
        if l.startswith('"apgcode"'): continue
        p = l.strip().split('","')
        if len(p) == 2:
            d[p[0].strip('"')] = int(p[1].strip('"')[-3:])
    tab[cls] = d
k = int(sys.argv[1]) if len(sys.argv) > 1 else 1
best = {}
for fn in sys.argv[2:]:
    for l in open(fn):
        if l.startswith('#'): continue
        s = l.split()
        if len(s) != 7: continue
        ia, ic, rot, lane, ph, per, oa = s
        ic = int(ic); cls = oa.split('_')[0]
        if cls not in tab: continue
        cur = tab[cls].get(oa)
        new = ic + k
        if cur is None or new < cur:
            if oa not in best or new < best[oa][0]:
                best[oa] = (new, cur, ia, ic, rot, lane, ph, per)
for oa, (new, cur, ia, ic, rot, lane, ph, per) in sorted(best.items(), key=lambda kv: -((kv[1][1] or 999) - kv[1][0])):
    tag = 'UNTAB' if cur is None else 'IMPROVE'
    print(tag, oa, 'new', new, 'cur', cur, 'from', ia, ic, 'rot', rot, 'lane', lane, 'ph', ph, 'per', per)
