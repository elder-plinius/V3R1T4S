#!/usr/bin/env python3
"""Bounded direct/dual dependency search on preregistered fixed maps."""
import argparse, collections, copy, datetime, json, os, random, signal, time
import synth, dag_search

def key(s): return 'x'.join(map(str,s['n']))

def edge_graph(vals,targets):
    index={v:i for i,v in enumerate(vals)}; edges=[[] for _ in vals]; cancelled=0
    for i,v in enumerate(vals):
        for j in range(i,len(vals)):
            for s in (1,-1):
                cv,sg=synth.canonical(synth.add(v,vals[j],s)); k=index.get(cv)
                if k is None or k in (i,j): continue
                edges[k].append((i,j,sg,sg*s))
                if any(a and b and a*s*b<0 for a,b in zip(v,vals[j])): cancelled+=1
    targetids=[]
    for t in targets:
        cv,sg=synth.canonical(t); targetids.append((index.get(cv),sg))
    return vals,edges,targetids,targets,cancelled

def enrich(n,maps,stage,limit,rng,mag):
    base=dag_search.grammar(n,*maps[0],False); vals=base[0][:]; seen=set(vals); targets=base[3]
    if stage in ('merge','targetdiff','bridges'):
        for f,r in maps[1:]:
            for v in dag_search.grammar(n,f,r,False)[0]:
                if v not in seen: vals.append(v); seen.add(v)
    if stage in ('targetdiff','bridges'):
        extras=collections.Counter()
        for i,t in enumerate(targets):
            for w in targets[i+1:]:
                for s in (1,-1):
                    v,sg=synth.canonical(synth.add(t,w,s))
                    if v not in seen and any(v) and synth.norm(v)<=4 and max(map(abs,v))<=mag:
                        extras[v]+=1
        choices=sorted(extras,key=lambda v:(extras[v]/(1+synth.norm(v)),rng.random()),reverse=True)
        target_limit=limit if stage=='targetdiff' else max(len(vals),int(limit*0.7))
        for v in choices:
            if len(vals)>=target_limit: break
            vals.append(v); seen.add(v)
    if stage=='bridges':
        # Count exact exits into old nodes. Frequent exits indicate shared use.
        exits=collections.Counter()
        for t in vals:
            for w in vals:
                for s in (1,-1):
                    v,sg=synth.canonical(synth.add(t,w,s))
                    if v not in seen and any(v) and max(map(abs,v))<=mag:
                        exits[v]+=1
        # Every new candidate is an actual sum of two existing dictionary nodes.
        candidates=[]
        for i,t in enumerate(vals):
            for w in vals[i+1:]:
                for s in (1,-1):
                    v,sg=synth.canonical(synth.add(t,w,s))
                    if v in seen or not any(v) or max(map(abs,v))>mag: continue
                    support=synth.norm(v)
                    candidates.append((exits[v]/(1+support)**0.35,rng.random(),v))
        candidates.sort(reverse=True)
        for score,noise,v in candidates:
            if len(vals)>=limit: break
            if v not in seen: vals.append(v); seen.add(v)
    return edge_graph(vals,targets)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--stage',choices=['baseline','merge','targetdiff','bridges'],default='baseline')
    ap.add_argument('--seconds',type=int,default=180); ap.add_argument('--seed',type=int,default=17); ap.add_argument('--trials',type=int,default=32)
    ap.add_argument('--limit',type=int,default=240); ap.add_argument('--mag',type=int,default=1); ap.add_argument('--shared',action='store_true'); ap.add_argument('--warm',action='store_true'); args=ap.parse_args()
    segment=json.loads((synth.HERE/'output/segment.json').read_text()); now=datetime.datetime.now(datetime.timezone.utc)
    cutoff=datetime.datetime.fromisoformat(segment['line_start_cutoff_utc']); end=datetime.datetime.fromisoformat(segment['deadline_utc'])
    if now>=cutoff: raise SystemExit('new line cutoff reached')
    hard=min(args.seconds,int((end-now).total_seconds())); start=time.monotonic(); rng=random.Random(args.seed)
    tag=f"{args.stage}_seed{args.seed}_mag{args.mag}"+('_shared' if args.shared else '')+('_warm' if args.warm else ''); records=[]; best={}; circuits={}; seedmaps={}; graphs={}
    search_fn=dag_search.shared_search if args.shared else dag_search.search
    pid={'pid':os.getpid(),'started_utc':now.isoformat(),'hard_seconds':hard,'args':vars(args)}
    (synth.HERE/'output'/f'{tag}_pid.json').write_text(json.dumps(pid,indent=2)+'\n')
    signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard cap'))); signal.alarm(hard)
    inputs=[p for p in (synth.HERE/'inputs').glob('candidate_*.json') if p.name.startswith(('candidate_2x4x8_','candidate_3x4x5_'))]
    assert all(json.loads(p.read_text())['n'] not in ([2,5,5],[2,5,6]) for p in inputs)
    try:
      for p in inputs:
        s=json.loads(p.read_text()); fmt=key(s); others=[]
        if args.warm:
            for rp in (synth.HERE/'result').glob('candidate_'+fmt+'_*.json'):
                obj=json.loads(rp.read_text())
                assert obj['m']==s['m'] and synth.exact_check.factors(obj)==synth.exact_check.factors(s)
                others.append(obj)
            if others:s=min([s]+others,key=synth.exact_check.addition_count)
        sizes,m=synth.load_maps(s); best[fmt]=synth.exact_check.addition_count(s); circuits[fmt]=(s,sizes,m)
        bank={k:[m[k]] for k in m}
        for obj in others:
            om=synth.load_maps(obj)[1]
            for k in bank:bank[k].append(om[k])
        for sp in synth.source_list():
            if not sp.name.startswith(fmt+'_'): continue
            orig=json.loads(sp.read_text())
            if orig['m']!=s['m'] or synth.exact_check.factors(orig)!=synth.exact_check.factors(s): continue
            om=synth.load_maps(orig)[1]
            for k in bank: bank[k].append(om[k])
        seedmaps[fmt]=bank
        graphs[fmt]={}
        for k,n in sizes.items():
            if (fmt in ('2x4x8','2x5x6') and k in ('u','w')) or (fmt=='3x4x5' and k=='u'):
                # Fixed U maps attain the distinct target lower bound. Fixed W
                # maps attain its transposed counterpart, so retain them.
                graphs[fmt][k]=None
                print(json.dumps({'event':'skip_fixed_bound','format':fmt,'map':k,'cost':synth.count(*m[k])}),flush=True)
                continue
            g=enrich(n,bank[k],args.stage,args.limit,rng,args.mag)
            dualbank=[synth.transpose(n,*pair,rng) for pair in bank[k]]
            dg=enrich(len(m[k][1]),dualbank,args.stage,args.limit,rng,args.mag)
            graphs[fmt][k]=(g,dg)
            print(json.dumps({'event':'dictionary','format':fmt,'map':k,'direct_nodes':len(g[0]),'dual_nodes':len(dg[0]),'direct_cancellation_edges':g[4],'dual_cancellation_edges':dg[4]}),flush=True)
      cycle=0
      while time.monotonic()-start<hard:
       cycle+=1
       for fmt,(s,sizes,m) in list(circuits.items()):
        selected=m.copy(); measurements={}
        for k,n in sizes.items():
            if graphs[fmt][k] is None:
                measurements[k]={'fixed_bound_cost':synth.count(*selected[k])}
                continue
            g,dg=graphs[fmt][k]; base=synth.count(*selected[k]); measured={'source':base,'direct':base,'dual':base}
            for trial in range(args.trials):
                f,r=search_fn(n,g,rng,(trial+cycle)%4); cost=synth.count(f,r)
                if cost<measured['direct']: measured['direct']=cost
                if cost<synth.count(*selected[k]): selected[k]=(f,r)
                df,dr=search_fn(len(m[k][1]),dg,rng,(trial+cycle)%4); f,r=synth.transpose(len(m[k][1]),df,dr,rng)
                assert synth.vectors(n,f,r)==g[3]; cost=synth.count(f,r)
                if cost<measured['dual']: measured['dual']=cost
                if cost<synth.count(*selected[k]): selected[k]=(f,r)
            measurements[k]=measured
        total=sum(synth.count(*c) for c in selected.values()); rec={'cycle':cycle,'format':fmt,'rank':s['m'],'cost':total,'maps':measurements,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}; records.append(rec)
        if total<best[fmt]:
            best[fmt]=total; artifact=synth.HERE/'result'/f'candidate_{fmt}_rank{s["m"]}_adds{total}_{tag}.json'
            ck=synth.save_candidate(artifact,s,selected,f'{tag} enriched signed AND/OR dictionary')
            assert synth.exact_check.factors(json.loads(artifact.read_text()))==synth.exact_check.factors(s)
            print(json.dumps({'event':'improvement','artifact':artifact.name,**rec,'identity':ck}),flush=True)
            circuits[fmt]=(s,sizes,selected)
        (synth.HERE/'output'/f'{tag}_checkpoint.json').write_text(json.dumps({'elapsed_seconds':time.monotonic()-start,'bests':best,'records':records,'pid':pid},indent=2)+'\n')
    except TimeoutError as e: print(json.dumps({'event':'time_cap','elapsed_seconds':time.monotonic()-start,'records':len(records),'reason':str(e)}),flush=True)
    finally:
        signal.alarm(0)
        (synth.HERE/'output'/f'{tag}_results.json').write_text(json.dumps({'bests':best,'records':records,'pid':pid},indent=2)+'\n')

if __name__=='__main__': main()
