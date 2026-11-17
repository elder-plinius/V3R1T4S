"""Per-setting audit: species RF baseline (20x10 CV), covariate-only models, pair decomposition.
Usage: python -I audit_main.py <run_dir> <cache_dir> <SETTING> <out_dir>"""
import sys, os, json, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, sklearn
from audit_lib import *

run, cache, name, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(out, exist_ok=True)
t0 = time.time()
D, X = load(run, cache)
m = setting_mask(D, name)
Ds = D[m].reset_index(drop=True); Xs = X[m]; y = Ds['y'].values.astype(int)
F = load_folds(run, name, D, m)
folds = [F[f'r{r}'].values for r in range(20)]
res = {'setting': name, 'n': int(len(y)), 'cases': int(y.sum()), 'controls': int((1 - y).sum()),
       'published_auc': PUBLISHED[name], 'sklearn': sklearn.__version__, 'numpy': np.__version__}

# species RF baseline (the paper's own model)
A, OOF = cv_run(y, folds, species_fit_predict(Xs, y, 500))
res['species_rf'] = summarize(A)
res['species_rf']['per_fold_auc'] = A.round(6).tolist()
np.save(os.path.join(out, f'{name}_species_oof.npy'), OOF)
print(name, 'species RF', json.dumps({k: v for k, v in res['species_rf'].items() if k != 'per_fold_auc'}), f'{time.time()-t0:.0f}s', flush=True)

pooled = name in ('P1', 'P2')
sets = {'depth': ['depth'], 'age': ['age'], 'bmi': ['bmi'], 'age+bmi': ['age', 'bmi'], 'country': ['country'],
        'study': ['study'],
        'ALL': (['study'] if pooled else []) + ['depth', 'age', 'bmi', 'country'],
        'ALL+sex': (['study'] if pooled else []) + ['depth', 'age', 'bmi', 'country', 'sex']}
res['covariate_lr'] = {}; res['covariate_rf'] = {}
cov_oof = {}
for sname, covs in sets.items():
    Cdf = cov_frame(Ds, covs)
    A, O = cv_run(y, folds, cov_fit_predict(Cdf, y, covs, 'lr'))
    s = summarize(A); s['per_fold_auc'] = A.round(6).tolist()
    s['frac_vs_published'] = frac(s['auc_mean'], PUBLISHED[name])
    s['frac_vs_published_ci'] = [frac(s['ci95'][0], PUBLISHED[name]), frac(s['ci95'][1], PUBLISHED[name])]
    s['frac_vs_reproduced'] = frac(s['auc_mean'], res['species_rf']['auc_mean'])
    s['n_nonmissing'] = {c: int(pd.notna(Cdf[c]).sum()) if c in NUMERIC else int((Cdf[c] != 'missing').sum()) for c in covs}
    res['covariate_lr'][sname] = s; cov_oof[sname] = O
    print(name, 'cov LR', sname, round(s['auc_mean'], 4), [round(v, 4) for v in s['ci95']], 'frac_pub', round(s['frac_vs_published'], 3), flush=True)
for sname in ('study', 'ALL'):
    covs = sets[sname]; Cdf = cov_frame(Ds, covs)
    A, O = cv_run(y, folds, cov_fit_predict(Cdf, y, covs, 'rf'))
    s = summarize(A); s['frac_vs_published'] = frac(s['auc_mean'], PUBLISHED[name])
    s['frac_vs_reproduced'] = frac(s['auc_mean'], res['species_rf']['auc_mean'])
    res['covariate_rf'][sname] = s
    print(name, 'cov RF', sname, round(s['auc_mean'], 4), [round(v, 4) for v in s['ci95']], flush=True)

# pair decomposition (pooled settings): same-study vs different-study (case, control) pairs
def pair_auc(s, y, st, same):
    ci = np.where(y == 1)[0]; cj = np.where(y == 0)[0]
    S = (s[ci][:, None] > s[cj][None, :]) + 0.5 * (s[ci][:, None] == s[cj][None, :])
    M = (st[ci][:, None] == st[cj][None, :]) if same else (st[ci][:, None] != st[cj][None, :])
    return float(S[M].mean()), int(M.sum())
if pooled:
    st = np.asarray(Ds['study'].astype(str).tolist(), dtype=object)  # plain numpy (pandas 3 arrow strings do not broadcast)
    dec = {}
    for label, O in [('species_rf', OOF), ('cov_lr_study', cov_oof['study']), ('cov_lr_ALL', cov_oof['ALL'])]:
        same = [pair_auc(O[r], y, st, True) for r in range(20)]; diff = [pair_auc(O[r], y, st, False) for r in range(20)]
        allp = [pair_auc(O[r], y, st, True)[1] + pair_auc(O[r], y, st, False)[1] for r in range(1)]
        dec[label] = {'same_study_pairs_auc_mean': float(np.mean([a for a, _ in same])),
                      'same_study_pairs_auc_range95': [float(np.percentile([a for a, _ in same], 2.5)), float(np.percentile([a for a, _ in same], 97.5))],
                      'diff_study_pairs_auc_mean': float(np.mean([a for a, _ in diff])),
                      'diff_study_pairs_auc_range95': [float(np.percentile([a for a, _ in diff], 2.5)), float(np.percentile([a for a, _ in diff], 97.5))],
                      'n_same_pairs': same[0][1], 'n_diff_pairs': diff[0][1],
                      'pooled_oof_auc_mean': float(np.mean([roc_auc_score(y, O[r]) for r in range(20)]))}
        print(name, 'decomp', label, json.dumps(dec[label]), flush=True)
    res['pair_decomposition'] = dec
res['seconds'] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(out, f'{name}_audit.json'), 'w'), indent=1)
print(name, 'done', res['seconds'], 's')
