# validate.py libdir prefix T eta [npts] : independent numpy replay (not rigorous; a bug detector, separate formula code)
import sys, struct, math
import numpy as np
lib,pre,T,eta=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
npts=int(sys.argv[5]) if len(sys.argv)>5 else 3000
M=[l.split() for l in open(lib+"/minorants.txt")]
E=np.array([float.fromhex(m[0]) for m in M]);P=np.array([float.fromhex(m[1]) for m in M]);Q=np.array([float.fromhex(m[2]) for m in M])
EX=[l.split() for l in open(lib+"/excl.txt")]; SV=[float.fromhex(a) for a,b in EX]; RV=[float.fromhex(b) for a,b in EX]
rho0=math.floor(eta*2**20)/2**20
d=np.frombuffer(open(pre+".leaves","rb").read(),dtype=np.dtype([('la','u1'),('lr','u1'),('lu','u1'),('k','u1'),('ia','<u4'),('ir','<u4'),('iu','<u4'),('w','<u4')]))
W=np.fromfile(pre+".wits",dtype='<f8').reshape(-1,11)
Alo=d['ia']/2.0**d['la'];Ahi=(d['ia']+1.0)/2.0**d['la']
Rlo=rho0+4*d['ir']/2.0**d['lr'];Rhi=rho0+4*(d['ir']+1.0)/2.0**d['lr']
Ulo=d['iu']/2.0**d['lu'];Uhi=(d['iu']+1.0)/2.0**d['lu']
vol=((Ahi-Alo)*(Rhi-Rlo)*(Uhi-Ulo)).sum(); print("vol ratio",vol/4)
def locate(A,R,U):
    m=(Alo<=A)&(A<=Ahi)&(Rlo<=R)&(R<=Rhi)&(Ulo<=U)&(U<=Uhi)
    return np.nonzero(m)[0]
th=np.linspace(0,2*np.pi,1<<15,endpoint=False)
cT,sT=np.cos(th),np.sin(th)
Tp=math.sqrt(3)/4+T
def cval(i,A,R,U):
    w=W[d['w'][i]]
    dx=np.array([A-w[0],R-w[1],U-w[2]])
    return w[3]+w[5:8]@dx, w[4]+w[8:11]@dx
def primalmin(A,R,U,cx,cy):
    phi=U*math.pi/2
    b2=-A*np.cos(2*th); b3=R*np.cos(3*th+phi)
    H=(E[:,None]+P[:,None]*b2[None,:]+Q[:,None]*b3[None,:]).max(axis=0)
    return (H-cx*cT-cy*sT).min()
import os
VC=float(os.environ.get('VC','3.2888'))
rng=np.random.default_rng(12345)
Amin=9;cnt={0:0,1:0,2:0};worst=(9,)
def test(A,R,U):
    global worst
    ids=locate(A,R,U)
    assert len(ids)>=1,(A,R,U)
    i=ids[0];k=int(d['k'][i]);cnt[k]+=1
    if k==2:
        assert R>VC; return
    if k==1:
        s=int(d['w'][i]&63);tk=int(d['w'][i]>>6);tau=2*math.pi*tk/2**18
        v=-A*math.cos(2*tau)+SV[s]*R*math.cos(3*tau+U*math.pi/2)
        assert v>RV[s],("excl fails",A,R,U,v,RV[s]); return
    cx,cy=cval(i,A,R,U); assert math.hypot(cx,cy)<0.22
    v=primalmin(A,R,U,cx,cy)
    if v<worst[0]: worst=(v,A,R,U,i)
    assert v>Tp,("primal fails",A,R,U,v-Tp)
for _ in range(npts):
    test(rng.uniform(0,1),rng.uniform(eta,VC),rng.uniform(0,1))
for _ in range(npts): # valley-focused
    test(1-rng.uniform(0,0.03)**1.0,rng.uniform(eta,min(eta+0.8,VC)),rng.uniform(0,1))
