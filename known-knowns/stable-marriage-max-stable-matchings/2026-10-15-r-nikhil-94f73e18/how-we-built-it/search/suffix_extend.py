from pathlib import Path
import sys,json,subprocess,re,time,hashlib
source=Path(sys.argv[1]);out=Path(sys.argv[2]);seconds=float(sys.argv[3]);maxdepth=int(sys.argv[4]);v=list(map(int,source.read_text().split()));n,L=v[:2];initial=v[2:2+n];base=[v[2+n+2*k:4+n+2*k] for k in range(L)];counter=Path(__file__).with_name('smcount');deadline=time.monotonic()+seconds
best=0;nodes=0;cutoff=False;records=[]
def construct(cycles):
 cur=initial[:];men=[[w] for w in cur];women=[[] for _ in cur]
 for m,w in enumerate(cur):women[w].append(m)
 for c in cycles:
  assert len(c)>=2 and len(set(c))==len(c);dest=[cur[c[(j+1)%len(c)]] for j in range(len(c))]
  for a,w in zip(c,dest):assert w not in men[a];men[a].append(w);women[w].append(a);cur[a]=w
 rows=[p+[w for w in range(n) if w not in p] for p in men]+[p[::-1]+[m for m in range(n) if m not in p] for p in women]
 text='\n'.join(' '.join(str(z+1) for z in row) for row in rows)+'\n'
 return cur,men,text

def cycles_at(cycles,minimum):
 cur,men,_=construct(cycles);edges=[[b for b in range(n) if a!=b and cur[b] not in men[a]] for a in range(n)];found=[]
 def walk(p):
  if p[0] in edges[p[-1]] and len(p)>=minimum:found.append(p[:])
  for b in edges[p[-1]]:
   if b>p[0] and b not in p:walk(p+[b])
 for a in range(n):walk([a])
 return found

def visit(extra):
 global best,nodes,cutoff
 if time.monotonic()>deadline or nodes>=10000:cutoff=True;return
 allcycles=base+extra;cur,men,text=construct(allcycles);p=Path(str(out)+'.scratch.prefs');p.write_text(text)
 z=subprocess.run([str(counter),'count',str(p)],capture_output=True,text=True,timeout=60,check=True);value=int(re.search(r'count_poset: (\d+)',z.stdout)[1]);nodes+=1
 records.append(dict(extra=extra,count=value));
 if value>best:
  best=value;stem=str(out)+f'.n{n}.c{value}';Path(stem+'.prefs').write_text(text);Path(stem+'.json').write_text(json.dumps(dict(n=n,initial=initial,cycles=allcycles,extra=extra,source_word_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),count=value),indent=2)+'\n');print(json.dumps(dict(best=value,node=nodes,extra=extra)),flush=True)
 if len(extra)<maxdepth:
  for c in cycles_at(allcycles,3 if not extra else 2):
   visit(extra+[c])
   if cutoff:return
visit([])
result=dict(n=n,best=best,nodes=nodes,maxdepth=maxdepth,cutoff=cutoff,source_word_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),records=records)
Path(str(out)+'.results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'}))
