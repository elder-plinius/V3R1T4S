# ADAPTED COPY of ../kings/ctmgen2.py (own work); only change: new model "vertex" (monomer-dimer). Original header follows.
# Generic high-precision CTM for IRF (face-weight) models given as a sparse face tensor a[l,u,r,d].
# models: site  = king graph independent sets, spins on sites, face weight [sum of 4 corner spins <= 1], D=4 pair legs
#         block = same model grouped into 2x2 blocks (5 block states: empty, BL, BR, TL, TR), D=21 pair legs;
#                 kappa_block = kappa^4 per block.
# Projectors: float64 SVD of [M_k^T | M_{k+1}] (isometry Y_k per bond), exactly re-orthonormalised in arb (Newton-Schulz).
# All tensor contractions (and C, T storage) in arb (python-flint) at PREC bits.
import sys, time, itertools
import numpy as np
from flint import arb, arb_mat, ctx
model=sys.argv[1]; chi=int(sys.argv[2]); iters=int(sys.argv[3]); PREC=int(sys.argv[4])
ctx.prec=PREC
import os
THR=float(os.environ.get('THR','0'))
NORMBLK=int(os.environ.get('NORMBLK','1'))
def build(model):
    if model=="vertex":
        # monomer-dimer vertex model: legs = bond occupation (0/1); site tensor = 1 iff l+u+r+d <= 1 (at most one dimer at a site;
        # none = monomer).  kappa = Z per site = exp(h2).
        ents=[(l,u,r,d) for l in (0,1) for u in (0,1) for r in (0,1) for d in (0,1) if l+u+r+d<=1]
        return (2,2),ents
    if model=="site":
        ns=2
        def W(bl,br,tl,tr): return bl+br+tl+tr<=1
        H=lambda x,y: True; V=lambda x,y: True
        hp=[(x,y) for x in range(ns) for y in range(ns)]
        vp=hp
    elif model=="domino":
        # vertical dominos (2 sites): states 0 empty, 1 lower occupied, 2 upper occupied; kappa_domino = kappa^2
        ns=3
        H=lambda x,y: (x==0 or y==0)
        V=lambda x,y: not (x==2 and y==1)
        def W(bl,br,tl,tr):
            return H(bl,br) and H(tl,tr) and V(bl,tl) and V(br,tr) and not (bl==2 and tr==1) and not (br==2 and tl==1)
        hp=[(x,y) for x in range(ns) for y in range(ns) if H(x,y)]
        vp=[(x,y) for x in range(ns) for y in range(ns) if V(x,y)]
    else:
        ns=5  # 0 empty,1 BL,2 BR,3 TL,4 TR
        H=lambda x,y: not (x in (2,4) and y in (1,3))
        V=lambda x,y: not (x in (3,4) and y in (1,2))
        def W(bl,br,tl,tr):
            return H(bl,br) and H(tl,tr) and V(bl,tl) and V(br,tr) and not (bl==4 and tr==1) and not (br==3 and tl==2)
        hp=[(x,y) for x in range(ns) for y in range(ns) if H(x,y)]
        vp=[(x,y) for x in range(ns) for y in range(ns) if V(x,y)]
    hi={p:i for i,p in enumerate(hp)}; vi={p:i for i,p in enumerate(vp)}
    ents=[]
    for bl,br,tl,tr in itertools.product(range(ns),repeat=4):
        if W(bl,br,tl,tr):
            ents.append((vi[(bl,tl)],hi[(tl,tr)],vi[(br,tr)],hi[(bl,br)]))   # l,u,r,d
    return (len(vp),len(hp)),ents
(DV,DH),ENTS=build(model)
L,U,R,Dn=0,1,2,3
DIM={L:DV,R:DV,U:DH,Dn:DH}
corner_legs={0:(L,U,Dn,R),1:(U,R,L,Dn),2:(R,Dn,U,L),3:(Dn,L,R,U)}
edge_legs={0:(U,Dn,L,R),1:(R,L,U,Dn),2:(Dn,U,R,L),3:(L,R,Dn,U)}
def permuted(ents,order):  # entries with legs reordered to the given leg order
    return [tuple(e[i] for i in order) for e in ents]
def obj1(shape,val):
    o=np.empty(shape,dtype=object).reshape(-1)
    for i in range(o.size): o[i]=arb(val)
    return o.reshape(shape)
def zeros(shape): return obj1(shape,0)
def tomat(A):
    r,c=A.shape
    return arb_mat(r,c,A.reshape(-1).tolist())
def frommat(M):
    o=np.empty(M.nrows()*M.ncols(),dtype=object); o[:]=M.entries()
    return o.reshape(M.nrows(),M.ncols())
def mm(A,B): return frommat((tomat(A)*tomat(B)).mid())
def tofloat(A): return np.array([float(x.mid()) for x in A.reshape(-1)]).reshape(A.shape)
def fromfloat(A):
    o=np.empty(A.size,dtype=object)
    for i,x in enumerate(A.reshape(-1)): o[i]=arb(float(x))
    return o.reshape(A.shape)
def maxabs(A): return max(abs(float(x.mid())) for x in A.reshape(-1))
def scale(A,s):
    inv=arb(1)/s
    o=np.empty(A.size,dtype=object)
    for i,x in enumerate(A.reshape(-1)): o[i]=(x*inv).mid()
    return o.reshape(A.shape)
def orthonormalize(Y):
    n,k=Y.shape
    half=arb(1)/2
    for _ in range(int(np.ceil(np.log2(PREC/50.0)))+2):
        G=mm(Y.T,Y)
        W=np.empty(G.shape,dtype=object)
        for i in range(k):
            for j in range(k):
                W[i,j]=(((arb(3) if i==j else arb(0))-G[i,j])*half).mid()
        Y=mm(Y,W)
    return Y
