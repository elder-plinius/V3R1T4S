#!/usr/bin/env python3
"""Independent integer SLP checker, written before opening claim/verify.py.
A[i,h] has offset i*m+h, B[h,j] has offset h*p+j,
and output C[i,j] has offset j*n+i. C[i,j]=sum_h A[i,h]*B[h,j].
Only binary signed additions, aliases, free signs and the m explicit U*V
products occur in the interpreted language. Intermediate integer forms are
unrestricted; expanded U,V,W factors must be ternary.
"""
import argparse
import hashlib
import json
from pathlib import Path

class Invalid(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise Invalid(message)

def unique_pairs(pairs):
    d = {}
    for key, val in pairs:
        require(key not in d, 'duplicate JSON key '+key)
        d[key] = val
    return d

def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_pairs)

def form(row, bound, label):
    require(isinstance(row, list), label+' must be a list')
    for t in row:
        require(isinstance(t, dict) and set(t)=={'index','value'}, label+' invalid term schema')
        require(type(t['index']) is int and 0 <= t['index'] < bound, label+' forward/out-of-range reference')
        require(type(t['value']) is int and t['value'] in (-1,1), label+' nonunit literal coefficient')
    return row

def expand_stage(s, side, size, rows):
    env = [tuple(int(i==j) for j in range(size)) for i in range(size)]
    dependencies = [set() for _ in range(size)]
    trace, counts = [], {'fresh':0, 'terminal':0, 'aliases':0, 'free_negative_aliases':0}
    expanded = []
    for category, programs in [('fresh',s.get(side+'_fresh',[])), ('terminal',s[side])]:
        require(isinstance(programs,list), side+' invalid program array')
        if category == 'terminal':
            require(len(programs)==rows, side+' wrong terminal count')
        for ix,row in enumerate(programs):
            label = side+'_'+category+'['+str(ix)+']'
            form(row,len(env),label)
            vector = tuple(sum(t['value']*env[t['index']][j] for t in row) for j in range(size))
            if len(row)==1:
                counts['aliases'] += 1
                counts['free_negative_aliases'] += int(row[0]['value']==-1)
            # Lower the literal k-term expression to k-1 signed binary sums.
            for term_index in range(1,len(row)):
                trace.append({'stage':side,'kind':category,'row':ix,'step':term_index,
                              'left':row[:term_index], 'right':row[term_index]})
                counts[category] += 1
            if category=='fresh':
                dependencies.append(set(t['index'] for t in row))
                env.append(vector)
            else:
                expanded.append(vector)
    needed = set(t['index'] for row in s[side] for t in row)
    stack = list(needed)
    while stack:
        x = stack.pop()
        for y in dependencies[x]:
            if y not in needed:
                needed.add(y)
                stack.append(y)
    dead = [i for i in range(size,len(env)) if i not in needed]
    expanded_values = sorted({v for vec in expanded for v in vec})
    require(set(expanded_values) <= {-1,0,1},side+' nonternary expanded factor')
    return expanded, {'counts':counts,'fresh_gates':len(s.get(side+'_fresh',[])),
                      'dead_fresh_indices':dead,'expanded_coefficient_domain':expanded_values,
                      'intermediate_coefficient_domain':sorted({v for vec in env[size:] for v in vec}),
                      'max_intermediate_absolute_coefficient':max([abs(v) for vec in env[size:] for v in vec]+[0])}, trace

def canonical(v):
    first=next((x for x in v if x),None)
    require(first is not None,'zero product factor')
    return tuple(x if first>0 else -x for x in v)

def literal_eval(s,side,base):
    # Evaluates instructions directly, without calling or using the expander.
    env=list(base)
    for row in s.get(side+'_fresh',[]):
        acc=0
        for t in row:
            x=env[t['index']]
            acc = acc+x if t['value']==1 else acc-x
        env.append(acc)
    outputs=[]
    for row in s[side]:
        acc=0
        for t in row:
            x=env[t['index']]
            acc=acc+x if t['value']==1 else acc-x
        outputs.append(acc)
    return outputs

