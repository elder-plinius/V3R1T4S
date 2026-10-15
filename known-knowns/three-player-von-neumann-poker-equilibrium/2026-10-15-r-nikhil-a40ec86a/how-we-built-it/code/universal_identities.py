"""Exact symbolic ledger for the all-positive-b proof; no sample establishes it."""
import sympy as s
import json
b,C,B,A,y,x=s.symbols('b C B A y x')
E1=3*A*A-(b+3)*C*C+b
E2=3*B*B-2*C*B-1
E3=(2*b+3)*C*A-b*(A+1-B)
G=s.groebner([E1,E2,E3],A,B,C,x,y,b,domain=s.QQ)
checks={}
def same(name,p,q):
    rem=s.expand(p-q)
    assert G.reduce(rem)[1]==0,(name,rem)
    checks[name]=True
# Existence: certify the only nontrivial endpoint denominator inequality.
r=b/(b+3)
margin=s.factor((2*b+3)**2*r-b*b)
assert margin==3*b*(b*b+3*b+3)/(b+3)
checks['denominator_at_C0_positive_after_squaring']=str(margin)
# Positive denominator and numerator derivative signs make g strictly decreasing.
same('A_less_C_by_EqA',A*A-C*C,b*(C*C-1)/3)
same('I_low',(b+3)*C*C-b-3*x*x,3*(A-x)*(A+x))
same('I_high',b*(3*x*x-2*C*x-1),b*(x-B)*(3*(x+B)-2*C))
T=A+1-B
for label,W,R,factor in [
    ('caller_0_A',y,0,(2*b+3)*C*(y-A)),
    ('caller_A_C',A,0,0),
    ('caller_C_B',A,y-C,3*(b+1)*A*(y-C)),
    ('caller_B_1',A+y-B,y-C,3*(b+1)*A*(y-C)+(y-B)*(3*(b+1)*y-b*C))]:
    same(label,W*((2*b+3)*C+3*(b+1)*R)-b*T,factor)
v=-A**3+(b+3)*A*C*C-b*A-b*B**3+b*B*B*C+b*B-b*C
same('value_simplification',v,2*A**3+b*(B-C)*(1-B*B))
# Endpoint continuity of raw polynomials.
lo=(b+3)*C*C-b-3*x*x;hi=b*(3*x*x-2*C*x-1)
assert s.expand((lo-hi).subs(x,C))==0
checks['I_continuous_at_C']=True
# Derivative B'(C)=(1+C/sqrt(C²+3))/3 >0 uses only C>=0.
# B(1)=1; B(C)>C follows sqrt(C²+3)>2C for C<1.
assert s.expand(C*C+3-4*C*C)==3*(1-C*C)
checks['B_greater_C_squared_margin']='3*(1-C^2)'
# The low boundary at C0 has A=0; at C=1 A=1.
assert s.simplify(((b+3)*r-b)/3)==0
assert s.simplify(((b+3)-b)/3)==1
checks['sqrt_A_endpoints']=[0,1]
print(json.dumps(checks,indent=2))
print('PASS: exact symbolic identities for all b; analytic positivity proof in ALL_B_PROOF.md')
