#!/usr/bin/env python3
"""Verify a reduced bilinear schedule on every input basis pair over Z."""
import json
import sys

def stage(inputs, fresh, outputs):
    values=list(inputs)
    def evaluate(row):
        ids=[term['index'] for term in row]
        if len(ids)!=len(set(ids)):raise ValueError('repeated variable')
        total=0
        for term in row:
            i,s=term['index'],term['value']
            if type(i) is not int or not 0<=i<len(values) or type(s) is not int or abs(s)!=1:
                raise ValueError('invalid variable or scalar')
            total+=s*values[i]
        return total
    for row in fresh:values.append(evaluate(row))
    return [evaluate(row) for row in outputs]

def check(s):
    a,b,c=s['n'];rank=s['m']
    assert len(s['u'])==len(s['v'])==rank and len(s['w'])==a*c
    assert not s.get('z2',False)
    counts={side:sum(max(0,len(row)-1) for row in s.get(side+'_fresh',[])+s[side]) for side in 'uvw'}
    tested=0
    for ai in range(a*b):
        A=[0]*(a*b);A[ai]=1
        left=stage(A,s.get('u_fresh',[]),s['u'])
        for bi in range(b*c):
            B=[0]*(b*c);B[bi]=1
            right=stage(B,s.get('v_fresh',[]),s['v'])
            products=[x*y for x,y in zip(left,right)]
            actual=stage(products,s.get('w_fresh',[]),s['w'])
            expected=[int(ai//b==i and bi%c==j and ai%b==bi//c) for j in range(c) for i in range(a)]
            if actual!=expected:raise ValueError('basis pair mismatch '+str((ai,bi)))
            tested+=len(expected)
    return {'valid':True,'format':[a,b,c],'rank':rank,'addition_counts':counts,
            'additions':sum(counts.values()),'identities_verified':tested}

if __name__=='__main__':
    try:print(json.dumps(check(json.load(open(sys.argv[1])))))
    except Exception as e:print(json.dumps({'valid':False,'error':str(e)}));sys.exit(1)
