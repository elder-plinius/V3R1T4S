"""Reconstruct an explicit clone-overlap completion; no counting or searching."""
import pathlib,itertools,re,sys
source,completion,output=map(pathlib.Path,sys.argv[1:4]);n=int(sys.argv[4]);v=int(sys.argv[5]);new=n+1
base={}
for line in source.read_text().splitlines():
 m=re.fullmatch(r'(\d+) (\d+) (\d+) ([123])N([123])',line)
 if not m:raise ValueError('malformed source')
 a,b,c,i,j=map(int,m.groups());t=(a,b,c)
 if not 1<=a<b<c<=n or t in base:raise ValueError('source triple')
 base[t]=(i,j)
if set(base)!=set(itertools.combinations(range(1,n+1),3)):raise ValueError('incomplete source')
rows=[(t,*ij) for t,ij in base.items()]
for a,b in itertools.combinations(range(1,n+1),2):
 if v in(a,b):continue
 t=(a,b,new);old=tuple(sorted((a,b,v)));i,j=base[old];x=old[i-1];x=new if x==v else x;rows.append((t,t.index(x)+1,j))
seen=set()
for line in completion.read_text().splitlines():
 m=re.fullmatch(r'(\d+) (\d+) (\d+) ([123])N([123])',line)
 if not m:raise ValueError('malformed completion')
 a,b,c,i,j=map(int,m.groups());t=(a,b,c)
 if not 1<=a<b<c==new or v not in t or t in seen:raise ValueError('completion triple')
 seen.add(t);rows.append((t,i,j))
if len(seen)!=n-1:raise ValueError('incomplete completion')
output.write_text(''.join(f'{t[0]} {t[1]} {t[2]} {i}N{j}\n' for t,i,j in rows))
