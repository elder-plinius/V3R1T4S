import sys, subprocess, hashlib
# usage: python3 gentreeg_xcheck.py PATH_TO_GENTREEG CERT_DIR  (nauty 2.8.9 gentreeg built from source)
GENTREEG, CERTS = sys.argv[1], sys.argv[2]
# own canonical form: centre-rooted AHU with integer ids via shared dict (bottom-up by BFS layers)
def canon(n, adj):
    deg=[len(a) for a in adj]; layer=[v for v in range(n) if deg[v]<=1]; rem=n; gone=[False]*n
    while rem>2:
        nxt=[]
        for v in layer:
            gone[v]=True; rem-=1
            for w in adj[v]:
                if not gone[w]:
                    deg[w]-=1
                    if deg[w]==1: nxt.append(w)
        layer=nxt
    cs=[v for v in range(n) if not gone[v]]
    best=None
    for c in cs:
        # iterative postorder
        par={c:-1}; order=[c]; i=0
        while i<len(order):
            u=order[i]; i+=1
            for w in adj[u]:
                if w!=par[u]: par[w]=u; order.append(w)
        s={}
        for u in reversed(order):
            s[u]="["+"".join(sorted(s[w] for w in adj[u] if w!=par[u]))+"]"
        if best is None or s[c]<best: best=s[c]
    return hashlib.sha1(best.encode()).digest()
def gen(n):
    out=subprocess.run([GENTREEG,"-q","-p",str(n)],capture_output=True,text=True,check=True).stdout
    S=set(); cnt=0
    for line in out.splitlines():
        p=list(map(int,line.split())); assert len(p)==n
        adj=[[] for _ in range(n)]
        for i in range(1,n):
            j=p[i]-1; adj[i].append(j); adj[j].append(i)
        assert p[0]==0
        S.add(canon(n,adj)); cnt+=1
    return cnt,S
A={18:123867,19:317955,20:823065}
for n in (18,19,20):
    cnt,G=gen(n)
    seen={}; bad=0; lines=0
    for line in open(f"{CERTS}/cert_n{n}.txt"):
        if not line.strip(): continue
        lines+=1
        f=line.rstrip("\n").split(";")
        nn=int(f[0]); E=[tuple(map(int,e.split("-"))) for e in f[1].split(",")]; L=list(map(int,f[2].split(",")))
        ok = nn==n and len(E)==n-1 and len(L)==n and sorted(L)==list(range(1,n+1))
        adj=[[] for _ in range(n)]
        for u,v in E:
            if not(0<=u<n and 0<=v<n and u!=v): ok=False; break
            adj[u].append(v); adj[v].append(u)
        if ok:
            # connectivity
            st=[0]; vis={0}
            while st:
                u=st.pop()
                for w in adj[u]:
                    if w not in vis: vis.add(w); st.append(w)
            ok = len(vis)==n
        if ok:
            sums=sorted(L[u]+L[v] for u,v in E); ok = sums==list(range(sums[0],sums[0]+n-1))
        if not ok: bad+=1; continue
        c=canon(n,adj); seen[c]=seen.get(c,0)+1
    dup=sum(1 for v in seen.values() if v>1)
    print(f"n={n} gentreeg={cnt} gentreeg_distinct={len(G)} A000055={A[n]} cert_lines={lines} bad={bad} distinct={len(seen)} dup={dup} missing={len(G-set(seen))} extra={len(set(seen)-G)}",flush=True)
