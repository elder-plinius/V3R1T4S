import sys, os, json, time, random, collections
sys.path.insert(0,'code'); import lowprio; print('PID',lowprio.set_below_normal(),flush=True)
import numpy as np
from fractions import Fraction
from leafdec import Cert, BlockIndex
from bound import leaf_bound, TAU
c=Cert('work/cert_B_08344.bin')
LOG='work/full_leaflog.txt'
L=[]
for l in open(LOG):
    p=l.split()
    if len(p)>=4: L.append((int(p[0]),int(p[1]),float(p[3]),p[2]))
print('log entries',len(L),flush=True)
random.seed(77)
low=sorted(L,key=lambda t:t[2])[:600]; lowset={(t[0],t[1]) for t in low}
rest=[t for t in L if (t[0],t[1]) not in lowset and t[2]<0.9]   # hull leaves only
pick=low+random.sample(rest,900)
byseed=collections.defaultdict(list)
for t in pick: byseed[t[0]].append(t)
out=open('outputs/cross_vs_interval.tsv','w')
out.write('seed\tpos\tdepth\tpick\tinterval_lb\tmy_lb_certified\tmy_N1024\tmy_N4096\tmy_N16384\tdiff_interval_minus_mine\taccepted\n')
t0=time.time(); n=0
for sd,lst in byseed.items():
    ix=BlockIndex(c,sd)
    for (s,pos,v,hx) in lst:
        assert ix.bits[pos-1]==0, (s,pos)
        b,dp=ix.descend_to_pos(pos-1)
        r=leaf_bound(b); lb=r['hullF']; 
        out.write('\t'.join(map(str,[s,pos,dp,'low' if (s,pos) in lowset else 'rand',repr(v),repr(float(lb)),repr(r['tiers'][1024]),repr(r['tiers'][4096]),repr(r['tiers'][16384]),repr(v-float(lb)),int(lb>=TAU+Fraction(1,10**12))]))+'\n'); out.flush(); n+=1
        if n%100==0: print(n,time.time()-t0,flush=True)
    del ix
print('done',n)
