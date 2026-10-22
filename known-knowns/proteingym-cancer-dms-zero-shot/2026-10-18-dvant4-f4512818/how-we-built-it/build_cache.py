# Cache score matrices (without sequences) as parquet-free pickles; write the frozen split file.
import pandas as pd, numpy as np, pickle, json
PG='pg'; LIVE='DMS_substitutions_Spearman_DMS_level.csv'
live=pd.read_csv(LIVE).set_index('DMS ID')
cache={}
for a in live.index:
    cols=pd.read_csv(f'{PG}/{a}.csv',nrows=0).columns
    s=pd.read_csv(f'{PG}/{a}.csv',usecols=[c for c in cols if c!='mutated_sequence'])
    cache[a]=s
pickle.dump(cache,open('pg_cache.pkl','wb'))
uni=live['UniProt ID']
TARGET_PROT={'BRCA1_HUMAN','BRCA2_HUMAN','PTEN_HUMAN','MSH2_HUMAN','P53_HUMAN','RASK_HUMAN','RASH_HUMAN','ERBB2_HUMAN'}
# conservative extra exclusions: other proteins with an oncogene / tumour-suppressor role (kept out of fitting, not scored)
EXTRA={'MET_HUMAN','SRC_HUMAN','RAF1_HUMAN','MK01_HUMAN','PPM1D_HUMAN','SHOC2_HUMAN','YAP1_HUMAN','TPOR_HUMAN','PPARG_HUMAN','CAR11_HUMAN','PRKN_HUMAN','GRB2_HUMAN','CASP3_HUMAN','CASP7_HUMAN','MLH1_HUMAN','VHL_HUMAN'}
targets=[a for a in live.index if uni[a] in TARGET_PROT]
excl=[a for a in live.index if uni[a] in EXTRA]
fit=[a for a in live.index if a not in targets and a not in excl]
json.dump({'target_proteins':sorted(TARGET_PROT),'target_assays':targets,'extra_excluded_proteins':sorted(EXTRA),'extra_excluded_assays':excl,'fitting_assays':fit},open('split.json','w'),indent=1)
print(len(targets),len(excl),len(fit)); print(targets); print(excl)
print('uniprot of targets',{uni[a] for a in targets})
