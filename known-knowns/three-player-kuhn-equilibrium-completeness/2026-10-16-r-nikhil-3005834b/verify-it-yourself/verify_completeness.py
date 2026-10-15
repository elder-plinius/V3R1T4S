"""Compose the full-game no-opening and conditional family certificates."""
if not __debug__:raise RuntimeError('Do not disable proof assertions')
from pathlib import Path
import sys,json,time
import verify_no_initial_bet as opening
import verify_conditional_family as family
F=opening.F;N=family.F;ROOT=opening.ROOT

def restrict(p):
 out=N.Poly()
 for mon,co in p.c.items():
  if any(mon[F.N.index(name)] for name in ['a','b','c','C']):continue
  assert not any(mon[32:]),'initial response survives after opening probabilities vanish'
  out+=N.Poly({mon[:32]:co})
 return out

def verify(folder):
 start=time.time();folder=Path(folder)
 get=lambda name:json.loads((folder/name).read_text())
 op=opening.verify(get('no_initial_bet_certificate.json'))
 assert F.N[:32]==N.N
 for i in range(3):assert restrict(F.U[i])==N.U[i],'full-game restriction mismatch'
 # Restricting P1's available deviations to the face a=b=c=C=0
 # preserves every best-response inequality of a full-game equilibrium.
 # Other players' feasible realization strategies are unchanged, and the
 # exact polynomial comparison above identifies the resulting game.
 fam=family.verify(*(get(n) for n in ['normalization_preconditions.json','normalization_dominance.json','restricted_family_certificate.json','terminal_family_certificate.json']))
 return {'opening':op,'conditional_family':fam,'conclusion':'Every Nash equilibrium of three-player Kuhn poker induces the same terminal-history distribution as some member of Szafron-Gibson-Sturtevant Tables 2-3.','criterion':'B','seconds':time.time()-start}
if __name__=='__main__':
 folder=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'attempts/solver/output'
 print(json.dumps(verify(folder),indent=2));print('FULL_GAME_COMPLETENESS: PASS')
