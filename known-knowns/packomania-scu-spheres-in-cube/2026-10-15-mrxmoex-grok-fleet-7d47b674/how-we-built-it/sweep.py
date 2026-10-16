# p3: posted coords vs own 30-dec table radius, N=1..1000. float prefilter of near-min pairs/walls, then mpmath dps=50 on those.
import numpy as np, os, sys, time, datetime
RUN=os.path.abspath(os.path.dirname(__file__)+'/../../..'); sys.path.insert(0,RUN); import check as CK
mp=CK.mp; O=RUN+'/attempts/integrity'; prog=O+'/progress.tsv'
DEADLINE=datetime.datetime(2026,10,15,5,20,tzinfo=datetime.timezone.utc).timestamp()
done={int(l.split()[0]) for l in open(prog)} if os.path.exists(prog) else set()
for n in range(1,1001):
    if n in done: continue
    if time.time()>DEADLINE: break
    C=CK.load(f'{RUN}/data/coords_all/scu{n}.txt'); X=np.array([[float(v) for v in c] for c in C])
    if len(C)!=n: open(prog,'a').write(f"{n}\tCOUNT_MISMATCH {len(C)}\n"); continue
    w=min(mp.mpf('0.5')-max(abs(v) for v in c) for c in C)
    if n>1:
        D=np.sqrt(((X[:,None]-X[None])**2).sum(-1)); np.fill_diagonal(D,9); I,J=np.where(np.triu(D<D.min()+1e-9,1))
        d=min(mp.sqrt(sum((C[i][k]-C[j][k])**2 for k in range(3))) for i,j in zip(I,J)); r=min(d/2,w)
    else: r=w
    t=CK.table(n,RUN+'/data/radius.txt'); diff=r-t
    flag='MISMATCH' if abs(diff)>mp.mpf('1e-25') else 'OK'
    open(prog,'a').write(f"{n}\t{mp.nstr(diff,6)}\t{flag}\n")
with open(O+'/p3_findings.txt','w') as f:
    L=[l.split('\t') for l in open(prog).read().strip().split('\n')]
    f.write(f"# p3 sweep {datetime.datetime.now(datetime.timezone.utc).isoformat()} checked {len(L)} N; threshold |r*-table|>1e-25 (30-dec rounding ~1e-30)\n")
    for x in L:
        if x[-1].strip()!='OK': f.write('\t'.join(x).strip()+'\n')
