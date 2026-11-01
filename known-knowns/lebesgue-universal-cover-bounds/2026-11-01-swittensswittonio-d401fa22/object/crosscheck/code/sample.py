import sys, os; sys.path.insert(0,'code'); import lowprio; print('PID',lowprio.set_below_normal(),flush=True)
import json, re, random, time, collections
import numpy as np
from leafdec import Cert, BlockIndex, CIRC5
c=Cert('work/cert_B_08344.bin')
rng=np.random.default_rng(20261031); random.seed(20261031)
DUMP='<previous-run leaf dump (not shipped)>'
tot=int(c.cum[-1]); print('total leaves',tot,'nodes',2*tot-c.nseed,'forest identity',2*tot-c.nseed==486799600)
samples={}
def add(seed,k,dp,box,strat,extra=None):
    key=(int(seed),int(k))
    d=samples.setdefault(key,{'seed':int(seed),'k':int(k),'gid':int(c.cum[seed])+int(k),'depth':int(dp),'box':list(box),'strata':[]})
    if strat not in d['strata']: d['strata'].append(strat)
    if extra: d.update(extra)
HEAVY=20000
poolD=[]   # (seed,k,depth,box) uniform-by-leaf pool for depth strata
t=time.time()
# --- U
g=np.sort(rng.choice(tot,size=1000,replace=False)); blk=np.searchsorted(c.cum,g,side='right')-1
byblk=collections.defaultdict(list)
for gi,bi in zip(g,blk): byblk[int(bi)].append(int(gi-c.cum[bi]))
g2=np.sort(rng.choice(tot,size=12000,replace=False)); blk2=np.searchsorted(c.cum,g2,side='right')-1
byblk2=collections.defaultdict(list)
for gi,bi in zip(g2,blk2): byblk2[int(bi)].append(int(gi-c.cum[bi]))
for bi in byblk2: byblk.setdefault(bi,[])
for bi,ks in byblk.items():
    if c.leaves[bi]>HEAVY:
        ix=BlockIndex(c,bi); z=ix.zeros(); assert len(z)==c.leaves[bi]
        for k in ks:
            b,dp=ix.descend_to_pos(int(z[k])); add(bi,k,dp,b,'U')
        for k in byblk2[bi]:
            b,dp=ix.descend_to_pos(int(z[k])); poolD.append((bi,k,dp,b))
        del ix
    else:
        S=set(ks); S2=set(byblk2[bi])
        for k,dp,b in c.walk(bi):
            if k in S: add(bi,k,dp,b,'U')
            if k in S2: poolD.append((bi,k,dp,b))
print('U done',len(byblk),'blocks',len(samples),time.time()-t,flush=True)
# --- W
rows=[]
for line in open(DUMP,encoding='ascii',errors='ignore'):
    if line.startswith('LEAF '):
        m=re.match(r'LEAF (\d+) \[([^\]]*)\] (\S+)',line)
        rows.append((float(m.group(3)),int(m.group(1)),tuple(float(x) for x in m.group(2).split(','))))
rows.sort(); print('dump leaves',len(rows),'lowest LB',rows[0][0],rows[999][0])
byseed=collections.defaultdict(list)
for lb,sd,box in rows[:1000]: byseed[sd].append((lb,box))
nmatch=0; nmiss=0
for sd,lst in byseed.items():
    if c.leaves[sd]>HEAVY:
        ix=BlockIndex(c,sd)
        for lb,box in lst:
            r=ix.descend_to_box(box)
            if r is None: nmiss+=1
            else: add(sd,r[0],r[1],box,'W',{'prev_lb':lb}); nmatch+=1
        del ix
    else:
        boxes={tuple(b):lb for lb,b in lst}; found=set()
        for k,dp,b in c.walk(sd):
            if b in boxes: add(sd,k,dp,b,'W',{'prev_lb':boxes[b]}); nmatch+=1; found.add(b)
        nmiss+=len(boxes)-len(found)
print('W matched',nmatch,'missed',nmiss,'seeds',len(byseed),time.time()-t,flush=True)
# --- global worst boxes (seed unknown in dump): locate by descending from the root
def find_seed(box):
    b=c.root; i=0
    for _ in range(c.depth):
        c1,c2=c.split(b); w=(b[1],b[3],CIRC5*b[5],b[7],b[9]); ax=int(np.argmax(w))
        if box[2*ax]<b[2*ax]: i=2*i; b=c1
        else: i=2*i+1; b=c2
    return i
for lb,sd,box in rows:
    if sd==0 and lb<0.8344160:
        sdd=find_seed(box); assert tuple(c.seed_box(sdd))!=None
        ix=BlockIndex(c,sdd) if c.leaves[sdd]>HEAVY else None
        if ix is not None:
            r=ix.descend_to_box(box)
        else:
            r=None
            for k,dp,b in c.walk(sdd):
                if b==box: r=(k,dp)
        print('global worst box found: seed',sdd,'result',r,'prev lb',lb)
        if r is not None: add(sdd,r[0],r[1],box,'W',{'prev_lb':lb})
# --- D
cand=[int(i) for i in rng.permutation(c.nseed)[:20000] if c.leaves[i]<=30000][:300]
for bi in cand:
    for k,dp,b in c.walk(bi):
        if dp>22 or random.random()<0.02: poolD.append((bi,k,dp,b))
pool=collections.defaultdict(list)
for bi,k,dp,b in poolD: pool[dp].append((bi,k,b))
print('depth pool',{d:len(v) for d,v in sorted(pool.items())},time.time()-t,flush=True)
quota=45
for dp,v in sorted(pool.items()):
    for bi,k,b in random.sample(v,min(quota,len(v))): add(bi,k,dp,b,'D')
Sx=sorted(samples.values(),key=lambda d:d['gid'])
json.dump(Sx,open('work/sample.json','w'))
print('total distinct',len(Sx),collections.Counter(s for d in Sx for s in d['strata']),'depth hist',sorted(collections.Counter(d['depth'] for d in Sx).items()))
