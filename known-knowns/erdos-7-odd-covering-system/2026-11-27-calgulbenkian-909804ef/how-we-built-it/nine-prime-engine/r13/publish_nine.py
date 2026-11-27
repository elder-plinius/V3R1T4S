from pathlib import Path
import sys, json
from fractions import Fraction as F
from itertools import islice, product
sys.path.insert(0,'package')
from verify_scalar import exponent_vectors, odd_primes, BOUND

src=json.loads(Path('r13/nine-compact.json').read_text())['boxes']
cases=[]
seen=set()
least=None
for cap,rows in src:
    k=[(a,b,c,-1,j,0,0,0,-1) for a,b,c,j in product((1,2),(2,4),(1,2),range(1,5))]
    if {tuple(key) for _,key,_,_ in rows}!=set(k) or len(rows)!=32: raise ValueError("keys")
    if tuple(cap) in seen: raise ValueError("duplicate cap")
    seen.add(tuple(cap))
    for phase,key,R,S in rows:
        m=F(R)-F(S)
        if phase!="basic" or m<=0: raise ValueError("invalid row")
        if least is None or m<least: least=m
    cases.append({"exps":cap,"rows":rows})
primes=tuple(islice(odd_primes(),9))
covered=0
for v in exponent_vectors(primes,BOUND):
    if not any(all(w is None or x<=w for x,w in zip(v,c)) for c in seen): raise ValueError(v)
    covered+=1
j={"bound":BOUND,"primes":primes,"C7":"3/2","taus_later":[4,4,6,8,12,16],"U":9,"V":7,"certificates":cases}
p=Path('package/nine-finite.json')
t=Path('r13/nine-ready.json')
t.write_text(json.dumps(j,separators=(',',':'))+'\n')
t.replace(p)
print("models",len(cases),"rows",32*len(cases),"vectors",covered,"least",least,float(least),"bytes",p.stat().st_size)
