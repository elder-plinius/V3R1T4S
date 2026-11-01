import sys, subprocess, time, numpy as np, cupy as cp
sys.path.insert(0,'.')
import gil_gpu as g
NB=1<<22; lo=1500000000000001
p=g.Pipe(NB=NB, cap=NB)
n=p.sieve(lo,0); cp.cuda.Stream.null.synchronize()
P=p.P[:n].get()
hi=lo+2*NB
r=subprocess.run(['primesieve',str(lo),str(hi-1),'--print'],capture_output=True,text=True)
Q=np.array([int(x) for x in r.stdout.split()],dtype=np.uint64)
print('gpu',n,'primesieve',len(Q),'equal',len(Q)==n and bool((Q==P).all()))
nch=(n-g.O-1)//g.M
d=cp.zeros(nch,dtype=cp.uint16); cl=cp.zeros(nch,dtype=cp.uint8)
p.rows(nch,0,d,cl); cp.cuda.Stream.null.synchronize()
d=d.get()
ref=[g.ref_depth(Q,c) for c in range(nch)]
print('chunks',nch,'depths',d[:10].tolist(),'ref',ref[:10],'match',list(d)==ref, 'max',d.max())

print('clean',cl.get().tolist()[:10],'ref',[g.ref_clean(Q,c) for c in range(min(nch,6))])
