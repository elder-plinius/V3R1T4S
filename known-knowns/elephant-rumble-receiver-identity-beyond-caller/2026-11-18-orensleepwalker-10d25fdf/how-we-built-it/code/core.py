"""Elephant receiver-identity pipeline (Andy, 2026-11-18). Shared by every program in this run.

Data: the 437 calls with Cert_ID_Bin == 1 from the Dryad n469 revision files (data/).
Folds: 7 folds stratified by caller x receiver: for each (caller, receiver) stratum, in sorted order, its calls are shuffled
and dealt round-robin to folds starting from a random fold.
Models:
  habit  - the bank's caller-habit baseline (most frequent receiver of the call's caller in the training folds,
           ties broken at random, overall most frequent receiver as the fallback; overall ties broken at random too).
  rf     - the paper's random forest re-implemented: 500 trees, 6 features tried per split, leaves of size 1,
           no depth limit, each tree grown on 60% of the training calls drawn WITHOUT replacement; majority vote,
           ties broken at random. Features: the paper's 94 spectral features. Caller ID is not an input.
  prior+acoustic (the full-win pipeline 'pa') - see score_pa().
"""
import os, numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
SPEC = '20231225_dfall_obs_data_and_spectral_features_revision1_n469.csv'
CEPS = '20240106_dfall_obs_data_and_cepstral_features_revision1_n469.csv'
K = 7


def feats(n_pca):
    return ['sprsMed', 'sprsMbw', 'sprsEqbw', 'sprsMc'] + [f'V{i}' for i in range(1, n_pca + 1)] + \
           [f'{p}{i}' for p in ('Fw', 'Mw', 'F', 'M') for i in range(1, 5)]


def load():
    s = pd.read_csv(os.path.join(DATA, SPEC)); c = pd.read_csv(os.path.join(DATA, CEPS))
    s = s[s.Cert_ID_Bin == 1].reset_index(drop=True); c = c[c.Cert_ID_Bin == 1].reset_index(drop=True)
    assert len(s) == 437 and (s.soundID.values == c.soundID.values).all()
    callers = s.CallerID.astype(str).values; recv = s.Elicitor1_ID.astype(str).values
    Xs = s[feats(74)].to_numpy(float); Xc = c[feats(12)].to_numpy(float)
    assert not np.isnan(Xs).any() and not np.isnan(Xc).any()
    return dict(caller=callers, recv=recv, X={'spectral': Xs, 'cepstral': Xc}, context=s.Context2.astype(str).values,
                soundID=s.soundID.astype(str).values)


def make_folds(caller, recv, rng, k=K):
    f = np.zeros(len(caller), int); strata = {}
    for i, key in enumerate(zip(caller, recv)): strata.setdefault(key, []).append(i)
    for key in sorted(strata):
        idx = list(strata[key]); rng.shuffle(idx); s = int(rng.integers(k))
        for j, i in enumerate(idx): f[i] = (s + j) % k
    return f


def shuffle_within_caller(caller, recv, rng):
    out = recv.copy()
    for c in sorted(set(caller)):
        idx = np.flatnonzero(caller == c); out[idx] = recv[idx][rng.permutation(len(idx))]
    return out


def _pick(rng, labels):
    return labels[int(rng.integers(len(labels)))] if len(labels) > 1 else labels[0]


def habit_predict(caller, recv, tr, te, rng):
    from collections import Counter
    overall = Counter(recv[tr]); top = max(overall.values()); og = sorted(r for r, v in overall.items() if v == top)
    byc = {}
    for i in tr: byc.setdefault(caller[i], Counter())[recv[i]] += 1
    pred = []
    for i in te:
        cc = byc.get(caller[i])
        if cc:
            m = max(cc.values()); pred.append(_pick(rng, sorted(r for r, v in cc.items() if v == m)))
        else:
            pred.append(_pick(rng, og))
    return np.array(pred, dtype=object)


def rf_predict(X, recv, tr, te, rng, n_trees=500, mtry=6, frac=0.6):
    classes, y = np.unique(recv[tr], return_inverse=True)
    n = len(tr); m = int(frac * n)  # ranger truncates num_samples * sample.fraction
    votes = np.zeros((len(te), len(classes)))
    Xtr, Xte = X[tr], X[te]
    for _ in range(n_trees):
        sub = rng.choice(n, m, replace=False)
        t = DecisionTreeClassifier(max_features=mtry, min_samples_leaf=1, random_state=int(rng.integers(2**31 - 1)))
        t.fit(Xtr[sub], y[sub])
        votes[np.arange(len(te)), t.predict(Xte).astype(int)] += 1  # labels are global class indices
    pred = []
    for v in votes:
        best = np.flatnonzero(v == v.max()); pred.append(classes[best[int(rng.integers(len(best)))]] if len(best) > 1 else classes[best[0]])
    return np.array(pred, dtype=object)


