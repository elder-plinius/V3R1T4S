"""Lead agent's step-5 check (author evidence, not panel evidence). Written from the bank's definitions; does not import code/core.py.
Checks every saved real draw (fold rule, accuracies, habit predictions valid, forest predictions drawn from training receivers),
the null files, and re-runs a DIFFERENT forest implementation (sklearn RandomForestClassifier, bootstrap with replacement,
max_samples 0.6, 500 trees, max_features 6) on 20 of the saved fold draws and on 50 within-caller shuffles."""
import csv, json, glob, os, collections, numpy as np
from sklearn.ensemble import RandomForestClassifier
RUN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
rows = [r for r in csv.DictReader(open(os.path.join(RUN, 'data/20231225_dfall_obs_data_and_spectral_features_revision1_n469.csv'), encoding='utf-8-sig')) if r['Cert_ID_Bin'] == '1']
assert len(rows) == 437
cal = np.array([r['CallerID'] for r in rows], dtype=object); rec = np.array([r['Elicitor1_ID'] for r in rows], dtype=object)
cols = ['sprsMed', 'sprsMbw', 'sprsEqbw', 'sprsMc'] + ['V%d' % i for i in range(1, 75)] + ['%s%d' % (p, i) for p in ('Fw', 'Mw', 'F', 'M') for i in range(1, 5)]
X = np.array([[float(r[c]) for c in cols] for r in rows])
R = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(RUN, 'output/real/draw_*.json')))]; assert len(R) == 100
bad = collections.Counter(); acc = collections.defaultdict(list)
for r in R:
    f = np.array(r['folds']); assert set(f) == set(range(7))
    for key in set(zip(cal, rec)):
        m = (cal == key[0]) & (rec == key[1]); cnt = np.bincount(f[m], minlength=7)
        if cnt.max() - cnt.min() > 1: bad['stratum_unbalanced'] += 1
    for k in ('habit', 'rf', 'pa'):
        p = np.array(r[k], dtype=object); a = (p == rec).mean(); acc[k].append(a)
        if abs(a - r['acc_' + k]) > 1e-12: bad['acc_mismatch_' + k] += 1
    for fo in range(7):
        tr = f != fo
        overall = collections.Counter(rec[tr]); om = max(overall.values())
        for i in np.flatnonzero(f == fo):
            cc = collections.Counter(rec[tr & (cal == cal[i])])
            ok = {x for x, v in cc.items() if v == max(cc.values())} if cc else {x for x, v in overall.items() if v == om}
            if r['habit'][i] not in ok: bad['habit_not_modal'] += 1
            if r['rf'][i] not in set(rec[tr]): bad['rf_label_not_in_training'] += 1
            if cc and r['pa'][i] not in set(cc): bad['pa_outside_caller_receivers'] += 1
print('real draws checked: 100; problems:', dict(bad) or 'none')
print('means recomputed: ' + ', '.join('%s %.6f' % (k, np.mean(v)) for k, v in acc.items()))
NR = [json.load(open(p)) for p in glob.glob(os.path.join(RUN, 'output/null_rf/rerun_*.json'))]
v = np.array([n['acc_rf'] for n in NR]); assert len(v) == 1000 and sorted(n['rerun'] for n in NR) == list(range(1000)) and all(n['fold_draw'] == n['rerun'] % 100 for n in NR)
print('rf null: n %d mean %.6f p99.9 %.6f max %.6f; real rf mean above max: %s' % (len(v), v.mean(), np.percentile(v, 99.9), v.max(), np.mean(acc['rf']) > v.max()))
def forest(y, f, seed):
    p = np.empty(len(y), dtype=object)
    for fo in range(7):
        tr = f != fo; m = RandomForestClassifier(n_estimators=500, max_features=6, max_samples=0.6, n_jobs=4, random_state=seed + fo).fit(X[tr], y[tr]); p[f == fo] = m.predict(X[f == fo])
    return (p == y).mean()
alt = [forest(rec, np.array(R[s]['folds']), 1000 * s) for s in range(20)]
print('different forest implementation on saved folds of draws 0-19: mean %.4f (sd %.4f)' % (np.mean(alt), np.std(alt, ddof=1)))
rng = np.random.default_rng(77); sh = []
for j in range(50):
    y = rec.copy()
    for c in set(cal): idx = np.flatnonzero(cal == c); y[idx] = rec[idx][rng.permutation(len(idx))]
    sh.append(forest(y, np.array(R[j % 100]['folds']), 5000 + j))
print('different forest, 50 within-caller shuffles on saved folds: mean %.4f, max %.4f' % (np.mean(sh), np.max(sh)))
