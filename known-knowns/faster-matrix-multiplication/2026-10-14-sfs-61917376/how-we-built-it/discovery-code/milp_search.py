#!/usr/bin/env python3
"""Acyclic finite signed-grammar dependency selection, checked over Z."""
import argparse, datetime, hashlib, json, os, random, resource, signal, sys, time
sys.dont_write_bytecode=True
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
import synth,dag_search

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def solve(n,g,upper,seconds,rng):
 vals,edges,targetids,targets,cancelled=g;N=len(vals)
 flat=[(k,i,j,a,b) for k,es in enumerate(edges) if k>=n for i,j,a,b in es];E=len(flat)
 num=2*N+E;obj=np.zeros(num);obj[n:N]=1
 lb=np.zeros(num);ub=np.ones(num);ub[N+E:]=N;lb[:n]=ub[:n]=1;ub[N+E:N+E+n]=0
 for k,s in targetids:
    if k is not None:lb[k]=1
 integer=np.zeros(num);integer[:N+E]=1
 rowids=[];colids=[];data=[];low=[];high=[]
 def constraint(coefs,l=-np.inf,h=np.inf):
    q=len(low)
    for j,c in coefs.items():rowids.append(q);colids.append(j);data.append(c)
    low.append(l);high.append(h)
 outgoing={k:{} for k in range(n,N)}
 for e,(k,i,j,a,b) in enumerate(flat):
    y=N+e;outgoing[k][y]=1
    for parent in {i,j}:
        constraint({parent:1,y:-1},l=0)
        constraint({N+E+parent:1,N+E+k:-1,y:N+1},h=N)
 for k,terms in outgoing.items():terms[k]=-1;constraint(terms,0,0)
 constraint({k:1 for k in range(n,N)},h=upper)
 matrix=coo_matrix((data,(rowids,colids)),shape=(len(low),num)).tocsc()
 before=time.monotonic()
 res=milp(obj,integrality=integer,bounds=Bounds(lb,ub),constraints=LinearConstraint(matrix,low,high),options={'time_limit':seconds,'mip_rel_gap':0.0,'threads':1})
 info={'status':int(res.status),'message':str(res.message),'seconds':time.monotonic()-before,'vectors':N,'edges':E,'variables':num,'constraints':len(low),'upper_bound':upper,'mip_gap':getattr(res,'mip_gap',None),'mip_node_count':getattr(res,'mip_node_count',None),'objective':None if res.fun is None else float(res.fun)}
 if res.x is None:return None,info
 selected={k:(i,j,a,b) for e,(k,i,j,a,b) in enumerate(flat) if res.x[N+e]>.5}
 active={k for k in range(n,N) if res.x[k]>.5};assert set(selected)==active
 circuit=synth.Circuit(n);available={i:{i:1} for i in range(n)};pending=set(selected)
 while pending:
    ready=sorted(k for k in pending if selected[k][0] in available and selected[k][1] in available)
    if not ready:raise ValueError('selected dependency graph contains a cycle')
    for k in ready:
        i,j,a,b=selected[k]
        available[k]=circuit.materialize([(v,a*c) for v,c in available[i].items()]+[(v,b*c) for v,c in available[j].items()],rng)
        pending.remove(k)
 outputs=[{} if k is None else {i:s*c for i,c in available[k].items()} for k,s in targetids]
 result=synth.prune(n,circuit.fresh,outputs);assert synth.vectors(n,*result)==targets
 info['reconstructed_count']=synth.count(*result);info['selected_dependencies']=[{'node':k,'parents':list(v)} for k,v in sorted(selected.items())]
 return result,info

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,default=420);ap.add_argument('--per-map',type=float,default=8);ap.add_argument('--seed',type=int,default=2026101406);ap.add_argument('--tag',default='milp-source');ap.add_argument('--files',nargs='*');args=ap.parse_args()
 start=time.monotonic();rng=random.Random(args.seed);records=[];out=synth.HERE/'output'
 resource.setrlimit(resource.RLIMIT_CPU,(args.seconds+2,args.seconds+3));resource.setrlimit(resource.RLIMIT_NOFILE,(256,256))
 signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard SIGALRM cap')));signal.alarm(args.seconds)
 selected=json.loads((synth.HERE.parents[1]/'data/selected-sources.json').read_text());selected=[v for v in selected if not args.files or v['file'] in args.files]
 assert all(51<v['rank']<=118 for v in selected)
 pid={'pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),'started_utc':utc(),'args':vars(args),'source_order':[v['file'] for v in selected]}
 (out/(args.tag+'_pid.json')).write_text(json.dumps(pid,indent=2)+'\n');print(json.dumps({'event':'start',**pid}),flush=True)
 def checkpoint():(out/(args.tag+'_checkpoint.json')).write_text(json.dumps({'utc':utc(),'elapsed_seconds':time.monotonic()-start,'args':vars(args),'records':records},indent=2)+'\n')
 try:
  for item in selected:
   p=synth.ROOT/'sources/schemes'/item['file'];s=json.loads(p.read_text());sizes,maps=synth.load_maps(s);path=synth.HERE/'result'/('best_'+p.name);chosen=maps.copy()
   if path.exists():
    prior_bytes=path.read_bytes();prior=json.loads(prior_bytes);_,chosen=synth.load_maps(prior);(out/(args.tag+'_warm_'+p.name)).write_bytes(prior_bytes)
    assert synth.exact_check.factors(prior)==synth.exact_check.factors(s)
   record={'file':p.name,'format':s['n'],'rank':s['m'],'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'maps':{}};records.append(record)
   for k,n in sizes.items():
    f,r=maps[k];target=synth.vectors(n,f,r);base=synth.count(*chosen[k]);measure={'starting_best':base};record['maps'][k]=measure
    for dual in (False,True):
     if dual:gf,gr=synth.transpose(n,f,r,rng);gn=len(r)
     else:gf,gr=f,r;gn=n
     g=dag_search.grammar(gn,gf,gr,False);upper=synth.count(*chosen[k])-1
     # Calibration records the transpose operation-count shift on all36 source
     # maps. This is a constructive screening bound, not an exclusion theorem
     # for transpose schedules with additional cancellations.
     shift=len(r)-n if dual else 0;upper+=shift
     fr,info=solve(gn,g,upper,args.per_map,rng)
     info['transpose_screening_shift']=shift
     if dual and fr is not None:fr=synth.transpose(gn,*fr,rng)
     if fr is not None:
      assert synth.vectors(n,*fr)==target;cost=synth.count(*fr);info['primal_count']=cost
      if cost<synth.count(*chosen[k]):
       chosen[k]=fr;identity=synth.save_candidate(path,s,chosen,'acyclic MILP finite source grammar; seed '+str(args.seed))
       print(json.dumps({'event':'candidate','file':p.name,'cost':identity['additions'],'map':k,'dual':dual,'identity':identity}),flush=True)
     measure['dual' if dual else 'direct']=info;checkpoint()
   record['cost']=sum(synth.count(*x) for x in chosen.values());record['completed_utc']=utc();checkpoint()
   print(json.dumps({'event':'source_complete','file':p.name,'cost':record['cost']}),flush=True)
 except TimeoutError as e:print(json.dumps({'event':'time_cap','reason':str(e),'elapsed_seconds':time.monotonic()-start}),flush=True)
 finally:
  signal.alarm(0);checkpoint();(out/(args.tag+'_results.json')).write_text(json.dumps({'records':records,'args':vars(args),'elapsed_seconds':time.monotonic()-start,'ended_utc':utc()},indent=2)+'\n')
  print(json.dumps({'event':'finish','records':len(records),'elapsed_seconds':time.monotonic()-start}),flush=True)

if __name__=='__main__':main()
