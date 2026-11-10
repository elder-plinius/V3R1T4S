# B: mpmath dps=50, sweep-line on x (sorted), computes r* explicitly.
import sys,re,io,tarfile,urllib.request,hashlib
import mpmath as mp; mp.mp.dps=50
K=sys.argv[1]
def fetch(u):
    b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'V3R1T4S-crosscheck-B'}),timeout=120).read()
    print('#',u,hashlib.sha256(b).hexdigest()); return b
rt={int(a):b for a,b in (l.split() for l in fetch('https://packomania.com/ssp/txt/radius.txt').decode().splitlines() if l and l[0].isdigit())}
html=fetch('https://packomania.com/ssp/ssp.html').decode('latin-1'); ht={}
for row in html.split('<tr>'):
    m=re.search(r'name="ssp(\d+)"',row)
    if m:
        cells=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        ht[int(m.group(1))]=re.sub(r'<[^>]+>|&nbsp;','',cells[1]).strip()
NS=[int(l.split(',')[0]) for l in open(K+'/object/ssp_radiustxt_errata.csv').read().split()[1:]]  # single N list: the errata CSV
tf=tarfile.open(K+'/data/ssp_coords.tar.gz'); names={m.name.split('/')[-1]:m for m in tf.getmembers()}
lo=mp.mpf('1e-10'); good=0
for n in NS:
    rows=[l.split() for l in tf.extractfile(names[f'ssp{n}.txt']).read().decode().splitlines() if not l.startswith('#')]
    C=[tuple(mp.mpf(x) for x in r[1:4]) for r in rows if len(r)>=4]
    fl=sorted(range(len(C)),key=lambda i:float(C[i][0])); X=[tuple(map(float,C[i])) for i in fl]
    best=9.0; cand=[]
    for a in range(len(X)):
        b=a+1
        while b<len(X) and X[b][0]-X[a][0]<best+1e-9:
            d=((X[a][0]-X[b][0])**2+(X[a][1]-X[b][1])**2+(X[a][2]-X[b][2])**2)**.5
            if d<best+1e-9:
                cand.append((d,fl[a],fl[b]))
                if d<best: best=d
            b+=1
    pr=min(mp.sqrt(sum((C[i][k]-C[j][k])**2 for k in range(3))) for d,i,j in cand if d<best+1e-9)/2
    wall=1-max(mp.sqrt(sum(v*v for v in c)) for c in C)
    r=min(pr,wall); t=mp.mpf(rt[n]); h=mp.mpf(ht[n])
    v=len(C)==n and r<t-lo and abs(h-r)<=lo; good+=v
    print(n,rt[n],ht[n],mp.nstr(r,20),mp.nstr(r-t,6),mp.nstr(h-r,4),'pair' if pr<wall else 'wall','OK' if v else 'NO')
print('# confirmed',good,'of',len(NS)); print('PASS' if good==len(NS) else 'FAIL')
