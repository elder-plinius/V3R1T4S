import json, itertools
from fractions import Fraction as F
edges=set()
for i,l in enumerate(open('../../../data/hervay_inputs/certificate/search.cert','rb')):
    if i==0: continue
    d=json.loads(l.split(b' ',1)[1])
    if d['component']=='Global': edges.add(tuple(d['edge']))
h=F(1,2)
one=(F(1),F(0)); phi=(h,h); phi2=(3*h,h); phi3=(F(2),F(1)); two_phi=(F(1),F(1)); twoplus=(5*h,h); zero=(F(0),F(0))
neg=lambda x:(-x[0],-x[1])
fams=[(one,one,phi3),(phi2,phi,two_phi),(twoplus,zero,phi2)]
allv=set()
for f in fams:
    for p in [f,(f[1],f[2],f[0]),(f[2],f[0],f[1])]:
        for s in itertools.product((1,-1),repeat=3):
            allv.add(tuple(c if si>0 else neg(c) for c,si in zip(p,s)))
allv=list(allv); print(len(allv))
val=lambda x: float(x[0])+float(x[1])*5**.5
def dist2(u,v):
    return sum((val(a)-val(b))**2 for a,b in zip(u,v))
for name,key in [('tuple',lambda v:v),('numeric',lambda v:tuple(val(c) for c in v))]:
  for rev in (False,True):
    V=sorted(allv,key=key,reverse=rev)
    bad=sum(1 for a,b in edges if abs(dist2(V[a],V[b])-4)>1e-6)
    print(name,rev,bad)
