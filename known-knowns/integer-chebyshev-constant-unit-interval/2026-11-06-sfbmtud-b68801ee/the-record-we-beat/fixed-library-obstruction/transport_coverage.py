#!/usr/bin/env python3
"""Exact independent check that a w-library covers all symmetrized lower-library factors."""
import argparse
import hashlib
import json
import math
from pathlib import Path

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return a
def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):out[i+j]+=ai*bj
    return trim(out)
def reflect(a):
    out=[0]*len(a)
    for k,ak in enumerate(a):
        for j in range(k+1):out[j]+=ak*math.comb(k,j)*(-1)**j
    return trim(out)
def wpower(k):
    out=[0]*(2*k+1)
    for j in range(k+1):out[k+j]=math.comb(k,j)*(-1)**j
    return out
def descend(a):
    a=trim(a);out=[0]*((len(a)-1)//2+1)
    assert reflect(a)==a
    while len(a)>1:
        n=len(a)-1;assert n%2==0
        d=n//2;coefficient=a[-1]*(-1)**d;out[d]=coefficient
        p=wpower(d)
        a=trim([ai-coefficient*p[i] for i,ai in enumerate(a)])
    out[0]=a[0]
    return trim(out)
def compose_w(a):
    out=[0]*(2*len(a)-1)
    for k,ak in enumerate(a):
        for i,v in enumerate(wpower(k)):out[i]+=ak*v
    return trim(out)
def canonical(a):
    a=trim(a)
    content=math.gcd(*a)
    assert content==1, 'Unexpected nonprimitive transported polynomial'
    sign=1 if a[-1]>0 else -1
    return [sign*x for x in a],sign

def audit(lower_bytes,union_bytes,transport=None,original_bytes=None):
    lower=json.loads(lower_bytes);union=json.loads(union_bytes)
    indices={tuple(f['coeffs_desc_w']):i for i,f in enumerate(union['factors'])}
    assert len(indices)==len(union['factors'])
    rows=[];direct=0;norm=0;missing=[]
    for i,desc in enumerate(lower['library']):
        assert isinstance(desc,list) and len(desc)>1 and all(type(x) is int for x in desc) and desc[0]!=0
        a=list(reversed(desc));reflected=reflect(a)
        if reflected==a:
            invariant=a;method='direct_invariant';direct+=1
        else:
            invariant=mul(a,reflected);method='reflection_product';norm+=1
        w=descend(invariant)
        assert compose_w(w)==invariant
        w,sign=canonical(w)
        wdesc=tuple(reversed(w))
        index=indices.get(wdesc)
        if index is None:missing.append({'lower_index':i,'coeffs_desc_w':wdesc})
        rows.append({'lower_index':i,'method':method,'x_degree':len(desc)-1,'w_degree':len(w)-1,
                     'sign_of_identity':sign,'union_factor_index':index})
    provenance_checked=0
    if transport is not None:
        for row in transport['candidates']:
            origin=row['origin'];i=origin['lower_index']
            assert origin['coeffs_desc_x']==lower['library'][i]
            assert tuple(row['coeffs_desc_w']) in indices
            expected=rows[i]
            assert indices[tuple(row['coeffs_desc_w'])]==expected['union_factor_index']
            provenance_checked+=1
    missing_original=[];original_count=None
    if original_bytes is not None:
        original=json.loads(original_bytes);original_count=len(original['factors'])
        for i,row in enumerate(original['factors']):
            if tuple(row['coeffs_desc_w']) not in indices:missing_original.append(i)
    result={'status':'PASS_EXACT_TRANSPORT_COVERAGE' if not missing and not missing_original else 'MISSING_TRANSPORTS',
            'lower_source_sha256':hashlib.sha256(lower_bytes).hexdigest(),
            'union_library_sha256':hashlib.sha256(union_bytes).hexdigest(),
            'source_lower_factor_count':len(rows),'direct_invariant_count':direct,
            'reflection_product_count':norm,'covered_count':len(rows)-len(missing),
            'distinct_union_factors_used':len(set(r['union_factor_index'] for r in rows if r['union_factor_index'] is not None)),
            'transport_origin_records_checked':provenance_checked,'missing':missing,'mapping':rows}
    if original_bytes is not None:
        result.update({'original_upper_source_sha256':hashlib.sha256(original_bytes).hexdigest(),
                       'original_upper_factor_count':original_count,'original_upper_covered_count':original_count-len(missing_original),
                       'missing_original_upper_indices':missing_original})
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lower',required=True);ap.add_argument('--union',required=True)
    ap.add_argument('--original')
    ap.add_argument('--transport');ap.add_argument('--out')
    args=ap.parse_args()
    transport=json.loads(Path(args.transport).read_text()) if args.transport else None
    original=Path(args.original).read_bytes() if args.original else None
    result=audit(Path(args.lower).read_bytes(),Path(args.union).read_bytes(),transport,original)
    if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='mapping'},indent=2))
    return 0 if result['status']=='PASS_EXACT_TRANSPORT_COVERAGE' else 2

if __name__=='__main__':raise SystemExit(main())
