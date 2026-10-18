#!/usr/bin/env python3
"""Independent complete integer checker, written before claim/verify.py was read.

Definition: for every i,j, C[i,j] = sum_k A[i,k]*B[k,j].
A[i,k] -> i*n2+k; B[k,j] -> k*n3+j; C[i,j] -> j*n1+i.
Each sparse form is a literal ordered sequence of signed references. A t-term
form is implemented by t-1 binary +/- gates. Sign changes and aliases are free.
Only the declared U*V products multiply quantities. Fresh references point back.
An intermediate expansion can contain 2; final U,V,W factors must be ternary.
"""
import argparse
import hashlib
import json
from pathlib import Path


class Invalid(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def integer(value):
    return type(value) is int


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=no_duplicate_keys)


def terms(row, limit, label):
    require(type(row) is list and len(row) > 0, label + ': nonempty sparse row required')
    for term in row:
        require(type(term) is dict and set(term) == {'index', 'value'}, label + ': unexpected arithmetic field')
        require(integer(term['index']) and 0 <= term['index'] < limit, label + ': forward or invalid reference')
        require(integer(term['value']) and term['value'] in (-1, 1), label + ': nonunit literal scalar')


def expand_side(data, side, base_count, final_count):
    fresh = data[side + '_fresh']
    finals = data[side]
    require(type(fresh) is list and type(finals) is list, side + ': arrays required')
    require(len(finals) == final_count, side + ': wrong final form count')
    values = [[int(i == j) for j in range(base_count)] for i in range(base_count)]
    cost_fresh = 0
    for number, row in enumerate(fresh):
        terms(row, base_count + number, side + '_fresh[' + str(number) + ']')
        expansion = [sum(term['value'] * values[term['index']][j] for term in row) for j in range(base_count)]
        values.append(expansion)
        cost_fresh += len(row) - 1
    expanded = []
    cost_final = 0
    for number, row in enumerate(finals):
        terms(row, len(values), side + '[' + str(number) + ']')
        expanded.append([sum(term['value'] * values[term['index']][j] for term in row) for j in range(base_count)])
        cost_final += len(row) - 1
    reached = set()
    pending = [term['index'] for row in finals for term in row]
    while pending:
        index = pending.pop()
        if index in reached:
            continue
        reached.add(index)
        if index >= base_count:
            pending.extend(term['index'] for term in fresh[index - base_count])
    dead = sorted(set(range(base_count, len(values))) - reached)
    require(not dead, side + ': dead fresh gates: ' + str(dead))
    require(all(value in (-1, 0, 1) for row in expanded for value in row), side + ': nonternary final factor')
    return expanded, {'fresh': cost_fresh, 'final': cost_final,
                      'total': cost_fresh + cost_final, 'fresh_count': len(fresh),
                      'max_intermediate_abs': max(abs(value) for row in values for value in row),
                      'dead_fresh': len(dead)}


def canonical_product(u, v):
    coefficients = tuple(a * b for a in u for b in v)
    first = next((value for value in coefficients if value), 0)
    return coefficients if first >= 0 else tuple(-value for value in coefficients)


def coefficient_check(u, v, output_forms, shape, modulus=None):
    n1, n2, n3 = shape
    compared = 0
    failures = []
    for a in range(n1 * n2):
        i, ka = divmod(a, n2)
        for b in range(n2 * n3):
            kb, j = divmod(b, n3)
            for output in range(n1 * n3):
                actual = sum(u[r][a] * v[r][b] * output_forms[output][r] for r in range(len(u)))
                expected = int(ka == kb and output == j * n1 + i)
                delta = actual - expected
                if modulus is not None:
                    delta %= modulus
                if delta and len(failures) < 8:
                    failures.append({'a': a, 'b': b, 'output': output,
                                     'actual': actual, 'expected': expected})
                compared += 1
    return compared, failures


def execute_forms(fresh, final, inputs):
    registers = list(inputs)
    def evaluate(row):
        accumulator = row[0]['value'] * registers[row[0]['index']]
        for term in row[1:]:
            accumulator += term['value'] * registers[term['index']]
        return accumulator
    for row in fresh:
        registers.append(evaluate(row))
    return [evaluate(row) for row in final]


