"""Standalone exact verification; Python standard library only."""
import hashlib,itertools,json,sys
from pathlib import Path

def check(path,expected=None):
 raw=Path(path).read_bytes()
 lines=raw.decode('ascii').splitlines()
 if not lines or any(len(s)!=35 or set(s)-{'0','1'} for s in lines):
  raise ValueError('expected one 35-bit word per line')
 words=[int(s,2) for s in lines]
 if expected is not None and len(words)!=expected:raise ValueError('incorrect cardinality')
 if any(w.bit_count()!=6 for w in words):raise ValueError('incorrect weight')
 if len(set(words))!=len(words):raise ValueError('duplicate words')
 # Any common 4-subset would give intersection >=4 and distance <=4.
 seen=set()
 for w in words:
  positions=[i for i in range(35) if w>>i&1]
  for sub in itertools.combinations(positions,4):
   if sub in seen:raise ValueError('repeated 4-subset, distance below six')
   seen.add(sub)
 mind=35;pairs=0
 for j,x in enumerate(words):
  for y in words[:j]:
   dist=(x^y).bit_count();pairs+=1
   if dist<6:raise ValueError('distance below six')
   mind=min(mind,dist)
 return {'n':35,'d_min':mind,'w':6,'M':len(words),'pairs_checked':pairs,'distinct_four_subsets':len(seen),'sha256':hashlib.sha256(raw).hexdigest()}
if __name__=='__main__':
 try:
  print(json.dumps(check(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else None),sort_keys=True))
  print('PASS')
 except (ValueError,UnicodeError,OSError,IndexError) as e:
  print('FAIL:',e);sys.exit(1)
