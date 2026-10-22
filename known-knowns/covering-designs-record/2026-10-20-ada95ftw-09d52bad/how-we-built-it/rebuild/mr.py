# helpers copied verbatim from an earlier search script, msum_resume.py (lines 1-65)
#!/usr/bin/env python3
"""Lens structured: intransitive G-sets (disjoint unions of coset actions G/H) for G in {A5, S5, PSL(2,7)}.
For each G-set of size v (10..32, <=3 orbits) and each open snapshot cell (v,k,t), 3<=t<=5, solve the exact
orbit set-cover with CP-SAT (time cap). usage: msum_resume.py cap maxck outdir worker nworkers
RESUME (run 2026-10-19-1303): skips the jobs that run 2026-10-18-1802 already ran (5 workers, jobs[w::5],
matched sequentially against its res_w*.jsonl rows) and splits the remaining jobs round-robin."""
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
