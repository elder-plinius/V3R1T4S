#!/usr/bin/env python3
"""Integer linear-map synthesis with cancellation and reverse accumulation."""
import argparse, collections, copy, itertools, json, os, pathlib, random, signal, sys, time

HERE = pathlib.Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
import exact_check

def count(fresh, rows):
    return sum(max(0, len(r)-1) for r in fresh+rows)

def norm(v):
    return sum(abs(x) for x in v)

def add(a,b,s=1):
    return tuple(x+s*y for x,y in zip(a,b))

def canonical(v):
    for x in v:
        if x:
            s=1 if x>0 else -1
            return tuple(s*x for x in v),s
    return v,1

def to_rows(ds):
    return [[{'index':i,'value':v} for i,v in sorted(d.items())] for d in ds]

def from_rows(rs):
    return [{t['index']:t['value'] for t in r} for r in rs]

def vectors(n,fresh,rows):
    vals=[tuple(int(i==j) for j in range(n)) for i in range(n)]
    for r in fresh:
        vals.append(tuple(sum(c*vals[i][j] for i,c in r.items()) for j in range(n)))
    return [tuple(sum(c*vals[i][j] for i,c in r.items()) for j in range(n)) for r in rows]

class Circuit:
    def __init__(self,n): self.n=n; self.fresh=[]
    def materialize(self,terms,rng=None):
        terms=collections.Counter(dict()) if not terms else collections.Counter(terms) if isinstance(terms,dict) else self.collect(terms)
        expanded=[]
        for i,c in terms.items():
            expanded.extend([(i,1 if c>0 else -1)]*abs(c))
        if rng: rng.shuffle(expanded)
        if not expanded: return {}
        while len(expanded)>1:
            i,a=expanded.pop(0); j,b=expanded.pop(0)
            if i==j:
                if a==-b: continue
                j=self.n+len(self.fresh); self.fresh.append({i:1})
            k=self.n+len(self.fresh); self.fresh.append({i:a,j:b})
            expanded.insert(0,(k,1))
        return dict(expanded)
    @staticmethod
    def collect(terms):
        d=collections.Counter()
        for i,c in terms: d[i]+=c
        return {i:c for i,c in d.items() if c}

def prune(n,fresh,rows):
    required=set(i for r in rows for i in r if i>=n)
    for k in range(len(fresh)-1,-1,-1):
        if n+k in required: required.update(i for i in fresh[k] if i>=n)
    remap={i:i for i in range(n)}; fs=[]
    for k,r in enumerate(fresh):
        if n+k in required:
            nr={remap[i]:c for i,c in r.items()}
            remap[n+k]=n+len(fs); fs.append(nr)
    return fs,[{remap[i]:c for i,c in r.items()} for r in rows]

def transpose(n,fresh,rows,rng=None):
    """Reverse all edges, accumulating adjoints exactly over Z."""
    c=Circuit(len(rows)); adj=[[] for _ in range(n+len(fresh))]
    for j,r in enumerate(rows):
        for i,s in r.items(): adj[i].append((j,s))
    for k in range(len(fresh)-1,-1,-1):
        deriv=c.materialize(adj[n+k],rng)
        for i,s in fresh[k].items():
            for v,t in deriv.items(): adj[i].append((v,s*t))
    out=[c.materialize(adj[i],rng) for i in range(n)]
    return prune(len(rows),c.fresh,out)

def matrix_transpose(targets,n):
    return [tuple(row[i] for row in targets) for i in range(n)]

def diff_tree(targets,n,rng=None):
    """Prim tree over signed targets and the free original variables."""
    c=Circuit(n); done={}; pending=set(range(len(targets)))
    while pending:
        choices=[]
        for j in pending:
            t=targets[j]; direct=norm(t)-1 if norm(t) else 0
            choices.append((direct,j,None,1,t))
            for k,ref in done.items():
                for s in (1,-1):
                    delta=add(t,targets[k],-s)
                    choices.append((norm(delta),j,k,s,delta))
        best=min(x[0] for x in choices); tied=[x for x in choices if x[0]==best]
        cost,j,k,s,d=(rng.choice(tied) if rng else tied[0])
        terms=[]
        if k is not None: terms.extend((i,s*v) for i,v in done[k].items())
        for i,v in enumerate(d): terms.extend([(i,1 if v>0 else -1)]*abs(v))
        done[j]=c.materialize(terms,rng); pending.remove(j)
    return prune(n,c.fresh,[done[j] for j in range(len(targets))])

