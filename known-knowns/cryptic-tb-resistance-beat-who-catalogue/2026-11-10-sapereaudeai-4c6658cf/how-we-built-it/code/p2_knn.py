"""p2 leakage test (PREREG.md, run 2026-11-10-1136; REPAIRED: the <= 5% test is done in integers, see ../REPAIR.md): genome-wide kNN on the released SNP distances.
Score of a test isolate = distance-weighted R fraction of its k = 10 nearest training isolates (among isolates with a
HIGH-filter R/S phenotype for the drug; ties by matrix index), w = 1/(1+d). Metric: sensitivity at >= 95% specificity
(threshold from the test negatives), average precision alongside.
Real = split v2 (split/split.csv). Controls = random isolate-level splits with the same TEST size (seeds 1..N).
Alternative cluster-aware splits = the split-v2 rule with salts 'V3R1T4S-cryptic-split-v2-alt-<i>'.
Usage: p2_knn.py VALUES.npy LABELS.npy RUN_DIR DRUG N_RANDOM N_ALT OUT_CSV"""
import warnings; warnings.filterwarnings("ignore")
import sys, os, hashlib, time
import numpy as np, pandas as pd
from sklearn.metrics import average_precision_score
vals_p, labs_p, RUN, DRUG, NR, NA, OUT = sys.argv[1:8]; NR, NA = int(NR), int(NA)
K = 10
t0 = time.time()
V = np.load(vals_p, mmap_mode='r'); L = np.load(labs_p, allow_pickle=True); pos = {str(u): i for i, u in enumerate(L)}
reuse = pd.read_csv(os.path.join(RUN, 'data', 'CRyPTIC_reuse_table_20240917.csv'), low_memory=False)
split = pd.read_csv(os.path.join(RUN, 'split', 'split.csv'))
allids = split.UNIQUEID.tolist(); N = len(allids)
ok = reuse[(reuse[DRUG + '_PHENOTYPE_QUALITY'] == 'HIGH') & reuse[DRUG + '_BINARY_PHENOTYPE'].isin(['R', 'S'])]
ok = ok.assign(m=ok.UNIQUEID.map(pos)).dropna(subset=['m']).sort_values('m')
m = ok.m.astype(int).values; y = (ok[DRUG + '_BINARY_PHENOTYPE'] == 'R').values; uid = ok.UNIQUEID.values; n = len(m)
D = np.empty((n, n), dtype=np.int16)
for s in range(0, n, 512):
    D[s:s + 512] = np.asarray(V[m[s:s + 512]])[:, m]
del V; import gc; gc.collect()   # release the memory map (working-set cap)
print('drug', DRUG, 'phenotyped isolates', n, 'R', int(y.sum()), 'load s %.1f' % (time.time() - t0)); sys.stdout.flush()
col = np.arange(n, dtype=np.int64)
TESTN = int((split.SPLIT == 'test').sum())


def metric(test):
    """test: bool over the n phenotyped isolates."""
    tr = np.flatnonzero(~test); te = np.flatnonzero(test)
    if len(te) == 0 or y[te].sum() == 0 or (~y[te]).sum() == 0:
        return None
    sc = np.empty(len(te))
    for s in range(0, len(te), 512):
        blk = D[te[s:s + 512]][:, tr].astype(np.int64) * n + col[tr]       # unique keys: (distance, matrix order)
        nn = np.argpartition(blk, K - 1, axis=1)[:, :K]
        d = np.take_along_axis(blk, nn, axis=1) // n
        w = 1.0 / (1.0 + d); r = y[tr][nn]
        sc[s:s + 512] = (w * r).sum(1) / w.sum(1)
    yt = y[te]; neg = np.sort(sc[~yt]); pos_ = sc[yt]
    cand = np.unique(np.concatenate([sc, [np.inf]]))
    nge = len(neg) - np.searchsorted(neg, cand, side='left')               # number of negatives with score >= t
    t = cand[np.argmax(20 * nge <= len(neg))]                              # exact integer form of nge/len(neg) <= 0.05 (repair)
    sens = float((pos_ >= t).mean()); spec = float((neg < t).mean())
    return dict(sens95=sens, spec_at_t=spec, threshold=float(t), ap=float(average_precision_score(yt, sc)),
                n_test=int(len(te)), R_test=int(yt.sum()))


ph = pd.Series(np.arange(n), index=uid)
def mask_from_ids(test_ids):
    msk = np.zeros(n, bool); idx = ph.reindex(list(set(test_ids) & set(uid))).values; msk[idx.astype(int)] = True
    return msk


rows = []
real = metric(mask_from_ids(split.UNIQUEID[split.SPLIT == 'test']))
rows.append(dict(kind='real_split_v2', seed='', **real)); print('real', real); sys.stdout.flush()
for s in range(1, NR + 1):
    r = np.random.default_rng(s); te_ids = [allids[i] for i in r.choice(N, TESTN, replace=False)]
    rows.append(dict(kind='random', seed=s, **metric(mask_from_ids(te_ids))))
    if s % 50 == 0:
        print('random', s, 'elapsed %.0f s' % (time.time() - t0)); sys.stdout.flush()
sizes = split.groupby('CLUSTER').size(); key = {c: c[1:] for c in sizes.index}
for a in range(1, NA + 1):
    salt = 'V3R1T4S-cryptic-split-v2-alt-%d|' % a
    order = sorted(sizes.index, key=lambda c: hashlib.sha256((salt + key[c]).encode()).hexdigest())
    test = set(); nt = 0
    for c in order:
        if sizes[c] > 614 or nt >= TESTN - 1:   # same rule: stop once TEST holds >= 3,072 isolates
            continue
        test.add(c); nt += int(sizes[c])
    te_ids = split.UNIQUEID[split.CLUSTER.isin(test)]
    res = metric(mask_from_ids(te_ids))
    if res: rows.append(dict(kind='alt_cluster_aware', seed=a, **res))
df = pd.DataFrame(rows); df.to_csv(OUT, index=False, lineterminator='\n')
rnd = df[df.kind == 'random'].sens95; alt = df[df.kind == 'alt_cluster_aware'].sens95
print('drug', DRUG, 'real sens95 %.4f' % real['sens95'], 'AP %.4f' % real['ap'])
print('random n', len(rnd), 'min %.4f mean %.4f max %.4f' % (rnd.min(), rnd.mean(), rnd.max()),
      'AP mean %.4f' % df[df.kind == 'random'].ap.mean(), 'controls_above_real', int((rnd > real['sens95']).sum()))
if len(alt):
    print('alt cluster-aware n', len(alt), 'min %.4f mean %.4f max %.4f' % (alt.min(), alt.mean(), alt.max()),
          'AP mean %.4f' % df[df.kind == 'alt_cluster_aware'].ap.mean())
print('real_beats_all_controls', 'yes' if (rnd > real['sens95']).all() else 'no', 'margin_mean_minus_real %.4f' % (rnd.mean() - real['sens95']),
      'elapsed %.0f s' % (time.time() - t0))
