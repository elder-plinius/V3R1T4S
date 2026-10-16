"""Penalty inflation library (adapted from run 0411 penalty.py). rad(X): feasible radius (float). inflate(X,secs,log,save): raise target R geometrically while L-BFGS can remove all overlap."""
import time,numpy as np
from scipy.optimize import minimize; from scipy.spatial import cKDTree
def rad(X):
    d,_=cKDTree(X).query(X,2); return min(d[:,1].min()/2, 0.5-np.abs(X).max())
def energy(Y,R):
    n=len(Y); P=np.array(list(cKDTree(Y).query_pairs(2*R))); g=np.zeros_like(Y); E=0.0
    if len(P):
        a=Y[P[:,0]]-Y[P[:,1]]; d=np.linalg.norm(a,axis=1); o=2*R-d; E+=(o**2).sum(); gg=(-2*o/d)[:,None]*a
        np.add.at(g,P[:,0],gg); np.add.at(g,P[:,1],-gg)
    w=np.abs(Y)-(0.5-R); m=w>0; E+=(w[m]**2).sum(); g[m]+=2*w[m]*np.sign(Y[m]); return E,g
def relax(X,R,maxiter=3000):
    n=len(X)
    def f(y):
        E,g=energy(y.reshape(n,3),R); return E,g.ravel()
    res=minimize(f,X.ravel(),jac=True,method='L-BFGS-B',options=dict(maxiter=maxiter,gtol=1e-20,ftol=1e-30))
    return res.x.reshape(n,3),res.fun
def inflate(X,secs,log=None,save=None,step=1e-6,R0=None):
    best=rad(X); B=X.copy(); t0=time.time()
    if R0 is not None and R0>best:  # squeeze start: target radius above current feasible radius
        Y,E=relax(B,R0); r=rad(Y)
        if log: log.write('squeeze R0=%.15f got=%.15f E=%.2e\n'%(R0,r,E))
        B=Y; best=r
    while time.time()-t0<secs and step>1e-13:
        R=best*(1+step); Y,E=relax(B,R); r=rad(Y)
        if log: log.write('step=%.1e R=%.15f got=%.15f best=%.15f E=%.2e t=%.0f\n'%(step,R,r,best,E,time.time()-t0)); log.flush()
        if r>best+1e-15:
            best,B=r,Y; step*=2
            if save: np.savetxt(save,B,fmt='%.20f')
        else: step/=4
    return B,best
