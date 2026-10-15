"""Exact, definition-based conditional completeness checker, standard library."""
if not __debug__:raise RuntimeError('Do not disable proof assertions')
from pathlib import Path
import sys,json,time
from fractions import Fraction as Q
from itertools import permutations
import verify_normalization as norm
F=norm.full;R=norm.reduced

def require(facts,p,rel):
 assert any(v==p and rr==rel for v,rr in facts.values()),'missing required family fact'

def leaves(deal,vs):
 a,b,c=deal
 pcall=[[vs[n] for n in row] for row in [['a12','d','h','a42'],['a13','f','t','a43'],['a14','a24','j','a44']]]
 bet=[vs[n] for n in ['r','s','k','q']];cf=[vs[n] for n in ['b13','y','z','b43']];cc=[vs[n] for n in ['b14','b24','e','b44']]
 lastbet=[vs[n] for n in ['u','v','l','A']];lastcall=[vs[n] for n in ['c12','n','w','c42']]
 x,y,z=pcall[0][a],pcall[1][a],pcall[2][a];b0=bet[b];bf=cf[b];bc=cc[b];c0=lastbet[c];c1=lastcall[c]
 return {'BFF':F.Poly(),'BFC':F.Poly(),'BCF':F.Poly(),'BCC':F.Poly(),
 'KKK':(1-b0)*(1-c0),'KBFF':(1-y)*b0*(1-c1),'KBFC':y*b0*(1-c1),'KBCF':(1-z)*b0*c1,'KBCC':z*b0*c1,
 'KKBFF':(1-x)*(1-b0-bf)*c0,'KKBFC':(1-x)*bf*c0,'KKBCF':x*(1-b0-bc)*c0,'KKBCC':x*bc*c0}

def verify(pre,dom,red,terminal):
 start=time.time();normal=norm.verify(pre,dom,red)
 facts,pc,closed=F.check(pre['events']);assert not closed
 rf,rc,closed=R.check(red['events']);assert not closed
 for key,(p,rel) in rf.items():facts['reduced_'+key]=(norm.lift(p),rel)
 d=F.D;u,v,r,s,y,z,q,w,t,j=[d[n] for n in ['u','v','r','s','y','z','q','w','t','j']];beta=2*r*u+2*s*v
 common=[(2*z+2*y-1-r-s-beta,'eq'),(beta-s-2*y,'ge'),(2-r-u*(3+2*r+2*s),'ge'),(u*(r-s),'ge'),(v*(s-r),'ge'),(y*v,'eq')]
 for p,rel in common:require(facts,p,rel)
 for n in ['r','s']:require(facts,Q(1,4)-d[n],'ge')
 require(facts,u+v-Q(1,2),'eq');require(facts,q-2*(r+s),'eq')
 # Probability conversion y/(1-s) is valid, since s<=1/4.
 # Fixed b32=1/2,c33=c34=0 satisfy the unused opening-response ranges
 # because the remaining Table-3 width (3(r+s)+beta)/4 is nonnegative.
 assert terminal['variables']==F.N
 facts,tc,closed=F.check(terminal['events'],facts);assert not closed
 cases=terminal['cases'];assert set(cases)=={'zero','half','interior_outer','interior_inner'}
 zero,zc,zclosed=F.check(cases['zero'],facts,u,'eq');assert not zclosed
 require(zero,s-r,'ge');require(zero,y,'eq')
 half,hc,hclosed=F.check(cases['half'],facts,v,'eq');assert not hclosed
 require(half,r-s,'ge');require(half,Q(1,2)-2*r-s,'ge');require(half,r-s-2*y,'ge')
 outer,oc,oclosed=F.check(cases['interior_outer'],facts,u,'gt');assert not oclosed
 inner,ic,iclosed=F.check(cases['interior_inner'],outer,v,'gt');assert not iclosed
 require(inner,r-s,'eq');require(inner,y,'eq')
 # Exhaustive case cover: u,v>=0 and u+v=1/2 imply u=0, v=0,
 # or u>0 and v>0. These are the literal three family subcases.
 defaults={'a12':0,'a13':0,'a14':0,'a24':0,'a42':1,'a43':1,'a44':1,'b13':0,'b14':0,'b24':0,'b43':1-q,'b44':1-q,'c12':0,'c42':1,
 'd':0,'f':0,'h':0,'j':0,'e':0,'k':0,'l':0,'n':0,'A':1,'t':Q(1,2),'w':0}
 canonical={n:F.Poly(defaults[n]) if n in defaults else d[n] for n in F.N}
 expected={(deal,history) for deal in permutations(range(4),3) for history in leaves(deal,d)}
 seen=set()
 for row in terminal['terminals']:
  deal=tuple(row['deal']);history=row['history'];key=(deal,history);assert key in expected and key not in seen;seen.add(key)
  actual=leaves(deal,d)[history];standard=leaves(deal,canonical)[history]
  equality=F.Poly()
  for fact,mult in row['equalities']:
   p,rel=facts[fact];assert rel=='eq';equality+=p*F.decode(mult)
  assert equality==actual-standard,('terminal mismatch',deal,history)
 assert seen==expected,'missing terminal-history record'
 return {'normalization':normal,'family_range_events':zc+hc+oc+ic,'terminal_events':tc,'terminal_records':len(seen),
 'conclusion':'every full32 no-opening Nash equilibrium induces the same terminal-history distribution as a literal Tables 2-3 family member',
 'scope':'conditional on no initial P1 betting; not a full-game bank win','seconds':time.time()-start}

if __name__=='__main__':
 out=norm.ROOT/'attempts/solver/output';names=['normalization_preconditions.json','normalization_dominance.json','restricted_family_certificate.json','terminal_family_certificate.json']
 paths=[out/n for n in names] if len(sys.argv)==1 else [Path(p) for p in sys.argv[1:]];assert len(paths)==4
 result=verify(*(json.loads(p.read_text()) for p in paths));print(json.dumps(result,indent=2));print('CONDITIONAL_FAMILY: PASS')
