import sys, lzma, networkx as nx
exec(open(sys.path[0]+'/my_check.py').read().split('def main')[0])
def key(N, adj):
    deg=[len(a) for a in adj]; rem=N; layer=[v for v in range(N) if deg[v]==1]; gone=[False]*N
    while rem>2:
        nxt=[]
        for v in layer:
            gone[v]=True; rem-=1
            for w in adj[v]:
                if not gone[w]:
                    deg[w]-=1
                    if deg[w]==1: nxt.append(w)
        layer=nxt
    cs=[v for v in range(N) if not gone[v]]
    if len(cs)==1: return "U"+code(adj,cs[0],-1)
    a,b=cs; ca,cb=code(adj,a,b),code(adj,b,a); return "B"+min(ca,cb)+"|"+max(ca,cb)
path,N=sys.argv[1],int(sys.argv[2]); op=lzma.open if path.endswith('.xz') else open
cert=set()
for raw in op(path,'rt'):
    if raw.strip():
        f=raw.split(';'); adj=[[] for _ in range(N)]
        for e in f[1].split(','):
            u,v=map(int,e.split('-')); adj[u].append(v); adj[v].append(u)
        cert.add(key(N,adj))
g=miss=0
for T in nx.nonisomorphic_trees(N):
    g+=1; adj=[list(T[v]) for v in range(N)]; k=key(N,adj)
    if k in cert: cert.discard(k)
    else: miss+=1
print(f"n={N} networkx_generated={g} missing={miss} extra={len(cert)}")
