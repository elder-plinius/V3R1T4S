# Same as exact_block.py but reports first violation under both counting conventions, and the margins of the
# last 5 pairs before the inclusive crossing.
import sys, numpy as np
from flint import arb, ctx
ctx.prec=200
a,b,N0=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
C=4*arb('0.6601618158468695739278121100145557784326233602847334133194484233')
two=arb(2); c2=two.li()-two/two.log()
def CLi2(x): x=arb(x); return C*((x.li()-x/x.log())-c2)
hi=b+6; r=int(hi**0.5)+2
s=np.ones(r+1,bool); s[:2]=False
for i in range(2,int(r**0.5)+1):
    if s[i]: s[i*i::i]=False
seg=np.ones(hi-a,bool)
for p in np.nonzero(s)[0].tolist():
    st=max(p*p,((a+p-1)//p)*p); seg[st-a::p]=False
pr=np.nonzero(seg)[0]+a; starts=pr[pr<b]; starts=starts[seg[starts+6-a]]
N=N0; inc=exc=None; hist=[]
for p in starts.tolist():
    N+=1; L=CLi2(p)
    if inc is None:
        hist.append((p,N,L.mid().str(20),(L-N).mid().str(12))); hist=hist[-6:]
        if L-N<0: inc=(p,N,L.str(22))
    if exc is None and L-(N-1)<0: exc=(p,N-1,L.str(22))
    if inc and exc: break
print('inclusive first:',inc); print('exclusive first:',exc)
print('last pairs up to inclusive crossing (p, pi6 incl, C*Li2, margin):')
for h in hist: print('  ',h)
