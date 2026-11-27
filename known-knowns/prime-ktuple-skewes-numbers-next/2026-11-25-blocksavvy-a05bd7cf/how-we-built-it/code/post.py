# Post-process sexyA/sexyB block records: prefix counts, chord-bound margins per block, power-of-ten counts.
import sys, numpy as np, re
from flint import arb, ctx
ctx.prec=200
B=6*(1<<21)
recfile, Lfile, txt = sys.argv[1], sys.argv[2], sys.argv[3]
exact_below=int(float(sys.argv[4])) if len(sys.argv)>4 else 10**8   # blocks starting below this are covered by the exact small-case check
dt=np.dtype([('cnt','<u4'),('M','<f8'),('ckc','<i8')])
r=np.fromfile(recfile,dtype=dt); L=np.fromfile(Lfile,dtype='<f8'); nb=len(r); assert len(L)==nb+1
cnt=r['cnt'].astype(np.int64); Nb=np.concatenate([[0],np.cumsum(cnt)])[:-1]
M=r['M']; has=cnt>0
margin=np.where(has, L[:-1]-Nb-M, np.inf)
start=np.arange(nb)*B
chk=start>=exact_below
fl=np.nonzero(chk & (margin<1e-3))[0]
mi=np.argmin(np.where(chk,margin,np.inf))
C2=arb('0.6601618158468695739278121100145557784326233602847334133194484233'); two=arb(2); c2=two.li()-two/two.log()
print(f'blocks={nb} range=[0,{nb*B}) total_pairs={cnt.sum()} chord_checked_blocks={chk.sum()} (start>={exact_below})')
print(f'min_chord_margin={margin[mi]:.6f} at block {mi} (n in [{mi*B},{(mi+1)*B})) flagged_blocks={len(fl)} {fl[:20].tolist()}')
for line in open(txt):
    m=re.match(r'ck (\d+) block (\d+) inblock (-?\d+)',line)
    if m:
        c,b,ib=map(int,m.groups()); pi=int(Nb[b])+ib; x=arb(c); v=4*C2*((x.li()-x/x.log())-c2)
        print(f'pi6({c})={pi}  C*Li2={v.mid().str(15)}  deficit={(v-pi).mid().str(10)}')
# coarse profile of the deficit lower bound at block starts
for e in range(9,20):
    j=int(10**(e/1.0)//B) if e<=15 else None
