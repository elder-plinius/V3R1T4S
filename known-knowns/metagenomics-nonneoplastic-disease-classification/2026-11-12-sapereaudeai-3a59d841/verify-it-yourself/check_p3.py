"""Standalone checker for the p3 confound audit (Python 3 standard library only). Run from the package folder.

Definition checked (bank p3): "quantify how much of the published AUC is recoverable from sequencing-depth,
study-of-origin, age/BMI/country covariates alone (and from label permutation within study) ... documenting the
fraction of apparent signal that is cohort structure." Fraction = (AUC - 0.5) / (published AUC - 0.5).

Checks:
1. object/audit_results.csv has the sha256 recorded below (a corrupted copy fails).
2. Single-covariate AUCs recomputed from scratch from verify-it-yourself/data/covariates_P2.csv and the committed fold
   files: for a logistic regression on one standardised covariate, the fitted score is monotone in the covariate with
   the sign of the training-fold covariance, so each test-fold AUC equals the covariate's own AUC (or 1 - AUC).
   Recomputed: W1 age, W1 depth, W1 BMI, W2 BMI, W2 depth, P1 age, P1 depth. Each must equal the object value to 1e-4.
3. Study-of-origin-only AUC in P2 recomputed with the training-fold case fraction of each study as the score; must
   equal the object value to 0.005 (the logistic model's L2 shrinkage can reorder near-equal studies).
4. Within-study permutation summaries (mean, max, real beats all 400) recomputed from the saved permutation files;
   null N1 (study-only real vs 400 study-permuted controls) recomputed from its saved controls.
5. Fractions of published signal recomputed for the headline rows.
Last line: PASS or FAIL.
"""
import bisect
import csv
import hashlib
import os
import sys

OBJ = 'object/audit_results.csv'
EXPECT_SHA = '3a59d8419b0ec3f809e9b8f51d0447624da7f34e454d46c6a603ef6b0a57af89'
PUB = {'W1': 0.744, 'W2': 0.762, 'P1': 0.743, 'P2': 0.837}
D = os.path.join('verify-it-yourself', 'data')
fails = []


def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        fails.append(msg)


def auc(y, s):
    pos = sorted(v for v, t in zip(s, y) if t == 1)
    neg = sorted(v for v, t in zip(s, y) if t == 0)
    if not pos or not neg:
        return None
    w = 0.0
    for p in pos:
        lo = bisect.bisect_left(neg, p)
        hi = bisect.bisect_right(neg, p)
        w += lo + 0.5 * (hi - lo)
    return w / (len(pos) * len(neg))


assert auc([1, 1, 0, 0], [3, 2, 1, 0]) == 1.0 and auc([1, 0], [1, 1]) == 0.5 and auc([1, 0], [0, 1]) == 0.0

h = hashlib.sha256(open(OBJ, 'rb').read()).hexdigest()
ok(h == EXPECT_SHA, 'object sha256 %s' % h)
obj = list(csv.DictReader(open(OBJ, encoding='utf-8')))


def objval(setting, quantity, model):
    for r in obj:
        if r['setting'] == setting and r['quantity'] == quantity and r['model'] == model:
            return float(r['auc'])
    raise KeyError((setting, quantity, model))


cov = {r['sampleID']: r for r in csv.DictReader(open(os.path.join(D, 'covariates_P2.csv'), encoding='utf-8'))}


def folds(name):
    return list(csv.DictReader(open(os.path.join(D, 'folds_%s.csv' % name), encoding='utf-8')))


def num(v):
    return float(v) if v not in ('', 'nan', 'NaN') else None


def mono_auc(name, col):
    rows = folds(name)
    ids = [r['sampleID'] for r in rows]
    y = [int(r['y']) for r in rows]
    x = [num(cov[i][col]) for i in ids]
    assert all(v is not None for v in x), 'missing values in %s %s' % (name, col)
    tot, n = 0.0, 0
    for rep in range(20):
        f = [int(r['r%d' % rep]) for r in rows]
        for k in range(10):
            tr = [i for i in range(len(y)) if f[i] != k]
            te = [i for i in range(len(y)) if f[i] == k]
            n1 = sum(1 for i in tr if y[i] == 1)
            n0 = sum(1 for i in tr if y[i] == 0)
            m1 = sum(x[i] for i in tr if y[i] == 1) / n1
            m0 = sum(x[i] for i in tr if y[i] == 0) / n0
            sgn = 1.0 if m1 > m0 else (-1.0 if m1 < m0 else 0.0)
            tot += auc([y[i] for i in te], [sgn * x[i] for i in te])
            n += 1
    return tot / n


