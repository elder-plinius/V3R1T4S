"""chain.py SRC N0 STEPS PEN_SECS OUTDIR: from a config with N0 spheres, repeat STEPS times: add one sphere at the largest hole
(hole2), penalty-inflate PEN_SECS, save OUTDIR/scu<N>_chain.txt, log r vs live table and vs the Moki&Julio queued value."""
import sys,os,csv,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); sys.path.insert(0,H+'/../../../checker'); sys.path.insert(0,H+'/../../evaluator-first/code')
from plib import inflate,rad; from hole import hole2; from scu_io import loadf,T,D
MJ={int(r['N']):float(r['new_radius']) for r in csv.DictReader(open(D+'mj_github/MANIFEST.csv')) if r['shelf']=='scu'}
src,N0,K,ps,od=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]),sys.argv[5]; os.makedirs(od,exist_ok=True)
X=loadf(src); assert len(X)==N0; log=open(od+'/chain_from%d.log'%N0,'a')
for s in range(K):
    p,h,k,b=hole2(X); X=np.vstack([X,p]); N=len(X); r0=rad(X)
    X,r=inflate(X,ps); np.savetxt(od+'/scu%d_chain.txt'%N,X,fmt='%.20f')
    mj=MJ.get(N,float('nan'))
    log.write('N=%d insert_r=%.15f relaxed_r=%.15f table=%.15f d_table=%.3e MJ=%.15f d_MJ=%.3e\n'%(N,r0,r,T[N],r-T[N],mj,r-mj)); log.flush()
    if r<T[N] and not (r<mj): pass
