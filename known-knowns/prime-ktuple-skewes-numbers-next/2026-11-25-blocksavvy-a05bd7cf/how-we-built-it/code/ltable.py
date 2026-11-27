# Lower bounds of C*Li2(j*B) for j=0..nblocks, Arb (python-flint, 200 bits), written as float64 rounded DOWN.
# Li2(x)=int_2^x dt/log^2 t = [li(t)-t/log t]_2^x.  C=4*C2 (C2 from OEIS A005597, 64 digits; our prime-zeta value agrees to 1e-33).
import sys, struct, math, numpy as np
from multiprocessing import Pool
B=6*(1<<21)
def work(rng):
    from flint import arb, ctx
    ctx.prec=200
    C=4*arb('0.6601618158468695739278121100145557784326233602847334133194484233')-arb('1e-60')
    two=arb(2); c2=two.li()-two/two.log()
    res=[]
    for j in range(*rng):
        if j*B<2: res.append(0.0); continue
        x=arb(j*B); v=C*((x.li()-x/x.log())-c2)
        lo=float(v.lower()) if hasattr(v,'lower') else float(v.mid()-v.rad())
        lo=math.nextafter(math.nextafter(lo,-math.inf),-math.inf)
        res.append(lo)
    return res
if __name__=='__main__':
    n=int(sys.argv[1]); out=sys.argv[2]; nproc=int(sys.argv[3]) if len(sys.argv)>3 else 4
    step=max(1,(n+1)//(nproc*16)+1); rngs=[(i,min(i+step,n+1)) for i in range(0,n+1,step)]
    with Pool(nproc) as p: parts=p.map(work,rngs)
    a=np.array([v for part in parts for v in part],dtype='<f8'); assert len(a)==n+1
    a.tofile(out); print('wrote',out,len(a),a[-1])
