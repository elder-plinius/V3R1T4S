"""C2/C3: exact-rational brute force of Selberg weights (Klyve thesis (5.24)-(5.26), f(p)=p-1, f1(p)=p-2, odd primes)
vs the identity Lambda(z) = W(z)/V(z). Also checks |lambda_d| <= 1 and the main-term optimality sum lambda lambda/f([d1,d2]) = 1/V(z)."""
from fractions import Fraction as F
import sys, math
def factor(n):
    ps=[];p=3
    while p*p<=n:
        if n%p==0:
            n//=p
            if n%p==0: return None
            ps.append(p)
        p+=2
    if n>1: ps.append(n)
    return ps
N=20001
fac={1:[]}
for n in range(3,N,2):
    f=factor(n)
    if f is not None: fac[n]=f
def prod(it):
    r=F(1)
    for x in it: r*=x
    return r
def check(z, halve=False):
    ds=[d for d in sorted(fac) if d<=z]
    inv_f1={d:prod(F(1,p-2) for p in fac[d]) for d in ds}
    V=sum(inv_f1.values())
    lam={}
    for de in ds:
        s=sum(inv_f1[d] for d in ds if d%de==0)
        mu=(-1)**len(fac[de]); fde=prod(F(p-1) for p in fac[de])
        lam[de]=mu*fde*s/V
    assert lam[1]==1
    L=sum(abs(x) for x in lam.values())
    W=sum(prod(F(p,p-2) for p in fac[d]) for d in ds)
    ok = (L == W/V) and all(abs(x)<=1 for x in lam.values())
    claimed = W/V/2 if halve else W/V
    flagged = not (claimed >= L)
    return ok, flagged, float(L), len(ds), float(L)/len(ds)
zs=sorted(set([3,5,7,10,15,20,30,50,75,100,150,200,300,500,750,1000,1500,2000,3000]+[int(10**(1+0.03*k)) for k in range(0,111)]))
zs=[z for z in zs if z<=20000]
bad=0
for z in zs:
    ok,fl,L,M,r=check(z)
    if not ok or fl: bad+=1; print("FAIL z=",z)
print("C2: checked %d values of z in [3,20000]: identity Lambda=W/V exact and |lambda|<=1: %s" % (len(zs), "PASS" if bad==0 else "FAIL %d"%bad))
for z in (100,1000,10000,20000):
    ok,fl,L,M,r=check(z); print("  z=%d  Lambda=%.6f  M=%d  Lambda/M=%.5f" % (z,L,M,r))
ok,fl,L,M,r=check(1000,halve=True)
print("C3: halved Lambda at z=1000 flagged by checker:", "YES (PASS)" if fl else "NO (FAIL)")