for i in rng.integers(0,len(d),npts//3): # leaf corners
    for a in (Alo[i],Ahi[i]):
        for r in (max(Rlo[i],eta),min(Rhi[i],VC)):
            for u in (Ulo[i],Uhi[i]):
                if d['k'][i]!=2 and eta<=r<=VC: test(a,r,u)
print("points by kind",cnt,"worst gain margin on dense grid %.3e at A=%.6f rho=%.6f u=%.6f"%(worst[0]-Tp,*worst[1:4]))
# --- explicit members, end to end ---
s3=math.sqrt(3)
gl_x,gl_w=np.polynomial.legendre.leggauss(80); r0=float(os.environ.get('VR',str(1/s3))); tt=(gl_x+1)/2*r0; ww=gl_w/2*r0
def f1(z): return (1-s3*z)/(1-z/s3)**3
def fone(z): return np.ones_like(z)
def fq(z): return 1-z*z
# membership sanity of generators
rr=np.linspace(0,0.999,400)[:,None];pp=np.exp(1j*np.linspace(0,2*np.pi,721))[None,:]; zz=rr*pp
for f,n in ((f1,"f1"),(fq,"1-z^2")):
    m=((1-np.abs(zz)**2)*np.abs(f(zz))).max(); print("sup (1-|z|^2)|%s| = %.6f"%(n,m))
    assert m<=1+1e-9
def Rtrue(comp,th_):
    # comp: list of (w,gen,tau,conj) f(z)=sum w gen(e^{i tau} z) possibly conj
    z=tt[None,:]*np.exp(1j*th_)[:,None]
    v=np.zeros_like(z,dtype=complex)
    for w_,g,tau in comp: v=v+w_*g(np.exp(1j*tau)*z)
    return v
th2=np.linspace(0,2*np.pi,1440,endpoint=False)
a2gen={'f1':-1.0,'one':0.0,'q':-1.0}; a3gen={'f1':-8/(3*s3),'one':0.0,'q':0.0}; G={'f1':f1,'one':fone,'q':fq}
def endtoend(comp):
    # comp entries (w,name,tau)
    a2=sum(w*a2gen[n]*np.exp(2j*t) for w,n,t in comp); a3=sum(w*a3gen[n]*np.exp(3j*t) for w,n,t in comp)
    A=abs(a2); tau=(np.pi-np.angle(a2))/2 if A>0 else 0.0
    a3r=a3*np.exp(3j*tau); 
    if a3r.real<0: tau+=np.pi; a3r=-a3r
    conj=a3r.imag<0
    R_=abs(a3r); phi=abs(np.angle(a3r))
    if R_<eta or R_>VC: return None
    # function g(z)=f(e^{i tau} z) or conj f(e^{i tau} conj z)
    C=[(w,G[n],t+tau) for w,n,t in comp]
    def R_of(th_):
        zr=tt[None,:]*np.exp(1j*th_)[:,None]
        v=np.zeros_like(zr,dtype=complex)
        for w_,g,t_ in C: v=v+w_*g(np.exp(1j*t_)*(np.conj(zr) if conj else zr))
        if conj: v=np.conj(v)
        return (v.real*ww[None,:]).sum(axis=1)
    Rv=R_of(th2)
    U=min(phi/(np.pi/2),1.0); A=min(float(A),1.0)
    b2=-A*np.cos(2*th2); b3=R_*np.cos(3*th2+phi)
    H=(E[:,None]+P[:,None]*b2[None,:]+Q[:,None]*b3[None,:]).max(axis=0)
    assert (H<=Rv+1e-9).all(),("minorant exceeds true R",comp,(H-Rv).max())
    ids=locate(A,R_,U); i=ids[0]; k=int(d['k'][i])
    if k!=0: return ('excluded member!',A,R_,U,k)
    cx,cy=cval(i,A,R_,U)
    gain=(Rv-cx*np.cos(th2)-cy*np.sin(th2)).min()-math.sqrt(3)/4
    return (gain,(H-Rv).max(),A,R_,U)
res=endtoend([(1.0,'f1',0.0)])
if res: print("Bonk extremal: gain with witness centre %.6f, max(H-R)=%.3e, A=%.3f rho=%.4f u=%.3f"%res)
rngm=np.random.default_rng(7); low=9;nmem=0;mx=-9;nex=0;lowr=(0,0,0,0,0)
for t_ in range(4000):
    n=rngm.integers(1,5); w=rngm.dirichlet(np.ones(n)*rngm.choice([0.3,1,3]))
    spread=rngm.choice([0.02,0.1,0.3,1.0,3.14])
    comp=[]
    for wi in w:
        nm=rngm.choice(['f1','f1','f1','one','q'])
        tau_=rngm.normal(0,spread)+rngm.choice([0,np.pi])
        comp.append((wi,nm,tau_))
    r_=endtoend(comp)
    if r_ is None: continue
    if isinstance(r_[0],str): nex+=1; print(r_); continue
    nmem+=1
    if r_[0]<low: low=r_[0];lowr=r_
    mx=max(mx,r_[1])
print("members tested (|a3|>=eta): %d, excluded-but-member errors: %d, min true gain with witness %.6f (A=%.4f rho=%.4f u=%.3f), max(H-R) over members and theta %.3e"%(nmem,nex,low,lowr[2],lowr[3],lowr[4],mx))
assert nex==0 and low>T
print("VALIDATE OK")
