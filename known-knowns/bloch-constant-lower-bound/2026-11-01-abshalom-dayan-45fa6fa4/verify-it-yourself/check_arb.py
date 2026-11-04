# check_arb.py libdir prefix T eta : full third replay of a cover in Arb balls (128 bit), no trig table, no C.
# Same mathematical inequality as check.c (second-order Taylor in (A,rho,phi,theta)); arithmetic and cosines fully by Arb.
import sys,struct,math,time
from flint import arb,ctx
ctx.prec=128
lib,pre,Ts,etas=sys.argv[1:5]
t0=time.time()
Tp=arb(3).sqrt()/4+arb(float(Ts))
eta=float(etas); rho0=math.floor(eta*2**20)/2**20
M=[l.split() for l in open(lib+"/minorants.txt")]
E=[arb(float.fromhex(m[0])) for m in M];P=[arb(float.fromhex(m[1])) for m in M];Q=[arb(float.fromhex(m[2])) for m in M]
Ef=[float(x) for x in E];Pf=[float(x) for x in P];Qf=[float(x) for x in Q]
EX=[l.split() for l in open(lib+"/excl.txt")]; SV=[arb(float.fromhex(a)) for a,b in EX]; RV=[arb(float.fromhex(b)) for a,b in EX]
Cdbl=None
for l in open(lib+"/meta.txt"):
    a=l.split()
    if a[0]=="C_up": Cdbl=float.fromhex(a[1])
PI=arb.pi(); N=2**18; cc={}
def tc(i):
    i%=N
    v=cc.get(i)
    if v is None:
        v=(PI*2*i/N).cos(); cc[i]=v
    return v
