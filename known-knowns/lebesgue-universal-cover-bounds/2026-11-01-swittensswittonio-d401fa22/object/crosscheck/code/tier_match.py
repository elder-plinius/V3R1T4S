import sys,csv,random; sys.path.insert(0,'code')
from leafdec import *; from bound import *
c=Cert('work/cert_B_08344.bin')
R=list(csv.DictReader(open('outputs/cross_vs_interval.tsv'),delimiter='\t')); random.seed(5)
import collections
top=collections.Counter(r['seed'] for r in R).most_common(1)[0][0]
sm=random.sample([r for r in R if r['seed']==top],25)
print(len(sm))
import numpy as np
res={N:[] for N in (128,256,512,1024,2048)}
for r in sm:
    sd=int(r['seed']);pos=int(r['pos'])
    ix=BlockIndex(c,sd); b,dp=ix.descend_to_pos(pos-1)
    for N in res:
        a=hull_bound(b,N)[0]; res[N].append(float(r['interval_lb'])-float(a))
for N,v in res.items(): print(N,'interval-mine: min %.3e max %.3e mean %.3e'%(min(v),max(v),sum(v)/len(v)))
