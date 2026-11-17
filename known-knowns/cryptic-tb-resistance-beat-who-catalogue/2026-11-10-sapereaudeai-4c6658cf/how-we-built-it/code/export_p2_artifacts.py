"""Release files for p2: (1) the 400 random isolate-level control splits as TEST row indices into split/split.csv
(regenerated with the same numpy calls as p2_knn.py: default_rng(seed).choice(12287, 3073, replace=False), seeds
1..400); (2) per-isolate 10-NN scores and calls on the split-v2 TEST part for ETH (same scoring as p2_knn.py).
Usage: export_p2_artifacts.py VALUES.npy LABELS.npy RUN_DIR OUT_DIR"""
import sys, os, numpy as np, pandas as pd
vals_p, labs_p, RUN, OUT = sys.argv[1:5]; os.makedirs(OUT, exist_ok=True)
split = pd.read_csv(os.path.join(RUN, 'split', 'split.csv')); N = len(split); TESTN = int((split.SPLIT == 'test').sum())
idx = np.stack([np.sort(np.random.default_rng(s).choice(N, TESTN, replace=False)) for s in range(1, 401)]).astype(np.int16)
np.savez_compressed(os.path.join(OUT, 'random_control_splits_test_rows.npz'), test_rows=idx, seeds=np.arange(1, 401))
V = np.load(vals_p, mmap_mode='r'); L = np.load(labs_p, allow_pickle=True); pos = {str(u): i for i, u in enumerate(L)}
reuse = pd.read_csv(os.path.join(RUN, 'data', 'CRyPTIC_reuse_table_20240917.csv'), low_memory=False)
ok = reuse[(reuse.ETH_PHENOTYPE_QUALITY == 'HIGH') & reuse.ETH_BINARY_PHENOTYPE.isin(['R', 'S'])]
ok = ok.assign(m=ok.UNIQUEID.map(pos)).dropna(subset=['m']).sort_values('m')
m = ok.m.astype(int).values; y = (ok.ETH_BINARY_PHENOTYPE == 'R').values; uid = ok.UNIQUEID.values; n = len(m)
test = split.set_index('UNIQUEID').SPLIT.reindex(uid).values == 'test'
tr = np.flatnonzero(~test); te = np.flatnonzero(test); col = np.arange(n, dtype=np.int64)
sc = np.empty(len(te)); nn1 = np.empty(len(te), dtype=np.int64)
for s in range(0, len(te), 512):
    blk = np.asarray(V[m[te[s:s + 512]]])[:, m[tr]].astype(np.int64) * n + col[tr]
    nn = np.argpartition(blk, 9, axis=1)[:, :10]; d = np.take_along_axis(blk, nn, axis=1) // n
    w = 1.0 / (1.0 + d); sc[s:s + 512] = (w * y[tr][nn]).sum(1) / w.sum(1); nn1[s:s + 512] = d.min(1)
yt = y[te]; neg = np.sort(sc[~yt]); cand = np.unique(np.concatenate([sc, [np.inf]]))
t = cand[np.argmax(20 * (len(neg) - np.searchsorted(neg, cand, side='left')) <= len(neg))]   # integer form (repair)
pd.DataFrame(dict(UNIQUEID=uid[te], ETH_PHENOTYPE=np.where(yt, 'R', 'S'), KNN10_SCORE=sc, CALL=np.where(sc >= t, 'R', 'notR'),
                  NEAREST_TRAIN_DISTANCE=nn1)).to_csv(os.path.join(OUT, 'predictions_ETH_knn10_split_v2_test.csv'), index=False, lineterminator='\n')
print('threshold', t, 'sens95', float((sc[yt] >= t).mean()), 'spec', float((sc[~yt] < t).mean()), 'n_test', len(te), 'R', int(yt.sum()),
      'nearest TRAIN distance min', int(nn1.min()))
