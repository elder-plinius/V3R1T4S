# A: exact rational arithmetic (fractions). Independent design: witnesses + exhaustive neighbour bound, no sqrt.
import sys,re,io,tarfile,urllib.request,hashlib,math
from fractions import Fraction as Q
K=sys.argv[1]
def fetch(u):
    b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'V3R1T4S-crosscheck-A'}),timeout=120).read()
    print('#',u,hashlib.sha256(b).hexdigest()); return b
RT={}
for l in fetch('https://packomania.com/ssp/txt/radius.txt').decode().splitlines():
    s=l.split()
    if len(s)==2 and s[0].isdigit(): RT[int(s[0])]=s[1]
H={}
for m in re.finditer(r'name="ssp(\d+)"[^>]*>.*?</a>\s*</td>\s*<td>([^<]*)</td>',fetch('https://packomania.com/ssp/ssp.html').decode('latin-1')):
    H[int(m.group(1))]=m.group(2).replace('&nbsp;','').strip()
NS=[int(l.split(',')[0]) for l in open(K+'/object/ssp_radiustxt_errata.csv').read().split()[1:]]  # single N list: the errata CSV
tb=open(K+'/data/ssp_coords.tar.gz','rb').read(); print('# tarball',hashlib.sha256(tb).hexdigest())
want={f'ssp{n}.txt' for n in NS}; files={}
with tarfile.open(fileobj=io.BytesIO(tb)) as t:
    for m in t:
        if m.name.rsplit('/',1)[-1] in want: files[int(m.name.rsplit('/',1)[-1][3:-4])]=t.extractfile(m).read().decode()
M=Q(1,10**10); ok=0
for n in NS:
    P=[tuple(Q(v) for v in l.split()[1:4]) for l in files[n].splitlines() if len(l.split())>=4 and not l.startswith('#')]
    t=Q(RT[n]); h=Q(H[n]); 
    c1=len(P)==n
    # (2) exact witness: some pair with d^2 < (2(t-M))^2 or a centre with |c|^2 > (1-(t-M))^2
    a=t-M; F=[tuple(float(x) for x in p) for p in P]
    cell=float(2*h)*1.05; G={}
    for i,p in enumerate(F): G.setdefault(tuple(int(math.floor(x/cell)) for x in p),[]).append(i)
    d2min=None; wmax=max(sum(x*x for x in p) for p in P)
    for k,L in G.items():
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                for dz in(-1,0,1):
                    for j in G.get((k[0]+dx,k[1]+dy,k[2]+dz),()):
                        for i in L:
                            if i<j:
                                if sum((F[i][q]-F[j][q])**2 for q in range(3))<(float(2*h)*1.01)**2:
                                    d2=sum((P[i][q]-P[j][q])**2 for q in range(3))
                                    if d2min is None or d2<d2min: d2min=d2
    # any pair farther than cell is > 2h*1.05 so cannot be the minimum below 2(h+M)
    c2 = (d2min < (2*a)**2) or (wmax > (1-a)**2)
    lo=h-M; hi=h+M   # (3) r* in [h-M, h+M]  <=> min(d2min/4, (1-sqrt w)^2) bracket, checked without sqrt
    pair_ok = d2min>=(2*lo)**2 and (d2min<=(2*hi)**2 or True)
    wall_ok = wmax<=(1-lo)**2
    upper = d2min<=(2*hi)**2 or wmax>=(1-hi)**2
    c3 = pair_ok and wall_ok and upper
    v=c1 and c2 and c3; ok+=v
    print(n,RT[n],H[n],c1,c2,c3,'OK' if v else 'NO')
print('# confirmed',ok,'of',len(NS)); print('PASS' if ok==len(NS) else 'FAIL')