def dictionary_synth(targets,n,rng,seconds=8,mag=1,beam=0):
    """Choose signed vector sums using target residuals and exact two-sum exits.

    A candidate can overlap both parents and cancel coordinates. Scoring is a
    constructive completion bound, not a shared-support occurrence count.
    """
    start=time.monotonic(); deadline=start+seconds
    basis=[tuple(int(i==j) for j in range(n)) for i in range(n)]
    vals=basis[:]; refs=[{i:1} for i in range(n)]; lookup={v:i for i,v in enumerate(vals)}
    c=Circuit(n); unresolved=set(range(len(targets))); outs={}
    distances=[max(0,norm(t)-1) for t in targets]
    iterations=0
    while unresolved and time.monotonic()<deadline and iterations<3*sum(norm(t) for t in targets):
        iterations+=1
        # Exact signed singletons and two-sums are finished immediately.
        for j in list(unresolved):
            t=targets[j]; cv,sg=canonical(t)
            if cv in lookup:
                outs[j]={i:sg*v for i,v in refs[lookup[cv]].items()}; unresolved.remove(j); continue
            for i,v in enumerate(vals):
                found=None
                for s in (1,-1):
                    rem=add(t,v,-s); cr,sr=canonical(rem)
                    if cr in lookup:
                        k=lookup[cr]
                        terms=[(z,s*q) for z,q in refs[i].items()]+[(z,sr*q) for z,q in refs[k].items()]
                        found=c.materialize(terms,rng); break
                if found is not None:
                    outs[j]=found; unresolved.remove(j); break
        if not unresolved: break
        # Distance from one available sum plus free original variables.
        nearest={}
        for j in unresolved:
            t=targets[j]; opts=[(max(0,norm(t)-1),None,1,t)]
            for i,v in enumerate(vals):
                for s in (1,-1):
                    rem=add(t,v,-s); opts.append((norm(rem),i,s,rem))
            nearest[j]=min(opts,key=lambda q:q[0]); distances[j]=nearest[j][0]
        candidates={}
        for i,v in enumerate(vals):
            for k in range(i+1,len(vals)):
                for s in (1,-1):
                    cv,sg=canonical(add(v,vals[k],s))
                    if cv in lookup or not any(cv) or max(map(abs,cv))>mag: continue
                    if cv not in candidates: candidates[cv]=(i,k,s,sg)
        bestscore=None; tied=[]
        for cv,parents in candidates.items():
            reductions=[]; sq=0; completed=0
            for j in unresolved:
                d=min(norm(add(targets[j],cv,-1)),norm(add(targets[j],cv,1)))
                improve=max(0,distances[j]-d)
                reductions.append(improve); sq+=improve*improve; completed+=int(d==0)
            score=(sum(reductions),completed,sq,-norm(cv))
            if bestscore is None or score>bestscore: bestscore=score; tied=[(cv,parents)]
            elif score==bestscore: tied.append((cv,parents))
        if not tied or bestscore[0]<=1:
            # A completed target becomes reusable for later target differences.
            order=list(unresolved); rng.shuffle(order)
            j=min(order,key=lambda q:nearest[q][0]); d,i,s,rem=nearest[j]
            terms=[] if i is None else [(z,s*q) for z,q in refs[i].items()]
            for z,q in enumerate(rem): terms.extend([(z,1 if q>0 else -1)]*abs(q))
            out=c.materialize(terms,rng); outs[j]=out; unresolved.remove(j)
            cv,sg=canonical(targets[j])
            if cv not in lookup:
                lookup[cv]=len(vals); vals.append(cv); refs.append({z:sg*q for z,q in out.items()})
            continue
        cv,(i,k,s,sg)=rng.choice(tied)
        terms=[(z,sg*q) for z,q in refs[i].items()]+[(z,sg*s*q) for z,q in refs[k].items()]
        ref=c.materialize(terms,rng); lookup[cv]=len(vals); vals.append(cv); refs.append(ref)
    # Construct any unfinished targets honestly from the best single residual.
    for j in unresolved:
        t=targets[j]; opts=[(max(0,norm(t)-1),None,1,t)]
        for i,v in enumerate(vals):
            for s in (1,-1):
                rem=add(t,v,-s); opts.append((norm(rem),i,s,rem))
        d,i,s,rem=min(opts,key=lambda x:x[0]); terms=[] if i is None else [(z,s*q) for z,q in refs[i].items()]
        for z,q in enumerate(rem): terms.extend([(z,1 if q>0 else -1)]*abs(q))
        outs[j]=c.materialize(terms,rng)
    f,r=prune(n,c.fresh,[outs[j] for j in range(len(targets))])
    assert vectors(n,f,r)==targets
    return f,r

def source_list():
    return sorted(p for p in (ROOT/'sources'/'schemes').glob('*.json') if not p.name.endswith('.fetch.json'))

