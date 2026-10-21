import sys,os,time,json,datetime,argparse,hashlib
from pathlib import Path
import numpy as np
from ddlib import load_graph,load_edges_file_order,edges_to_adj,adj_to_edges,exact_cost,write_edges
from sa2 import sa2_run
r=Path(__file__).resolve().parents[3];w=r.parents[1]
sys.path.insert(0,str(r/'attempts/constructor/code'))
from build import build
ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float);args=ap.parse_args()
deadline=datetime.datetime.fromisoformat(json.loads((r/'start.json').read_text())['search_deadline']).timestamp()
if args.seconds:deadline=min(deadline,time.time()+args.seconds)
out=r/'attempts/optimizer';checkpoint=out/'checkpoint.json'
valid=w/'outbox/submitted-baseline-package/object/G_13_4_n6631.edges'
state=r/'attempts/constructor/seed0_n6632_c232.edges'
seed=1000;rounds=0;best_cost=232;stale=0;best_n=6631
if checkpoint.exists():
 cp=json.loads(checkpoint.read_text());state=Path(cp['state']);valid=Path(cp['valid']);seed=cp['next_seed'];rounds=cp['rounds'];best_cost=cp['cost'];stale=cp['stale'];best_n=cp['best_valid_n']
def log(**data):
 print(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**data)),flush=True)
def savecp():
 checkpoint.write_text(json.dumps(dict(pid=os.getpid(),state=str(state),valid=str(valid),next_seed=seed,rounds=rounds,cost=best_cost,stale=stale,best_valid_n=best_n,deadline=deadline),indent=2))
savecp();log(event='start',pid=os.getpid(),deadline=deadline,state=str(state))
while time.time()<deadline:
 n,E=load_edges_file_order(state);a,d=edges_to_adj(n,E,13)
 c0=int(exact_cost(a,d,n,4)[0]);assert c0==best_cost
 # Small chunks preserve a checkpoint and impose a practical per-call ceiling.
 T0,T1=[(.15,.02),(.5,.04),(1.5,.08),(.08,.01)][rounds%4]
 t=time.monotonic();best,aa,dd,acc,nfull,nscr=sa2_run(a,d,n,4,13,5000,T0,T1,seed,.6,0.,.2,10**12,0)
 E2=adj_to_edges(aa,dd);actual=int(exact_cost(aa,dd,n,4)[0]);assert int(best)==actual
 elapsed=time.monotonic()-t
 log(event='anneal',seed=seed,n=n,start_cost=c0,best_cost=actual,accepted=int(acc),full=int(nfull),screened=int(nscr),seconds=elapsed,T0=T0,T1=T1)
 seed+=1;rounds+=1
 if actual<best_cost:
  state=out/f'best_n{n}_s{seed-1}_c{actual}.edges';write_edges(state,E2,f'local bounded annealing; N={n}; bad_pairs={actual}; seed={seed-1}')
  best_cost=actual;stale=0
 else:stale+=1
 savecp()
 if actual==0:
  valid=state;best_n=n
  log(event='valid_candidate_unpanelled',n=n,path=str(valid),sha256=hashlib.sha256(valid.read_bytes()).hexdigest())
  (out/'best_valid.json').write_text(json.dumps(dict(n=n,path=str(valid),sha256=hashlib.sha256(valid.read_bytes()).hexdigest(),status='PROMISING (single-context, unpanelled)'),indent=2))
  savecp()
  if time.time()+120>=deadline:break
  state,best_cost=build(valid,13,4,r/f'attempts/constructor/reinsert{n+1}_s{seed}',seed)
  stale=0;savecp()
 elif stale>=24 and time.time()+120<deadline:
  # Rebuild a different cover rather than repeatedly anneal an unchanged basin.
  new,c=build(valid,13,4,r/f'attempts/constructor/restart_s{seed}',seed)
  if c<best_cost or rounds%96==0:state,best_cost=new,c
  stale=0;savecp()
log(event='search_stop',best_valid_n=best_n,state=str(state),cost=best_cost,rounds=rounds)
savecp()
