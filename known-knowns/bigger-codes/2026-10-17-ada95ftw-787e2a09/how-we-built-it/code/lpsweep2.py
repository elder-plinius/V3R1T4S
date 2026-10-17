"""Extended sweep: the same LP/certificate code as lpsweep.py, over the main table PLUS the secondary
'Values of A(n,d,w)' tables (n up to 76). Where both tables list a cell, U uses the smaller numeric upper bound."""
import sys, json, time
sys.argv = ['lpsweep2', '../../tools', '../../data/Andw.html']
src = open('code/lpsweep.py').read().split("if __name__")[0]
exec(src)
from cells2 import parse2
C2 = parse2('../../data/Andw.html')
for k, v in C2.items():
    if k not in CELLS: CELLS[k] = v
    else:
        a, b = CELLS[k], v
        his = [h for h in (a[1], b[1]) if h is not None]
        CELLS[k] = (max(a[0], b[0]), min(his) if his else None, a[2] + ' | ' + b[2])
U.cache_clear()
t0 = time.time(); out = []
for (n, d, w), (lo, hi, raw) in sorted(CELLS.items()):
    if 2 * w > n: continue
    r = certify(n, d, w); rd = certify(n, d, w, moments=False, xb=False)
    if r is None: print('FAIL', n, d, w); continue
    o = dict(n=n, d=d, w=w, lo=lo, hi=hi, raw=raw, delsarte=rd and rd['bound'], strong=r['bound'], cert=str(r['cert']),
             active=[t for t, y in zip(r['tags'], r['y']) if y != 0])
    out.append(o)
    if hi is not None and r['bound'] < hi: print('BELOW', o, flush=True)
    if r['bound'] < lo: print('BUG? below lower bound', o, flush=True)
json.dump(out, open('output/sweep2.json', 'w'), indent=0)
print('cells', len(out), 'below_table', sum(1 for o in out if o['hi'] is not None and o['strong'] < o['hi']),
      'below_lo', sum(1 for o in out if o['strong'] < o['lo']), 'secs', round(time.time() - t0, 1))
