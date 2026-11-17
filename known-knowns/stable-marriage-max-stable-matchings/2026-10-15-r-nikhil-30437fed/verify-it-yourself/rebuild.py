from pathlib import Path
import sys
v=list(map(int,Path(sys.argv[1]).read_text().split()));n,L=v[:2];cur=v[2:2+n];assert sorted(cur)==list(range(n));men=[[w] for w in cur];women=[[] for _ in cur]
for m,w in enumerate(cur):women[w].append(m)
at=2+n
for _ in range(L):
 k=v[at];cycle=v[at+1:at+1+k];at+=1+k;assert len(cycle)==k and 2<=k<=n and len(set(cycle))==k and all(0<=m<n for m in cycle)
 dest=[cur[cycle[(j+1)%k]] for j in range(k)]
 for m,w in zip(cycle,dest):assert w not in men[m];men[m].append(w);women[w].append(m);cur[m]=w
assert at==len(v)
rows=[p+[w for w in range(n) if w not in p] for p in men]+[p[::-1]+[m for m in range(n) if m not in p] for p in women]
Path(sys.argv[2]).write_text('\n'.join(' '.join(str(v+1) for v in row) for row in rows)+'\n')
