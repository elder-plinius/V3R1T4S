"""Independent AUC checker (pair counting, standard library only) + known positive/negative tests.
Usage: python -I check_auc.py [oof.npy folds.csv]  (with args: cross-check fold AUCs of repeat 0 against sklearn values)"""
import sys
def auc(y, s):
    pos = [v for v, t in zip(s, y) if t == 1]; neg = [v for v, t in zip(s, y) if t == 0]
    if not pos or not neg: return float('nan')
    w = 0.0
    for p in pos:
        for n in neg:
            w += 1.0 if p > n else (0.5 if p == n else 0.0)
    return w / (len(pos) * len(neg))
assert auc([1, 1, 0, 0], [0.9, 0.8, 0.2, 0.1]) == 1.0, 'known positive failed'
assert auc([1, 1, 0, 0], [0.5, 0.5, 0.5, 0.5]) == 0.5, 'known negative failed'
assert auc([1, 0, 1, 0], [0.1, 0.9, 0.2, 0.8]) == 0.0
print('checker tests: PASS (perfect=1.0, constant=0.5, reversed=0.0)')
if len(sys.argv) > 2:
    import numpy as np, pandas as pd, json
    O = np.load(sys.argv[1]); F = pd.read_csv(sys.argv[2], dtype={'sampleID': str})
    js = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
    y = F['y'].values; f = F['r0'].values
    mine = [auc(list(y[f == k]), list(O[0][f == k])) for k in range(10)]
    print('repeat-0 fold AUCs (independent):', [round(a, 6) for a in mine])
    if js:
        ref = js['species_rf']['per_fold_auc'][0]
        print('max abs diff vs saved per-fold AUCs:', max(abs(a - b) for a, b in zip(mine, ref)))
