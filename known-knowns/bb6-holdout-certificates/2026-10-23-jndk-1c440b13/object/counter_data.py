"""Run-counter transducer. No binary tape expansion, bitset, or TM table.
State = {'phase':'front'/'sweep','left':[(gap,ones),...],
         'right':{'z':leading_zero_count_or_None,'tokens':[(ones,gap_or_None),...]}}.
left is nearest-first; right is increasing coordinate; final gap None is blank.
All primitives splice integer intervals and operate once per RUN, never percell.
"""
from bisect import bisect_right

class Runs:
 def __init__(self,intervals=()):self.iv=self.merge(intervals)
 @staticmethod
 def merge(iv):
  out=[]
  for a,b in sorted(iv):
   if a>=b:continue
   if out and a<=out[-1][1]:out[-1]=(out[-1][0],max(b,out[-1][1]))
   else:out.append((a,b))
  return out
 def locate(self,q):
  i=bisect_right([a for a,b in self.iv],q)-1
  return i if i>=0 and self.iv[i][0]<=q<self.iv[i][1]else None
 def bit(self,q):return int(self.locate(q)is not None)
 def right_ones(self,q):
  i=self.locate(q)
  return self.iv[i][1]-q if i is not None else 0
 def left_ones(self,q):
  i=self.locate(q)
  return q-self.iv[i][0]+1 if i is not None else 0
 def gap_right(self,q):
  for a,b in self.iv:
   if b>q:return max(a-q,0)
  return None
 def gap_left(self,q):
  for a,b in reversed(self.iv):
   if a<q:return max(q-b,0)
  return None
 def clear(self,lo,hi):
  out=[]
  for a,b in self.iv:
   if b<=lo or a>=hi:out.append((a,b))
   else:
    if a<lo:out.append((a,lo))
    if b>hi:out.append((hi,b))
  self.iv=out
 def add(self,lo,hi):self.iv=self.merge(self.iv+[(lo,hi)])
 def put(self,lo,runs):
  length=sum(n for bit,n in runs);self.clear(lo,lo+length)
  add=[];q=lo
  for bit,n in runs:
   assert bit in(0,1)and n>=0
   if bit and n:add.append((q,q+n))
   q+=n
  self.iv=self.merge(self.iv+add)

def well_formed(state):
 try:
  if state['phase']not in('front','sweep'):return False
  left=state['left'];right=state['right'];tokens=right['tokens'];z=right['z']
  if any(type(g)is not int or type(b)is not int or b<1 or g<(0 if i==0 else 1)for i,(g,b)in enumerate(left)):return False
  if not tokens:return z is None
  if type(z)is not int or z<1:return False
  for i,(b,g)in enumerate(tokens):
   if type(b)is not int or b<1:return False
   if i==len(tokens)-1:
    if g is not None:return False
   elif type(g)is not int or g<1:return False
  return True
 except (TypeError,KeyError,ValueError):return False

def decode(state):
 assert well_formed(state)
 iv=[];q=0
 for g,b in state['left']:
  assert g>=0 and b>=1
  q-=g;iv.append((q-b,q));q-=b
 right=state['right'];tokens=right['tokens'];z=right['z']
 if tokens:
  assert z>=1;q=z
  for i,(b,g)in enumerate(tokens):
   assert b>=1
   iv.append((q,q+b));q+=b
   if i==len(tokens)-1:assert g is None
   else:assert g>=1;q+=g
 else:assert z is None
 return Runs(iv)

def encode(t,p,phase):
 assert not t.bit(p)
 left=[];q=p;ri=[]
 for a,b in reversed(t.iv):
  if b<=p:left.append((q-b,b-a));q=a
 for a,b in t.iv:
  if a>p:ri.append((a,b))
 tokens=[(b-a,ri[i+1][0]-b if i+1<len(ri)else None)for i,(a,b)in enumerate(ri)]
 return dict(phase=phase,left=left,right=dict(z=ri[0][0]-p if ri else None,tokens=tokens))

def grammar(state):
 """Candidate reachable language; preservation needs a universal proof."""
 if not well_formed(state):return False
 phase=state['phase'];z=state['right']['z'];tokens=state['right']['tokens']
 if not tokens:return phase=='front'and z is None
 if z not in(1,2,3)or(phase=='sweep'and z!=1):return False
 if any(g not in(1,2,None)for b,g in tokens):return False
 if phase=='sweep'or z in(2,3):tested=tokens
 elif tokens[0][0]==1 and tokens[0][1]==1:tested=tokens[2:]
 else:tested=tokens
 return all(g!=1 or b>=2 for b,g in tested)

