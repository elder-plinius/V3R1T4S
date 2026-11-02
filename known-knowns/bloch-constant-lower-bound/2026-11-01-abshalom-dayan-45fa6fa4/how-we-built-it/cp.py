import sys,numpy as np,time,math,json
from nlp import *
sq=math.sqrt(3)/4
def seed_rows(zpath):
    z=np.load(zpath,allow_pickle=False); return z
def loop(P,rho,psi,gam,K,rmax,rounds=25,topk=500,verbose=True,evalf=None,tol=1e-11,maxrows=6000,stop=2e-8):
    """cutting plane. returns rho,psi,gam,lam,a,hist"""
    hist=[]; best=None
    for rd in range(rounds):
        t=time.time()
        a,lam,info=P.solve(rho,psi,gam,tol=tol)
        val=evalf(rho,psi,gam,lam) if evalf else info['obj']
        rn,pn,gn,mv=cuts(a,K,rmax,topk=topk,tol=1e-6)
        hist.append((rd,info['obj'],val,mv,len(rho),info['it'],info['rd']))
        if verbose: print('rd',rd,'obj %.9f certval %.9f maxviol %.2e rows %d it %d rd %.1e nnz %d t %.1f'%(info['obj'],val,mv,len(rho),info['it'],info['rd'],(lam>1e-10).sum(),time.time()-t),flush=True)
        if best is None or val>best[0]: best=(val,rho.copy(),psi.copy(),gam.copy(),lam.copy(),a.copy())
        if mv<stop or len(rn)==0: break
        # prune: keep rows active (lam big or nearly tight)
        keep=(lam>1e-9)
        R=rowmat(rho,psi,gam,K); sl=1-R@a
        keep|=sl<1e-3
        rho,psi,gam=np.r_[rho[keep],rn],np.r_[psi[keep],pn],np.r_[gam[keep],gn]
        # also linearise at same points with refreshed gamma already covered by cuts; cap size
        if len(rho)>maxrows:
            o=np.argsort(sl[keep])[:maxrows-len(rn)]
            k=keep.sum(); idx=np.r_[o,np.arange(k,len(rho))]
            rho,psi,gam=rho[idx],psi[idx],gam[idx]
    return best,hist
def integral_problem(r,K,b2=-1.0,b3=0.0):
    k=np.arange(K+1);w=r**(k+1)/(k+1)
    return w,Prob(w,K,{2:b2,3:b3},{})
def evalf_int(w,K):
    def f(rho,psi,gam,lam):
        lam=np.where(lam>0,lam,0);d,e=certvalue(w,K,rho,psi,gam,lam)
        return e-d[2]-sq
    return f
def point_problem(x,K,eta,a2box=1.0):
    k=np.arange(K+1);w=x**k
    return w,Prob(w,K,{},{2:a2box,3:eta})
def evalf_pt(w,K,eta,a2box=1.0,xhi=None):
    def f(rho,psi,gam,lam):
        lam=np.where(lam>0,lam,0);d,e=certvalue(w,K,rho,psi,gam,lam)
        return e-a2box*abs(d[2])-eta*abs(d[3])
    return f
