"""Cluster-aware split v2 (V3R1T4S run 2026-11-10-1136). Reads genotype distances only; no phenotype is read.
Rule (fixed before this script was run):
 1. Isolates = the 12,287 rows of CRyPTIC_reuse_table_20240917.csv. Distances = GPI_SNP_DISTANCES_VALUES.npy as released
    by CRyPTIC (labels GPI_SNP_DISTANCES_LABELS.npy). A reuse isolate absent from the matrix goes to TRAIN.
 2. Two isolates are linked if their SNP distance is <= 12 (the 12-SNP threshold of Walker et al. 2013, Lancet Infect
    Dis 13:137-146). Clusters = connected components of that graph (single linkage), with no hub removal, so no
    TRAIN isolate is within 12 SNPs of any TEST isolate.
 3. Components with more than 614 isolates (5% of 12,287) go to TRAIN whole.
 4. The other components are ordered by sha256('V3R1T4S-cryptic-split-v2|' + smallest UNIQUEID in the component) and
    go whole to TEST in that order until TEST first holds >= 3,072 isolates (25%); the rest go to TRAIN. One salt.
Usage: make_split_v2.py VALUES.npy LABELS.npy reuse.csv out_split.csv"""
import sys, hashlib, numpy as np, pandas as pd
vals_p, labs_p, reuse_p, out_p = sys.argv[1:5]
TH, BIG, FRAC = 12, 614, 0.25
V = np.load(vals_p, mmap_mode='r'); L = np.load(labs_p, allow_pickle=True)
print('matrix', V.shape, V.dtype, 'labels', len(L))
reuse = pd.read_csv(reuse_p, usecols=['UNIQUEID'])
pos = {str(u): i for i, u in enumerate(L)}
ids = reuse.UNIQUEID.astype(str).tolist(); n = len(ids)
present = np.array([u in pos for u in ids]); print('reuse isolates', n, 'in matrix', int(present.sum()))
midx = np.array([pos[u] for u in ids if u in pos]); loc = np.flatnonzero(present)   # matrix index, reuse index
inv = -np.ones(V.shape[0], dtype=np.int64); inv[midx] = loc
order = np.argsort(midx); sm = midx[order]
parent = np.arange(n)
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]; a = parent[a]
    return a
B = 256; nedge = 0; vmax = 0
for s in range(0, len(sm), B):
    rows = np.asarray(V[sm[s:s + B]])[:, midx]          # rows: reuse isolates (matrix order), cols: reuse isolates
    vmax = max(vmax, int(rows.max()))
    ii, jj = np.nonzero(rows <= TH)
    for a, b in zip(loc[order[s + ii]], loc[jj]):
        if a != b:
            nedge += 1; ra, rb = find(a), find(b)
            if ra != rb: parent[ra] = rb
    del rows
comp = np.array([find(i) for i in range(n)])
df = pd.DataFrame({'UNIQUEID': ids, 'COMP': comp, 'IN_MATRIX': present})
sizes = df.groupby('COMP').size()
key = df.groupby('COMP').UNIQUEID.min()
print('directed edges', nedge, 'max distance seen', vmax, 'components', len(sizes), 'singletons', int((sizes == 1).sum()),
      'largest', sizes.sort_values(ascending=False).head(5).to_dict())
h = {c: hashlib.sha256(('V3R1T4S-cryptic-split-v2|' + key[c]).encode()).hexdigest() for c in sizes.index}
test = set(); ntest = 0; target = int(np.ceil(FRAC * n))
for c in sorted(sizes.index, key=lambda c: h[c]):
    if sizes[c] > BIG or ntest >= target: continue
    test.add(c); ntest += int(sizes[c])
big = [c for c in sizes.index if sizes[c] > BIG]
df.loc[~df.IN_MATRIX, 'COMP'] = -1
df['CLUSTER'] = ['C' + key[c] if c >= 0 else 'NOMATRIX' for c in df.COMP]
df['SPLIT'] = np.where(df.COMP.isin(list(test)), 'test', 'train')
print('big components to TRAIN', [(key[c], int(sizes[c])) for c in big])
print('TEST isolates', int((df.SPLIT == 'test').sum()), 'TRAIN isolates', int((df.SPLIT == 'train').sum()),
      'TEST clusters', len(test), 'TRAIN clusters', int(len(sizes) - len(test)))
df[['UNIQUEID', 'CLUSTER', 'SPLIT']].to_csv(out_p, index=False, lineterminator='\n')
