import ast,json,copy,sys
from fractions import Fraction
VARS=('n','d','a','b','k','l','u','t','h','z');D=len(VARS);ZERO=(0,)*D
REQ_IDENTITIES={'u_divisibility','v_divisibility','band_implies_linear_ratio'}
def const(x):return {} if not x else {ZERO:Fraction(x)}
def add(p,q):
 z=dict(p)
 for m,c in q.items():
  z[m]=z.get(m,0)+c
  if not z[m]:del z[m]
 return z
def neg(p):return {m:-c for m,c in p.items()}
def mul(p,q):
 z={}
 for x,a in p.items():
  for y,b in q.items():
   m=tuple(i+j for i,j in zip(x,y));z[m]=z.get(m,0)+a*b
 return {m:c for m,c in z.items() if c}
def power(p,n):
 assert isinstance(n,int) and 0<=n<=64
 z=const(1)
 while n:
  if n&1:z=mul(z,p)
  p=mul(p,p);n//=2
 return z
def parse(s,env):
 def walk(x):
  if isinstance(x,ast.Constant) and type(x.value) is int:return const(x.value)
  if isinstance(x,ast.Name):assert x.id in env;return env[x.id]
  if isinstance(x,ast.UnaryOp) and isinstance(x.op,ast.USub):return neg(walk(x.operand))
  if isinstance(x,ast.BinOp):
   if isinstance(x.op,ast.Add):return add(walk(x.left),walk(x.right))
   if isinstance(x.op,ast.Sub):return add(walk(x.left),neg(walk(x.right)))
   if isinstance(x.op,ast.Mult):return mul(walk(x.left),walk(x.right))
   if isinstance(x.op,ast.Pow):assert isinstance(x.right,ast.Constant);return power(walk(x.left),x.right.value)
  raise AssertionError('unsupported expression node')
 return walk(ast.parse(str(s),mode='eval').body)
def environment():
 e={}
 for i,v in enumerate(VARS):m=list(ZERO);m[i]=1;e[v]={tuple(m):Fraction(1)}
 return e
def verify(c):
 assert c['scope'] and c['limits']
 assert set(x['name'] for x in c['identities'])==REQ_IDENTITIES
 assert len(c['positivity'])==15
 for row in c['identities']:
  e=environment();assert not add(parse(row['lhs'],e),neg(parse(row['rhs'],e))),row['name']
 for row in c['positivity']:
  e=environment()
  for v,value in row['substitutions'].items():assert v in e;e[v]=parse(value,e)
  p=parse(row['expr'],e)
  assert all(z>=0 for z in p.values()),row['name']
  if row['strict']:assert p.get(ZERO,0)>0,row['name']
 return {'identities':len(c['identities']),'positivity_certificates':len(c['positivity'])}
c=json.load(open(sys.argv[1]));counts=verify(c)
mut=copy.deepcopy(c);mut['identities'][0]['rhs']+=' + 1'
try:verify(mut)
except AssertionError:pass
else:raise AssertionError('corrupt identity accepted')
mut=copy.deepcopy(c);mut['positivity'][0]['expr']='-1'
try:verify(mut)
except AssertionError:pass
else:raise AssertionError('corrupt positivity accepted')
print(json.dumps({'result':'PASS','counts':counts,'identity_mutant_rejected':True,'positivity_mutant_rejected':True,'scope':c['scope'],'limits':c['limits']}))
