import json, itertools, collections
from fractions import Fraction as F
import numpy as np
S5=5**.5; phi=(1+S5)/2
recs=[]
for i,l in enumerate(open('../../../data/hervay_inputs/certificate/search.cert','rb')):
    if i==0: continue
    d=json.loads(l.split(b' ',1)[1])
    if d['component']=='Domain': recs.append(d)
print(collections.Counter(r['inequality'] for r in recs))
def box(path):
    lo=[0,0,-.4,-.4,-.4]; hi=[2/3,.4,.4,.4,.4]
    for k,ch in enumerate(path):
        a=k%5; m=(lo[a]+hi[a])/2
        if ch=='0': hi[a]=m
        else: lo[a]=m
    return lo,hi
# Q: tuples of (a,b) pairs
h=F(1,2)
def el(a,b=0): return (F(a),F(b))
Q=set()
for i in range(4):
    for sg in (1,-1):
        q=[el(0)]*4; q[i]=el(sg); Q.add(tuple(q))
for s in itertools.product((1,-1),repeat=4): Q.add(tuple(el(h*x) for x in s))
# even perms of 1/2(0,±1,±phi,±(phi-1)); phi=(1/2,1/2); phi-1=(-1/2,1/2)
base=[el(0),el(h),(h*h,h*h),(-h*h,h*h)]  # 1/2*(0,1,phi,phi-1)
def evenperm(p):
    inv=sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j]); return inv%2==0
for p in itertools.permutations(range(4)):
    if not evenperm(p): continue
    for s in itertools.product((1,-1),repeat=4):
        q=tuple((s[k]*base[p[k]][0],s[k]*base[p[k]][1]) for k in range(4))
        Q.add(q)
print(len(Q))
val=lambda x: float(x[0])+float(x[1])*S5
def firstpos(q):
    for c in q:
        if c!=(0,0): return c[0]>0 or (c[0]==0 and c[1]>0) if False else val(c)>0
Qp=[q for q in Q if firstpos(q)]
print(len(Qp))
def ell(q,u,r):
    be=val(q[0]); b=np.array([val(c) for c in q[1:]])
    u=np.array(u); r=np.array(r)
    return -be*u.dot(r)-b.dot(u+np.cross(u,r))
def viol(q,lo,hi):
    vals=[]
    for sc in itertools.product((0,1),repeat=2):
        s=(lo[0],hi[0])[sc[0]]; t=(lo[1],hi[1])[sc[1]]
        for rc in itertools.product((0,1),repeat=3):
            r=[(lo[2+k],hi[2+k])[rc[k]] for k in range(3)]
            vals.append((ell(q,(s,t,1),r),s,t))
    sg=np.sign(vals[0][0])
    return all(np.sign(v)==sg and v*v>1+s*s+t*t+1e-12 for v,s,t in vals)
fold=[r for r in recs if r['inequality']>=13]
print(len(fold))
cand=collections.defaultdict(collections.Counter)
for r in fold:
    lo,hi=box(r['path'])
    ok=[k for k,q in enumerate(Qp) if viol(q,lo,hi)]
    cand[r['inequality']].update(ok)
# for each inequality idx, which Qp elements valid in all records
byidx=collections.defaultdict(list)
for r in fold: byidx[r['inequality']].append(r)
for idx in sorted(byidx):
    n=len(byidx[idx]); 
    full=[k for k,c in cand[idx].items() if c==n]
    print(idx,n,full[:8])
json.dump({'Qp':[[ [str(c[0]),str(c[1])] for c in q] for q in Qp]},open('qp_unordered.json','w'))
