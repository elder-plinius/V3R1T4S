# Executes PREREG_B.md exactly.
import sys; sys.path.insert(0,"{WORKDIR}")
from extrap import wynn
from mpmath import mp,mpf,nstr
mp.dps=70
d={}
for l in open('{WORKDIR}/lam_open.txt'):
    m,_,x=l.split(); d[int(m)]=mpf(x)
for l in open('{WORKDIR}/lam_open_lean.txt'):
    m,_,x=l.split(); m=int(m)
    if m>28: d[m]=mpf(x)
M=max(d)
def prefix(vs):
    n=0
    for ch in zip(*vs):
        if len(set(ch))>1: break
        n+=1
    return n
E={}
for mmax in range(22,M+1):
    r=[d[m]/d[m-1] for m in range(3,mmax+1)]
    cols=wynn(r); ev=[c for k,c in enumerate(cols) if k%2==0 and c]
    E[mmax]=(len(ev)-1,nstr(ev[-1][-1],50).split('.')[1])
A='3426439511246012978517301618757403957194377338502545'
print('PREREG_B execution. widths 2..%d'%M)
for mmax in range(22,M+1):
    print('mmax=%d order=%d E=1.%s  common_with_siteCTM=%d'%(mmax,E[mmax][0],E[mmax][1][:44],prefix([E[mmax][1],A])))
for end in range(25,M+1):
    w=[E[k][1] for k in range(end-3,end+1)]
    print('window mmax=%d..%d : common decimals = %d'%(end-3,end,prefix(w)))
