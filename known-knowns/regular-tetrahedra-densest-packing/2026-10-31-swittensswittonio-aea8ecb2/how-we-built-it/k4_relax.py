import numpy as np, math
from scipy.optimize import minimize
V=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/(2*math.sqrt(2))
faces=[(1,2,3),(0,2,3),(0,1,3),(0,1,2)]
def prep():
    out=[]
    for f in faces:
        a,b,c=(V[i] for i in f); n=np.cross(b-a,c-a); n/=np.linalg.norm(n)
        cen=(a+b+c)/3
        if n@(cen-V.mean(0))<0: n=-n          # outward
        edges=[]
        for (p,q,r) in [(a,b,c),(b,c,a),(c,a,b)]:
            t=q-p; m=np.cross(n,t); m/=np.linalg.norm(m)      # in-plane normal of edge pq
            if m@(r-p)>0: m=-m                                 # outward from triangle
            edges.append((p,m))
        out.append((a,n,edges))
    return out
P=prep()
def lb_tri(O):
    ds=[]
    for a,n,edges in P:
        h=abs(n@(O-a)); out=max(max(m@(O-p) for p,m in edges),0.0)
        ds.append(math.hypot(h,out))
    return sorted(ds)
def inside(O):
    return all(n@(O-a)< 0 for a,n,e in P)
def ratio(O):
    if inside(O): return 0.0
    d=lb_tri(O); D=min(np.linalg.norm(O-v) for v in V)
    return D/max(d[2],1e-12)
rng=np.random.default_rng(1)
best=(0,None)
for it in range(200000):
    O=rng.uniform(-0.9,0.9,3)
    r=ratio(O)
    if r>best[0]: best=(r,O.copy())
print("relaxed random sup",best)
res=[]
for k in range(40):
    O0=best[1]+rng.normal(size=3)*0.05 if k<20 else rng.uniform(-0.8,0.8,3)
    r=minimize(lambda O:-ratio(O),O0,method="Nelder-Mead",options=dict(xatol=1e-12,fatol=1e-14,maxiter=4000))
    res.append((-r.fun,r.x))
res.sort(key=lambda t:-t[0])
for v,x in res[:3]: print("relaxed local max %.10f at %s"%(v,x))
print("3/sqrt2",3/math.sqrt(2))
