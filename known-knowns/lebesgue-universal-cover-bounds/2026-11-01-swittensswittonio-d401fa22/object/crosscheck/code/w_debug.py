import sys,re,collections; sys.path.insert(0,'code')
from leafdec import *
c=Cert('work/cert_B_08344.bin')
DUMP='<previous-run leaf dump (not shipped)>'
rows=[]
for line in open(DUMP,encoding='ascii',errors='ignore'):
    if line.startswith('LEAF '):
        m=re.match(r'LEAF (\d+) \[([^\]]*)\] (\S+)',line)
        rows.append((float(m.group(3)),int(m.group(1)),tuple(float(x) for x in m.group(2).split(','))))
rows.sort(); sel=rows[:1000]
print('distinct boxes',len({(s,b) for _,s,b in sel}))
dup=collections.Counter((s,b) for _,s,b in sel); print([ (k[0],v) for k,v in dup.items() if v>1][:10])
import json
S={ (d['seed'],tuple(d['box'])) for d in json.load(open('work/sample.json')) if 'W' in d['strata']}
miss=[(lb,s,b) for lb,s,b in sel if (s,b) not in S]
for lb,s,b in miss:
    print('MISS',lb,s,c.leaves[s],b)
    if c.leaves[s]<=20000:
        # nearest box
        best=min(c.walk(s),key=lambda t:sum(abs(x-y) for x,y in zip(t[2],b))); print(' nearest',best[2], sum(abs(x-y) for x,y in zip(best[2],b)))
    else:
        ix=BlockIndex(c,s); q=0;bb=ix.root
        while ix.bits[q]==1:
            c1,c2=c.split(bb); w=(bb[1],bb[3],CIRC5*bb[5],bb[7],bb[9]); ax=int(np.argmax(w))
            if b[2*ax]<bb[2*ax]: q+=1; bb=c1
            else: q=ix.end(q+1); bb=c2
        print(' reached leaf',bb,[x-y for x,y in zip(bb,b)])
