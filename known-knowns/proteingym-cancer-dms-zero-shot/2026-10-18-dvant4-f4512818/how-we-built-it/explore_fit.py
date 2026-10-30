# Exploration on FITTING assays only (no target-protein labels are read). Leave-protein-out (LOPO):
# for each held-out protein, choose the configuration on the other fitting assays, score it on the held-out one.
import pandas as pd, numpy as np, pickle, json, itertools
from scipy.stats import spearmanr, rankdata
cache=pickle.load(open('pg_cache.pkl','rb'))
split=json.load(open('split.json')); fit=split['fitting_assays']
live=pd.read_csv('DMS_substitutions_Spearman_DMS_level.csv').set_index('DMS ID')
meta=['Number of Mutants','Selection Type','UniProt ID','MSA_Neff_L_category','Taxon']
livemax=live.drop(columns=meta).apply(pd.to_numeric,errors='coerce').max(axis=1)
uni=live['UniProt ID']
models=[c for c in cache[fit[0]].columns if c not in ('mutant','DMS_score','DMS_score_bin')]
R={}   # per assay: rank-normalised (0..1) model scores matrix, and labels
rho={}
for a in fit:
    s=cache[a]; X=np.column_stack([rankdata(s[m])/len(s) for m in models]); y=s.DMS_score.values
    R[a]=(X,y); rho[a]=np.array([spearmanr(y,X[:,j]).correlation for j in range(len(models))])
RHO=pd.DataFrame(rho,index=models).T
def ens(a,idx,w=None):
    X,y=R[a]; w=np.ones(len(idx)) if w is None else w
    return spearmanr(y,X[:,idx]@w).correlation
prots=sorted({uni[a] for a in fit})
res={}
for K in [3,5,8,12,20]:
    out=[]
    for p in prots:
        tr=[a for a in fit if uni[a]!=p]; te=[a for a in fit if uni[a]==p]
        # protein-balanced mean rho on training assays
        w=pd.Series({a:1/sum(uni[b]==uni[a] for b in tr) for a in tr})
        score=(RHO.loc[tr].mul(w,axis=0)).sum()/w.sum()
        idx=[models.index(m) for m in score.sort_values(ascending=False).index[:K]]
        for a in te: out.append((a,ens(a,idx),RHO.loc[a].max(),livemax[a]))
    d=pd.DataFrame(out,columns=['assay','ens','best_file','best_live']).set_index('assay')
    d['margin']=d.ens-d.best_live
    res[K]=d
    print(f"topK={K:2d} mean ens {d.ens.mean():.4f} mean best_live {d.best_live.mean():.4f}  frac margin>=0.015: {(d.margin>=0.015).mean():.3f} ({(d.margin>=0.015).sum()}/{len(d)})  median margin {d.margin.median():+.4f}")
# top models overall on fitting set (protein-balanced)
w=pd.Series({a:1/sum(uni[b]==uni[a] for b in fit) for a in fit})
print((RHO.mul(w,axis=0).sum()/w.sum()).sort_values(ascending=False).head(15).round(4))
pickle.dump(res,open('explore_res.pkl','wb'))
