# Arb rebuild of minorants, |a3| bound, trig table, exclusion RHS. Run with venv python.
# usage: make_library.py arrays.json outdir [--verify]
#  --verify: rebuild from arrays and compare against outdir/minorants.txt etc, exit 1 on any mismatch (tamper test)
import sys, json, struct, math, hashlib
import flint
from flint import arb, ctx
arrays, outdir = sys.argv[1], sys.argv[2]
VERIFY = "--verify" in sys.argv
EXTRA = "--extra" in sys.argv
D = json.load(open(arrays))
def fx(h):  # exact double -> arb
    return arb(float.fromhex(h))
def Bk(k):
    return (arb(k+2)/k)**(arb(k)/2) * arb(k+2)/2
def rebuild(cut, prec, r=None):
    """Theorem 3.2 from the paper at r0=1/sqrt3: returns (e0,d2,d3) arbs."""
    ctx.prec = prec
    K = cut["K"]; assert K >= 4
    r0 = 1/arb(3).sqrt()
    E = arb(1).exp()
    lam = [fx(h) for h in cut["lam"]]; rho=[fx(h) for h in cut["rho"]]; psi=[fx(h) for h in cut["psi"]]; gam=[fx(h) for h in cut["gam"]]
    for h,hr in zip(cut["lam"],cut["rho"]):
        assert float.fromhex(h) >= 0.0, "negative multiplier"
        assert 0 <= float.fromhex(hr) < 1
    sumlam = sum(lam, arb(0))
    d = [r0**(k+1)/(k+1) for k in range(K+1)]
    # rows
    for l,rh,ps,ga in zip(lam,rho,psi,gam):
        pref = l*(1-rh*rh)
        pw = arb(1)
        # cos(k psi - gamma) by recurrence-free direct evaluation
        for k in range(K+1):
            d[k] = d[k] + pref*pw*(k*ps-ga).cos()
            pw = pw*rh
    # tails: T = e/2 sum lam (1-rho^2) sum_{k>K} (k+2) rho^k
    T = arb(0)
    for l,rh in zip(lam,rho):
        # sum_{k>K}(k+2) x^k = x^{K+1} ( (K+3)/(1-x) + x/(1-x)^2 )
        x=rh
        T += l*(1-x*x)*x**(K+1)*((K+3)/(1-x) + x/((1-x)*(1-x)))
    T = T*E/2
    T0 = E/2*arb(K+3)/(K+2)*r0**(K+2)/(1-r0)
    s = arb(0)
    for k in range(4,K+1):
        s += Bk(k)*abs(d[k])
    e0 = d[0]-sumlam-s-T-T0
    return e0,d[2],d[3]
def rebuild_a3(cut, prec):
    ctx.prec = prec
    K=cut["K"]; E=arb(1).exp()
    lam = [fx(h) for h in cut["lam"]]; rho=[fx(h) for h in cut["rho"]]; psi=[fx(h) for h in cut["psi"]]; gam=[fx(h) for h in cut["gam"]]
    for h in cut["lam"]: assert float.fromhex(h)>=0.0
    q=[arb(0) for k in range(K+1)]
    for l,rh,ps,ga in zip(lam,rho,psi,gam):
        pref=l*(1-rh*rh); pw=arb(1)
        for k in range(K+1):
            q[k]=q[k]+pref*pw*(k*ps-ga).cos(); pw=pw*rh
    T=arb(0)
    for l,x in zip(lam,rho):
        T+=l*(1-x*x)*x**(K+1)*((K+3)/(1-x)+x/((1-x)*(1-x)))
    T=T*E/2
    s=arb(0)
    for k in range(4,K+1): s+=Bk(k)*abs(q[k])
    assert q[3]>0
    return (sum(lam,arb(0))-q[0]+abs(q[2])+s+T)/q[3]
def up(x):  # upper double of arb real x, verified
    f=float(x.upper()); f2=math.nextafter(f,math.inf)
    assert arb(f2)>x
    return f2
def dn(x):
    f=float(x.lower()); f2=math.nextafter(f,-math.inf)
    assert arb(f2)<x
    return f2
Cdbl=float.fromhex(D["C"])
# |a3|
a=rebuild_a3(D["a3"],128); a2=rebuild_a3(D["a3"],256)
print("a3 bound 128:",a.str(20)," 256:",a2.str(20))
ctx.prec=256
assert a2<arb(Cdbl), "C fails"
assert a.overlaps(a2)
cuts=D["cuts"]+(D["extra"] if EXTRA else [])
lines=[]
for i,c in enumerate(cuts):
    e1,p1,q1=rebuild(c,128)
    e2,p2,q2=rebuild(c,256)
    assert e1.overlaps(e2) and p1.overlaps(p2) and q1.overlaps(q2), c["name"]
    assert max(float(e2.rad()),float(p2.rad()),float(q2.rad()))<1e-30, c["name"]
    pf=float(p2.mid()); qf=float(q2.mid())
    corrected=e2-abs(p2-arb(pf))-arb(Cdbl)*abs(q2-arb(qf))
    ef=dn(corrected)
    lines.append("%s %s %s %s"%(ef.hex(),pf.hex(),qf.hex(),c["name"]))
    if i<3 or i==len(cuts)-1: print(c["name"],"e",ef,"p",pf,"q",qf,"nnz",len(c["lam"]),"K",c["K"])
