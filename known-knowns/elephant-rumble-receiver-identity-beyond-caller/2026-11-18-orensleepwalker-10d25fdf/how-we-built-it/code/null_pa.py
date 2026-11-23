"""1,000 within-caller shuffled reruns of the pa pipeline, folds re-made from the shuffled labels (PREREG.md criterion 3).
Output: output/null_pa/rerun_JJJJ.json."""
import sys, os, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import core
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output', 'null_pa'); D = core.load()

def one(j):
    p = os.path.join(OUT, 'rerun_%04d.json' % j)
    if os.path.exists(p): return
    c = D['caller']; rng = np.random.default_rng([20261118, 1, j])
    y = core.shuffle_within_caller(c, D['recv'], rng); f = core.make_folds(c, y, rng)
    pa, chosen = core.pa_pipeline(D['X'], c, y, f, rng)
    json.dump(dict(rerun=j, acc_pa=float((pa == y).mean()), chosen=[list(x) for x in chosen]), open(p + '.tmp', 'w')); os.replace(p + '.tmp', p)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    with Pool(int(os.environ.get('WORKERS', 4))) as pool: list(pool.imap_unordered(one, range(1000), chunksize=4))
    print('done')
