"""Compute certified lower bounds for all sampled leaves; resumable; writes outputs/leaf_table.tsv"""
import sys, json, os, time
sys.path.insert(0,'code'); import lowprio; print('PID',lowprio.set_below_normal(),flush=True)
sys.path.insert(0,'code'); sys.path.insert(0,'<author repo src (format only)>')
from fractions import Fraction
import numpy as np
from bound import leaf_bound, TAU
import verifyB as A      # author's bound, used ONLY as a comparison column, never inside bound.py
from scipy.spatial import ConvexHull
ang=2*np.pi*np.arange(1024)/1024; ring=np.stack([0.5*np.cos(ang),0.5*np.sin(ang)],1)
def author_lb(b): return float(A.box_bound(tuple(b),ring,1024,None,lambda P:ConvexHull(P).volume))
S=json.load(open('work/sample.json')); out='outputs/leaf_table.tsv'
done=set()
if os.path.exists(out):
    for l in open(out):
        if not l.startswith('gid'): done.add(int(l.split('\t')[0]))
f=open(out,'a')
if not done: f.write('gid\tseed\tk\tdepth\tstrata\tlb_certified\tslack_vs_0.8344\taccepted\tapriori_lb\thull_lb_N1024\thull_lb_N4096\thull_lb_N16384\tauthor_double_lb\tprev_run_lb\td3\td5\n')
t=time.time(); n=0
for s in S:
    if s['gid'] in done: continue
    r=leaf_bound(s['box']); lbF=max(r['hullF'],Fraction(r['ap']))
    acc=lbF>=TAU+Fraction(1,10**12)
    f.write('\t'.join(map(str,[s['gid'],s['seed'],s['k'],s['depth'],'+'.join(s['strata']),repr(float(lbF)),repr(float(lbF-TAU)),int(acc),repr(r['ap']),repr(r['tiers'][1024]),repr(r['tiers'][4096]),repr(r['tiers'][16384]),repr(author_lb(s['box'])),repr(s.get('prev_lb','')),r['d3'],r['d5']]))+'\n'); f.flush(); n+=1
    if n%100==0: print(n,time.time()-t,flush=True)
print('done',n)
