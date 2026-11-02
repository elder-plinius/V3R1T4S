# cover_check.py prefix: separate covering script. Reads only leaves file, exact integers.
# Stack-merge in file order: two adjacent leaves that are the two halves of one dyadic box along one axis merge.
# PASS iff everything merges into the single root box [0,1]x[rho0,rho0+4]x[0,1] (i.e. all coordinates level 0).
import sys, struct
from fractions import Fraction
fn=sys.argv[1]+".leaves"; data=open(fn,"rb").read()
RS=struct.Struct("<4B4I")
n=len(data)//RS.size
if len(data)%RS.size: print("FAIL: truncated record"); sys.exit(1)
st=[]; vol=Fraction(0); kinds={}
for i in range(n):
    la,lr,lu,k,ia,ir,iu,w=RS.unpack_from(data,i*RS.size)
    kinds[k]=kinds.get(k,0)+1
    if k==255: print("FAIL: stuck leaf"); sys.exit(1)
    b=(la,ia,lr,ir,lu,iu); vol+=Fraction(1,2**(la+lr+lu))
    st.append(b)
    while len(st)>=2:
        p,q=st[-2],st[-1]; merged=None
        for ax in range(3):
            o=[0,1,2]; o.remove(ax)
            if all(p[2*x]==q[2*x] and p[2*x+1]==q[2*x+1] for x in o) and p[2*ax]==q[2*ax] and p[2*ax]>0 and p[2*ax+1]%2==0 and q[2*ax+1]==p[2*ax+1]+1:
                m=list(p); m[2*ax]=p[2*ax]-1; m[2*ax+1]=p[2*ax+1]//2; merged=tuple(m); break
        if merged is None: break
        st.pop(); st.pop(); st.append(merged)
ok = len(st)==1 and st[0]==(0,0,0,0,0,0) and vol==1
print(("PASS" if ok else "FAIL")+" cover: leaves=%d kinds=%s residual_stack=%d volume=%s"%(n,kinds,len(st),vol))
sys.exit(0 if ok else 1)
