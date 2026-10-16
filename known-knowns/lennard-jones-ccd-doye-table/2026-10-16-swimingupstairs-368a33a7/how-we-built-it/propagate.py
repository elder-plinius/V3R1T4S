"""Propagate a new N-structure to N+1 (grow) and N-1 (shrink). Usage: propagate.py start.txt seed outprefix"""
import sys,os,json,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..','..')
sys.path.insert(0,os.path.join(R,'checker')); from lj_lib import load,eg,relax
X=load(sys.argv[1]); seed=int(sys.argv[2]); out=sys.argv[3]; rng=np.random.default_rng(seed); N=len(X)
tab=dict((int(a),float(b)) for a,b in (l.split() for l in open(os.path.join(R,'lj_table_parsed.tsv'))))
def site_e(X):
    d=np.linalg.norm(X[:,None]-X[None],axis=-1); np.fill_diagonal(d,np.inf); i6=d**-6; return (4*(i6*i6-i6)).sum(1)
c=X.mean(0); r=np.linalg.norm(X-c,axis=1); surf=np.where(r>np.percentile(r,70))[0]; C=[]
for _ in range(3000):
    i=rng.choice(surf); u=rng.normal(size=3); u/=np.linalg.norm(u)
    if u@(X[i]-c)<0: u=-u
    p=X[i]+1.1*u; d=np.linalg.norm(X-p,axis=1)
    if d.min()<0.95: continue
    i6=d**-6; C.append(((4*(i6*i6-i6)).sum(),p))
C.sort(key=lambda t:t[0]); res={'grow':[], 'shrink':[]}; best={'grow':(0,None),'shrink':(0,None)}
for e,p in C[:40]:
    Y=relax(np.vstack([X,p]),gtol=1e-8,maxiter=5000); E=eg(Y)[0]; res['grow'].append(E)
    if E<best['grow'][0]: best['grow']=(E,Y)
for j in np.argsort(-site_e(X))[:40]:
    Y=relax(np.delete(X,j,0),gtol=1e-8,maxiter=5000); E=eg(Y)[0]; res['shrink'].append(E)
    if E<best['shrink'][0]: best['shrink']=(E,Y)
for k,M in (('grow',N+1),('shrink',N-1)):
    np.savetxt('%s_%s_%d.txt'%(out,k,M),best[k][1],fmt='%.17f')
    print(json.dumps(dict(move=k,N=M,trials=len(res[k]),best=best[k][0],table=tab[M],best_minus_table=best[k][0]-tab[M],lowest5=sorted(set(round(e,6) for e in res[k]))[:5])))
