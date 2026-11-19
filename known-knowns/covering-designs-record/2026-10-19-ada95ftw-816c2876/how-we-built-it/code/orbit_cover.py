#!/usr/bin/env python3
"""Exact orbit set-cover for covering designs C(v,k,t) under PGL/PSL/PGammaL(2,q) acting on PG(1,q) (v=q+1),
optionally with one extra fixed point (v=q+2). Writes JSON lines with status, best size, snapshot size.
Design files written for any OPTIMAL/FEASIBLE solution <= snapshot size."""
import sys, json, itertools, time, os
from math import comb
from ortools.sat.python import cp_model

def gf(q):
    # returns (add, mul, elements 0..q-1, primitive element) as tables
    p=None
    for pp in range(2,q+1):
        if q%pp==0: p=pp;break
    f=0;x=q
    while x>1: x//=p;f+=1
    if f==1:
        add=[[(a+b)%q for b in range(q)] for a in range(q)]
        mul=[[(a*b)%q for b in range(q)] for a in range(q)]
    else:
        # find irreducible monic poly of degree f over GF(p)
        def polymulmod(a,b,mod):
            res=[0]*(2*f)
            for i,ai in enumerate(a):
                for j,bj in enumerate(b): res[i+j]=(res[i+j]+ai*bj)%p
            for d in range(2*f-1,f-1,-1):
                c=res[d]
                if c:
                    for i in range(f+1): res[d-f+i]=(res[d-f+i]-c*mod[i])%p
            return res[:f]
        def toint(a): return sum(c*p**i for i,c in enumerate(a))
        def tovec(n): return [(n//p**i)%p for i in range(f)]
        for cand in range(p**f):
            mod=tovec(cand)+[1]
            # irreducible iff no roots in subfields... brute: check x^(p^f)=x and gcd conditions -> simple: check field by multiplicative group order
            mul=[[toint(polymulmod(tovec(a),tovec(b),mod)) for b in range(q)] for a in range(q)]
            # field iff no zero divisors
            if all(mul[a][b]!=0 for a in range(1,q) for b in range(1,q)): break
        add=[[toint([(x+y)%p for x,y in zip(tovec(a),tovec(b))]) for b in range(q)] for a in range(q)]
    # primitive element
    for g in range(2 if q>2 else 1,q):
        s=set();x=1
        for _ in range(q-1): x=mul[x][g]; s.add(x)
        if len(s)==q-1: break
    return p,f,add,mul,g

def group_gens(q, kind):
    p,f,add,mul,g=gf(q)
    INF=q
    inv=[0]*q
    for a in range(1,q):
        for b in range(1,q):
            if mul[a][b]==1: inv[a]=b
    neg=[0]*q
    for a in range(q):
        for b in range(q):
            if add[a][b]==0: neg[a]=b
    tr=[add[x][1] for x in range(q)]+[INF]
    sq=mul[g][g]
    m_g=[mul[x][g] for x in range(q)]+[INF]
    m_sq=[mul[x][sq] for x in range(q)]+[INF]
    # x -> -1/x
    flip=[INF if x==0 else neg[inv[x]] for x in range(q)]+[0]
    gens=[tr, flip]
    if kind=='PGL': gens.append(m_g)
    elif kind=='PSL': gens.append(m_sq)
    elif kind=='PGaL':
        gens.append(m_g)
        frob=[0]*q
        for x in range(q):
            y=1
            for _ in range(p): y=mul[y][x]
            frob[x]=y if x else 0
        gens.append(frob+[INF])
    return gens

def closure_order(gens,n):
    seen={tuple(range(n))};fr=[tuple(range(n))]
    while fr:
        nf=[]
        for a in fr:
            for gg in gens:
                b=tuple(gg[a[i]] for i in range(n))
                if b not in seen: seen.add(b);nf.append(b)
        fr=nf
        if len(seen)>200000: return -1
    return len(seen)

def make_mapper(perm,n):
    # bitmask image via 8-bit chunk tables
    nch=(n+7)//8
    tabs=[]
    for c in range(nch):
        t=[0]*256
        for byte in range(256):
            m=0
            for b in range(8):
                if byte>>b&1:
                    i=c*8+b
                    if i<n: m|=1<<perm[i]
            t[byte]=m
        tabs.append(t)
    def f(mask):
        r=0;c=0
        while mask:
            r|=tabs[c][mask&255];mask>>=8;c+=1
        return r
    return f

def orbits(n,k,maps):
    seen={}
    reps=[];sizes=[]
    for comb_ in itertools.combinations(range(n),k):
        m=0
        for i in comb_: m|=1<<i
        if m in seen: continue
        oid=len(reps);seen[m]=oid;st=[m];cnt=1
        while st:
            x=st.pop()
            for f in maps:
                y=f(x)
                if y not in seen: seen[y]=oid;st.append(y);cnt+=1
        reps.append(m);sizes.append(cnt)
    return reps,sizes,seen

def bits(m):
    out=[];i=0
    while m:
        if m&1: out.append(i)
        m>>=1;i+=1
    return out

def run(q,kind,extra,k,t,snap,cap,outdir):
    n=q+1+(1 if extra else 0)
    gens=group_gens(q,kind)
    if extra: gens=[g+[q+1] for g in gens]
    maps=[make_mapper(g,n) for g in gens]
    t0=time.time()
    kreps,ksizes,_=orbits(n,k,maps)
    treps,tsizes,tseen=orbits(n,t,maps)
    cov=[]
    for r in kreps:
        b=bits(r);s=set()
        for c in itertools.combinations(b,t):
            m=0
            for i in c: m|=1<<i
            s.add(tseen[m])
        cov.append(s)
    md=cp_model.CpModel()
    x=[md.NewBoolVar(f'x{i}') for i in range(len(kreps))]
    byT=[[] for _ in treps]
    for i,s in enumerate(cov):
        for j in s: byT[j].append(i)
    for j,l in enumerate(byT): md.AddBoolOr([x[i] for i in l])
    md.Minimize(sum(ksizes[i]*x[i] for i in range(len(kreps))))
    sv=cp_model.CpSolver();sv.parameters.max_time_in_seconds=cap;sv.parameters.num_workers=1
    st=sv.Solve(md)
    res=dict(q=q,group=kind,extra=extra,v=n,k=k,t=t,korb=len(kreps),torb=len(treps),status=sv.StatusName(st),snap=snap,secs=round(time.time()-t0,2))
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        sol=[i for i in range(len(kreps)) if sv.Value(x[i])]
        best=sum(ksizes[i] for i in sol); res['best']=best; res['bound']=int(sv.BestObjectiveBound())
        if snap is not None and best<=snap:
            # expand design and write
            blocks=set()
            for i in sol:
                st_=[kreps[i]];seen={kreps[i]}
                while st_:
                    y=st_.pop()
                    for f in maps:
                        z=f(y)
                        if z not in seen: seen.add(z);st_.append(z)
                blocks|=seen
            fn=os.path.join(outdir,f'C{n}_{k}_{t}_{kind}{"_fix" if extra else ""}_{len(blocks)}.txt')
            with open(fn,'w') as fh:
                for bm in sorted(blocks): fh.write(' '.join(str(p+1) for p in bits(bm))+'\n')
            res['file']=os.path.basename(fn)
    return res

if __name__=='__main__':
    snapfile, outdir, maxck, cap = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    snap=json.load(open(snapfile))
    qs=[7,8,9,11,13,16,17,19,23,25,27,29,31]
    done=set()
    resf=os.path.join(outdir,'results.jsonl')
    if os.path.exists(resf):
        for l in open(resf):
            r=json.loads(l); done.add((r['q'],r['group'],r['extra'],r['k'],r['t']))
    jobs=[]
    for q in qs:
        for extra in (0,1):
            n=q+1+extra
            for t in range(2,9):
                for k in range(t+1,min(n-1,25)+1):
                    key=f'C({n},{k},{t})'
                    if key not in snap: continue
                    if comb(n,k)>maxck: continue
                    s=snap[key]
                    if s['size']==s['low_bd']: continue  # exact cell, cannot beat
                    kinds=['PGL']
                    if q%2==1: kinds.append('PSL')
                    if q in (8,9,16,25,27): kinds.append('PGaL')
                    for kind in kinds: jobs.append((comb(n,k),q,kind,extra,k,t,s['size']))
    jobs.sort()
    print('jobs',len(jobs),flush=True)
    with open(resf,'a') as fh:
        for _,q,kind,extra,k,t,sz in jobs:
            if (q,kind,extra,k,t) in done: continue
            r=run(q,kind,extra,k,t,sz,cap,outdir)
            fh.write(json.dumps(r)+'\n');fh.flush()
            flag=' <=SNAP' if r.get('best') is not None and r['best']<=sz else ''
            print(json.dumps(r)+flag,flush=True)