# improved coefficient bounds chain (Theorem 3.5 analogue at k), each step uses earlier certified bounds only
ctx.prec=256
Bp={}
def getB(k):
    return Bp[k] if k in Bp else Bk(k)
chain=[a[len("--chain="):].split(",") for a in sys.argv if a.startswith("--chain=")]
chain=chain[0] if chain else []
for fn in chain:
    c=json.load(open(fn)); kt=c["k"]; K=c["K"]
    lam=[fx(h) for h in c["lam"]]; rho=[fx(h) for h in c["rho"]]; psi=[fx(h) for h in c["psi"]]; gam=[fx(h) for h in c["gam"]]
    for h,hr in zip(c["lam"],c["rho"]):
        assert float.fromhex(h)>=0.0 and 0<=float.fromhex(hr)<1
    q=[arb(0) for k in range(K+1)]
    for l,rh,ps,ga in zip(lam,rho,psi,gam):
        pref=l*(1-rh*rh); pw=arb(1)
        for k in range(K+1):
            q[k]=q[k]+pref*pw*(k*ps-ga).cos(); pw=pw*rh
    T=arb(0)
    for l,x in zip(lam,rho):
        T+=l*(1-x*x)*x**(K+1)*((K+3)/(1-x)+x/((1-x)*(1-x)))
    T=T*arb(1).exp()/2
    su=sum(lam,arb(0))-q[0]+abs(q[2])+arb(Cdbl)*abs(q[3])+T
    for k in range(4,K+1):
        if k!=kt: su+=getB(k)*abs(q[k])
    assert q[kt]>0
    val=su/q[kt]
    u=up(val)
    print("chain step k=%d bound %s -> up %.6f (crude B_k %.6f) nnz %d"%(kt,val.str(12),u,float(Bk(kt).mid()),len(lam)))
    if arb(u)<getB(kt): Bp[kt]=arb(u)
# exclusion radii
ctx.prec=256
S=[2**-11*x for x in (4,6,8,10,12,14,16,18,20,22,24,27,30,33,36,40,44,48,52,56,60,64,70,76,82,88,96,104,112,120,128,140,150,160,176,192,208,224,240,256,288,320,352,384,448,512,600,700,800,900,1000)]
E=arb(1).exp()
excl=[]
for s in S:
    x=arb(s); K=400
    tot=1/(1-x*x); pw=x*x
    for k in range(4,K+1):
        tot+=getB(k)*pw; pw*=x      # pw=x^{k-2}
    # tail k>K: B_k<=e/2 (k+2): sum_{k>K}(k+2) x^{k-2} = x^{-2} x^{K+1}((K+3)/(1-x)+x/(1-x)^2)
    tot+=E/2*x**(K-1)*((K+3)/(1-x)+x/((1-x)*(1-x)))
    excl.append("%s %s"%(s.hex(),up(tot).hex()))
meta=["C_up %s"%Cdbl.hex(),
      "eta %s"%D["eta"],
      "SQRT3_4_UP %s"%up(arb(3).sqrt()/4).hex(),
      "PI2_UP %s"%up(arb.pi()/2).hex(),
      "PI2_DN %s"%dn(arb.pi()/2).hex(),
      "TWOPI_UP %s"%up(arb.pi()*2).hex()]
# trig table
L=18
if not VERIFY or "--trig" in sys.argv:
    ctx.prec=128
    N=1<<L
    tab=[0.0]*N
    maxerr=arb(0)
    th=arb.pi()*2/N
    # first octant direct, rest by exact symmetry
    Q=N//4
    for k in range(Q+1):
        v=(th*k).cos()
        f=float(v.mid())
        err=abs(v-arb(f))
        if err.upper()>maxerr.upper(): maxerr=err.upper()
        tab[k]=f
    tab[Q]=0.0
    for k in range(Q+1,2*Q+1): tab[k]=-tab[2*Q-k]
    for k in range(2*Q+1,N): tab[k]=tab[N-k]
    assert float(maxerr)<1.2e-16, float(maxerr)
    print("trig max err",float(maxerr))
    blob=struct.pack("<%dd"%N,*tab)
    meta.append("TRIG_L %d"%L)
    meta.append("TRIG_EPS %s"%(2.0**-52).hex())
    meta.append("TRIG_SHA %s"%hashlib.sha256(blob).hexdigest())
if VERIFY:
    old=open(outdir+"/minorants.txt").read().split("\n")
    bad=0
    for a_,b_ in zip(lines,old):
        if a_!=b_: bad+=1; print("MISMATCH",a_,"|",b_)
    if len(old)-1!=len(lines): bad+=1; print("count mismatch")
    oldex=open(outdir+"/excl.txt").read().split("\n")
    for a_,b_ in zip(excl,oldex):
        if a_!=b_: bad+=1; print("MISMATCH excl",a_,b_)
    if "--trig" in sys.argv:
        if hashlib.sha256(open(outdir+"/trig.bin","rb").read()).hexdigest()!=hashlib.sha256(blob).hexdigest(): bad+=1; print("MISMATCH trig")
    print("VERIFY", "FAIL" if bad else "OK", "mismatches",bad)
    sys.exit(1 if bad else 0)
open(outdir+"/minorants.txt","w").write("\n".join(lines)+"\n")
open(outdir+"/excl.txt","w").write("\n".join(excl)+"\n")
open(outdir+"/meta.txt","w").write("\n".join(meta)+"\n")
open(outdir+"/trig.bin","wb").write(blob)
print("wrote",len(lines),"minorants")
