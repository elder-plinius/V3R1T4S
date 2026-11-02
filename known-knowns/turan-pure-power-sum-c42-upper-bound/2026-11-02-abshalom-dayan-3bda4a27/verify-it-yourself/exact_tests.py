#!/usr/bin/env python3
"""Exact small-case tests of (1.1), P_n = 0, (F2), (F3) and the identity for e. Standard library only.
Exit status 0 and last line 'exact tests ok' when every test holds."""
from fractions import Fraction as Fr
import random, math
class Q:
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a,s.b=Fr(a),Fr(b)
    def __add__(s,o): return Q(s.a+o.a,s.b+o.b)
    def __sub__(s,o): return Q(s.a-o.a,s.b-o.b)
    def __mul__(s,o): return Q(s.a*o.a-s.b*o.b,s.a*o.b+s.b*o.a)
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def n2(s): return s.a*s.a+s.b*s.b
    def scale(s,f): return Q(s.a*f,s.b*f)
    def fl(s): return complex(float(s.a),float(s.b))
def run(seed,n):
    random.seed(seed)
    z=[Q(1)]+[Q(Fr(random.randint(-9,9),10),Fr(random.randint(-9,9),10)) for _ in range(n-1)]
    # power sums
    pw=[Q(1) for _ in z];s=[None]
    for k in range(1,2*n+2):
        pw=[p*x for p,x in zip(pw,z)];t=Q();
        for p in pw:t=t+p
        s.append(t)
    # g = prod_{i>=2}(1-z_i x), coefficients up to 2n
    g=[Q(1)]+[Q() for _ in range(2*n)]
    for x in z[1:]:
        for m in range(2*n,0,-1): g[m]=g[m]-x*g[m-1]
    P=g
    assert P[n]==Q(),"P_n != 0"
    M=[Q()];A=[0.0]
    for j in range(2*n+1):M.append(M[-1]+P[j]);A.append(A[-1]+abs(P[j].fl()))
    c=[M[j+1] for j in range(2*n+1)]
    def E(l):
        t=Q()
        for i in range(1,l+1):t=t+s[i]*P[l-i]
        return t
    for l in range(1,2*n):
        assert P[l].scale(l)==M[l]-E(l),"(1.1)"
    N=[Q()]
    for j in range(2*n):N.append(N[-1]+c[j])
    for t in range(1,2*n):
        e1=Q()
        for i in range(1,t+1):e1=e1+s[i]*c[t-i]
        assert e1==N[t].scale(2)-c[t].scale(t),"(F2)"
        beta=Q(Fr(1,3),Fr(-2,7))
        lhs=E(t)+(beta*e1).scale(Fr(1,t))
        rhs=Q()
        for j in range(t):rhs=rhs+s[t-j]*(P[j]+(beta*c[j]).scale(Fr(1,t)))
        assert lhs==rhs,"(F3) identity"
def e_identity(trials=20000):
    random.seed(7)
    for _ in range(trials):
        y=random.uniform(.6,.8);T=.501
        w=complex(y-T*random.uniform(0,1)*math.cos(th:=random.uniform(0,6.3)),T*math.sin(th)*random.uniform(0,1))
        mu=(T*T-y*y*(1-y*y))/(2*y)
        a=mu+w.real-y*abs(w);b=((abs(w)-y*y)**2+T*T-abs(y-w)**2)/(2*y)
        assert abs(a-b)<1e-12,"e identity"
for seed,n in ((1,2),(2,3),(3,5),(4,8),(5,8),(6,12),(7,12)): run(seed,n)
e_identity()
print("exact tests ok")
