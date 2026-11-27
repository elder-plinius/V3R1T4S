# Exhaustive exact check for n <= N of patterns [0,2],[0,4],[0,6] under two counting conventions:
#   inclusive: pi_P(p) = #{instances q <= p}  (OEIS A210439 / bank wording)   exclusive: #{q < p} (Toth 2019 'less than n')
import sys, numpy as np
from flint import arb, ctx
ctx.prec=200
N=int(sys.argv[1])
C2=arb('0.6601618158468695739278121100145557784326233602847334133194484233')
two=arb(2); c2=two.li()-two/two.log()
def li2(x): x=arb(x); return (x.li()-x/x.log())-c2
s=np.ones(N+7,dtype=bool); s[:2]=False
for i in range(2,int((N+6)**0.5)+1):
    if s[i]: s[i*i::i]=False
pr=np.nonzero(s)[0]
for d,C,known in [(2,2*C2,1369391),(4,2*C2,5206837),(6,4*C2,None)]:
    st=pr[(pr<=N)]; st=st[s[st+d]]
    finc=fexc=None; mininc=None; unc=0
    for i,p in enumerate(st.tolist(),1):
        L=C*li2(p); vi=L-i; ve=L-(i-1)
        if vi.contains(0) or ve.contains(0): unc+=1
        if finc is None and vi<0: finc=(p,i,L.mid().str(20))
        if fexc is None and ve<0: fexc=(p,i-1,L.mid().str(20))
        if finc is None:
            m=float(vi.mid())
            if mininc is None or m<mininc[0]: mininc=(m,p)
        if finc and fexc: break
    print(f'pattern [0,{d}] N={N} instances={len(st)} first_inclusive={finc} known={known} first_exclusive={fexc} min_inclusive_margin_before_first={mininc} undecided={unc}',flush=True)
