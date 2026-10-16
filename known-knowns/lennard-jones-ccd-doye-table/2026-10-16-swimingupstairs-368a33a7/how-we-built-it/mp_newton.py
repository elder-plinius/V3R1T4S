"""mp_newton.py in out: Newton polish of an LJ cluster with energy+gradient in mpmath (dps 40); step from double Hessian
pseudo-inverse (6 zero modes removed). Writes coords with 35 digits; prints E (mpmath) and gradient 2-norm (mpmath)."""
import sys,os,numpy as np,mpmath as mp; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lj_lib import hessian_eigs
mp.mp.dps=40
P=[[mp.mpf(t) for t in l.split()] for l in open(sys.argv[1]) if l.strip()]; n=len(P)
def eg(P):
    E=mp.mpf(0); G=[[mp.mpf(0)]*3 for _ in range(n)]
    for i in range(n):
        a=P[i]; gi=G[i]
        for j in range(i+1,n):
            b=P[j]; dx=a[0]-b[0]; dy=a[1]-b[1]; dz=a[2]-b[2]; r2=dx*dx+dy*dy+dz*dz
            i6=1/(r2*r2*r2); E+=4*(i6*i6-i6); f=(-48*i6*i6+24*i6)/r2
            gj=G[j]; gi[0]+=f*dx; gi[1]+=f*dy; gi[2]+=f*dz; gj[0]-=f*dx; gj[1]-=f*dy; gj[2]-=f*dz
    return E,G
def H_full(X):
    d=X[:,None,:]-X[None,:,:]; r2=(d**2).sum(-1); np.fill_diagonal(r2,1.0)
    a=(-48*r2**-7+24*r2**-4); b=(672*r2**-8-192*r2**-5); I=np.eye(3)
    blk=-(a[:,:,None,None]*I+b[:,:,None,None]*d[:,:,:,None]*d[:,:,None,:])
    for i in range(n): blk[i,i]=0
    H=blk.transpose(0,2,1,3).reshape(3*n,3*n).copy()
    for i in range(n): H[3*i:3*i+3,3*i:3*i+3]=-blk[i].sum(0)
    return H
X=np.array([[float(c) for c in p] for p in P]); w,V=np.linalg.eigh(H_full(X)); m=w>1e-6
for k in range(4):
    E,G=eg(P); gn=mp.sqrt(sum(c*c for g in G for c in g)); print("iter %d E=%s grad=%s"%(k,mp.nstr(E,30),mp.nstr(gn,5)),flush=True)
    if gn<mp.mpf('1e-20'): break
    g=np.array([float(c) for gg in G for c in gg]); dx=-V[:,m]@((V[:,m].T@g)/w[m])
    P=[[P[i][c]+mp.mpf(dx[3*i+c]) for c in range(3)] for i in range(n)]
print("n_neg=%d n_zero=%d min_pos=%.6f"%((w<-1e-6).sum(),(abs(w)<1e-6).sum(),w[m].min()))
open(sys.argv[2],'w').write("".join(" ".join(mp.nstr(c,35,min_fixed=-1,max_fixed=0) if False else mp.nstr(c,35) for c in p)+"\n" for p in P))
print("FINAL E_mp40=%s grad=%s"%(mp.nstr(E,30),mp.nstr(gn,5)))
