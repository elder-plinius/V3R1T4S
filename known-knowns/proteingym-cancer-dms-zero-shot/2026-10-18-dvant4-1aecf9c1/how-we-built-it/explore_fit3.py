# Exploration 3 (FITTING assays only): normalisation (rank vs z) and weighting (equal vs rho-weighted) for top-K.
import pandas as pd, numpy as np, pickle, json
from scipy.stats import spearmanr, rankdata
cache=pickle.load(open('pg_cache.pkl','rb'))
split=json.load(open('split.json')); fit=split['fitting_assays']
live=pd.read_csv('DMS_substitutions_Spearman_DMS_level.csv').set_index('DMS ID')
meta=['Number of Mutants','Selection Type','UniProt ID','MSA_Neff_L_category','Taxon']
livemax=live.drop(columns=meta).apply(pd.to_numeric,errors='coerce').max(axis=1); uni=live['UniProt ID']
models=[c for c in cache[fit[0]].columns if c not in ('mutant','DMS_score','DMS_score_bin')]
Rr={};Rz={};Y={};rho={}
for a in fit:
    s=cache[a]; Y[a]=s.DMS_score.values
    Rr[a]=np.column_stack([rankdata(s[m])/len(s) for m in models])
    Z=s[models].values.astype(float); Rz[a]=(Z-Z.mean(0))/(Z.std(0)+1e-12)
    rho[a]=np.array([spearmanr(Y[a],Rr[a][:,j]).correlation for j in range(len(models))])
RHO=pd.DataFrame(rho,index=models).T
prots=sorted({uni[a] for a in fit})
for norm,RR in [('rank',Rr),('z',Rz)]:
  for K in [8,12,16]:
    for wt in ['equal','rho']:
      out=[]
      for p in prots:
        tr=[a for a in fit if uni[a]!=p]; te=[a for a in fit if uni[a]==p]
        w=pd.Series({a:1/sum(uni[b]==uni[a] for b in tr) for a in tr})
        sc=(RHO.loc[tr].mul(w,axis=0)).sum()/w.sum(); top=sc.sort_values(ascending=False).index[:K]
        idx=[models.index(m) for m in top]; ww=np.ones(K) if wt=='equal' else sc[top].values
        for a in te: out.append(spearmanr(Y[a],RR[a][:,idx]@ww).correlation-livemax[a])
      m=np.array(out); print(f"{norm:4s} K={K:2d} {wt:5s} frac>=0.015 {(m>=0.015).mean():.3f} ({(m>=0.015).sum()}) median {np.median(m):+.4f}")
