# check_pts.py eta_str : own Arb re-verification of near-lift pts cert: for real-coefficient f in B with |b2|<=1, |b3|<=eta, f(x)>0 on [r0-,r1].
# Written from Theorem 3.2 / (19), not importing near-lift code.
import sys,json,math,glob,time
from flint import arb,ctx
ctx.prec=128
eta_s=sys.argv[1]; f=glob.glob("../near-lift/certs/pts_eta%s_r*.json"%eta_s); assert len(f)==1
P=json.load(open(f[0])); K=P["K"]; assert K>=4 and "a2box" not in P
eta=arb(float.fromhex(P["eta"])); assert float.fromhex(P["eta"])==float(eta_s)
nodes=[float.fromhex(v) for v in P["nodes"]]; assert nodes[-1]==float.fromhex(P["r1"]); assert all(a<b for a,b in zip(nodes,nodes[1:]))
r0=1/arb(3).sqrt(); lo0=math.nextafter(nodes[0],0); assert arb(lo0)<r0
E=arb(1).exp(); B=[None]*(K+1)
for k in range(4,K+1): B[k]=(arb(k+2)/k)**(arb(k)/2)*arb(k+2)/2
t0=time.time(); C=[]
for rows in P["certs"]:
    q=[arb(0) for _ in range(K+1)]; sl=arb(0); T=arb(0)
    for ro,ps,ga,la in rows:
        ro,ps,ga,la=[float.fromhex(v) for v in (ro,ps,ga,la)]
        assert la>=0 and 0<=ro<1
        if la==0: continue
        x,PS,GA,L=arb(ro),arb(ps),arb(ga),arb(la); sl+=L; c=L*(1-x*x); pw=arb(1)
        for k in range(K+1):
            q[k]=q[k]+c*pw*(k*PS-GA).cos(); pw*=x
        T+=c*pw*((K+3)/(1-x)+x/((1-x)*(1-x)))
    C.append((q,sl,T*E/2))
assert len(C)==len(nodes)
def powers(x):
    p=[arb(1)]*(K+1); a=arb(x)
    for k in range(1,K+1): p[k]=p[k-1]*a
    return p
def ev(cc,hi,pl,ph):
    q,sl,T=cc; H=arb(hi)
    tail=E/2*H**(K+1)*((K+3)/(1-H)+H/((1-H)*(1-H)))
    s=arb(0)
    for k in range(4,K+1): s+=B[k]*abs(pl[k].union(ph[k])+q[k])
    return 1+q[0]-sl-s-T-tail-abs(pl[2].union(ph[2])+q[2])-eta*abs(pl[3].union(ph[3])+q[3])
mn=None;n=0
for j in range(len(nodes)-1):
    A=lo0 if j==0 else nodes[j]; b=nodes[j+1]
    st=[(A,b,powers(A),powers(b),0)]
    while st:
        lo,hi,pl,ph,d=st.pop()
        v=ev(C[j],hi,pl,ph); w=ev(C[j+1],hi,pl,ph)
        lb=max(v.lower(),w.lower()) if False else (v if v.lower()>w.lower() else w)
        if lb>arb(1e-5):
            n+=1
            if mn is None or lb.lower()<mn: mn=lb.lower()
            continue
        assert d<26,("cannot clear",lo,hi,lb.str(8))
        m=lo+(hi-lo)/2; pm=powers(m)
        st.append((lo,m,pl,pm,d+1)); st.append((m,hi,pm,ph,d+1))
print("PTS-PASS file=%s eta=%s r1=%.5f nodes=%d subintervals=%d min_lower=%s wall=%.0fs"%(f[0].split("/")[-1],eta_s,nodes[-1],len(nodes),n,mn.str(8,radius=False),time.time()-t0),flush=True)
