#!/usr/bin/env python3
"""Search a signed vector AND/OR grammar, permitting cancelled parent support."""
import argparse, collections, json, os, pathlib, random, signal, sys, time
import synth

def grammar(n,fresh,rows,extra=False):
    vals=[]; index={}
    def insert(v):
        cv,sg=synth.canonical(v)
        if not any(cv): return None,sg
        if cv not in index: index[cv]=len(vals); vals.append(cv)
        return index[cv],sg
    basis=[tuple(int(i==j) for j in range(n)) for i in range(n)]
    for v in basis: insert(v)
    originals=basis[:]
    for r in fresh+rows:
        acc=(0,)*n
        for i,c in r.items():
            acc=synth.add(acc,originals[i],c); insert(acc)
        if r in fresh: originals.append(acc)
    targets=synth.vectors(n,fresh,rows)
    targetids=[insert(v) for v in targets]
    if extra:
        # Complete target differences form a distinct cancellation neighborhood.
        for i,v in enumerate(targets):
            for w in targets[i+1:]:
                for s in (1,-1):
                    d=synth.add(v,w,s)
                    if synth.norm(d)<=4 and max(map(abs,d),default=0)<=1: insert(d)
    edges=[[] for _ in vals]; cancelled=0
    for i,v in enumerate(vals):
        for j in range(i,len(vals)):
            for s in (1,-1):
                cv,sg=synth.canonical(synth.add(v,vals[j],s))
                k=index.get(cv)
                if k is None or k in (i,j): continue
                edges[k].append((i,j,sg,sg*s))
                if any(a and b and a*s*b<0 for a,b in zip(v,vals[j])): cancelled+=1
    return vals,edges,targetids,targets,cancelled

def search(n,g,rng,ordering):
    vals,edges,targetids,targets,cancelled=g
    circuit=synth.Circuit(n); available={i:{i:1} for i in range(n)}
    needed=set(i for i,s in targetids if i is not None)
    while needed-available.keys():
        dist=[0 if i in available else 10**9 for i in range(len(vals))]
        parent={}; changed=True
        for iteration in range(len(vals)):
            if not changed: break
            changed=False
            ids=list(range(n,len(vals))); rng.shuffle(ids)
            for k in ids:
                if k in available: continue
                choices=[]; best=dist[k]
                for i,j,a,b in edges[k]:
                    cost=dist[i]+dist[j]+1
                    if cost<best: best=cost; choices=[(i,j,a,b)]
                    elif cost==best: choices.append((i,j,a,b))
                if choices:
                    if best<dist[k]: changed=True
                    dist[k]=best; parent[k]=rng.choice(choices)
        todo=list(needed-available.keys()); rng.shuffle(todo)
        if ordering==0: k=min(todo,key=lambda i:dist[i])
        elif ordering==1: k=max(todo,key=lambda i:dist[i])
        elif ordering==2: k=rng.choice(todo)
        else:
            uses=collections.Counter(i for es in edges for e in es for i in e[:2])
            k=min(todo,key=lambda i:dist[i]/(1+uses[i])**0.5)
        if dist[k]>=10**9: raise ValueError('unreachable source target')
        active=set()
        def build(k):
            if k in available: return available[k]
            if k in active: raise ValueError('cyclic derivation')
            active.add(k); i,j,a,b=parent[k]
            if not (dist[i]<dist[k] and dist[j]<dist[k]): raise ValueError('nondecreasing derivation')
            p=build(i); q=build(j)
            terms=[(z,a*c) for z,c in p.items()]+[(z,b*c) for z,c in q.items()]
            available[k]=circuit.materialize(terms,rng); active.remove(k)
            return available[k]
        build(k)
    out=[{} if k is None else {i:s*c for i,c in available[k].items()} for k,s in targetids]
    f,r=synth.prune(n,circuit.fresh,out)
    assert synth.vectors(n,f,r)==targets
    return f,r

