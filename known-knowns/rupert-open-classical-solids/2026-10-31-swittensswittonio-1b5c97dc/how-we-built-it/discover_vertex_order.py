# discovery only: find which natural vertex ordering makes every certificate "edge" pair an RID edge (float, tolerance)
import json, itertools, math
phi=(1+5**.5)/2
fams=[(1,1,phi**3),(phi**2,phi,2*phi),(2+phi,0,phi**2)]
edges=set(); verts=set()
for i,l in enumerate(open('../../../data/hervay_inputs/certificate/search.cert','rb')):
    if i==0: continue
    d=json.loads(l.split(b' ',1)[1])
    if d['component']=='Global': edges.add(tuple(d['edge'])); verts.add(d['vertex'])
print(len(edges),len(verts),max(max(e) for e in edges),max(verts))
def build(perm_outer, signorder, famorder):
    out=[];seen=set()
    for f in famorder:
        base=fams[f]
        perms=[base,(base[1],base[2],base[0]),(base[2],base[0],base[1])]
        signs=list(itertools.product(*[(1,-1) if s>0 else (-1,1) for s in signorder]))
        combos=[(p,s) for p in perms for s in signs] if perm_outer else [(p,s) for s in signs for p in perms]
        for p,s in combos:
            v=tuple(round(a*b,9) for a,b in zip(p,s))
            v=tuple(x+0.0 for x in v)
            if v in seen: continue
            seen.add(v); out.append(v)
    return out
best=[]
for po in (True,False):
  for so in itertools.product((1,-1),repeat=3):
    for fo in itertools.permutations(range(3)):
      V=build(po,so,fo)
      if len(V)!=60: continue
      bad=sum(1 for a,b in edges if abs(sum((x-y)**2 for x,y in zip(V[a],V[b]))-4)>1e-6)
      best.append((bad,po,so,fo))
best.sort(); print(best[:5])
print(sorted(edges))
allv=set()
for f in range(3):
    base=fams[f]
    for p in [base,(base[1],base[2],base[0]),(base[2],base[0],base[1])]:
        for s in itertools.product((1,-1),repeat=3):
            allv.add(tuple(round(a*b,9)+0.0 for a,b in zip(p,s)))
allv=list(allv); print(len(allv))
import functools
def test(V,name):
    bad=sum(1 for a,b in edges if abs(sum((x-y)**2 for x,y in zip(V[a],V[b]))-4)>1e-6)
    print(name,bad)
for rev in (False,True):
    for key in ('lex','lexneg','norm'):
        V=sorted(allv,key=(lambda v:v) if key=='lex' else (lambda v:tuple(-x for x in v)) if key=='lexneg' else (lambda v:(sum(x*x for x in v),v)),reverse=rev)
        test(V,(rev,key))
