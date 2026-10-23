#!/usr/bin/env python3
"""Deterministic semantic controls for the supplied integer SLP package.

Run from the package directory: python3 verify-it-yourself/semantic_controls.py
Only the standard library is needed. Mathematical entrypoints are called
without pinned-object hash options; the checkers themselves are unchanged.
Deliberately invalid objects exist only in memory, unless --fixtures is given.
A PASS covers these fixed controls, not every possible implementation fault.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

CASES = ('original', 'first_output_term_sign', 'whole_output_sign',
         'reduced_cost_plus_one', 'out_of_range_reference',
         'wrong_ring_flag', 'missing_product')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def independent(namespace, data):
    shape = tuple(data['n'])
    if shape == (3, 5, 5):
        return namespace['verify'](data)
    if shape == (2, 4, 8):
        return namespace['inspect'](data)[0]
    if shape == (4, 5, 8):
        return namespace['audit'](data)
    if shape == (2, 5, 6):
        return namespace['check'](data)[0]
    if shape == (4, 4, 6):
        return namespace['check'](data)
    if shape == (5, 5, 5):
        return namespace['verify'](data, strict=False)
    if shape == (3, 4, 5):
        return namespace['analyze'](data)
    if shape == (2, 5, 5):
        return namespace['check'](data)[0]
    raise RuntimeError('unregistered ordered shape')


def compact(result):
    # Preserve actual diagnostic witnesses, excluding large expanded/gate audits.
    return {key: value for key, value in result.items()
            if value is None or isinstance(value, (str, int, float, bool))
            or 'mismatch' in key or key in ('failures', 'integer_tensor_witness', 'basis_witness')}


def invoke(function, namespace, data, basis=False):
    started = time.perf_counter()
    try:
        result = function(data) if basis else independent(namespace, data)
        flags = ('valid',) if basis else ('pass', 'passed', 'exact_integer_identity', 'exact_Z_product')
        values = [result[key] for key in flags if key in result]
        if len(values) != 1 or type(values[0]) is not bool:
            raise RuntimeError('checker returned no unique Boolean acceptance flag')
        answer = {'accepted': values[0], 'diagnostics': compact(result)}
    except Exception as error:
        allowed = tuple(t for t in (namespace.get('CheckError'), namespace.get('Invalid'),
                                     namespace.get('Rejected'), ValueError) if isinstance(t, type))
        answer = {'accepted': False, 'exception': type(error).__name__, 'error': str(error),
                  'unexpected_exception': not isinstance(error, allowed)}
    answer['seconds'] = time.perf_counter() - started
    return answer


def mathematical_rejection(result):
    if result['accepted'] or result.get('unexpected_exception'):
        return False
    evidence = json.dumps(result.get('diagnostics', {}), sort_keys=True).lower()
    message = result.get('error', '').lower()
    tokens = ('tensor mismatch', 'basis pair mismatch', 'basis mismatch', 'basis-pair mismatch',
              'literal execution mismatch', 'literal scalar slp mismatch')
    if any(token in message for token in tokens):
        return True
    diagnostics = result.get('diagnostics', {})
    counts = ('tensor_failures', 'basis_failures', 'tensor_mismatches', 'direct_mismatches',
              'integer_tensor_mismatches', 'literal_output_mismatches',
              'coefficient_mismatch_count', 'basis_mismatch_count')
    return any(type(diagnostics.get(key)) is int and diagnostics[key] > 0 for key in counts)


def run(package, fixtures=None):
    started = time.perf_counter()
    objects = list((package / 'object').glob('*.json'))
    if len(objects) != 1:
        raise RuntimeError('one JSON object required')
    obj = objects[0]
    basis_path = package / 'verify-it-yourself' / 'basis_check.py'
    independent_path = package / 'verify-it-yourself' / 'independent_check.py'
    paths = (obj, basis_path, independent_path)
    original_hashes = {str(p.relative_to(package)): digest(p.read_bytes()) for p in paths}
    data = json.loads(obj.read_bytes())
    basis_ns = runpy.run_path(str(basis_path), run_name='semantic_controls_basis')
    independent_ns = runpy.run_path(str(independent_path), run_name='semantic_controls_independent')
    rows = []
    for name in CASES:
        changed = copy.deepcopy(data)
        if name == 'first_output_term_sign':
            changed['w'][0][0]['value'] *= -1
        elif name == 'whole_output_sign':
            for term in changed['w'][0]:
                term['value'] *= -1
        elif name == 'reduced_cost_plus_one':
            changed['complexity']['reduced'] += 1
        elif name == 'out_of_range_reference':
            changed['u'][0][0]['index'] = data['n'][0] * data['n'][1] + len(data['u_fresh'])
        elif name == 'wrong_ring_flag':
            changed['z2'] = True
        elif name == 'missing_product':
            changed['u'].pop()
        raw = json.dumps(changed, sort_keys=True, separators=(',', ':')).encode() + b'\n'
        # Every fixture is valid JSON. Semantic invalidity is intentional.
        changed = json.loads(raw)
        if fixtures is not None:
            fixtures.mkdir(parents=True, exist_ok=True)
            (fixtures / (name + '.json')).write_bytes(raw)
        row = {'case': name, 'fixture_sha256': digest(raw), 'fixture_bytes': len(raw),
               'independent': invoke(None, independent_ns, changed)}
        if name in ('original', 'first_output_term_sign', 'whole_output_sign'):
            row['basis'] = invoke(basis_ns['check'], basis_ns, changed, basis=True)
        if name == 'original':
            row['control_pass'] = row['independent']['accepted'] and row['basis']['accepted']
        elif name == 'whole_output_sign':
            row['control_pass'] = mathematical_rejection(row['independent']) and mathematical_rejection(row['basis'])
        elif name == 'first_output_term_sign':
            row['control_pass'] = (not row['independent']['accepted']
                                   and not row['independent'].get('unexpected_exception', False)
                                   and mathematical_rejection(row['basis']))
            row['independent_mathematical_mismatch_reported'] = mathematical_rejection(row['independent'])
        else:
            diagnostic = json.dumps(row['independent'], sort_keys=True).lower()
            terms = {'reduced_cost_plus_one': ('cost', 'count', 'metadata'),
                     'out_of_range_reference': ('reference', 'index'),
                     'wrong_ring_flag': ('integer', 'ring', 'z2'),
                     'missing_product': ('count', 'dimension', 'factor', 'terminal')}[name]
            row['control_pass'] = (not row['independent']['accepted']
                                   and not row['independent'].get('unexpected_exception', False)
                                   and any(term in diagnostic for term in terms))
        rows.append(row)
    after_hashes = {str(p.relative_to(package)): digest(p.read_bytes()) for p in paths}
    unchanged = original_hashes == after_hashes
    return {'pass': unchanged and all(row['control_pass'] for row in rows),
            'scope': 'Fixed deterministic semantic/schema controls; no exhaustive fault-detection claim.',
            'hash_guard_bypassed': True, 'checker_source_modified': False,
            'format': data['n'], 'rank': data['m'], 'original_sha256': digest(obj.read_bytes()),
            'original_and_checker_hashes': original_hashes,
            'original_and_checker_bytes_unchanged': unchanged,
            'case_order': list(CASES), 'controls': rows, 'seconds': time.perf_counter() - started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=Path.cwd())
    parser.add_argument('--fixtures', type=Path)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    receipt = run(args.package, args.fixtures)
    text = json.dumps(receipt, indent=2, sort_keys=True) + '\n'
    if args.receipt is not None:
        args.receipt.write_text(text)
    print(text, end='')
    print('SEMANTIC_CONTROLS: ' + ('PASS' if receipt['pass'] else 'FAIL'))
    return 0 if receipt['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
