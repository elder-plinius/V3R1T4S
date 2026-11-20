"""1,000 rf reruns with within-caller shuffled labels on the SAME folds as real draw j mod 100 (PREREG.md, p3).
Output: output/null_rf/rerun_JJJJ.json."""
import sys, os, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import core
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output', 'null_rf'); D = core.load()

def one(j):
    p = os.path.join(OUT, 'rerun_%04d.json' % j)
    if os.path.exists(p): return
    c, y0 = D['caller'], D['recv']
    f = core.make_folds(c, y0, np.random.default_rng([20261118, j % 100]))  # the real draw's folds (its first random use)
    rng = np.random.default_rng([20261118, 2, j]); y = core.shuffle_within_caller(c, y0, rng)
    pred = np.empty(len(y), dtype=object)
    for fo in range(core.K):
        tr = np.flatnonzero(f != fo); te = np.flatnonzero(f == fo)
        pred[te] = core.rf_predict(D['X']['spectral'], y, tr, te, rng)
    json.dump(dict(rerun=j, fold_draw=j % 100, acc_rf=float((pred == y).mean())), open(p + '.tmp', 'w')); os.replace(p + '.tmp', p)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    with Pool(int(os.environ.get('WORKERS', 4))) as pool: list(pool.imap_unordered(one, range(1000)))
    print('done')
