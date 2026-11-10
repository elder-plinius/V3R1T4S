#!/usr/bin/env python3
"""Exact, deterministic exponent compression; this does not prove the norm."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = '782f42518e5f248f778fbeca406ad9fa5d28d44dc31fd1b6b9e588ab87abde63'
SCALE = 10**12

def build(raw):
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('Unexpected frozen v8 source object')
    source = json.loads(raw)
    factors = []
    for factor in source['factors']:
        exponent = round(Fraction(factor['e'] * SCALE, source['N_w_degree']))
        if exponent > 0:
            factors.append(dict(factor, e=exponent))
    degree = sum(f['e'] * f['degw'] for f in factors)
    return {
        'problem': 'Explicit integer Chebyshev upper-bound witness on [0,1]',
        'variable': 'w=x(1-x)',
        'N_w_degree': degree,
        'x_degree': 2 * degree,
        'n_factors': len(factors),
        'factors': factors,
        'source_certificate_sha256': SOURCE_SHA256,
        'rounding': 'exact Fraction round to nearest, ties to even',
        'requested_degree_scale': SCALE,
    }

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source')
    ap.add_argument('output')
    args = ap.parse_args()
    result = build(Path(args.source).read_bytes())
    raw = (json.dumps(result, indent=2) + '\n').encode()
    Path(args.output).write_bytes(raw)
    print(hashlib.sha256(raw).hexdigest())

if __name__ == '__main__':
    main()
