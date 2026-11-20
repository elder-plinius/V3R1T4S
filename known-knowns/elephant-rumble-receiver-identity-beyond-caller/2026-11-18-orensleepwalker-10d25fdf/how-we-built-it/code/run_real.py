"""The 100 real fold draws (PREREG.md): habit, rf and pa on the same folds. Output: output/real/draw_SSS.json."""
import sys, os, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import core
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output', 'real'); D = core.load()

def one(s):
    p = os.path.join(OUT, 'draw_%03d.json' % s)
    if os.path.exists(p): return
    c, y = D['caller'], D['recv']; rng = np.random.default_rng([20261118, s])
    f = core.make_folds(c, y, rng); n = len(y)
    hab = np.empty(n, dtype=object); rf = np.empty(n, dtype=object)
    for fo in range(core.K):
        tr = np.flatnonzero(f != fo); te = np.flatnonzero(f == fo)
        hab[te] = core.habit_predict(c, y, tr, te, rng)
    for fo in range(core.K):
        tr = np.flatnonzero(f != fo); te = np.flatnonzero(f == fo)
        rf[te] = core.rf_predict(D['X']['spectral'], y, tr, te, rng)
    pa, chosen = core.pa_pipeline(D['X'], c, y, f, rng)
    r = dict(draw=s, folds=f.tolist(), habit=hab.tolist(), rf=rf.tolist(), pa=pa.tolist(), chosen=[list(x) for x in chosen],
             acc_habit=float((hab == y).mean()), acc_rf=float((rf == y).mean()), acc_pa=float((pa == y).mean()))
    json.dump(r, open(p + '.tmp', 'w')); os.replace(p + '.tmp', p)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    with Pool(int(os.environ.get('WORKERS', 4))) as pool: list(pool.imap_unordered(one, range(100)))
    print('done')