CHECKS = [('W1', 'age', 'age'), ('W1', 'depth_log10_reads', 'depth'), ('W1', 'bmi', 'bmi'),
          ('W2', 'bmi', 'bmi'), ('W2', 'depth_log10_reads', 'depth'),
          ('P1', 'age', 'age'), ('P1', 'depth_log10_reads', 'depth')]
for name, col, q in CHECKS:
    mine = mono_auc(name, col)
    theirs = objval(name, 'covariates only: %s' % q, 'LR covariates')
    ok(abs(mine - theirs) < 1e-4, '%s %s-only AUC recomputed %.4f vs object %.4f (fraction of published %.3f)'
       % (name, q, mine, theirs, (mine - 0.5) / (PUB[name] - 0.5)))

# 3. study-only in P2 by the training-fold case fraction of each study
rows = folds('P2')
ids = [r['sampleID'] for r in rows]
y = [int(r['y']) for r in rows]
st = [cov[i]['study_pubmed'] for i in ids]
tot, n = 0.0, 0
for rep in range(20):
    f = [int(r['r%d' % rep]) for r in rows]
    for k in range(10):
        tr = [i for i in range(len(y)) if f[i] != k]
        te = [i for i in range(len(y)) if f[i] == k]
        rate = {}
        for s in set(st[i] for i in tr):
            idx = [i for i in tr if st[i] == s]
            rate[s] = sum(y[i] for i in idx) / len(idx)
        tot += auc([y[i] for i in te], [rate.get(st[i], 0.0) for i in te])
        n += 1
mine = tot / n
theirs = objval('P2', 'covariates only: study', 'LR covariates')
ok(abs(mine - theirs) < 0.005, 'P2 study-only AUC (training case-fraction score) %.4f vs object %.4f; fraction of published: %.3f'
   % (mine, theirs, (mine - 0.5) / (PUB['P2'] - 0.5)))

# 4. permutations and null
PERM_Q = 'within-study label permutation (mean of 400)'
PERM_M = 'RF100 species, repeat-0 folds'
for name in ('W1', 'W2', 'P1', 'P2'):
    T = list(csv.DictReader(open(os.path.join(D, 'perm_%s.tsv' % name), encoding='utf-8'), delimiter='\t'))
    real = [float(r['auc_mean_fold']) for r in T if int(r['seed']) == -1][0]
    P = [float(r['auc_mean_fold']) for r in T if int(r['seed']) >= 0]
    seeds = set(int(r['seed']) for r in T if int(r['seed']) >= 0)
    ok(len(P) == 400 and len(seeds) == 400, '%s: 400 distinct permutation seeds' % name)
    mean = sum(P) / len(P)
    ok(abs(mean - objval(name, PERM_Q, PERM_M)) < 1e-4,
       '%s within-study permutation mean %.4f (fraction of published %.3f), max %.4f, real %.4f'
       % (name, mean, (mean - 0.5) / (PUB[name] - 0.5), max(P), real))
    ok(real > max(P), '%s real labels beat all 400 within-study permutations' % name)
ctrl = [float(l) for l in open(os.path.join(D, 'null_n1_controls.txt')) if l.strip()]
realn = objval('P2', 'null N1: study-only LR, repeat-0 folds (real)', 'LR study')
ok(len(ctrl) == 400 and realn > max(ctrl), 'null N1: real %.4f vs best of %d controls %.4f' % (realn, len(ctrl), max(ctrl)))

# 5. headline fractions from the object
HEAD = [('W1', 'covariates only: age', 0.961), ('W2', 'covariates only: ALL', 0.698),
        ('P1', 'covariates only: ALL', 0.869), ('P2', 'covariates only: study', 1.010)]
for s, q, exp in HEAD:
    a = objval(s, q, 'LR covariates')
    fr = (a - 0.5) / (PUB[s] - 0.5)
    ok(abs(fr - exp) < 0.002, '%s %s: AUC %.4f, fraction %.3f' % (s, q, a, fr))

print('PASS' if not fails else 'FAIL')
sys.exit(0 if not fails else 1)
