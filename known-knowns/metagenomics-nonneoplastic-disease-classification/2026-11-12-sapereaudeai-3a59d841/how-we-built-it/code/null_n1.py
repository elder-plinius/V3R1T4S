"""Null N1 (PREREG): P2, study-of-origin-only LR, repeat-0 folds; 400 controls with the study column permuted across samples.
Usage: python -I null_n1.py <run_dir> <cache_dir> <out_dir>"""
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from audit_lib import *
run, cache, out = sys.argv[1], sys.argv[2], sys.argv[3]
D, X = load(run, cache)
m = setting_mask(D, 'P2')
Ds = D[m].reset_index(drop=True); y = Ds['y'].values.astype(int)
F = load_folds(run, 'P2', D, m); f0 = [F['r0'].values]
def score(study_col):
    Cdf = pd.DataFrame({'study': study_col})
    A, _ = cv_run(y, f0, cov_fit_predict(Cdf, y, ['study'], 'lr'))
    return float(np.nanmean(A))
real = score(Ds['study'].astype(str).values)
ctrl = []
for sd in range(400):
    rng = np.random.default_rng(sd)
    ctrl.append(score(rng.permutation(Ds['study'].astype(str).values)))
ctrl = np.array(ctrl)
res = {'controls': 400, 'best_control': float(ctrl.max()), 'real': real, 'real_beats_all_controls': bool(real > ctrl.max()),
       'control_mean': float(ctrl.mean()), 'control_p2.5_p97.5': [float(np.percentile(ctrl, 2.5)), float(np.percentile(ctrl, 97.5))]}
json.dump(res, open(os.path.join(out, 'null_n1.json'), 'w'), indent=1)
np.savetxt(os.path.join(out, 'null_n1_controls.txt'), ctrl, fmt='%.6f')
print(json.dumps(res))
