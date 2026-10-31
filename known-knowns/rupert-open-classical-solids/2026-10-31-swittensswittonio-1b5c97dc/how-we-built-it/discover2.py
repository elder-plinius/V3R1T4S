import json, itertools
phi=(1+5**.5)/2
fams=[(1,1,phi**3),(phi**2,phi,2*phi),(2+phi,0,phi**2)]
edges=set()
for i,l in enumerate(open('../../../data/hervay_inputs/certificate/search.cert','rb')):
    if i==0: continue
    d=json.loads(l.split(b' ',1)[1])
    if d['component']=='Global': edges.add(tuple(d['edge']))
def key(v): return tuple(round(x,9)+0.0 for x in v)
res=[]
for fo in itertools.permutations(range(3)):
 for cyc in (1,2):
  for po in (True,False):
   for bo in itertools.permutations(range(3)):   # bo[k]=coordinate whose sign varies with weight 2^(2-k)
    for pol in itertools.product((1,-1),repeat=3):  # first sign choice per coordinate
     for dedup_first in (True,):
      out=[];seen=set()
      for f in fo:
        base=fams[f]
        perms=[tuple(base[(j*cyc+i)%3] for i in range(3)) for j in range(3)]
        signs=[]
        for m in range(8):
            s=[0,0,0]
            for k in range(3):
                bit=(m>>(2-k))&1
                s[bo[k]]= pol[bo[k]]*(1-2*bit)
            signs.append(tuple(s))
        combos=[(p,s) for p in perms for s in signs] if po else [(p,s) for s in signs for p in perms]
        for p,s in combos:
            v=key([a*b for a,b in zip(p,s)])
            if v in seen: continue
            seen.add(v); out.append(v)
      if len(out)!=60: continue
      bad=sum(1 for a,b in edges if abs(sum((x-y)**2 for x,y in zip(out[a],out[b]))-4)>1e-6)
      res.append((bad,fo,cyc,po,bo,pol))
res.sort(); print(len(res)); print(res[:10])
