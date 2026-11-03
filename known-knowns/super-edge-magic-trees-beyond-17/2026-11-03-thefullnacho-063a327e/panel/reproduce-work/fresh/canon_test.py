import itertools, random
from fresh_check import canon, free_trees
def prufer_edges(seq, n):
    deg=[1]*n
    for x in seq: deg[x]+=1
    E=[]
    for x in seq:
        for v in range(n):
            if deg[v]==1: E.append((v,x)); deg[v]-=1; deg[x]-=1; break
    u,w=[v for v in range(n) if deg[v]==1]; E.append((u,w)); return E
def adjof(E,n):
    a=[[] for _ in range(n)]
    for u,v in E: a[u].append(v); a[v].append(u)
    return a
for n in range(3,9):
    s={canon(n,adjof(prufer_edges(seq,n),n)) for seq in itertools.product(range(n),repeat=n-2)}
    print(n,len(s),free_trees(n),len(s)==free_trees(n))
random.seed(1); bad=0
for _ in range(3000):
    n=random.randint(10,20); seq=[random.randrange(n) for _ in range(n-2)]; E=prufer_edges(seq,n)
    p=list(range(n)); random.shuffle(p); E2=[(p[u],p[v]) for u,v in E]
    bad+= canon(n,adjof(E,n))!=canon(n,adjof(E2,n))
print("relabel mismatches",bad)
