#!/usr/bin/env python3
"""Independent REPRODUCE checker; written before reading author-code.
Definition, CLAIM.md: "For every integer n>=65536 and every integer j with
4<=j<=floor(n/2) and 2^36*(n-2j)^6<=n^5, there exists an odd prime dividing
both C(n,3) and C(n,j)."
Finite arithmetic checks corroborate, but do not prove, the universal argument.
"""
from math import comb, gcd
from fractions import Fraction as F
from collections import defaultdict
import json

def vp(x,p):
    e=0
    while x%p==0:
        e+=1; x//=p
    return e

def factval(n,p):
    v=0
    while n:
        n//=p; v+=n
    return v

def binval(n,j,p):
    return factval(n,p)-factval(j,p)-factval(n-j,p)

def factors(x):
    p=2
    while p*p<=x:
        if x%p==0:
            e=vp(x,p); yield p,e; x//=p**e
        p+=1
    if x>1: yield x,1

def shared(n,j):
    g=gcd(comb(n,3),comb(n,j))
    while g%2==0: g//=2
    return g>1
assert shared(8,4)
assert not shared(4,2)  # outside admissible j range, negative arithmetic test
local=0; direct=0; active3=0
for n in range(8,257):
    for j in range(4,n//2+1):
        assert shared(n,j); direct+=1
    for t in range(3):
        for p,e in factors(n-t):
            if p==2: continue
            assert binval(n,3,p)==e-(p==3)
            if p==3 and e==1: continue
            for j in range(n+1):
                if binval(n,j,p)==0:
                    assert j%(p**e)<=t
                    local+=1
                    if p==3: active3+=1

# Sparse polynomial implementation, independent of author data and code.
VARS=('n','d','a','b','k','l')
class P:
    def __init__(self,terms): self.t={m:c for m,c in terms.items() if c}
    @staticmethod
    def coerce(x): return x if isinstance(x,P) else P({(0,)*6:x})
    def __add__(self,x):
        x=P.coerce(x); out=defaultdict(int,self.t)
        for m,c in x.t.items():out[m]+=c
        return P(out)
    __radd__=__add__
    def __neg__(self):return P({m:-c for m,c in self.t.items()})
    def __sub__(self,x):return self+-P.coerce(x)
    def __rsub__(self,x):return P.coerce(x)+-self
    def __mul__(self,x):
        x=P.coerce(x); out=defaultdict(int)
        for m,c in self.t.items():
            for z,h in x.t.items():out[tuple(v+w for v,w in zip(m,z))]+=c*h
        return P(out)
    __rmul__=__mul__
    def __pow__(self,e):
        out=P.coerce(1)
        for _ in range(e):out=out*self
        return out
n,d,a,b,k,l=[P({tuple(int(i==j) for i in range(6)):1}) for j in range(6)]
U=a*d*l-2*b*k*(k-3*a)
V=a*l*l-2*b*U*(k-4*a)
R=k*(n-1)-a*(d*d-1)
S=(n-2)*l-2*b*d*(k-3*a)
T=(n-2)*U-2*b*(k+a)*(k-3*a)
assert not (T-(a*d*S-2*b*(k-3*a)*R)).t
# Direct independent expansion of the bracket after using the k relation.
assert not ((k*(n-1)+a)*(k-3*a)-(n-2)*(k+a)*(k-4*a)-((k-a)**2+4*a*a*(n-3))).t
# Full denominator-cleared v identity, without assuming either relation.
N=(k-3*a)*((k-a)**2+4*a*a*(n-3))
assert not ((n-2)**2*V-4*b*b*N-(a*S*S+4*a*b*d*(k-3*a)*S-2*b*(n-2)*(k-4*a)*T-4*b*b*(k-3*a)**2*R)).t

def strip(x):return 3 if vp(x,3)==1 else 1
fixtures=[]
for nn,jj in ((76672,26775),(3205956776,1556134875)):
    dd=nn-2*jj; aa=strip(nn-1); bb=strip(nn-2)
    AA=(nn-1)//aa; BB=(nn-2)//(2*bb)
    assert (dd*dd-1)%AA==0 and dd*(dd*dd-4)%BB==0
    kk=(dd*dd-1)//AA
    assert (dd*(kk-3*aa))%BB==0
    ll=dd*(kk-3*aa)//BB
    uu=aa*dd*ll-2*bb*kk*(kk-3*aa)
    vv=aa*ll*ll-2*bb*uu*(kk-4*aa)
    assert BB*uu==(kk+aa)*(kk-3*aa)
    assert BB*BB*vv==(kk-3*aa)*((kk-aa)**2+4*aa*aa*(nn-3))
    fixtures.append(dict(n=nn,j=jj,k=kk,l=ll,u=uu,v=vv,in_band=2**36*dd**6<=nn**5))
# Denominator bounds: each factor is at least n/2 for n>=4.
assert F(972)*32==31104 and F(3888)*8==31104
assert F(62208,65536)<1 and F(1,2**36)<F(1,2**16)
print(json.dumps(dict(definition_positive_negative='PASS',direct_pairs=direct,localization_checks=local,active_full_3_power_checks=active3,independent_polynomial_identities='PASS',constant_bounds='PASS',fixtures=fixtures,universal_proof='manual argument required; finite checks only'),indent=2))
