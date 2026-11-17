"""Collect the p3 audit numbers into one machine-readable table (the claim object) and a markdown summary.
Usage: python -I summarize_audit.py <run_dir> <out_csv> <out_md>"""
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd

run, out_csv, out_md = sys.argv[1], sys.argv[2], sys.argv[3]
PUB = {'W1': 0.744, 'W2': 0.762, 'P1': 0.743, 'P2': 0.837}
LOC = {'W1': 'within-cohort-audit', 'W2': 'within-cohort-audit', 'P1': 'pooled-audit', 'P2': 'pooled-audit'}
DESC = {'W1': 'T2D (Qin 2012) within-cohort, 170 T2D / 174 control',
        'W2': 'WT2D (Karlsson 2013) within-cohort, 53 T2D / 43 NGT',
        'P1': 'T2D + WT2D merged, 223 / 217',
        'P2': 'T2D + WT2D + healthy stool controls of cirrhosis, colorectal, HMP, IBD datasets, 223 / 659'}
rows = []
ALT = {'within-cohort-audit': os.path.join('results', 'within-cohort'), 'pooled-audit': os.path.join('results', 'pooled')}


def outdir(lens):
    a = os.path.join(run, 'attempts', lens, 'out')
    return a if os.path.isdir(a) else os.path.join(run, ALT[lens])


def fr(a, ref):
    return (a - 0.5) / (ref - 0.5)


for s in ('W1', 'W2', 'P1', 'P2'):
    p = os.path.join(outdir(LOC[s]), f'{s}_audit.json')
    if not os.path.exists(p):
        continue
    J = json.load(open(p))
    sp = J['species_rf']
    rows.append(dict(setting=s, description=DESC[s], quantity='species RF (paper baseline), reproduced', model='RF500 species',
                     auc=sp['auc_mean'], ci_low=sp['ci95'][0], ci_high=sp['ci95'][1], published_auc=PUB[s],
                     frac_of_published_signal=fr(sp['auc_mean'], PUB[s]), frac_ci_low=fr(sp['ci95'][0], PUB[s]),
                     frac_ci_high=fr(sp['ci95'][1], PUB[s]), n_controls_or_folds=sp['n_folds_scored']))
    for learner, key in (('LR', 'covariate_lr'), ('RF', 'covariate_rf')):
        for cs, c in J[key].items():
            rows.append(dict(setting=s, description=DESC[s], quantity=f'covariates only: {cs}', model=f'{learner} covariates',
                             auc=c['auc_mean'], ci_low=c['ci95'][0], ci_high=c['ci95'][1], published_auc=PUB[s],
                             frac_of_published_signal=fr(c['auc_mean'], PUB[s]), frac_ci_low=fr(c['ci95'][0], PUB[s]),
                             frac_ci_high=fr(c['ci95'][1], PUB[s]), n_controls_or_folds=c['n_folds_scored']))
    if 'pair_decomposition' in J:
        for lab, d in J['pair_decomposition'].items():
            for kind in ('same', 'diff'):
                a = d[f'{kind}_study_pairs_auc_mean']
                rows.append(dict(setting=s, description=DESC[s], quantity=f'pair decomposition {kind}-study pairs ({d["n_" + kind + "_pairs"]} pairs)',
                                 model=lab, auc=a, ci_low=d[f'{kind}_study_pairs_auc_range95'][0],
                                 ci_high=d[f'{kind}_study_pairs_auc_range95'][1], published_auc=PUB[s],
                                 frac_of_published_signal=fr(a, PUB[s]), frac_ci_low=np.nan, frac_ci_high=np.nan,
                                 n_controls_or_folds=20))
    pp = os.path.join(outdir(LOC[s]), f'perm_{s}.tsv')
    if os.path.exists(pp):
        T = pd.read_csv(pp, sep='\t')
        real = T[T.seed == -1].auc_mean_fold
        P = T[T.seed >= 0].auc_mean_fold.values
        if len(P):
            lo, hi = np.percentile(P, [2.5, 97.5])
            rows.append(dict(setting=s, description=DESC[s], quantity=f'within-study label permutation (mean of {len(P)})',
                             model='RF100 species, repeat-0 folds', auc=P.mean(), ci_low=lo, ci_high=hi, published_auc=PUB[s],
                             frac_of_published_signal=fr(P.mean(), PUB[s]), frac_ci_low=fr(lo, PUB[s]), frac_ci_high=fr(hi, PUB[s]),
                             n_controls_or_folds=len(P)))
            rows.append(dict(setting=s, description=DESC[s], quantity='within-study permutation: max control', model='RF100 species, repeat-0 folds',
                             auc=P.max(), ci_low=np.nan, ci_high=np.nan, published_auc=PUB[s], frac_of_published_signal=fr(P.max(), PUB[s]),
                             frac_ci_low=np.nan, frac_ci_high=np.nan, n_controls_or_folds=len(P)))
        if len(real):
            rows.append(dict(setting=s, description=DESC[s], quantity='real labels, same reduced pipeline', model='RF100 species, repeat-0 folds',
                             auc=float(real.iloc[0]), ci_low=np.nan, ci_high=np.nan, published_auc=PUB[s],
                             frac_of_published_signal=fr(float(real.iloc[0]), PUB[s]), frac_ci_low=np.nan, frac_ci_high=np.nan,
                             n_controls_or_folds=1))
n1 = os.path.join(outdir('pooled-audit'), 'null_n1.json')
if os.path.exists(n1):
    J = json.load(open(n1))
    rows.append(dict(setting='P2', description=DESC['P2'], quantity='null N1: study-only LR, repeat-0 folds (real)', model='LR study',
                     auc=J['real'], ci_low=np.nan, ci_high=np.nan, published_auc=PUB['P2'], frac_of_published_signal=fr(J['real'], PUB['P2']),
                     frac_ci_low=np.nan, frac_ci_high=np.nan, n_controls_or_folds=1))
    rows.append(dict(setting='P2', description=DESC['P2'], quantity='null N1: best of 400 study-permuted controls', model='LR study',
                     auc=J['best_control'], ci_low=np.nan, ci_high=np.nan, published_auc=PUB['P2'],
                     frac_of_published_signal=fr(J['best_control'], PUB['P2']), frac_ci_low=np.nan, frac_ci_high=np.nan,
                     n_controls_or_folds=400))
T = pd.DataFrame(rows)
T.to_csv(out_csv, index=False, float_format='%.4f', lineterminator='\n')
with open(out_md, 'w', encoding='utf-8') as f:
    for s in ('W1', 'W2', 'P1', 'P2'):
        sub = T[T.setting == s]
        if not len(sub):
            continue
        f.write(f'\n### {s}: {DESC[s]} (published RF species AUC {PUB[s]})\n\n| quantity | model | AUC | interval | fraction of published signal |\n|---|---|---|---|---|\n')
        for _, r in sub.iterrows():
            iv = '' if pd.isna(r.ci_low) else f'{r.ci_low:.3f}-{r.ci_high:.3f}'
            fi = '' if pd.isna(r.frac_ci_low) else f' ({r.frac_ci_low:.2f} to {r.frac_ci_high:.2f})'
            f.write(f'| {r.quantity} | {r.model} | {r.auc:.4f} | {iv} | {r.frac_of_published_signal:.3f}{fi} |\n')
print(T.to_string(max_colwidth=60))
