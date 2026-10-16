# independent recheck (mpmath dps 50, all pairs, fresh process per N); format: idx x y z radius
import sys, itertools, mpmath as mp
mp.mp.dps=50
f,rad,N=sys.argv[1],sys.argv[2],sys.argv[3]
T=[l.split() for l in open(rad) if l.split() and not l.startswith('#')]; cell=mp.mpf(dict((a[0],a[1]) for a in T)[N])
C=[[mp.mpf(v) for v in p[1:4]] for p in (l.split() for l in open(f)) if len(p) in (4,5) and not p[0].startswith('#')]
w=min(mp.mpf(1)/2-max(abs(v) for v in c) for c in C)
d=min(mp.sqrt(mp.fsum((a-b)**2 for a,b in zip(C[i],C[j]))) for i,j in itertools.combinations(range(len(C)),2))
r=min(d/2,w)
print(f"N={N} centres={len(C)} r*={mp.nstr(r,30)} cell={mp.nstr(cell,30)} r*-cell={mp.nstr(r-cell,10)}")
