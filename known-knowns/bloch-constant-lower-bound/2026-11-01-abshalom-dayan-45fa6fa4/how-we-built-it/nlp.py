"""Dense Mehrotra IPM + cutting-plane search for near certificates. Float only: search, nothing trusted."""
import numpy as np, json, time, math
def Bk(K):
    k=np.arange(K+1,dtype=float); B=np.ones(K+1); B[1:]=((k[1:]+2)/k[1:])**(k[1:]/2)*(k[1:]+2)/2; return B
def rowmat(rho,psi,gam,K):
    """rows r_k (m x K+1)"""
    k=np.arange(K+1)[None,:]
    return (1-rho**2)[:,None]*np.exp(k*np.log(np.maximum(rho,1e-300))[:,None])*np.cos(k*psi[:,None]-gam[:,None])
def ipm(c,G,h,tol=1e-10,maxit=120,verbose=False,x0=None):
    """min c'x st Gx<=h, -1<=x<=1. returns x,z (row duals),zu,zl,info"""
    n=len(c);m=G.shape[0]
    x=np.zeros(n) if x0 is None else np.clip(x0,-.95,.95)
    su=1-x;sl=1+x
    s=np.maximum(h-G@x,1e-2); z=np.ones(m)*1e-2
    zu=np.ones(n)*1e-2+np.maximum(-c,0);zl=np.ones(n)*1e-2+np.maximum(c,0)
    nu=2*n+m
    hist=None
    for it in range(maxit):
        rd=c+G.T@z+zu-zl; rp=G@x+s-h
        mu=(s@z+su@zu+sl@zl)/nu
        pobj=c@x; 
        if verbose and it%5==0: print(it,'mu %.2e rd %.2e rp %.2e obj %.10f'%(mu,np.abs(rd).max(),np.abs(rp).max(),pobj),flush=True)
        if mu<tol and np.abs(rd).max()<tol*10 and np.abs(rp).max()<tol*10: break
        W=z/s; Du=zu/su+zl/sl
        M=(G*W[:,None]).T@G
        M[np.diag_indices(n)]+=Du+1e-13
        try:
            L=np.linalg.cholesky(M); chol=True
        except np.linalg.LinAlgError:
            M[np.diag_indices(n)]+=1e-9; L=np.linalg.cholesky(M)
        def sol(rc,rcu,rcl):
            b=-rd-G.T@(rc/s+W*rp)-rcu/su+rcl/sl
            y=np.linalg.solve(L,b); dx=np.linalg.solve(L.T,y)
            for _ in range(1):
                res=b-(G.T@(W*(G@dx))+(Du+1e-13)*dx)
                dx=dx+np.linalg.solve(L.T,np.linalg.solve(L,res))
            ds=-G@dx-rp; dsu=-dx; dsl=dx
            dz=(rc-z*ds)/s; dzu=(rcu-zu*dsu)/su; dzl=(rcl-zl*dsl)/sl
            return dx,ds,dsu,dsl,dz,dzu,dzl
        def step(v,dv):
            neg=dv<0
            return 1.0 if not neg.any() else min(1.0,(-v[neg]/dv[neg]).min())
        dx,ds,dsu,dsl,dz,dzu,dzl=sol(-z*s,-zu*su,-zl*sl)
        ap=min(step(s,ds),step(su,dsu),step(sl,dsl)); ad=min(step(z,dz),step(zu,dzu),step(zl,dzl))
        mua=((s+ap*ds)@(z+ad*dz)+(su+ap*dsu)@(zu+ad*dzu)+(sl+ap*dsl)@(zl+ad*dzl))/nu
        sig=(mua/mu)**3
        dx,ds,dsu,dsl,dz,dzu,dzl=sol(sig*mu-z*s-ds*dz,sig*mu-zu*su-dsu*dzu,sig*mu-zl*sl-dsl*dzl)
        ap=min(1,.995*min(step(s,ds),step(su,dsu),step(sl,dsl))); ad=min(1,.995*min(step(z,dz),step(zu,dzu),step(zl,dzl)))
        x=x+ap*dx;s=s+ap*ds;su=su+ap*dsu;sl=sl+ap*dsl
        z=z+ad*dz;zu=zu+ad*dzu;zl=zl+ad*dzl
    return x,z,zu,zl,dict(it=it,mu=mu,rd=np.abs(rd).max(),rp=np.abs(rp).max(),obj=c@x)
