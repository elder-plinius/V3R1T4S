#!/usr/bin/env python3
"""Selected-source larger-rank signed grammar, direct and reverse-mode probes.

Preserves full integer factors, freezes source order and seed, saves improvements
after each map, and checkpoints even if the global SIGALRM is reached.
"""
import argparse, collections, copy, datetime, hashlib, json, os, pathlib, random, resource, signal, time
import synth, dag_search

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(path,data):
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data,indent=2)+'\n'); tmp.replace(path)

def enriched_grammar(n,f,r,kind,rng):
    """Only enrich dictionaries after the broad bridge probe proved expensive.

    Bridges receive the sum of improvements in the existing constructive
    residual bound; retain at most64 with score>1. Prefix enrichment preserves
    original vectors and adds one random order of each source sum.
    """
    vals,oldedges,targetids,targets,oldcancel=dag_search.grammar(n,f,r,False)
    index={v:i for i,v in enumerate(vals)}; added=[]
    def insert(v):
        cv,sg=synth.canonical(v)
        if any(cv) and cv not in index:
            index[cv]=len(vals);vals.append(cv);added.append(cv)
    if kind=='union':
        family_sizes={}
        for member in ('prefix','prefix','prefix','bridges','mag2'):
            family,meta=enriched_grammar(n,f,r,member,rng)
            before=len(vals)
            for v in family[0]:insert(v)
            family_sizes[member]=family_sizes.get(member,0)+len(vals)-before
    elif kind=='prefix':
        originals=[tuple(int(i==j) for j in range(n)) for i in range(n)]
        for row in f:
            terms=list(row.items()); rng.shuffle(terms);acc=(0,)*n
            for i,c in terms: acc=synth.add(acc,originals[i],c);insert(acc)
            originals.append(acc)
        for row in r:
            terms=list(row.items());rng.shuffle(terms);acc=(0,)*n
            for i,c in terms: acc=synth.add(acc,originals[i],c);insert(acc)
    else:
        pool=collections.Counter()
        parents=vals if kind=='mag2' else targets
        for i,v in enumerate(parents):
            for w in parents[i:] if kind=='mag2' else parents[i+1:]:
                for sign in (1,-1):
                    cv,sg=synth.canonical(synth.add(v,w,sign))
                    magnitude=max(map(abs,cv))
                    admissible=(magnitude==2 and synth.norm(cv)<=5) if kind=='mag2' else (magnitude<=1 and synth.norm(cv)<=4)
                    if cv not in index and any(cv) and admissible:pool[cv]+=1
        # Full target vectors are grammar states, not free prepared values.
        # Allowing each target as its own reference gives every bound zero and
        # makes a bridge screen vacuous. Exclude all target states here.
        targetset={synth.canonical(t)[0] for t in targets}
        reference=[v for i,v in enumerate(vals) if i<n or v not in targetset]
        distances=[min([max(0,synth.norm(t)-1)]+[synth.norm(synth.add(t,v,s)) for v in reference for s in (1,-1)]) for t in targets]
        scored=[]
        for cv,uses in pool.items():
            score=sum(max(0,d-min(synth.norm(synth.add(t,cv,s)) for s in (1,-1))) for d,t in zip(distances,targets))
            if score>1: scored.append((score,uses,-synth.norm(cv),cv))
        scored.sort(reverse=True)
        for score,uses,negcost,cv in scored[:64]:insert(cv)
    edges=[[] for _ in vals];cancelled=0
    for i,v in enumerate(vals):
        for j in range(i,len(vals)):
            for s in (1,-1):
                cv,sg=synth.canonical(synth.add(v,vals[j],s)); k=index.get(cv)
                if k is None or k in (i,j):continue
                edges[k].append((i,j,sg,sg*s))
                if any(a and b and a*s*b<0 for a,b in zip(v,vals[j])):cancelled+=1
    metadata={'base_vectors':len(vals)-len(added),'added_vectors':len(added),'added_dictionary':added}
    if kind=='union':metadata['family_added_vectors']=family_sizes
    return (vals,edges,targetids,targets,cancelled),metadata

