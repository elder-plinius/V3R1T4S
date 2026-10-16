# day v3: one independent worker per core; heartbeat file for external watchdog; per-trial cap; ckpt per trial (<=10 min)
import numpy as np, json, time, os, sys, datetime
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
RUN=os.path.abspath(os.path.dirname(__file__)+'/..'); sys.path.insert(0,RUN+'/code'); import check as CK
K=int(sys.argv[1]); NW=int(sys.argv[2]); DEADLINE=float(sys.argv[3])
OUT=RUN+f'/out/w{K}'; os.makedirs(OUT,exist_ok=True); HB=RUN+f'/logs/w{K}.hb'
TRIAL_CAP=120
NS=[int(a) for a in open(RUN+'/code/NLIST.txt').read().strip().split(',')]
MY=[n for i,n in enumerate(NS) if i%NW==K-1]
D=RUN+'/data_night'
now=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def loadc(n): return np.array([[float(v) for v in l.split()[-3:]] for l in open(f'{D}/coords_all/scu{n}.txt') if l.strip()])
TAB={int(l.split()[0]):float(l.split()[1]) for l in open(D+'/radius.txt') if l.strip()}
def rs(X):
    Dm=np.sqrt(((X[:,None]-X[None])**2).sum(-1)); np.fill_diagonal(Dm,9); return min(Dm.min()/2, 0.5-np.abs(X).max())
def slp(X,stop):
    n=len(X); tr=1e-2; r=rs(X)
    for it in range(400):
        open(HB,'w').write(f'{time.time()} it={it}\n')
        if time.time()>stop or tr<1e-13: break
        Dm=np.sqrt(((X[:,None]-X[None])**2).sum(-1)); np.fill_diagonal(Dm,9)
        I,J=np.where(np.triu(Dm<2*r+4*tr+1e-9,1)); ri,ci,v,b=[],[],[],[]; m=0
        for i,j in zip(I,J):
            u=(X[i]-X[j])/Dm[i,j]
            for k in range(3): ri+=[m,m]; ci+=[3*i+k,3*j+k]; v+=[-u[k],u[k]]
            ri.append(m); ci.append(3*n); v.append(2); b.append(Dm[i,j]); m+=1
        for k in range(3):
            for i in np.where(np.abs(X[:,k])>0.5-r-4*tr-1e-9)[0]:
                ri+=[m,m]; ci+=[3*i+k,3*n]; v+=[np.sign(X[i,k]),1]; b.append(0.5-abs(X[i,k])); m+=1
        A=coo_matrix((v,(ri,ci)),shape=(m,3*n+1)).tocsr(); c=np.zeros(3*n+1); c[-1]=-1
        res=linprog(c,A_ub=A,b_ub=np.array(b),bounds=[(-tr,tr)]*(3*n)+[(0,1)],method='highs',options={'time_limit':max(1.0,min(30,stop-time.time()))})
        if res.status!=0 or res.x is None: tr/=2; continue
        Y=X+res.x[:-1].reshape(n,3); ry=rs(Y)
        if ry>r: X,r=Y,ry; tr=min(tr*1.5,2e-2)
        else: tr/=3
    return X,r
rng=np.random.default_rng(1015000+K)
CKF=OUT+'/checkpoint.json'; best=json.load(open(CKF)) if os.path.exists(CKF) else {}
while time.time()<DEADLINE-30:
    for n in MY:
        if time.time()>DEADLINE-30: break
        b=best.setdefault(str(n),dict(table=TAB[n],best=-1,src='',tries=0))
        u=rng.random(); X0=loadc(n); src='posted'
        if u<0.25 and os.path.exists(f'{D}/coords_all/scu{n+1}.txt'): X0=np.delete(loadc(n+1),rng.integers(n+1),0); src='N+1-minus1'
        elif u<0.4 and os.path.exists(f'{D}/coords_all/scu{n-1}.txt'): X0=np.vstack([loadc(n-1),rng.uniform(-.45,.45,(1,3))]); src='N-1-plus1'
        elif u<0.5: X0=rng.uniform(-.45,.45,(n,3)); src='random'
        sig=10**rng.uniform(-5,-1.5); X=np.clip(X0+rng.normal(0,sig,X0.shape),-0.45,0.45)
        t0=time.time(); X,r=slp(X,min(time.time()+TRIAL_CAP,DEADLINE-20)); b['tries']+=1
        if r>b['best']: b['best']=r; b['src']=f'{src} sig={sig:.1e}'; np.savetxt(f'{OUT}/best{n}.txt',X,fmt='%.30f')
        open(OUT+'/trials.log','a').write(f"{now()} N={n} {src} sig={sig:.1e} r={r:.16f} table={TAB[n]:.16f} gap={r-TAB[n]:+.3e} sec={time.time()-t0:.0f}\n")
        if r-TAB[n]>1e-12:
            C=CK.load(f'{OUT}/best{n}.txt'); e=CK.rstar(C)-CK.table(n,D+'/radius.txt')
            open(OUT+'/CANDIDATES.txt','a').write(f"{now()} N={n} exact_diff={CK.mp.nstr(e,8)} {'PASS' if e>=CK.mp.mpf('1e-11') else 'FAIL'}\n")
        json.dump(best,open(CKF+'.tmp','w'),indent=1); os.replace(CKF+'.tmp',CKF)
