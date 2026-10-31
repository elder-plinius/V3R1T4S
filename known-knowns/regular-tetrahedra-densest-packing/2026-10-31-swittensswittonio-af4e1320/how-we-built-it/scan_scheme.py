"""NUMERICAL scan of the decoupled counting scheme (see REDUCTION.md section E) for several deficit classes Q.
floats only (mp 25 digits); the best parameters are then certified in cert_final.py."""
import sys, math
from mpmath import mp, mpf, sqrt, pi
sys.path.insert(0,'.')
import aexact
mp.dps=25
th=mp.acos(mpf(1)/3); al=th/(2*pi)
a=aexact.a_exact
RHOQ=mpf('4.7118e-12'); RHO5=mpf('1.1254e-11')
def gam(q):
    lo,hi=mpf(0),mpf(1)
    for _ in range(80):
        m=(lo+hi)/2
        if al+q*a(m)>1: lo=m
        else: hi=m
    return lo
GMAX=int(sys.argv[2]) if len(sys.argv)>2 else 400
Gt=[None]*(GMAX+1)
def G(q):
    if Gt[q] is None: Gt[q]=gam(q)
    return Gt[q]
VB=4*pi/3; VT=sqrt(2)/12; kap=sqrt(2)/3; s23=sqrt(mpf(2)/3); e,g=6,4
def evalp(Q,rhoQ,k,u):
    gq=G(Q)
    rv=u/(gq*kap); sigma=2*u; d=(1-(k-1)*sigma)/2; delta=2*u
    if d<=2*rv or d<4*u: return None
    def qmin(dl,R1):
        if R1<=0: return None
        for q in range(5,GMAX):
            if G(q)*R1>dl: return q
        return None
    q=qmin(delta,s23*d-delta); qv=qmin(2*rv,s23*d-2*rv)
    if q is None or qv is None: return None
    m=math.ceil(float(2*delta/sigma)-1e-12); mv=int(math.floor(float(2*rv/sigma)))+1
    good=e*k-g*qv*mv
    if good<=0: return None
    Delta=m*(q-1)
    b=mpf(good)/(Delta+1)*VB/VT*u**3*rhoQ
    return b,dict(Q=Q,k=k,u=float(u),q=q,qv=qv,m=m,mv=mv,good=good,Delta=Delta,d=float(d),rv=float(rv))
if __name__=="__main__":
    Q=int(sys.argv[1]); rhoQ=RHO5 if Q==5 else RHOQ
    best=None
    for ui in [x/1e5 for x in range(60,3000,20)]:
        u=mpf(ui)
        for k in list(range(2,60))+list(range(60,400,5)):
            r=evalp(Q,rhoQ,k,u)
            if r and (best is None or r[0]>best[0]): best=r
    print("Q=%d best b=%.4e"%(Q,best[0]),best[1])
