import sys,time,os,numpy as np
from search import *
def sph(k,rng):
    v=rng.standard_normal((k,4)); return v/np.linalg.norm(v,axis=1)[:,None]
def shell_seed(n,nout,nc,rho,rng):
    x=[sph(nout,rng)]
    nin=n-nout-nc
    x.append(rho*sph(nin,rng))
    if nc: x.append(0.05*rng.standard_normal((nc,4)))
    return np.vstack(x)
def run(n,nout,nc,seed,DT):
    rng=np.random.default_rng(seed)
    x=shell_seed(n,nout,nc,rng.uniform(0.45,0.6),rng)
    for fac in [1.06,1.03,1.015,1.005]: x=relax(x,DT*fac,iters=4000)
    xp=project(x); x2,D2=inflate(xp,min_dist(xp),rounds=25)
    x3,D3=slp(x2,iters=120,delta=0.003,tol=1e-13)
    return x3,D3
if __name__=="__main__":
    n=int(sys.argv[1]); rT=float(sys.argv[2]); DT=2*rT/(1-rT); out=sys.argv[3]
    jobs=[(int(a.split(':')[0]),int(a.split(':')[1]),int(a.split(':')[2])) for a in sys.argv[4:]]
    for nout,nc,seed in jobs:
        t=time.time(); x,D=run(n,nout,nc,seed,DT); r=r_of_D(D)
        nr=np.linalg.norm(x,axis=1); ko=(nr>1-1e-6).sum()
        np.save(f"{out}/{n}_{nout}_{nc}_{seed}.npy",x)
        print(n,nout,nc,seed,'r=%.12f diff=%+.3e kout=%d t=%.0f'%(r,r-rT,ko,time.time()-t),flush=True)
