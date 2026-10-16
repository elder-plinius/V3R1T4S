"""LJ surface basin hopping. Usage: bh.py N seed seconds mode(surf|cap|mc|exile) outprefix"""
import sys,os,time,json,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..','..')
sys.path.insert(0,os.path.join(R,'checker')); from lj_lib import load,eg,relax
N,seed,secs,mode,out=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),sys.argv[4],sys.argv[5]
rng=np.random.default_rng(seed); tab=dict((int(a),float(b)) for a,b in (l.split() for l in open(os.path.join(R,'lj_table_parsed.tsv'))))
X=relax(load(os.environ.get('START') or os.path.join(R,'tbl','LJ562-1000','%d.TXT'%N)),gtol=1e-9); E=eg(X)[0]; cur=(E,X); best=(E,X); t0=time.time(); it=0; seen=set()
def site_e(X):
    d=np.linalg.norm(X[:,None]-X[None],axis=-1); np.fill_diagonal(d,np.inf); i6=d**-6; return (4*(i6*i6-i6)).sum(1)
def surf_site(X):
    c=X.mean(0); r=np.linalg.norm(X-c,axis=1); s=np.where(r>np.percentile(r,75))[0]
    for _ in range(200):
        i=rng.choice(s); u=rng.normal(size=3); u/=np.linalg.norm(u)
        if u@(X[i]-c)<0: u=-u
        p=X[i]+1.1*u
        if np.linalg.norm(X-p,axis=1).min()>0.95: return p
    return X[i]+1.5*(X[i]-c)/np.linalg.norm(X[i]-c)
kT=0.3 if mode=='mc' else 0.0
while time.time()-t0<secs:
    it+=1; Y=cur[1].copy(); m=mode if mode!='mc' else rng.choice(['surf','cap'])
    if m in('surf','exile'):
        k=rng.integers(1,4) if m=='surf' else rng.integers(3,9); se=site_e(Y); idx=np.argsort(-se)[:k+3]; idx=rng.choice(idx,k,replace=False)
        Z=np.delete(Y,idx,0)
        for _ in range(k): Z=np.vstack([Z,surf_site(Z)])
        if m=='exile': Z=relax(Z,gtol=1e-6,maxiter=500)
        Y=Z
    else:
        c=Y.mean(0); a=Y[rng.integers(N)]; idx=np.argsort(np.linalg.norm(Y-a,axis=1))[:rng.integers(10,31)]; Y[idx]+=rng.normal(scale=0.3,size=(len(idx),3))
    Y=relax(Y,gtol=1e-8,maxiter=5000); Ey=eg(Y)[0]; seen.add(round(Ey,4))
    if Ey<cur[0]-1e-9 or (kT>0 and rng.random()<np.exp(-(Ey-cur[0])/kT)): cur=(Ey,Y)
    if Ey<best[0]-1e-7: best=(Ey,Y); np.savetxt(out+'_best.txt',Y,fmt='%.17f')
    if it%10==0: json.dump(dict(N=N,it=it,best=best[0],table=tab[N],cur=cur[0],distinct=len(seen),elapsed=time.time()-t0),open(out+'_ckpt.json','w'))
r=dict(N=N,mode=mode,seed=seed,iters=it,best=best[0],table=tab[N],best_minus_table=best[0]-tab[N],distinct_minima_4dp=len(seen),lowest5=sorted(seen)[:5],elapsed=time.time()-t0)
print(json.dumps(r)); json.dump(r,open(out+'_final.json','w'))
