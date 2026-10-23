#!/usr/bin/env python3
"""Combine empirically justified finite grammar families, then reconstruct."""
import argparse,datetime,hashlib,json,os,random,resource,signal,sys,time
sys.dont_write_bytecode=True
import synth,dag_search,run_large,milp_search

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--tag',default='union-probe');ap.add_argument('--seconds',type=int,default=660);ap.add_argument('--per-map',type=float,default=5);ap.add_argument('--trials',type=int,default=8);ap.add_argument('--seed',type=int,default=2026101411);ap.add_argument('--rounds',type=int,default=1);ap.add_argument('--files',nargs='*');ap.add_argument('--warm-grammar',action='store_true');args=ap.parse_args()
 start=time.monotonic();rng=random.Random(args.seed);h=synth.HERE;out=h/'output';records=[]
 segment=json.loads((h.parents[1]/'data/segment.json').read_text());cutoff=datetime.datetime.fromisoformat(segment['line_start_cutoff_utc']);seconds=min(args.seconds,max(1,int((cutoff-datetime.datetime.now(datetime.timezone.utc)).total_seconds())))
 resource.setrlimit(resource.RLIMIT_CPU,(seconds+2,seconds+3));resource.setrlimit(resource.RLIMIT_NOFILE,(256,256))
 try:resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
 except (OSError,ValueError):pass
 signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard SIGALRM cap')));signal.alarm(seconds)
 selected=json.loads((h.parents[1]/'data/selected-sources.json').read_text());selected=[v for v in selected if not args.files or v['file'] in args.files];assert all(51<v['rank']<=118 for v in selected)
 jobs=[(v['file'],synth.ROOT/'sources/schemes'/v['file'],h/'result'/('best_'+v['file'])) for v in selected if v['format']!=[4,6,6]]
 jobs.append(('composition_4x6x6_rank105',h/'input/composition_4x6x6_rank105_adds388.json',h/'result/composition_optimized_4x6x6_rank105.json'))
 pid={'pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),'started_utc':run_large.utc(),'hard_seconds':seconds,'args':vars(args),'source_order':[v[0] for v in jobs]};run_large.write(out/(args.tag+'_pid.json'),pid);print(json.dumps({'event':'start',**pid}),flush=True)
 snapshots=out/'code-snapshots'/args.tag;snapshots.mkdir(parents=True,exist_ok=True)
 for name in ('union_search.py','synth.py','dag_search.py','run_large.py','milp_search.py'):(snapshots/name).write_bytes((h/'code'/name).read_bytes())
 def checkpoint():run_large.write(out/(args.tag+'_checkpoint.json'),{'utc':run_large.utc(),'elapsed_seconds':time.monotonic()-start,'args':vars(args),'records':records})
 try:
  for rnd in range(args.rounds):
   for label,source_path,result_path in jobs:
    s=json.loads(source_path.read_text());sizes,maps=synth.load_maps(s);chosen=maps.copy()
    if result_path.exists():
     warm=result_path.read_bytes();_,chosen=synth.load_maps(json.loads(warm));(out/(args.tag+'_round'+str(rnd)+'_warm_'+result_path.name)).write_bytes(warm)
     assert synth.exact_check.factors(s)==synth.exact_check.factors(json.loads(warm))
    if label.startswith('composition_'):s['research_parent_source']=str(source_path.relative_to(synth.ROOT))
    record={'round':rnd,'file':label,'format':s['n'],'rank':s['m'],'source_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),'maps':{}};records.append(record)
    def save(k,method,trial):
     identity=synth.save_candidate(result_path,s,chosen,'union signed grammar '+method+'; seed '+str(args.seed)+' round '+str(rnd));assert synth.exact_check.factors(json.loads(result_path.read_text()))==synth.exact_check.factors(s)
     print(json.dumps({'event':'candidate','file':label,'round':rnd,'map':k,'method':method,'trial':trial,'cost':identity['additions'],'identity':identity}),flush=True)
    for k,n in sizes.items():
     f,r=maps[k];target=synth.vectors(n,f,r);m={'starting_best':synth.count(*chosen[k]),'trials':[]};record['maps'][k]=m
     for dual in (False,True):
      if dual:gf,gr=synth.transpose(n,f,r,rng);gn=len(r)
      else:gf,gr=f,r;gn=n
      g,meta=run_large.enriched_grammar(gn,gf,gr,'union',rng)
      if args.warm_grammar:
       wf,wr=chosen[k]
       if dual:wf,wr=synth.transpose(n,wf,wr,rng)
       wg=dag_search.grammar(gn,wf,wr,False);assert wg[3]==g[3]
       g,added=run_large.add_dictionary_vectors(g,wg[0]);meta['warm_dictionary_added_vectors']=added
      meta.update({'vectors':len(g[0]),'edges':sum(map(len,g[1])),'cancellation_edges':g[4]});m['dual_graph' if dual else 'direct_graph']=meta
      for trial in range(args.trials):
       fr=dag_search.search(gn,g,rng,trial%4)
       if dual:fr=synth.transpose(gn,*fr,rng)
       assert synth.vectors(n,*fr)==target;cost=synth.count(*fr);m['trials'].append({'dual':dual,'trial':trial,'cost':cost})
       if cost<synth.count(*chosen[k]):chosen[k]=fr;save(k,'dual' if dual else 'direct',trial)
       checkpoint()
      fr,info=milp_search.solve(gn,g,synth.count(*chosen[k])-1+(len(r)-n if dual else 0),args.per_map,rng)
      if fr is not None:
       if dual:fr=synth.transpose(gn,*fr,rng)
       assert synth.vectors(n,*fr)==target;cost=synth.count(*fr);info['primal_count']=cost
       if cost<synth.count(*chosen[k]):chosen[k]=fr;save(k,'dual_milp' if dual else 'direct_milp',None)
      m['dual_milp' if dual else 'direct_milp']=info;checkpoint()
     m['best']=synth.count(*chosen[k]);checkpoint()
    record['cost']=sum(synth.count(*fr) for fr in chosen.values());record['completed_utc']=run_large.utc();checkpoint();print(json.dumps({'event':'source_complete','file':label,'round':rnd,'cost':record['cost']}),flush=True)
 except TimeoutError as e:print(json.dumps({'event':'time_cap','reason':str(e),'elapsed_seconds':time.monotonic()-start}),flush=True)
 finally:
  signal.alarm(0);checkpoint();run_large.write(out/(args.tag+'_results.json'),{'records':records,'args':vars(args),'elapsed_seconds':time.monotonic()-start,'ended_utc':run_large.utc()});print(json.dumps({'event':'finish','records':len(records),'elapsed_seconds':time.monotonic()-start}),flush=True)

if __name__=='__main__':main()