# ---------------- full-win pipeline: caller-habit prior plus a within-caller acoustic term ----------------
LAMBDAS = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0)
FAMILIES = ('nn', 'centroid')
FEATSETS = ('spectral', 'cepstral')


def _acoustic(Z, caller, recv, tr, i, cands, family):
    """Within-caller acoustic term for test call i: for each candidate receiver r, minus the distance (in training-fold
    z-scores, divided by sqrt(#features)) from call i to the caller's training calls addressed to r: the nearest one
    ('nn') or their mean ('centroid')."""
    out = []
    for r in cands:
        idx = tr[(caller[tr] == caller[i]) & (recv[tr] == r)]
        if family == 'nn':
            d = np.sqrt(((Z[idx] - Z[i]) ** 2).mean(axis=1)).min()
        else:
            d = np.sqrt(((Z[idx].mean(axis=0) - Z[i]) ** 2).mean())
        out.append(-d)
    return np.array(out)


def pa_predict_all(Xd, caller, recv, tr, te, rng):
    """Predictions of every (featset, family, lambda) combination for the test calls te, trained on tr.
    Score(r) = log(1 + n_cr) + lambda * acoustic(r) over the receivers r the caller addressed in tr; lambda = 0 is the
    caller-habit baseline (same ties, same fallback). Returns {(fs, fam, lam): array of predicted receivers}."""
    from collections import Counter
    overall = Counter(recv[tr]); top = max(overall.values()); og = sorted(r for r, v in overall.items() if v == top)
    byc = {}
    for j in tr: byc.setdefault(caller[j], Counter())[recv[j]] += 1
    Zs = {}
    for fs in FEATSETS:
        X = Xd[fs]; mu = X[tr].mean(axis=0); sd = X[tr].std(axis=0); sd[sd == 0] = 1.0; Zs[fs] = (X - mu) / sd
    keys = [(fs, fam, lam) for fs in FEATSETS for fam in FAMILIES for lam in LAMBDAS]
    out = {k: [] for k in keys}
    for i in te:
        cc = byc.get(caller[i])
        u = rng.random(64)  # one set of tie-break draws per call, shared by all combinations
        if not cc:
            p = og[int(u[0] * len(og))]
            for k in keys: out[k].append(p)
            continue
        cands = sorted(cc); prior = np.log1p(np.array([cc[r] for r in cands], float))
        if len(cands) == 1:
            for k in keys: out[k].append(cands[0])
            continue
        for fs in FEATSETS:
            for fam in FAMILIES:
                a = _acoustic(Zs[fs], caller, recv, tr, i, cands, fam)
                for lam in LAMBDAS:
                    s = prior + lam * a; best = np.flatnonzero(np.isclose(s, s.max(), rtol=0, atol=1e-12))
                    out[(fs, fam, lam)].append(cands[best[int(u[1] * len(best))]])
    return {k: np.array(v, dtype=object) for k, v in out.items()}


def pa_pipeline(Xd, caller, recv, folds, rng):
    """Nested selection: for each outer fold, the combination is chosen by leave-one-fold-out over the six training
    folds (accuracy summed over inner test calls; ties go to the smaller lambda, then the order of FEATSETS and FAMILIES).
    Returns (outer predictions, list of chosen combinations per outer fold)."""
    n = len(caller); pred = np.empty(n, dtype=object); chosen = []
    keys = [(fs, fam, lam) for fs in FEATSETS for fam in FAMILIES for lam in LAMBDAS]
    for fo in range(K):
        tr_folds = [g for g in range(K) if g != fo]
        score = {k: 0 for k in keys}
        for gi in tr_folds:
            itr = np.flatnonzero((folds != fo) & (folds != gi)); ite = np.flatnonzero(folds == gi)
            P = pa_predict_all(Xd, caller, recv, itr, ite, rng)
            for k in keys: score[k] += int((P[k] == recv[ite]).sum())
        order = sorted(keys, key=lambda k: (-score[k], k[2], FEATSETS.index(k[0]), FAMILIES.index(k[1])))
        best = order[0]; chosen.append(best)
        tr = np.flatnonzero(folds != fo); te = np.flatnonzero(folds == fo)
        pred[te] = pa_predict_all(Xd, caller, recv, tr, te, rng)[best]
    return pred, chosen
