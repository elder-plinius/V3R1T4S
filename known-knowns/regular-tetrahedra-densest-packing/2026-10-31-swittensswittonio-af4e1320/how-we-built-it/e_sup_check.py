"""NUMERICAL check of GEK Lemma 3.1 sup: max vol fraction of a theta-wedge W (c not in int W) with edge distance d0<=r, vs flush value V(r).
2D wedge in cross-section (prism along edge), slices of ball integrated exactly in h; area via polar quadrature around c."""
import numpy as np
th=np.arccos(1/3)
NPHI=2400; phi=(np.arange(NPHI)+0.5)*2*np.pi/NPHI
NH=80
hs=(np.arange(NH)+0.5)/NH*2-1   # midpoint rule on [-1,1]
Rs=np.sqrt(1-hs**2)
def wedge_vol(apex, omega):
    """2D wedge with apex 'apex' (2-vector, c at origin), interior = directions omega..omega+th from apex (ccw)."""
    # half-planes: wedge = {x: n1.(x-a)<=0, n2.(x-a)<=0}
    u1=np.array([np.cos(omega),np.sin(omega)]); u2=np.array([np.cos(omega+th),np.sin(omega+th)])
    # interior to left of u1 ray, right of u2 ray: n1 = -perp(u1)?? left normal of u1 is (-u1y,u1x); interior is left => outward normal = (u1y,-u1x)
    n1=np.array([u1[1],-u1[0]]); n2=np.array([-u2[1],u2[0]])
    a=np.asarray(apex)
    d=np.stack([np.cos(phi),np.sin(phi)],1)           # ray directions from c=origin
    # along ray t>=0: n.(t d - a)<=0 -> t*(n.d) <= n.a
    lo=np.zeros(NPHI); hi=np.full(NPHI,np.inf)
    for n in (n1,n2):
        nd=d@n; na=n@a
        pos=nd>1e-14; neg=nd<-1e-14; zer=~(pos|neg)
        hi=np.where(pos,np.minimum(hi,na/np.where(pos,nd,1)),hi)
        lo=np.where(neg,np.maximum(lo,na/np.where(neg,nd,1)),lo)
        hi=np.where(zer&(na<0),-1,hi)   # empty
    hi=np.where(hi<lo,lo,hi)
    tot=0.0
    for R in Rs:
        o=np.minimum(hi,R); i=np.minimum(lo,R)
        tot+=0.5*np.sum(o**2-i**2)*(2*np.pi/NPHI)
    return tot*(2/NH)/(4*np.pi/3)
def inside(apex,omega):  # is origin interior to wedge
    pass
def V_flush(d):
    # face-through-c wedge: face1 ray from apex passes through c, c ahead of apex along ray at distance d. choose apex = (-d,0), omega=0 => ray along +x passes c=(0,0)
    # but then c lies on face 1 (boundary): c in closure, ok; interior directions 0..th (ccw) => wedge above x axis.
    return wedge_vol((-d,0.0),0.0)
al=th/(2*np.pi)
print("alpha",al,"V_flush(0)",V_flush(1e-9))
for r in (0.2,0.5):
    vf=V_flush(r)
    best=0;arg=None
    for ang in np.linspace(0,2*np.pi,61):          # position of apex at distance r in direction ang
        a=r*np.array([np.cos(ang),np.sin(ang)])
        for om in np.linspace(0,2*np.pi,61):
            u1=np.array([np.cos(om),np.sin(om)])
            # check c not interior: c-a relative angle
            v=-a; ca=(np.arctan2(v[1],v[0])-om)%(2*np.pi)
            if 1e-9<ca<th-1e-9: continue
            vol=wedge_vol(a,om)
            if vol>best: best,arg=vol,(ang,om)
    print("r=%.2f  sup(nonflush grid)=%.6f  V_flush(r)=%.6f  diff=%.2e"%(r,best,vf,best-vf),arg,flush=True)

from scipy.optimize import minimize
def admissible(a,om):
    v=-a; ca=(np.arctan2(v[1],v[0])-om)%(2*np.pi)
    return not (1e-9<ca<th-1e-9)
rng=np.random.default_rng(3)
print("--- local search at fixed edge distance")
for r in (0.3,0.6,1.0):
    vf=V_flush(r); best=0
    for it in range(12):
        x0=[rng.uniform(0,2*np.pi),rng.uniform(0,2*np.pi)]
        def f(x):
            a=r*np.array([np.cos(x[0]),np.sin(x[0])])
            if not admissible(a,x[1]): return 1.0
            return -wedge_vol(a,x[1])
        res=minimize(f,x0,method='Nelder-Mead',options={'xatol':1e-5,'fatol':1e-9,'maxiter':200})
        best=max(best,-res.fun)
    print("r=%.2f best_local=%.6f  V_flush=%.6f  diff=%.2e"%(r,best,vf,best-vf),flush=True)
