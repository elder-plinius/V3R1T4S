from pathlib import Path
import sys
v=list(map(int,Path(sys.argv[1]).read_text().split()));n,l=v[:2];cur=v[2:2+n];mp=[[x] for x in cur];wp=[[] for _ in cur]
for m,w in enumerate(cur):wp[w].append(m)
for k in range(l):
 a,b=v[2+n+2*k:4+n+2*k];cur[a],cur[b]=cur[b],cur[a]
 for m in (a,b):
  assert cur[m] not in mp[m];mp[m].append(cur[m]);wp[cur[m]].append(m)
rows=[x+[y for y in range(n) if y not in x] for x in mp]+[x[::-1]+[y for y in range(n) if y not in x] for x in wp]
Path(sys.argv[2]).write_text('\n'.join(' '.join(str(x+1) for x in row) for row in rows)+'\n')
