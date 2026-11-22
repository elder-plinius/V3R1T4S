import sys,time
sys.path.insert(0,'{WORKDIR}')
from rqlean import lam
from mpmath import mp,nstr
mp.dps=80
iters=int(sys.argv[1]); out=sys.argv[2]
for m in [int(x) for x in sys.argv[3:]]:
    t=time.time(); l=lam(m,iters)
    open(out,'a').write('%d %d %s\n'%(m,iters,nstr(l,70)))
    print(m,nstr(l,45),'%.0fs'%(time.time()-t),flush=True)
