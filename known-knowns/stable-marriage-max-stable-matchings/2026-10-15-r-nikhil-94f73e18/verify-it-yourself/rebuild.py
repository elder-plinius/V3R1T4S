from pathlib import Path
import sys,json
z=json.loads(Path(sys.argv[1]).read_text());n=z['n'];cur=z['initial'][:];assert sorted(cur)==list(range(n));men=[[w] for w in cur];women=[[] for _ in cur]
for m,w in enumerate(cur):women[w].append(m)
for cycle in z['cycles']:
 assert 2<=len(cycle)<=n and len(set(cycle))==len(cycle) and all(0<=a<n for a in cycle)
 dest=[cur[cycle[(j+1)%len(cycle)]] for j in range(len(cycle))]
 for m,w in zip(cycle,dest):assert w not in men[m];men[m].append(w);women[w].append(m);cur[m]=w
rows=[p+[w for w in range(n) if w not in p] for p in men]+[p[::-1]+[m for m in range(n) if m not in p] for p in women]
Path(sys.argv[2]).write_text('\n'.join(' '.join(str(v+1) for v in row) for row in rows)+'\n')
