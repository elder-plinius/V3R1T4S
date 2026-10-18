#!/usr/bin/env python3
"""Apply larger-rank reconstruction to the attributed105-product composition."""
import datetime,hashlib,json,os,random,resource,signal,sys,time
sys.dont_write_bytecode=True
import synth,dag_search,run_large,milp_search

def main():
 start=time.monotonic();seconds=420;seed=2026101410;rng=random.Random(seed);h=synth.HERE;out=h/'output'
 resource.setrlimit(resource.RLIMIT_CPU,(seconds+2,seconds+3));resource.setrlimit(resource.RLIMIT_NOFILE,(256,256))
 signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard SIGALRM cap')));signal.alarm(seconds)
 p=h/'input/composition_4x6x6_rank105_adds388.json';s=json.loads(p.read_text());assert s['m']==105 and s['n']==[4,6,6]
 assert synth.exact_check.verify(s)['additions']==388
 s['research_parent_source']='runs/2026-10-14-1241/attempts/large-circuits/input/composition_4x6x6_rank105_adds388.json'
 sizes,maps=synth.load_maps(s);chosen=maps.copy();records=[];path=h/'result/composition_optimized_4x6x6_rank105.json'
 pid={'pid':os.getpid(),'nice':os.getpriority(os.PRIO_PROCESS,0),'started_utc':run_large.utc(),'seed':seed,'hard_seconds':seconds,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 run_large.write(out/'composition-probe_pid.json',pid);print(json.dumps({'event':'start',**pid}),flush=True)
 snapshots=out/'code-snapshots/composition-probe';snapshots.mkdir(parents=True,exist_ok=True)
 for name in ('composition_probe.py','synth.py','dag_search.py','run_large.py','milp_search.py'):(snapshots/name).write_bytes((h/'code'/name).read_bytes())
 def checkpoint():run_large.write(out/'composition-probe_checkpoint.json',{'utc':run_large.utc(),'elapsed_seconds':time.monotonic()-start,'records':records,'cost':sum(synth.count(*fr) for fr in chosen.values())})
 def save(k,method,trial):
    identity=synth.save_candidate(path,s,chosen,'Strassen×2x3x3 composition signed grammar '+method+'; seed '+str(seed))
    assert synth.exact_check.factors(json.loads(path.read_text()))==synth.exact_check.factors(s)
    print(json.dumps({'event':'candidate','map':k,'method':method,'trial':trial,'cost':identity['additions'],'identity':identity}),flush=True)
 try:
  for k,n in sizes.items():
   f,r=maps[k];target=synth.vectors(n,f,r);record={'map':k,'source_cost':synth.count(f,r),'trials':[]};records.append(record)
   for kind in ('source','prefix','bridges','mag2'):
    for dual in (False,True):
     if dual:gf,gr=synth.transpose(n,f,r,rng);gn=len(r)
     else:gf,gr=f,r;gn=n
     if kind=='source':g=dag_search.grammar(gn,gf,gr,False);meta={}
     else:g,meta=run_large.enriched_grammar(gn,gf,gr,kind,rng)
     record[kind+('_dual_graph' if dual else '_direct_graph')]={'vectors':len(g[0]),'edges':sum(map(len,g[1])),'cancellation_edges':g[4],**meta}
     for trial in range(20):
      fr=dag_search.search(gn,g,rng,trial%4)
      if dual:fr=synth.transpose(gn,*fr,rng)
      assert synth.vectors(n,*fr)==target;cost=synth.count(*fr);record['trials'].append({'kind':kind,'dual':dual,'trial':trial,'cost':cost})
      if cost<synth.count(*chosen[k]):chosen[k]=fr;save(k,kind,trial)
      checkpoint()
     fr,info=milp_search.solve(gn,g,synth.count(*chosen[k])-1+(len(r)-n if dual else 0),5,rng)
     if fr is not None:
      if dual:fr=synth.transpose(gn,*fr,rng)
      assert synth.vectors(n,*fr)==target;cost=synth.count(*fr);info['primal_count']=cost
      if cost<synth.count(*chosen[k]):chosen[k]=fr;save(k,kind+'_milp',None)
     record[kind+('_dual_milp' if dual else '_direct_milp')]=info;checkpoint()
   record['best']=synth.count(*chosen[k]);checkpoint()
  save('all','complete',None)
 except TimeoutError as e:print(json.dumps({'event':'time_cap','reason':str(e),'elapsed_seconds':time.monotonic()-start}),flush=True)
 finally:
  signal.alarm(0);checkpoint();run_large.write(out/'composition-probe_results.json',{'records':records,'seed':seed,'source_sha256':pid['source_sha256'],'cost':sum(synth.count(*fr) for fr in chosen.values()),'elapsed_seconds':time.monotonic()-start,'ended_utc':run_large.utc()})
  print(json.dumps({'event':'finish','cost':sum(synth.count(*fr) for fr in chosen.values()),'elapsed_seconds':time.monotonic()-start}),flush=True)

if __name__=='__main__':main()
