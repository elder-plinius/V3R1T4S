# Leakage audit: rebuild M1 from scratch with (a) every target-protein assay's DMS_score replaced by random noise and
# (b) the 30 non-fitting assays deleted; the selection and every prediction file must be bit-identical.
import pandas as pd, numpy as np, pickle, json, hashlib, copy
from scipy.stats import spearmanr
cache=pickle.load(open('pg_cache.pkl','rb'))
split=json.load(open('split.json')); fit=split['fitting_assays']; targets=split['target_assays']
live=pd.read_csv('DMS_substitutions_Spearman_DMS_level.csv').set_index('DMS ID'); uni=live['UniProt ID']
rng=np.random.default_rng(7)
c2={a:cache[a].copy() for a in fit}
for a in targets:
    t=cache[a].copy(); t['DMS_score']=rng.normal(size=len(t)); t['DMS_score_bin']=-1; c2[a]=t
models=[c for c in c2[fit[0]].columns if c not in ('mutant','DMS_score','DMS_score_bin')]
rho=pd.DataFrame({a:[spearmanr(c2[a].DMS_score,c2[a][m]).correlation for m in models] for a in fit},index=models).T
w=pd.Series({a:1/sum(uni[b]==uni[a] for b in fit) for a in fit}); sel=list((rho.mul(w,axis=0).sum()/w.sum()).sort_values(ascending=False).index[:12])
orig=json.load(open('m1_selection.json'))['selected']
print('selection identical:',sel==orig)
ok=0
for a in targets:
    s=c2[a]; Z=s[sel].values.astype(float); Z=(Z-Z.mean(0))/Z.std(0)
    buf=pd.DataFrame({'mutant':s.mutant,'prediction':Z.mean(1)}).to_csv(index=False,lineterminator='\n').encode()
    h=hashlib.sha256(buf).hexdigest(); h0=hashlib.sha256(open(f'result/{a}.M1.csv','rb').read().replace(b'\r\n',b'\n')).hexdigest()
    ok+=h==h0; print(f'{a:42s} identical={h==h0}')
print(f'{ok}/{len(targets)} prediction files bit-identical with target labels randomised')
print('UniProt overlap fitting vs targets:',sorted({uni[a] for a in fit}&{uni[a] for a in targets}))
