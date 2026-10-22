"""Prover: conservative interval expansion with early stopping at unknown order."""
import json,time,argparse,resource
from pathlib import Path
from collections import Counter
from functools import lru_cache
from fractions import Fraction as F
from fast_regions import setup,encpoly,decpoly,sign,sub,mul,Split,canonical,cut

def bounds(poly,depth,start):
 signs={};weights=Counter()
 def sg(line):
  if line not in signs:
   try:signs[line]=sign(line,poly)
   except Split:signs[line]=None
  return signs[line]
 @lru_cache(None)
 def rec(s,d):
  if d==0:return 0,4
  lo=hi=0
  for i,j in ((0,1),(0,2),(1,2)):
   line=sub(s[i],s[j]);order=sg(line);unit=6**(d-1)
   if order is None:
    hi+=(9 if 0 in (i,j) else 4)*unit
    weights[canonical(line)]+=(9 if 0 in (i,j) else 4)*unit
   elif order==0:
    if 0 in (i,j):lo+=5*unit;hi+=5*unit
   else:
    small,big=(i,j) if order<0 else (j,i)
    if small==0:lo+=5*unit;hi+=5*unit
    t=list(s);t[small]=mul(s[small],2);t[big]=sub(s[big],s[small])
    a,b=rec(tuple(t),d-1);lo+=a;hi+=b
  return lo,hi
 a,b=rec(tuple(start),depth)
 return a,b,weights

def run(args):
 p=Path(args.output);roots,A,B=setup(args.order)
 if p.exists() and args.resume:
  obj=json.loads(p.read_text());nodes=obj['nodes'];queue=obj['pending']
 else:
  nodes=[{'poly':encpoly(q)} for q in roots];queue=list(range(len(nodes)));obj={'schema':'adaptive-homogeneous-v1','order':args.order,'depth':args.depth,'roots':list(queue),'nodes':nodes}
 start=time.monotonic();step=0
 while queue and time.monotonic()-start<args.seconds:
  ix=queue.pop();node=nodes[ix];poly=decpoly(node['poly']);a,b,w=bounds(poly,args.depth,A);c,d,v=bounds(poly,args.depth,B)
  if a>d:node['bounds']=[a,b,c,d]
  else:
   w.update(v)
   if not w:node['unresolved']=[a,b,c,d]
   else:
    line=w.most_common(1)[0][0];cs=[]
    for q in cut(poly,line):
     assert q
     j=len(nodes);nodes.append({'poly':encpoly(q)});cs.append(j);queue.append(j)
    node['line']=list(line);node['children']=cs
  step+=1
  if step%500==0:print('nodes',len(nodes),'pending',len(queue),'step',step,flush=True)
 obj['pending']=queue
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(obj,separators=(',',':')));tmp.replace(p)
 vals=[q['bounds'] for q in nodes if 'bounds'in q];bad=[i for i,q in enumerate(nodes) if 'unresolved'in q]
 summary={'order':args.order,'depth':args.depth,'nodes':len(nodes),'leaves':len(vals),'pending':len(queue),'unresolved':bad,'minimum_bound':str(F(min((a-d for a,b,c,d in vals),default=0),5*6**args.depth)),'last_seconds':time.monotonic()-start,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 p.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('order',choices=['middle','leader','shortest']);p.add_argument('depth',type=int);p.add_argument('output');p.add_argument('--seconds',type=float,default=40);p.add_argument('--resume',action='store_true');run(p.parse_args())
