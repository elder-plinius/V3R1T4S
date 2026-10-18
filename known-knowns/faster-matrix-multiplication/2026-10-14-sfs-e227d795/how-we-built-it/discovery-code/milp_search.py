#!/usr/bin/env python3
"""Select an acyclic integer linear circuit inside a frozen finite dictionary."""
import argparse,datetime,json,math,os,random,signal,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
import synth,followup

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--format',choices=['2x4x8','3x4x5'],required=True);ap.add_argument('--map',choices=['v','w'],default='v');ap.add_argument('--seed',type=int,default=101);ap.add_argument('--limit',type=int,default=180);ap.add_argument('--mag',type=int,default=2);ap.add_argument('--seconds',type=int,default=90);ap.add_argument('--dual',action='store_true');args=ap.parse_args()
 segment=json.loads((synth.HERE/'output/segment.json').read_text());now=datetime.datetime.now(datetime.timezone.utc)
 if now>=datetime.datetime.fromisoformat(segment['line_start_cutoff_utc']):raise SystemExit('new line cutoff')
 hard=min(args.seconds,int((datetime.datetime.fromisoformat(segment['deadline_utc'])-now).total_seconds()));tag=f'milp_{args.format}_{args.map}_seed{args.seed}'+('_dual' if args.dual else '');pid={'pid':os.getpid(),'started_utc':now.isoformat(),'hard_seconds':hard,'args':vars(args)};(synth.HERE/'output'/f'{tag}_pid.json').write_text(json.dumps(pid,indent=2)+'\n');signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard cap')));signal.alarm(hard)
 rng=random.Random(args.seed);pool=[]
 for folder in ['inputs','result']:
  for p in (synth.HERE/folder).glob('candidate_'+args.format+'_*.json'):pool.append(json.loads(p.read_text()))
 source=min(pool,key=synth.exact_check.addition_count);sizes,maps=synth.load_maps(source);k=args.map;n=sizes[k];original=maps[k];base=synth.count(*original);bank=[original]
 for s in pool:
  assert synth.exact_check.factors(s)==synth.exact_check.factors(source);bank.append(synth.load_maps(s)[1][k])
 for p in synth.source_list():
  if p.name.startswith(args.format+'_'):
   s=json.loads(p.read_text())
   if s['m']==source['m'] and synth.exact_check.factors(s)==synth.exact_check.factors(source):bank.append(synth.load_maps(s)[1][k])
 if args.dual:
  bank=[synth.transpose(n,*pair,rng) for pair in bank];original=bank[0];n=len(maps[k][1]);base=synth.count(*original)
 g=followup.enrich(n,bank,'bridges',args.limit,rng,args.mag);vals,es,tids,targets,cancelled=g;N=len(vals);edges=[(k,*e) for k in range(n,N) for e in es[k]];E=len(edges);D=N+E;size=2*N+E
 c=np.zeros(size);c[n:N]=1;lo=np.zeros(size);hi=np.ones(size);hi[D:]=base
 lo[:n]=1;lo[D:D+n]=0;hi[D:D+n]=0
 for i,sg in tids:
  if i is not None:lo[i]=1
 integrality=np.zeros(size);integrality[:D]=1
 rr=[];cc=[];vv=[];lower=[];upper=[]
 def constraint(coeffs,lb=-np.inf,ub=np.inf):
  row=len(lower)
  for col,value in coeffs.items():rr.append(row);cc.append(col);vv.append(value)
  lower.append(lb);upper.append(ub)
 incoming={i:[] for i in range(n,N)}
 for eid,(out,i,j,a,b) in enumerate(edges):
  y=N+eid;incoming[out].append(y)
  for parent in set([i,j]):
   constraint({y:1,parent:-1},ub=0)
   constraint({D+parent:1,D+out:-1,y:base+1},ub=base)
 for i,ys in incoming.items():
  coeffs={y:1 for y in ys};coeffs[i]=-1;constraint(coeffs,0,0)
  minimum_depth=max(1,int(math.ceil(math.log2(synth.norm(vals[i])))))
  constraint({D+i:1,i:-minimum_depth},lb=0)
  constraint({D+i:1,i:-base},ub=0)
 constraint({i:1 for i in range(n,N)},ub=base-1)
 A=coo_matrix((vv,(rr,cc)),shape=(len(lower),size)).tocsr();out={'pid':pid,'format':args.format,'map':k,'source_map_additions':base,'dictionary_nodes':N,'edge_choices':E,'cancellation_edges':cancelled,'rows':len(lower),'column_variables':size,'status':'solver pending'}
 # The saved source circuit is a known feasible control before the stricter
 # addition-budget row is imposed. Check every other constraint explicitly.
 lookup={v:i for i,v in enumerate(vals)};edgeids={e:i for i,e in enumerate(edges)};witness=np.zeros(size);witness[:n]=1
 raw=[tuple(int(i==j) for j in range(n)) for i in range(n)];known=set(range(n));depths={i:0 for i in range(n)}
 for rowno,row in enumerate(original[0]+original[1]):
  acc=None
  for rawindex,coefficient in row.items():
   term=tuple(coefficient*x for x in raw[rawindex])
   if acc is None:acc=term;continue
   ca,sa=synth.canonical(acc);cb,sb=synth.canonical(term);acc=synth.add(acc,term);cv,sg=synth.canonical(acc)
   if not any(cv):continue
   v=lookup[cv]
   if v in known:continue
   i,j=lookup[ca],lookup[cb];a,b=sg*sa,sg*sb
   if i>j:i,j,a,b=j,i,b,a
   eid=edgeids[(v,i,j,a,b)];witness[v]=1;witness[N+eid]=1;depths[v]=max(depths[i],depths[j])+1;witness[D+v]=depths[v];known.add(v)
  if rowno<len(original[0]):raw.append(acc if acc is not None else (0,)*n)
 control=A@witness;violations=[i for i,(value,lb,ub) in enumerate(zip(control,lower,upper)) if value<lb-1e-7 or value>ub+1e-7]
 assert not [i for i in violations if i!=len(lower)-1],('source-control constraint failure',violations)
 out['known_source_control_valid_without_strict_budget']=True;out['known_source_control_nodes']=int(sum(witness[n:N]));out['known_source_control_budget_violation']=bool(violations)
 (synth.HERE/'output'/f'{tag}_checkpoint.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
 try:
  result=milp(c,integrality=integrality,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(lower),np.array(upper)),options={'time_limit':max(1,hard-10),'mip_rel_gap':0,'disp':True})
  out.update({'status':int(result.status),'message':result.message,'objective':None if result.fun is None else float(result.fun),'dual_bound':None if getattr(result,'mip_dual_bound',None) is None else float(result.mip_dual_bound)})
  if result.x is not None:
   selected=[edges[eid] for eid in range(E) if result.x[N+eid]>0.5];circuit=synth.Circuit(n);refs={i:{i:1} for i in range(n)}
   while selected:
    ready=[e for e in selected if e[1] in refs and e[2] in refs]
    if not ready:raise ValueError('selected derivation is cyclic')
    for e in ready:
     v,i,j,a,b=e;refs[v]=circuit.materialize([(z,a*q) for z,q in refs[i].items()]+[(z,b*q) for z,q in refs[j].items()]);selected.remove(e)
   rows=[{} if i is None else {z:sg*q for z,q in refs[i].items()} for i,sg in tids];f,r=synth.prune(n,circuit.fresh,rows);assert synth.vectors(n,f,r)==targets;cost=synth.count(f,r);assert cost<base
   if args.dual:
    f,r=synth.transpose(n,f,r);assert synth.vectors(sizes[k],f,r)==synth.vectors(sizes[k],*maps[k]);cost=synth.count(f,r);assert cost<synth.count(*maps[k])
   maps[k]=(f,r);total=sum(synth.count(*v) for v in maps.values());artifact=synth.HERE/'result'/f'candidate_{args.format}_rank{source["m"]}_adds{total}_{tag}.json';ck=synth.save_candidate(artifact,source,maps,'finite dictionary MILP with acyclic signed sum choices');out['candidate']={'file':artifact.name,'map_additions':cost,**ck};print(json.dumps({'event':'improvement',**out['candidate']}),flush=True)
 except TimeoutError:out['status']='hard cap'
 finally:
  signal.alarm(0);out['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(synth.HERE/'output'/f'{tag}_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