def shared_search(n,g,rng,ordering):
    """Count the union of dependency nodes instead of summing tree costs."""
    vals,edges,targetids,targets,cancelled=g
    circuit=synth.Circuit(n); available={i:{i:1} for i in range(n)}
    needed=set(i for i,s in targetids if i is not None)
    while needed-available.keys():
        dependencies=[frozenset() if i in available else None for i in range(len(vals))]
        dist=[0 if i in available else 10**9 for i in range(len(vals))]; parent={}
        for iteration in range(len(vals)):
            changed=False; ids=list(range(n,len(vals))); rng.shuffle(ids)
            for k in ids:
                if k in available: continue
                best=dist[k]; choices=[]
                for i,j,a,b in edges[k]:
                    if dependencies[i] is None or dependencies[j] is None: continue
                    deps=dependencies[i]|dependencies[j]
                    if k in deps: continue
                    deps=deps|{k}; cost=len(deps)
                    if cost<best: best=cost; choices=[((i,j,a,b),deps)]
                    elif cost==best: choices.append(((i,j,a,b),deps))
                if choices:
                    if best<dist[k]: changed=True
                    edge,deps=rng.choice(choices); dist[k]=best; parent[k]=edge; dependencies[k]=deps
            if not changed: break
        todo=list(needed-available.keys()); rng.shuffle(todo)
        if ordering==0:k=min(todo,key=lambda i:dist[i])
        elif ordering==1:k=max(todo,key=lambda i:dist[i])
        elif ordering==2:k=rng.choice(todo)
        else:
            uses=collections.Counter(i for es in edges for e in es for i in e[:2]); k=min(todo,key=lambda i:dist[i]/(1+uses[i])**0.5)
        if dist[k]>=10**9: raise ValueError('unreachable shared dependency')
        active=set()
        def build(k):
            if k in available:return available[k]
            if k in active:raise ValueError('cyclic shared dependency')
            active.add(k); i,j,a,b=parent[k]
            p=build(i);q=build(j)
            available[k]=circuit.materialize([(z,a*c) for z,c in p.items()]+[(z,b*c) for z,c in q.items()],rng)
            active.remove(k);return available[k]
        build(k)
    out=[{} if k is None else {i:s*c for i,c in available[k].items()} for k,s in targetids]
    f,r=synth.prune(n,circuit.fresh,out);assert synth.vectors(n,f,r)==targets
    return f,r

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seconds',type=int,default=300); ap.add_argument('--trials',type=int,default=20)
    ap.add_argument('--seed',type=int,default=1); ap.add_argument('--max-rank',type=int,default=51); ap.add_argument('--extra',action='store_true'); args=ap.parse_args()
    start=time.monotonic(); rng=random.Random(args.seed); entries=[]; bests={}; jobs=[]
    (synth.HERE/'output'/'dag_pid.json').write_text(json.dumps({'pid':os.getpid(),'started_utc':time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime()),'hard_seconds':args.seconds,'args':vars(args)})+'\n')
    signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard time cap'))); signal.alarm(args.seconds)
    for p in synth.source_list():
        s=json.loads(p.read_text())
        if s['m']<=args.max_rank: jobs.append((p,s))
    # Source grammar remains fixed for every randomized reconstruction.
    try:
      for p,s in jobs:
        sizes,maps=synth.load_maps(s); graphs={}; selected=maps.copy(); measures={}
        for k,n in sizes.items():
            f,r=maps[k]; g=grammar(n,f,r,args.extra); graphs[k]=g
            dualf,dualr=synth.transpose(n,f,r,rng)
            dg=grammar(len(r),dualf,dualr,args.extra)
            measures[k]={'source':synth.count(f,r),'dictionary_vectors':len(g[0]),'cancellation_edges':g[4],'best_direct':synth.count(f,r),'best_dual':synth.count(f,r)}
            for trial in range(args.trials):
                a,b=search(n,g,rng,trial%4); direct=synth.count(a,b)
                if direct<measures[k]['best_direct']: measures[k]['best_direct']=direct
                if direct<synth.count(*selected[k]): selected[k]=(a,b)
                da,db=search(len(r),dg,rng,trial%4); ta,tb=synth.transpose(len(r),da,db,rng)
                assert synth.vectors(n,ta,tb)==synth.vectors(n,f,r)
                dual=synth.count(ta,tb)
                if dual<measures[k]['best_dual']: measures[k]['best_dual']=dual
                if dual<synth.count(*selected[k]): selected[k]=(ta,tb)
        cost=sum(synth.count(*c) for c in selected.values()); base=synth.exact_check.addition_count(s)
        record={'file':p.name,'format':s['n'],'rank':s['m'],'source_cost':base,'cost':cost,'maps':measures,'args':vars(args),'utc':time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime())}; entries.append(record)
        key=str((s['n'],s['m']))
        if cost<bests.get(key,10**9):
            bests[key]=cost; out=synth.HERE/'result'/('dag_'+p.name)
            record['identity']=synth.save_candidate(out,s,selected,'signed vector AND/OR grammar with cancellation and dual accumulation')
            print(json.dumps({'event':'best',**record}),flush=True)
        (synth.HERE/'output'/'dag_checkpoint.json').write_text(json.dumps({'records':entries,'bests':bests,'elapsed_seconds':time.monotonic()-start},indent=2)+'\n')
    except TimeoutError as e: print(json.dumps({'event':'time_cap','elapsed_seconds':time.monotonic()-start,'records':len(entries),'reason':str(e)}),flush=True)
    finally:
        signal.alarm(0)
        (synth.HERE/'output'/'dag_results.json').write_text(json.dumps(entries,indent=2)+'\n')

if __name__=='__main__': main()
