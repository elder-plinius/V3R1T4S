"""Independent, standard-library rational polynomial proof kernel.
No generator, symbolic library, SMT solver, or prover code is imported.
The no-opening game is independently enumerated directly below.
"""
if not __debug__:
 raise RuntimeError('Proof checking requires assertions; do not use python -O')
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import json,sys,time
N='d f h t j r s k q y z e u v l A n w'.split();DIM=len(N);Z=(0,)*DIM
class Poly:
 def __init__(self,x=0):
  if isinstance(x,Poly):self.c=dict(x.c)
  elif isinstance(x,dict):self.c={m:Q(c) for m,c in x.items() if c}
  else:self.c={Z:Q(x)} if x else {}
 def __add__(self,b):
  c=dict(self.c)
  for m,v in Poly(b).c.items():c[m]=c.get(m,Q(0))+v
  return Poly(c)
 __radd__=__add__
 def __neg__(self):return Poly({m:-c for m,c in self.c.items()})
 def __sub__(self,b):return self+-Poly(b)
 def __rsub__(self,b):return Poly(b)+-self
 def __mul__(self,b):
  c={}
  for m,u in self.c.items():
   for n,v in Poly(b).c.items():
    k=tuple(a+b for a,b in zip(m,n));c[k]=c.get(k,Q(0))+u*v
  return Poly(c)
 __rmul__=__mul__
 def __eq__(self,b):return self.c==Poly(b).c
 def diff(self,i):
  c={}
  for m,v in self.c.items():
   if m[i]:n=list(m);n[i]-=1;c[tuple(n)]=v*m[i]
  return Poly(c)
 def value(self,values):
  ans=Q(0)
  for m,c in self.c.items():
   for i,power in enumerate(m):c*=values[i]**power
   ans+=c
  return ans

def variable(i):m=[0]*DIM;m[i]=1;return Poly({tuple(m):Q(1)})
D={n:variable(i) for i,n in enumerate(N)}
def decode(rows):
 assert isinstance(rows,list);out={}
 for mon,co in rows:
  assert len(mon)==DIM and all(isinstance(x,int) and 0<=x<=20 for x in mon)
  mon=tuple(mon);assert mon not in out;out[mon]=Q(co)
 return Poly(out)

def game():
 d,f,h,t,j,r,s,k,q,y,z,e,u,v,l,A,n,w=[D[a] for a in N]
 pc=[[0,d,h,1],[0,f,t,1],[0,0,j,1]]
 pb=[r,s,k,q];pfc=[0,y,z,1-q];pcc=[0,0,e,1-q]
 tb=[u,v,l,A];tc=[0,n,w,1]
 # Each entry supplies contributions, active seats and one realization factor
 # per player. Every no-opening terminal outcome appears once.
 out=[Poly(),Poly(),Poly()]
 for a,b,c in permutations(range(4),3):
  aa,ab,ac=pc[0][a],pc[1][a],pc[2][a];bb=pb[b];bf=pfc[b];bc=pcc[b];cb=tb[c];cc=tc[c]
  leaves=[
   ([1,1,1],[0,1,2],Poly(1)*(1-bb)*(1-cb)),
   ([1,2,1],[1],(1-ab)*bb*(1-cc)),
   ([2,2,1],[0,1],ab*bb*(1-cc)),
   ([1,2,2],[1,2],(1-ac)*bb*cc),
   ([2,2,2],[0,1,2],ac*bb*cc),
   ([1,1,2],[2],(1-aa)*(1-bb-bf)*cb),
   ([1,2,2],[1,2],(1-aa)*bf*cb),
   ([2,1,2],[0,2],aa*(1-bb-bc)*cb),
   ([2,2,2],[0,1,2],aa*bc*cb)]
  assert sum(mass for _,_,mass in leaves)==1
  cards=[a,b,c]
  for costs,active,mass in leaves:
   winner=max(active,key=lambda i:cards[i]);pot=sum(costs)
   for i in range(3):out[i]+=mass*((pot if i==winner else 0)-costs[i])
 assert sum(out)==0
 owners=[0]*5+[1]*7+[2]*6
 grad={n:out[p].diff(i) for i,(n,p) in enumerate(zip(N,owners))}
 for i,n in enumerate(N):
  for m in grad[n].c:assert all(not m[j] for j in range(DIM) if owners[j]==owners[i])
 return out,grad
U,G=game()

def signexpr(node,facts):
 kind=node[0]
 if kind=='const':
  c=Q(node[1]);assert c>=0;return Poly(c),c>0
 if kind=='square':
  p=decode(node[1]);return p*p,False
 if kind=='ref':
  p,rel=facts[node[1]];assert rel in ['ge','gt'];return p,rel=='gt'
 assert kind in ['add','mul'] and len(node)==3
 a,sa=signexpr(node[1],facts);b,sb=signexpr(node[2],facts)
 return (a+b,sa or sb) if kind=='add' else (a*b,sa and sb)