def inspect(s, metadata=True):
    require(isinstance(s,dict),'top-level must be object')
    dims=s.get('n')
    require(isinstance(dims,list) and len(dims)==3 and all(type(x) is int and x>0 for x in dims),'invalid dimensions')
    n,m,p=dims
    rank=s.get('m')
    require(type(rank) is int and rank>0,'invalid product count')
    require(s.get('z2') is False,'integer flag must be false')
    U,ua,ut=expand_stage(s,'u',n*m,rank)
    V,va,vt=expand_stage(s,'v',m*p,rank)
    W,wa,wt=expand_stage(s,'w',rank,n*p)
    unused=[r for r in range(rank) if not any(row[r] for row in W)]
    require(not unused,'inactive products '+str(unused))
    signatures=[(canonical(U[r]),canonical(V[r])) for r in range(rank)]
    require(len(set(signatures))==rank,'duplicate products up to free signs')
    tensor_errors=[]
    tensor_delta=[]
    for c in range(n*p):
        i,j=c%n,c//n
        for a in range(n*m):
            ai,ah=divmod(a,m)
            for b in range(m*p):
                bh,bj=divmod(b,p)
                want=int(ai==i and bj==j and ah==bh)
                got=sum(U[r][a]*V[r][b]*W[c][r] for r in range(rank))
                delta=got-want
                tensor_delta.append(delta)
                if delta:
                    tensor_errors.append({'output':c,'A':a,'B':b,'expected':want,'actual':got})
    direct_errors=[]
    for a in range(n*m):
        A=[int(x==a) for x in range(n*m)]
        u=literal_eval(s,'u',A)
        for b in range(m*p):
            B=[int(x==b) for x in range(m*p)]
            v=literal_eval(s,'v',B)
            result=literal_eval(s,'w',[x*y for x,y in zip(u,v)])
            for c,value in enumerate(result):
                i,j=c%n,c//n
                want=int(a//m==i and a%m==b//p and b%p==j)
                if value != want:
                    direct_errors.append({'output':c,'A':a,'B':b,'expected':want,'actual':value})
    costs={side:audit['counts']['fresh']+audit['counts']['terminal'] for side,audit in [('u',ua),('v',va),('w',wa)]}
    naive=sum(max(0,sum(x!=0 for x in row)-1) for row in U+V+W)
    total=sum(costs.values())
    if metadata:
        require(s.get('complexity')=={'naive':naive,'reduced':total},'complexity metadata mismatch')
    result={'format':dims,'products':rank,'active_distinct_products':len(set(signatures)),
            'output_order':'j*n+i','input_order':'A i*m+h; B h*p+j','binary_additions':costs,'total_additions':total,
            'naive_additions':naive,'tensor_coefficients_checked':len(tensor_delta),
            'tensor_mismatches':len(tensor_errors),'first_tensor_mismatches':tensor_errors[:5],
            'basis_pairs_checked':n*m*m*p,'direct_output_values_checked':n*m*m*p*n*p,
            'direct_mismatches':len(direct_errors),'first_direct_mismatches':direct_errors[:5],
            'mod2_tensor_mismatches':sum(x%2 != 0 for x in tensor_delta),
            'audit':{'u':ua,'v':va,'w':wa},'zero_hidden_scalar_operations':True,
            'extra_metadata_keys':sorted(set(s)-{'n','m','z2','complexity','u_fresh','u','v_fresh','v','w_fresh','w'}),
            'exact_Z_product':not tensor_errors and not direct_errors}
    return result,ut+vt+wt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('scheme')
    ap.add_argument('--trace')
    args=ap.parse_args()
    path=Path(args.scheme)
    result,trace=inspect(load(path))
    result['scheme_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    if args.trace:
        Path(args.trace).write_text(json.dumps(trace,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['exact_Z_product'] else 1)
if __name__=='__main__':
    main()
