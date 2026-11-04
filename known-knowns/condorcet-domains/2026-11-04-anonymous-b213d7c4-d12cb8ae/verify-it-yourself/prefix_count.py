"""Independent derivation: when appending x, a forbidden triple rank j is
violated exactly when j-1 of its other two labels already lie in prefix S.
Thus valid prefixes are counted by a subset DP; every full order has one path.
Written before inspecting prior checker/search implementations this run.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import defaultdict
import argparse, datetime, hashlib, json, math, re, time

def parse(path):
    rows=[]; seen=set(); n=0
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith('#'): continue
        m=re.fullmatch(r'([1-9][0-9]*) ([1-9][0-9]*) ([1-9][0-9]*) ([123])N([123])',line)
        if m is None: raise ValueError('malformed row')
        a,b,c,i,j=map(int,m.groups())
        if not a<b<c or (a,b,c) in seen: raise ValueError('triple ordering or duplicate')
        seen.add((a,b,c)); n=max(n,c);rows.append(((a-1,b-1,c-1),i-1,j-1))
    if n<3 or seen!=set(combinations(range(1,n+1),3)): raise ValueError('missing triple')
    return n,rows

def count(n, rows):
    tests=[[] for _ in range(n)]
    for labels,i,j in rows:
        x=labels[i]; others=[1<<y for y in labels if y!=x]
        tests[x].append((others[0],others[1],j))
    layer={0:1}; states=1
    for k in range(n):
        nxt=defaultdict(int)
        for mask,ways in layer.items():
            remaining=((1<<n)-1)^mask
            while remaining:
                bit=remaining&-remaining; remaining-=bit; x=bit.bit_length()-1
                if all(((bool(mask&a)+bool(mask&b))!=j) for a,b,j in tests[x]):
                    nxt[mask|bit]+=ways
        layer=nxt; states+=len(layer)
    return layer.get((1<<n)-1,0),states

def brute(n,rows):
    value=0
    for order in permutations(range(n)):
        pos=[0]*n
        for k,x in enumerate(order): pos[x]=k
        if all(sum(pos[y]<pos[t[i]] for y in t)!=j for t,i,j in rows): value+=1
    return value

def selftest():
    assert count(3,[((0,1,2),1,0)])[0]==4
    assert brute(3,[((0,1,2),1,0)])==4
    # Impossible domain: prohibit every rank of the same element in one triple.
    assert count(3,[((0,1,2),0,j) for j in range(3)])[0]==0
    triples=list(combinations(range(4),3)); total=0
    for choices in product(range(9),repeat=4):
        rows=[(t,c//3,c%3) for t,c in zip(triples,choices)]
        assert count(4,rows)[0]==brute(4,rows); total+=1
    return dict(exhaustive_n4_assignments=total,positive_n3=4,impossible_domain=0)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('assignment',nargs='?');ap.add_argument('--selftest',action='store_true');a=ap.parse_args();start=time.monotonic();out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    if a.selftest:out['selftest']=selftest()
    if a.assignment:
        n,rows=parse(a.assignment);v,s=count(n,rows);out.update(n=n,count=v,prefix_states=s,sha256=hashlib.sha256(Path(a.assignment).read_bytes()).hexdigest())
    out['elapsed_seconds']=time.monotonic()-start;print(json.dumps(out,indent=2))
