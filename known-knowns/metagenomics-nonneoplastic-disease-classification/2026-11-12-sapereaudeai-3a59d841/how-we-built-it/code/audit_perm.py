"""Within-study label permutation (PREREG R3/N2): reduced species RF (100 trees), repeat-0 folds, mean fold AUC.
Checkpointed: appends one line per permutation; seed -1 = real labels.
Usage: python -I audit_perm.py <run_dir> <cache_dir> <SETTING> <start> <end> <out_tsv>"""
import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from audit_lib import *
run, cache, name, a, b, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
D, X = load(run, cache)
m = setting_mask(D, name)
Ds = D[m].reset_index(drop=True); Xs = X[m]; y = Ds['y'].values.astype(int); st = Ds['study'].values
F = load_folds(run, name, D, m); f0 = [F['r0'].values]
done = set()
if os.path.exists(out):
    for line in open(out):
        if line.strip() and not line.startswith('seed'): done.add(int(line.split('\t')[0]))
else:
    open(out, 'w').write('seed\tauc_mean_fold\tn_folds\n')
seeds = ([-1] if a == 0 else []) + list(range(a, b))
t0 = time.time()
for sd in seeds:
    if sd in done: continue
    yp = y if sd < 0 else permute_within(y, st, sd)
    A, _ = cv_run(yp, f0, species_fit_predict(Xs, yp, 100))
    with open(out, 'a') as fh:
        fh.write(f'{sd}\t{np.nanmean(A):.6f}\t{int(np.sum(~np.isnan(A)))}\n')
print(name, 'perms', a, b, 'done in', round(time.time() - t0), 's', flush=True)
