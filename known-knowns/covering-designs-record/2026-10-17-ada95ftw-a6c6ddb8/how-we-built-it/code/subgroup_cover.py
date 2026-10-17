#!/usr/bin/env python3
"""Hypothesis 8: small subgroups (orders 12..120: A4, S4, A5, dihedral, etc.) of PGL(2,q) acting on PG(1,q) (v=q+1)
or with an extra fixed point (v=q+2). Subgroups found as closures of random element pairs from the full PGL(2,q).
Exact orbit set-cover by CP-SAT with a time cap. usage: subgroup_cover.py q extra maxck cap seed outdir"""
import sys, json, random, os, itertools
from math import comb
import orbit_cover as oc
from ortools.sat.python import cp_model

def elements(gens,n):
    seen={tuple(range(n))};fr=[tuple(range(n))]
    while fr:
        nf=[]
        for a in fr:
            for g in gens:
                b=tuple(g[a[i]] for i in range(n))
                if b not in seen: seen.add(b);nf.append(b)
        fr=nf
    return list(seen)
def closure(gens,n,cap=200):
    seen={tuple(range(n))};fr=[tuple(range(n))]
    while fr:
        nf=[]
        for a in fr:
            for g in gens:
                b=tuple(g[a[i]] for i in range(n))
                if b not in seen:
                    seen.add(b);nf.append(b)
                    if len(seen)>cap: return None
        fr=nf
    return seen
def orbit_sig(G,n):
    # orbit lengths on points, for de-dup of conjugacy (heuristic, plus order)
    seen=set();lens=[]
    for p in range(n):
        if p in seen: continue
        o={g[p] for g in G};seen|=o;lens.append(len(o))
    return tuple(sorted(lens))
q,extra,maxck,cap,seed,outdir=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
random.seed(seed)
n0=q+1
full=elements(oc.group_gens(q,'PGL'),n0)
subs={}
for _ in range(20000):
    a,b=random.choice(full),random.choice(full)
    G=closure([a,b],n0,cap=120)
    if G is None or len(G)<6: continue
    if len(G) not in (12,24,60): continue
    inv=sum(1 for g in G if g!=tuple(range(n0)) and all(g[g[i]]==i for i in range(n0)))
    if (len(G),inv) not in ((12,3),(24,9),(60,15)): continue   # A4, S4, A5 only (dihedral/AGL-type covered before)
    key=(len(G),orbit_sig(G,n0))
    if key not in subs: subs[key]=[a,b]
snap=json.load(open('snap.json'))
n=n0+extra
resf=os.path.join(outdir,f'sub_results_q{q}_e{extra}.jsonl')
with open(resf,'a') as fh:
    for (order,sig),gens in sorted(subs.items(),key=lambda x:-x[0][0]):
        gg=[list(g)+([n0] if extra else []) for g in gens]
        maps=[oc.make_mapper(g,n) for g in gg]
        for t in range(3,9):
            for k in range(t+1,min(n-1,25)+1):
                key=f'C({n},{k},{t})'
                if key not in snap or comb(n,k)>maxck: continue
                s=snap[key]
                if s['size']==s['low_bd']: continue
                kreps,ksizes,_=oc.orbits(n,k,maps)
                if len(kreps)>20000: continue
                treps,tsizes,tseen=oc.orbits(n,t,maps)
                md=cp_model.CpModel();x=[md.NewBoolVar('') for _ in kreps]
                byT=[[] for _ in treps]
                for i,r in enumerate(kreps):
                    b=oc.bits(r);ss=set()
                    for c in itertools.combinations(b,t):
                        m=0
                        for p in c: m|=1<<p
                        ss.add(tseen[m])
                    for j in ss: byT[j].append(i)
                for l in byT: md.AddBoolOr([x[i] for i in l])
                obj=sum(ksizes[i]*x[i] for i in range(len(kreps)))
                md.Minimize(obj)
                sv=cp_model.CpSolver();sv.parameters.max_time_in_seconds=cap;sv.parameters.num_workers=2
                st=sv.Solve(md)
                r=dict(q=q,extra=extra,order=order,sig=list(sig),v=n,k=k,t=t,korb=len(kreps),torb=len(treps),status=sv.StatusName(st),snap=s['size'],low_bd=s['low_bd'])
                if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
                    sol=[i for i in range(len(kreps)) if sv.Value(x[i])]
                    r['best']=sum(ksizes[i] for i in sol);r['bound']=int(sv.BestObjectiveBound())
                    if r['best']<=s['size']:
                        blocks=set()
                        for i in sol:
                            stck=[kreps[i]];seen={kreps[i]}
                            while stck:
                                y=stck.pop()
                                for f in maps:
                                    z=f(y)
                                    if z not in seen: seen.add(z);stck.append(z)
                            blocks|=seen
                        fn=os.path.join(outdir,f'C{n}_{k}_{t}_q{q}e{extra}o{order}_{len(blocks)}.txt')
                        with open(fn,'w') as f2:
                            for bm in sorted(blocks): f2.write(' '.join(str(p+1) for p in oc.bits(bm))+'\n')
                        r['file']=os.path.basename(fn)
                fh.write(json.dumps(r)+'\n');fh.flush()
                print(json.dumps(r)+(' <=SNAP' if r.get('best',10**9)<=s['size'] else ''),flush=True)
