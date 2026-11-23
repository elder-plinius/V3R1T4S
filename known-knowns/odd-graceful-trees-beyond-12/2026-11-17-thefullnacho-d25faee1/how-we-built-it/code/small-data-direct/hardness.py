import sys, statistics
def diam(n, edges):
    a=[[] for _ in range(n)]
    for u,v in edges: a[u].append(v); a[v].append(u)
    def bfs(s):
        d=[-1]*n; d[s]=0; q=[s]
        for x in q:
            for w in a[x]:
                if d[w]<0: d[w]=d[x]+1; q.append(w)
        m=max(d); return d.index(m), m
    return bfs(bfs(0)[0])[1]
for f in sys.argv[1:]:
    rows=[]
    for line in open(f):
        p=line.strip().split(';'); n=int(p[0]); edges=[tuple(map(int,x.split('-'))) for x in p[1].split(',')]
        nodes=int(p[3]) if p[2] else int(p[3].split()[1])
        deg=[0]*n
        for u,v in edges: deg[u]+=1; deg[v]+=1
        rows.append((nodes, diam(n,edges), max(deg), sum(1 for d in deg if d==1), p[1]))
    ns=[r[0] for r in rows]
    print("%s: trees=%d median_nodes=%d mean=%.0f max=%d max/median=%.0f" % (f, len(rows), statistics.median(ns), statistics.mean(ns), max(ns), max(ns)/max(1,statistics.median(ns))))
    by={}
    for r in rows: by.setdefault(r[1],[]).append(r[0])
    print("  by diameter: " + "  ".join("d%d:n=%d,med=%d,max=%d" % (d,len(v),statistics.median(v),max(v)) for d,v in sorted(by.items())))
    for r in sorted(rows, reverse=True)[:3]:
        print("  hardest: nodes=%d diam=%d maxdeg=%d leaves=%d edges=%s" % r)
