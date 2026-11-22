import sys,subprocess,time,os
sys.path.insert(0,'.')
from rq import rq
from mpmath import mp,nstr
mp.dps=80
cyc=int(sys.argv[1]); ms=range(int(sys.argv[2]),int(sys.argv[3])+1); iters=int(sys.argv[4])
out='lam_%s.txt'%('cyc' if cyc else 'open')
for m in ms:
    t=time.time(); pre='bin_%d_%d'%(cyc,m)
    subprocess.run(['./tm',str(m),str(cyc),str(iters),'12',pre],check=True,stderr=subprocess.DEVNULL)
    l=rq(pre,m); os.remove(pre+'.bin')
    open(out,'a').write('%d %d %s\n'%(m,iters,nstr(l,70)))
    print(m,nstr(l,50),time.time()-t,flush=True)
