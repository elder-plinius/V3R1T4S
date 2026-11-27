#!/usr/bin/env python3
"""Method D at general degree d (Dd.py, exact Fractions) over all cycle types of N, one lane of several, each type
diffed against method A (engine.F_A, computed here). Order: by number of long cycles ascending. Output lines
'partition;F_D;F_A;ok|MISMATCH|ERR|TIMEOUT;seconds', flushed per type (= checkpoint); restart skips done types and
retries ERR/TIMEOUT. With all types ok, U_d(N) = sum F/z_lambda by both methods (dsumcheck-style)."""
import sys, os, time, argparse, resource, signal, gc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import Dd, Ddsym, Ddsym2, engine as E
ap = argparse.ArgumentParser()
ap.add_argument('--d', type=int); ap.add_argument('--N', type=int); ap.add_argument('--out'); ap.add_argument('--lane', type=int, default=0)
ap.add_argument('--lanes', type=int, default=1); ap.add_argument('--tcap', type=int, default=0)
ap.add_argument('--clearmb', type=int, default=600)
ap.add_argument('--symL', type=int, default=99)
ap.add_argument('--noA', action='store_true')
ap.add_argument('--sub', type=int, default=0); ap.add_argument('--subs', type=int, default=1); ap.add_argument('--done', default='')  # 2026-11-21: split one lane's remaining types over --subs processes; --done = the lane file whose finished types are skipped
ap.add_argument('--cvdp', action='store_true')  # 2026-11-21: with --vdp, the short part by the C program svdp (Svdpc)
ap.add_argument('--vdp', action='store_true')  # Ddsym2: short part by the vertex DP (Svdp.S_all), for d >= 6  # skip the per-type method-A value (U_D is compared with method A's U in dsumcheck)  # types with >= symL long cycles use Ddsym (count-vector long part)
a = ap.parse_args()
Dd.set_degree(a.d); E.set_degree(a.d)
if a.cvdp:
    import Svdpc; Ddsym2.SALL = Svdpc.S_all
types = sorted(Dd._parts(a.N), key=lambda t: (sum(1 for x in t if x >= 3), len(t)))[a.lane::a.lanes]
class TCap(Exception): pass
def _al(*_): raise TCap()
signal.signal(signal.SIGALRM, _al)
# 2026-11-20: Dd/engine keep unbounded lru caches across types; after one MemoryError the process stayed full and every
# later type failed in ~0 s (1800 false ERR on d5 N=30). Now: caches cleared when VmSize passes --clearmb and after any
# MemoryError (then the type is retried once on empty caches); only a second MemoryError is recorded as ERR.
def _vm_mb():
    try: return int(open('/proc/self/statm').read().split()[0]) * os.sysconf('SC_PAGE_SIZE') // 2**20
    except Exception: return 0
def _clear():
    Dd.set_degree(a.d); E.set_degree(a.d); Dd._nodes.cache_clear(); gc.collect()
done = set()
for _f in [x for x in (a.out, a.done) if x and os.path.exists(x)]:
    for ln in open(_f):
        f = ln.split(';')
        if len(f) >= 4 and f[3] not in ('TIMEOUT', 'ERR'): done.add(f[0])
lane_done = set(ln.split(';')[0] for ln in open(a.done) if len(ln.split(';')) >= 4 and ln.split(';')[3] not in ('TIMEOUT', 'ERR')) if a.done and os.path.exists(a.done) else set()
types = [t for t in types if ' '.join(map(str, t)) not in lane_done][a.sub::a.subs]  # split fixed by the lane file only, so a resumed sub keeps its share
t0 = time.time(); n = bad = 0
with open(a.out, 'a') as fo:
    for lam in types:
        p = ' '.join(map(str, lam))
        if p in done: continue
        t = time.time()
        if _vm_mb() > a.clearmb: _clear()
        st = None
        for attempt in (0, 1):
            try:
                signal.alarm(a.tcap); fd = (Ddsym2.F_D if a.vdp else Ddsym.F_D if sum(1 for x in lam if x >= 3) >= a.symL else Dd.F_D)(lam); signal.alarm(0); fa = -1 if a.noA else E.F_A(lam); st = 'Donly' if a.noA else ('ok' if fd == fa else 'MISMATCH')
                break
            except MemoryError:
                signal.alarm(0); fd = fa = -1; st = 'ERR'; _clear()
            except TCap:
                fd = fa = -1; st = 'TIMEOUT'; break
        n += 1; bad += st not in ('ok', 'Donly')
        fo.write(f'{p};{fd};{fa};{st};{time.time()-t:.3f}\n'); fo.flush()
print(f'DONE d={a.d} N={a.N} lane={a.lane} new={n} notok={bad} dt={time.time()-t0:.1f}s maxrss={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024}MB', flush=True)
