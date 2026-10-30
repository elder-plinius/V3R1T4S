"""Independent deterministic verifier derived from the never-position definition.
Usage: python3 verify_assignment.py assignment.txt 25 EXPECTED_COUNT
The assignment gives one a b c iNj condition per triple, ranked top to bottom.
"""
from itertools import combinations,permutations
from pathlib import Path
import hashlib,json,re,sys,time

def parse(text,n):
 triples={}
 for line in text.splitlines():
  if not line.strip() or line.startswith('#'):continue
  m=re.fullmatch(r'\s*(\d+)\s+(\d+)\s+(\d+)\s+([123])N([123])\s*',line)
  if not m:raise ValueError('malformed line')
  a,b,c,i,j=map(int,m.groups());t=(a,b,c)
  if not 1<=a<b<c<=n or t in triples:raise ValueError('duplicate/out-of-range/unsorted triple')
  triples[t]=(t[i-1]-1,j)
 if set(triples)!=set(combinations(range(1,n+1),3)):raise ValueError('missing triple')
 return [(v,j,sum(1<<(x-1) for x in t if x!=v+1)) for t,(v,j) in triples.items()]

def count(n,cs):
 rules=[[] for _ in range(n)]
 for v,j,m in cs:rules[v].append((m,j-1))
 dp={0:1};states=0
 for depth in range(n):
  nxt={};states+=len(dp)
  for placed,ways in dp.items():
   for v in range(n):
    bit=1<<v
    if placed&bit:continue
    if all((placed&m).bit_count()!=rank for m,rank in rules[v]):
     child=placed|bit;nxt[child]=nxt.get(child,0)+ways
  dp=nxt
 return dp.get((1<<n)-1,0),states+len(dp)

def brute(n,cs):
 rules=[(v,j,tuple(x for x in range(n) if m>>x&1)) for v,j,m in cs]
 ans=0
 for order in permutations(range(n)):
  pos=[0]*n
  for k,v in enumerate(order):pos[v]=k
  ans+=all(1+sum(pos[x]<pos[v] for x in others)!=j for v,j,others in rules)
 return ans

def fish(n):return '\n'.join(f'{a} {b} {c} 2N{1 if b%2==0 else 3}' for a,b,c in combinations(range(1,n+1),3))

def validate():
 for n,want in [(3,4),(9,488),(20,2115186)]:assert count(n,parse(fish(n),n))[0]==want
 for bad in ['', '1 2 3 4N1','1 2 3 2N1\n1 2 3 2N1','2 1 3 1N1','1 2 4 1N1']:
  try:parse(bad,3)
  except ValueError:pass
  else:raise AssertionError('invalid parser input accepted')

if __name__=='__main__':
 start=time.monotonic();name,n,want=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]);data=Path(name).read_bytes();cs=parse(data.decode(),n)
 validate();v,states=count(n,cs);assert v==want,(v,want)
 restricted='\n'.join(l for l in data.decode().splitlines() if l.strip() and not l.startswith('#') and max(map(int,l.split()[:3]))<=9)
 c9=parse(restricted,9);d9=count(9,c9)[0];b9=brute(9,c9);assert b9==d9
 print(json.dumps({'assignment_sha256':hashlib.sha256(data).hexdigest(),'n':n,'triples':len(cs),'exact_count':v,'reachable_prefix_sets':states,'first9_dp':d9,'first9_bruteforce':b9,'calibration':'Fishburn9=488;20=2115186;malformed negatives rejected','seconds':time.monotonic()-start},indent=2))
 print('PASS')
