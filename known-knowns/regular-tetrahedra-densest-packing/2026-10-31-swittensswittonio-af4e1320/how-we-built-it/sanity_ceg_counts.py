"""Consistency check of the counting claims of REDUCTION.md section 4 (Q=40,k=38,u=0.0084) on the actual CEG 4000/4671 packing (NUMERICAL, not a proof):
 (a) #other tets having an edge-centre within delta=2u of a given centre  <= q-1 (=4)
 (b) #tets having an edge-centre within r_v of any vertex <= q_v (=9); centres per tet within r_v of vertex <= mv (=17)."""
import json, itertools, numpy as np
from fractions import Fraction as F
from scipy.spatial import cKDTree
d=json.load(open('../../../baseline/ceg_4000_4671.json'))
L=np.array([[float(F(x)) for x in r] for r in d['L']]); B=np.array([[[float(F(x)) for x in v] for v in b] for b in d['bodies']])
a=np.linalg.norm(B[0,0]-B[0,1]); L/=a; B/=a
k=38; u=0.0084; sigma=2*u; dd=(1-(k-1)*sigma)/2; GQ=0.7883351964594869; rv=u/(GQ*np.sqrt(2)/3); delta=2*u
print("edge",a,"d",dd,"rv",rv)
R=range(-3,4)
tets=[];cells=[]
for i,j,l in itertools.product(R,R,R):
    t=i*L[0]+j*L[1]+l*L[2]
    for bi in range(len(B)): tets.append(B[bi]+t); cells.append((i,j,l,bi))
tets=np.array(tets); n=len(tets)
edges=list(itertools.combinations(range(4),2))
cen=[];owner=[]
for ti,T in enumerate(tets):
    for (p,q) in edges:
        for s in range(k):
            x=dd+s*sigma; cen.append(T[p]+(T[q]-T[p])*x); owner.append(ti)
cen=np.array(cen);owner=np.array(owner)
tree=cKDTree(cen)
central=[ti for ti,c in enumerate(cells) if c[:3]==(0,0,0)]
# (a)
maxa=0; maxcent=0
for ti in central:
    idx=np.where(owner==ti)[0][::7]
    for i in idx:
        nb=tree.query_ball_point(cen[i],delta*(1-1e-9))
        others={owner[j] for j in nb if owner[j]!=ti}
        maxa=max(maxa,len(others))
        per={}
        for j in nb:
            if owner[j]!=ti: per[owner[j]]=per.get(owner[j],0)+1
        if per: maxcent=max(maxcent,max(per.values()))
print("(a) max #other tets with a centre within delta:",maxa,"(bound q-1=4);  max centres per other tet:",maxcent,"(bound m=2)")
# (b)
maxb=0;maxper=0
for ti in central:
    for w in tets[ti]:
        nb=tree.query_ball_point(w,rv)
        per={}
        for j in nb:
            if owner[j]!=ti: per[owner[j]]=per.get(owner[j],0)+1
        maxb=max(maxb,len(per)); 
        if per: maxper=max(maxper,max(per.values()))
print("(b) max #tets with a centre within rv of a vertex:",maxb,"(bound qv=9); max centres per tet:",maxper,"(bound mv=3)")

# (c) true uncovered fraction of deficit balls B(c,u) around good centres of the CEG packing (MC), to show the slack vs rho_hat
rng=np.random.default_rng(1)
V=tets
def inside_any(pts, cand):
    for ti in cand:
        T=V[ti]; M=np.stack([T[1]-T[0],T[2]-T[0],T[3]-T[0]],1)
        bc=np.linalg.solve(M,(pts-T[0]).T).T
        m=(bc>=0).all(1)&(bc.sum(1)<=1)
        if m.any(): yield m
vert_tree=cKDTree(tets.reshape(-1,3))
fr=[]
sel=[i for i in range(len(cen)) if owner[i] in central][::97]
for i in sel:
    c=cen[i]
    if len(vert_tree.query_ball_point(c,rv))>0: continue       # not good
    pts=c+u*rng.normal(size=(4000,3))/1; pts=c+(pts-c)/np.linalg.norm(pts-c,axis=1)[:,None]*u*rng.random(4000)[:,None]**(1/3)
    cand=[ti for ti in range(n) if np.linalg.norm(tets[ti].mean(0)-c)<1.2]
    cov=np.zeros(len(pts),bool)
    for m in inside_any(pts,cand): cov|=m
    fr.append(1-cov.mean())
print("(c) %d good centres sampled; uncovered fraction of B(c,u): min %.4f mean %.4f  (certified rho_hat(0,40) = 3.6e-12; conjectured 0.0204)"%(len(fr),min(fr),np.mean(fr)))
