"""Prover: split relatively open rational polygons on needed decision lines."""
import json,time,argparse,math
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
class Split(Exception):
 def __init__(self,line):self.line=canonical(line)
def canonical(l):
 g=math.gcd(*l)
 if not g:return tuple(l)
 l=tuple(v//g for v in l)
 return tuple(-v for v in l) if next(v for v in l if v)!=abs(next(v for v in l if v)) else l
def point(p):
 if len(p)==2:
  x,y=map(F,p);w=math.lcm(x.denominator,y.denominator);p=(int(x*w),int(y*w),w)
 g=math.gcd(*p);p=tuple(x//g for x in p)
 return tuple(-x for x in p) if p[2]<0 else p
def val(l,p):return sum(a*b for a,b in zip(l,p))
def sign(l,poly):
 v=[val(l,p) for p in poly];lo,hi=min(v),max(v)
 if lo==hi==0:return 0
 if lo>=0:return 1
 if hi<=0:return -1
 raise Split(l)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,k):return tuple(k*x for x in a)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def clean(p):
 q=[]
 for x in p:
  if x not in q:q.append(x)
 while len(q)>2:
  changed=False
  for i in range(len(q)):
   if val(cross(q[i-1],q[i]),q[(i+1)%len(q)])==0:q.pop(i);changed=True;break
  if not changed:break
 return tuple(q)
def cut(poly,line):
 out=[]
 for keep in (-1,1):
  q=[]
  edges=list(zip(poly,poly[1:]+poly[:1])) if len(poly)>2 else [(poly[0],poly[-1])]
  for a,b in edges:
   va,vb=val(line,a)*keep,val(line,b)*keep
   if va>=0:q.append(a)
   if va*vb<0:q.append(point(tuple(vb*a[i]-va*b[i] for i in range(3))))
   if len(poly)==2 and vb>=0:q.append(b)
  out.append(clean(q))
 eq=[]
 for q in out:
  for p in q:
   if val(line,p)==0 and p not in eq:eq.append(p)
 return out[0],clean(eq),out[1]
def encpoly(p):return [list(point(q)) for q in p]
def decpoly(p):return tuple(tuple(q) for q in p)
def calc(poly,n,initial):
 cache={}
 def sg(l):
  if l not in cache:cache[l]=sign(l,poly)
  return cache[l]
 @lru_cache(None)
 def rec(state,k):
  if k==0:return (0,1) # numerator of loss and survival, denominator 6^k
  for a in state:
   if sg(a)<=0:return (0,0)
  a,b,c=state
  lose=int(sg(sub(a,b))<=0)+int(sg(sub(a,c))<=0)
  h=lose*6**(k-1);surv=0
  nxt=[(mul(a,2),sub(b,a),c),(mul(a,2),b,sub(c,a)),(sub(a,b),mul(b,2),c),(a,mul(b,2),sub(c,b)),(sub(a,c),b,mul(c,2)),(a,sub(b,c),mul(c,2))]
  for s in nxt:
   # Prune absorption before k=0.
   if all(sg(t)>0 for t in s):
    u,v=rec(s,k-1);h+=u;surv+=v
  return h,surv
 return rec(tuple(initial),n)
def setup(order):
 X=(1,0,0); Z=(0,1,0); ONE=(0,0,1)
 if order=='middle':return [((F(0),F(0)),(F(0),F(1)),(F(1),F(1)))],(X,ONE,Z),(ONE,ONE,Z)
 # normalize y+z=1, coordinates x,y
 Y=(0,1,0);ZZ=(0,-1,1)
 if order=='leader':return [((F(0),F(0)),(F(0),F(1,2)),(F(1,2),F(1,2))),((F(0),F(1,2)),(F(1,2),F(1,2)))],(X,Y,ZZ),(Y,Y,ZZ)
 if order=='shortest':return [((F(0),F(0)),(F(1),F(0)),(F(1),F(1))),((F(0),F(0)),(F(1),F(1)))],(X,ONE,Z),(ONE,ONE,Z)
 raise ValueError(order)
def run(args):
 path=Path(args.output); roots,A,B=setup(args.order)
 if path.exists() and args.resume:
  obj=json.loads(path.read_text());nodes=obj['nodes'];queue=obj['pending'];min_gap=int(obj['minimum_numerator'])
 else:
  nodes=[{'poly':encpoly(p)} for p in roots];queue=list(range(len(nodes)));obj={'schema':'homogeneous-v1','order':args.order,'depth':args.depth,'roots':list(queue),'nodes':nodes};min_gap=6**args.depth
 start=time.monotonic();leaves=0
 while queue and time.monotonic()-start<args.seconds:
  ix=queue.pop();node=nodes[ix];poly=decpoly(node['poly'])
  try:
   ha,sa=calc(poly,args.depth,A);hb,sb=calc(poly,args.depth,B)
  except Split as s:
   children=[]
   for child in cut(poly,s.line):
    assert child
    j=len(nodes);nodes.append({'poly':encpoly(child)});children.append(j);queue.append(j)
   node['line']=list(s.line);node['children']=children
  else:
   gap=ha-hb;node['values']=[ha,sa,hb,sb];min_gap=min(min_gap,gap);leaves+=1
  if len(nodes)%1000<3:print('nodes',len(nodes),'pending',len(queue),'min',min_gap,flush=True)
 obj.update(pending=queue,minimum_numerator=str(min_gap),last_seconds=time.monotonic()-start)
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,separators=(',',':')));tmp.replace(path)
 vals=[q['values'] for q in nodes if 'values'in q]
 den=6**args.depth
 summary={'order':args.order,'depth':args.depth,'nodes':len(nodes),'leaves':len(vals),'pending':len(queue),'minimum_numerator':min_gap,'denominator':den,'minimum':str(F(min_gap,den)),'universal_tail_pass':bool(not queue and min_gap>3**args.depth),'survival_tail_failures':sum(5*(a-c)<=4*d for a,b,c,d in vals),'last_seconds':obj['last_seconds']}
 print(json.dumps(summary),flush=True)
 path.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('order',choices=['middle','leader','shortest']);p.add_argument('depth',type=int);p.add_argument('output');p.add_argument('--seconds',type=float,default=40);p.add_argument('--resume',action='store_true');run(p.parse_args())
