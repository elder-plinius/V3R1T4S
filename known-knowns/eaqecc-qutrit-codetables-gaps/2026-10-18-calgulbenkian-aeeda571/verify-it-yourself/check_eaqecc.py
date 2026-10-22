"""Independent EAQECC check over GF(3) (written from the definition; standard library plus numpy).

Usage: python3 check_eaqecc.py OBJECT.json TABLE_D_LOWER TABLE_D_UPPER

Encoding: S is a list of s rows of integers 0..2 (elements of GF(3)), 2n columns: x_1..x_n then z_1..z_n.
Symplectic form form(u,v) = u_x.v_z - u_z.v_x. s = rank(S); c = rank(S J S^T)/2; k = n - s + c.
Dual = {v : S J v = 0}. Isotropic part = dual intersect span(S). d = minimum symplectic weight over dual vectors
NOT in the isotropic part (exhaustive over all cosets of the isotropic part). The verdict compares against the
object's own k, c, d_claimed fields and against the table cell d_lower-d_upper.
"""
import sys,json,itertools,time
import numpy as np
def rref(M):
    M=M.copy()%3; r=0; piv=[]
    for c in range(M.shape[1]):
        p=None
        for i in range(r,M.shape[0]):
            if M[i,c]: p=i;break
        if p is None: continue
        M[[r,p]]=M[[p,r]]
        if M[r,c]==2: M[r]=(M[r]*2)%3
        for i in range(M.shape[0]):
            if i!=r and M[i,c]: M[i]=(M[i]-M[i,c]*M[r])%3
        piv.append(c); r+=1
        if r==M.shape[0]: break
    return M[:r],piv
def rank(M): return len(rref(M)[1]) if M.size else 0
def nullspace(M):  # vectors v with M v = 0
    R,piv=rref(M); m=M.shape[1]; free=[c for c in range(m) if c not in piv]; out=[]
    for f in free:
        v=np.zeros(m,dtype=np.int64); v[f]=1
        for i,p in enumerate(piv): v[p]=(-R[i,f])%3
        out.append(v)
    return np.array(out,dtype=np.int64).reshape(len(out),m)
def J(n):
    Z=np.zeros((n,n),dtype=np.int64); I=np.eye(n,dtype=np.int64)
    return np.block([[Z,I],[(-I)%3,Z]])
def analyse(S,n,layout='xz'):
    S=np.array(S,dtype=np.int64)%3
    if layout=='inter':
        perm=list(range(0,2*n,2))+list(range(1,2*n,2)); S=S[:,perm]
    Jn=J(n)
    R,_=rref(S); s=len(R)
    G=(R@Jn@R.T)%3; c=rank(G)//2
    k=n-s+c
    # dual: v with R J v = 0
    D=nullspace((R@Jn)%3)
    # radical = dual ∩ span(R): coefficients a with a G =0
    ra=nullspace(G) # a: G a=0 (G antisym)
    Rad=(ra@R)%3 if len(ra) else np.zeros((0,2*n),dtype=np.int64)
    # extend rad basis to dual basis
    basis=[r for r in Rad]; cur=rank(np.array(basis)) if basis else 0
    comp=[]
    for v in D:
        t=np.array(basis+[v]); 
        if rank(t)>cur: basis.append(v); comp.append(v); cur+=1
    comp=np.array(comp); Rad=np.array(Rad)
    assert len(comp)+len(Rad)==len(D)
    return dict(n=n,s=s,c=c,k=k,dimdual=len(D),dimrad=len(Rad),comp=comp,rad=Rad,rank_raw=s)
def allcomb(B):
    m=len(B)
    if m==0: return np.zeros((1,B.shape[1] if B.ndim==2 else 0),dtype=np.int8)
    co=np.array(list(itertools.product(range(3),repeat=m)),dtype=np.int64)
    return ((co@B)%3).astype(np.int8)
def mind(info,n):
    comp,rad=info['comp'],info['rad']
    if len(comp)==0: return None
    RA=allcomb(rad)
    def wt(V): return ((V[:,:n]!=0)|(V[:,n:]!=0)).sum(1)
    # reduce: in subset ordering, only compute for comp vectors nonzero
    best=10**9; cnt=0
    for co in itertools.product(range(3),repeat=len(comp)):
        if not any(co): continue
        v=(np.array(co)@comp)%3
        V=(RA+v.astype(np.int8))%3
        w=wt(V).min(); 
        if best>w: best=w
    return int(best)

def main():
    f=sys.argv[1]; dl=int(sys.argv[2]); du=int(sys.argv[3])
    d=json.load(open(f)); n=d['n']; t=time.time()
    info=analyse(d['S'],n,'xz')
    print('file',f.replace(chr(92),'/').split('/')[-1],'n',n,'s',info['s'],'c',info['c'],'k',info['k'],'dual_dim',info['dimdual'],'isotropic_dim',info['dimrad'])
    if not (info['k']==d['k'] and info['c']==d['c']):
        print('computed k,c =',info['k'],info['c'],'but object claims',d['k'],d['c']); print('FAIL'); sys.exit(1)
    dist=mind(info,n)
    print('exact minimum distance d =',dist,'(%.1f s)'%(time.time()-t))
    conds={'c>=1':info['c']>=1,'d==d_claimed':dist==d['d_claimed'],'d>table_d_lower(%d)'%dl:dist>dl,'d<=table_d_upper(%d)'%du:dist<=du}
    for k_,v_ in conds.items(): print(' ',k_,v_)
    ok=all(conds.values())
    print('[[%d,%d,%d;%d]]_3'%(n,info['k'],dist,info['c']),'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
if __name__=='__main__': main()
