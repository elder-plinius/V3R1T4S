"""Independent, standard-library rational polynomial proof kernel.
No generator, symbolic library, SMT solver, or prover code is imported.
The full game is independently enumerated directly below.
"""
if not __debug__:
 raise RuntimeError('Proof checking requires assertions; do not use python -O')
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import json,sys,time
N='a12 a13 a14 d f a24 h t j a42 a43 a44 r b13 b14 s y b24 k z e q b43 b44 u c12 v n l w A c42 a b c C BJ BQ BK BA CJ CQ CK CA DJ DQ DK DA'.split();DIM=len(N);Z=(0,)*DIM
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
 pa=[D[n] for n in ['a','b','c','C']]
 pc=[[D[n] for n in row] for row in [['a12','d','h','a42'],['a13','f','t','a43'],['a14','a24','j','a44']]]
 pb=[D[n] for n in ['r','s','k','q']];bfirst=[D[n] for n in ['BJ','BQ','BK','BA']]
 bf=[D[n] for n in ['b13','y','z','b43']];bc=[D[n] for n in ['b14','b24','e','b44']]
 cb=[D[n] for n in ['u','v','l','A']];cc=[D[n] for n in ['c12','n','w','c42']]
 cf=[D[n] for n in ['CJ','CQ','CK','CA']];ct=[D[n] for n in ['DJ','DQ','DK','DA']]
 out=[Poly(),Poly(),Poly()]
 for a,b,c in permutations(range(4),3):
  ab=pa[a];a0,a1,a2=[row[a] for row in pc];bb=pb[b];bb0=bfirst[b];cb0=cb[c];cb1=cc[c]
  leaves=[
   ([2,1,1],[0],ab*(1-bb0)*(1-cf[c])),
   ([2,1,2],[0,2],ab*(1-bb0)*cf[c]),
   ([2,2,1],[0,1],ab*bb0*(1-ct[c])),
   ([2,2,2],[0,1,2],ab*bb0*ct[c]),
   ([1,1,1],[0,1,2],(1-ab)*(1-bb)*(1-cb0)),
   ([1,2,1],[1],(1-ab-a1)*bb*(1-cb1)),
   ([2,2,1],[0,1],a1*bb*(1-cb1)),
   ([1,2,2],[1,2],(1-ab-a2)*bb*cb1),
   ([2,2,2],[0,1,2],a2*bb*cb1),
   ([1,1,2],[2],(1-ab-a0)*(1-bb-bf[b])*cb0),
   ([1,2,2],[1,2],(1-ab-a0)*bf[b]*cb0),
   ([2,1,2],[0,2],a0*(1-bb-bc[b])*cb0),
   ([2,2,2],[0,1,2],a0*bc[b]*cb0)]
  assert sum(m for _,_,m in leaves)==1
  cards=[a,b,c]
  for costs,active,mass in leaves:
   winner=max(active,key=lambda i:cards[i]);pot=sum(costs)
   for i in range(3):out[i]+=mass*((pot if i==winner else 0)-costs[i])
 assert sum(out)==0
 owners=[0]*12+[1]*12+[2]*8+[0]*4+[1]*4+[2]*8
 grad={n:out[p].diff(i) for i,(n,p) in enumerate(zip(N,owners))}
 for i,n in enumerate(N):
  for mon in grad[n].c:assert all(not mon[j] for j in range(DIM) if owners[j]==owners[i])
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
   if name=='polytope':assert any(p==a for a in [1-D[bet]-D[call] for bet,calls in [('a',['a12','a13','a14']),('b',['d','f','a24']),('c',['h','t','j']),('C',['a42','a43','a44']),('r',['b13','b14']),('s',['y','b24']),('k',['z','e']),('q',['b43','b44'])] for call in calls])
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
  elif rule=='kkt_product':
   name=event['name'];assert name in N;assert p==D[name]*G[name] and rel=='ge'
  elif rule=='pyramid_vertex_bet':
   groups={'a':['a12','a13','a14'],'b':['d','f','a24'],'c':['h','t','j'],'C':['a42','a43','a44'],'r':['b13','b14'],'s':['y','b24'],'k':['z','e'],'q':['b43','b44']}
   name=event['name'];assert event['calls']==groups[name]
   assert p==(D[name]-1)*G[name]+sum(D[c]*G[c] for c in groups[name]) and rel=='ge'
  elif rule=='pyramid_bet_vertex':
   groups={'a':['a12','a13','a14'],'b':['d','f','a24'],'c':['h','t','j'],'C':['a42','a43','a44'],'r':['b13','b14'],'s':['y','b24'],'k':['z','e'],'q':['b43','b44']}
   name=event['name'];calls=event['calls'];assert name in groups and len(set(calls))==len(calls) and set(calls)<=set(groups[name])
   premise,rr=facts[event['premise']];assert premise==D[name] and rr=='gt'
   assert p==G[name]-sum(G[n] for n in calls) and rel=='ge'
  elif rule=='pyramid_bet_compare':
   name=event['name'];groups={'a':['a12','a13','a14'],'b':['d','f','a24'],'c':['h','t','j'],'C':['a42','a43','a44'],'r':['b13','b14'],'s':['y','b24'],'k':['z','e'],'q':['b43','b44']};assert event['calls']==groups[name]
   pr,sr=facts[event['premise']];assert pr==1-D[name] and sr=='gt';assert len(event['nonnegative'])==len(groups[name])
   for call,key in zip(event['calls'],event['nonnegative']):
    gg,rr=facts[key];assert gg==G[call] and rr in ['ge','gt']
   assert p==sum(G[c] for c in event['calls'])-G[name] and rel=='ge'
  elif rule=='pyramid_bet_gradle':
   name=event['name'];groups={'a':['a12','a13','a14'],'b':['d','f','a24'],'c':['h','t','j'],'C':['a42','a43','a44'],'r':['b13','b14'],'s':['y','b24'],'k':['z','e'],'q':['b43','b44']};assert event['calls']==groups[name]
   pr,sr=facts[event['premise']];assert pr==1-D[name] and sr=='gt'
   assert len(event['nonpositive'])==len(groups[name])
   for call,key in zip(event['calls'],event['nonpositive']):
    gg,rr=facts[key];assert gg==-G[call] and rr in ['ge','gt']
   assert p==-G[name] and rel=='ge'
  elif rule in ['cap_high','cap_upperproduct','cap_gradle']:
   name,bet=event['name'],event['bet'];pairs={'a12':'a','a13':'a','a14':'a','d':'b','f':'b','a24':'b','h':'c','t':'c','j':'c','a42':'C','a43':'C','a44':'C','b13':'r','b14':'r','y':'s','b24':'s','z':'k','e':'k','b43':'q','b44':'q'};assert pairs.get(name)==bet
   if rule=='cap_high':
    pr,sr=facts[event['premise']];assert pr==G[name] and sr=='gt' and p==D[name]+D[bet]-1 and rel=='eq'
   elif rule=='cap_gradle':
    pr,sr=facts[event['premise']];assert pr==1-D[bet]-D[name] and sr=='gt' and p==-G[name] and rel=='ge'
   else:assert p==-(1-D[bet]-D[name])*G[name] and rel=='ge'
  elif rule=='kkt_upperproduct':
   name=event['name'];assert name not in ['a','b','c','C','a12','a13','a14','d','f','a24','h','t','j','a42','a43','a44','r','s','k','q','b13','b14','y','b24','z','e','b43','b44'];assert p==-(1-D[name])*G[name] and rel=='ge'
  elif rule=='kkt':
   name=event['name'];v=D[name];g=G[name];prem,sr=facts[event['premise']];mode=event['mode']
   if mode=='low':assert prem==-g and sr=='gt' and p==v and rel=='eq'
   elif mode=='high':
    assert prem==g and sr=='gt' and p==v-1 and rel=='eq'
    assert name not in ['a','b','c','C','a12','a13','a14','d','f','a24','h','t','j','a42','a43','a44','r','s','k','q','b13','b14','y','b24','z','e','b43','b44']
   elif mode=='grad_ge':assert prem==v and sr=='gt' and p==g and rel=='ge'
   elif mode=='grad_le':
    assert prem==1-v and sr=='gt' and p==-g and rel=='ge'
    assert name not in ['a','b','c','C','a12','a13','a14','d','f','a24','h','t','j','a42','a43','a44','r','s','k','q','b13','b14','y','b24','z','e','b43','b44']
   elif mode=='pyramid':assert name=='k' and prem==v and sr=='gt' and p==g-G['z']-G['e'] and rel=='ge'
   else:raise AssertionError(mode)
  else:raise AssertionError(rule)
  facts[ident]=(p,rel)
 return facts,count,closed

def verify_document(obj):
 assert obj['variables']==N
 facts,count,closed=check(obj['events']);assert not closed
 return {'scope':'full 48-coordinate game','events_checked':count,'facts':len(facts)}
if __name__=='__main__':
 obj=json.loads(Path(sys.argv[1]).read_text());print(json.dumps(verify_document(obj)));print('FULL_GAME_CERTIFICATE: PASS')
