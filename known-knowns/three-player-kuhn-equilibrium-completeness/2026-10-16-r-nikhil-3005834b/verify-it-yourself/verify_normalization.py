"""Independent exact verification of a no-opening normalization theorem.
Imports only separately implemented certificate checkers; no prover code.
"""
if not __debug__:raise RuntimeError('Do not disable proof assertions')
from pathlib import Path
import sys,json,time
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'checker'))
import verify_offpath_k as full
import verify_reduction as reduced

def substitute(p,mapping):
 out=full.Poly()
 for mon,co in p.c.items():
  term=full.Poly(co)
  for i,power in enumerate(mon):
   for _ in range(power):term*=mapping.get(full.N[i],full.D[full.N[i]])
  out+=term
 return out

def lift(p):
 out=full.Poly()
 for mon,co in p.c.items():
  term=full.Poly(co)
  for i,power in enumerate(mon):
   for _ in range(power):term*=full.D[reduced.N[i]]
  out+=term
 return out

def verify(precondition,dominance,restricted):
 started=time.time();assert precondition['variables']==full.N
 facts,count,closed=full.check(precondition['events']);assert not closed
 # All these preconditions are proved for the original no-opening game.
 base={'k':0,'l':0,'n':0,'a12':0,'A':1,'a42':1,'c12':0}
 for name,val in base.items():assert full.has_eq(facts,full.D[name]-val),('missing precondition',name)
 default={'a12':0,'a13':0,'a14':0,'a24':0,'a42':1,'a43':1,'a44':1,'b13':0,'b14':0,'b24':0,'b43':1-full.D['q'],'b44':1-full.D['q'],'c12':0,'c42':1}
 assert set(default).isdisjoint(reduced.N)
 assert set(default)|set(reduced.N)==set(full.N)
 owners={name:0 if i<12 else 1 if i<24 else 2 for i,name in enumerate(full.N)}
 # The map changes only the corresponding player's realization coordinates.
 # Each replacement is 0, 1, or 1-q in that same player's pyramid.
 for name,expr in default.items():
  for mon in full.Poly(expr).c:
   for i,e in enumerate(mon):
    if e:assert owners[full.N[i]]==owners[name]
 assert default['b43']==1-full.D['q'] and default['b44']==1-full.D['q']
 # Feasible reduced domains: P1/P3 intervals; P2 triangle (s,y),
 # pyramid (k,z,e), and intervals r,q. Their image is full-domain feasible.
 assert reduced.N=='d f h t j r s k q y z e u v l A n w'.split()
 for i in range(3):assert substitute(full.U[i],default)==lift(reduced.U[i]),'model mismatch'
 assert sum(full.U)==0 and sum(reduced.U)==0
 # Positivity certificates must use domains only, not equilibrium conditions
 # that could silently constrain a player's hypothetical deviation.
 assert dominance['variables']==full.N
 for event in dominance['events']:
  assert event['rule'] in ['domain','derive']
  if event['rule']=='derive':assert event['equalities']==[]
 df,dc,dcl=full.check(dominance['events']);assert not dcl
 assert len(dominance['goals'])==3
 for i,key in enumerate(dominance['goals']):
  own={name:val for name,val in default.items() if owners[name]==i}
  opponents={name:val for name,val in base.items() if owners[name]!=i}
  actual=substitute(substitute(full.U[i],own),opponents)
  normal=substitute(substitute(full.U[i],default),opponents)
  p,rel=df[key];assert p==actual-normal and rel in ['ge','gt'],'deviation dominance mismatch'
 # Generic zero-sum reduction, justified in NORMALIZATION_PROOF.md:
 # Nash => U_i(x)>=U_i(T_i x_i,x_-i)>=U_i(Tx). Sum_i U_i=0
 # forces equality. For every reduced deviation z_i the same dominance
 # yields U_i(Tx)>=U_i(z_i,T_-i x). Thus Tx is a reduced Nash profile.
 # These are universally quantified polynomial inequalities checked above.
 rr=reduced.verify_document(restricted)
 return {'scope':'every equilibrium of full32 no-opening game, arbitrary off-path calls retained',
 'precondition_events':count,'dominance_events':dc,'dominance_polynomials':3,
 'reduced_certificate':rr,'conclusion':'normalized profile is restricted18 Nash with identical payoffs; hence full32 no-opening U2=-1/48 and full family payoff vector',
 'seconds':time.time()-started}

if __name__=='__main__':
 out=ROOT/'attempts/solver/output'
 files=[out/'normalization_preconditions.json',out/'normalization_dominance.json',out/'restricted_family_certificate.json']
 if len(sys.argv)>1:files=[Path(p) for p in sys.argv[1:]];assert len(files)==3
 result=verify(*(json.loads(p.read_text()) for p in files));print(json.dumps(result,indent=2));print('NOOPEN_NORMALIZATION: PASS')
