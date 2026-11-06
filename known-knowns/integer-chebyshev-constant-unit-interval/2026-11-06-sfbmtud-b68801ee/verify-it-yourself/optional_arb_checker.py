#!/usr/bin/env python3
"""Independent Arb polynomial/Taylor cover verifier; no author's code used.

Input coefficients are descending exact integers. A leaf [d,k] is the closed
interval [k/2**(d+2), (k+1)/2**(d+2)]. All proof arithmetic is Arb; ordinary floats
are used only for time limits and human-readable diagnostics.
"""
import argparse
import hashlib
import json
import os
import resource
from pathlib import Path
import time
from fractions import Fraction
from flint import arb, arb_poly, ctx


def exact_int(x):
    return type(x) is int


def validate(data):
    for key in ('N_w_degree', 'x_degree', 'n_factors'):
        if not exact_int(data[key]) or data[key] <= 0:
            raise ValueError('positive exact integer required: '+key)
    if len(data['factors']) != data['n_factors']:
        raise ValueError('factor count mismatch')
    degree = 0
    for j, f in enumerate(data['factors']):
        c = f['coeffs_desc_w']
        if not isinstance(c, list) or len(c) < 1:
            raise ValueError('nonempty coefficient list required')
        if not all(exact_int(a) for a in c) or c[0] == 0:
            raise ValueError('integer coefficients and nonzero leading coefficient required')
        if not exact_int(f['e']) or f['e'] <= 0:
            raise ValueError('positive integer exponent required')
        if not exact_int(f['degw']) or f['degw'] != len(c)-1:
            raise ValueError('factor degree mismatch')
        degree += f['e']*f['degw']
    if degree != data['N_w_degree'] or 2*degree != data['x_degree']:
        raise ValueError('declared total degree mismatch')
    return degree


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, data):
    path = Path(path)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data, indent=2)+'\n')
    os.replace(tmp, path)


class Checker:
    def __init__(self, data, threshold, bits=192):
        ctx.prec = bits
        self.degree = validate(data)
        self.bits = bits
        rational = Fraction(threshold)
        if rational <= 0:
            raise ValueError('positive threshold required')
        self.threshold = str(rational)
        self.limit = (arb(rational.numerator)/rational.denominator).log().lower()
        self.polys = [arb_poly(list(reversed(f['coeffs_desc_w']))) for f in data['factors']]
        self.weights = [arb(f['e'])/(2*self.degree) for f in data['factors']]
        self.factor_count = len(self.polys)
        self.root_count_with_multiplicity = sum(f['degw'] for f in data['factors'])

    @staticmethod
    def cell(d, k):
        if not exact_int(d) or not exact_int(k) or d < 0 or k < 0 or k >= 2**d:
            raise ValueError('invalid dyadic cell')
        return arb((2*k+1, -d-3)), arb((1, -d-3))

    def bound(self, d, k, method='taylor'):
        m, h = self.cell(d, k)
        z = arb(0, h)
        x = arb(m, h)
        factor_upper = arb(0)
        f0 = arb(0)
        f1 = arb(0)
        f2 = arb(0)
        smooth = method == 'taylor'
        shift = arb_poly([m, 1])
        for p, weight in zip(self.polys, self.weights):
            if method == 'horner':
                r = p(x)
                q = None
                sup = r.abs_upper()
            else:
                q = p(shift)
                r = q(z)
                # Triangle inequality at the exact dyadic radius avoids the
                # fixed-precision interval-radius slack in r.abs_upper().
                sup = arb_poly([a.abs_upper() for a in q.coeffs()])(h).upper()
            if sup.is_zero():
                return arb.neg_inf(), 'identically_zero'
            factor_upper += weight*sup.log()
            if smooth:
                if r.contains(0):
                    smooth = False
                    continue
                rp = q.derivative()
                rv1 = rp(z)
                rv2 = rp.derivative()(z)
                f0 += weight*abs(q[0]).log()
                f1 += weight*q[1]/q[0]
                f2 += weight*(rv2/r-(rv1/r)**2)
        best = factor_upper.upper()
        used = 'factor'
        if smooth:
            b = f1.abs_upper()
            c = f2.upper()
            # For |t|<=h, F(m+t)<=F0+b|t|+c*t*t/2. Maximize
            # that scalar quadratic with outward arithmetic and safe comparison.
            if c < 0 and b <= (-c*h).lower():
                extra = -b*b/(2*c)
            elif c < 0:
                extra = b*h+c*h*h/2
            else:
                extra = b*h+c*h*h/2
            candidate = (f0+extra).upper()
            if candidate < best:
                best = candidate
                used = 'taylor'
        return best, used

    def accept(self, upper):
        return upper <= self.limit


