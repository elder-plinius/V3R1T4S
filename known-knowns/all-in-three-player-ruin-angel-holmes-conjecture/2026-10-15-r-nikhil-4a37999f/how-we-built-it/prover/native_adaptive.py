"""Optional fast prover. Verification uses a separate exact forward implementation."""
import ctypes,json,time,argparse,resource
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
from fractions import Fraction as F
from fast_regions import setup,encpoly,decpoly,cut
lib=ctypes.CDLL(str(Path(__file__).with_name('bounds_fast.dylib').resolve()))
I=ctypes.c_longlong;P=ctypes.POINTER(I)
lib.compute_bounds.argtypes=[P,ctypes.c_int,P,P,ctypes.c_int,P,P];lib.compute_bounds.restype=ctypes.c_int

def native(poly,A,B,depth):
 vals=[a for p in poly for a in p];av=[v for row in A for v in row];bv=[v for row in B for v in row]
 if any(abs(v)>=2**63 for v in vals+av+bv):raise ValueError('coordinate overflow')
 out=(I*4)();line=(I*3)();status=lib.compute_bounds((I*len(vals))(*vals),len(poly),(I*9)(*av),(I*9)(*bv),depth,out,line)
 if status<0:raise ValueError('kernel input')
 return list(out),tuple(line)if status else None

def run(args):
 path=Path(args.output);roots,A,B=setup(args.order)
 if path.exists() and args.resume:
  o=json.loads(path.read_text());nodes=o['nodes'];queue=o['pending']
 else:
  nodes=[{'poly':encpoly(p)}for p in roots];queue=list(range(len(nodes)));o={'schema':'adaptive-homogeneous-v1','order':args.order,'depth':args.depth,'roots':list(queue),'nodes':nodes}
 tick=time.monotonic();steps=0
 def assign(ix,vals,line):
  node=nodes[ix]
  if vals[0]>vals[3]:node['bounds']=vals
  elif line is None:node['unresolved']=vals
  else:
   children=[]
   for p in cut(decpoly(node['poly']),line):
    if not p:raise ValueError('empty child')
    j=len(nodes);nodes.append({'poly':encpoly(p),'depth':node.get('depth',o['depth'])});children.append(j);queue.append(j)
   node['line']=line;node['children']=children
 with ThreadPoolExecutor(max_workers=args.workers) as pool:
  active={}
  while queue or active:
   while queue and len(active)<args.workers and time.monotonic()-tick<args.seconds:
    ix=queue.pop();level=max(args.depth,nodes[ix].get('depth',o['depth']));nodes[ix]['depth']=level;active[pool.submit(native,decpoly(nodes[ix]['poly']),A,B,level)]=ix
   if not active:break
   done,_=wait(active,timeout=1,return_when=FIRST_COMPLETED)
   for f in sorted(done,key=lambda f:active[f]):
    ix=active.pop(f);vals,line=f.result();assign(ix,vals,line);steps+=1
   if steps and steps%200==0:print('nodes',len(nodes),'pending',len(queue),'steps',steps,flush=True)
 o['pending']=queue;tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(o,separators=(',',':')));tmp.replace(path)
 vals=[(p['bounds'],p.get('depth',o['depth']))for p in nodes if 'bounds'in p];bad=[i for i,p in enumerate(nodes)if'unresolved'in p]
 summary={'order':args.order,'depth':o['depth'],'maximum_depth':max(n.get('depth',o['depth'])for n in nodes),'nodes':len(nodes),'leaves':len(vals),'pending':len(queue),'unresolved':bad,'minimum_bound':str(min((F(v[0]-v[3],5*6**level) for v,level in vals),default=F(0))),'last_seconds':time.monotonic()-tick,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'engine':'native-optional','workers':args.workers}
 path.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('order',choices=['leader','middle','shortest']);p.add_argument('depth',type=int);p.add_argument('output');p.add_argument('--resume',action='store_true');p.add_argument('--seconds',type=float,default=38);p.add_argument('--workers',type=int,choices=[1,2],default=1);run(p.parse_args())
