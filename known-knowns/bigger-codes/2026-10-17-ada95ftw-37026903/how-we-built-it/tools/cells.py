"""Parse live Andw.html into {(n,d,w): (lo, hi or None, raw)} for w as printed (w<=n/2 columns)."""
import re,json,sys
def parse(path):
    h=open(path,encoding='latin-1').read()
    out={}
    secs=re.split(r'<h1><a name="d(\d+)">',h)
    for i in range(1,len(secs),2):
        d=int(secs[i]); body=secs[i+1].split('<h1>')[0]
        for row in re.findall(r'<tr>(.*?)</tr>',body,re.S):
            m=re.search(r'<th>(\d+)</th>',row)
            if not m: continue
            n=int(m.group(1))
            cells=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
            for j,c in enumerate(cells):
                t=re.sub(r'<sup>.*?</sup>','',c,flags=re.S); t=re.sub(r'<[^>]*>','',t).strip()
                if not re.search(r'\d',t): continue
                w=d//2+1+j
                if '-' in t:
                    a,b=t.split('-',1); lo=int(re.findall(r'\d+',a)[0]); bb=re.findall(r'\d+',b); hi=int(bb[0]) if bb else None
                else:
                    lo=hi=int(re.findall(r'\d+',t)[0])
                out[(n,d,w)]=(lo,hi,t)
    return out
if __name__=='__main__':
    c=parse(sys.argv[1]); print(len(c)); print(sum(1 for v in c.values() if v[1] is None),'cells without numeric hi')
    for k in [(31,12,10),(32,12,16),(16,6,7),(18,8,8),(29,6,12)]: print(k,c.get(k))
