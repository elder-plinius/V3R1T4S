"""Minimal restricted run-counter recurrence; no TM interpreter or tape expansion.
See counter_data.py for exact full-context counter encoding and language predicate.
The only terminal is a small-counter halting pattern. EveryNEXT haspositive time.
"""
from counter_data import decode,encode,grammar,well_formed
START={'phase':'front','left':[],'right':{'z':None,'tokens':[]}}

def step(state):
 t=decode(state);p=0;s=state['phase'];halt=False
 def runleft():
  nonlocal p,s
  m=t.left_ones(p)
  if m:
   p-=m
   if m%2:s='sweep'if s=='front'else'front'
  return m
 if s=='sweep':
  b=t.left_ones(p-1)
  if b:
   lo=p-b-1;t.put(lo,[(0,1),(1,b-1),(0,2)]);p=lo;s='sweep'if b%2==0 else'front';dt=b+1;rule='C_adj'
  elif not t.bit(p-2):
   t.put(p-2,[(0,1),(1,1),(0,1)]);p-=2;s='front';dt=2;rule='C_END'
  else:
   b=t.left_ones(p-2);lo=p-b-2;t.put(lo,[(0,1),(1,b+1),(0,1)]);p=lo;s='sweep'if b%2 else'front';dt=b+2;rule='C_iso'
 else:
  assert s=='front'
  n=t.right_ones(p+1);g=t.gap_right(p+1+n)
  if n==0:
   t.put(p,[(1,2)]);p-=1;dt=3+runleft();rule='ZERO'
  elif n>=2:
   if g==1:
    t.put(p,[(1,n-1),(0,1),(1,1),(0,1)]);p+=n+1;dt=5*n-7;rule='SCAN'
   else:
    assert g is None or g>=2
    x=t.bit(p-1);t.put(p-1,[(x,1),(1,n-2),(0,2),(1,3)]);p-=1;s='front'if n%2==0 else'sweep';dt=6*n-3+runleft();rule='TRANSFER'
  else:
   assert n==1
   if g is None or g>=2:
    t.put(p,[(1,1),(0,3)]);p+=3;dt=3;halt=True;rule='HALT_FRONT1'
   else:
    assert g==1
    c=t.right_ones(p+3);gg=t.gap_right(p+3+c)
    if c==1:
     if gg is None:
      t.put(p,[(1,1),(0,1),(1,1),(0,1),(1,1)]);p+=1;dt=7;rule='D1_TRAVEL'
     else:
      b=t.right_ones(p+4+gg);assert b>=1
      t.put(p,[(1,gg),(0,1),(1,1),(0,1),(1,b+1)]);p+=gg;dt=7*gg;rule='D1_FOLD'
    elif c==2:
     if gg is None or gg>=2:
      t.put(p,[(1,1),(0,6)]);p+=6;dt=6;halt=True;rule='HALT_D2'
     else:
      assert gg==1
      # InitialD2prefix and eachcarrycycle deletea singletonblock/gap/firstone
      # ofitsnextblock. Cursor is always a runboundary, never an interpretedTMstep.
      t.add(p,p+1);t.clear(p+1,p+4);cursor=p+4;k=1
      while t.right_ones(cursor)==1 and t.gap_right(cursor+1)==1:
       t.clear(cursor,cursor+3);cursor+=3;k+=1
      if not t.bit(cursor):
       t.add(cursor,cursor+1);t.add(cursor-2,cursor-1);p=cursor-3;dt=3*k+4;rule='CARRY_ONE'
      elif t.right_ones(cursor)>=2:
       t.clear(cursor,cursor+1);p=cursor+2;dt=3*k+3
       if t.bit(p):
        assert t.left_ones(p)==2
        dt+=runleft()
       rule='CARRY_LARGE'
      else:
       assert t.gap_right(cursor+1)is None or t.gap_right(cursor+1)>=2
       t.clear(cursor,cursor+2);p=cursor+2;dt=3*k+3;halt=True;rule='HALT_CARRY'
    elif c==3:
     if gg==1:
      t.put(p,[(1,1),(0,4),(1,1),(0,1)]);p+=6;dt=6;rule='D3_GAP1'
     else:
      assert gg is None or gg>=2
      t.put(p,[(1,1),(0,2),(1,1),(0,1),(1,3)]);p+=2;dt=12;rule='D3_FOLD'
    else:
     assert c>=4
     t.put(p,[(1,1),(0,4),(1,2)]);p+=4;dt=8;rule='D_SEED'
 assert dt>0
 return ('HALT' if halt else 'NEXT'),encode(t,p,s),p,dt,rule
