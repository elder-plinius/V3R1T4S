#!/usr/bin/env python3
"""Run method D (D.py) over the cycle types in a CSV of method-A values, one lane of several.
Order: by #cycles of length>=3 ascending (cost grows ~x5-8 per long cycle); within that, types B cannot cover (> BMAX cycles) first.
Engine: D.F_D for < symL long cycles, Dsym.F_Dsym (same short part, symmetric long DP) otherwise.
Output lines: 'partition;F_D;F_A;ok|MISMATCH|ERR' appended and flushed per type (= checkpoint);
on restart, types already in the output are skipped."""
import sys, os, time, argparse, resource, signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import D, Dsym
ap = argparse.ArgumentParser()
ap.add_argument('--csv'); ap.add_argument('--N', type=int, default=0); ap.add_argument('--out'); ap.add_argument('--lane', type=int, default=0)
ap.add_argument('--lanes', type=int, default=1); ap.add_argument('--bmax', type=int, default=11)
ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--tcap', type=int, default=0)  # per-type seconds; 0 = none
ap.add_argument('--stride', type=int, default=1)
ap.add_argument('--pmod', type=int, default=521)  # modulus 2^pmod-1 (Mersenne prime exponent)
ap.add_argument('--symL', type=int, default=8)  # use Dsym (symmetric long part) for types with >= symL long cycles
a = ap.parse_args()
D.PMOD = Dsym.PMOD = (1 << a.pmod) - 1
D.set_degree(3)
types = []
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for k in range(min(n, mx), 0, -1):
        for r in parts(n - k, k): yield (k,) + r
if a.N:  # no method-A values per type: status 'na', the sum is checked against method A's U(N)
    types = [(lam, None) for lam in parts(a.N)]
else:
    for ln in open(a.csv):
        if ln.startswith('#') or not ln.strip(): continue
        p, v = ln.strip().split(';'); lam = tuple(int(x) for x in p.split())
        types.append((lam, int(v)))
key = lambda t: (sum(1 for x in t[0] if x >= 3), 0 if len(t[0]) > a.bmax else 1, len(t[0]))
types.sort(key=key)
mine = types[a.lane::a.lanes]
mine = mine[::a.stride]
if a.limit: mine = mine[:a.limit]
class TCap(Exception): pass
def _al(*_): raise TCap()
signal.signal(signal.SIGALRM, _al)
done = set()
if os.path.exists(a.out):
    for ln in open(a.out):
        f = ln.split(';')
        if len(f) >= 4 and f[3] not in ('TIMEOUT', 'ERR'): done.add(f[0])  # ERR (MemoryError) is retried
t0 = time.time(); n = mism = 0
with open(a.out, 'a') as fo:
    for lam, fa in mine:
        p = ' '.join(map(str, lam))
        if p in done: continue
        t = time.time()
        try:
            signal.alarm(a.tcap); L = sum(1 for x in lam if x >= 3)
            fd = Dsym.F_Dsym(lam) if L >= a.symL else D.F_D(lam); signal.alarm(0); st = 'na' if fa is None else ('ok' if fd == fa else 'MISMATCH')
        except MemoryError:
            signal.alarm(0); fd, st = -1, 'ERR'
        except TCap:
            fd, st = -1, 'TIMEOUT'
        n += 1; mism += st not in ('ok', 'na')
        fo.write(f'{p};{fd};{fa};{st};{time.time()-t:.3f}\n'); fo.flush()
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024
print(f'DONE lane={a.lane} new={n} notok={mism} dt={time.time()-t0:.1f}s maxrss={rss}MB', flush=True)
