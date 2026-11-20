"""Summarise the frozen outputs against PREREG.md. Writes output/summary.json and prints a text summary."""
import json, glob, os, collections, numpy as np
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
L = lambda d: [json.load(open(p)) for p in sorted(glob.glob(os.path.join(B, d, '*.json')))]
R, C, NP, NR = L('real'), L('context'), L('null_pa'), L('null_rf')
assert (len(R), len(C), len(NP), len(NR)) == (100, 100, 1000, 1000)
y = np.array(R[0]['habit'], dtype=object)  # placeholder for shape only
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import core
D = core.load(); recv = D['recv']; caller = D['caller']
acc = {k: np.array([r['acc_' + k] for r in R]) for k in ('habit', 'rf', 'pa')}
# recompute accuracies from the stored per-call predictions (consistency check)
for k in acc:
    re = np.array([(np.array(r[k], dtype=object) == recv).mean() for r in R]); assert np.allclose(re, acc[k])
diff = acc['pa'] - acc['habit']
npa = np.array([n['acc_pa'] for n in NP]); nrf = np.array([n['acc_rf'] for n in NR])
p999 = lambda a: float(np.percentile(a, 99.9))
# calls whose caller has 2+ receivers in its training folds, and disagreement pa vs habit
multi_ok = {k: [] for k in acc}; differ = []
for r in R:
    f = np.array(r['folds'])
    for fo in range(core.K):
        tr = np.flatnonzero(f != fo); te = np.flatnonzero(f == fo)
        nrec = {c: len(set(recv[tr][caller[tr] == c])) for c in set(caller[te])}
        m = np.array([nrec[caller[i]] >= 2 for i in te])
        for k in acc:
            p = np.array(r[k], dtype=object)[te]; multi_ok[k].append(((p == recv[te]) & m).sum() / max(m.sum(), 1) if m.any() else np.nan)
    differ.append(float((np.array(r['pa'], dtype=object) != np.array(r['habit'], dtype=object)).mean()))
S = dict(
    n_calls=len(recv), draws=len(R),
    mean={k: float(v.mean()) for k, v in acc.items()}, sd={k: float(v.std(ddof=1)) for k, v in acc.items()},
    pa_minus_habit=dict(mean=float(diff.mean()), min=float(diff.min()), max=float(diff.max()), draws_pa_better=int((diff > 0).sum())),
    null_pa=dict(n=len(npa), mean=float(npa.mean()), p99_9=p999(npa), max=float(npa.max())),
    null_rf=dict(n=len(nrf), mean=float(nrf.mean()), sd=float(nrf.std(ddof=1)), p99_9=p999(nrf), max=float(nrf.max())),
    context=dict(habit=float(np.mean([c['acc_habit'] for c in C])), pa=float(np.mean([c['acc_pa'] for c in C]))),
    multi_receiver_callers_accuracy={k: float(np.nanmean(v)) for k, v in multi_ok.items()},
    share_calls_pa_differs_from_habit=float(np.mean(differ)),
    chosen_top=[[list(k), v] for k, v in collections.Counter(tuple(c) for r in R for c in r['chosen']).most_common(10)],
)
full = dict(c1=S['mean']['pa'] > 0.295, c2=S['pa_minus_habit']['mean'] >= 0.02, c3=S['mean']['pa'] > S['null_pa']['p99_9'])
p3 = dict(within_0_02_of_0_275=abs(S['mean']['rf'] - 0.275) <= 0.02,
          paper_0_275_exceeds_habit=0.275 > S['mean']['habit'], rf_mean_exceeds_habit=S['mean']['rf'] > S['mean']['habit'],
          paper_0_275_exceeds_null_p99_9=0.275 > S['null_rf']['p99_9'], rf_mean_exceeds_null_p99_9=S['mean']['rf'] > S['null_rf']['p99_9'],
          rf_mean_exceeds_all_1000_controls=S['mean']['rf'] > S['null_rf']['max'])
S['full_win_criteria'] = full; S['full_win'] = all(full.values()); S['p3'] = p3
json.dump(S, open(os.path.join(B, 'summary.json'), 'w'), indent=1)
print(json.dumps(S, indent=1))
