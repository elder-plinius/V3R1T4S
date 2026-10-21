"""Largest-hole evaluator for spheres in the cube [-1/2,1/2]^3.
hole(C) = max_p min( min_i |p-c_i|/2 , 1/2 - max_k |p_k| ): the largest common radius a NEW sphere centred at p can have
against the existing centres C (pairs) and the walls. Candidates: Voronoi vertices of C plus a grid; best 40 polished by
SLSQP (maximize t s.t. |p-c_i| >= 2t for the 60 nearest centres, 1/2 -+ p_k >= t), re-checked against all centres. NUMERICAL."""
import numpy as np
from scipy.spatial import cKDTree, Voronoi
from scipy.optimize import minimize
def rho(P,T):
    d,_=T.query(P); return np.minimum(d/2, 0.5-np.abs(P).max(1))
def polish(p0,C,T,k=60):
    p=p0.copy()
    for it in range(12):
        _,idx=T.query(p,min(k,len(C))); Q=C[np.atleast_1d(idx)]
        cons=[{'type':'ineq','fun':lambda z,Q=Q:((z[:3]-Q)**2).sum(1)-4*z[3]**2,
               'jac':lambda z,Q=Q:np.hstack([2*(z[:3]-Q),-8*z[3]*np.ones((len(Q),1))])},
              {'type':'ineq','fun':lambda z:np.r_[0.5-z[:3]-z[3],0.5+z[:3]-z[3]],
               'jac':lambda z:np.vstack([np.hstack([-np.eye(3),-np.ones((3,1))]),np.hstack([np.eye(3),-np.ones((3,1))])])}]
        t0=float(rho(p[None],T)[0]); z0=np.r_[p,max(t0,0)]
        res=minimize(lambda z:-z[3],z0,jac=lambda z:np.r_[0,0,0,-1.],constraints=cons,method='SLSQP',options=dict(maxiter=500,ftol=1e-16))
        pn=np.clip(res.x[:3],-0.5,0.5)
        t1=float(rho(pn[None],T)[0])
        if t1>=t0-1e-16: p=pn
        if t1<=t0+1e-16: break
    return p,float(rho(p[None],T)[0])
def hole(C,ngrid=None,ntop=40):
    C=np.asarray(C,float); T=cKDTree(C); n=len(C)
    V=Voronoi(C).vertices if len(C)>4 else np.zeros((0,3)); V=V[(np.abs(V)<=0.5).all(1)]
    d,_=T.query(C,2); r0=min(d[:,1].min()/2,0.5-np.abs(C).max()) if n>1 else 0.25; b=0.5-r0
    g=ngrid or max(30,int(round(4*n**(1/3)))); a=np.linspace(-b,b,g); G=np.stack(np.meshgrid(a,a,a),-1).reshape(-1,3)  # grid on the shrunken box, incl. its corners/edges/faces
    P=np.vstack([V,G]); R=rho(P,T); top=np.argsort(-R)[:ntop*3]
    picked=[]; 
    for i in top:
        if all(np.linalg.norm(P[i]-P[j])>1e-3 for j in picked): picked.append(i)
        if len(picked)>=ntop: break
    best=(None,-1)
    for i in picked:
        p,v=polish(P[i],C,T)
        if v>best[1]: best=(p,v)
    return best

def hole2(C,maxpolish=4000):
    """Bounded search: Voronoi vertices of C plus its 6 face mirrors (x -> +-1 - x), restricted to the cube, are the vertices of the
    clipped Voronoi cells. For p in the cell of c, rho(p) <= |p-c|/2 <= max over the cell's vertices of |v-c|/2. We polish vertices in
    descending d/2 and stop when d/2 <= best found (or after maxpolish). Returns (p, value, n_polished, stopped_by_bound)."""
    C=np.asarray(C,float); T=cKDTree(C); n=len(C); A=[C]
    for k in range(3):
        for s in (-1,1):
            M=C.copy(); M[:,k]=s-M[:,k]; A.append(M)
    try: V=Voronoi(np.vstack(A)).vertices
    except Exception: V=Voronoi(np.vstack(A),qhull_options='Qbb Qc Qz QJ').vertices
    V=V[(np.abs(V)<=0.5+1e-12).all(1)]; V=np.clip(V,-0.5,0.5)
    d,_=T.query(V); U=d/2; o=np.argsort(-U); best=(None,-1.0); k=0
    for i in o:
        if U[i]<=best[1] or k>=maxpolish: break
        p,v=polish(V[i],C,T); k+=1
        if v>best[1]: best=(p,v)
    return best[0],best[1],k,bool(k<maxpolish)
