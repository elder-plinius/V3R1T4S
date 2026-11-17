"""Descriptive covariate tables by group (no model): MetAML metadata vs cMD sampleMetadata cross-check."""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd, numpy as np
run, cache = sys.argv[1], sys.argv[2]
D = pd.read_csv(os.path.join(cache, 'samples.tsv'), sep='\t', dtype={'study': str, 'sampleID': str})
cm = pd.read_csv(os.path.join(cache, 'cmd_sampleMetadata_subset.tsv'), sep='\t', dtype=str)
cm = cm.drop_duplicates('sample_id').set_index('sample_id')
D['cmd_age'] = pd.to_numeric(D['sampleID'].map(cm['age']), errors='coerce')
D['cmd_bmi'] = pd.to_numeric(D['sampleID'].map(cm['BMI']), errors='coerce')
D['cmd_gender'] = D['sampleID'].map(cm['gender'])
D['cmd_condition'] = D['sampleID'].map(cm['study_condition'])
for name, mask in [('W1 Qin2012', D.setting_w1.astype(bool)), ('W2 WT2D', D.setting_w2.astype(bool))]:
    s = D[mask]
    print('==', name)
    print(s.groupby('y')[['age_n', 'cmd_age', 'bmi_n', 'cmd_bmi', 'depth_log10']].describe().T.round(2).to_string())
    print('sex x y:\n', pd.crosstab(s['sex_c'], s['y']).to_string())
    print('cmd condition x y:\n', pd.crosstab(s['cmd_condition'].fillna('NA'), s['y']).to_string())
    print('age agreement MetAML vs cMD (abs diff <= 1):', float((abs(s.age_n - s.cmd_age) <= 1).mean()))
    print('bmi agreement MetAML vs cMD (abs diff <= 0.5):', float((abs(s.bmi_n - s.cmd_bmi) <= 0.5).mean()))
    if name.startswith('W1'):
        print('by dataset (stage) x y, age mean:\n', s.groupby(['dataset_name', 'y'])['age_n'].agg(['count', 'mean', 'std']).round(2).to_string())
        print('by dataset x y, depth mean:\n', s.groupby(['dataset_name', 'y'])['depth_log10'].agg(['count', 'mean', 'std']).round(3).to_string())
