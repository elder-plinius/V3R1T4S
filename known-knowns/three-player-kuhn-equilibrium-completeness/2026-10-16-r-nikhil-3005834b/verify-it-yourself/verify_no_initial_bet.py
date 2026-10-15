"""Check a full-game proof that all four P1 opening frequencies vanish."""
if not __debug__:raise RuntimeError('Do not disable proof assertions')
from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'checker'))
import verify_full_open as F

def verify(obj):
 started=time.time();assert obj['variables']==F.N
 root,n,closed=F.check(obj['events']);assert not closed
 S=F.D['a']+F.D['b']
 positive,np,closed=F.check(obj['positive_bluff'],root,S,'gt');assert closed,'positive opening branch is not refuted'
 zero,nz,closed=F.check(obj['zero_bluff'],root,S,'eq');assert not closed
 for name in ['a','b','c','C']:assert F.has_eq(zero,F.D[name]),'missing zero opening conclusion'
 # Full-domain a,b>=0 makes S>=0; S>0 is impossible, and the S=0
 # branch proves all four opening probabilities equal zero.
 for name in ['a','b']:assert any(p==F.D[name] and rel=='ge' for p,rel in root.values())
 return {'variables':48,'events_checked':n+np+nz,'conclusion':'In every Nash equilibrium of the full game, P1 never bets first with any card.','seconds':time.time()-started}
if __name__=='__main__':
 p=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'attempts/solver/output/no_initial_bet_certificate.json'
 print(json.dumps(verify(json.loads(p.read_text())),indent=2));print('NO_INITIAL_BET: PASS')
