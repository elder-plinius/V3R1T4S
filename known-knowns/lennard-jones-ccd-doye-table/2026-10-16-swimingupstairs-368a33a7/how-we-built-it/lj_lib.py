"""LJ cluster: E = 4 sum_{i<j} (r^-12 - r^-6) (sigma = epsilon = 1)."""
import numpy as np, mpmath
from scipy.optimize import minimize
def load(path):
    v=np.array([float(x) for x in open(path).read().split()]); return v.reshape(-1,3)
def eg(X):
    d=X[:,None,:]-X[None,:,:]; r2=(d**2).sum(-1); n=len(X); np.fill_diagonal(r2,1.0)
    ir6=r2**-3; ir12=ir6*ir6; np.fill_diagonal(ir6,0); np.fill_diagonal(ir12,0)
    E=2*(ir12-ir6).sum()
    f=(-48*ir12+24*ir6)/r2   # dE/dr * 1/r
    g=(f[:,:,None]*d).sum(1)
    return E,g
def energy(X): return eg(X)[0]
def relax(X,gtol=1e-10,maxiter=20000):
    n=len(X)
    def f(y): E,g=eg(y.reshape(n,3)); return E,g.ravel()
    r=minimize(f,X.ravel(),jac=True,method='L-BFGS-B',options=dict(maxiter=maxiter,gtol=gtol,ftol=1e-16,maxcor=30))
    return r.x.reshape(n,3)
def energy_mp(X,dps=30):
    mpmath.mp.dps=dps; P=[[mpmath.mpf(repr(float(c))) for c in p] for p in X]; E=mpmath.mpf(0)
    for i in range(len(P)):
        a=P[i]
        for j in range(i+1,len(P)):
            b=P[j]; r2=(a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2; i6=1/r2**3; E+=4*(i6*i6-i6)
    return E
def hessian_eigs(X):
    n=len(X); d=X[:,None,:]-X[None,:,:]; r2=(d**2).sum(-1); np.fill_diagonal(r2,1.0)
    a=(-48*r2**-7+24*r2**-4)            # (1/r)dE/dr
    b=(672*r2**-8-192*r2**-5)           # d/dr2 terms: second-derivative factor
    I=np.eye(3)
    blk=-(a[:,:,None,None]*I+b[:,:,None,None]*d[:,:,:,None]*d[:,:,None,:])
    for i in range(n): blk[i,i]=0
    H=blk.transpose(0,2,1,3).reshape(3*n,3*n).copy()
    for i in range(n): H[3*i:3*i+3,3*i:3*i+3]=-blk[i].sum(0)
    return np.linalg.eigvalsh(H)