def load_maps(s):
    a,b,c=s['n']; sizes={'u':a*b,'v':b*c,'w':s['m']}
    return sizes,{k:(from_rows(s.get(k+'_fresh',[])),from_rows(s[k])) for k in sizes}

def save_candidate(path,source,maps,tag):
    s=copy.deepcopy(source)
    for k,(f,r) in maps.items(): s[k+'_fresh']=to_rows(f); s[k]=to_rows(r)
    s['complexity']['reduced']=exact_check.addition_count(s)
    result=exact_check.verify(s)
    s['research_method']=tag
    path.write_text(json.dumps(s,indent=2)+'\n')
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['calibrate','sweep','roundtrip'],default='calibrate')
    ap.add_argument('--seconds',type=float,default=60); ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--per-map',type=float,default=0.3); ap.add_argument('--max-rank',type=int,default=51); args=ap.parse_args()
    start=time.monotonic(); rng=random.Random(args.seed); results=[]; bests={}
    (HERE/'output'/'pid.json').write_text(json.dumps({'pid':os.getpid(),'started_utc':time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime()),'hard_seconds':args.seconds,'mode':args.mode})+'\n')
    signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(TimeoutError('hard time cap')))
    signal.alarm(int(args.seconds)+1)
    allfiles=source_list(); refs={}
    for p in allfiles:
        s=json.loads(p.read_text()); key=(tuple(s['n']),s['m']); cost=exact_check.addition_count(s)
        refs[key]=min(refs.get(key,10**9),cost)
    files=[p for p in allfiles if json.loads(p.read_text())['m']<=args.max_rank]
    try:
      rounds=1 if args.mode=='calibrate' else 10**6
      for rnd in range(rounds):
       rng.shuffle(files)
       for path in files:
        if time.monotonic()-start>args.seconds: raise TimeoutError('hard time cap')
        s=json.loads(path.read_text()); sizes,original=load_maps(s); key=(tuple(s['n']),s['m']); baseline=exact_check.addition_count(s)
        chosen=dict(original); measurements={}
        for k,n in sizes.items():
            f,r=original[k]; target=vectors(n,f,r); base=count(f,r); options=[('source',(f,r))]
            if args.mode in ('calibrate','sweep'):
                options.append(('signed_difference',diff_tree(target,n,rng)))
                if n<=18:
                    options.append(('dictionary',dictionary_synth(target,n,rng,args.per_map,1+(rnd%5==4))))
                dual=matrix_transpose(target,n)
                if len(dual[0])<=18:
                    df,dr=dictionary_synth(dual,len(target),rng,args.per_map,1+(rnd%5==4))
                    tf,tr=transpose(len(target),df,dr,rng)
                    assert vectors(n,tf,tr)==target
                    options.append(('dual_dictionary',(tf,tr)))
                df,dr=diff_tree(dual,len(target),rng)
                tf,tr=transpose(len(target),df,dr,rng)
                assert vectors(n,tf,tr)==target
                options.append(('dual_difference',(tf,tr)))
            # Existing DAG round trip tests reverse accumulation alone.
            tf,tr=transpose(n,f,r,rng)
            rf,rr=transpose(len(target),tf,tr,rng)
            assert vectors(n,rf,rr)==target
            options.append(('roundtrip',(rf,rr)))
            measurements[k]={name:count(*circuit) for name,circuit in options}
            name,circuit=min(options,key=lambda x:count(*x[1])); chosen[k]=circuit
        total=sum(count(*c) for c in chosen.values()); record={'round':rnd,'file':path.name,'format':s['n'],'rank':s['m'],'source_cost':baseline,'minimum_reference':refs[key],'cost':total,'maps':measurements,'utc':time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime())}
        results.append(record)
        bestkey=str(key)
        if total<bests.get(bestkey,10**9):
            bests[bestkey]=total
            out=HERE/'result'/('best_'+path.name)
            check=save_candidate(out,s,chosen,args.mode+' cancellation dictionary, target differences and transposition')
            print(json.dumps({'event':'best','file':out.name,**record,'identity':check}),flush=True)
        (HERE/'output'/(args.mode+'_checkpoint.json')).write_text(json.dumps({'elapsed_seconds':time.monotonic()-start,'seed':args.seed,'records':results,'bests':bests},indent=2)+'\n')
    except TimeoutError as e:
        print(json.dumps({'event':'time_cap','elapsed_seconds':time.monotonic()-start,'records':len(results),'reason':str(e)}),flush=True)
    finally:
        signal.alarm(0)
        (HERE/'output'/(args.mode+'_results.json')).write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__': main()
