#!/usr/bin/env python3
"""Lens structured: intransitive G-sets (disjoint unions of coset actions G/H) for G in {A5, S5, PSL(2,7)}.
For each G-set of size v (10..32, <=3 orbits) and each open snapshot cell (v,k,t), 3<=t<=5, solve the exact
orbit set-cover with CP-SAT (time cap). usage: msum_cover.py cap maxck outdir worker nworkers"""
import sys, json, os, itertools, random
from math import comb
sys.path.insert(0, os.path.dirname(__file__))
import orbit_cover as oc
from ortools.sat.python import cp_model

def mul(a,b): return tuple(a[b[i]] for i in range(len(b)))  # a after b
def elements(gens):
    n=len(gens[0]);e=tuple(range(n));seen={e};fr=[e]
    while fr:
        nf=[]
        for a in fr:
            for g in gens:
                b=mul(g,a)
                if b not in seen: seen.add(b);nf.append(b)
        fr=nf
    return seen
def inv(a):
    r=[0]*len(a)
    for i,x in enumerate(a): r[x]=i
    return tuple(r)
def groups():
    G={}
    G['A5']=[(1,2,3,4,0),(1,2,0,3,4)]
    G['S5']=[(1,2,3,4,0),(1,0,2,3,4)]
    # PSL(2,7) on PG(1,7): points 0..6, inf=7; x->x+1, x->2x, x->-1/x
    def f(fn):
        return tuple(fn(x) for x in range(8))
    def p1(x): return 7 if x==7 else (x+1)%7
    def p2(x): return 7 if x==7 else (2*x)%7
    def p3(x):
        if x==7: return 0
        if x==0: return 7
        return (-pow(x,5,7))%7
    G['PSL27']=[f(p1),f(p2),f(p3)]
    return G
def subgroup_classes(gens,seed=1):
    E=list(elements(gens));random.seed(seed)
    subs=set()
    for a in E:
        subs.add(frozenset(elements([a])))
    for _ in range(4000):
        a,b=random.choice(E),random.choice(E)
        subs.add(frozenset(elements([a,b])))
    classes=[];seen=set()
    for H in sorted(subs,key=len):
        if H in seen: continue
        conj=set()
        for g in E:
            gi=inv(g);conj.add(frozenset(mul(mul(g,h),gi) for h in H))
        seen|=conj;classes.append(H)
    return E,classes
def coset_action(gens,E,H):
    Hl=list(H);cos={};reps=[]
    for g in E:
        if g in cos: continue
        c=frozenset(mul(g,h) for h in Hl);i=len(reps);reps.append(g)
        for x in c: cos[x]=i
    return [tuple(cos[mul(s,r)] for r in reps) for s in gens]
def main():
    cap,maxck,outdir,w,nw=float(sys.argv[1]),int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
    snap=json.load(open(os.path.join(os.path.dirname(__file__),'../../../data/coverdata.json')))
    jobs=[]
    for gname,gens in groups().items():
        E,cls=subgroup_classes(gens)
        acts=[]
        for H in cls:
            d=len(E)//len(H)
            if d>30: continue
            acts.append((d,len(H),coset_action(gens,E,H)))
        for r in (1,2,3):
            for combo in itertools.combinations_with_replacement(range(len(acts)),r):
                v=sum(acts[i][0] for i in combo)
                if not 10<=v<=32: continue
                if sum(1 for i in combo if acts[i][0]==1)>2: continue
                if all(acts[i][0]==1 for i in combo): continue
                for t in (3,4,5):
                    for k in range(t+1,v-1):
                        key=f'C({v},{k},{t})'
                        if key not in snap or comb(v,k)>maxck or comb(v,t)>maxck: continue
                        s=snap[key]
                        if s['size']<=s['low_bd']: continue
                        jobs.append((comb(v,k),gname,combo,v,k,t))
    jobs.sort()
    mine=jobs[w::nw]
    print(f'worker {w}: {len(mine)} of {len(jobs)} jobs',flush=True)
    G=groups();cache={}
    resf=os.path.join(outdir,f'res_w{w}.jsonl')
    with open(resf,'a') as fh:
        for ck,gname,combo,v,k,t in mine:
            if gname not in cache:
                E,cls=subgroup_classes(G[gname])
                cache[gname]=[(len(E)//len(H),len(H),coset_action(G[gname],E,H)) for H in cls if len(E)//len(H)<=30]
            acts=cache[gname]
            # disjoint union of the chosen coset actions
            perms=[[] for _ in G[gname]];off=0;sig=[]
            for i in combo:
                d,ho,pa=acts[i];sig.append([d,ho])
                for j,p in enumerate(pa): perms[j]+= [x+off for x in p]
                off+=d
            maps=[oc.make_mapper(p,v) for p in perms]
            kreps,ksizes,_=oc.orbits(v,k,maps)
            if len(kreps)>20000: continue
            treps,tsizes,tseen=oc.orbits(v,t,maps)
            md=cp_model.CpModel();x=[md.NewBoolVar('') for _ in kreps]
            byT=[[] for _ in treps]
            for i,rr in enumerate(kreps):
                b=oc.bits(rr);ss=set()
                for c in itertools.combinations(b,t):
                    m=0
                    for p in c: m|=1<<p
                    ss.add(tseen[m])
                for j in ss: byT[j].append(i)
            for l in byT: md.AddBoolOr([x[i] for i in l])
            md.Minimize(sum(ksizes[i]*x[i] for i in range(len(kreps))))
            sv=cp_model.CpSolver();sv.parameters.max_time_in_seconds=cap;sv.parameters.num_workers=1
            st=sv.Solve(md);s=snap[f'C({v},{k},{t})']
            r=dict(group=gname,orbits=sig,v=v,k=k,t=t,korb=len(kreps),torb=len(treps),status=sv.StatusName(st),snap=s['size'],low_bd=s['low_bd'])
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
                    fn=os.path.join(outdir,f'C{v}_{k}_{t}_{gname}_{"-".join(str(a[0]) for a in sig)}_{len(blocks)}.txt')
                    with open(fn,'w') as f2:
                        for bm in sorted(blocks): f2.write(' '.join(str(p+1) for p in oc.bits(bm))+'\n')
                    r['file']=os.path.basename(fn)
            fh.write(json.dumps(r)+'\n');fh.flush()
            if r.get('best',10**9)<=s['size']: print(json.dumps(r)+' <=SNAP',flush=True)
main()
