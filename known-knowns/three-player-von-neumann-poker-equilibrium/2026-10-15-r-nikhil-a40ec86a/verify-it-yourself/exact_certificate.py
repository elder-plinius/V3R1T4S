"""Standard-library exact b=2 certificate checker: Q[t]/P(t), Sturm, intervals.
The algebraic equality checks do not use floating point or SymPy.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from pathlib import Path
import json,sys

def trim(a):
    a=list(map(F,a))
    while len(a)>1 and not a[-1]:a.pop()
    return a

def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def divrem(a,b):
    a=trim(a);b=trim(b);assert b!=[0]
    q=[F(0)]*max(1,len(a)-len(b)+1)
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b);z=a[-1]/b[-1];q[k]+=z
        a=sub(a,[0]*k+[z*x for x in b])
    return trim(q),trim(a)
def ev(a,x):
    z=F(0)
    for c in reversed(a):z=z*x+c
    return z
def deriv(a):return trim([i*a[i] for i in range(1,len(a))] or [0])
def sturm(a):
    out=[trim(a),deriv(a)]
    while out[-1]!=[0]:
        z=neg(divrem(out[-2],out[-1])[1])
        if z==[0]:break
        out.append(z)
    return out

def variations(seq,x):
    signs=[1 if ev(a,x)>0 else -1 for a in seq if ev(a,x)]
    return sum(x!=y for x,y in zip(signs,signs[1:]))
def count(a,lo,hi):
    assert lo<hi and ev(a,lo)!=0 and ev(a,hi)!=0
    seq=sturm(a);return variations(seq,lo)-variations(seq,hi)
P=[245,280,-3252,-2968,14782,9288,-29460,-7560,19845]
class K:
    def __init__(self,a):self.a=divrem(a.a if isinstance(a,K) else (a if isinstance(a,list) else [a]),P)[1]
    def __add__(self,o):return K(add(self.a,K(o).a))
    __radd__=__add__
    def __neg__(self):return K(neg(self.a))
    def __sub__(self,o):return self+-K(o)
    def __rsub__(self,o):return K(o)+-self
    def __mul__(self,o):return K(mul(self.a,K(o).a))
    __rmul__=__mul__
    def inv(self):
        r0,r1=trim(P),self.a;t0,t1=[F(0)],[F(1)]
        while r1!=[0]:
            q,r=divrem(r0,r1);r0,r1=r1,r;t0,t1=t1,sub(t0,mul(q,t1))
        assert len(r0)==1 and r0[0]
        return K([x/r0[0] for x in t0])
    def __truediv__(self,o):return self*K(o).inv()
    def __rtruediv__(self,o):return K(o)*self.inv()
    def __pow__(self,n):
        assert n>=0;z=K(1)
        for _ in range(n):z=z*self
        return z
    def __eq__(self,o):return self.a==K(o).a
    def __repr__(self):return str(self.a)

@dataclass(frozen=True)
class I:
    lo:F
    hi:F
    def __post_init__(self):assert self.lo<=self.hi
    @staticmethod
    def coerce(x):return x if isinstance(x,I) else I(F(x),F(x))
    def __add__(self,o):o=I.coerce(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-I.coerce(o)
    def __rsub__(self,o):return I.coerce(o)+-self
    def __mul__(self,o):
        o=I.coerce(o);v=[a*b for a in [self.lo,self.hi] for b in [o.lo,o.hi]];return I(min(v),max(v))
    __rmul__=__mul__
    def inv(self):
        assert self.lo*self.hi>0
        return I(1/self.hi,1/self.lo)
    def __truediv__(self,o):return self*I.coerce(o).inv()
    def __rtruediv__(self,o):return I.coerce(o)*self.inv()
    def __pow__(self,n):
        z=I.coerce(1)
        for _ in range(n):z=z*self
        return z
    def inside(self,o):return o.lo<=self.lo and self.hi<=o.hi
    def strings(self):return [str(self.lo),str(self.hi)]

def thresholds(B):
    C=(3*B**2-1)/(2*B)
    A=2*(1-B)/(7*C-2)
    return A,C

def gamevalue(A,B,C):return -A**3+5*A*C**2-2*A-2*B**3+2*B**2*C+2*B-2*C

def decimal(q,places=55):
    from decimal import Decimal,localcontext
    with localcontext() as c:
        c.prec=places
        return str(Decimal(q.numerator)/Decimal(q.denominator))

def check(obj):
    assert obj['bet']==2 and obj['information']=='simultaneous callers; own hand only'
    assert obj['A_definition']=='2*(1-B)/(7*C-2)'
    assert obj['C_definition']=='(3*B^2-1)/(2*B)'
    assert obj['value_definition']=='-A^3+5*A*C^2-2*A-2*B^3+2*B^2*C+2*B-2*C'
    assert obj['profile']=='I bets for x<A or x>B; II and III call for y>C; threshold ties arbitrary; endpoints chosen by continuity'
    assert obj['B_polynomial_ascending']==P
    B=K([0,1]);A,C=thresholds(B)
    assert 3*A**2-5*C**2+2==0
    assert 3*B**2-2*C*B-1==0
    assert 7*C*A-2*(A+1-B)==0
    vb=gamevalue(A,B,C)
    assert list(map(F,obj['value_in_B_ascending']))==vb.a
    bb=I(*map(F,obj['B_interval']))
    assert count(P,bb.lo,bb.hi)==1
    aa,cc=thresholds(bb);vv=gamevalue(aa,bb,cc)
    intervals={name:I(*map(F,obj[name+'_interval'])) for name in ['A','C','value']}
    assert aa.inside(intervals['A']) and cc.inside(intervals['C']) and vv.inside(intervals['value'])
    assert 0<aa.lo and aa.hi<cc.lo and cc.hi<bb.lo and bb.hi<1
    for name,element in [('A',A),('C',C),('value',vb)]:
        coeff=list(map(F,obj[name+'_polynomial_ascending']))
        z=K(0)
        for c in reversed(coeff):z=z*element+c
        assert z==0
        box=intervals[name];assert count(coeff,box.lo,box.hi)==1
    # Polynomial identities in own hand x, with coefficients in the quotient.
    # Independent from root evaluation; each displayed factorization is exact.
    low=[5*C*C-2,K(0),K(-3)]
    assert low==[3*A*A,K(0),K(-3)]
    high=[K(-2),-4*C,K(6)]
    factor=[-2*B*(3*B-2*C),-4*C,K(6)]
    assert high==factor
    T=A+1-B
    actual=[[-2*T,7*C],[7*C*A-2*T],[-2*C*A-2*T,9*A],
            [-2*C*(A-B)-2*T,9*(A-B)-2*C,K(9)]]
    reduced=[[-7*C*A,7*C],[K(0)],[-9*A*C,9*A],
             [-9*A*C+2*B*C,9*A-9*B-2*C,K(9)]]
    assert actual==reduced
    # All signs follow from 0<A<C<B<1 and the factor forms:
    # I low:3(A-x)(A+x); high:2(x-B)(3(x+B)-2C).
    # Callers:7C(x-A),0,9A(x-C),9A(x-C)+(x-B)(9x-2C).
    assert 7*cc.lo>0 and 9*aa.lo>0 and 3*(cc.lo+bb.lo)-2*cc.hi>0 and 9*bb.lo-2*cc.hi>0
    printed=F('0.122557074714865');halfunit=F(1,2*10**15)
    matches=vv.inside(I(printed-halfunit,printed+halfunit))
    disjoint=vv.hi<printed-halfunit or vv.lo>printed+halfunit
    assert disjoint
    return dict(exact_equations=True,isolated_roots=True,ordered_thresholds=True,
      payoff_factorizations=True,all_measurable_deviations='nonprofitable by pointwise maximization',
      A=[decimal(aa.lo),decimal(aa.hi)],B=[decimal(bb.lo),decimal(bb.hi)],C=[decimal(cc.lo),decimal(cc.hi)],
      value=[decimal(vv.lo),decimal(vv.hi)],published_value=str(printed),
      printed_15_decimal_match=matches,printed_rounding_interval_disjoint=disjoint,
      value_minus_printed=[decimal(vv.lo-printed),decimal(vv.hi-printed)])

if __name__=='__main__':
    path=Path(sys.argv[1])
    result=check(json.loads(path.read_text()));print(json.dumps(result,indent=2))
    print('PASS: exact b=2 equilibrium certificate; printed decimal criterion is FALSE')
