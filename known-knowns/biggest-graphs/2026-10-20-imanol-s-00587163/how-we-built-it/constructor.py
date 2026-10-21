import json
from pathlib import Path
import numpy as np
from ddlib import load_graph, edges_to_adj, exact_cost, write_edges, reach_sets
from covers import cover

def cost(n,E,delta,D):
 a,d=edges_to_adj(n,np.array(sorted(E),np.int64),delta)
 return int(exact_cost(a,d,n,D)[0])

def build(path,delta,D,out,seed=0,fill=True):
 n,E=load_graph(path);a,d=edges_to_adj(n,E,delta);W=(n+63)//64
 B=reach_sets(a,d,n,D-1,W,np.zeros((n,W),np.uint64),np.zeros((n,W),np.uint64)).copy()
 unc,S=cover(B,n,delta,np.arange(n),seed)
 print(json.dumps(dict(event='cover',n=n,seed=seed,uncovered=unc,chosen=S)),flush=True)
 cur=set(map(tuple,E.tolist()));rng=np.random.default_rng(seed)
 for s in S:
  _,deg=edges_to_adj(n,np.array(sorted(cur),np.int64),delta)
  if deg[s]<delta:continue
  free=[int(u) for u in np.where(deg<delta)[0] if u not in S]
  if len(free)>32:free=rng.choice(free,32,replace=False).tolist()
  scored=sorted((cost(n,cur-{e},delta,D),e) for e in cur if s in e)
  best=(scored[0][0],scored[0][1],None)
  for base_c,e in scored[:3]:
   t=e[1] if e[0]==s else e[0]
   for u in free:
    new=tuple(sorted((t,u)))
    if u==t or new in cur:continue
    c=cost(n,(cur-{e})|{new},delta,D)
    if c<best[0]:best=(c,e,u)
  c,e,u=best;cur.remove(e)
  if u is not None:
   t=e[1] if e[0]==s else e[0];cur.add(tuple(sorted((t,u))))
  print(json.dumps(dict(event='pivot',center=s,edge=e,partner=u,cost=c)),flush=True)
 for s in S:cur.add((s,n))
 if fill:
  while True:
   _,deg=edges_to_adj(n+1,np.array(sorted(cur),np.int64),delta)
   if deg[n]>=delta:break
   free=[int(v) for v in np.where(deg[:n]<delta)[0] if (v,n) not in cur]
   if not free:break
   scored=[(cost(n+1,cur|{(v,n)},delta,D),v) for v in free]
   c,v=min(scored);cur.add((v,n))
   print(json.dumps(dict(event='fill',v=v,cost=c)),flush=True)
 c=cost(n+1,cur,delta,D);p=Path(str(out)+f'_n{n+1}_c{c}.edges')
 write_edges(p,np.array(sorted(cur),np.int64),f'local construction seed={seed}; N={n+1}; bad_pairs={c}')
 print(json.dumps(dict(event='constructed',path=str(p),n=n+1,cost=c,seed=seed)),flush=True)
 return p,c
