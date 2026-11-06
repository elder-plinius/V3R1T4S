#!/usr/bin/env python3
"""Independent onset checker (written separately from fsearch.c; plain dict-based simulation).
Convention: ant at (0,0) facing north, y grows downward; white->turn right, black->turn left, flip, step.
Onset = least s such that the heading sequence is 104-periodic from s on with net 104-step displacement (+-2,+-2),
checked over a long window, plus a sweep check: by the window's end the ant is farther (Chebyshev) from every
cell touched before s+104 than it travels back in any period (it never revisits them while the window holds).
Usage: check_onset.py "(x,y) (x,y) ..."  [periods]"""
import sys,re
def run(cells,periods):
    black=set(cells); x=y=0; d=0  # 0=N,1=E,2=S,3=W
    D=[(0,-1),(1,0),(0,1),(-1,0)]
    H=[];P=[(0,0)]
    N=None; steps=0; L=None
    limit=200000
    while True:
        c=(x,y)
        if c in black: d=(d+3)%4; black.discard(c)
        else: d=(d+1)%4; black.add(c)
        x+=D[d][0]; y+=D[d][1]; H.append(d); P.append((x,y)); steps+=1
        if steps>=limit: break
    return H,P
def onset(cells,periods=300):
    H,P=run(cells,periods)
    n=len(H)
    # last index where periodicity fails
    bad=-1
    for u in range(104,n):
        if H[u]!=H[u-104]: bad=u
    s=bad-104+1 if bad>=0 else 0   # turns H[s..] periodic
    assert n-s>104*periods, "window too short"
    dx=P[s+104][0]-P[s][0]; dy=P[s+104][1]-P[s][1]
    assert abs(dx)==2 and abs(dy)==2, (dx,dy)
    # sweep: cells touched before s+104 (and initial cells) vs final ant position
    touched=set(cells)|set(P[:s+105])
    ex,ey=P[-1]
    dist=min(max(abs(ex-a),abs(ey-b)) for a,b in touched)
    return s,dist
if __name__=="__main__":
    cells=[tuple(map(int,m)) for m in re.findall(r"\((-?\d+),(-?\d+)\)",sys.argv[1])] if len(sys.argv)>1 and sys.argv[1]!="blank" else []
    s,dist=onset(cells)
    print(f"ONSET={s} cells={len(cells)} final_dist_from_touched={dist}")