class Prob:
    """Objective w_k (k=0..K); bnd[k] box half width for free k, pinned dict k->value. a0=1, a1=0."""
    def __init__(self,w,K,pinned,box):
        self.w=w;self.K=K;self.pinned=dict(pinned);self.pinned[0]=1.0;self.pinned[1]=0.0
        self.free=[k for k in range(K+1) if k not in self.pinned]
        self.B=np.array([box.get(k,0) if k in box else 0 for k in self.free]); B=Bk(K)
        self.B=np.array([box[k] if k in box else B[k] for k in self.free])
    def solve(self,rho,psi,gam,tol=1e-10,verbose=False):
        K=self.K; R=rowmat(rho,psi,gam,K)
        pin=np.zeros(R.shape[0]); cst=0
        for k,v in self.pinned.items():
            pin+=R[:,k]*v; cst+=self.w[k]*v
        tau=math.e/2*(1-rho**2)*rho**(K+1)*((K+3)/(1-rho)+rho/(1-rho)**2)
        h=1-pin+tau; G=R[:,self.free]*self.B; c=self.w[self.free]*self.B
        x,z,zu,zl,info=ipm(c,G,h,tol=tol,verbose=verbose)
        a=np.zeros(K+1)
        for k,v in self.pinned.items(): a[k]=v
        a[self.free]=x*self.B
        info['obj']=c@x+cst
        return a,z,info
def certvalue(w,K,rho,psi,gam,lam,box=None,pinned=None,tailr=None,point=False):
    """Float estimate of the certified minorant: returns dict with d, e0 (with B penalty k>=4)"""
    R=rowmat(rho,psi,gam,K); q=lam@R; d=w+q; B=Bk(K); 
    s=(B[4:]*np.abs(d[4:])).sum()
    T=math.e/2*np.sum(lam*(1-rho**2)*rho**(K+1)*((K+3)/(1-rho)+rho/(1-rho)**2))
    return d,d[0]-lam.sum()-s-T
def cuts(a,K,rmax,nr=240,npsi=4096,topk=400,tol=1e-7,rmin=.02,rho_extra=None):
    """Separation: scan (1-rho^2)|f|, find local maxima with violation. Returns rho,psi,gam,maxviol"""
    # radii clustered to the outer edge
    t=np.linspace(0,1,nr); rg=rmin+(rmax-rmin)*(1-(1-t)**2)
    if rho_extra is not None: rg=np.sort(np.concatenate([rg,rho_extra]))
    pw=np.exp(np.arange(K+1)[None,:]*np.log(rg)[:,None])*a[None,:]
    F=np.fft.fft(pw,n=npsi,axis=1).conj()  # f(rho e^{i psi}) = sum a_k rho^k e^{+ik psi}
    V=(1-rg**2)[:,None]*np.abs(F)
    V=V[:,:npsi//2+1]; F=F[:,:npsi//2+1]
    # local maxima in 2D
    L=np.ones_like(V,dtype=bool)
    L[:,1:]&=V[:,1:]>=V[:,:-1]; L[:,:-1]&=V[:,:-1]>=V[:,1:]
    L[1:,:]&=V[1:,:]>=V[:-1,:]; L[:-1,:]&=V[:-1,:]>=V[1:,:]
    ii,jj=np.nonzero(L&(V>1+tol))
    mv=V.max()-1
    if len(ii)>topk:
        o=np.argsort(-V[ii,jj])[:topk]; ii,jj=ii[o],jj[o]
    psi=jj*2*np.pi/npsi
    return rg[ii],psi,np.angle(F[ii,jj]),mv
def save_cert(path,kind,K,r,eta,rho,psi,gam,lam):
    idx=np.nonzero(lam>0)[0]
    rows=[[float(rho[i]).hex(),float(psi[i]).hex(),float(gam[i]).hex(),float(lam[i]).hex()] for i in idx]
    json.dump({'kind':kind,'K':K,'r':float(r).hex(),'eta':float(eta).hex(),'rows':rows},open(path,'w'))
