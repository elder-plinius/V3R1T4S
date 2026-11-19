import sys
from math import prod
B0=168131152814624
primes=[3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]
nodes=0; band=0; bandab=0; ab=0
stack=[(0,1,(),1,1)]
bandprofiles=[]
while stack:
    idx,v,ex,sn,sd=stack.pop()
    nodes+=1
    if idx>0:
        if sn>=2*sd: ab+=1
        if 3*v>B0:
            band+=1
            if sn>=2*sd: bandab+=1; bandprofiles.append(ex)
    p=primes[idx]; pe=p; e=1
    while v*pe<=B0:
        stack.append((idx+1,v*pe,ex+(e,),sn*((pe*p-1)//(p-1)),sd*pe)); pe*=p; e+=1
print("nodes",nodes,"abundant",ab,"band",band,"band&abundant",bandab)
# leaves for dictionary-free vs dict
rows=[l.split('\t') for l in open(sys.argv[1]).read().splitlines()[1:]]
tot_leaf=0; tot_dict=0; mx=0
for r in rows:
    ex=tuple(map(int,r[0].split(',')))
    keys={1}
    for i in range(len(ex)):
        tot_leaf+=prod(e+1 for e in ex[:i]); tot_dict+=len(keys); mx=max(mx,len(keys))
        keys={k*(1+t) for k in keys for t in range(ex[i]+1)}
print("leaf",tot_leaf,"dict",tot_dict,"maxdict",mx)
