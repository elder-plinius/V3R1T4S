"""K4 (GEK Lemma 3.5): T unit-edge regular tetra, O not in int T, all vertices at distance > 3r/sqrt2 from O  => T∩B(O,r) is a B-wedge.
Necessary condition for NOT being a wedge: >=3 of the 4 closed face triangles come within distance < r of O  (derivation in REPORT).
Compute sup over O (outside int T) of  D(O)/r3(O), D=min vertex distance, r3 = 3rd smallest triangle distance."""
import numpy as np, math
from scipy.optimize import minimize
V=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/(2*math.sqrt(2))   # edge 1
faces=[(1,2,3),(0,2,3),(0,1,3),(0,1,2)]
def pt_tri(p,a,b,c):
    # closest point on triangle (Ericson)
    ab=b-a; ac=c-a; ap=p-a
    d1=ab@ap; d2=ac@ap
    if d1<=0 and d2<=0: return a
    bp=p-b; d3=ab@bp; d4=ac@bp
    if d3>=0 and d4<=d3: return b
    vc=d1*d4-d3*d2
    if vc<=0 and d1>=0 and d3<=0: return a+ab*(d1/(d1-d3))
    cp=p-c; d5=ab@cp; d6=ac@cp
    if d6>=0 and d5<=d6: return c
    vb=d5*d2-d1*d6
    if vb<=0 and d2>=0 and d6<=0: return a+ac*(d2/(d2-d6))
    va=d3*d6-d5*d4
    if va<=0 and (d4-d3)>=0 and (d5-d6)>=0:
        w=(d4-d3)/((d4-d3)+(d5-d6)); return b+(c-b)*w
    den=1/(va+vb+vc); v=vb*den; w=vc*den
    return a+ab*v+ac*w
def dists(O):
    return sorted(np.linalg.norm(O-pt_tri(O,*(V[i] for i in f))) for f in faces)
def inside(O):
    # inside tetra? barycentric
    M=np.vstack([V.T,np.ones(4)]); lam=np.linalg.solve(M,np.append(O,1)); return (lam>1e-12).all()
def ratio(O):
    if inside(O): return 0.0
    d=dists(O); D=min(np.linalg.norm(O-v) for v in V)
    return D/max(d[2],1e-12)
if __name__=='__main__':
    rng=np.random.default_rng(0)
    best=(0,None)
    for it in range(300000):
        O=rng.uniform(-1.2,1.2,3)*0.7
        r=ratio(O)
        if r>best[0]: best=(r,O.copy())
    print("random sup",best, "3/sqrt2=",3/math.sqrt(2))
    res=[]
    for k in range(60):
        O0=best[1]+rng.normal(size=3)*0.05 if k<30 else rng.uniform(-0.8,0.8,3)
        r=minimize(lambda O:-ratio(O),O0,method="Nelder-Mead",options=dict(xatol=1e-12,fatol=1e-14,maxiter=4000))
        res.append((-r.fun,r.x))
    res.sort(key=lambda t:-t[0])
    for v,x in res[:5]: print("local max ratio %.10f at O=%s dists=%s D=%.6f"%(v,x,dists(x),min(np.linalg.norm(x-v_) for v_ in V)))
