# independent spot check: r* = min(min pair dist/2, 1 - max |c|) from live coordinate files
import sys, re
from decimal import Decimal as D, getcontext
getcontext().prec=60
import numpy as np
from collections import defaultdict
import itertools
rad={}
for l in open('raw/radius_txt_txt.txt'):
    p=l.split()
    if len(p)==2 and p[0].isdigit(): rad[int(p[0])]=D(p[1])
html=open('raw/ssp.html.redacted',encoding='latin-1').read()
for N in map(int,sys.argv[1:]):
    L=open(f'raw/ssp{N}.txt').read().split('\n')
    hdr=D(L[0].strip())
    rows=[l.split() for l in L[1:] if l.strip()]
    C=[(D(a),D(b),D(c)) for _,a,b,c in rows]
    assert len(C)==N, (len(C),N)
    X=np.array([[float(v) for v in c] for c in C])
    h0=2*float(hdr)*1.05; G=defaultdict(list)
    for i,p in enumerate(X): G[tuple((p//h0).astype(int))].append(i)
    P=[]
    for key,ids in G.items():
        for off in itertools.product((-1,0,1),repeat=3):
            for j in G.get((key[0]+off[0],key[1]+off[1],key[2]+off[2]),()):
                for i in ids:
                    if i<j: P.append((i,j))
    pairs=np.array(P)
    d=np.linalg.norm(X[pairs[:,0]]-X[pairs[:,1]],axis=1); idx=np.argsort(d)[:50]
    pmin=min(sum((C[i][k]-C[j][k])**2 for k in range(3)).sqrt() for i,j in pairs[idx])/2
    w=1-max(sum(v*v for v in c).sqrt() for c in C)
    rs=min(pmin,w)
    m=re.search(rf'name="ssp{N}".*?<td>&nbsp;&nbsp; ([0-9.]+)</td>',html)
    h=D(m.group(1))
    print(f"N={N} file_header={hdr} r*={rs:.15f} binding={'wall' if w<pmin else 'pair'} ssp.html={h} radius.txt={rad[N]} r*-radius.txt={float(rs-rad[N]):.6e} r*-html={float(rs-h):.3e}")
