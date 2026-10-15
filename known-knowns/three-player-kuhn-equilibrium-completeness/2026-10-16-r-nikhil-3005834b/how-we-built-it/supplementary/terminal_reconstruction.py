"""Definition-based exact proof of behavioral identification from joint terminal laws.
No imports from any supplied game, checker, or prover. Standard library only.
"""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
from collections import defaultdict
from datetime import datetime,timezone
import json
# SGS Table 1, rows P1,P2,P3, columns k=1..4. K check; B bet; F fold; C call.
SITUATIONS=(('', 'KKB', 'KBF', 'KBC'),('K','B','KKBF','KKBC'),('KK','KB','BF','BC'))
ACTORS={h:(i,k) for i,row in enumerate(SITUATIONS) for k,h in enumerate(row)}
class P:
 def __init__(self,x=0):self.c={m:Q(v) for m,v in x.items() if v} if isinstance(x,dict) else ({():Q(x)} if x else {})
 def __add__(self,y):
  y=y if isinstance(y,P) else P(y);d=dict(self.c)
  for m,v in y.c.items():d[m]=d.get(m,Q(0))+v
  return P(d)
 __radd__=__add__
 def __neg__(self):return P({m:-v for m,v in self.c.items()})
 def __sub__(self,y):return self+-((y if isinstance(y,P) else P(y)))
 def __rsub__(self,y):return P(y)+-self
 def __mul__(self,y):
  y=y if isinstance(y,P) else P(y);d=defaultdict(Q)
  for a,v in self.c.items():
   for b,w in y.c.items():d[tuple(sorted(a+b))]+=v*w
  return P(d)
 __rmul__=__mul__
 def __eq__(self,y):return self.c==(y.c if isinstance(y,P) else P(y).c)
 def value(self,x):
  out=Q(0)
  for m,c in self.c.items():
   for k in m:c*=x[k]
   out+=c
  return out
 def encode(self):return [[list(m),str(v)] for m,v in sorted(self.c.items())]
def variable(i,j,k):return P({(16*i+4*j+k,):1})
def tree(deal,h='',mass=None):
 mass=P(1) if mass is None else mass
 if h not in ACTORS:return {h:mass},{}
 i,k=ACTORS[h];q=variable(i,deal[i],k);letters='FC' if 'B' in h else 'KB'
 leaves={};prefixes={h:mass}
 for a,f in zip(letters,(1-q,q)):
  l,p=tree(deal,h+a,mass*f);leaves.update(l);prefixes.update(p)
 return leaves,prefixes

def main():
 deals=list(permutations(range(4),3));laws={};reaches={};cert=[];identities=0
 for deal in deals:
  leaves,prefixes=tree(deal);laws[deal]=leaves
  assert len(leaves)==13 and sum(leaves.values())==1
  for h,mass in prefixes.items():
   children=[x for x in leaves if x.startswith(h)]
   assert sum(leaves[x] for x in children)==mass
   i,k=ACTORS[h];last='C' if 'B' in h else 'B'
   chosen=[x for x in children if x.startswith(h+last)]
   assert sum(leaves[x] for x in chosen)==mass*variable(i,deal[i],k)
   cert.append({'deal':list(deal),'prefix':h,'actor':i,'card':deal[i],'situation':k,'terminal_cylinder':children,'positive_cylinder':chosen})
   identities+=2
 for i in range(3):
  for j in range(4):
   for k,h in enumerate(SITUATIONS[i]):
    direct=P();terminal=P();positive=P()
    for deal in deals:
     if deal[i]!=j:continue
     l,p=tree(deal);direct+=Q(1,24)*p[h]
     terminal+=Q(1,24)*sum(v for word,v in l.items() if word.startswith(h))
     positive+=Q(1,24)*sum(v for word,v in l.items() if word.startswith(h+('C' if 'B' in h else 'B')))
    assert terminal==direct and positive==direct*variable(i,j,k)
    reaches[(i,j,k)]=direct;identities+=2
 # Known negative: omitting a positive symbolic leaf breaks a cylinder identity.
 d=deals[0];leaf=next(iter(laws[d]));assert sum(v for h,v in laws[d].items() if h!=leaf)!=1
 # Public actions alone omit private chance data and do not identify behavior.
 x=[Q(0)]*48;y=x.copy()
 for i in range(3):
  for j in range(4):
   for k in range(1,4):x[16*i+4*j+k]=y[16*i+4*j+k]=Q(1)
 x[0]=1;y[4]=1
 def pub(z):
  out=defaultdict(Q)
  for l in laws.values():
   for h,v in l.items():out[h]+=v.value(z)/24
  return dict(out)
 assert pub(x)==pub(y) and x[0]!=y[0] and reaches[(0,0,0)].value(x)>0
 assert any(p.value(x)!=p.value(y) for l in laws.values() for p in l.values())
 out=None
 result={'utc':datetime.now(timezone.utc).isoformat(),'deals':len(deals),'leaf_cells':sum(map(len,laws.values())),'prefix_cells':len(cert),'information_sets':len(reaches),'symbolic_identities':identities,'omitted_leaf_rejected':True,'public_history_only_counterexample':{'x':list(map(str,x)),'y':list(map(str,y)),'common_public_law':{h:str(p) for h,p in pub(x).items() if p}},'scope':'All behavioral profiles; joint chance-deal/terminal-action law identifies all reached actions. No Nash assumption.'}
 # Supplementary copy prints results; no output writes.
 # Cylinder records are derived in memory.
 print(json.dumps({k:v for k,v in result.items() if k!='public_history_only_counterexample'},indent=2));print('TERMINAL_RECONSTRUCTION: PASS')
if __name__=='__main__':main()
