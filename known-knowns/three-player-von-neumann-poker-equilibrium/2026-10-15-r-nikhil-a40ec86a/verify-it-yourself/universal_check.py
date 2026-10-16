"""Portable exact polynomial proof checker; standard library only, no eval.
The analytic IVT/monotonicity argument remains explicitly stated in ALL_B_PROOF.md.
"""
from fractions import Fraction as F
import ast,json,sys
from pathlib import Path
NAMES=('A','B','C','b','x','y','c0','s','c','B1','B2','D1','D2')
ZERO=(0,)*len(NAMES)
class Poly:
 def __init__(self,d):self.d={m:F(v) for m,v in d.items() if v}
 @staticmethod
 def const(x):return Poly({ZERO:F(x)})
 def __add__(self,o):
  d=dict(self.d)
  for m,v in o.d.items():d[m]=d.get(m,F(0))+v
  return Poly(d)
 def __neg__(self):return Poly({m:-v for m,v in self.d.items()})
 def __sub__(self,o):return self+-o
 def __mul__(self,o):
  d={}
  for a,v in self.d.items():
   for b,w in o.d.items():
    m=tuple(x+y for x,y in zip(a,b));d[m]=d.get(m,F(0))+v*w
  return Poly(d)
 def __pow__(self,n):
  assert type(n) is int and 0<=n<=12
  p=Poly.const(1)
  for _ in range(n):p=p*self
  return p
 def __eq__(self,o):return self.d==o.d

def parse(text):
 def walk(n):
  if isinstance(n,ast.Constant):
   assert type(n.value) is int
   return Poly.const(n.value)
  if isinstance(n,ast.Name):
   assert n.id in NAMES
   m=list(ZERO);m[NAMES.index(n.id)]=1;return Poly({tuple(m):1})
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -walk(n.operand)
  if isinstance(n,ast.BinOp):
   l=walk(n.left)
   if isinstance(n.op,ast.Pow):
    assert isinstance(n.right,ast.Constant);return l**n.right.value
   r=walk(n.right)
   if isinstance(n.op,ast.Add):return l+r
   if isinstance(n.op,ast.Sub):return l-r
   if isinstance(n.op,ast.Mult):return l*r
   if isinstance(n.op,ast.Div):
    assert set(r.d)=={ZERO};return l*Poly.const(1/r.d[ZERO])
  raise ValueError('unsupported polynomial syntax')
 return walk(ast.parse(text,mode='eval').body)

# Raw action differences are defined from net terminal-pot utilities.
E=['3*A**2-(b+3)*C**2+b','3*B**2-2*C*B-1','(2*b+3)*C*A-b*(A+1-B)']
RAW={
'I_low':'(b+3)*C**2-b-3*x**2',
'I_high':'b*(3*x**2-2*C*x-1)',
'caller_0_A':'y*(2*b+3)*C-b*(A+1-B)',
'caller_A_C':'A*(2*b+3)*C-b*(A+1-B)',
'caller_C_B':'A*((2*b+3)*C+3*(b+1)*(y-C))-b*(A+1-B)',
'caller_B_1':'(A+y-B)*((2*b+3)*C+3*(b+1)*(y-C))-b*(A+1-B)',
'A_less_C':'A**2-C**2',
'value':'-A**3+(b+3)*A*C**2-b*A-b*B**3+b*B**2*C+b*B-b*C'}
FACTORS={
'I_low':'3*(A-x)*(A+x)',
'I_high':'b*(x-B)*(3*(x+B)-2*C)',
'caller_0_A':'(2*b+3)*C*(y-A)',
'caller_A_C':'0',
'caller_C_B':'3*(b+1)*A*(y-C)',
'caller_B_1':'3*(b+1)*A*(y-C)+(y-B)*(3*(b+1)*y-b*C)',
'A_less_C':'b*(C**2-1)/3',
'value':'2*A**3+b*(B-C)*(1-B**2)'}
MULTIPLIERS={'I_low':['-1','0','0'],'I_high':['0','b','0'],
 'caller_0_A':['0','0','1'],'caller_A_C':['0','0','1'],
 'caller_C_B':['0','0','1'],'caller_B_1':['0','0','1'],
 'A_less_C':['1/3','0','0'],'value':['-A','0','0']}

def verify(obj):
 assert obj['target']=='three-player-von-neumann-poker-equilibrium'
 assert obj['bet_domain']=='all real b > 0'
 assert obj['equations']==E and set(obj['identities'])==set(RAW)
 for k,raw in RAW.items():
  item=obj['identities'][k]
  assert item['factor']==FACTORS[k]
  assert len(item['multipliers'])==3
  residual=parse(raw)-parse(item['factor'])
  rhs=Poly.const(0)
  for m,e in zip(item['multipliers'],E):rhs=rhs+parse(m)*parse(e)
  assert residual==rhs,k
 extras={
 'left_denominator_margin':'(b+3)*((2*b+3)**2*c0**2-b**2)-3*b*(b**2+3*b+3)-(2*b+3)**2*((b+3)*c0**2-b)',
 'B_upper_root_margin':'(3-c)**2-(c**2+3)-6*(1-c)',
 'B_lower_root_margin':'(c**2+3)-(2*c)**2-3*(1-c**2)',
 'B_quadratic':'3*(3*B**2-2*c*B-1)-((3*B-c)**2-c**2-3)',
 'ratio_monotonicity':'(1-B1)*D2-(1-B2)*D1-((B2-B1)*D1+(1-B1)*(D2-D1))'}
 assert obj['existence_identities']==extras
 for k,e in extras.items():assert parse(e)==Poly.const(0),k
 return {'action_and_value_identities':len(RAW),'existence_identities':len(extras),'arithmetic':'exact rational polynomial coefficients','analytic_argument':'IVT and strict monotonicity in the accompanying proof; not a formal proof assistant'}

def make():
 obj={'target':'three-player-von-neumann-poker-equilibrium','bet_domain':'all real b > 0','equations':E,
 'identities':{k:{'factor':FACTORS[k],'multipliers':MULTIPLIERS[k]} for k in RAW},
 'existence_identities':{
 'left_denominator_margin':'(b+3)*((2*b+3)**2*c0**2-b**2)-3*b*(b**2+3*b+3)-(2*b+3)**2*((b+3)*c0**2-b)',
 'B_upper_root_margin':'(3-c)**2-(c**2+3)-6*(1-c)',
 'B_lower_root_margin':'(c**2+3)-(2*c)**2-3*(1-c**2)',
 'B_quadratic':'3*(3*B**2-2*c*B-1)-((3*B-c)**2-c**2-3)',
 'ratio_monotonicity':'(1-B1)*D2-(1-B2)*D1-((B2-B1)*D1+(1-B1)*(D2-D1))'}}
 verify(obj);return obj
if __name__=='__main__':
 if sys.argv[1]=='--make':
  Path(sys.argv[2]).write_text(json.dumps(make(),indent=2)+'\n')
 else:
  print(json.dumps(verify(json.loads(Path(sys.argv[1]).read_text())),indent=2));print('PASS: universal exact polynomial certificate')
