"""Grow (N-1 -> N) and shrink (N+1 -> N) sweeps; also central-vacancy toggle. Usage: sweep.py worker nworkers seconds"""
import sys,os,time,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..','..')
sys.path.insert(0,os.path.join(R,'checker')); from lj_lib import load,eg,relax
w,nw,secs=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]); t0=time.time(); rng=np.random.default_rng(w)
tab=dict((int(a),float(b)) for a,b in (l.split() for l in open(os.path.join(R,'tab_ok.tsv'))))
L=lambda N: load(os.path.join(R,'tbl','LJ562-1000','%d.TXT'%N))
def site_e(X):
    d=np.linalg.norm(X[:,None]-X[None],axis=-1); np.fill_diagonal(d,np.inf); i6=d**-6; return (4*(i6*i6-i6)).sum(1)
def best_add(X,k=10,trials=400):
    c=X.mean(0); r=np.linalg.norm(X-c,axis=1); surf=np.where(r>np.percentile(r,70))[0]; C=[]
    for _ in range(trials):
        i=rng.choice(surf); u=rng.normal(size=3); u/=np.linalg.norm(u)
        if u@(X[i]-c)<0: u=-u
        p=X[i]+1.1*u; d=np.linalg.norm(X-p,axis=1)
        if d.min()<0.95: continue
        i6=d**-6; C.append(((4*(i6*i6-i6)).sum(),p))
    C.sort(key=lambda t:t[0]); return [p for _,p in C[:k]]
out=open(os.path.join(H,'..','out',os.environ.get('TAG','sweep')+'_%d.tsv'%w),'w')
done=set(int(x) for x in open(os.environ['DONE'])) if os.environ.get('DONE') else set()
Ns=[N for N in sorted(tab) if N not in done][w::nw]
for N in Ns:
    if time.time()-t0>secs: break
    best=(np.inf,'')
    if N-1 in tab:
        X=L(N-1)
        for j,p in enumerate(best_add(X)):
            E=eg(relax(np.vstack([X,p]),gtol=1e-8,maxiter=4000))[0]
            if E<best[0]: best=(E,'grow%d'%j)
            if E<tab[N]-1e-5: np.savetxt(os.path.join(H,'..','out','cand_%d_grow%d.txt'%(N,j)),relax(np.vstack([X,p]),gtol=1e-8,maxiter=4000),fmt='%.17f')
    if N+1 in tab:
        X=L(N+1); se=site_e(X)
        for j in np.argsort(-se)[:10]:
            Y=relax(np.delete(X,j,0),gtol=1e-8,maxiter=4000); E=eg(Y)[0]
            if E<best[0]: best=(E,'shrink%d'%j)
            if E<tab[N]-1e-5: np.savetxt(os.path.join(H,'..','out','cand_%d_shrink%d.txt'%(N,j)),Y,fmt='%.17f')
    X=L(N); c=X.mean(0); i0=np.argmin(np.linalg.norm(X-c,axis=1)); Xc=np.delete(X,i0,0)
    for j,p in enumerate(best_add(Xc,k=5)):
        Y=relax(np.vstack([Xc,p]),gtol=1e-8,maxiter=4000); E=eg(Y)[0]
        if E<best[0]: best=(E,'vac%d'%j)
        if E<tab[N]-1e-5: np.savetxt(os.path.join(H,'..','out','cand_%d_vac%d.txt'%(N,j)),Y,fmt='%.17f')
    out.write('%d\t%.6f\t%.9f\t%s\t%.3e\n'%(N,tab[N],best[0],best[1],best[0]-tab[N])); out.flush()
print('done',len(Ns),time.time()-t0)
