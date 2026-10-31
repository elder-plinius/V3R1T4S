"""NUMERICAL sanity of the necessity claim (N): if at most two closed face triangles are within distance < r of O then
T ∩ B(O,r) = B(O,r) ∩ (intersection of the half-spaces of those faces)  [or T∩B empty].  Random T-frame (fixed T), random O, r."""
import numpy as np, math
from k4_num import V, faces, pt_tri
rng=np.random.default_rng(7)
nrm=[]; off=[]
for k in range(4):
    n=-V[k]; nrm.append(n/np.linalg.norm(n)); off.append(-1/ math.sqrt(3)*(-1) if False else None)
# half-space of face k (T side): V_k.x >= -1  (V unnormalised scaled by 1/(2sqrt2) in k4_num -> use the k4_num coordinates directly)
Vs=V; 
def face_hs(k,x):                        # True if x on T side of face opposite vertex k (uses k4_num's scale)
    n=Vs[k]-Vs[[i for i in range(4) if i!=k]].mean(0)   # points from face centroid to the opposite vertex = inward normal
    c=Vs[[i for i in range(4) if i!=k]].mean(0)
    return (x-c)@n>=0
bad=0; tested=0; npts=3000
for it in range(6000):
    O=rng.uniform(-0.8,0.8,3); r=rng.uniform(0.02,0.6)
    d=[np.linalg.norm(O-pt_tri(O,*(Vs[i] for i in f))) for f in faces]
    S=[k for k in range(4) if d[k]<r]
    if len(S)>2: continue
    pts=rng.normal(size=(npts,3)); pts/=np.linalg.norm(pts,axis=1)[:,None]; pts=O+pts*r*rng.random(npts)[:,None]**(1/3)
    inT=np.ones(npts,bool)
    for k in range(4): inT&=face_hs(k,pts)
    W=np.ones(npts,bool)
    for k in S: W&=face_hs(k,pts)
    tested+=1
    if (inT!=W).any() and inT.any(): bad+=1
print("tested cases (<=2 close faces, T∩B nonempty or not):",tested,"; cases where T∩B differs from the <=2-half-space wedge (and T∩B nonempty):",bad)
