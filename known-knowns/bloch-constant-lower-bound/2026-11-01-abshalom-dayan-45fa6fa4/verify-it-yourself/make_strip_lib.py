# make_strip_lib.py e1 e2 baselib outdir [--verify] : Arb rebuild (128,256 bits) of affine minorants R_r >= e+p b2+q b3, Theorem 3.2 with weights r^{k+1}/(k+1), T0 at r.
# Reads ../near-lift/certs/tier_{e1}_{e2}.json rows as data; every extra json in strips/extra_{e1}_{e2}/ also. Radius and eta cross-checked against pts cert.
import sys,json,math,glob,shutil,os,hashlib
from flint import arb,ctx
e1s,e2s,base,out=sys.argv[1:5]; VERIFY="--verify" in sys.argv
NL="../near-lift/certs"
BOTTOM=float(e1s)==0.0
if BOTTOM:  # bottom piece: single integral cut from int_eta{e2}_r*.json
    fi=glob.glob("%s/int_eta%s_r*.json"%(NL,e2s)); assert len(fi)==1
    tier=json.load(open(fi[0])); r=float.fromhex(tier["r"]); e2=float.fromhex(tier["eta"]); e1=0.0; assert e2==float(e2s)
else:
    tier=json.load(open("%s/tier_%s_%s.json"%(NL,e1s,e2s)))
    r=float.fromhex(tier["r"]); e2=float.fromhex(tier["e2"]); e1=float.fromhex(tier["e1"]); assert e2==float(e2s) and e1==float(e1s)
pf=glob.glob("%s/pts_eta%s_r*.json"%(NL,e2s)); assert len(pf)==1
P=json.load(open(pf[0])); assert float.fromhex(P["r1"])==r and float.fromhex(P["eta"])==e2 and float.fromhex(P["nodes"][-1])==r and "a2box" not in P
print("radius",r,"pts file",pf[0],"nodes",len(P["nodes"]),"eta",float.fromhex(P["eta"]))
def Bk(k): return (arb(k+2)/k)**(arb(k)/2)*arb(k+2)/2
def build(rows,K,prec):
    ctx.prec=prec; R=arb(r); E=arb(1).exp()
    d=[R**(k+1)/(k+1) for k in range(K+1)]; sl=arb(0); T=arb(0)
    for ro,ps,ga,la in rows:
        ro,ps,ga,la=[float.fromhex(v) for v in (ro,ps,ga,la)]
        assert la>=0 and 0<=ro<1
        x,PS,GA,L=arb(ro),arb(ps),arb(ga),arb(la); sl+=L; c=L*(1-x*x); pw=arb(1)
        for k in range(K+1):
            d[k]=d[k]+c*pw*(k*PS-GA).cos(); pw*=x
        T+=c*pw*((K+3)/(1-x)+x/((1-x)*(1-x)))
    T=T*E/2; T0=E/2*arb(K+3)/(K+2)*R**(K+2)/(1-R)
    s=arb(0)
    for k in range(4,K+1): s+=Bk(k)*abs(d[k])
    return d[0]-sl-s-T-T0,d[2],d[3]
def dn(x):
    f=math.nextafter(float(x.lower()),-math.inf); assert arb(f)<x; return f
C=3.2888
cuts=[("center",tier["rows"],tier["K"])] if BOTTOM else [("plus",tier["plus"],tier["K"]),("minus",tier["minus"],tier["K"]),("center",tier["center"],tier["K"])]
for fn in sorted(glob.glob("strips/extra_%s_%s/*.json"%(e1s,e2s))):
    c=json.load(open(fn)); cuts.append((os.path.basename(fn),c["rows"],c["K"]))
lines=[]
for name,rows,K in cuts:
    a=build(rows,K,128); b=build(rows,K,256)
    assert all(u.overlaps(v) for u,v in zip(a,b)); ctx.prec=256
    pfl=float(b[1].mid()); qfl=float(b[2].mid())
    cor=b[0]-abs(b[1]-arb(pfl))-arb(C)*abs(b[2]-arb(qfl))
    ef=dn(cor); lines.append("%s %s %s %s"%(ef.hex(),pfl.hex(),qfl.hex(),name))
    print(name,"e",ef,"p",pfl,"q",qfl,"e-p gain",ef-pfl-math.sqrt(3)/4,"rows",len(rows),"K",K,flush=True)
if VERIFY:
    old=open(out+"/minorants.txt").read().split("\n")[:-1]
    ok=old==lines; print("VERIFY","OK" if ok else "FAIL"); sys.exit(0 if ok else 1)
os.makedirs(out,exist_ok=True)
open(out+"/minorants.txt","w").write("\n".join(lines)+"\n")
shutil.copy(base+"/excl.txt",out+"/excl.txt"); shutil.copy(base+"/trig.bin",out+"/trig.bin")
m=[]
for l in open(base+"/meta.txt"):
    if l.startswith("C_up"): m.append("C_up %s\n"%e2.hex())
    elif l.startswith("eta"): m.append("eta %s\n"%e1.hex())
    else: m.append(l)
m.append("RADIUS %s\n"%r.hex())
open(out+"/meta.txt","w").writelines(m)
