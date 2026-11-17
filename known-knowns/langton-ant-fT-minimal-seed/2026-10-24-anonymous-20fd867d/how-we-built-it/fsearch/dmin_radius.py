# Doc-fix check (2026-10-23): blank-grid highway geometry behind fsearch's Dmin=159 and the debris radius.
# Light computation only (one blank simulation). Convention: t = updates done; heading N, y down; white->right.
N0=9977; P=104; NP=110; T=N0+P*NP+P
D=[(0,-1),(1,0),(0,1),(-1,0)]
x=y=0; h=0; black=set(); first={}; pos=[]
for t in range(T):
    pos.append((x,y))
    c=(x,y)
    if c not in first: first[c]=t
    if c in black: h=(h-1)%4; black.discard(c)
    else: h=(h+1)%4; black.add(c)
    x+=D[h][0]; y+=D[h][1]
pos.append((x,y))
# drift per period
dx=pos[N0+P][0]-pos[N0][0]; dy=pos[N0+P][1]-pos[N0][1]
print("drift per period", (dx,dy))
# periodicity of first reads (translation by drift) over periods 1..NP-1 relative to period 0 of the highway
bytime={t:c for c,t in first.items()}
ok=True
for t in range(N0+P, N0+P*NP):
    a=bytime.get(t); b=bytime.get(t-P)
    if (a is None)!=(b is None) or (a and (a[0]-b[0],a[1]-b[1])!=(dx,dy)): ok=False;break
print("first-read times/cells translate by drift each period from 9977+104 to 9977+%d:"%(P*NP), ok)
# replay to get black set at each phase start (re-simulate to N0+P)
x=y=0;h=0;bl=set();rad=[]
for t in range(N0+P):
    if t>=N0:
        ax,ay=x,y; rad.append(max(max(abs(u-ax),abs(v-ay)) for (u,v) in bl))
    c=(x,y)
    if c in bl: h=(h-1)%4; bl.discard(c)
    else: h=(h+1)%4; bl.add(c)
    x+=D[h][0]; y+=D[h][1]
print("max Chebyshev radius of black debris about the ant over the 104 phases:", max(rad))
# per phase: min Chebyshev distance and min drift-projection of cells first read in period j (j=80..NP-2), from ant at s
ux,uy=dx//abs(dx),dy//abs(dy)
mins={}; projmin={}
for p in range(P):
    s=N0+p; ax,ay=pos[s]
    for j in range(80,NP-1):
        lo=s+j*P; hi=lo+P
        cs=[bytime[t] for t in range(lo,hi) if t in bytime]
        dch=min(max(abs(u-ax),abs(v-ay)) for u,v in cs)
        dpr=min(((u-ax)*ux+(v-ay)*uy) for u,v in cs)  # = 2*projection; Chebyshev >= |dpr|/2
        mins.setdefault(j,[]).append(dch); projmin.setdefault(j,[]).append(dpr)
print("period j: min Chebyshev over phases, min (u.dx+v.dy)/2 lower bound")
for j in sorted(mins):
    if j<86 or j>=NP-3: print(j, min(mins[j]), min(projmin[j])/2)
