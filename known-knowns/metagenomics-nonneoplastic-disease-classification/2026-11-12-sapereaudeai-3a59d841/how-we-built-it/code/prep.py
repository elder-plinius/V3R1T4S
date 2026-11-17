"""Build the T2D audit tables from MetAML abundance.txt.bz2 + cMD sampleMetadata (depth), write folds.
Usage: python -I prep.py <run_dir> <cache_dir>"""
import sys, os, bz2, hashlib, json
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

run, cache = sys.argv[1], sys.argv[2]
META = ['dataset_name','sampleID','subjectID','bodysite','disease','age','gender','country','pubmedid','bmi']
meta, sp_names, sp_rows = {}, [], []
with bz2.open(os.path.join(run, 'data', 'abundance.txt.bz2'), 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        r = line.rstrip('\n').split('\t')
        if r[0] in META:
            meta[r[0]] = [x.strip() for x in r[1:]]
        elif r[0].startswith('k__') and '|s__' in r[0] and '|t__' not in r[0]:
            sp_names.append(r[0]); sp_rows.append(np.array(r[1:], dtype=float))
X_all = np.vstack(sp_rows).T  # samples x species
M = pd.DataFrame(meta)
print('samples', len(M), 'species rows', len(sp_names))

ds = M['dataset_name']; dis = M['disease']; body = M['bodysite']
w1 = ds.isin(['t2dmeta_long', 't2dmeta_short']) & dis.isin(['t2d', 'n'])
w2 = (ds == 'WT2D') & dis.isin(['t2d', 'n'])
ext = ds.isin(['Quin_gut_liver_cirrhosis', 'Zeller_fecal_colorectal_cancer', 'hmp', 'hmpii', 'metahit']) & (dis == 'n') & (body == 'stool')
sel = w1 | w2 | ext
D = M[sel].copy()
D['setting_w1'] = w1[sel].values; D['setting_w2'] = w2[sel].values; D['external'] = ext[sel].values
D['y'] = (D['disease'] == 't2d').astype(int)
D['study'] = D['pubmedid']
def num(s):
    try:
        v = float(s)
        return v if np.isfinite(v) else np.nan
    except Exception:
        return np.nan
D['age_n'] = D['age'].map(num); D['bmi_n'] = D['bmi'].map(num)
D['country_c'] = D['country'].where(~D['country'].isin(['nd', 'na', '-', '']), 'missing')
D['sex_c'] = D['gender'].where(D['gender'].isin(['male', 'female']), 'missing')
D['group'] = D['dataset_name'].str.lower() + ':' + D['subjectID'].str.lower()
# hmp and hmpii share subjects (same HMP subject ids): group by subject id only for HMP
hmpmask = D['dataset_name'].isin(['hmp', 'hmpii'])
D.loc[hmpmask, 'group'] = 'hmp:' + D.loc[hmpmask, 'subjectID'].str.lower()

# depth from cMD
cm = pd.read_csv(os.path.join(cache, 'cmd_sampleMetadata_subset.tsv'), sep='\t', dtype=str)
cm['number_reads'] = pd.to_numeric(cm['number_reads'], errors='coerce')
dmap = {}
for _, r in cm.iterrows():
    if pd.notna(r['number_reads']):
        dmap.setdefault(r['sample_id'], set()).add((r['study_name'], r['number_reads']))
def depth(s):
    v = dmap.get(s)
    if not v or len(v) != 1: return np.nan
    return np.log10(list(v)[0][1])
D['depth_log10'] = D['sampleID'].map(depth)
D = D.reset_index().rename(columns={'index': 'col_index'})
X = X_all[D['col_index'].values, :]

for name, mask in [('W1', D['setting_w1']), ('W2', D['setting_w2']), ('P1', D['setting_w1'] | D['setting_w2']), ('P2', np.ones(len(D), bool))]:
    sub = D[mask]
    print(f'{name}: n={len(sub)} cases={int(sub.y.sum())} controls={int((1-sub.y).sum())} groups={sub.group.nunique()} '
          f'studies={sub.study.value_counts().to_dict()} depth_matched={int(sub.depth_log10.notna().sum())} '
          f'age={int(sub.age_n.notna().sum())} bmi={int(sub.bmi_n.notna().sum())} countries={sub.country_c.value_counts().to_dict()}')
print('external by dataset:', D[D.external].dataset_name.value_counts().to_dict())
print('depth matched by dataset:', D.groupby('dataset_name').depth_log10.apply(lambda s: f'{s.notna().sum()}/{len(s)}').to_dict())

os.makedirs(cache, exist_ok=True)
np.save(os.path.join(cache, 'X_species.npy'), X)
D.drop(columns=['col_index']).to_csv(os.path.join(cache, 'samples.tsv'), sep='\t', index=False)
with open(os.path.join(cache, 'species_names.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(sp_names) + '\n')

# folds per setting, written before any fit
fdir = os.path.join(run, 'folds'); os.makedirs(fdir, exist_ok=True)
lines = []
for name, mask in [('W1', D['setting_w1']), ('W2', D['setting_w2']), ('P1', D['setting_w1'] | D['setting_w2']), ('P2', np.ones(len(D), bool))]:
    sub = D[mask]
    F = pd.DataFrame({'sampleID': sub['sampleID'].values, 'dataset_name': sub['dataset_name'].values, 'y': sub['y'].values})
    for r in range(20):
        fold = np.full(len(sub), -1)
        cv = StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=r)
        for k, (_, te) in enumerate(cv.split(np.zeros(len(sub)), sub['y'].values, sub['group'].values)):
            fold[te] = k
        assert (fold >= 0).all()
        F[f'r{r}'] = fold
    p = os.path.join(fdir, f'folds_{name}.csv')
    F.to_csv(p, index=False, lineterminator='\n')
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    lines.append(f'{h}  folds_{name}.csv')
open(os.path.join(fdir, 'FOLDS.sha256'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