def has_eq(facts,p):return any(rel=='eq' and (v==p or v==-p) for v,rel in facts.values())
def check(events,inherited=None,assumption=None,assumerel='gt'):
 facts=dict(inherited or {});count=0;closed=False
 for index,event in enumerate(events):
  rule=event['rule'];count+=1
  if rule=='contradiction':
   p,rel=facts[event['fact']];assert p==0 and rel=='gt';assert index==len(events)-1;closed=True;continue
  ident=event['id'];assert ident not in facts;p=decode(event['poly']);rel=event['rel'];assert rel in ['ge','gt','eq','ne']
  if rule=='assume':assert assumption is not None and index==0 and p==assumption and rel==assumerel
  elif rule=='domain':
   assert inherited is None and rel=='ge'
   name=event['name']
   if name=='polytope':assert any(p==a for a in [1-D['s']-D['y'],1-D['k']-D['z'],1-D['k']-D['e']])
   else:assert p==(D[name] if event['side']=='lo' else 1-D[name])
  elif rule=='derive':
   total,strict=signexpr(event['positive'],facts)
   for key,mult in event['equalities']:
    eq,eqrel=facts[key];assert eqrel=='eq';total+=eq*decode(mult)
   assert total==p,('identity mismatch',ident);assert rel==('gt' if strict else 'ge')
  elif rule=='antisymmetry':
   a,ar=facts[event['a']];b,br=facts[event['b']];assert ar in ['ge','gt'] and br in ['ge','gt'];assert a==p and b==-p and rel=='eq'
  elif rule=='refute':
   ap=decode(event['assumption']);ar=event.get('assumerel','gt');assert ar in ['gt','eq'];child,cc,cl=check(event['events'],facts,ap,ar);count+=cc;assert cl;assert (p==-ap and rel=='ge') if ar=='gt' else (p==ap and rel=='ne')
  elif rule=='divsign':
   product,pr=facts[event['product']];factor,fr=facts[event['factor']];assert pr in ['ge','gt'] and ((fr=='gt') or (fr=='ge' and pr=='gt'));assert p*factor==product and rel==pr
  elif rule=='zero_product':
   product,pr=facts[event['equation']];factor,fr=facts[event['factor']];assert fr=='gt' and pr=='eq';assert p*factor==product and rel=='eq'
  elif rule=='strictify':
   nonneg,nr=facts[event['nonnegative']];nonzero,zr=facts[event['nonzero']];assert nr in ['ge','gt'] and zr=='ne' and nonneg==p and (nonzero==p or nonzero==-p) and rel=='gt'
  elif rule=='triangle_vertex':
   name=event['name'];assert name in ['s','y'];assert p==D['s']*G['s']+D['y']*G['y']-G[name] and rel=='ge'
  elif rule=='triangle_slack':
   name=event['name'];assert name in ['s','y'];pr,rr=facts[event['premise']];assert pr==1-D['s']-D['y'] and rr=='gt';assert p==-G[name] and rel=='ge'
  elif rule=='kkt_product':
   name=event['name'];assert name in N;assert p==D[name]*G[name] and rel=='ge'
  elif rule=='kkt':
   name=event['name'];v=D[name];g=G[name];prem,sr=facts[event['premise']];mode=event['mode']
   if mode=='low':assert prem==-g and sr=='gt' and p==v and rel=='eq'
   elif mode=='high':
    assert prem==g and sr=='gt' and p==v-1 and rel=='eq'
    if name in ['s','y']:assert has_eq(facts,D['y' if name=='s' else 's'])
    if name in ['z','e']:assert has_eq(facts,D['k'])
    assert name!='k'
   elif mode=='grad_ge':assert prem==v and sr=='gt' and p==g and rel=='ge'
   elif mode=='grad_le':
    assert prem==1-v and sr=='gt' and p==-g and rel=='ge'
    assert name not in ['s','y','k']
    if name in ['z','e']:assert has_eq(facts,D['k'])
   elif mode=='pyramid':assert name=='k' and prem==v and sr=='gt' and p==g-G['z']-G['e'] and rel=='ge'
   elif mode=='triangle_s':assert name in ['s','y'] and event['other'] in ['s','y'];assert prem==v and sr=='gt' and p==g-G[event['other']] and rel=='ge'
   else:raise AssertionError(mode)
  else:raise AssertionError(rule)
  facts[ident]=(p,rel)
 return facts,count,closed

def verify_document(obj):
 start=time.time();assert obj['variables']==N
 facts,count,closed=check(obj['events']);assert not closed
 goals=[(2*D['q']-3*(D['r']+D['s']),'ge')]+[(D[n],'eq') for n in ['k','l','n','f','d','h','e']]+[(D['A']-1,'eq'),(D['t']+D['w']-Q(1,2),'eq'),(D['u']+D['v']-Q(1,2),'eq'),(D['q']-2*(D['r']+D['s']),'eq'),(D['j']*(D['r']+D['s']),'eq'),(2*U[1]+1,'eq')]
 beta=2*D['r']*D['u']+2*D['s']*D['v']
 goals += [(D['w']*(D['r']+D['s']),'eq'),(beta,'ge'),(Q(1,4)-beta,'ge'),(beta-D['r'],'ge'),(beta-D['s'],'ge'),((beta-D['r'])*(beta-D['s']),'eq'),(2*U[0]+1+2*beta,'eq'),(U[2]-1-beta,'eq')]
 for target,rel in goals:assert any(v==target and rr==rel for v,rr in facts.values()),'missing required conclusion'
 return {'scope':'18-variable no-opening game with Table-2 fixed globally','events_checked':count,'root_facts':len(facts),'conclusions':['3(r+s)<=2q','k=l=n=f=d=h=e=0','A=1','t+w=u+v=1/2','q=2(r+s)','j(r+s)=0','P2 payoff=-1/48','beta=max(r,s) in [0,1/4]','full payoff vector matches family'],'seconds':time.time()-start}
if __name__=='__main__':
 print(json.dumps(verify_document(json.loads(Path(sys.argv[1]).read_text()))));print('RATIONAL_REDUCTION_CERTIFICATE: PASS')
