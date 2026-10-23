# Integrity sweep: posted coords vs own table radius. usage: sweep2.py ssp|scu
# r* = min(dmin/2, wall); scu wall = 1/2 - max_i max|x_k| (cube [-1/2,1/2]^3); ssp wall = 1 - max_i |c_i| (container radius 1).
# Float (cKDTree) prefilter selects pairs within 1e-9 of min distance and centers within 1e-9 of the max wall term; those are recomputed in mpmath dps=50.
import sys, os, re, time, numpy as np, mpmath as mp
from scipy.spatial import cKDTree
mp.mp.dps=50
CAT=sys.argv[1]; W=os.path.abspath(os.path.dirname(__file__)+'/..'); D=f'{W}/data/{CAT}'
OUT=f'{W}/results_{CAT}.tsv'; MARGIN=mp.mpf('1e-10')
tab={}
for l in open(D+'/radius.txt'):
    s=l.split()
    if len(s)>=2 and not l.startswith('#'): tab[int(s[0])]=s[1]
done=set()
if os.path.exists(OUT): done={int(l.split('\t')[0]) for l in open(OUT) if l[0].isdigit()}
else: open(OUT,'w').write("N\ttable_radius\tdecimals\trecomputed_r\tgap\tbinding\tpair_r\twall_r\tclass\n")
def load(n):
    S=[]
    for l in open(f'{D}/coords/{CAT}{n}.txt'):
        if l.startswith('#'): continue
        t=l.split()
        if len(t)>=4: S.append(t[1:4])
    return S
for n in sorted(tab):
    if n in done: continue
    p=f'{D}/coords/{CAT}{n}.txt'
    if not os.path.exists(p): open(OUT,'a').write(f"{n}\t{tab[n]}\t\t\t\t\t\t\tNO_COORDS\n"); continue
    S=load(n); X=np.array(S,dtype=float)
    partial=''
    if len(S)==n-1: partial='_PARTIAL(last sphere blank in file; r* of N-1 posted spheres is an upper bound on r* of the full set)'
    if len(S)!=n and not partial: open(OUT,'a').write(f"{n}\t{tab[n]}\t\t\t\t\t\t\tCOUNT_MISMATCH {len(S)}\n"); continue
    if len(S)==0: open(OUT,'a').write(f"{n}\t{tab[n]}\t\t\t\t\t\t\tUNCHECKABLE_EMPTY{partial}\n"); continue
    X=X.reshape(-1,3)
    M=lambda i:[mp.mpf(v) for v in S[i]]
    if CAT=='scu':
        wf=np.abs(X).max(1); idx=np.where(wf>wf.max()-1e-9)[0]
        wall=min(mp.mpf('0.5')-max(abs(v) for v in M(i)) for i in idx)
    else:
        wf=np.sqrt((X**2).sum(1)); idx=np.where(wf>wf.max()-1e-9)[0]
        wall=min(1-mp.sqrt(sum(v*v for v in M(i))) for i in idx)
    if len(S)>1:
        dd,_=cKDTree(X).query(X,k=2); dmin=dd[:,1].min()
        pairs=cKDTree(X).query_pairs(dmin+1e-9,output_type='ndarray')
        pr=min(mp.sqrt(sum((a-b)**2 for a,b in zip(M(i),M(j)))) for i,j in pairs)/2
    else: pr=mp.inf
    r=min(pr,wall); t=mp.mpf(tab[n]); dec=len(tab[n].split('.')[1]); gap=r-t
    half=mp.mpf(10)**(-dec)/2
    ulp=mp.mpf(10)**(-dec); cls='MATCH' if abs(gap)<=ulp+mp.mpf('1e-45') else ('ROUNDING_NOISE' if abs(gap)<=MARGIN else ('ERRATA' if gap<0 else 'COORDS_BETTER_THAN_TABLE'))
    bind='pair' if pr<wall else ('wall' if wall<pr else 'both')
    open(OUT,'a').write(f"{n}\t{tab[n]}\t{dec}\t{mp.nstr(r,35)}\t{mp.nstr(gap,12)}\t{bind}\t{mp.nstr(pr,35)}\t{mp.nstr(wall,35)}\t{cls}{partial}\n")
open(OUT+'.DONE','w').write(time.strftime('%FT%TZ',time.gmtime())+'\n')
