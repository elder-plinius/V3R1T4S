# Exact per-pair comparison inside [a,b): numpy segmented sieve + Arb Li2. N0 = number of sexy-pair starts < a.
import sys, numpy as np
from flint import arb, ctx
ctx.prec=200
a,b,N0=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]); stop_first='--all' not in sys.argv
C=4*arb('0.6601618158468695739278121100145557784326233602847334133194484233')
two=arb(2); c2=two.li()-two/two.log()
def CLi2(x): x=arb(x); return C*((x.li()-x/x.log())-c2)
hi=b+6; r=int(hi**0.5)+2
s=np.ones(r+1,bool); s[:2]=False
for i in range(2,int(r**0.5)+1):
    if s[i]: s[i*i::i]=False
ps=np.nonzero(s)[0]
seg=np.ones(hi-a,bool)
for p in ps.tolist():
    st=max(p*p,((a+p-1)//p)*p)
    seg[st-a::p]=False
if a<2: seg[:2-a]=False
pr=np.nonzero(seg)[0]+a
starts=pr[(pr<b)]; starts=starts[seg[starts+6-a]]
print(f'block [{a},{b}) pairs={len(starts)} N0={N0}')
N=N0; first=None; rows=[]
for p in starts.tolist():
    N+=1; v=CLi2(p)-N
    if v<0 and first is None:
        first=p; print(f'FIRST CROSSING p={p} pi6(p)={N} C*Li2(p)={CLi2(p).str(25)} diff={v.str(15)}  (p+6={p+6})')
        if stop_first: break
    if v.contains(0): print('UNDECIDED at',p)
print('last N',N,'first',first)
