#!/usr/bin/env python3
"""Orbit covers under small groups acting on cosets: A5 and S5 acting on G/H for subgroups H (transitive actions of
degree 10..40), plus 0-2 extra fixed points. Exact CP-SAT orbit set-cover with a time cap.
usage: coset_cover.py spec maxck cap outdir   where spec = G:H:extra, e.g. A5:Z3:2"""
import sys, json, os, itertools
from math import comb
import orbit_cover as oc
from ortools.sat.python import cp_model
def compose(a,b): return tuple(a[b[i]] for i in range(len(b)))  # a after b
def closure(gens):
    e=tuple(range(len(gens[0])));S={e};fr=[e]
    while fr:
        nf=[]
        for x in fr:
            for g in gens:
                y=compose(g,x)
                if y not in S: S.add(y);nf.append(y)
        fr=nf
    return S
def cyc(*cs):
    p=list(range(5))
    for c in cs:
        for i in range(len(c)): p[c[i]]=c[(i+1)%len(c)]
    return tuple(p)
S5=closure([cyc((0,1)),cyc((0,1,2,3,4))]); A5=closure([cyc((0,1,2)),cyc((0,1,2,3,4))])
Hs={'Z3':[cyc((2,3,4))],'Z2':[cyc((0,1),(2,3))],'V4':[cyc((0,1),(2,3)),cyc((0,2),(1,3))],'Z5':[cyc((0,1,2,3,4))],
    'S3':[cyc((2,3,4)),cyc((2,3))],'S3tw':[cyc((2,3,4)),cyc((2,3),(0,1))],'D10':[cyc((0,1,2,3,4)),cyc((1,4),(2,3))],
    'Z4':[cyc((0,1,2,3))],'D8':[cyc((0,1,2,3)),cyc((0,2))],'Z6':[cyc((2,3,4),(0,1))],'V4b':[cyc((0,1)),cyc((2,3))]}
def coset_action(G,H):
    Hset=closure(H); assert Hset<=G, 'H not in G'
    cosets=[];index={}
    for g in sorted(G):
        if g in index: continue
        c=frozenset(compose(g,h) for h in Hset); cid=len(cosets); cosets.append(c)
        for x in c: index[x]=cid
    n=len(cosets)
    def perm_of(s): return [index[compose(s,next(iter(c)))] for c in cosets]
    return n,perm_of
spec,maxck,cap,outdir=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
parts=spec.split(':');Gn,Hn,extra=parts[:3];extra=int(extra);Kn=parts[3] if len(parts)>3 else None
onlycell=tuple(map(int,parts[4].split(','))) if len(parts)>4 else None
G={'A5':A5,'S5':S5}[Gn]
gens5=[cyc((0,1,2)),cyc((0,1,2,3,4))] if Gn=='A5' else [cyc((0,1)),cyc((0,1,2,3,4))]
Ks={'A4':[cyc((0,1,2)),cyc((0,1),(2,3))],'D10':[cyc((0,1,2,3,4)),cyc((1,4),(2,3))],'S3e':[cyc((0,1,2)),cyc((0,1),(3,4))],
    'Z5':[cyc((0,1,2,3,4))],'V4':[cyc((0,1),(2,3)),cyc((0,2),(1,3))],'Z3':[cyc((0,1,2))],'S4':[cyc((0,1,2,3)),cyc((0,1))]}
Kgens=Ks[Kn] if Kn else gens5
n0,perm_of=coset_action(G,Hs[Hn])
gens=[perm_of(g)+list(range(n0,n0+extra)) for g in Kgens]
n=n0+extra
print('group order',oc.closure_order(gens,n),flush=True)
maps=[oc.make_mapper(g,n) for g in gens]
snap=json.load(open('snap.json'))
resf=os.path.join(outdir,f'coset_results.jsonl')
jobs=[]
for t in range(3,9):
    for k in range(t+1,min(n-1,25)+1):
        key=f'C({n},{k},{t})'
        if key in snap and comb(n,k)<=maxck and snap[key]['size']>snap[key]['low_bd'] and (onlycell is None or (k,t)==onlycell): jobs.append((comb(n,k),k,t))
jobs.sort()
for _,k,t in jobs:
    s=snap[f'C({n},{k},{t})']
    kreps,ksizes,_=oc.orbits(n,k,maps)
    if len(kreps)>40000: continue
    treps,tsizes,tseen=oc.orbits(n,t,maps)
    md=cp_model.CpModel();x=[md.NewBoolVar('') for _ in kreps];byT=[[] for _ in treps]
    for i,r in enumerate(kreps):
        ss=set()
        for c in itertools.combinations(oc.bits(r),t):
            m=0
            for p in c: m|=1<<p
            ss.add(tseen[m])
        for j in ss: byT[j].append(i)
    for l in byT: md.AddBoolOr([x[i] for i in l])
    md.Minimize(sum(ksizes[i]*x[i] for i in range(len(kreps))))
    sv=cp_model.CpSolver();sv.parameters.max_time_in_seconds=cap;sv.parameters.num_workers=2
    if len(sys.argv)>5: sv.parameters.num_workers=int(sys.argv[5])
    st=sv.Solve(md)
    r=dict(spec=spec,v=n,k=k,t=t,korb=len(kreps),torb=len(treps),status=sv.StatusName(st),snap=s['size'],low_bd=s['low_bd'])
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
            fn=os.path.join(outdir,f'C{n}_{k}_{t}_{Gn}{Hn}e{extra}{Kn or ""}_{len(blocks)}.txt')
            with open(fn,'w') as f2:
                for bm in sorted(blocks): f2.write(' '.join(str(p+1) for p in oc.bits(bm))+'\n')
            r['file']=os.path.basename(fn)
    with open(resf,'a') as fh: fh.write(json.dumps(r)+'\n')
    print(json.dumps(r)+(' <=SNAP' if r.get('best',10**9)<=s['size'] else ''),flush=True)
