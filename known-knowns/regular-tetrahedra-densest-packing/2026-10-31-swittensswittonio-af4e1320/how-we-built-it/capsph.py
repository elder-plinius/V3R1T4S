"""NUMERICAL: sup of (surface fraction C1 + C2) for two disjoint spherical caps (radius<=pi/2) disjoint from lune L (angle theta) on S^2.
caps: normal nu_i, radius rho_i<=min(pi/2, d(nu_i,L)); disjoint: angle(nu1,nu2)>=rho1+rho2."""
import numpy as np
from scipy.optimize import minimize
th=np.arccos(1/3)
def dist_L(v):  # angular distance from unit vector v to lune L={azimuth in[-th/2,th/2] about z? use axis z}
    # lune about z axis: azimuth in [-th/2,th/2]
    az=np.arctan2(v[1],v[0]); colat=np.arccos(np.clip(v[2],-1,1)); 
    if abs(az)<=th/2: return 0.0
    # distance to nearest face semicircle (great circle containing z axis at azimuth +-th/2) : points on semicircle: azimuth exactly +-th/2
    best=np.inf
    for s in (th/2,-th/2):
        dphi=az-s
        # angular dist from point (colat,az) to the half great circle at azimuth s (colatitude 0..pi)
        # in the plane: if |dphi|<=pi/2 distance to full great circle = asin(sin(colat)*sin|dphi|)
        dphi=(dphi+np.pi)%(2*np.pi)-np.pi
        if abs(dphi)<=np.pi/2:
            d=np.arcsin(np.clip(np.sin(colat)*abs(np.sin(dphi)),0,1))
        else:
            d=min(colat,np.pi-colat)  # nearest vertex
            # actually nearest point of semicircle is a vertex (+-z)
            d=min(colat,np.pi-colat)
        best=min(best,d)
    # also vertices
    best=min(best,colat,np.pi-colat) if True else best
    return best
def A(r): return (1-np.cos(r))/2
def unit(a,b): return np.array([np.sin(a)*np.cos(b),np.sin(a)*np.sin(b),np.cos(a)])
def obj(x):
    v1=unit(x[0],x[1]); v2=unit(x[2],x[3])
    r1=min(np.pi/2,dist_L(v1)); r2=min(np.pi/2,dist_L(v2))
    ang=np.arccos(np.clip(v1@v2,-1,1))
    # choose rho1,rho2 maximizing A1+A2 s.t. rho<=r_i, rho1+rho2<=ang : greedy: convex -> put as much on larger
    best=0
    for first in (0,1):
        a_,b_=(r1,r2) if first==0 else (r2,r1)
        p=min(a_,ang); q=min(b_,ang-p); best=max(best,A(p)+A(max(q,0)))
    return -best
rng=np.random.default_rng(0)
best=(0,None)
for it in range(400):
    x0=np.array([np.arccos(rng.uniform(-1,1)),rng.uniform(0,2*np.pi),np.arccos(rng.uniform(-1,1)),rng.uniform(0,2*np.pi)])
    r=minimize(obj,x0,method='Nelder-Mead',options={'xatol':1e-10,'fatol':1e-12,'maxiter':4000})
    if -r.fun>best[0]: best=(-r.fun,r.x)
print("sup area sum ~",best[0],"  conj 0.5+(1-cos((pi-th)/2))/2 =",0.5+(1-np.cos((np.pi-th)/2))/2)
