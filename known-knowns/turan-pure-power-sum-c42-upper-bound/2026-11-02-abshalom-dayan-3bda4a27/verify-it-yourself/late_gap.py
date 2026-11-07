#!/usr/bin/env python
"""(LATE) and (GAP) of reduction.md for T=501/1000, b=7/2000, beta=-(17/20)i, gamma=1/2+(433/500)i, Lam0=5, Lam1=10, alpha=6/5, L=8.
LATE: y_{l+1}=y_l-mu(y_l)/l from y_1=1, two independent lower-bound iterations (Arb lower endpoints; exact integers at scale 2^128, rounding y down).
Uses that y -> y-h mu(y) is increasing on (0,1] for h<=1 (reduction.md, Step 1), so a lower bound stays a lower bound.
GAP: all constants in Arb from exact rationals; L_tau,L_phi and V(0,0) from the exact float values in V_b.npy; (TERM) lower bound in Arb with chord bounds."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from flint import arb, ctx
ctx.prec=256
base=sys.argv[1]
J0=10**6
T=Fr(501,1000); b=Fr(7,2000); bet=Fr(17,20); gr=Fr(1,2); gi=Fr(433,500); L0=Fr(5); L1=Fr(10); al=Fr(6,5); L=Fr(8)
assert gr*gr+gi*gi<=1
def A(q): return arb(q.numerator)/arb(q.denominator)
aT=A(T)
# ---- LATE, Arb
t0=time.time()
y=arb(1); T2=aT*aT
for l in range(1,J0):
    y2=y*y
    z=y-(T2-y2*(1-y2))/(2*y)/l
    y=z.lower()
    y=arb(y.mid()) if y.rad()==0 else y.lower()
yarb=y
print('LATE Arb: y_J0 >=',yarb.str(25),'J0',J0,'time',round(time.time()-t0,1),flush=True)
# ---- LATE, integers, scale S=2^128: Y/S is a lower bound of y_l
t0=time.time()
S=1<<128; Y=S; S2=S*S; S4=S2*S2
for l in range(1,J0):
    y2=Y*Y
    N=251001*S4-10**6*y2*S2+10**6*y2*y2           # mu = N/(10^6 S^4) / (2 Y/S)
    den=2*10**6*S2*Y*l
    Y=Y-(-((-N)//den))                             # subtract ceil(N/den) (N>=0 since mu>=0)
yint=Fr(Y,S)
print('LATE integers: y_J0 >=',float(yint),'time',round(time.time()-t0,1),flush=True)
yl=min(Fr(int(float(yint)*10**12),10**12), yint)
assert yl<=yint and arb(yl.numerator)/yl.denominator<=yarb+arb(10)**-9
# rho_+=1/sqrt2+b exact comparison: y>rho_+ iff (y-b)^2>1/2
assert yl>b and (yl-b)**2>Fr(1,2)
print('LATE holds: y_J0 >= %s > rho_+ (checked by exact squaring)'%float(yl))
# ---- table constants
P=json.load(open(base+'.json')); V=np.load(base+'.npy')
assert P['T']==0.501 and P['b']==0.0035 and P['beta_im']==-0.85 and P['gamma_re']==0.5 and P['gamma_im']==0.866 and P['L0']==5 and P['L1']==10 and P['al']==1.2 and P['L']==8
nt,nth=P['nt'],P['nth']; assert V.shape==(nt+1,nth)
d=Fr(8,nt); PI=arb.pi(); dth=2*PI/nth
dVt=np.abs(V[1:]-V[:-1]).max(); dVp=np.abs(np.roll(V,-1,1)-V).max()
Ltau=A(Fr(float(dVt))/d)*(1+arb(2)**-50); Lphi=(arb(float(dVp))/dth)*(1+arb(2)**-50)
V00=A(Fr(float(V[nt,0])))
print('L_tau',Ltau.str(10),'L_phi',Lphi.str(10),'V(0,0)',V00.str(12),'V range',float(V.min()),float(V.max()))
# ---- derived constants of reduction.md
rs=arb(1)/arb(2).sqrt(); rm=rs-A(b); rp=rs+A(b); aB=A(bet); aL0=A(L0); aL1=A(L1); aal=A(al); aL=A(L)
assert rm>aT
def mu(y): return (aT*aT-y*y*(1-y*y))/(2*y)
Wb=rp+aT; Zb=Wb/rm
assert arb(J0)>=2*Zb+2 and arb(J0)*aal>=1
# mu is convex on (0,inf) (mu''=T^2/y^3+3y>0), so its max on the band is at an end
mumax=mu(rp) if mu(rp)>mu(rm) else mu(rm)
if not (mu(rp)>mu(rm) or mu(rm)>mu(rp)): raise SystemExit('cannot order mu at ends')
eb=mumax+Wb*(1+rp)
C0=Ltau/2+Lphi*Zb*Zb+Wb*(Ltau+Lphi*Zb)+aT*aB*rp+2*aB*rp*(1+Zb)+(aT+2)*aB*Wb+2*aal*aL1*eb
eps1=(2*C0+2*Ltau+(aT+2)*aB+aB*Wb)/J0
Cp=aL0+aL1/aal
varpi=Wb/J0
bp2=2*A(b)-mu(rp)/J0
print('Wb',Wb.str(10),'Zb',Zb.str(10),'mu_max',mumax.str(12),'mu(rho_+)',mu(rp).str(12),'mu(rho_-)',mu(rm).str(12),'eb',eb.str(8))
print('C0',C0.str(10),'eps1',eps1.str(10),"C'",Cp.str(10),'varpi',varpi.str(6),"2b'",bp2.str(12))
# ---- TERM lower bound in Arb, chord bounds in rho and psi
gam=None
M=4096; NR=32
dl=PI/M; dr=2*A(b)/NR
u_max=rp+aT+rp*rp; Wpp=aT*rp/(rm-aT); epp=(aT*aT+u_max*Wpp)/rm
W_rr=1/(rm-aT); up=1+2*rp; upp=W_rr+2
e_rr=(up*up+u_max*upp)/rm+2*u_max*up/(rm*rm)+u_max*u_max/(rm*rm*rm)
Kt=aT+aL0*epp        # |gamma|<=1
Er=dr*dr/8*aL0*e_rr
ag_r=A(gr); ag_i=A(gi)
cs=[(PI+dl*i) for i in range(M+1)]
cc=[(c.cos(),c.sin()) for c in cs]
best=None; t0=time.time(); wh=None
for ir in range(NR+1):
    rho=rm+dr*ir
    vals=[]
    for c,s in cc:
        W=((rho-aT*c)**2+(aT*s)**2).sqrt()
        # Re(gamma*(T e^{i psi} - beta rho)), beta=-i*bet: -beta rho = +i bet rho
        re=aT*c; im=aT*s+aB*rho
        t=ag_r*re-ag_i*im+aL0*(W-rho*rho)**2/(2*rho)
        vals.append(t)
    for i in range(M):
        lo=vals[i].lower() if vals[i].lower()<vals[i+1].lower() else vals[i+1].lower()
        if best is None or lo<best: best=lo; wh=(float(rho),float(cs[i]))
term=best-Kt*dl*dl/8-Er
print('TERM min in Arb >=',term.str(12),'at rho,psi',wh,'chord',(Kt*dl*dl/8).str(4),Er.str(4),'time',round(time.time()-t0,1))
m=term-V00
print('m = TERM - V(0,0) >=',m.str(12))
etap=(m-eps1)/Cp
print("eta' =",etap.str(12))
g1=etap-(1+varpi)*mumax
g2=bp2-mumax*(aL+arb(1)/J0)
print("GAP1 eta'-(1+varpi)mu_max =",g1.str(10),'  ',g1>0)
print("GAP2 2b'-mu_max(L+1/J0) =",g2.str(10),'  ',g2>0)
req=eps1+Cp*(1+varpi)*mumax
print('smallest m that passes GAP1 with these constants:',req.str(10))
assert g1>0 and g2>0
print('GAP OK (given HJB and INIT from the certifier)')
print('INIT slack',(A(Fr(float(V[0].min())))-(aT+(aT+2)*aB*(-aL).exp())).str(10))
