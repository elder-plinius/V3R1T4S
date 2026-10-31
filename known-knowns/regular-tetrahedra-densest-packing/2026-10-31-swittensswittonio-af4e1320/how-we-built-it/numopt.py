"""NUMERICAL (heuristic) search for max total volume of non-central objects (wedges/caps) disjoint from the centred wedge W0 in the unit ball.
Lower bounds on missing volume fraction rho(c,w) (r=inf) are 1-alpha-max.  Monte Carlo on fixed sample points + penalty."""
import numpy as np, sys
from scipy.optimize import differential_evolution
th=np.arccos(1/3); al=th/(2*np.pi)
rng=np.random.default_rng(1)
N=15000
P=rng.normal(size=(N,3)); P/=np.linalg.norm(P,axis=1)[:,None]; P*=rng.random(N)[:,None]**(1/3)
# W0: edge along z, occupies azimuth in [-th/2, th/2]
az=np.arctan2(P[:,1],P[:,0])
inW0=np.abs(az)<th/2
def wedge_mask(p):  # p=(a,b,d1,psi,s)  face-1 normal angles a,b ; offset d1; edge direction angle psi in plane perp n1; s=edge position along perp-in-plane direction
    a,b,d1,psi,s=p
    n1=np.array([np.sin(a)*np.cos(b),np.sin(a)*np.sin(b),np.cos(a)])
    t1=np.cross(n1,[0.3,0.5,0.8]); t1/=np.linalg.norm(t1); t2=np.cross(n1,t1)
    e=np.cos(psi)*t1+np.sin(psi)*t2           # edge direction (in plane 1)
    u=np.cross(n1,e)                          # in-plane direction perp to edge
    # point on edge: q = d1 n1 + s u
    q=d1*n1+s*u
    # face 2 normal: rotate n1 about e by (pi - th): wedge interior dihedral th
    ang=np.pi-th
    n2=np.cos(ang)*n1+np.sin(ang)*np.cross(e,n1)+(1-np.cos(ang))*e*np.dot(e,n1)
    # interior wedge = {n1.(x-q)<=0, n2.(x-q)<=0}; choose sign so that wedge lies on u side? try both via flag in caller
    return n1,n2,q
def mk(p,flip):
    n1,n2,q=wedge_mask(p)
    if flip: 
        # reflect n2 across the plane containing e and n1 -> other side
        e=np.cross(n1,n2); e/=np.linalg.norm(e)
        n2=n2-2*np.dot(n2,np.cross(e,n1))*np.cross(e,n1)
    return (P-q)@n1<=0, (P-q)@n2<=0
def wedge(p,flip=False):
    A,B=mk(p,flip); return A&B
def cap(p):
    a,b,d=p
    n=np.array([np.sin(a)*np.cos(b),np.sin(a)*np.sin(b),np.cos(a)])
    return P@n>=d
bw=[(0,np.pi),(0,2*np.pi),(-1.2,1.2),(0,np.pi),(-3,3)]
bc=[(0,np.pi),(0,2*np.pi),(0,1)]
def run(kind,seed=0):
    # kind list e.g. ['cap','wedge']
    bounds=[]; 
    for k in kind: bounds+= bc if k=='cap' else bw
    def f(x):
        masks=[];i=0
        for k in kind:
            if k=='cap': masks.append(cap(x[i:i+3])); i+=3
            else:
                masks.append(wedge(x[i:i+5])); i+=5
        tot=0; ov=np.zeros(N,int)
        occ=inW0.astype(int)
        for m in masks: occ=occ+m.astype(int); tot+=m.mean()
        over=(occ>1).mean()
        return -tot+30*over
    r=differential_evolution(f,bounds,seed=seed,maxiter=120,popsize=15,tol=1e-8,polish=False)
    return r.fun,r.x
if __name__=="__main__":
    kind=sys.argv[1].split(','); 
    best=None
    for sd in range(int(sys.argv[2])):
        v,x=run(kind,sd)
        print(kind,sd,"obj",v,flush=True)
        if best is None or v<best[0]: best=(v,x)
    print("alpha=",al,"best max-vol-others ~",-best[0],"=> rho_hat ~",1-al+best[0])