def ts(i): return tc(i-N//4)
d=open(pre+".leaves","rb").read(); RS=struct.Struct("<4B4I"); wb=open(pre+".wits","rb").read()
n=len(d)//20; W=[struct.unpack_from("<11d",wb,i*88) for i in range(len(wb)//88)]
evals=0;mn=None;n0=n1=n2=0
def absu(x): return abs(x).upper()
for li in range(n):
    la,lr,lu,k,ia,ir,iu,w=RS.unpack_from(d,li*20)
    hA=arb(1)/2**(la+1); Am=hA*(2*ia+1); hR=arb(2)/2**lr; Rm=arb(rho0)+hR*(2*ir+1); hU=arb(1)/2**(lu+1); Um=hU*(2*iu+1)
    if k==2:
        assert Rm-hR>arb(Cdbl),("out",li); n2+=1; continue
    assert k in (0,1),("kind",li,k)
    hphi=hU*PI/2; pi=(2*iu+1)*2**(15-lu); Rmax=Rm+hR; Amax=Am+hA
    if k==1:
        s=w&63; t=w>>6
        c2=tc(2*t);c3=tc(3*t+pi);s3=ts(3*t+pi)
        lb=-Am*c2-hA*abs(c2)+SV[s]*(Rm*c3-hR*abs(c3)-Rmax*(abs(s3)*hphi+hphi*hphi/2))
        assert lb>RV[s],("excl",li); n1+=1; continue
    x=W[w]
    dA=Am-arb(x[0]);dR=Rm-arb(x[1]);dU=Um-arb(x[2])
    Jx=[arb(v) for v in x[5:8]];Jy=[arb(v) for v in x[8:11]]
    cx=arb(x[3])+Jx[0]*dA+Jx[1]*dR+Jx[2]*dU; cy=arb(x[4])+Jy[0]*dA+Jy[1]*dR+Jy[2]*dU
    JA=(Jx[0]**2+Jy[0]**2).sqrt();JR=(Jx[1]**2+Jy[1]**2).sqrt();JU=(Jx[2]**2+Jy[2]**2).sqrt()
    cn=(cx*cx+cy*cy).sqrt()+JA*hA+JR*hR+JU*hU
    assert cn<arb(0.22),("c",li)
    hint=[0]
    Rmaxf=float(Rmax);Amaxf=float(Amax);hphif=float(hphi);JAf=float(JA);JRf=float(JR);JUf=float(JU);cnf=float(cn)
    def rem(j,dl):
        q=abs(Q[j]);p=abs(P[j])
        return q*Rmax*hphi*hphi/2+q*hR*hphi+((3*q+JR)*hR+3*q*Rmax*hphi+JU*hU+(2*p+JA)*hA)*dl+(4*p*Amax+9*q*Rmax+cn)*dl*dl/2
    def lbj(j,c1,s1,c2,s2,c3,s3,dl):
        p=P[j];q=Q[j]
        G=E[j]-p*Am*c2+q*Rm*c3-cx*c1-cy*s1
        DA=-p*c2-Jx[0]*c1-Jy[0]*s1
        DR=q*c3-Jx[1]*c1-Jy[1]*s1
        DU=-q*Rm*s3*PI/2-Jx[2]*c1-Jy[2]*s1
        DT=2*p*Am*s2-3*q*Rm*s3+cx*s1-cy*c1
        return G-abs(DA)*hA-abs(DR)*hR-abs(DU)*hU-abs(DT)*dl-rem(j,dl)
    def iv(kk,dep):
        global evals,mn
        ti=(2*kk+1)*2**(17-dep); dl=PI/2**dep
        c1,s1,c2,s2,c3,s3=tc(ti),ts(ti),tc(2*ti),ts(2*ti),tc(3*ti+pi),ts(3*ti+pi)
        evals+=1
        v=lbj(hint[0],c1,s1,c2,s2,c3,s3,dl)-Tp
        if v>0:
            if mn is None or v<mn: mn=v
            return True
        fm=[float(z) for z in (c1,s1,c2,s2,c3,s3)]; A_=float(Am);R_=float(Rm);hA_=float(hA);hR_=float(hR);hU_=float(hU);dl_=float(dl);cxf=float(cx);cyf=float(cy)
        best=-9;bj=hint[0]
        for j in range(len(E)):
            pf,qf=Pf[j],Qf[j]
            g=Ef[j]-pf*A_*fm[2]+qf*R_*fm[4]-cxf*fm[0]-cyf*fm[1]
            dt=2*pf*A_*fm[3]-3*qf*R_*fm[5]+cxf*fm[1]-cyf*fm[0]
            da=-pf*fm[2]-x[5]*fm[0]-x[8]*fm[1]; dr=qf*fm[4]-x[6]*fm[0]-x[9]*fm[1]; du=-qf*R_*fm[5]*1.5707963-x[7]*fm[0]-x[10]*fm[1]
            aq=abs(qf);ap=abs(pf);b=g-abs(dt)*dl_-abs(da)*hA_-abs(dr)*hR_-abs(du)*hU_-(aq*Rmaxf*hphif*hphif/2+aq*hR_*hphif+((3*aq+JRf)*hR_+3*aq*Rmaxf*hphif+JUf*hU_+(2*ap+JAf)*hA_)*dl_+(4*ap*Amaxf+9*aq*Rmaxf+cnf)*dl_*dl_/2)
            if b>best: best=b;bj=j
        hint[0]=bj
        v=lbj(bj,c1,s1,c2,s2,c3,s3,dl)-Tp
        evals+=1
        if v>0:
            if mn is None or v<mn: mn=v
            return True
        assert dep<17,("theta depth",li,kk)
        return iv(2*kk,dep+1) and iv(2*kk+1,dep+1)
    for kk in range(32):
        assert iv(kk,5),("cert",li,kk)
    n0+=1
print("ARB-PASS T=%s eta=%s leaves=%d cert=%d excl=%d out=%d evals=%d min_margin_lower=%.4e wall=%.1fs"%(Ts,etas,n,n0,n1,n2,evals,float(mn.lower()),time.time()-t0))
