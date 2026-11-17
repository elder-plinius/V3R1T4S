#!/usr/bin/env python3
"""Exact strict-vs-pseudo test for a still life: search for a partition of live cells
into two nonempty sets A,B with A alone stable and B alone stable (backtracking)."""
import sys, os

def nbrs(c):
    x,y=c
    return [(x+dx,y+dy) for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy]

def is_strict_cells(cells):
    cells=sorted(cells); L=set(cells)
    idx={c:i for i,c in enumerate(cells)}
    region=set(L)
    for c in cells: region.update(nbrs(c))
    # constraint per region cell: list of live neighbor indices
    cons=[]
    for r in region:
        nb=[idx[q] for q in nbrs(r) if q in L]
        if nb: cons.append((r in L, idx.get(r), nb))
    # order constraints by max index needed
    n=len(cells)
    bylast={}
    for live,ri,nb in cons:
        last=max(nb+([ri] if ri is not None else []))
        bylast.setdefault(last,[]).append((live,ri,nb))
    assign=[0]*n
    def ok_upto(k):
        for live,ri,nb in bylast.get(k,()):
            for part in (0,1):
                cnt=sum(1 for j in nb if assign[j]==part)
                if live and assign[ri]==part:
                    if cnt not in (2,3): return False
                else:
                    if cnt==3: return False
        return True
    found=[False]
    def rec(k):
        if found[0]: return
        if k==n:
            if 0<sum(assign)<n: found[0]=True
            return
        for v in ((0,) if k==0 else (0,1)):
            assign[k]=v
            if ok_upto(k): rec(k+1)
    rec(0)
    return not found[0]

def is_strict(apg):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data', 'Shinjuku'))
    from shinjuku import lt
    p=lt.pattern(apg)
    if p[1]!=p: return None
    return is_strict_cells([tuple(map(int,c)) for c in p.coords()])

if __name__=='__main__':
    for line in sys.stdin:
        a=line.split()[-1]
        if a.startswith('xs'): print(is_strict(a), line.strip(), flush=True)
