#!/usr/bin/env python3
# Standalone stdlib checker (decimal prec 60). Fetches live ssp radius.txt, ssp.html and ssp_coords.tar.gz
# (or uses $SSP_TARBALL for a local copy of the archive), recomputes r* = min(min|ci-cj|/2, 1-max|ci|)
# for every N in object/ssp_radiustxt_errata.csv and checks: N spheres present; r* < radius.txt - 1e-10;
# |ssp.html - r*| <= 1e-10; object values reproduce (radius_txt, ssp_html exact strings; coord_rstar within 1e-15).
import sys,os,io,csv,tarfile,urllib.request,hashlib,decimal,collections
from decimal import Decimal as D
decimal.getcontext().prec=60
here=os.path.dirname(os.path.abspath(__file__)); obj=os.path.join(here,'..','object','ssp_radiustxt_errata.csv')
def fetch(u):
    b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'V3R1T4S-verify'}),timeout=600).read()
    print('# fetched',u,'sha256',hashlib.sha256(b).hexdigest()); return b
R={}
for line in fetch('https://packomania.com/ssp/txt/radius.txt').decode().split('\n'):
    p=line.split()
    if len(p)==2 and p[0].isdigit(): R[int(p[0])]=p[1]
txt=fetch('https://packomania.com/ssp/ssp.html').decode('latin-1'); H={}; i=0
while True:
    i=txt.find('name="ssp',i)
    if i<0: break
    j=txt.find('"',i+9); n=int(txt[i+9:j]); k=txt.find('<td',txt.find('</td>',j)); k=txt.find('>',k)+1; e=txt.find('</td>',k)
    H[n]=txt[k:e].replace('&nbsp;','').strip(); i=e
import json
CL=json.load(open(os.path.join(here,'CLAIM.json')))
osha=hashlib.sha256(open(obj,'rb').read()).hexdigest(); print('# object sha256',osha,'OK' if osha==CL['object_sha256'] else 'MISMATCH')
rows=list(csv.DictReader(open(obj))); need={int(r['N']) for r in rows}
tb=open(os.environ['SSP_TARBALL'],'rb').read() if os.environ.get('SSP_TARBALL') else fetch('https://packomania.com/ssp/txt/ssp_coords.tar.gz')
print('# tarball sha256',hashlib.sha256(tb).hexdigest()); got={}
with tarfile.open(fileobj=io.BytesIO(tb)) as t:
    for m in t:
        b=m.name.split('/')[-1]
        if b.startswith('ssp') and b.endswith('.txt') and b[3:-4].isdigit() and int(b[3:-4]) in need: got[int(b[3:-4])]=t.extractfile(m).read().decode()
E=D('1e-10'); bad=0
for row in rows:
    n=int(row['N']); pts=[[D(x) for x in f[1:4]] for f in (l.split() for l in got[n].split('\n') if l[:1]!='#') if len(f)>=4]
    s=2.5*float(H[n]); g=collections.defaultdict(list)
    for idx,p in enumerate(pts): g[tuple(int(float(c)//s) for c in p)].append(idx)
    m2=min(sum((pts[i][q]-pts[j][q])**2 for q in range(3)) for key,lst in g.items() for i in lst
           for a in(-1,0,1) for b in(-1,0,1) for c in(-1,0,1) for j in g.get((key[0]+a,key[1]+b,key[2]+c),[]) if j>i)
    r=min(m2.sqrt()/2, 1-max(sum(x*x for x in p).sqrt() for p in pts))
    ok = len(pts)==n and r < D(R[n])-E and abs(D(H[n])-r)<=E and row['radius_txt']==R[n] and row['ssp_html']==H[n] and abs(D(row['coord_rstar'])-r)<D('1e-15')
    bad+= not ok; print(n,R[n],H[n],str(r)[:22],'OK' if ok else 'MISMATCH')
print('# rows',len(rows),'failed',bad)
print('PASS' if osha==CL['object_sha256'] and bad==0 and len(rows)==90 else 'FAIL')
