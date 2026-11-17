"""PREREG A5 / C6: which catalogued 1973 deep moonquakes look most like the candidate (reverse search output).

usage: a5_analyse.py REVERSE_SCAN.jsonl LEVENT.csv VARIANT(a|b)
Score of a levent row = largest Dt of the declustered peaks (>= 0.10) whose onset (window start + 30 s) lies in
[start - 5 min, start + 10 min]; rows with no such peak score 0 (below 0.10). Peaks within +/- 10 min of the candidate
are excluded. C6: the 10 highest-scoring catalogued deep moonquakes (T2 = A) include no A100 event and one other nest
holds >= 3 of them while that nest is < 30% of all scored 1973 deep moonquakes.
Baseline: the same score for 3000 random 15-min windows of 1973 (seed 20261113) at least 30 min from any levent row.
"""
import sys, json
import numpy as np
import pandas as pd

RS, LEV, VAR = sys.argv[1], sys.argv[2], sys.argv[3]
NS = 1_000_000_000
CAND = int(np.datetime64('1973-11-26T07:46:28.641', 'ns').astype(np.int64))
pk_t, pk_d, pk_c = [], [], []
scanned = 0
for l in open(RS):
    r = json.loads(l)
    scanned += 1
    for p in r['peaks_' + VAR]:
        on = p[0] + 30 * NS
        if abs(on - CAND) <= 600 * NS:
            continue
        pk_t.append(on); pk_d.append(p[1]); pk_c.append(p[2])
pk_t = np.array(pk_t, dtype=np.int64); pk_d = np.array(pk_d); o = np.argsort(pk_t); pk_t, pk_d = pk_t[o], pk_d[o]
pk_c = [pk_c[i] for i in o]
print('variant %s: days scanned %d, peaks >= 0.10: %d' % (VAR, scanned, len(pk_t)))

cat = pd.read_csv(LEV, dtype=str)
cat = cat[cat['Y'] == '73'].copy()
day0 = np.datetime64('1973-01-01T00:00', 'ns').astype(np.int64)
cat['t'] = [int(day0 + ((int(r.JD) - 1) * 86400 + int(str(r.S).zfill(4)[:2]) * 3600 + int(str(r.S).zfill(4)[2:]) * 60) * NS)
            for r in cat.itertuples()]
done_days = set()
for l in open(RS):
    done_days.add(json.loads(l)['doy'])
cat = cat[cat['JD'].astype(int).isin(done_days)]


def score(t):
    a = np.searchsorted(pk_t, t - 300 * NS); b = np.searchsorted(pk_t, t + 600 * NS, side='right')
    if b <= a:
        return 0.0, None
    k = a + int(np.argmax(pk_d[a:b]))
    return float(pk_d[k]), k


sc = []
for r in cat.itertuples():
    s, k = score(r.t)
    sc.append((s, k))
cat['score'] = [s for s, _ in sc]
cat['peak_ccs'] = [None if k is None else pk_c[k] for _, k in sc]
cat['peak_onset'] = [None if k is None else str(np.datetime64(int(pk_t[k]), 'ns'))[:19] for _, k in sc]
dm = cat[cat['T2'] == 'A'].copy()
dm['N2'] = dm['N2'].str.strip()
dm = dm.sort_values('score', ascending=False)
print('scored 1973 deep moonquakes (T2 = A): %d; with a peak >= 0.10: %d' % (len(dm), int((dm['score'] > 0).sum())))
print('\nTop 20 catalogued deep moonquakes by similarity to the candidate:')
for r in dm.head(20).itertuples():
    print('  73-%s %s A%-4s score %.4f  peak onset %s  ccs %s  A4=%s' % (r.JD, str(r.S).zfill(4), r.N2, r.score, r.peak_onset, r.peak_ccs, r.A4))
top10 = list(dm.head(10)['N2'])
share = dm['N2'].value_counts() / len(dm)
cnt = pd.Series(top10).value_counts()
others = [(n, int(c), round(float(share.get(n, 0)), 3)) for n, c in cnt.items() if n != '100']
c6 = ('100' not in top10) and any(c >= 3 and s < 0.30 for n, c, s in others)
print('\ntop-10 nests:', dict(cnt), '| A100 in top 10:', '100' in top10, '| C6 holds:', c6)
print('nest shares of all scored deep moonquakes (top 8):', {k: round(float(v), 3) for k, v in share.head(8).items()})

a100 = dm[dm['N2'] == '100']
rank = {i: k + 1 for k, i in enumerate(dm.index)}
print('\nA100 events (1973): rank / score')
for r in a100.itertuples():
    print('  73-%s %s rank %d of %d score %.4f ccs %s' % (r.JD, str(r.S).zfill(4), rank[r.Index], len(dm), r.score, r.peak_ccs))
print('\nmoveout-indistinguishable nests (Nakamura 2005 16S-14S within 5 s of A100): A35, A244, A7')
for n in ('35', '244', '7'):
    for r in dm[dm['N2'] == n].itertuples():
        print('  A%s 73-%s %s rank %d score %.4f ccs %s' % (n, r.JD, str(r.S).zfill(4), rank[r.Index], r.score, r.peak_ccs))

g = dm.groupby('N2')['score']
tab = pd.DataFrame(dict(n=g.size(), median=g.median(), mean=g.mean(), max=g.max()))
tab = tab[tab['n'] >= 3].sort_values('median', ascending=False)
print('\nper-nest median score (nests with >= 3 scored 1973 events; 0 = no peak >= 0.10): top 12')
print(tab.head(12).round(4).to_string())
print('A100 median rank among %d nests: %d' % (len(tab), list(tab.index).index('100') + 1 if '100' in tab.index else -1))

rng = np.random.default_rng(20261113)
allt = np.sort(cat['t'].values.astype(np.int64))
lo = int(day0 + (min(done_days) - 1) * 86400 * NS); hi = int(day0 + max(done_days) * 86400 * NS)
base = []
while len(base) < 3000:
    t = int(rng.integers(lo, hi))
    j = np.searchsorted(allt, t)
    near = min([abs(t - allt[i]) for i in (j - 1, j) if 0 <= i < len(allt)] or [10 ** 18])
    if near < 1800 * NS or abs(t - CAND) < 3600 * NS:
        continue
    base.append(score(t)[0])
base = np.array(base)
print('\nrandom-window baseline (3000 windows): fraction with a peak >= 0.10: %.3f; quantiles 50/90/99/max: %.4f %.4f %.4f %.4f' % (
    np.mean(base > 0), np.quantile(base, 0.5), np.quantile(base, 0.9), np.quantile(base, 0.99), base.max()))
print('top-10 catalogued scores:', [round(x, 4) for x in dm.head(10)['score']])
