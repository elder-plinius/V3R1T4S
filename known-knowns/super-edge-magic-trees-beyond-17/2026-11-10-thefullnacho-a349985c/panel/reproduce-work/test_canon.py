import sys, itertools, random
sys.path.insert(0, '.')
from sem_check import canon, a000055
def prufer_tree(seq, n):
    deg=[1]*n
    for x in seq: deg[x]+=1
    edges=[]
    for x in seq:
        leaf=min(i for i in range(n) if deg[i]==1)
        edges.append((leaf,x)); deg[leaf]-=1; deg[x]-=1
    u,v=[i for i in range(n) if deg[i]==1]
    edges.append((u,v)); return edges
for n in range(3,10):
    keys=set()
    for seq in itertools.product(range(n),repeat=n-2):
        adj=[[] for _ in range(n)]
        for u,v in prufer_tree(seq,n): adj[u].append(v); adj[v].append(u)
        keys.add(canon(n,adj))
    print(n,len(keys),a000055(n),len(keys)==a000055(n))
