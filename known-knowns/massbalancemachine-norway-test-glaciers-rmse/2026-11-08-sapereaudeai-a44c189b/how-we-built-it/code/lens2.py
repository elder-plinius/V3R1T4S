"""Lens 2 (contrarian): attack the p3 reproduction. Usage: python -I lens2.py CLAIM_CODE_DIR DATADIR OUTDIR
1. How close is our retrain to the shipped booster, prediction by prediction (test and train rows)?
2. Determinism: seeds 1-2, nthread 1, tree_method approx/exact.
3. The 9.99 rule's effect; base_score left to xgboost's default (intercept estimated) instead of 0.5.
4. Discrimination: MBM's notebook-2.1.1 grid (depth 3/4/5, lr 0.01/0.1, 100-400 trees): how many within 0.01?
"""
import sys, os, json, time, itertools
import numpy as np, pandas as pd, xgboost as xgb
sys.path.insert(0, sys.argv[1])
import reimpl_p3 as R

DATA, OUT = sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
wide = pd.read_csv(os.path.join(DATA, R.DATA['wide']))
rows, _ = R.build_records(wide)
m = rows['BREID'].isin(R.TEST_BREID)
tr, te = rows[~m].reset_index(drop=True), rows[m].reset_index(drop=True)
res = {}


def sc_of(pred, part=te):
    return R.score(R.aggregate(part['rid'].values, part['season'].values, part['balance'].values, pred))


def line(name, sc):
    ok = R.verdict(sc)[1]
    print(f'{name:48s} {R.fmt(sc)} | within 0.01 of all three: {ok}', flush=True)
    res[name] = {'score': sc, 'within_tol_all': ok}
    return ok


t0 = time.time()
ship = xgb.Booster(); ship.load_model(os.path.join(DATA, R.DATA['booster']))
ours = R.train(tr, 5, 0.05, 300, 0, 4, 'hist')
for part, nm in [(te, 'test'), (tr, 'train')]:
    a, b = R.predict(ours, part), R.predict(ship, part)
    d = np.abs(a.astype(np.float64) - b.astype(np.float64))
    print(f'1. {nm} monthly rows {len(part)}: max |ours - shipped| {d.max():.3e}, mean {d.mean():.3e}, '
          f'bit-identical {bool(np.array_equal(a, b))}', flush=True)
    res[f'1_{nm}_max_abs_diff_vs_shipped'] = float(d.max())
    res[f'1_{nm}_bit_identical_vs_shipped'] = bool(np.array_equal(a, b))
# tree-structure comparison: dump both models as text and compare
da, db = ours.get_dump(), ship.get_dump()
same_trees = sum(1 for x, y in zip(da, db) if x == y)
print(f'1. trees with identical text dump: {same_trees} of {len(db)} (ours {len(da)})', flush=True)
res['1_identical_tree_dumps'] = same_trees

print('2. determinism variants (depth 5, lr 0.05, 300 trees):', flush=True)
for seed, nt, tm in [(1, 4, 'hist'), (2, 4, 'hist'), (0, 1, 'hist'), (0, 4, 'approx'), (0, 4, 'exact')]:
    b = R.train(tr, 5, 0.05, 300, seed, nt, tm)
    line(f'  seed {seed} nthread {nt} tree_method {tm}', sc_of(R.predict(b, te)))

print('3. pitfalls:', flush=True)
rows9, d9 = R.build_records(wide, drop_test_999=False)
te9 = rows9[rows9['BREID'].isin(R.TEST_BREID)].reset_index(drop=True)
line('  keep the 9.99 winter record (test)', sc_of(R.predict(ours, te9), te9))
params = {'max_depth': 5, 'eta': 0.05, 'gamma': 0, 'min_child_weight': 0, 'nthread': 4, 'tree_method': 'hist',
          'seed': 0}
dtr = xgb.DMatrix(tr[R.FEATS].values.astype(np.float32), label=tr['balance'].values)
bd = xgb.train(params, dtr, num_boost_round=300, obj=R.make_objective(tr['rid'].values))
line('  base_score not set (xgboost default)', sc_of(R.predict(bd, te)))

print("4. MBM notebook-2.1.1 grid (max_depth 3/4/5 x lr 0.01/0.1 x 100/200/300/400 trees):", flush=True)
n_ok, grid = 0, []
for depth, lr in itertools.product([3, 4, 5], [0.01, 0.1]):
    b = R.train(tr, depth, lr, 400, 0, 4, 'hist')
    dte = xgb.DMatrix(te[R.FEATS].values.astype(np.float32))
    for n in [100, 200, 300, 400]:
        ok = line(f'  depth {depth} lr {lr} trees {n}', sc_of(b.predict(dte, iteration_range=(0, n))))
        n_ok += ok
        grid.append({'depth': depth, 'lr': lr, 'trees': n, 'within_tol_all': ok})
print(f'4. grid configurations within 0.01 of all three published values: {n_ok} of {len(grid)}', flush=True)
res['4_grid_within_tol'] = n_ok; res['4_grid_size'] = len(grid)
json.dump(res, open(os.path.join(OUT, 'lens2_results.json'), 'w'), indent=1)
print('elapsed s', round(time.time() - t0, 1))
