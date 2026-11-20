"""Phase A benchmark. Usage: python3 phaseA_bench.py [n_sample=36] [lists=2000] [mixes=3]
Test 1 (consistency, 60 instances with a posted schedule): rebuild the posted schedule with SGS in order of its start times
using its modes, then FBI; the result must be checker-valid and never longer than the posted value.
Test 2 (quality from scratch, stratified sample: 2 instances per (activities, modes, renewable resources) group, one open and one
closed where possible): layer 1 mode mixes (each new mix excludes the previous ones) x layer 2 multistart; report the gap to the
current UB. Every kept schedule passes mm.check. Output: out/phaseA_bench.json and a printed summary."""
import sys, os, json, time, zipfile, random, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mm, engine
RAW = os.path.join(HERE, '..', '..', '2026-11-19-mmlib-scout', 'raw')
n_sample = int(sys.argv[1]) if len(sys.argv) > 1 else 36; LISTS = int(sys.argv[2]) if len(sys.argv) > 2 else 2000; MIXES = int(sys.argv[3]) if len(sys.argv) > 3 else 3
L = open(os.path.join(RAW, 'MMplus_2.csv'), encoding='utf-8-sig', errors='replace').read().splitlines(); h = L[4].split(';')
rows = {int(l.split(';')[0]): dict(zip(h, l.split(';'))) for l in L[5:] if l.split(';')[0].isdigit()}
bks = {}
for l in open(os.path.join(RAW, 'MMplus_2_BKS.csv'), encoding='utf-8-sig'):
    p = l.strip().split(';')
    if p[0].isdigit(): bks[int(p[0])] = [int(x) for x in p[4:] if x]
Z = zipfile.ZipFile(os.path.join(RAW, 'MMplus.zip'))
def inst(i): return mm.read(Z.read('MMplus/' + rows[i]['Ref1']).decode())
UB = lambda i: int(rows[i]['UB value']); LB = lambda i: int(rows[i]['LB value'])
out = dict(test1=[], test2=[])
# warm up numba
X0 = engine.Inst(inst(1)); m0, _ = engine.mode_mix(X0, 2); engine.multistart(X0, m0, 3)

rng = random.Random(20261119)
with_sched = [i for i in rows if bks.get(i)]
t1 = rng.sample(with_sched, 60); bad1 = 0; worse = 0; better = 0
for i in t1:
    I = inst(i); X = engine.Inst(I); n = X.n; v = bks[i]; k = len(v) // 2 - 1
    modes = np.array([1] + v[:k] + [1], np.int64); starts = np.array(v[k:], np.int64)
    d, q = engine.realise(X, modes); pos = {j: p for p, j in enumerate(engine.topo(X))}
    order = np.array(sorted(range(n), key=lambda j: (starts[j], pos[j])), np.int64)
    st = engine.sgs(order, d, q, X.cap, X.pp, X.pi, X.H); st, mk = engine.fbi(st, d, q, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20)
    r = mm.check(I, [int(x) for x in modes], [int(x) for x in st]); ok = r == 'VALID makespan %d' % mk
    bad1 += not ok; worse += mk > UB(i); better += mk < UB(i)
    out['test1'].append(dict(id=i, ub=UB(i), rebuilt=int(mk), check=r))
print('test 1: %d posted schedules rebuilt; checker failures %d; longer than posted %d; shorter than posted %d' % (len(t1), bad1, worse, better), flush=True)

groups = collections.defaultdict(list)
for i, r in rows.items(): groups[(int(r['# Act']), int(float(r['# Modes'].replace(',', '.'))), int(r['# RR']))].append(i)
sample = []
for g in sorted(groups):
    ids = groups[g]; op = [i for i in ids if LB(i) < UB(i)]; cl = [i for i in ids if LB(i) == UB(i)]
    pick = ([rng.choice(op)] if op else []) + ([rng.choice(cl)] if cl else [])
    sample += pick[:2]
sample = sample[:n_sample]
for i in sample:
    I = inst(i); X = engine.Inst(I); t0 = time.time(); avoid = []; best = None
    for mix in range(MIXES):
        modes, proxy = engine.mode_mix(X, 5.0, 4, seed=mix + 1, avoid=avoid)
        if modes is None: break
        avoid.append(modes); mk, st = engine.multistart(X, modes, LISTS // MIXES, seed=mix)
        if best is None or mk < best[0]: best = (mk, st, modes, proxy)
    if best is None:
        out['test2'].append(dict(id=i, ub=UB(i), lb=LB(i), result=None)); print(i, 'no budget-feasible mode mix found', flush=True); continue
    mk, st, modes, proxy = best
    r = mm.check(I, [int(x) for x in modes], [int(x) for x in st])
    rec = dict(id=i, file=rows[i]['Ref1'], open=LB(i) < UB(i), lb=LB(i), ub=UB(i), ours=int(mk), proxy=proxy, gap_to_ub=(mk - UB(i)) / UB(i), secs=round(time.time() - t0, 1), check=r)
    out['test2'].append(rec)
    print('%5d %-15s %s LB %4d UB %4d ours %4d (%+.1f%%) proxy %4d %5.1fs %s' % (i, rec['file'], 'open  ' if rec['open'] else 'closed', LB(i), UB(i), mk, 100 * rec['gap_to_ub'], proxy, rec['secs'], r), flush=True)
T2 = [r for r in out['test2'] if r.get('ours') is not None]
print('test 2: %d instances; checker failures %d; mean gap to UB %+.1f%% (open %+.1f%%, closed %+.1f%%); at or below UB %d; strictly below UB %d' % (
    len(T2), sum(not r['check'].startswith('VALID') for r in T2), 100 * np.mean([r['gap_to_ub'] for r in T2]),
    100 * np.mean([r['gap_to_ub'] for r in T2 if r['open']] or [0]), 100 * np.mean([r['gap_to_ub'] for r in T2 if not r['open']] or [0]),
    sum(r['ours'] <= r['ub'] for r in T2), sum(r['ours'] < r['ub'] for r in T2)))
json.dump(out, open(os.path.join(HERE, '..', 'out', 'phaseA_bench.json'), 'w'), indent=1)
