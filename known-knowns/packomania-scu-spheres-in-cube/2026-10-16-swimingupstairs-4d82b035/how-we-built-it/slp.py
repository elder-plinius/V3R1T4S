"""Sparse sequential-LP inflation (HiGHS). Maximize t s.t. linearised pair constraints d_ij + u_ij.(D_i - D_j) >= 2t for near pairs and
0.5 - s*(x_ik + D_ik) >= t for near walls, |D| <= Delta. Accept a step only if the TRUE feasible radius rises; adapt Delta.
slp(X, secs, log, save) -> (X_best, r_best)."""
import time,numpy as np, scipy.sparse as sp
from scipy.optimize import linprog
from scipy.spatial import cKDTree
def rad(X):
    d,_=cKDTree(X).query(X,2); return min(d[:,1].min()/2, 0.5-np.abs(X).max())
def lpstep(X,r,Delta,margin):
    n=len(X); P=np.array(sorted(cKDTree(X).query_pairs(2*r+margin)))
    rows=[];cols=[];vals=[];b=[]; m=0
    if len(P):
        a=X[P[:,0]]-X[P[:,1]]; d=np.linalg.norm(a,axis=1); u=a/d[:,None]; k=len(P); ii=np.arange(k)
        for c in range(3):
            rows+= [ii,ii]; cols+=[3*P[:,0]+c,3*P[:,1]+c]; vals+=[-u[:,c],u[:,c]]
        rows.append(ii); cols.append(np.full(k,3*n)); vals.append(np.full(k,2.0)); b.append((d-2*r)/Delta); m=k
    W=np.argwhere(np.abs(X)>0.5-r-margin)
    if len(W):
        s=np.sign(X[W[:,0],W[:,1]]); k=len(W); ii=m+np.arange(k)
        rows+=[ii,ii]; cols+=[3*W[:,0]+W[:,1],np.full(k,3*n)]; vals+=[s,np.ones(k)]; b.append((0.5-np.abs(X[W[:,0],W[:,1]])-r)/Delta); m+=k
    A=sp.csr_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(m,3*n+1)); bb=np.concatenate(b)
    c=np.zeros(3*n+1); c[-1]=-1; bounds=[(-1,1)]*(3*n)+[(None,None)]  # scaled: D=Delta*z, t=r+Delta*s (HiGHS tolerance 1e-7 is then relative to Delta)
    res=linprog(c,A_ub=A,b_ub=bb,bounds=bounds,method='highs')
    if res.status!=0: return None,None
    return X+Delta*res.x[:3*n].reshape(n,3),r+Delta*res.x[-1]
def slp(X,secs,log=None,save=None,Delta=1e-4,minDelta=1e-12):
    best=rad(X); B=X.copy(); t0=time.time(); it=0
    while time.time()-t0<secs and Delta>minDelta:
        it+=1; Y,t=lpstep(B,best,Delta,margin=max(4*Delta,1e-9)+best*0.02)
        if Y is None: Delta/=4; continue
        r=rad(Y)
        if log: log.write('it=%d Delta=%.2e lp_t=%.17f true=%.17f best=%.17f gain=%.3e t=%.0f\n'%(it,Delta,t,r,best,r-best,time.time()-t0)); log.flush()
        if r>best+1e-17:
            best,B=r,Y
            if save: np.savetxt(save,B,fmt='%.20f')
            if t-r<0.5*(t-best+1e-30): Delta*=2
        else: Delta/=4
    return B,best
