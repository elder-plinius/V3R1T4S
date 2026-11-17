"""Independent re-implementation of MassBalanceMachine's Norway test RMSEs (bank partial win p3).

V3R1T4S run 2026-11-08-1729. Own code: record building from the shipped wide CSV, the train/test split by BREID, the
one test cleaning rule of notebook 2.1.1, the aggregated-MSE objective, the training call and the scorer. Shared:
the xgboost library and MBM's selected hyperparameters. Imports nothing from the ML_MB_Norway repository and never
loads its pickle files.

Usage (from any directory; DATADIR holds the files listed in DATA below):
  python -I reimpl_p3.py DATADIR OUTDIR                      primary run (prints P3_PASS: yes|no)
  python -I reimpl_p3.py DATADIR OUTDIR --tag T --depth D --lr L --rounds N --seed S --nthread K --tree_method M
                         [--keep999] [--quick]               variants (lens 2); --quick skips checks (a)-(f)
"""
import argparse, csv, hashlib, json, math, os, sys
import numpy as np
import pandas as pd
import xgboost as xgb

DATA = {
    'wide': '2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf.csv',
    'test_monthly': '2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv',
    'booster': 'custom_loss_best_model.json',
}
SHA256 = {
    'wide': '43597e76ed7356850869605859d6a379a6efd44ffa5d02d74f4038ed4da1a61b',
    'test_monthly': 'd1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c',
    'booster': 'a7ddf96b2f11a51dd8415fbe6190f95671c23123526e200533fb09aae74e1d0d',
}
# notebook 2.1.1: "test_glaciers = [54, 703, 941, 1135, 1280, 2085, 2320, 2478, 2768, 2769, 3133, 3137, 3138, 3141]"
TEST_BREID = [54, 703, 941, 1135, 1280, 2085, 2320, 2478, 2768, 2769, 3133, 3137, 3138, 3141]
STATIC = ['altitude_diff', 'aspect', 'slope', 'skyview_factor']
CLIM = ['t2m', 'sshf', 'slhf', 'ssrd', 'fal', 'str', 'tp']
FEATS = STATIC + CLIM  # MBM's 11 features, in the shipped test CSV's column order
MONTHS = {'annual': ['oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep'],
          'winter': ['oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr'],
          'summer': ['may', 'jun', 'jul', 'aug', 'sep']}
BAL = {'annual': 'balance_netto', 'winter': 'balance_winter', 'summer': 'balance_summer'}
NMONTHS_TO_SEASON = {12: 'annual', 7: 'winter', 5: 'summer'}
# notebook 3.1.1 cell 36 output: Ba RMSE=1.00 Count=1065; Bw RMSE=0.59 Count=999; Bs RMSE=0.70 Count=1028
PUBLISHED = {'annual': (1.00, 1065), 'winter': (0.59, 999), 'summer': (0.70, 1028)}
TOL = 0.01
SEASONS = ['annual', 'winter', 'summer']


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def build_records(wide, drop_test_999=True):
    """One row per (stake record, month). Record ids: summer records first, then winter, then annual."""
    wide = wide.copy()
    wide['altitude_diff'] = wide['altitude_climate'] - wide['altitude']
    is_test = wide['BREID'].isin(TEST_BREID)
    parts, rid0, dropped = [], 0, 0
    for season in ['summer', 'winter', 'annual']:
        keep = wide[BAL[season]].notna()
        if season == 'winter' and drop_test_999:
            # notebook 2.1.1 cell 5: "# Remove strange value" (test winter set only)
            bad = is_test & (wide['balance_winter'] == 9.99)
            dropped = int(bad.sum())
            keep &= ~bad
        s = wide[keep].reset_index(drop=True)
        n = len(s)
        for m in MONTHS[season]:
            r = pd.DataFrame({'rid': np.arange(rid0, rid0 + n), 'season': season, 'BREID': s['BREID'].values,
                              'balance': s[BAL[season]].values.astype(float)})
            for c in STATIC:
                r[c] = s[c].values
            for v in CLIM:
                r[v] = s[f'{v}_{m}'].values
            parts.append(r)
        rid0 += n
    return pd.concat(parts, ignore_index=True), dropped


def make_objective(rid):
    """Loss 0.5*(sum of a record's monthly predictions - record balance)^2; grad broadcast to months; hess 1."""
    uniq, inv = np.unique(rid, return_inverse=True)

    def objective(pred, dtrain):
        y = dtrain.get_label()
        rec_sum = np.bincount(inv, weights=pred, minlength=len(uniq))
        rec_y = np.zeros(len(uniq))
        rec_y[inv] = y
        grad = (rec_sum - rec_y)[inv]
        return grad, np.ones_like(pred)
    return objective


