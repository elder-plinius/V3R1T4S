import numpy as np,time,json,pathlib,os,datetime,itertools,random,ctypes
P=pathlib.Path(__file__).resolve().parents[1]; random.seed(13791)
try:ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
except Exception:pass
(P/'pid.txt').write_text(str(os.getpid())); T=time.time(); END=T+1100
mul=np.array([[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]],dtype=np.uint8)
points=np.array(list(itertools.product(range(4),repeat=2)),dtype=np.uint8)
raw=np.array([a^mul[b,points[:,0]]^mul[c,points[:,1]] for a,b,c in itertools.product(range(4),repeat=3)],dtype=np.uint8)
table=json.load(open(P.parents[1]/'data/table.json')); tab={(x['n'],x['d']):x['value'] for x in table if not x['optimal']}
best={}; counts={}; trials=0

def clique(adj,limit):
 deadline=time.time()+limit; best=[];nodes=0
 def go(R,mask):
  nonlocal best,nodes
  nodes+=1
  if nodes%256==0 and time.time()>deadline:return
  if len(R)+mask.bit_count()<=len(best):return
  order=[];bounds=[];left=mask;color=0
  while left:
   color+=1;avail=left
   while avail:
    bit=avail&-avail;v=bit.bit_length()-1;order.append(v);bounds.append(color);left^=bit;avail^=bit;avail&=~adj[v]
  for v,b in zip(order[::-1],bounds[::-1]):
   if len(R)+b<=len(best):return
   new=mask&adj[v]
   if new:go(R+[v],new)
   elif len(R)+1>len(best):best=R+[v]
   mask&=~(1<<v)
   if time.time()>deadline:return
 go([], (1<<len(adj))-1)
 return best,nodes

def evaluate(W,d,label,limit=.025):
 global trials
 trials+=1;n=W.shape[1]
 rc=(W[:,::-1]^1); dist=np.count_nonzero(W[:,None,:]!=rc[None,:,:],axis=2)
 good=np.where(np.diag(dist)>=d)[0]
 if len(good)<=best.get((n,d),0):return
 ordinary=np.count_nonzero(W[good,None,:]!=W[None,good,:],axis=2)
 ok=(dist[np.ix_(good,good)]>=d)&(ordinary>=d);np.fill_diagonal(ok,False)
 adj=[sum(1<<int(j) for j in np.flatnonzero(row)) for row in ok]
 ids,nodes=clique(adj,limit);m=len(ids);key=(n,d)
 counts[label]=counts.get(label,0)+1
 if m>best.get(key,0):
  best[key]=m;ws=[''.join('ATCG'[int(v)] for v in row) for row in W[good[ids]]]
  out={'n':n,'d':d,'size':m,'table':tab.get(key),'method':label,'words':ws,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trial':trials,'seconds':time.time()-T}
  (P/('best_%s_%s.json'%key)).write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='words'}),flush=True)
  if m>tab.get(key,10**9):print('TABLE_IMPROVEMENT',flush=True)

def build(cols,ts):
 n=len(cols);off=np.zeros(n,dtype=np.uint8)
 for i,t in enumerate(ts):off[n-1-i]=1^t
 W=raw[:,cols]^off
 return W[np.count_nonzero(W>=2,axis=1)==n//2]
