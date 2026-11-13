#!/usr/bin/env python3
"""Exact strict-vs-pseudo test by exhaustive stable-subset/complement enumeration.
A stable proper subset alone is not enough to be pseudo: its complement must
also be stable. No island heuristic or search cap.
For every subset bit vector, enforce B3/S23 at every target cell and every
neighbor of a target cell. Everywhere else necessarily stays dead. Constraints
are evaluated only after their last input bit is assigned; pruning therefore
removes only branches whose every completion fails a fully determined equation.
"""
from life_check import decode_apgcode,step

def stable_subsets(cells):
    pts=sorted(cells); idx={p:i for i,p in enumerate(pts)}; n=len(pts)
    region=set(pts)
    for x,y in pts:
        region.update((x+dx,y+dy) for dx in (-1,0,1) for dy in (-1,0,1))
    bylast={}
    for x,y in sorted(region):
        nb=[idx[x+dx,y+dy] for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and (x+dx,y+dy) in idx]
        selfbit=idx.get((x,y)); inputs=nb+([] if selfbit is None else [selfbit])
        if inputs: bylast.setdefault(max(inputs),[]).append((selfbit,nb))
    bits=[0]*n; solutions=[]; nodes=0
    def visit(k):
        nonlocal nodes
        nodes+=1
        if k==n:
            solutions.append(sum(b<<i for i,b in enumerate(bits))); return
        for value in (0,1):
            bits[k]=value; valid=True
            for own,nb in bylast.get(k,[]):
                cnt=sum(bits[i] for i in nb); alive=0 if own is None else bits[own]
                if bool(cnt==3 or (alive and cnt==2))!=bool(alive): valid=False;break
            if valid: visit(k+1)
    visit(0)
    proper=[m for m in solutions if m not in (0,(1<<n)-1)]
    partitions=[m for m in proper if ((1<<n)-1)^m in solutions]
    return {'population':n,'full_stable':step(set(pts))==set(pts),'nodes':nodes,'stable_subsets_total':len(solutions),'proper_stable_subsets':len(proper),'stable_complement_partitions':len(partitions)//2,'strict':step(set(pts))==set(pts) and not partitions}

def controls():
    block={(0,0),(1,0),(0,1),(1,1)}
    cases=[('block',block,True),('two_blocks',block|{(x+6,y) for x,y in block},False),('single_cell',{(0,0)},False)]
    for label,c,want in cases:
        res=stable_subsets(c); print('control',label,res); assert res['strict']==want
if __name__=='__main__':
    import sys
    controls()
    result=stable_subsets(decode_apgcode(sys.argv[1])[2]);print('target',sys.argv[1],result)
    print('PASS' if result['strict'] else 'FAIL');sys.exit(0 if result['strict'] else 1)
