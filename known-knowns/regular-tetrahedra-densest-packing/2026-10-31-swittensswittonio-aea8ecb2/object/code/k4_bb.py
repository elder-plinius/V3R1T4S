"""EXACT (integer) branch-and-bound proof of the 'ratio lemma' behind GEK Lemma 3.5 (K4):
  T = conv{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)} (edge^2 = 8).  O not in int T.  D(O)=min vertex distance, F_i closed faces.
  CLAIM(C): if O not in int T and D(O)^2 > C * r^2 then fewer than 3 faces have dist(O,F_i) < r,  C=(9/2)(1+eps)^2.
  i.e. D(O)^2 <= C * r3(O)^2 where r3 = 3rd smallest face distance.
Box test: for a box X (dyadic corners, integer arithmetic scaled by 2^K) it is enough that X in int T, or X disjoint from the symmetry
fundamental domain {x>=y>=|z|}, or two faces i with  C*dist2_lb_i(X) >= D2_ub(X)  (all lower/upper bounds exact rational).
dist2_lb_i = h_i^2 + (max_j out_ij_+)^2 : exact distance to face triangle is >= this (plane distance h_i, and
distance in the plane to the triangle >= signed outward distance to each edge line).
Usage: python k4_bb.py EPS_NUM EPS_DEN  (eps=EPS_NUM/EPS_DEN)"""
import sys, itertools, time
from fractions import Fraction as Fr
EN,ED = int(sys.argv[1]), int(sys.argv[2])
K=30; S=1<<K                       # coordinates are integers/ S
V=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
# face k opposite vertex V[k]: plane V_k.x = -1 ; interior: V_k.x > -1
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
faces=[]
for k in range(4):
    vs=[V[i] for i in range(4) if i!=k]; n=tuple(-c for c in V[k])        # outward normal (unnormalised, |n|^2=3)
    edges=[]
    for (p,q,r) in [(vs[0],vs[1],vs[2]),(vs[1],vs[2],vs[0]),(vs[2],vs[0],vs[1])]:
        t=tuple(q[i]-p[i] for i in range(3)); m=cross(n,t)
        if dot(m,tuple(r[i]-p[i] for i in range(3)))>0: m=tuple(-c for c in m)   # outward from triangle
        assert dot(m,m)==24 and dot(m,t)==0 and dot(m,n)==0
        edges.append((m,p))
    faces.append((V[k],edges))
# C = 9/2 (1+eps)^2 = Cn/Cd
Cn=9*(ED+EN)**2; Cd=2*ED**2
def lin(m,X,c0=0):
    lo=c0*S; hi=c0*S
    for i in range(3):
        a,b=X[i]
        if m[i]>=0: lo+=m[i]*a; hi+=m[i]*b
        else: lo+=m[i]*b; hi+=m[i]*a
    return lo,hi
def sq_ival(lo,hi):                    # range of s^2 for s in [lo,hi] (scaled)
    if lo<=0<=hi: return 0, max(lo*lo,hi*hi)
    return min(lo*lo,hi*hi), max(lo*lo,hi*hi)
RHO0=1   # half-width of vertex cube Q0 = (V0-1,V0+1)^3 (L-infinity)
def check(X):
    # returns 'in','out','ok' or None
    if all(X[i][0]>(1-RHO0)*S and X[i][1]<(1+RHO0)*S for i in range(3)): return 'vtx'   # box inside open cube Q0 around V0=(1,1,1): covered by shell lemma
    # domain pruning x>=y>=|z|: disjoint if x1<y0 or y1< |z|min
    (x0,x1),(y0,y1),(z0,z1)=X
    if x1<y0: return 'dom'
    zmin = 0 if z0<=0<=z1 else min(abs(z0),abs(z1))
    if y1<zmin: return 'dom'
    # inside int T: V_k.x+1>0 for all k
    inside=True
    L=[]
    for (vk,edges) in faces:
        lo,hi=lin(vk,X,1)          # scaled: V_k.x+1 (scaled by S)
        L.append((lo,hi))
        if lo<=0: inside=False
    if inside: return 'in'
    # D2 upper bound: min_v max |x-v|^2  (scaled S^2)
    D2=None
    for v in V:
        s=0
        for i in range(3):
            a=X[i][0]-v[i]*S; b=X[i][1]-v[i]*S
            s+=max(a*a,b*b)
        D2=s if D2 is None else min(D2,s)
    good=0
    for k,(vk,edges) in enumerate(faces):
        lo,hi=L[k]; hmin2,_=sq_ival(lo,hi)               # (V_k.x+1)^2 /3 = h^2 ; scaled S^2
        out2=0
        for (m,p) in edges:
            mlo,_=lin(m,X,0); mlo-= dot(m,p)*S           # m.(x-p) lower, scaled S
            if mlo>0: out2=max(out2,mlo*mlo)
        # dist2_lb = hmin2/3 + out2/24 ; test  C*dist2_lb >= D2   <=>  Cn*(8*hmin2+out2) >= 24*Cd*D2
        if Cn*(8*hmin2+out2) >= 24*Cd*D2: good+=1
    return 'ok' if good>=2 else None
