"""PREREG.v2 sensitivity analyses S1-S5. Usage: python -I sensitivity.py <run_dir> <cache_dir> <part> <out_dir> [args]
parts: folds_s1 | s1 | s2 | s3 <SETTING> <start> <end> | s4 | s5 | s6 (PREREG.v4) | s7 (PREREG.v5)"""
import sys, os, json, time, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from audit_lib import *

run, cache, part, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(out, exist_ok=True)
D, X = load(run, cache)

if part == 'folds_s1':
    m = setting_mask(D, 'P2'); sub = D[m]
    F = pd.DataFrame({'sampleID': sub['sampleID'].values, 'dataset_name': sub['dataset_name'].values, 'y': sub['y'].values})
    for r in range(20):
        fold = np.full(len(sub), -1)
        for k, (_, te) in enumerate(StratifiedKFold(10, shuffle=True, random_state=r).split(np.zeros(len(sub)), sub['y'].values)):
            fold[te] = k
        F[f'r{r}'] = fold
    p = os.path.join(run, 'folds', 'folds_P2_ungrouped.csv'); F.to_csv(p, index=False, lineterminator='\n')
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    open(os.path.join(run, 'folds', 'FOLDS_v2.sha256'), 'w').write(f'{h}  folds_P2_ungrouped.csv\n'); print(h)

elif part == 's1':
    m = setting_mask(D, 'P2'); Ds = D[m].reset_index(drop=True); Xs = X[m]; y = Ds['y'].values.astype(int)
    F = pd.read_csv(os.path.join(run, 'folds', 'folds_P2_ungrouped.csv'), dtype={'sampleID': str})
    assert list(F['sampleID']) == list(Ds['sampleID'])
    folds = [F[f'r{r}'].values for r in range(20)]
    A, _ = cv_run(y, folds, species_fit_predict(Xs, y, 500)); s_sp = summarize(A)
    Cdf = cov_frame(Ds, ['study']); A2, _ = cv_run(y, folds, cov_fit_predict(Cdf, y, ['study'], 'lr')); s_st = summarize(A2)
    res = {'species_rf_ungrouped': s_sp, 'study_lr_ungrouped': s_st,
           'frac_study_vs_published': frac(s_st['auc_mean'], PUBLISHED['P2'])}
    json.dump(res, open(os.path.join(out, 's1_ungrouped.json'), 'w'), indent=1); print(json.dumps(res))

elif part == 's2':
    m = setting_mask(D, 'P2'); Ds = D[m].reset_index(drop=True); Xs = X[m]
    st = Ds['study'].astype(str).values; labels = sorted(set(st))
    F = load_folds(run, 'P2', D, m); f = F['r0'].values
    P = np.zeros((len(st), len(labels)))
    for k in range(10):
        te = f == k; tr = ~te
        mdl = rf(500, k); mdl.fit(Xs[tr], st[tr])
        pr = mdl.predict_proba(Xs[te]); cls = list(mdl.classes_)
        for j, lab in enumerate(labels):
            P[te, j] = pr[:, cls.index(lab)] if lab in cls else 0.0
    res = {lab: float(roc_auc_score((st == lab).astype(int), P[:, j])) for j, lab in enumerate(labels)}
    res['accuracy'] = float(np.mean(np.array(labels)[P.argmax(1)] == st))
    json.dump(res, open(os.path.join(out, 's2_study_recognition.json'), 'w'), indent=1); print(json.dumps(res))

elif part == 's3':
    name, a, b = sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
    m = setting_mask(D, name); Ds = D[m].reset_index(drop=True); Xs = np.log10(X[m] / 100.0 + 1e-5)
    y = Ds['y'].values.astype(int); st = Ds['study'].values
    F = load_folds(run, name, D, m); f0 = [F['r0'].values]
    def lin_fp(yv):
        def fp(tr, te, r, k):
            mdl = Pipeline([('sc', StandardScaler()), ('lr', LogisticRegression(C=1.0, max_iter=5000))])
            mdl.fit(Xs[tr], yv[tr]); return mdl.predict_proba(Xs[te])[:, 1]
        return fp
    outp = os.path.join(out, f's3_linear_perm_{name}.tsv')
    done = set()
    if os.path.exists(outp):
        done = {int(l.split('\t')[0]) for l in open(outp) if l.strip() and not l.startswith('seed')}
    else:
        open(outp, 'w').write('seed\tauc_mean_fold\n')
    for sd in ([-1] if a == 0 else []) + list(range(a, b)):
        if sd in done: continue
        yp = y if sd < 0 else permute_within(y, st, sd)
        A, _ = cv_run(yp, f0, lin_fp(yp))
        open(outp, 'a').write(f'{sd}\t{np.nanmean(A):.6f}\n')
    print('s3', name, a, b, 'done')

