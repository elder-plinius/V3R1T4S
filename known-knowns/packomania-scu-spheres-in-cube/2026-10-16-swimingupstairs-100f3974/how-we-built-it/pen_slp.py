"""pen_slp.py SRC N OUTPREFIX PEN_SECS SLP_SECS [DELTA0]: penalty inflation (coarse) then sparse SLP polish (Delta<=1e-6). Saves OUTPREFIX_best.txt whenever the true radius rises."""
import sys,os,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); sys.path.insert(0,H+'/../../../checker')
from plib import inflate,rad; import slp; from scu_io import loadf
src,N,out,ps,ss=sys.argv[1],int(sys.argv[2]),sys.argv[3],float(sys.argv[4]),float(sys.argv[5]); d0=float(sys.argv[6]) if len(sys.argv)>6 else 1e-7
X=loadf(src); assert len(X)==N,(len(X),N); log=open(out+'.log','a'); r0=rad(X); log.write('start %s N=%d r=%.17f\n'%(src,N,r0)); log.flush()
np.savetxt(out+'_best.txt',X,fmt='%.20f')
if ps>0: X,r=inflate(X,ps,log=log,save=out+'_best.txt'); log.write('penalty done r=%.17f gain=%.3e\n'%(r,r-r0)); log.flush()
if ss>0: X,r=slp.slp(X,ss,log=log,save=out+'_best.txt',Delta=d0,minDelta=1e-13); log.write('slp done r=%.17f gain=%.3e\n'%(r,r-r0))
log.write('final r=%.17f\n'%rad(np.loadtxt(out+'_best.txt'))); log.close()
