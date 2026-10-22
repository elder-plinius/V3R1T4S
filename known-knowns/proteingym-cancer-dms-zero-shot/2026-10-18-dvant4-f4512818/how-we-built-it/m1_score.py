# Method M1 exactly as PREREG.md (frozen 2026-10-18T19:11:52Z). Step 1-2 use fitting assays only; step 3 builds
# predictions without labels; scoring happens only through the independent checker.
import pandas as pd, numpy as np, pickle, json, os, subprocess, sys, hashlib
from scipy.stats import spearmanr
cache=pickle.load(open('pg_cache.pkl','rb'))
split=json.load(open('split.json')); fit=split['fitting_assays']; targets=split['target_assays']
live=pd.read_csv('DMS_substitutions_Spearman_DMS_level.csv').set_index('DMS ID')
uni=live['UniProt ID']
models=[c for c in cache[fit[0]].columns if c not in ('mutant','DMS_score','DMS_score_bin')]
rho=pd.DataFrame({a:[spearmanr(cache[a].DMS_score,cache[a][m]).correlation for m in models] for a in fit},index=models).T
w=pd.Series({a:1/sum(uni[b]==uni[a] for b in fit) for a in fit})
pb=(rho.mul(w,axis=0).sum()/w.sum()).sort_values(ascending=False)
sel=list(pb.index[:12]); print('M1 selected models:',sel)
json.dump({'selected':sel,'pb_mean':pb[sel].round(5).to_dict()},open('m1_selection.json','w'),indent=1)
os.makedirs('result',exist_ok=True)
for a in targets:
    s=cache[a]; Z=s[sel].values.astype(float); Z=(Z-Z.mean(0))/Z.std(0)
    pd.DataFrame({'mutant':s.mutant,'prediction':Z.mean(1)}).to_csv(f'result/{a}.M1.csv',index=False)
print('wrote',len(targets),'prediction files')