elif part == 's4':
    m = setting_mask(D, 'P2'); Ds = D[m].reset_index(drop=True); y = Ds['y'].values.astype(int)
    F = load_folds(run, 'P2', D, m)
    keep = Ds['depth_log10'].notna().values
    yk = y[keep]; Ck = cov_frame(Ds[keep].reset_index(drop=True), ['depth'])
    folds = [F[f'r{r}'].values[keep] for r in range(20)]
    def fp(tr, te, r, k):
        mdl = Pipeline([('sc', StandardScaler()), ('lr', LogisticRegression(C=1.0, max_iter=5000))])
        mdl.fit(Ck.iloc[tr][['depth']].values, yk[tr]); return mdl.predict_proba(Ck.iloc[te][['depth']].values)[:, 1]
    A, _ = cv_run(yk, folds, fp); s = summarize(A)
    s['n'] = int(keep.sum()); s['cases'] = int(yk.sum()); s['frac_vs_published'] = frac(s['auc_mean'], PUBLISHED['P2'])
    s['by_dataset_depth_median_log10'] = Ds[keep].groupby('dataset_name')['depth_log10'].median().round(3).to_dict()
    json.dump(s, open(os.path.join(out, 's4_depth_complete_case.json'), 'w'), indent=1); print(json.dumps(s))

elif part == 's5':
    m = setting_mask(D, 'P1'); Ds = D[m].reset_index(drop=True); y = Ds['y'].values.astype(int); st = Ds['study'].values
    O = np.load(os.path.join(run, 'attempts', 'pooled-audit', 'out', 'P1_species_oof.npy'))
    res = {}
    for s_ in sorted(set(st)):
        idx = st == s_
        v = [roc_auc_score(y[idx], O[r][idx]) for r in range(O.shape[0])]
        res[s_] = {'n': int(idx.sum()), 'auc_mean_over_repeats': float(np.mean(v)),
                   'range95': [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]}
    res['pooled_oof_auc_mean'] = float(np.mean([roc_auc_score(y, O[r]) for r in range(O.shape[0])]))
    json.dump(res, open(os.path.join(out, 's5_P1_within_study.json'), 'w'), indent=1); print(json.dumps(res))

elif part == 's6':
    m = setting_mask(D, 'P2'); Ds = D[m].reset_index(drop=True); y = Ds['y'].values.astype(int)
    F = load_folds(run, 'P2', D, m)
    keep = (Ds['age_n'].notna() & Ds['bmi_n'].notna()).values
    yk = y[keep]; Dk = Ds[keep].reset_index(drop=True)
    folds = [F[f'r{r}'].values[keep] for r in range(20)]
    res = {'n': int(keep.sum()), 'cases': int(yk.sum()), 'by_dataset': Dk['dataset_name'].value_counts().to_dict()}
    for name, cols in (('age', ['age_n']), ('bmi', ['bmi_n']), ('age+bmi', ['age_n', 'bmi_n'])):
        V = Dk[cols].astype(float).values
        def fp(tr, te, r, k, V=V):
            mdl = Pipeline([('sc', StandardScaler()), ('lr', LogisticRegression(C=1.0, max_iter=5000))])
            mdl.fit(V[tr], yk[tr]); return mdl.predict_proba(V[te])[:, 1]
        A, _ = cv_run(yk, folds, fp); s_ = summarize(A); s_['frac_vs_published'] = frac(s_['auc_mean'], PUBLISHED['P2'])
        res[name] = s_
        print('s6', name, round(s_['auc_mean'], 4), [round(v, 4) for v in s_['ci95']], flush=True)
    json.dump(res, open(os.path.join(out, 's6_P2_age_bmi_complete_case.json'), 'w'), indent=1)

elif part == 's7':
    from scipy.stats import spearmanr
    res = {}
    for name, col, tol, lens in (('W1', 'age_n', 3.0, 'within-cohort-audit'), ('W2', 'bmi_n', 1.0, 'within-cohort-audit')):
        m = setting_mask(D, name); Ds = D[m].reset_index(drop=True); y = Ds['y'].values.astype(int)
        v = Ds[col].astype(float).values
        O = np.load(os.path.join(run, 'attempts', lens, 'out', f'{name}_species_oof.npy'))
        ci = np.where(y == 1)[0]; cj = np.where(y == 0)[0]
        Mt = np.abs(v[ci][:, None] - v[cj][None, :]) <= tol
        def pauc(sc):
            S = (sc[ci][:, None] > sc[cj][None, :]) + 0.5 * (sc[ci][:, None] == sc[cj][None, :])
            return float(S[Mt].mean())
        a = [pauc(O[r]) for r in range(O.shape[0])]
        res[name] = {'covariate': col, 'tolerance': tol, 'n_matched_pairs': int(Mt.sum()), 'n_all_pairs': int(Mt.size),
                     'species_score_auc_matched_pairs_mean': float(np.mean(a)),
                     'range95': [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))],
                     'raw_covariate_auc_matched_pairs': pauc(v),
                     'species_score_auc_all_pairs_mean': float(np.mean([roc_auc_score(y, O[r]) for r in range(O.shape[0])])),
                     'spearman_score_vs_cov_controls': float(spearmanr(O[0][y == 0], v[y == 0]).statistic),
                     'spearman_score_vs_cov_cases': float(spearmanr(O[0][y == 1], v[y == 1]).statistic)}
        print('s7', name, json.dumps(res[name]), flush=True)
    json.dump(res, open(os.path.join(out, 's7_matched_pairs.json'), 'w'), indent=1)
