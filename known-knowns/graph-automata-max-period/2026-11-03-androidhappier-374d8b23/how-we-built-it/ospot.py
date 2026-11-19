#!/usr/bin/env python3
"""Self-break spot checker (numpy, written from the OEIS A357951 definition; shares no code with otA.c/otB.go).
For each graph6 argument: all 2^(2n) outer-totalistic rules (B,S subsets of {0..n-1}) x all 2^n starts, vectorised
over rules. Iterate f 2^n times from every start (lands on the cycle), then find the least k>=1 with f^k(y)=y.
Prints per-graph maximum and the list of (B,S) rules reaching it (rules restricted to counts <= maxdeg are shown)."""
import sys, numpy as np
def dec(s):
    d=[ord(c)-63 for c in s]; n=d[0]; b=''.join(format(x,'06b') for x in d[1:]); adj=[0]*n; k=0
    for j in range(1,n):
        for i in range(j):
            if b[k]=='1': adj[i]|=1<<j; adj[j]|=1<<i
            k+=1
    return n,adj
for g in sys.argv[1:]:
    n,adj=dec(g); N=1<<n; K=2*n; R=np.arange(1<<K,dtype=np.int32)[:,None]
    S=np.arange(N)
    nxt=np.zeros((1<<K,N),dtype=np.int16)
    for v in range(n):
        c=np.array([bin(s&adj[v]).count('1') for s in range(N)]); own=(S>>v)&1
        bit=c+n*own                       # rule bit consulted by vertex v in state s
        nxt|=(((R>>bit[None,:])&1)<<v).astype(np.int16)
    y=np.broadcast_to(S,(1<<K,N)).copy()
    for _ in range(N): y=np.take_along_axis(nxt,y,1)
    L=np.zeros(y.shape,dtype=np.int16); z=np.take_along_axis(nxt,y,1); k=1
    while True:
        hit=(z==y)&(L==0); L[hit]=k
        if (L>0).all(): break
        z=np.take_along_axis(nxt,z,1); k+=1
    per=L.max(1); M=int(per.max()); D=max(bin(a).count('1') for a in adj)
    rules=set()
    for r in np.nonzero(per==M)[0]:
        r=int(r); Bs=tuple(c for c in range(n) if (r>>c)&1 and c<=D); Ss=tuple(c for c in range(n) if (r>>(n+c))&1 and c<=D)
        rules.add((Bs,Ss))
    import resource; print(g,'max',M,'maxdeg',D,'rules_reaching_max(restricted to counts<=maxdeg)',sorted(rules),"peak_rss_MB",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss//1024,flush=True)
