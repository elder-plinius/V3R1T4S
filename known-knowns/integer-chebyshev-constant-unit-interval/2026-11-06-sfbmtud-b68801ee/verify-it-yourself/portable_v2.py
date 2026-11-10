#!/usr/bin/env python3
"""Portable v2: exact Bernstein verifier with mandatory validation guard.

No binary floating arithmetic participates in acceptance. Standard library only.
Real-rootedness is not tested or assumed. Every root-free cell uses the
general second-order bound; other cells use the exact Bernstein hull.
See METHOD_ADDENDUM.md and the original METHOD.md for the proof.
"""
if not __debug__:
    raise SystemExit("Refusing optimized Python: exact input validation and controls require assertions.")

import argparse, collections, hashlib, json, math, os, resource, sys, time
from fractions import Fraction
from pathlib import Path

P = 128
Q = 1 << P
TERMS = 48

def ceildiv(a,b):
    assert b > 0
    return -((-a)//b)

def log_unit_bounds(a,b):
    """Enclose log(a/b) when 1 <= a/b <= 2, in units 2^-P."""
    assert 0 < b <= a <= 2*b
    if a == b: return 0,0
    zl=(Q*(a-b))//(a+b); zu=ceildiv(Q*(a-b),a+b)
    z2l=(zl*zl)//Q; z2u=ceildiv(zu*zu,Q)
    tl,tu=zl,zu
    lo=hi=0
    for n in range(TERMS):
        den=2*n+1
        lo += tl//den
        hi += ceildiv(tu,den)
        tl=(tl*z2l)//Q
        tu=ceildiv(tu*z2u,Q)
    # tl,tu now bound z^(2 TERMS+1). Actual z<=1/3 gives
    # 2*sum_{n>=TERMS} z^(2n+1)/(2n+1)
    # <= (9/4)*z^(2 TERMS+1)/(2 TERMS+1).
    return 2*lo, 2*hi+ceildiv(9*tu,4*(2*TERMS+1))

LOG2=log_unit_bounds(2,1)

def log_bounds(a,b=1):
    assert a > 0 and b > 0
    k=a.bit_length()-b.bit_length()
    if k>=0:
        an,bn=a,b<<k
    else:
        an,bn=a<<(-k),b
    if an<bn:
        k-=1
        an*=2
    assert bn<=an<2*bn
    lo,hi=log_unit_bounds(an,bn)
    if k>=0: return lo+k*LOG2[0],hi+k*LOG2[1]
    return lo+k*LOG2[1],hi+k*LOG2[0]

def strict_int(x):
    return type(x) is int

def parse_certificate(path):
    raw=Path(path).read_bytes(); obj=json.loads(raw)
    factors=obj['factors']
    assert isinstance(factors,list) and factors, 'empty/non-list factors'
    assert strict_int(obj['n_factors']) and obj['n_factors']==len(factors), 'factor count mismatch'
    N=0
    for f in factors:
        assert strict_int(f['e']) and f['e']>0, 'exponent must be positive integer'
        assert strict_int(f['degw']) and f['degw']>=0, 'degree must be nonnegative integer'
        c=f['coeffs_desc_w']
        assert isinstance(c,list) and c and all(map(strict_int,c)), 'coefficients must be integer list (not bool)'
        assert c[0]!=0, 'zero polynomial or leading zero'
        assert f['degw']==len(c)-1, 'factor degree mismatch'
        N += f['e']*f['degw']
    assert N>0, 'total degree must be positive'
    assert strict_int(obj['N_w_degree']) and obj['N_w_degree']==N, 'w degree mismatch'
    assert strict_int(obj['x_degree']) and obj['x_degree']==2*N, 'x degree mismatch'
    return obj,hashlib.sha256(raw).hexdigest(),N

def initial_bernstein(desc):
    """Integer numerator array, common denominator on w=t/4."""
    d=len(desc)-1
    c=list(reversed(desc))
    lcm=math.lcm(*(math.comb(d,k) for k in range(d+1)))
    D=lcm*(4**d)
    b=[sum(c[k]*math.comb(i,k)*(D//((4**k)*math.comb(d,k))) for k in range(i+1)) for i in range(d+1)]
    assert b[0]*1==c[0]*D
    return b,D

def split_bernstein(b,D):
    """Exact half split, plus midpoint numerator and scaled derivative ratio.
    Return L,R,newD,mnum,diff; mid=mnum/newD and
    (cell halfwidth)*p'(mid)/p(mid)=d*diff/mnum.
    """
    d=len(b)-1
    if d==0: return b[:],b[:],D,b[0],0
    row=b[:]; left=[row[0]<<d]; right=[row[-1]<<d]
    diff=0
    for k in range(1,d+1):
        if len(row)==2: diff=row[1]-row[0]
        row=[a+c for a,c in zip(row,row[1:])]
        left.append(row[0]<<(d-k)); right.append(row[-1]<<(d-k))
    return left,list(reversed(right)),D<<d,row[0],diff

def partition_valid(cells):
    """Exact, order-independent dyadic cover; rejects gaps/overlaps/duplicates."""
    if not isinstance(cells,list) or not cells: return False
    clean=[]
    for item in cells:
        if isinstance(item,dict): d,i=item['depth'],item['index']
        else: d,i=item
        if not strict_int(d) or not strict_int(i) or d<0 or i<0 or i>=1<<d: return False
        clean.append((d,i))
    maxd=max(d for d,i in clean)
    segments=sorted((i<<(maxd-d),(i+1)<<(maxd-d)) for d,i in clean)
    endpoint=0
    for a,b in segments:
        if a!=endpoint: return False
        endpoint=b
    return endpoint==1<<maxd

def leaf_from_path(initial,d,i):
    node=initial
    for k in range(d-1,-1,-1):
        which=(i>>k)&1
        node=[(split_bernstein(b,D)[which],D<<((len(b)-1))) for b,D in node]
    return node

def evaluate(node,factors,mode='taylor2'):
    ranges=[(min(b),max(b)) for b,D in node]
    nonzero=all(lo>0 or hi<0 for lo,hi in ranges)
    if nonzero and mode!='hull':
        splits=[split_bernstein(b,D) for b,D in node]
        loghi=0; dl=du=0; curvature=0
        for f,s,(b,oldD),(lo,hi) in zip(factors,splits,node,ranges):
            L,R,D,m,diff=s; e=f['e']; deg=f['degw']
            loghi+=e*log_bounds(abs(m),D)[1]
            num=e*deg*diff*Q
            if m<0: num=-num;m=-m
            dl+=num//m;du+=ceildiv(num,m)
            if deg>=2:
                # For u=(w-mid)/halfwidth, log|p|''_u
                # = p''_u/p -(p'_u/p)^2 <= |p''_u|/min|p|.
                # Bernstein p''_u coefficients are d(d-1) Delta²b /4.
                # Taylor contributes at most 1/2 of this on |u|<=1.
                second=max(abs(b[k+2]-2*b[k+1]+b[k]) for k in range(deg-1))
                lower_abs=min(abs(lo),abs(hi))
                curvature+=ceildiv(Q*e*deg*(deg-1)*second,8*lower_abs)
        return loghi+max(abs(dl),abs(du))+curvature, 'taylor2',splits
    s=0
    for f,(b,D),(lo,hi) in zip(factors,node,ranges):
        bound=max(abs(lo),abs(hi))
        assert bound>0
        s+=f['e']*log_bounds(bound,D)[1]
    return s,'hull',None

def test_core():
    # Exact known extrema and de Casteljau midpoint agreement.
    cases=[([1,0],Fraction(1,4)),([4,-1],Fraction(1)),([16,-8,1],Fraction(1)),([1],Fraction(1)),([-1],Fraction(1))]
    for c,expected in cases:
        b,D=initial_bernstein(c)
        assert Fraction(max(map(abs,b)),D)>=expected
        L,R,E,m,di=split_bernstein(b,D)
        value=Fraction(0)
        for a in c: value=value*Fraction(1,8)+a
        assert Fraction(m,E)==value
        assert Fraction(L[0],E)==Fraction(b[0],D)
        assert Fraction(R[-1],E)==Fraction(b[-1],D)
        assert L[-1]==R[0]
    # Bernstein quadratic with exact interior extremum at w=1/8.
    b,D=initial_bernstein([-64,16,0])
    L,R,E,m,di=split_bernstein(b,D)
    assert Fraction(m,E)==1 and di==0
    assert max(L)<=E and max(R)<=E
    # Exact rational point checks are calibration, not continuum proof.
    for a in range(1,40):
        for b0 in range(1,20):
            l,u=log_bounds(a,b0);rl,ru=log_bounds(b0,a)
            assert l<=u and l+rl<=0<=u+ru
    assert log_bounds(1)==(0,0)
    assert log_bounds(2)==LOG2
    assert LOG2[0] > Q//2 and LOG2[1] < Q
    assert partition_valid([[1,0],[2,2],[2,3]])
    assert not partition_valid([[1,0],[2,3]])
    assert not partition_valid([[0,0],[1,0]])
    return {'core_controls':'PASS','log_precision_bits':P,'log_series_terms':TERMS}

def atomic_json(path,obj):
    p=Path(path); q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(obj,indent=2)+'\n');q.replace(p)

def run(args):
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    t0=time.monotonic(); controls=test_core()
    obj,sha,N=parse_certificate(args.certificate);factors=obj['factors']
    threshold=Fraction(args.threshold)
    assert threshold>0
    threshold_log_lo=log_bounds(threshold.numerator,threshold.denominator)[0]
    target=2*N*threshold_log_lo
    initial=[initial_bernstein(f['coeffs_desc_w']) for f in factors]
    supplied=None
    if args.partition:
        supplied=json.loads(Path(args.partition).read_text())
        assert partition_valid(supplied), 'partition gap, overlap or invalid cell'
        stack=[]
        for item in supplied:
            d,i=(item['depth'],item['index']) if isinstance(item,dict) else item
            # Reconstruct supplied cells one at a time, not one large array
            # of coefficient trees for the whole partition.
            stack.append((d,i,None))
    else: stack=[(0,0,initial)]
    leaves=[]; visited=0; methods=collections.Counter(); maxdepth=0; max_upper=None; maxcell=None
    last_checkpoint=t0; incomplete=False
    while stack:
        if (args.max_nodes and visited>=args.max_nodes) or time.monotonic()-t0>args.seconds:
            incomplete=True;break
        d,i,node=stack.pop();visited+=1;maxdepth=max(maxdepth,d)
        if node is None: node=leaf_from_path(initial,d,i)
        ub,method,splits=evaluate(node,factors,args.mode)
        if ub<target:  # Strict computational separation proves <= requested rational threshold.
            leaves.append({'depth':d,'index':i,'upper_scaled':str(ub),'method':method})
            methods[method]+=1
            if max_upper is None or ub>max_upper: max_upper,maxcell=ub,[d,i]
        else:
            if supplied is not None or d>=args.max_depth:
                incomplete=True;stack.append((d,i,node));break
            if splits is None: splits=[split_bernstein(b,D) for b,D in node]
            left=[(s[0],s[2]) for s in splits];right=[(s[1],s[2]) for s in splits]
            stack.append((d+1,2*i+1,right));stack.append((d+1,2*i,left))
        if time.monotonic()-last_checkpoint>args.checkpoint_seconds:
            atomic_json(out/'checkpoint.json',{'visited':visited,'accepted':len(leaves),'pending':len(stack),'elapsed_seconds':time.monotonic()-t0,'last_cell':[d,i]})
            print(json.dumps({'checkpoint':visited,'accepted':len(leaves),'pending':len(stack)}),flush=True)
            last_checkpoint=time.monotonic()
    cover_complete=(not incomplete and not stack and partition_valid(leaves))
    atomic_json(out/'partition.json',leaves)
    result={**controls,'claim_level':'PROVED-HERE' if cover_complete else 'INCONCLUSIVE','certificate_sha256':sha,'threshold_exact':str(threshold),'threshold_decimal_input':args.threshold,'factor_count':len(factors),'w_degree':N,'x_degree':2*N,'unweighted_degree_sum':sum(f['degw'] for f in factors),'real_rootedness':'not assumed or tested','checker_variant':'portable_v1','site_packages_disabled':bool(sys.flags.no_site),'visited':visited,'accepted_leaves':len(leaves),'pending_cells':len(stack),'maximum_depth':maxdepth,'accepted_methods':dict(methods),'finite_cover_complete':cover_complete,'max_accepted_upper_scaled':str(max_upper),'comparison_target_scaled':str(target),'minimum_acceptance_margin_scaled':str(target-max_upper) if max_upper is not None else None,'worst_accepted_cell':maxcell,'common_scale_denominator':str(Q),'normalization':2*N,'elapsed_seconds':time.monotonic()-t0,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python_version':sys.version,'pid':os.getpid(),'mode':args.mode}
    atomic_json(out/'result.json',result)
    # A checkpoint stores exact cell addresses so recomputing the Bernstein data
    # recovers a paused traversal without serialising large coefficient arrays.
    atomic_json(out/'checkpoint.json',{'completed':cover_complete,'accepted_file':'partition.json','pending':[[d,i] for d,i,node in stack],'visited':visited,'elapsed_seconds':time.monotonic()-t0})
    print(json.dumps(result,indent=2),flush=True)
    return 0 if cover_complete else 2

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',required=True);ap.add_argument('--threshold',default='0.422684697505');ap.add_argument('--out',required=True);ap.add_argument('--seconds',type=float,default=50);ap.add_argument('--max-nodes',type=int,default=0);ap.add_argument('--max-depth',type=int,default=60);ap.add_argument('--checkpoint-seconds',type=float,default=120);ap.add_argument('--mode',choices=['taylor2','hull'],default='taylor2');ap.add_argument('--partition')
    try: sys.exit(run(ap.parse_args()))
    except (AssertionError,KeyError,ValueError,TypeError) as e:
        print(json.dumps({'claim_level':'INVALID_INPUT_OR_FAILED_CONTROL','error':str(e)}),flush=True);sys.exit(3)
