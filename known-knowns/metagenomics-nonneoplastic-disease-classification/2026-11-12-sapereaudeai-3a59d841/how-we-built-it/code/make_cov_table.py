"""Derived per-sample covariate table for the package checker (public sample ids, labels, covariates, depth)."""
import sys, os
import pandas as pd
cache, out = sys.argv[1], sys.argv[2]
D = pd.read_csv(os.path.join(cache, 'samples.tsv'), sep='\t', dtype={'study': str, 'sampleID': str})
T = D[['sampleID', 'dataset_name', 'study', 'y', 'age_n', 'bmi_n', 'country_c', 'sex_c', 'depth_log10', 'setting_w1', 'setting_w2']].copy()
T.columns = ['sampleID', 'dataset_name', 'study_pubmed', 'y_t2d', 'age', 'bmi', 'country', 'sex', 'depth_log10_reads', 'in_W1', 'in_W2']
T['in_W1'] = T['in_W1'].astype(int); T['in_W2'] = T['in_W2'].astype(int)
T.to_csv(out, index=False, lineterminator='\n', float_format='%.6g')
print(T.shape)