def step(C,T,chi):
    Ms=[]
    for k in range(4):
        pl,nl,po,no=corner_legs[k]
        Tp=T[(k-1)%4]; Tn=T[k]
        X=mm(C[k],Tn.reshape(Tn.shape[0],-1))
        x=Tp.shape[0]; z=Tn.shape[2]
        ds,dt,da,db=DIM[pl],DIM[nl],DIM[po],DIM[no]
        Z1=mm(Tp.reshape(x*ds,Tp.shape[2]),X).reshape(x,ds,dt,z)   # x,s,t,z
        M=zeros((x,da,z,db))
        for e in permuted(ENTS,(pl,nl,po,no)):
            s_,t_,a_,b_=e
            M[:,a_,:,b_]=M[:,a_,:,b_]+Z1[:,s_,t_,:]
        Ms.append(M.reshape(x*da,z*db))
    Ys=[];Ss=[]
    for k in range(4):
        A_=tofloat(Ms[k]).T; B_=tofloat(Ms[(k+1)%4])
        N=np.hstack([A_/np.linalg.norm(A_),B_/np.linalg.norm(B_)]) if NORMBLK else np.hstack([A_,B_])
        Uu,S,Vt=np.linalg.svd(N,full_matrices=False)
        kk=min(chi,len(S),int((S>THR*S[0]).sum()))
        Ys.append(orthonormalize(fromfloat(Uu[:,:kk]))); Ss.append(S[:kk])
    newC=[]
    for k in range(4):
        c=mm(mm(Ys[(k-1)%4].T,Ms[k]),Ys[k])
        newC.append(scale(c,arb(maxabs(c))))
    newT=[]
    for k in range(4):
        out,inn,near,far=edge_legs[k]
        Tk=T[k]; p,_,q=Tk.shape
        dn,di,df=DIM[near],DIM[inn],DIM[far]
        E=zeros((p,dn,di,q,df))                                # p,n,i,q,f
        for e in permuted(ENTS,(near,out,far,inn)):
            n_,s_,f_,i_=e
            E[:,n_,i_,:,f_]=E[:,n_,i_,:,f_]+Tk[:,s_,:]
        Y=Ys[k]; kk=Y.shape[1]
        Tn=np.empty((kk,di,kk),dtype=object)
        for i_ in range(di):
            Ei=E[:,:,i_,:,:].reshape(p*dn,q*df)
            Tn[:,i_,:]=mm(mm(Y.T,Ei),Y)
        newT.append(scale(Tn,arb(maxabs(Tn))))
    return newC,newT,Ss
def chain(mats):
    P=mats[0]
    for m in mats[1:]: P=mm(P,m)
    return P
def trace(M):
    s=arb(0)
    for i in range(M.shape[0]): s+=M[i,i]
    return s
def kappa(C,T):
    C1,C2,C3,C4=C;T1,T2,T3,T4=T
    sl=lambda Tk,s: Tk[:,s,:]
    N00=trace(chain([C1,C2,C3,C4]))
    N10=sum((trace(chain([C1,sl(T1,s),C2,C3,sl(T3,s),C4])) for s in range(DIM[U])),arb(0))
    N01=sum((trace(chain([C1,C2,sl(T2,s),C3,C4,sl(T4,s)])) for s in range(DIM[R])),arb(0))
    N11=arb(0)
    for (l,u,r,d) in ENTS:
        N11+=trace(chain([C1,sl(T1,u),C2,sl(T2,r),C3,sl(T3,d),C4,sl(T4,l)]))
    return (N11*N00/(N10*N01)).mid()
def dump(C,T,fn):
    import json
    def enc(A): return {"shape":list(A.shape),"v":[x.str(90,radius=False) for x in A.reshape(-1)]}
    json.dump({"C":[enc(c) for c in C],"T":[enc(t) for t in T]},open(fn,"w"))
def load(fn):
    import json
    d=json.load(open(fn))
    def dec(e):
        o=np.empty(len(e["v"]),dtype=object)
        for i,x in enumerate(e["v"]): o[i]=arb(x)
        return o.reshape(e["shape"])
    return [dec(c) for c in d["C"]],[dec(t) for t in d["T"]]
if __name__=="__main__":
    init=sys.argv[5] if len(sys.argv)>5 and sys.argv[5]!="-" else None
    outf=sys.argv[6] if len(sys.argv)>6 else None
    if init: C,T=load(init)
    else:
        C=[obj1((1,1),1) for _ in range(4)]
        T=[obj1((1,DIM[edge_legs[k][0]],1),1) for k in range(4)]
    print('model',model,'DV,DH',DV,DH,'faces',len(ENTS),'chi',chi,'prec',PREC,'init',init,flush=True)
    prev=None; stable=0
    for it in range(iters):
        t=time.time()
        C,T,Ss=step(C,T,chi)
        k=kappa(C,T)
        if model=="block": k=k.sqrt().sqrt()
        if model=="domino": k=k.sqrt()
        print(it,k.str(60,radius=False),'sv_last %.3e'%(Ss[0][-1]/Ss[0][0]),'chi_eff',C[0].shape[0],'%.1fs'%(time.time()-t),flush=True)
        if outf and it%10==9: dump(C,T,outf)
        if prev is not None and abs(float((k-prev)*arb(10)**36))<1: stable+=1
        else: stable=0
        prev=k
        if stable>=3: print('converged (|dk|<1e-36 x3)',flush=True); break
    if outf: dump(C,T,outf)