def train(train_rows, depth, lr, rounds, seed, nthread, tree_method):
    params = {'max_depth': depth, 'eta': lr, 'gamma': 0, 'min_child_weight': 0, 'subsample': 1.0,
              'colsample_bytree': 1.0, 'lambda': 1, 'base_score': 0.5, 'seed': seed, 'nthread': nthread,
              'tree_method': tree_method}
    d = xgb.DMatrix(train_rows[FEATS].values.astype(np.float32), label=train_rows['balance'].values)
    return xgb.train(params, d, num_boost_round=rounds, obj=make_objective(train_rows['rid'].values))


def predict(booster, rows):
    return booster.predict(xgb.DMatrix(rows[FEATS].values.astype(np.float32)))


def aggregate(rid, season, y, pred):
    df = pd.DataFrame({'rid': rid, 'season': season, 'y': y, 'p': np.asarray(pred, dtype=float)})
    g = df.groupby('rid', sort=True)
    return pd.DataFrame({'season': g['season'].first(), 'y': g['y'].first(), 'yhat': g['p'].sum()}).reset_index()


def score(rec):
    out = {}
    for s in SEASONS:
        r = rec[rec['season'] == s]
        out[s] = {'rmse': float(np.sqrt(np.mean((r['yhat'] - r['y']) ** 2))), 'n': int(len(r))}
    return out


def verdict(sc):
    ok = {s: abs(sc[s]['rmse'] - PUBLISHED[s][0]) <= TOL and sc[s]['n'] == PUBLISHED[s][1] for s in SEASONS}
    return ok, all(ok.values())


def pure_python_score(path):
    """Second scorer, standard library only, on the saved record-level predictions."""
    acc = {s: [0.0, 0] for s in SEASONS}
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            e = float(row['yhat']) - float(row['y'])
            acc[row['season']][0] += e * e
            acc[row['season']][1] += 1
    return {s: {'rmse': math.sqrt(acc[s][0] / acc[s][1]), 'n': acc[s][1]} for s in SEASONS}