def verify_cover(leaves):
    if not leaves:
        raise ValueError('empty partition')
    cells = []
    for d,k in leaves:
        Checker.cell(d,k)
        cells.append((Fraction(k,2**(d+2)),Fraction(k+1,2**(d+2))))
    cells.sort()
    cursor = Fraction(0)
    for a,b in cells:
        if a != cursor:
            raise ValueError('gap or overlap in partition')
        cursor = b
    if cursor != Fraction(1,4):
        raise ValueError('partition does not cover [0,1/4]')
    return True


def run_search(c, args, source_hash):
    started = time.monotonic()
    Path(str(args.proof)+'.pid').write_text(str(os.getpid())+'\n')
    pending = [[0,0]]
    leaves = []
    upper_dyadics = []
    processed = 0
    method_counts = {'factor':0,'taylor':0,'identically_zero':0}
    max_depth = 0
    max_upper = arb.neg_inf()
    last_checkpoint = started
    if args.resume and Path(args.proof).exists():
        old = json.loads(Path(args.proof).read_text())
        if old['source_sha256'] != source_hash or old['threshold'] != c.threshold or old['bits'] != c.bits or old['method'] != args.method:
            raise ValueError('resume metadata mismatch')
        pending, leaves = old['pending'], old['leaves']
        upper_dyadics = old['upper_dyadics']
        processed, method_counts, max_depth = old['processed'], old['method_counts'], old['max_depth']
        if old.get('max_accepted_upper_dyadic'):
            ma,ex=old['max_accepted_upper_dyadic']
            max_upper=arb((int(ma),ex))

    def record(status):
        elapsed = time.monotonic()-started
        state = dict(status=status, source_sha256=source_hash, threshold=c.threshold,
                     bits=c.bits, method=args.method, x_degree=2*c.degree,
                     N_w_degree=c.degree, factor_count=c.factor_count,
                     root_count_with_multiplicity=c.root_count_with_multiplicity,
                     processed=processed, accepted=len(leaves), pending=pending,
                     leaves=leaves, upper_dyadics=upper_dyadics,
                     max_depth=max_depth, method_counts=method_counts,
                     elapsed_seconds=elapsed, cells_per_second=(processed/elapsed if elapsed else 0),
                     log_threshold_lower=str(c.limit), max_accepted_upper=str(max_upper), pid=os.getpid(),
                     peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        state['max_accepted_upper_dyadic'] = ([str(max_upper.man_exp()[0]),int(max_upper.man_exp()[1])] if max_upper.is_finite() else None)
        atomic_json(args.proof,state)
        print(json.dumps({k:v for k,v in state.items() if k not in ('pending','leaves','upper_dyadics')},sort_keys=True),flush=True)
        return state

    while pending:
        if time.monotonic()-started >= args.seconds:
            return record('INCOMPLETE_TIME_LIMIT')
        d,k = pending.pop()
        upper, used = c.bound(d,k,args.method)
        processed += 1
        max_depth = max(max_depth,d)
        if c.accept(upper):
            leaves.append([d,k])
            mantissa,exponent=upper.man_exp()
            upper_dyadics.append([str(mantissa),int(exponent)])
            method_counts[used] += 1
            if upper > max_upper:
                max_upper = upper
        else:
            if d >= args.max_depth:
                pending.append([d,k])
                return record('INCOMPLETE_MAX_DEPTH')
            pending.append([d+1,2*k+1])
            pending.append([d+1,2*k])
        if time.monotonic()-last_checkpoint >= args.checkpoint_seconds:
            record('RUNNING')
            last_checkpoint = time.monotonic()
    verify_cover(leaves)
    return record('PASS_FINITE_COVER')


def replay(c,args,source_hash):
    proof = json.loads(Path(args.proof).read_text())
    if proof['source_sha256'] != source_hash or proof['threshold'] != c.threshold:
        raise ValueError('proof source/threshold mismatch')
    if (proof['N_w_degree'] != c.degree or proof['x_degree'] != 2*c.degree or
        proof['factor_count'] != c.factor_count or
        proof['root_count_with_multiplicity'] != c.root_count_with_multiplicity or
        proof['accepted'] != len(proof['leaves'])):
        raise ValueError('proof metadata mismatch')
    if proof.get('pending'):
        raise ValueError('proof still has pending cells')
    verify_cover(proof['leaves'])
    if len(proof['upper_dyadics']) != len(proof['leaves']):
        raise ValueError('missing per-cell upper bounds')
    started = time.monotonic()
    max_upper = arb.neg_inf()
    for n,(d,k) in enumerate(proof['leaves']):
        upper,used = c.bound(d,k,args.method)
        ma,ex=proof['upper_dyadics'][n]
        stated=arb((int(ma),ex))
        if not c.accept(stated):
            raise ValueError('stated cell bound misses threshold '+str([d,k]))
        if args.bits==proof['bits'] and args.method==proof['method'] and not upper <= stated:
            raise ValueError('recomputed bound exceeds stored bound '+str([d,k]))
        if not c.accept(upper):
            raise ValueError('unproved cell '+str([d,k]))
        if upper > max_upper:
            max_upper = upper
    result = dict(status='PASS_REPLAY', source_sha256=source_hash, leaves=n+1,
                  bits=c.bits, method=args.method, elapsed_seconds=time.monotonic()-started,
                  max_upper=str(max_upper), limit_lower=str(c.limit),
                  normalized_norm_upper=str(max_upper.exp().upper()))
    print(json.dumps(result,sort_keys=True),flush=True)
    return result


def controls():
    # Exact extrema and schema/coverage errors; no finite sampling proves a bound.
    data = dict(N_w_degree=1,x_degree=2,n_factors=1,
                factors=[dict(e=1,degw=1,coeffs_desc_w=[1,0])])
    c = Checker(data,'0.5')
    u,_ = c.bound(0,0)
    # Arb log upper cannot in general be <= a separate Arb log lower at exact
    # equality. Compare normalized enclosure with the known exact supremum.
    assert u.exp().contains(arb('0.5')) or u.exp() >= arb('0.5')
    assert Checker(data,'0.500000000001').accept(u)
    assert not Checker(data,'0.499999999999').accept(u)
    tests=['known_w_exact_norm_enclosed','w_above_threshold_pass','w_below_threshold_fail']
    for name,mutator in [
        ('wrong_total_degree', lambda d:d.update(x_degree=3)),
        ('wrong_w_degree',lambda d:d.update(N_w_degree=2)),
        ('wrong_factor_count',lambda d:d.update(n_factors=2)),
        ('negative_exponent',lambda d:d['factors'][0].update(e=-1)),
        ('fractional_exponent',lambda d:d['factors'][0].update(e=0.5)),
        ('bool_exponent',lambda d:d['factors'][0].update(e=True)),
        ('float_coefficient',lambda d:d['factors'][0].update(coeffs_desc_w=[1.0,0])),
        ('bool_coefficient',lambda d:d['factors'][0].update(coeffs_desc_w=[True,0])),
        ('leading_zero',lambda d:d['factors'][0].update(coeffs_desc_w=[0,1])),
    ]:
        d=json.loads(json.dumps(data)); mutator(d)
        try: validate(d)
        except ValueError: tests.append(name+'_rejected')
        else: raise AssertionError(name)
    assert verify_cover([[1,0],[2,2],[2,3]])
    tests.append('exact_partition_pass')
    for name,leaves in [('gap',[[2,0],[1,1]]),('overlap',[[0,0],[1,0]]),('missing_end',[[1,0]])]:
        try: verify_cover(leaves)
        except ValueError: tests.append(name+'_rejected')
        else: raise AssertionError(name)
    # Explicit shifted-polynomial enclosures at rational points for a quadratic.
    quad = dict(N_w_degree=2,x_degree=4,n_factors=1,
                factors=[dict(e=1,degw=2,coeffs_desc_w=[16,-4,0])])
    q=Checker(quad,'0.71')
    qu,_=q.bound(0,0)
    assert qu.exp() >= arb('0.5').sqrt()
    assert q.accept(q.bound(6,31)[0])
    tests.append('quadratic_cell_enclosure')
    print(json.dumps(dict(status='PASS_CONTROLS', count=len(tests), tests=tests)),flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--certificate', default='../../data/upper_certificate.json')
    p.add_argument('--threshold',default='0.422684697505')
    p.add_argument('--mode',choices=['pilot','search','replay','controls'],default='pilot')
    p.add_argument('--method',choices=['horner','shift','taylor'],default='taylor')
    p.add_argument('--bits',type=int,default=192)
    p.add_argument('--seconds',type=float,default=40)
    p.add_argument('--max-depth',type=int,default=80)
    p.add_argument('--checkpoint-seconds',type=float,default=120)
    p.add_argument('--proof',default='proof.json')
    p.add_argument('--resume',action='store_true')
    args=p.parse_args()
    if args.mode=='controls':
        controls();return
    data=json.loads(Path(args.certificate).read_text())
    c=Checker(data,args.threshold,args.bits)
    h=digest(args.certificate)
    if args.mode=='replay': replay(c,args,h)
    else: run_search(c,args,h)


if __name__=='__main__': main()
