#!/usr/bin/env python3
"""Independent exact/Arb fixed-library dual checker. No optimizer is imported."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys
from flint import arb,ctx

class InvalidWitness(ValueError): pass

def exact_rational(text,label):
    if type(text) is not str: raise InvalidWitness(label+' must be an exact rational string')
    try: return Fraction(text)
    except (ValueError,ZeroDivisionError): raise InvalidWitness('invalid '+label)

def aball(q): return arb(q.numerator)/arb(q.denominator)

def exact_lower(x):
    q=x.lower().fmpq()
    return Fraction(int(q.numerator),int(q.denominator))

def exact_upper(x):
    q=x.upper().fmpq()
    return Fraction(int(q.numerator),int(q.denominator))

def floor_decimal(q,digits=18):
    scale=10**digits
    return str(Fraction((q.numerator*scale)//q.denominator,scale))

def floor_decimal_string(q,digits=18):
    scale=10**digits
    scaled=(q.numerator*scale)//q.denominator
    sign='-' if scaled<0 else ''
    whole,remainder=divmod(abs(scaled),scale)
    return sign+str(whole)+'.'+str(remainder).zfill(digits)

def evaluate(library_bytes, measure, precision=192):
    if type(precision) is not int or precision<64: raise InvalidWitness('precision must be integer >=64')
    ctx.prec=precision
    if not isinstance(measure,dict) or measure.get('format')!='fixed-library-dual-v1': raise InvalidWitness('wrong measure format')
    digest=hashlib.sha256(library_bytes).hexdigest()
    if measure.get('library_sha256')!=digest: raise InvalidWitness('library digest mismatch')
    try: library=json.loads(library_bytes)
    except (json.JSONDecodeError,UnicodeDecodeError): raise InvalidWitness('invalid library JSON')
    if not isinstance(library,dict) or not isinstance(library.get('factors'),list): raise InvalidWitness('missing factor list')
    factors=library['factors']
    if not factors: raise InvalidWitness('empty library')
    if type(measure.get('n_factors')) is not int or measure['n_factors']!=len(factors): raise InvalidWitness('factor count mismatch')
    threshold=exact_rational(measure.get('threshold'),'threshold')
    if threshold<=0: raise InvalidWitness('threshold must be positive')
    parsed=[]
    for j,factor in enumerate(factors):
        if not isinstance(factor,dict): raise InvalidWitness('invalid factor')
        coeffs=factor.get('coeffs_desc_w');degree=factor.get('degw')
        if not isinstance(coeffs,list) or not coeffs or any(type(c) is not int for c in coeffs): raise InvalidWitness('factor coefficients must be exact integers')
        if type(degree) is not int or degree<1 or degree!=len(coeffs)-1 or coeffs[0]==0: raise InvalidWitness('factor degree mismatch or zero leading coefficient')
        parsed.append((degree,coeffs))
    support=measure.get('support')
    if not isinstance(support,list) or not support: raise InvalidWitness('empty/missing support')
    points=[]
    for atom in support:
        if not isinstance(atom,dict): raise InvalidWitness('invalid atom')
        x=exact_rational(atom.get('w'),'support point')
        mass=exact_rational(atom.get('mass'),'mass')
        if x<0 or x>Fraction(1,4): raise InvalidWitness('support outside [0,1/4]')
        if mass<=0: raise InvalidWitness('mass must be strictly positive; omit zero atoms')
        points.append((x,mass))
    total=sum((m for _,m in points),Fraction(0))
    if total!=1: raise InvalidWitness('mass total is not exactly one')
    max_degree=max(d for d,_ in parsed)
    prepared=[]
    for x,mass in points:
        qpowers=[1]
        for _ in range(max_degree): qpowers.append(qpowers[-1]*x.denominator)
        prepared.append((x.numerator,x.denominator,qpowers,aball(mass),arb(x.denominator).log()))
    target=2*aball(threshold).log()
    integrals=[]
    for j,(degree,coeffs) in enumerate(parsed):
        integral=arb(0)
        for k,(p,q,qpowers,massball,logq) in enumerate(prepared):
            numerator=coeffs[0]
            for exponent,coefficient in enumerate(coeffs[1:],1):
                numerator=numerator*p+coefficient*qpowers[exponent]
            # Exact polynomial value is numerator / q**degree.
            if numerator==0:
                return {'status':'NO_FINITE_OBSTRUCTION','reason':'factor vanishes at positive-mass support atom',
                        'factor_index':j,'atom_index':k,'precision_bits':precision},2
            logarithm=arb(abs(numerator)).log()-degree*logq
            integral+=massball*logarithm
        integral/=degree
        lower=exact_lower(integral);upper=exact_upper(integral)
        integrals.append({'factor_index':j,'degree':degree,'integral_ball':integral.str(55),
                          'lower_exact':str(lower),'upper_exact':str(upper),
                          'strictly_above_target':bool(integral>target)})
    lower=min(Fraction(x['lower_exact']) for x in integrals)
    lower_index=min(range(len(integrals)),key=lambda j:Fraction(integrals[j]['lower_exact']))
    threshold_margin=aball(lower)-target
    norm_lower_ball=(aball(lower)/2).exp()
    passed=all(x['strictly_above_target'] for x in integrals)
    return {'status':'CERTIFIED_FIXED_LIBRARY_OBSTRUCTION' if passed else 'NOT_CERTIFIED_AT_THRESHOLD',
            'scope':'All nonnegative real degree-normalized weights on this exact finite library only.',
            'library_sha256':digest,'precision_bits':precision,'support_count':len(points),
            'factor_count':len(parsed),'exact_mass_total':str(total),'threshold':str(threshold),
            'target_log_w_ball':target.str(55),'minimum_integral_lower_exact':str(lower),
            'minimum_integral_lower_decimal_floor':floor_decimal(lower,18),
            'minimum_integral_lower_decimal':floor_decimal_string(lower,18),
            'limiting_factor_index_by_lower_endpoint':lower_index,
            'normalized_norm_lower_decimal_floor':floor_decimal(exact_lower(norm_lower_ball),18),
            'normalized_norm_lower_decimal':floor_decimal_string(exact_lower(norm_lower_ball),18),
            'log_w_margin_over_threshold_lower_decimal_floor':floor_decimal(exact_lower(threshold_margin),18),
            'log_w_margin_over_threshold_lower_decimal':floor_decimal_string(exact_lower(threshold_margin),18),
            'integrals':integrals},0 if passed else 2

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library',required=True);parser.add_argument('--measure',required=True)
    parser.add_argument('--precision',type=int,default=192);parser.add_argument('--out')
    args=parser.parse_args()
    try:
        data=Path(args.library).read_bytes();measure=json.loads(Path(args.measure).read_text())
        result,code=evaluate(data,measure,args.precision)
    except (InvalidWitness,ValueError,TypeError,KeyError,OverflowError) as error:
        result={'status':'REJECTED_INPUT','reason':str(error)};code=3
    encoded=json.dumps(result,indent=2)+'\n'
    if args.out: Path(args.out).write_text(encoded)
    summary={k:v for k,v in result.items() if k!='integrals'}
    print(json.dumps(summary,indent=2))
    return code

if __name__=='__main__': sys.exit(main())
