#!/usr/bin/env python3
"""Independent review checker; written before reading supplied implementation.

Definition quoted from GAME.md:
"Independently at each round, choose one of the three unordered pairs with
probability 1/3 and choose which member wins with probability 1/2. The loser
transfers the smaller of the two pre-round stacks to the winner. Stop at the
first zero stack. The function f(x,y,z) is the probability that player 1 is
the player eliminated at that stopping time."

All geometry is rational. All certificate nodes and leaves are mandatory.
This script writes the entire independently reconstructed bounds-check workload.
The companion independent.cpp evaluates that workload without author imports.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def hull(points):
    p=sorted(set(points))
    if len(p)<3: return tuple(p)
    low=[]; high=[]
    for q in p:
        while len(low)>1 and cross(low[-2],low[-1],q)<=0: low.pop()
        low.append(q)
    for q in reversed(p):
        while len(high)>1 and cross(high[-2],high[-1],q)<=0: high.pop()
        high.append(q)
    return tuple(low[:-1]+high[:-1])

def poly(raw):
    assert isinstance(raw,list) and raw
    for p in raw:
        assert len(p)==3 and all(type(c) is int for c in p) and p[2]>0
    points=[(Q(x,w),Q(y,w)) for x,y,w in raw]
    result=hull(points)
    assert len(result)==len(points) and set(result)==set(points), 'Non-extreme or duplicate vertex'
    return result

def value(line,p): return line[0]*p[0]+line[1]*p[1]+line[2]

def split_polygon(p,line):
    values=[value(line,v) for v in p]
    assert min(values)<0<max(values), 'Split does not cross relative interior'
    neg=[]; pos=[]; zero=[]
    for a,b in zip(p,p[1:]+p[:1]):
        va,vb=value(line,a),value(line,b)
        if va<=0: neg.append(a)
        if va>=0: pos.append(a)
        if va==0: zero.append(a)
        if va*vb<0:
            t=va/(va-vb)
            q=tuple(a[j]+t*(b[j]-a[j]) for j in range(2))
            neg.append(q); pos.append(q); zero.append(q)
    return hull(neg),hull(zero),hull(pos)

DOMAINS={
    'leader': [[(0,0),(0,Q(1,2)),(Q(1,2),Q(1,2))],[(0,Q(1,2)),(Q(1,2),Q(1,2))]],
    'middle': [[(0,0),(0,1),(1,1)]],
    'shortest': [[(0,0),(1,0),(1,1)],[(0,0),(1,1)]]}
EXPECTED={
    'leader':(128,86,{7:86},Q(181,1399680)),
    'middle':(7,5,{3:5},Q(1,135)),
    'shortest':(9704,6470,{12:2260,13:4210},Q(379,1813985280))}

def initial(order,raw):
    # Stack values at each vertex, multiplied by that vertex's positive denominator.
    # Every game update is homogeneous, so these values suffice for exact signs.
    if order=='leader':
        return [[x for x,y,w in raw],[y for x,y,w in raw],[w-y for x,y,w in raw]], [[y for x,y,w in raw],[y for x,y,w in raw],[w-y for x,y,w in raw]]
    return [[x for x,y,w in raw],[w for x,y,w in raw],[y for x,y,w in raw]], [[w for x,y,w in raw],[w for x,y,w in raw],[y for x,y,w in raw]]

@lru_cache(None)
def exact_h(state,n):
    """Exact finite-horizon scalar checker, explicitly enumerating all six outcomes."""
    if 0 in state: return Q(state[0]==0)
    if n==0: return Q(0)
    ans=Q(0)
    for winner in range(3):
        for loser in range(3):
            if winner==loser: continue
            t=list(state); bet=min(t[winner],t[loser])
            t[winner]+=bet; t[loser]-=bet
            ans+=exact_h(tuple(t),n-1)/6
    return ans

def prepare(cert_path,out_path):
    data=Path(cert_path).read_bytes(); c=json.loads(data)
    assert set(c)=={'schema','order','depth','roots','nodes','pending'}
    assert c['schema']=='adaptive-homogeneous-v1' and c['pending']==[]
    order=c['order']; assert order in DOMAINS
    nodes=c['nodes']; roots=c['roots']
    assert len(roots)==len(DOMAINS[order])
    expected_roots=[hull(p) for p in DOMAINS[order]]
    work=list(zip(roots,expected_roots)); seen=set(); leaves=[]; depths=Counter(); gaps=[]; dimensions=Counter()
    while work:
        index,expected=work.pop()
        assert type(index) is int and 0<=index<len(nodes) and index not in seen, 'Invalid/duplicate reference'
        seen.add(index); node=nodes[index]; actual=poly(node['poly'])
        assert actual==expected, ('Region mismatch',index,actual,expected)
        if 'children' in node:
            assert set(node) in ({'poly','line','children'},{'poly','line','children','depth'})
            if 'depth' in node:
                assert type(node['depth']) is int and 0<=node['depth']<=18
            assert len(node['line'])==3 and all(type(k) is int for k in node['line'])
            assert len(node['children'])==3
            children=split_polygon(actual,node['line'])
            work.extend(zip(node['children'],children))
        else:
            assert set(node) in ({'poly','bounds'},{'poly','bounds','depth'})
            d=node.get('depth',c['depth'])
            assert type(d) is int and 0<=d<=18
            b=node['bounds']; assert len(b)==4 and all(type(k) is int for k in b)
            den=5*6**d
            assert 0<=b[0]<=b[1]<=den and 0<=b[2]<=b[3]<=den
            assert b[0]>b[3], ('Nonpositive separation',index)
            depths[d]+=1; dimensions[min(2,len(actual)-1)]+=1
            gaps.append(Q(b[0]-b[3],den)); leaves.append((index,d,node))
    assert seen==set(range(len(nodes))), 'Unreachable node'
    observed=(len(nodes),len(leaves),dict(depths),min(gaps))
    assert observed==EXPECTED[order], ('Claimed statistics mismatch',observed)
    with open(out_path,'w') as f:
        f.write(str(len(leaves))+'\n')
        for index,d,node in sorted(leaves):
            aa,bb=initial(order,node['poly'])
            for s in aa+bb:
                assert min(s)>=0 and max(s)>0, 'Initial state not live on relative interior'
            row=[index,d,len(node['poly'])]+[v for state in (aa,bb) for s in state for v in s]+node['bounds']
            f.write(' '.join(map(str,row))+'\n')
    print(json.dumps({'certificate':str(cert_path),'sha256':hashlib.sha256(data).hexdigest(),'all_geometry_verified':True,'nodes':len(nodes),'leaves':len(leaves),'dimensions':dict(dimensions),'depths':dict(depths),'stored_minimum':str(min(gaps)),'bounds_recomputation_required':True},sort_keys=True),flush=True)

if __name__=='__main__':
    prepare(sys.argv[1],sys.argv[2])