def add_dictionary_vectors(g,extra):
    """Permit cross-family binary derivations without treating any state as free."""
    vals=list(g[0]);index={v:i for i,v in enumerate(vals)};before=len(vals)
    for v in extra:
        cv,sg=synth.canonical(v)
        if any(cv) and cv not in index:index[cv]=len(vals);vals.append(cv)
    edges=[[] for _ in vals];cancelled=0
    for i,v in enumerate(vals):
        for j in range(i,len(vals)):
            for s in (1,-1):
                cv,sg=synth.canonical(synth.add(v,vals[j],s));k=index.get(cv)
                if k is None or k in (i,j):continue
                edges[k].append((i,j,sg,sg*s))
                if any(a and b and a*s*b<0 for a,b in zip(v,vals[j])):cancelled+=1
    return (vals,edges,g[2],g[3],cancelled),len(vals)-before

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--tag',required=True)
    ap.add_argument('--seconds',type=int,default=300)
    ap.add_argument('--trials',type=int,default=3)
    ap.add_argument('--seed',type=int,default=20261014)
    ap.add_argument('--mode',choices=['probe','grammar','extra','bridges','prefix','mag2','roundtrip','cycles','difference'],default='probe')
    ap.add_argument('--files',nargs='*')
    args=ap.parse_args(); start=time.monotonic(); rng=random.Random(args.seed)
    snapshots=synth.HERE/'output/code-snapshots'/args.tag;snapshots.mkdir(parents=True,exist_ok=True)
    code_hashes={}
    for name in ('run_large.py','synth.py','dag_search.py'):
        content=(synth.HERE/'code'/name).read_bytes();(snapshots/name).write_bytes(content)
        code_hashes[name]=hashlib.sha256(content).hexdigest()
    selected=json.loads((synth.HERE.parents[1]/'data/selected-sources.json').read_text())
    segment=json.loads((synth.HERE.parents[1]/'data/segment.json').read_text())
    deadline=datetime.datetime.fromisoformat(segment['deadline_utc'])
    seconds=min(args.seconds,max(1,int((deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds())-10))
    resource.setrlimit(resource.RLIMIT_NOFILE,(256,256))
    resource.setrlimit(resource.RLIMIT_CPU,(seconds+2,seconds+3))
    try: resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
    except (ValueError,OSError): pass
    signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard SIGALRM cap')))
    signal.alarm(seconds)
    out=synth.HERE/'output'; records=[]; candidates=[]
    selected=[v for v in selected if not args.files or v['file'] in args.files]
    assert all(51<v['rank']<=118 for v in selected)
    bars=json.loads((synth.ROOT/'sources/strongest-addition-bars.json').read_text())
    updated=synth.HERE/'output/updated-bars.json'
    if updated.exists():
        for key,value in json.loads(updated.read_text()).items():
            if type(value) is int: bars[key]=min(bars.get(key,10**9),value)
    pid={'pid':os.getpid(),'started_utc':utc(),'hard_seconds':seconds,'nice':os.getpriority(os.PRIO_PROCESS,0),'args':vars(args),'source_order':[v['file'] for v in selected],'code_hashes':code_hashes,'resource_caps':{'cpu_seconds':seconds+3,'open_files':256,'address_space_bytes':1536*1024**2}}
    write(out/(args.tag+'_pid.json'),pid); print(json.dumps({'event':'start',**pid}),flush=True)
    def checkpoint(event):
        write(out/(args.tag+'_checkpoint.json'),{'utc':utc(),'elapsed_seconds':time.monotonic()-start,'args':vars(args),'event':event,'records':records,'candidates':candidates})
    try:
      for item in selected:
        source_path=synth.ROOT/'sources/schemes'/item['file']; s=json.loads(source_path.read_text())
        sizes,maps=synth.load_maps(s); chosen=maps.copy(); measures={}
        previous=synth.HERE/'result'/('best_'+source_path.name)
        if previous.exists():
            prior_bytes=previous.read_bytes(); prior=json.loads(prior_bytes); _,prior_maps=synth.load_maps(prior)
            warm=synth.HERE/'output'/(args.tag+'_warm_'+source_path.name)
            warm.write_bytes(prior_bytes)
            assert synth.exact_check.factors(s)==synth.exact_check.factors(prior)
            chosen={k:min((maps[k],prior_maps[k]),key=lambda fr:synth.count(*fr)) for k in maps}
        base=synth.exact_check.addition_count(s)
        key='x'.join(map(str,s['n'])); bar=bars.get(key)
        record={'file':source_path.name,'format':s['n'],'rank':s['m'],'source_cost':base,'screening_bar':bar,'seed':args.seed,'mode':args.mode,'maps':measures,'source_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest()}
        records.append(record)
        if previous.exists(): record['warm_start_sha256']=hashlib.sha256(prior_bytes).hexdigest()
        def save(method,k,trial):
            total=sum(synth.count(*fr) for fr in chosen.values()); record['cost']=total
            if total<base:
                identity=synth.save_candidate(previous,s,chosen,'larger-rank '+method+'; seed '+str(args.seed))
                assert synth.exact_check.factors(s)==synth.exact_check.factors(json.loads(previous.read_text()))
                event={'event':'candidate','file':source_path.name,'artifact':str(previous.relative_to(synth.ROOT)),'cost':total,'screening_bar':bar,'below_screening_bar':bar is not None and total<bar,'method':method,'map':k,'trial':trial,'utc':utc(),'identity':identity}
                candidates.append(event); print(json.dumps(event),flush=True)
            checkpoint({'file':source_path.name,'map':k,'trial':trial,'method':method})
        for k,n in sizes.items():
            f,r=maps[k]; target=synth.vectors(n,f,r); m={'source':synth.count(f,r),'starting_best':synth.count(*chosen[k]),'trials':[]}; measures[k]=m
            def score(name,fr,trial):
                assert synth.vectors(n,*fr)==target
                cost=synth.count(*fr); m['trials'].append({'method':name,'trial':trial,'cost':cost})
                if cost<synth.count(*chosen[k]):
                    chosen[k]=fr; save(name,k,trial)
                else: checkpoint({'file':source_path.name,'map':k,'trial':trial,'method':name,'cost':cost})
            if args.mode in ('probe','grammar','extra','bridges','prefix','mag2'):
                graph_start=time.monotonic()
                if args.mode in ('bridges','prefix','mag2'):
                    g,metadata=enriched_grammar(n,f,r,args.mode,rng);m['direct_enrichment']=metadata
                else:g=dag_search.grammar(n,f,r,args.mode=='extra')
                m['direct_graph']={'vectors':len(g[0]),'edges':sum(map(len,g[1])),'cancellation_edges':g[4],'build_seconds':time.monotonic()-graph_start}
                for trial in range(args.trials): score('direct_'+args.mode,dag_search.search(n,g,rng,trial%4),trial)
                df,dr=synth.transpose(n,f,r,rng)
                graph_start=time.monotonic()
                if args.mode in ('bridges','prefix','mag2'):
                    dg,metadata=enriched_grammar(len(r),df,dr,args.mode,rng);m['dual_enrichment']=metadata
                else:dg=dag_search.grammar(len(r),df,dr,args.mode=='extra')
                m['dual_graph']={'vectors':len(dg[0]),'edges':sum(map(len,dg[1])),'cancellation_edges':dg[4],'build_seconds':time.monotonic()-graph_start}
                for trial in range(args.trials):
                    da,db=dag_search.search(len(r),dg,rng,trial%4)
                    score('dual_'+args.mode,synth.transpose(len(r),da,db,rng),trial)
            if args.mode in ('probe','roundtrip'):
                for trial in range(args.trials):
                    tf,tr=synth.transpose(n,f,r,rng); rf,rr=synth.transpose(len(r),tf,tr,rng)
                    score('roundtrip',(rf,rr),trial)
            if args.mode=='cycles':
                cf,cr=chosen[k]
                for trial in range(args.trials):
                    tf,tr=synth.transpose(n,cf,cr,rng);cf,cr=synth.transpose(len(r),tf,tr,rng)
                    score('iterated_double_transpose',(cf,cr),trial)
            if args.mode in ('probe','difference'):
                for trial in range(args.trials):
                    score('difference',synth.diff_tree(target,n,rng),trial)
                    tf,tr=synth.diff_tree(synth.matrix_transpose(target,n),len(r),rng)
                    score('dual_difference',synth.transpose(len(r),tf,tr,rng),trial)
            m['best']=synth.count(*chosen[k]); checkpoint({'event':'map_complete','file':source_path.name,'map':k})
        save('completed_'+args.mode,'all',args.trials)
        record['completed_utc']=utc(); print(json.dumps({'event':'source_complete',**record}),flush=True)
    except TimeoutError as e:
        print(json.dumps({'event':'time_cap','utc':utc(),'elapsed_seconds':time.monotonic()-start,'reason':str(e)}),flush=True)
    finally:
        signal.alarm(0); checkpoint({'event':'finished'})
        write(out/(args.tag+'_results.json'),{'started_utc':pid['started_utc'],'ended_utc':utc(),'elapsed_seconds':time.monotonic()-start,'args':vars(args),'records':records,'candidates':candidates})
        print(json.dumps({'event':'finish','tag':args.tag,'records':len(records),'candidates':len(candidates),'elapsed_seconds':time.monotonic()-start}),flush=True)

if __name__=='__main__': main()
