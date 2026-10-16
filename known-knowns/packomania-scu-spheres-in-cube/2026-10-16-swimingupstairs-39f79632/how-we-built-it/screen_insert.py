"""Insertion screen: for each N in [lo,hi], take the COMPLETE posted listing scu<N-1>.txt (N-1 centres), find its largest hole h;
cand = min(r_listing(N-1), h). Report cand - r_table(N). Usage: screen_insert.py lo hi worker nworkers"""
import sys,os,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); sys.path.insert(0,H+'/../../../checker')
from hole import hole2; from scu_io import T,load,rad
lo,hi,w,nw=map(int,sys.argv[1:5]); out=open(H+'/../out/insert_%d.tsv'%w,'a')
for N in range(lo,hi+1)[w::nw]:
    C=load(N-1)
    if len(C)!=N-1: out.write('%d\tskip_listing_%d\n'%(N,len(C))); out.flush(); continue
    p,h,k,b=hole2(C); r=rad(C); cand=min(r,h)
    out.write('%d\t%.15f\t%.15f\t%.15f\t%.6e\t%d\t%s\t%s\n'%(N,r,h,T[N],cand-T[N],k,b,' '.join('%.17f'%v for v in p))); out.flush()
out.write('done\n')
