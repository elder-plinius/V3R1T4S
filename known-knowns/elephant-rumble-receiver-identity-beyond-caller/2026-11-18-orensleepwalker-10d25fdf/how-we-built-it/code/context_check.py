"""Context check (PREREG.md, reported only): 100 draws with folds stratified by caller x receiver x Context2; habit and pa.
Output: output/context/draw_SSS.json."""
import sys, os, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import core
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output', 'context'); D = core.load()

def one(s):
    p = os.path.join(OUT, 'draw_%03d.json' % s)
    if os.path.exists(p): return
    c, y = D['caller'], D['recv']; rng = np.random.default_rng([20261118, 3, s])
    strat = np.array([a + '|' + b for a, b in zip(y, D['context'])], dtype=object)
    f = core.make_folds(c, strat, rng); hab = np.empty(len(y), dtype=object)
    for fo in range(core.K):
        tr = np.flatnonzero(f != fo); te = np.flatnonzero(f == fo); hab[te] = core.habit_predict(c, y, tr, te, rng)
    pa, chosen = core.pa_pipeline(D['X'], c, y, f, rng)
    json.dump(dict(draw=s, acc_habit=float((hab == y).mean()), acc_pa=float((pa == y).mean()), chosen=[list(x) for x in chosen]), open(p + '.tmp', 'w')); os.replace(p + '.tmp', p)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    with Pool(int(os.environ.get('WORKERS', 4))) as pool: list(pool.imap_unordered(one, range(100)))
    print('done')
