"""Shared audit machinery (frozen protocol of PREREG.md). Import with the run's code/ dir on sys.path."""
import os, sys, json, time
import numpy as np, pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import roc_auc_score

NJOBS = int(os.environ.get("V3_NJOBS", "4"))  # thread count only; results do not depend on it
SETTINGS = ('W1', 'W2', 'P1', 'P2')
PUBLISHED = {'W1': 0.744, 'W2': 0.762, 'P1': 0.743, 'P2': 0.837}
NUMERIC = {'depth': 'depth_log10', 'age': 'age_n', 'bmi': 'bmi_n'}
CATEG = {'country': 'country_c', 'study': 'study', 'sex': 'sex_c'}


def load(run, cache):
    D = pd.read_csv(os.path.join(cache, 'samples.tsv'), sep='\t', dtype={'pubmedid': str, 'study': str, 'sampleID': str})
    X = np.load(os.path.join(cache, 'X_species.npy'))
    return D, X


def setting_mask(D, name):
    w1 = D['setting_w1'].astype(bool).values; w2 = D['setting_w2'].astype(bool).values
    return {'W1': w1, 'W2': w2, 'P1': w1 | w2, 'P2': np.ones(len(D), bool)}[name]


def load_folds(run, name, D, mask):
    F = pd.read_csv(os.path.join(run, 'folds', f'folds_{name}.csv'), dtype={'sampleID': str})
    assert list(F['sampleID']) == list(D.loc[mask, 'sampleID']), 'fold file order mismatch'
    return F


def rf(n_estimators, seed):
    return RandomForestClassifier(n_estimators=n_estimators, max_features='sqrt', criterion='gini',
                                  random_state=seed, n_jobs=NJOBS)


def cov_frame(Ds, covs):
    cols = {}
    for c in covs:
        if c in NUMERIC: cols[c] = Ds[NUMERIC[c]].astype(float).values
        else: cols[c] = Ds[CATEG[c]].astype(str).values
    return pd.DataFrame(cols)


def cov_model(covs, learner='lr', seed=0):
    num = [c for c in covs if c in NUMERIC]; cat = [c for c in covs if c in CATEG]
    tr = []
    if num:
        tr.append(('num', Pipeline([('imp', SimpleImputer(strategy='median', add_indicator=True)),
                                    ('sc', StandardScaler())]), num))
    if cat:
        tr.append(('cat', OneHotEncoder(handle_unknown='ignore'), cat))
    ct = ColumnTransformer(tr)
    clf = LogisticRegression(C=1.0, max_iter=5000) if learner == 'lr' else rf(500, seed)
    return Pipeline([('ct', ct), ('clf', clf)])


def fold_auc(y, s):
    if len(np.unique(y)) < 2: return np.nan
    return roc_auc_score(y, s)


def cv_run(y, fold_cols, fit_predict, repeats=None):
    """fit_predict(train_idx, test_idx, r, k) -> scores for test. Returns per-fold AUC matrix (R x 10) and OOF scores (R x n)."""
    R = len(fold_cols) if repeats is None else repeats
    A = np.full((R, 10), np.nan); OOF = np.full((R, len(y)), np.nan)
    for r in range(R):
        f = fold_cols[r]
        for k in range(10):
            te = np.where(f == k)[0]; tr = np.where(f != k)[0]
            s = fit_predict(tr, te, r, k)
            OOF[r, te] = s
            A[r, k] = fold_auc(y[te], s)
    return A, OOF


def summarize(A):
    R = A.shape[0]
    mean = float(np.nanmean(A))
    rep_means = np.nanmean(A, axis=1)
    se = np.nanstd(A, axis=1, ddof=1) / np.sqrt(np.sum(~np.isnan(A), axis=1))
    margin = float(stats.t.ppf(0.975, 9) * np.nanmean(se)) if A.shape[1] > 1 else float('nan')
    out = {'auc_mean': mean, 'margin95': margin, 'ci95': [mean - margin, mean + margin], 'repeats': R,
           'rep_mean_range95': [float(np.percentile(rep_means, 2.5)), float(np.percentile(rep_means, 97.5))],
           'n_folds_scored': int(np.sum(~np.isnan(A)))}
    return out


def frac(auc, ref):
    return (auc - 0.5) / (ref - 0.5)


def species_fit_predict(X, y, n_estimators):
    def fp(tr, te, r, k):
        m = rf(n_estimators, 1000 * r + k)
        m.fit(X[tr], y[tr])
        return m.predict_proba(X[te])[:, 1]
    return fp


def cov_fit_predict(Cdf, y, covs, learner):
    def fp(tr, te, r, k):
        m = cov_model(covs, learner, seed=1000 * r + k)
        m.fit(Cdf.iloc[tr], y[tr])
        return m.predict_proba(Cdf.iloc[te])[:, 1]
    return fp


def permute_within(y, groups, seed):
    rng = np.random.default_rng(seed)
    yp = y.copy()
    for g in np.unique(groups):
        idx = np.where(groups == g)[0]
        yp[idx] = y[rng.permutation(idx)]
    return yp
