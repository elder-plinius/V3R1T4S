"""Audit of split v2 from the distance matrix (no phenotype read). Usage: audit_split_v2.py VALUES.npy LABELS.npy split.csv
MYKROBE_LINEAGE.csv.gz run1_split.csv run1_nohub_clusters.csv"""
import sys, numpy as np, pandas as pd
vals_p, labs_p, split_p, myk_p, r1_p, r1c_p = sys.argv[1:7]
V = np.load(vals_p, mmap_mode='r'); L = np.load(labs_p, allow_pickle=True); pos = {str(u): i for i, u in enumerate(L)}
sp = pd.read_csv(split_p); sp['m'] = sp.UNIQUEID.map(pos)
te = np.sort(sp.m[sp.SPLIT == 'test'].values); tr = np.sort(sp.m[sp.SPLIT == 'train'].values); allr = np.sort(sp.m.values)
neg = 0; mins = []; asym = 0
for s in range(0, len(te), 256):
    blk = np.asarray(V[te[s:s + 256]])
    neg += int((blk[:, allr] < 0).sum())
    mins.append(blk[:, tr].min(axis=1))
for s in range(0, len(tr), 512):
    neg += int((np.asarray(V[tr[s:s + 512]])[:, allr] < 0).sum())
mins = np.concatenate(mins)
# symmetry spot check on the TEST x TRAIN block (transpose direction)
colmin = np.full(len(te), 32767, dtype=np.int64)
for s in range(0, len(tr), 512):
    blk = np.asarray(V[tr[s:s + 512]])[:, te]; colmin = np.minimum(colmin, blk.min(axis=0))
print('negative entries in reuse x reuse block', neg)
print('min TRAIN-TEST distance (TEST rows)', int(mins.min()), '(TRAIN rows)', int(colmin.min()), 'pairs <= 12:', int((mins <= 12).sum()), int((colmin <= 12).sum()))
q = np.percentile(mins, [0, 1, 5, 10, 25, 50]); print('nearest-TRAIN distance of TEST isolates percentiles 0/1/5/10/25/50:', q.tolist())
for t in (12, 20, 30, 50, 100): print('  TEST isolates with a TRAIN isolate within', t, 'SNPs:', int((mins <= t).sum()))
cl = sp.groupby('CLUSTER').SPLIT.nunique(); print('clusters under the rule spanning TRAIN and TEST:', int((cl > 1).sum()), 'of', len(cl))
ts = sp[sp.SPLIT == 'test'].groupby('CLUSTER').size(); print('TEST cluster sizes: n', len(ts), 'singletons', int((ts == 1).sum()), 'largest', ts.sort_values(ascending=False).head(5).tolist())
myk = pd.read_csv(myk_p); lab = myk.set_index('UNIQUEID')['MYKROBE_LINEAGE_NAME_2'] if 'MYKROBE_LINEAGE_NAME_2' in myk else None
if lab is not None:
    sp['LIN'] = sp.UNIQUEID.map(lab).fillna('NA').astype(str); sp['MAJOR'] = sp.LIN.str.split('.').str[0]
    print('major lineage by split:'); print(pd.crosstab(sp.MAJOR, sp.SPLIT).to_string())
r1 = pd.read_csv(r1_p).set_index('UNIQUEID').SPLIT; sp['R1'] = sp.UNIQUEID.map(r1)
print('overlap with run-1 split (rows: v2, cols: run 1):'); print(pd.crosstab(sp.SPLIT, sp.R1).to_string())
r1c = pd.read_csv(r1c_p); r1c = r1c[~r1c.HUB].set_index('UNIQUEID').SNP_CLUSTER; sp['R1C'] = sp.UNIQUEID.map(r1c)
x = sp.dropna(subset=['R1C']).groupby('R1C').SPLIT.nunique(); print('run-1 hub-removed 12-SNP clusters spanning v2 TRAIN/TEST:', int((x > 1).sum()))
