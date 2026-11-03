import sys, subprocess, hashlib
G, C = sys.argv[1], sys.argv[2]
A = {18:123867, 19:317955, 20:823065}  # OEIS A000055
def canon(n, adj):
    # find centre(s) by repeated leaf stripping
    deg=[len(a) for a in adj]; leaves=[v for v in range(n) if deg[v]==1]; alive=n; dead=[0]*n
    while alive>2:
        nl=[]
        for v in leaves:
            dead[v]=1; alive-=1
            for w in adj[v]:
                if not dead[w]:
                    deg[w]-=1
                    if deg[w]==1: nl.append(w)
        leaves=nl
    best=None
    for c in [v for v in range(n) if not dead[v]]:
        par=[-2]*n; par[c]=-1; order=[c]
        for u in order:
            for w in adj[u]:
                if par[w]==-2: par[w]=u; order.append(w)
        lab={}
        for u in reversed(order):
            lab[u]=tuple(sorted(lab[w] for w in adj[u] if w!=par[u]))
        t=repr(lab[c])
        if best is None or t<best: best=t
    return hashlib.sha256(best.encode()).digest()
ok_all=True
for n in (18,19,20):
    out=subprocess.run([G,"-q","-p",str(n)],capture_output=True,text=True,check=True).stdout.split("\n")
    gs=set(); gc=0
    for line in out:
        if not line.strip(): continue
        p=list(map(int,line.split())); gc+=1
        adj=[[] for _ in range(n)]
        for i in range(1,n):
            j=p[i]-1; adj[i].append(j); adj[j].append(i)
        gs.add(canon(n,adj))
    cs={}; bad=0; lines=0
    for line in open(f"{C}/cert_n{n}.txt"):
        if not line.strip(): continue
        lines+=1
        try:
            f=line.rstrip("\n").split(";")
            nn=int(f[0]); E=[tuple(int(x) for x in e.split("-")) for e in f[1].split(",")]; L=[int(x) for x in f[2].split(",")]
            assert nn==n and len(E)==n-1 and all(len(e)==2 for e in E)
            assert sorted(L)==list(range(1,n+1))
            adj=[[] for _ in range(n)]
            for u,v in E:
                assert 0<=u<n and 0<=v<n and u!=v
                adj[u].append(v); adj[v].append(u)
            seen={0}; st=[0]
            while st:
                u=st.pop()
                for w in adj[u]:
                    if w not in seen: seen.add(w); st.append(w)
            assert len(seen)==n
            s=sorted(L[u]+L[v] for u,v in E)
            assert all(s[i+1]-s[i]==1 for i in range(n-2))
        except Exception:
            bad+=1; continue
        k=canon(n,adj); cs[k]=cs.get(k,0)+1
    dup=sum(1 for v in cs.values() if v>1); miss=len(gs-cs.keys()); extra=len(cs.keys()-gs)
    good = gc==len(gs)==A[n]==lines==len(cs) and not (bad or dup or miss or extra)
    ok_all &= good
    print(f"n={n} gentreeg_lines={gc} gentreeg_distinct={len(gs)} A000055={A[n]} cert_lines={lines} bad={bad} distinct={len(cs)} dup={dup} missing={miss} extra={extra} -> {'PASS' if good else 'FAIL'}", flush=True)
print("OVERALL", "PASS" if ok_all else "FAIL")
