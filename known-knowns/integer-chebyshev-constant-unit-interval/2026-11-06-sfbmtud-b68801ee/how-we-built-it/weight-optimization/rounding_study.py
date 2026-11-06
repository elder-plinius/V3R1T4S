#!/usr/bin/env python3
"""Heuristic exponent-compression experiment; no rigorous norm claim."""
import argparse
import hashlib
import json
import math
import resource
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from flint import ctx
from optimize import Library, write


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate')
    ap.add_argument('output')
    args = ap.parse_args()
    begin = time.monotonic()
    ctx.prec = 256
    source = Path(args.certificate)
    original = json.loads(source.read_text())
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    factors = original['factors']
    lib = Library(factors)
    denominator = original['N_w_degree']
    rows = []
    for scale in [10**k for k in range(5, 16)]:
        exponents = [round(Fraction(f['e'] * scale, denominator)) for f in factors]
        degree = sum(e * f['degw'] for e, f in zip(exponents, factors))
        weights = np.array([float(Fraction(e * f['degw'], degree)) for e, f in zip(exponents, factors)])
        _, values, _ = lib.extrema(weights)
        proposed = [dict(f, e=e) for f, e in zip(factors, exponents) if e > 0]
        candidate = {
            'problem': 'HEURISTIC degree-compression candidate; rigorous verification required',
            'variable': 'w=x(1-x)',
            'N_w_degree': degree,
            'x_degree': 2 * degree,
            'n_factors': len(proposed),
            'factors': proposed,
            'source_certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'rounding': 'exact Fraction round to nearest, ties to even',
            'requested_degree_scale': scale,
        }
        write(out / f'scale_{scale}.json', candidate)
        rows.append({'scale': scale, 'actual_x_degree': 2 * degree,
                     'factor_count': len(proposed),
                     'heuristic_normalized_norm': math.exp(float(values.max()) / 2)})
        write(out / 'checkpoint.json', {'rows': rows})
    result = {'classification': 'HEURISTIC; all norms need rigorous continuum verification',
              'rows': rows, 'elapsed_seconds': time.monotonic() - begin,
              'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    write(out / 'summary.json', result)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