def fmt(sc):
    return ' / '.join(f"{s} {sc[s]['rmse']:.4f} (n={sc[s]['n']})" for s in SEASONS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('datadir'); ap.add_argument('outdir')
    ap.add_argument('--tag', default='primary'); ap.add_argument('--depth', type=int, default=5)
    ap.add_argument('--lr', type=float, default=0.05); ap.add_argument('--rounds', type=int, default=300)
    ap.add_argument('--seed', type=int, default=0); ap.add_argument('--nthread', type=int, default=4)
    ap.add_argument('--tree_method', default='hist'); ap.add_argument('--keep999', action='store_true')
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    paths = {k: os.path.join(a.datadir, v) for k, v in DATA.items()}
    res = {'tag': a.tag, 'config': vars(a).copy(), 'xgboost': xgb.__version__}
    res['config'].pop('datadir'); res['config'].pop('outdir')
    for k, p in paths.items():
        h = sha256(p)
        assert h == SHA256[k], f'{k}: sha256 {h} != {SHA256[k]}'
    print('inputs: sha256 match for', ', '.join(DATA.values()))
    print('xgboost', xgb.__version__, '| config', res['config'])

    wide = pd.read_csv(paths['wide'])
    rows, dropped = build_records(wide, drop_test_999=not a.keep999)
    te_mask = rows['BREID'].isin(TEST_BREID)
    tr, te = rows[~te_mask].reset_index(drop=True), rows[te_mask].reset_index(drop=True)
    assert not tr['BREID'].isin(TEST_BREID).any()
    ntr = tr.groupby('season')['rid'].nunique().to_dict()
    nte = te.groupby('season')['rid'].nunique().to_dict()
    print(f"wide rows {len(wide)}, glaciers {wide['BREID'].nunique()}; train glaciers {tr['BREID'].nunique()}, "
          f"test glaciers {te['BREID'].nunique()}; test winter records dropped by the 9.99 rule: {dropped}")
    print('train records', ntr, '| test records', nte, '| test monthly rows', len(te))
    res.update({'train_records': ntr, 'test_records': nte, 'test_monthly_rows': int(len(te)), 'dropped_999': dropped,
                'train_999_winter': int(((wide['balance_winter'] == 9.99) & ~wide['BREID'].isin(TEST_BREID)).sum())})

    bst = train(tr, a.depth, a.lr, a.rounds, a.seed, a.nthread, a.tree_method)
    p = predict(bst, te)
    rec = aggregate(te['rid'].values, te['season'].values, te['balance'].values, p)
    sc = score(rec)
    ok, passed = verdict(sc)
    res.update({'score': sc, 'within_tol': ok, 'pass': passed})
    print('OUR MODEL on OUR test records:', fmt(sc))
    for s in SEASONS:
        print(f"  {s}: RMSE {sc[s]['rmse']:.4f} published {PUBLISHED[s][0]:.2f} |diff| "
              f"{abs(sc[s]['rmse'] - PUBLISHED[s][0]):.4f} <= {TOL}: {ok[s]}; n {sc[s]['n']} == {PUBLISHED[s][1]}")

    if not a.quick:
        bst.save_model(os.path.join(a.outdir, f'model_{a.tag}.json'))
        rec_path = os.path.join(a.outdir, f'test_record_predictions_{a.tag}.csv')
        rec.to_csv(rec_path, index=False, float_format='%.17g')
        # (a) targets equal the shipped monthly test CSV's records
        st = pd.read_csv(paths['test_monthly'], index_col=0)
        cols = [c for c in st.columns if c in FEATS]
        assert cols == FEATS, cols
        st_season = st['n_months'].map(NMONTHS_TO_SEASON)
        st_rec = st.assign(season=st_season).groupby('id').agg(season=('season', 'first'), y=('balance', 'mean'))
        same = {}
        for s in SEASONS:
            t1 = np.sort(st_rec[st_rec['season'] == s]['y'].values)
            t2 = np.sort(rec[rec['season'] == s]['y'].values)
            same[s] = bool(len(t1) == len(t2) and np.allclose(t1, t2))
        res['a_targets_equal_shipped_test_csv'] = same
        print('(a) record targets equal the shipped test CSV per season:', same, '| shipped monthly rows', len(st))
        # (b) the shipped booster through the same scorer on our records
        ship = xgb.Booster(); ship.load_model(paths['booster'])
        sc_b = score(aggregate(te['rid'].values, te['season'].values, te['balance'].values, predict(ship, te)))
        res['b_shipped_booster_on_our_records'] = sc_b
        print('(b) shipped MBM booster, our records, our scorer:', fmt(sc_b), '| within tol:', verdict(sc_b)[1])
        # (c) our model on the shipped monthly test CSV
        sc_c = score(aggregate(st['id'].values, st_season.values, st['balance'].values, predict(bst, st)))
        res['c_our_model_on_shipped_test_csv'] = sc_c
        maxdiff = max(abs(sc_c[s]['rmse'] - sc[s]['rmse']) for s in SEASONS)
        print('(c) our model on the shipped monthly test CSV:', fmt(sc_c), f'| max |diff| vs primary {maxdiff:.2e}')
        # (d) determinism: a second identical fit
        p2 = predict(train(tr, a.depth, a.lr, a.rounds, a.seed, a.nthread, a.tree_method), te)
        res['d_bit_identical_refit'] = bool(np.array_equal(p, p2))
        print('(d) second identical fit gives bit-identical predictions:', res['d_bit_identical_refit'])
        # (e) known negatives
        z = rec.assign(yhat=0.0)
        rng = np.random.default_rng(20261108)
        sh = rec.copy()
        for s in SEASONS:
            m = sh['season'] == s
            sh.loc[m, 'yhat'] = rng.permutation(sh.loc[m, 'yhat'].values)
        sc_z, sc_s = score(z), score(sh)
        res['e_negative_zero'] = sc_z; res['e_negative_shuffled'] = sc_s
        res['e_negatives_fail'] = (not verdict(sc_z)[1]) and (not verdict(sc_s)[1])
        print('(e) zero prediction:', fmt(sc_z), '| pass?', verdict(sc_z)[1])
        print('    record-shuffled predictions:', fmt(sc_s), '| pass?', verdict(sc_s)[1])
        # (f) pure-Python scorer on the saved record predictions
        sc_f = pure_python_score(rec_path)
        res['f_pure_python_score'] = sc_f
        fd = max(abs(sc_f[s]['rmse'] - sc[s]['rmse']) for s in SEASONS)
        res['f_agree_1e-9'] = bool(fd <= 1e-9 and all(sc_f[s]['n'] == sc[s]['n'] for s in SEASONS))
        print('(f) pure-Python scorer on', os.path.basename(rec_path), ':', fmt(sc_f), f'| max |diff| {fd:.1e}')
        res['record_predictions_sha256'] = sha256(rec_path)
        res['model_sha256'] = sha256(os.path.join(a.outdir, f'model_{a.tag}.json'))
    with open(os.path.join(a.outdir, f'result_{a.tag}.json'), 'w') as f:
        json.dump(res, f, indent=1)
    print('P3_PASS:', 'yes' if passed else 'no')


if __name__ == '__main__':
    main()
