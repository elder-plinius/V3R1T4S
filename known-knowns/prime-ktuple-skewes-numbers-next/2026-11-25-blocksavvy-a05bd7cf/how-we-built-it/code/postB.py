# Independent comparison for sexyB counts, using mpmath (not Arb) and a monotone (not chord) bound.
#  For sub-block s = [u, u+65536): every pair start q in it satisfies pi6(q) <= N(u+65536) and Li2(q) >= Li2(u).
#  Li2(u) >= Li2(a) + (u-a)/log(u)^2 for a <= u (integrand decreasing), with Li2(a) by mpmath at a = multiples of 2^23.
#  So if N(u+65536) <= C*[Li2(a)+(u-a)/log(u)^2] - 1e-3 the whole sub-block is safe. Otherwise every pair of the
#  sub-block is dumped by sexyB and compared exactly with mpmath (50 digits). Stops at the first violation.
import sys, os, subprocess, numpy as np, mpmath as mp
mp.mp.dps=50
SUB=65536; A=1<<23
cnt=np.fromfile(sys.argv[1],dtype='<u4').astype(np.int64); exact_below=int(float(sys.argv[2])); stop_at=int(float(sys.argv[3])) if len(sys.argv)>3 else None
nsub=len(cnt); Nend=np.cumsum(cnt); Nstart=Nend-cnt
C=4*mp.mpf('0.6601618158468695739278121100145557784326233602847334133194484233')
c2=mp.li(2)-2/mp.log(2)
def Li2(x): x=mp.mpf(x); return mp.li(x)-x/mp.log(x)-c2
na=(nsub*SUB)//A+1
La=np.array([float(Li2(j*A)) if j*A>=2 else 0.0 for j in range(na)])
u=np.arange(nsub,dtype=np.float64)*SUB; a_idx=(np.arange(nsub)*SUB)//A; a=a_idx.astype(np.float64)*A
with np.errstate(divide='ignore',invalid='ignore'):
    low=C.__float__()*(La[a_idx]+(u-a)/np.log(np.maximum(u,3.0))**2)*(1-1e-15)-1e-3
safe=(cnt==0)|(Nend<=low)
check=np.arange(nsub)*SUB>=exact_below
flag=np.nonzero(check & ~safe)[0]
print(f'subblocks={nsub} range=[0,{nsub*SUB}) pairs={cnt.sum()} monotone-safe={int((safe&check).sum())} flagged={len(flag)} (start>={exact_below}) flagged_before_stop={int((flag*SUB<(stop_at or 1<<62)).sum())}',flush=True)
mins=None; first=None; nexact=0
for s in flag.tolist():
    if stop_at and s*SUB>=stop_at: break
    out=subprocess.run([os.environ.get('SEXYB','./code/sexyB'),'dump',str(s*SUB),str((s+1)*SUB)],capture_output=True,text=True,check=True).stdout.split()
    assert len(out)==cnt[s], (s,len(out),cnt[s])
    N=int(Nstart[s])
    for q in map(int,out):
        N+=1; v=C*Li2(q)-N; nexact+=1
        if v<0: first=(q,N,C*Li2(q)); break
        if mins is None or v<mins[0]: mins=(v,q,N)
    if first: break
print('exactly compared pairs:',nexact,' min exact margin before first violation:',(mp.nstr(mins[0],12),mins[1],mins[2]) if mins else None)
if first: print(f'FIRST VIOLATION q={first[0]} pi6(q)={first[1]} C*Li2(q)={mp.nstr(first[2],25)} diff={mp.nstr(first[2]-first[1],15)} subblock={first[0]//SUB}')