def basis_check(data):
    n1, n2, n3 = data['n']
    pairs = 0
    compared = 0
    for a in range(n1 * n2):
        a_values = [int(index == a) for index in range(n1 * n2)]
        left = execute_forms(data['u_fresh'], data['u'], a_values)
        for b in range(n2 * n3):
            b_values = [int(index == b) for index in range(n2 * n3)]
            right = execute_forms(data['v_fresh'], data['v'], b_values)
            products = [x * y for x, y in zip(left, right)]
            result = execute_forms(data['w_fresh'], data['w'], products)
            for i in range(n1):
                for j in range(n3):
                    expected = sum(a_values[i * n2 + k] * b_values[k * n3 + j] for k in range(n2))
                    require(result[j * n1 + i] == expected,
                            'basis mismatch: ' + str((a, b, i, j, result[j * n1 + i], expected)))
                    compared += 1
            pairs += 1
    return pairs, compared


def check(data, expected_shape=None, expected_rank=None, expected_cost=None):
    required = {'n', 'm', 'z2', 'complexity', 'u_fresh', 'u', 'v_fresh', 'v', 'w_fresh', 'w'}
    require(type(data) is dict and required <= set(data), 'missing schema fields')
    require(set(data) <= required | {'research_method'}, 'unexpected top-level arithmetic field')
    if 'research_method' in data:
        require(type(data['research_method']) is str, 'research_method must be text metadata')
    shape = data['n']
    require(type(shape) is list and len(shape) == 3 and all(integer(n) and n > 0 for n in shape), 'invalid ordered shape')
    require(data['z2'] is False, 'integer ring required, z2 must be false')
    rank = data['m']
    require(integer(rank) and rank > 0, 'invalid rank')
    require(expected_shape is None or shape == expected_shape, 'immutable ordered shape mismatch')
    require(expected_rank is None or rank == expected_rank, 'immutable declared rank mismatch')
    n1, n2, n3 = shape
    u, uc = expand_side(data, 'u', n1 * n2, rank)
    v, vc = expand_side(data, 'v', n2 * n3, rank)
    outputs, wc = expand_side(data, 'w', rank, n1 * n3)
    w = [[outputs[o][r] for o in range(n1 * n3)] for r in range(rank)]
    active = sum(any(u[r]) and any(v[r]) and any(w[r]) for r in range(rank))
    require(active == rank, 'inactive declared product')
    distinct = len({canonical_product(u[r], v[r]) for r in range(rank)})
    require(distinct == rank, 'duplicate bilinear products up to free sign')
    cost = uc['total'] + vc['total'] + wc['total']
    require(expected_cost is None or cost == expected_cost, 'immutable candidate cost mismatch')
    naive = sum(sum(value != 0 for value in row) - 1 for row in u + v + outputs)
    metadata = data['complexity']
    require(type(metadata) is dict and set(metadata) == {'naive', 'reduced'} and
            all(integer(value) and value >= 0 for value in metadata.values()), 'invalid cost metadata')
    require(metadata['reduced'] == cost, 'reduced metadata mismatch')
    require(metadata['naive'] == naive, 'naive metadata mismatch')
    coefficient_count, mismatches = coefficient_check(u, v, outputs, shape)
    require(not mismatches, 'integer tensor mismatch: ' + json.dumps(mismatches))
    pairs, basis_values = basis_check(data)
    return {'shape': shape, 'rank': rank, 'active_products': active, 'distinct_products_up_to_sign': distinct,
            'cost': cost, 'naive_cost': naive, 'sides': {'u': uc, 'v': vc, 'w': wc},
            'integer_coefficients_checked': coefficient_count, 'basis_pairs_checked': pairs,
            'basis_output_values_checked': basis_values, 'final_factors_ternary': True,
            'literal_unit_signs_only': True, 'backward_references_only': True,
            'hidden_arithmetic': False, 'passed': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('object')
    parser.add_argument('--candidate', action='store_true')
    arguments = parser.parse_args()
    try:
        data = load(arguments.object)
        result = check(data, [4, 4, 6] if arguments.candidate else None,
                       73 if arguments.candidate else None, 264 if arguments.candidate else None)
        result['object_sha256'] = hashlib.sha256(Path(arguments.object).read_bytes()).hexdigest()
        print(json.dumps(result, indent=2))
    except (Invalid, KeyError, TypeError, IndexError, json.JSONDecodeError) as error:
        print(json.dumps({'passed': False, 'reason': str(error)}, indent=2))
        raise SystemExit(1)
