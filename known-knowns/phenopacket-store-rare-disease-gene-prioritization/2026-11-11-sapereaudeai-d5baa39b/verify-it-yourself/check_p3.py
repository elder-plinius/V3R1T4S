"""Standalone checker (Python standard library only) for the p3 audit numbers in object/.
Checks: the object files are the published ones (sha256); every per-case reciprocal rank, top-1 and top-10 value
follows from the stored rank counts (n_greater, n_ties) under uniform random tie-breaking; MRR and top-1 per
condition, the paired drop and its share equal summary.json; the 400-control paired label-swap null reproduces
exactly; case- and publication-level percentile bootstrap intervals agree with summary.json within Monte Carlo
tolerance (0.015 and 0.03). Last line PASS or FAIL. Run from the package folder."""
import csv, hashlib, json, math, random, sys

PINNED = {'object/percase.tsv': 'd5baa39b2d9caf36add75717a90213c2751e649a73774b60e5b07308200aca10', 'object/summary.json': '00dfa4b9f2879a320b565e73d706968d489230053842abde0c9695833270e393'}
fails = []
def bad(msg):
    fails.append(msg); print('MISMATCH:', msg)
for p, h in PINNED.items():
    got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if got != h:
        bad('%s sha256 %s != pinned %s' % (p, got, h))
rows = list(csv.DictReader(open('object/percase.tsv', encoding='utf-8'), delimiter='\t'))
S = json.load(open('object/summary.json'))
def stats(g, k):
    g = int(g); k = int(k)
    rr = math.fsum(1.0 / r for r in range(g + 1, g + k + 2)) / (k + 1)
    t1 = 1.0 / (k + 1) if g == 0 else 0.0
    t10 = 0.0 if g >= 10 else min(k + 1, 10 - g) / (k + 1)
    return rr, t1, t10
V = {'C': [], 'PRE': []}
for r in rows:
    for c in ('C', 'PRE'):
        rr, t1, t10 = stats(r['g_ngt_' + c], r['g_ties_' + c])
        for name, v in (('rr', rr), ('top1', t1), ('top10', t10)):
            if abs(v - float(r['%s_%s' % (name, c)])) > 1e-9:
                bad('%s %s_%s %r != %r' % (r['case_id'], name, c, float(r['%s_%s' % (name, c)]), v))
        V[c].append((rr, t1, t10))
n = len(rows)
print('cases', n, 'publications', len(set(r['pmid'] for r in rows)))
if n != S['n_cases']: bad('n_cases')
mean = lambda a: math.fsum(a) / len(a)
mC = mean([v[0] for v in V['C']]); mP = mean([v[0] for v in V['PRE']])
tC = mean([v[1] for v in V['C']]); tP = mean([v[1] for v in V['PRE']])
for k, v in (('MRR_C', mC), ('MRR_PRE', mP), ('dMRR', mC - mP), ('share_dMRR', (mC - mP) / mC), ('top1_C', tC), ('top1_PRE', tP), ('dTop1', tC - tP)):
    print('%-10s recomputed %.6f claimed %.6f' % (k, v, S[k]['point']))
    if abs(v - S[k]['point']) > 1e-9: bad(k)
d = [a[0] - b[0] for a, b in zip(V['C'], V['PRE'])]
ctrl = []
for k in range(400):
    rng = random.Random(20261111 + k)
    s = [(-1.0 if rng.random() < 0.5 else 1.0) for _ in range(n)]
    ctrl.append(math.fsum(x * y for x, y in zip(s, d)) / n)
print('null: 400 controls, best %.6f, real %.6f, real beats all: %s' % (max(ctrl), mC - mP, (mC - mP) > max(ctrl)))
if abs(max(ctrl) - S['null_NSF']['best_control']) > 1e-9 or not (mC - mP) > max(ctrl): bad('null')
rng = random.Random(7)
def pct(a, q):
    a = sorted(a); i = q * (len(a) - 1); lo = math.floor(i); hi = math.ceil(i)
    return a[lo] + (a[hi] - a[lo]) * (i - lo)
boot = {'dMRR': [], 'dTop1': []}
for _ in range(2000):
    idx = [rng.randrange(n) for _ in range(n)]
    boot['dMRR'].append(mean([d[i] for i in idx]))
    boot['dTop1'].append(mean([V['C'][i][1] - V['PRE'][i][1] for i in idx]))
pm = {}
for i, r in enumerate(rows): pm.setdefault(r['pmid'], []).append(i)
keys = sorted(pm); cb = []
for _ in range(2000):
    idx = [i for _k in range(len(keys)) for i in pm[keys[rng.randrange(len(keys))]]]
    cb.append(mean([d[i] for i in idx]))
for k, b, tol, w in (('dMRR', boot['dMRR'], 0.015, 'ci95_case'), ('dTop1', boot['dTop1'], 0.015, 'ci95_case'), ('dMRR', cb, 0.03, 'ci95_pub_cluster')):
    lo, hi = pct(b, 0.025), pct(b, 0.975); cl = S[k][w]
    print('%s %s: stdlib bootstrap [%.4f, %.4f], claimed [%.4f, %.4f]' % (k, w, lo, hi, cl[0], cl[1]))
    if abs(lo - cl[0]) > tol or abs(hi - cl[1]) > tol: bad('%s %s' % (k, w))
print('FAIL' if fails else 'PASS')
sys.exit(1 if fails else 0)
