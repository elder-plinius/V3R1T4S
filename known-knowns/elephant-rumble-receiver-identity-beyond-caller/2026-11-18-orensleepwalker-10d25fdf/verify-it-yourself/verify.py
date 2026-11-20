"""Standalone checker for the p3 package (Python standard library only), written from the definitions in the bank entry.
Usage: python3 verify-it-yourself/verify.py <package folder>
Checks, from object/calls.csv and the saved per-call predictions:
- 437 calls; every one of the 100 real draws has 7 folds stratified by caller x receiver (fold counts of a stratum differ by at most 1);
- every habit prediction is a most frequent receiver of the call's caller in the training folds (an overall most frequent one if the
  caller is absent from training); every forest prediction is a receiver present in the training folds;
- the accuracies, recomputed from predictions and labels, equal the saved ones; their means equal object/summary.json;
- 1,000 shuffle controls with ids 0-999, each on the folds of draw (id mod 100); mean, 99.9th percentile (linear interpolation) and maximum
  equal object/summary.json;
- partial win p3: |rf mean - 0.275| <= 0.02; the statements about 0.275 vs the habit mean and vs the 99.9th percentile.
Prints one line per check and exits non-zero on any failure."""
import sys, os, csv, json, collections
P = sys.argv[1]; bad = []
def check(ok, msg):
    print(('ok    ' if ok else 'FAIL  ') + msg)
    if not ok: bad.append(msg)
calls = list(csv.DictReader(open(os.path.join(P, 'object/calls.csv'), encoding='utf-8')))
cal = [r['CallerID'] for r in calls]; rec = [r['Elicitor1_ID'] for r in calls]; n = len(calls)
check(n == 437, 'call list has 437 calls (%d)' % n)
S = json.load(open(os.path.join(P, 'object/summary.json')))
d = os.path.join(P, 'object/real-draws'); names = sorted(os.listdir(d))
check(names == ['draw_%03d.json' % s for s in range(100)], '100 real draws, draw_000 to draw_099')
acc = {'habit': [], 'rf': []}; strat_bad = habit_bad = rf_bad = acc_bad = 0
strata = collections.defaultdict(list)
for i in range(n): strata[(cal[i], rec[i])].append(i)
for name in names:
    R = json.load(open(os.path.join(d, name))); f = R['folds']
    if sorted(set(f)) != list(range(7)) or len(f) != n: strat_bad += 1; continue
    for idx in strata.values():
        cnt = [0] * 7
        for i in idx: cnt[f[i]] += 1
        if max(cnt) - min(cnt) > 1: strat_bad += 1
    for k in acc:
        a = sum(R[k][i] == rec[i] for i in range(n)) / n; acc[k].append(a)
        if abs(a - R['acc_' + k]) > 1e-12: acc_bad += 1
    for fo in range(7):
        tr = [i for i in range(n) if f[i] != fo]; overall = collections.Counter(rec[i] for i in tr); om = max(overall.values())
        trrec = set(rec[i] for i in tr); byc = collections.defaultdict(collections.Counter)
        for i in tr: byc[cal[i]][rec[i]] += 1
        for i in range(n):
            if f[i] != fo: continue
            cc = byc.get(cal[i])
            ok = {r for r, v in cc.items() if v == max(cc.values())} if cc else {r for r, v in overall.items() if v == om}
            habit_bad += R['habit'][i] not in ok; rf_bad += R['rf'][i] not in trrec
check(strat_bad == 0, 'folds stratified by caller x receiver in every draw (%d problems)' % strat_bad)
check(habit_bad == 0, 'every habit prediction follows the caller-habit rule (%d problems)' % habit_bad)
check(rf_bad == 0, 'every forest prediction is a receiver present in the training folds (%d problems)' % rf_bad)
check(acc_bad == 0, 'saved accuracies equal the recomputed ones (%d problems)' % acc_bad)
mean = {k: sum(v) / len(v) for k, v in acc.items()}
for k in mean: check(abs(mean[k] - S['mean'][k]) < 1e-12, '%s mean %.6f equals summary' % (k, mean[k]))
ctrl = [json.loads(l) for l in open(os.path.join(P, 'object/null-rf-controls.jsonl'))]
check(sorted(c['rerun'] for c in ctrl) == list(range(1000)) and all(c['fold_draw'] == c['rerun'] % 100 for c in ctrl), '1,000 controls, ids 0-999, folds of draw id mod 100')
v = sorted(c['acc_rf'] for c in ctrl); pos = 0.999 * (len(v) - 1); lo = int(pos)
p999 = v[lo] + (v[min(lo + 1, len(v) - 1)] - v[lo]) * (pos - lo); m = sum(v) / len(v)
for name, a, b in (('mean', m, S['null_rf']['mean']), ('99.9th percentile', p999, S['null_rf']['p99_9']), ('maximum', v[-1], S['null_rf']['max'])):
    check(abs(a - b) < 1e-12, 'control %s %.6f equals summary' % (name, a))
check(abs(mean['rf'] - 0.275) <= 0.02, 'p3: |rf mean - 0.275| = %.4f <= 0.02' % abs(mean['rf'] - 0.275))
check(not (0.275 > mean['habit']), 'p3 statement: 0.275 does not exceed the caller-habit baseline %.4f' % mean['habit'])
check(0.275 > p999 and mean['rf'] > p999, 'p3 statement: 0.275 and the rf mean %.4f exceed the shuffle 99.9th percentile %.4f' % (mean['rf'], p999))
sys.exit(1 if bad else 0)
