"""Conservative re-sweep: identical LP, but a table cell printed as a SINGLE number (no 'lo-hi' range) is NOT used as an
upper bound for other cells (only explicit 'lo-hi' upper bounds and elementary bounds are used). This removes any
dependence on the reading 'single number = exact value'. Also reports, for each surviving cell, the input cells used."""
import sys, json, re
sys.argv = ['x', '../../tools', '../../data/Andw.html']
exec(open('code/lpsweep.py').read().split("if __name__")[0])
from cells2 import parse2
C2 = parse2('../../data/Andw.html')
for k, v in C2.items():
    if k not in CELLS: CELLS[k] = v
    else:
        a, b = CELLS[k], v; his = [h for h in (a[1], b[1]) if h is not None]
        CELLS[k] = (max(a[0], b[0]), min(his) if his else None, a[2] + ' | ' + b[2])
TABLE = dict(CELLS)
# keep only explicit ranges as usable upper bounds for sub-cells
for k, (lo, hi, raw) in list(CELLS.items()):
    if '-' not in raw: CELLS[k] = (lo, None, raw)
U.cache_clear()
res = []
for k, (lo, hi, raw) in sorted(TABLE.items()):
    n, d, w = k
    if 2 * w > n or hi is None: continue
    r = certify(n, d, w)
    if r and r['bound'] < hi:
        X, rows, rhs, tags = build(n, d, w)
        used = []
        for t, y in zip(tags, r['y']):
            if y == 0: continue
            if t.startswith('M'):
                tt, s = int(t[1]), int(t[2]); used.append(f'{t}:U({n-tt},{d},{w-s})={U(n-tt,d,w-s)} [{TABLE.get((n-tt,d,min(w-s,n-tt-w+s)),("","","elementary"))[2]}]')
            elif t.startswith('X'):
                x = int(t[1:]); used.append(f'{t}:min(U({n},{d},{2*x}),C({w},{x})U({n-w},{d},{x})={comb(w,x)}*{U(n-w,d,x)} [{TABLE.get((n-w,d,min(x,n-w-x)),("","","elementary"))[2]}],...)')
            else: used.append(t)
        o = dict(cell=k, table=raw, bound=r['bound'], cert=str(r['cert']), uses=used); res.append(o); print(o, flush=True)
json.dump(res, open('output/sweep3_conservative.json', 'w'), indent=1, default=str)
print('robust cells below table:', len(res))