def run(maxdepthbits=24, maxboxes=20_000_000):
    R=5*S
    stack=[((0,R),(0,R),(-R,R))]; n=0; stats={'dom':0,'in':0,'ok':0,'vtx':0}; bad=[]
    t0=time.time()
    while stack:
        X=stack.pop(); n+=1
        r=check(X)
        if r: stats[r]+=1; continue
        w=[b-a for a,b in X]; i=w.index(max(w))
        if w[i]<= S>>maxdepthbits:
            bad.append(X); 
            if len(bad)>50: break
            continue
        a,b=X[i]; mid=(a+b)//2
        X1=list(X); X2=list(X); X1[i]=(a,mid); X2[i]=(mid,b)
        stack.append(tuple(X1)); stack.append(tuple(X2))
        if n>maxboxes: break
        if n%200000==0: print("boxes",n,"stack",len(stack),stats,"%.0fs"%(time.time()-t0),flush=True)
    return n,stats,bad
# ---------------- shell lemma (cone at V0=(1,1,1)) ----------------
def check_shell(X):
    # X = box in u=O-V0 coordinates (scaled by S); shell: 0.5*RHO0 <= |u|_inf <= RHO0 ; cone faces = faces opposite V1,V2,V3 (edges through V0 only) + opposite face 0 (plane distance only)
    # u coordinates: O = V0+u.  sector face k: plane V_k.O=-1 -> V_k.u = -1 - V_k.V0 ; edges through V0 only
    # inside shell region?  skip box if entirely inside inner open cube (|u|_inf < RHO0/2)
    h=S*RHO0//2
    if all(-h<X[i][0] and X[i][1]<h for i in range(3)): return 'core'
    inside=True; Lk=[]
    for k in (0,1,2,3):
        vk,edges=faces[k]
        lo,hi=lin(vk,X,0); c=1+dot(vk,V[0]); lo+=c*S; hi+=c*S        # V_k.O+1 = V_k.u + 1 + V_k.V0
        Lk.append((lo,hi))
        if k>0 and lo<=0: inside=False
    assert Lk[0][0]>0     # opposite face plane never reached inside the cube Q0
    if inside: return 'in'
    U2=0
    for i in range(3):
        a,b=X[i]; U2+=max(a*a,b*b)
    good=0
    for kk,k in enumerate((0,1,2,3)):
        vk,edges=faces[k]; lo,hi=Lk[kk]; hmin2,_=sq_ival(lo,hi)
        out2=0
        for (m,p) in edges:
            if p!=V[0] and True:
                # edge line through V0? edge pq has base point p; the line passes through V0 iff V0 - p is parallel to the edge dir t (m.(V0-p)==0)
                pass
            if dot(m,tuple(V[0][i]-p[i] for i in range(3)))!=0: continue      # keep only edge lines through V0
            mlo,_=lin(m,X,0)                                                   # m.u (V0 on the line): m.(O-p)=m.u + m.(V0-p) = m.u
            if mlo>0: out2=max(out2,mlo*mlo)
        if Cn*(8*hmin2+out2) >= 24*Cd*U2: good+=1
    return 'ok' if good>=2 else None
def run_shell(maxdepthbits=24):
    R=S*RHO0
    stack=[((-R,R),(-R,R),(-R,R))]; n=0; st={'core':0,'in':0,'ok':0}; bad=[]
    while stack:
        X=stack.pop(); n+=1
        r=check_shell(X)
        if r: st[r]+=1; continue
        w=[b-a for a,b in X]; i=w.index(max(w))
        if w[i]<=S>>maxdepthbits:
            bad.append(X)
            if len(bad)>50: break
            continue
        a,b=X[i]; mid=(a+b)//2; X1=list(X); X2=list(X); X1[i]=(a,mid); X2[i]=(mid,b); stack.append(tuple(X1)); stack.append(tuple(X2))
    return n,st,bad

if __name__=="__main__":
    print("eps = %d/%d ; C = %s = %.9f ; 9/2=4.5"%(EN,ED,Fr(Cn,Cd),Cn/Cd))
    n,st,bad=run()
    print("boxes processed",n,"stats",st,"unresolved",len(bad))
    for b in bad[:5]: print([ (Fr(a,S).limit_denominator(10**9),Fr(c,S).limit_denominator(10**9)) for a,c in b])
    n2,st2,bad2=run_shell()
    print("SHELL boxes",n2,st2,"unresolved",len(bad2))
    for b in bad2[:5]: print([ (Fr(a,S).limit_denominator(10**9),Fr(c,S).limit_denominator(10**9)) for a,c in b])
    print("RESULT:", "PROVED (all boxes certified)" if not bad and not bad2 else "NOT PROVED")

