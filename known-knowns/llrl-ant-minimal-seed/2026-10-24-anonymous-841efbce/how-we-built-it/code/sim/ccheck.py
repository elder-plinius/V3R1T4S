#!/usr/bin/env python3
"""Checker C: independent pure-Python simulator + exact translate certificate (dict grid, no shared code).
usage: ccheck.py RULE NSTEPS "x,y,c;x,y,c;..."  (empty string = blank)
Prints least onset of the tail highway (backward extension of the periodic read word), P, D, and cert at onset / onset-1."""
import sys
H=[(0,-1),(1,0),(0,1),(-1,0)]
def run(rule,N,seed):
    n=len(rule); g=dict(seed); x=y=h=0; rd=[]; poses=[]; snaps={}
    for t in range(N):
        poses.append((x,y,h)); c=g.get((x,y),0); rd.append(c)
        h=(h+(1 if rule[c]=='R' else 3))%4; g[(x,y)]=(c+1)%n; x+=H[h][0]; y+=H[h][1]
    return rd,poses
def state_at(rule,seed,t):
    n=len(rule); g=dict(seed); x=y=h=0
    for _ in range(t):
        c=g.get((x,y),0); h=(h+(1 if rule[c]=='R' else 3))%4; g[(x,y)]=(c+1)%n; x+=H[h][0]; y+=H[h][1]
    return g,(x,y,h)
def cert(rule,seed,t,P):
    n=len(rule); g0,(x,y,h)=state_at(rule,seed,t); g=dict(g0); A=[]
    for _ in range(P):
        A.append((x,y)); c=g.get((x,y),0); h2=(h+(1 if rule[c]=='R' else 3))%4; g[(x,y)]=(c+1)%n; h=h2; x+=H[h][0]; y+=H[h][1]
    x0,y0,h0=state_at(rule,seed,t)[1]; D=(x-x0,y-y0)
    if h!=h0 or D==(0,0): return False,D
    sup=[k for k,v in g0.items() if v]+[k for k,v in g.items() if v]
    mp=max(a*D[0]+b*D[1] for a,b in sup) if sup else -10**9
    for (cx,cy) in set(A):
        while cx*D[0]+cy*D[1]<=mp:
            if g.get((cx+D[0],cy+D[1]),0)!=g0.get((cx,cy),0): return False,D
            cx+=D[0]; cy+=D[1]
    return True,D
if __name__=='__main__':
    rule,N=sys.argv[1],int(sys.argv[2]); s=sys.argv[3] if len(sys.argv)>3 else ''
    seed={}
    for it in filter(None,s.split(';')):
        a,b,c=map(int,it.split(',')); seed[(a,b)]=c
    rd,_=run(rule,N,seed); P=None
    for p in range(1,1001):
        if all(rd[u]==rd[u+p] for u in range(N-5000,N-p)): P=p; break
    if P is None: print("NO_PERIOD"); sys.exit()
    t=N-P
    while t>0 and rd[t-1]==rd[t-1+P]: t-=1
    ok,D=cert(rule,seed,t,P); ok1,_=cert(rule,seed,t-1,P) if t>0 else (None,None)
    print(f"C rule={rule} onset={t} P={P} D={D} cert_onset={ok} cert_onset-1={ok1}")
