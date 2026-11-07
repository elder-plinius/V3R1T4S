# C: stdlib decimal (prec 60) + uniform grid; extracts tarball members via tar CLI-free streaming; reads html by text scan.
import sys,io,tarfile,urllib.request,hashlib,decimal,collections
from decimal import Decimal as D
decimal.getcontext().prec=60
K=sys.argv[1]
def fetch(u):
    b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'V3R1T4S-crosscheck-C'}),timeout=120).read()
    print('#',u,hashlib.sha256(b).hexdigest()); return b
R={}
for line in fetch('https://packomania.com/ssp/txt/radius.txt').decode().split('\n'):
    p=line.split()
    if len(p)==2 and p[0].isdigit(): R[int(p[0])]=D(p[1])
Hs={}
txt=fetch('https://packomania.com/ssp/ssp.html').decode('latin-1')
i=0
while True:
    i=txt.find('name="ssp',i)
    if i<0: break
    j=txt.find('"',i+9); n=int(txt[i+9:j]); k=txt.find('<td',txt.find('</td>',j)); k=txt.find('>',k)+1; e=txt.find('</td>',k)
    Hs[n]=D(txt[k:e].replace('&nbsp;','').strip()); i=e
NS=[int(l.split(',')[0]) for l in open(K+'/object/ssp_radiustxt_errata.csv').read().split()[1:]]  # single N list: the errata CSV
need=set(NS); got={}
with tarfile.open(K+'/data/ssp_coords.tar.gz','r:gz') as t:
    for m in t:
        b=m.name.split('/')[-1]
        if b.startswith('ssp') and b.endswith('.txt') and b[3:-4].isdigit() and int(b[3:-4]) in need: got[int(b[3:-4])]=t.extractfile(m).read().decode()
E=D('1e-10'); cnt=0
for n in NS:
    pts=[]
    for l in got[n].split('\n'):
        f=l.split()
        if l[:1]!='#' and len(f)>=4: pts.append([D(x) for x in f[1:4]])
    h=float(Hs[n]); g=collections.defaultdict(list); s=2.5*h
    for idx,p in enumerate(pts): g[(int(float(p[0])//s),int(float(p[1])//s),int(float(p[2])//s))].append(idx)
    m2=None
    for key,lst in g.items():
        nb=[q for a in(-1,0,1) for b in(-1,0,1) for c in(-1,0,1) for q in g.get((key[0]+a,key[1]+b,key[2]+c),[])]
        for i in lst:
            for j in nb:
                if j>i:
                    d2=sum((pts[i][k]-pts[j][k])**2 for k in range(3))
                    if m2 is None or d2<m2: m2=d2
    rp=m2.sqrt()/2; rw=1-max(sum(x*x for x in p).sqrt() for p in pts); r=min(rp,rw)
    ok=len(pts)==n and r<R[n]-E and abs(Hs[n]-r)<=E; cnt+=ok
    print(n,R[n],Hs[n],str(r)[:22],'%.6g'%float(r-R[n]),'%.3g'%float(Hs[n]-r),'OK' if ok else 'NO')
print('# confirmed',cnt,'of',len(NS)); print('PASS' if cnt==len(NS) else 'FAIL')
