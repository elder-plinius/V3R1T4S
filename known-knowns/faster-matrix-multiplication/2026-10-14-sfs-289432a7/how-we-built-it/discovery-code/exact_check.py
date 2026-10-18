#!/usr/bin/env python3
"""Independently expand reduced FMM schedules over integer bilinear monomials."""
import json
import sys

def combine(row, values):
    result = {}
    seen = set()
    for term in row:
        index, coefficient = term['index'], term['value']
        if index in seen or type(index) is not int or not 0 <= index < len(values):
            raise ValueError('duplicate or unavailable variable')
        if coefficient not in (-1, 1):
            raise ValueError('nonternary scheduled coefficient')
        seen.add(index)
        for key, value in values[index].items():
            result[key] = result.get(key, 0) + coefficient * value
    return {key: value for key, value in result.items() if value}

def expand(fresh, rows, originals):
    values = list(originals)
    for row in fresh:
        values.append(combine(row, values))
    return [combine(row, values) for row in rows]

def addition_count(scheme):
    return sum(max(0, len(row)-1) for key in ('u_fresh','v_fresh','w_fresh','u','v','w')
               for row in scheme.get(key, []))

def factors(scheme):
    a,b,c=scheme['n']; rank=scheme['m']
    u=expand(scheme.get('u_fresh',[]), scheme['u'], [{i:1} for i in range(a*b)])
    v=expand(scheme.get('v_fresh',[]), scheme['v'], [{i:1} for i in range(b*c)])
    w=expand(scheme.get('w_fresh',[]), scheme['w'], [{i:1} for i in range(rank)])
    return u,v,w

def verify(scheme):
    a,b,c=scheme['n']; rank=scheme['m']
    u,v,w=factors(scheme)
    if len(u)!=rank or len(v)!=rank or len(w)!=a*c or scheme.get('z2',False):
        raise ValueError('wrong dimensions or binary-only scheme')
    for output, coefficients in enumerate(w):
        actual={}
        for product, weight in coefficients.items():
            for ai, av in u[product].items():
                for bi, bv in v[product].items():
                    key=(ai,bi)
                    actual[key]=actual.get(key,0)+weight*av*bv
        actual={key:value for key,value in actual.items() if value}
        i,j=output%a,output//a
        expected={(i*b+k,k*c+j):1 for k in range(b)}
        if actual != expected:
            raise ValueError('bilinear identity mismatch at output '+str(output))
    return {'valid':True,'format':scheme['n'],'rank':rank,
            'additions':addition_count(scheme),'outputs_verified':a*c,
            'brent_identities':a*b*b*c*a*c}

if __name__=='__main__':
    for path in sys.argv[1:]:
        try:
            print(json.dumps({'file':path.rsplit('/',1)[-1],**verify(json.load(open(path)))}))
        except Exception as error:
            print(json.dumps({'file':path.rsplit('/',1)[-1],'valid':False,'error':str(error)}))
            sys.exit(1)
