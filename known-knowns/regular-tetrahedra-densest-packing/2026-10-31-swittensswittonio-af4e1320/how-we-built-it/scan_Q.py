"""NUMERICAL scan (mp floats) of the decoupled scheme with deficit-ball class K(0,Q): u = gamma_Q * R0."""
import sys, math
sys.path.insert(0,'.')
from mpmath import mp, mpf, sqrt, pi, findroot
import aexact
import profile_dp as P
mp.dps=25
al=P.al; a=aexact.a_exact
def gam(q):
    # alpha + q a(r) = 1
    lo,hi=mpf(0),mpf(1)
    for _ in range(100):
        m=(lo+hi)/2
        if al+q*a(m)>1: lo=m
        else: hi=m
    return lo
G={q:gam(q) for q in range(5,80)}
# rho(0,Q) sequence via 1-param solve (all-wedge states)
rho0={}
P.NMAX=5
for (c,w) in P.order:
    P.rho[(c,w)]=P.state_val(c,w); P.mono_close()
rho0[5]=P.rho[(0,5)]
def cov_ok(T,Qn):
    tot=mpf(0)
    for i in range(1,Qn):          # i-th non-central object, enters when i-1 present: state (0,i)
        u=(T/rho0[i])**(mpf(1)/3)
        if u<1: tot+=a(u)
    return tot<=1-al
for i in range(1,5): rho0[i]=P.rho[(0,i)] if (0,i) in P.rho else None
rho0[1]=1-al; rho0[2]=mpf(1)/2-al
for Qn in range(6,41):
    lo,hi=mpf(0),rho0[Qn-1]
    if cov_ok(lo,Qn): rho0[Qn]=lo
    else:
        for _ in range(100):
            mid=(lo+hi)/2
            if cov_ok(mid,Qn): hi=mid
            else: lo=mid
        rho0[Qn]=hi
    if Qn in (6,7,8,10,15,20,30,40): print("rho_hat(0,%d)=%.4e  gamma_%d=%.4f  gamma^3*rho=%.3e"%(Qn,rho0[Qn],Qn,G[Qn],G[Qn]**3*rho0[Qn]),flush=True)
print("rho_hat(0,5)=%.4e gamma5=%.4f gamma^3 rho=%.3e"%(rho0[5],G[5],G[5]**3*rho0[5]))
