"""Prototype (mpmath floats; NUMERICAL) of the profile-aware multi-scale recursion.  See REDUCTION.md section C."""
import sys, itertools
sys.path.insert(0,'.')
from mpmath import mp, mpf, sqrt, acos, pi
mp.dps=25
import aexact
th=acos(mpf(1)/3); al=th/(2*pi)
def E(e):   # GEK printed wedge-volume excess (prototype)
    e=mpf(e)
    if e>=1: return mpf(1)/2-al
    return min(sqrt(2)/4*e+sqrt(2)/18*e*e, mpf(1)/2-al)
a=aexact.a_exact
FCAP=1-al-sqrt(2)/(3*pi)       # Lemma A: total volume of >=2 caps (vs W0)
def capvol_total(c): return mpf(c)/2 if c<=1 else FCAP
def capvol(dl): dl=mpf(dl); return (1-dl)**2*(2+dl)/4
rho={}
rho[(0,1)]=1-al; rho[(1,1)]=mpf(1)/2-al
for c in range(2,12): rho[(c,1)]=sqrt(2)/(3*pi)
rho[(0,2)]=mpf(1)/2-al
def bis(f,lo,hi,it=200):  # f decreasing; returns smallest x with f(x)<=0 (approx, from hi side)
    for _ in range(it):
        m=(lo+hi)/2
        if f(m)<=0: hi=m
        else: lo=m
    return hi
def solve_t_lt1(c,w):
    rk=[rho[(c+w-1-k,1+k)] for k in range(w-1)]
    def VOL(T):
        tot=1-w*al-capvol_total(c)
        for k in range(w-1):
            u=(T/rk[k])**(mpf(1)/3)
            tot-= E(u)
        return tot
    return bis_root(VOL)
def bis_root(VOL):
    lo,hi=mpf(0),mpf(1)
    for _ in range(200):
        m=(lo+hi)/2
        if VOL(m)-m>0: lo=m
        else: hi=m
    return lo
def solve_t_gt1(c,w,verbose=False):
    m=c+w-1; best=None; bsig=None
    seqs=set(itertools.permutations(['c']*c+['w']*(w-1)))
    for sig in seqs:
        # types of first i objects
        rh=[]; cc=ww=0
        for i,x in enumerate(sig):
            rh.append(rho[(cc,1+ww)]); 
            if x=='c': cc+=1
            else: ww+=1
        def cov_ok(T):
            tot=mpf(0); caps=mpf(0); ncap=0
            for i,x in enumerate(sig):
                u=(T/rh[i])**(mpf(1)/3)
                if u>=1: continue
                if x=='c': tot+=(1-u)/2; caps+=capvol(u); ncap+=1
                else: tot+=a(u)
            ok = tot<=1-al
            if ncap>=2: ok = ok and caps<=FCAP
            return ok
        lo,hi=mpf(0),max(rh)
        if cov_ok(lo): T=lo
        else:
            for _ in range(120):
                mid=(lo+hi)/2
                if cov_ok(mid): hi=mid
                else: lo=mid
            T=hi
        # T cannot exceed rho of the state with last object absent: handled since u>=1 -> skipped; also cap by min rh? term i: u^3*rh[i]=T ok
        if best is None or T<best: best,bsig=T,sig
    return best,bsig
def mono_close():
    keys=list(rho)
    for k in keys:
        for k2 in keys:
            if k2[1]>=k[1] and k2[0]+k2[1]>=k[0]+k[1] and rho[k2]>rho[k]: rho[k]=rho[k2]
def state_val(c,w):
    t=w*al+mpf(c)/2
    if t<1: return solve_t_lt1(c,w)
    return solve_t_gt1(c,w)[0]
import os
NMAX=int(os.environ.get('NMAX','5'))
order=sorted([(c,w) for w in range(1,9) for c in range(0,8) if c+w<=NMAX and w>=2 and (c,w)!=(0,2)], key=lambda x:(x[0]+x[1],x[1]))
if __name__=="__main__":
    for (c,w) in order:
        v=state_val(c,w)
        t=w*al+mpf(c)/2
        rho[(c,w)]=v
        mono_close()
        print((c,w),"t=%.3f"%t,"rho_hat=%.4e"%v, "(after mono close %.4e)"%rho[(c,w)],flush=True)
    print("rho(0,5) =",rho[(0,5)])
