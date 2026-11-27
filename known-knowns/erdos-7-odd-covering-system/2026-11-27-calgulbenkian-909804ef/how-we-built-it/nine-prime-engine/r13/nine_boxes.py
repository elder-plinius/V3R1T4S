"""Group finite nine-prime exponent vectors and regenerate basic and mixed inequalities."""
from fractions import Fraction as F
from itertools import islice, product
from math import log
from pathlib import Path
from time import monotonic
import json
import sys

from eight import Eight, SPECS
from harvest import mixed
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "package"))
from verify_scalar import BOUND, exponent_vectors, odd_primes

P=tuple(islice(odd_primes(),9))
qs=P[2:]
weights=tuple(map(log,P))
start=monotonic()

def certificate(cap, allow_mixed):
    name="finite-nine"
    SPECS[name]=(qs,cap,(4,4,6,8,12,16),(9,7),(),F(1,1000000))
    eng=Eight(name)
    out=[]
    for a,b,c in product((1,2),(2,4),(1,2)):
        roots=[(a,b,c,-1,j,0,0,0,-1) for j in range(1,5)]
        def rows(phase,keys):
            selected=[]
            for k in keys:
                R,losses=eng.eval(phase,k)
                S=sum(losses)
                if R<=S:
                    return None
                selected.append([phase,k,str(R),str(S)])
            return selected
        group=rows("basic",roots)
        if group is None and b==2:
            group=rows("basic75",roots)
        if group is None and allow_mixed:
            group=rows("mixed",mixed(a,b,c))
        if group is None:
            return None
        out.extend(group)
    return out

def hull(vs):
    return tuple(map(max,zip(*vs)))

def split(vs):
    best=None
    for i in range(9):
        for pivot in sorted({v[i] for v in vs})[:-1]:
            left=[v for v in vs if v[i]<=pivot]
            right=[v for v in vs if v[i]>pivot]
            score=sum(len(s)*sum(e*w for e,w in zip(hull(s),weights)) for s in (left,right))
            if best is None or score<best[0]:
                best=score,left,right
    return best[1:]

if __name__=="__main__":
    original=list(exponent_vectors(P,BOUND))
    reduced=[tuple([v[0],max(v[1],2),*v[2:]]) for v in original if v[0]>3 and v[2]>1]
    certs=[]; misses=[]; count=0
    for i,cap in ((0,3),(2,1)):
        top=[None]*9; top[i]=cap
        rows=certificate(tuple(top),False)
        if rows is None: raise ValueError("initial cap")
        certs.append([top,rows])
    def walk(vs):
        global count
        count+=1
        cap=tuple(None if (i==1 and e>4) or (i==2 and e>3) else e for i,e in enumerate(hull(vs)))
        rows=certificate(cap, False)
        if rows is None and len(vs)==1:
            rows=certificate(cap,True)
        if rows is not None:
            certs.append([cap,rows])
        elif len(vs)>1:
            for s in split(vs): walk(s)
        else:
            misses.append(cap)
    walk(list(set(reduced)))
    print("vectors",len(original),"remaining",len(reduced),"distinct lifted",len(set(reduced)),"boxes tried",count)
    print("certificates",len(certs),"rows",sum(len(x[1]) for x in certs),"mixed",sum(phase=="mixed" for _,rs in certs for phase,*_ in rs))
    print("open",len(misses),misses)
    print("seconds",round(monotonic()-start,2))
    Path("r13/nine-boxes.json").write_text(json.dumps({"boxes":certs,"open":misses},separators=(",",":"))+"\n")
