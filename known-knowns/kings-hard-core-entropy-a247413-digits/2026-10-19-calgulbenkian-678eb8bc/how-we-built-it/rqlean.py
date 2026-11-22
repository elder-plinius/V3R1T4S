import sys,subprocess
from mpmath import mp,mpf,sqrt
mp.dps=80
def lam_from_output(txt):
    S={}
    for l in txt.strip().split('\n'):
        p=l.split()
        if p[0] in 'WV': S[p[0]]=sum(int(c)<<(40*k) for k,c in enumerate(p[1:]))
    return sqrt(mpf(S['W'])/mpf(S['V']))
def lam(m,iters,threads=12):
    out=subprocess.run(['./tmlean',str(m),str(iters),str(threads),'x'],check=True,capture_output=True,text=True).stdout
    return lam_from_output(out)
