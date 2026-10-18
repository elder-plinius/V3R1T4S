#!/usr/bin/env python3
"""Standalone exact-Z verifier for an ordered 5x5x5 rank-93 ternary SLP.

Verification functions are copied verbatim from the independent checker
written before claim/verify.py was inspected. This CLI uses only the
standard library, its JSON argument, and memory. It performs no network
access and writes no files.
"""
import json
import pathlib
import sys

class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def exact_int(x):
    return type(x) is int


def read_json(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            need(key not in out, 'duplicate JSON key: ' + key)
            out[key] = value
        return out
    return json.loads(path.read_text(), object_pairs_hook=unique)


def inspect_rows(rows, available, label):
    need(type(rows) is list, label + ' must be list')
    for r, terms in enumerate(rows):
        need(type(terms) is list, label + ' row must be list')
        limit = available(r)
        for term in terms:
            need(type(term) is dict and set(term) == {'index', 'value'},
                 label + ' unexpected expression/arithmetic field')
            idx, sign = term['index'], term['value']
            need(exact_int(idx) and 0 <= idx < limit,
                 label + ' reference is noninteger, negative or not backward/available')
            need(exact_int(sign) and sign in (-1, 1),
                 label + ' literal scalar must be +1 or -1')


def expand_stage(base_size, fresh, outputs):
    # Intermediate coefficients may exceed one. They represent paid sums,
    # never free scalar multiplication. Only FINAL factors are ternary.
    library = [[int(i == j) for j in range(base_size)] for i in range(base_size)]
    def row(terms):
        out = [0] * base_size
        for term in terms:
            vector = library[term['index']]
            sign = term['value']
            for q in range(base_size):
                out[q] += sign * vector[q]
        return out
    for terms in fresh:
        library.append(row(terms))
    final = [row(terms) for terms in outputs]
    cost = sum(max(0, len(terms) - 1) for terms in fresh + outputs)
    return final, library[base_size:], cost


def literal_stage(base, fresh, outputs):
    library = list(base)
    additions = 0
    def row(terms):
        nonlocal additions
        if not terms:
            return 0
        first = terms[0]
        accumulator = library[first['index']]
        if first['value'] == -1:
            accumulator = -accumulator
        for term in terms[1:]:
            # Explicitly one binary +/-; no dot product, cancellation,
            # repeated-ref shortcut, or nonunit scalar shortcut.
            if term['value'] == 1:
                accumulator = accumulator + library[term['index']]
            else:
                accumulator = accumulator - library[term['index']]
            additions += 1
        return accumulator
    for terms in fresh:
        library.append(row(terms))
    return [row(terms) for terms in outputs], additions


def schema(data, expected_n=None, expected_rank=None):
    need(type(data) is dict, 'object must be dict')
    required = {'n', 'm', 'z2', 'complexity', 'u_fresh', 'u', 'v_fresh', 'v', 'w_fresh', 'w'}
    need(required <= set(data) <= required | {'research_method'}, 'unexpected/missing top-level field')
    if 'research_method' in data:
        need(type(data['research_method']) is str, 'research_method is inert string metadata')
    n = data['n']
    need(type(n) is list and len(n) == 3 and all(exact_int(x) and 0 < x <= 8 for x in n), 'invalid format')
    need(expected_n is None or n == expected_n, 'wrong ordered format')
    rank = data['m']
    need(exact_int(rank) and rank > 0, 'invalid multiplication count')
    need(expected_rank is None or rank == expected_rank, 'wrong multiplication count')
    need(data['z2'] is False, 'integer computation requires z2 false')
    need(type(data['complexity']) is dict and set(data['complexity']) == {'naive', 'reduced'}, 'invalid cost metadata')
    need(all(exact_int(v) and v >= 0 for v in data['complexity'].values()), 'invalid cost number')
    sizes = {'u': n[0] * n[1], 'v': n[1] * n[2], 'w': rank}
    lengths = {'u': rank, 'v': rank, 'w': n[0] * n[2]}
    for name, base in sizes.items():
        fresh, outputs = data[name + '_fresh'], data[name]
        inspect_rows(fresh, lambda r: base + r, name + '_fresh')
        inspect_rows(outputs, lambda r: base + len(fresh), name)
        need(len(outputs) == lengths[name], name + ' wrong final vector count')
    return n, rank


def expected_tensor(n):
    n1, n2, n3 = n
    aa, bb, cc = n1*n2, n2*n3, n3*n1
    expected = [0] * (aa * bb * cc)
    for i in range(n1):
        for k in range(n2):
            for j in range(n3):
                a, b, c = i*n2+k, k*n3+j, j*n1+i
                expected[(a * bb + b) * cc + c] = 1
    return expected


def tensor_of(U, V, W):
    aa, bb, cc = len(U[0]), len(V[0]), len(W)
    out = [0] * (aa * bb * cc)
    for r in range(len(U)):
        for a, ua in enumerate(U[r]):
            if not ua:
                continue
            for b, vb in enumerate(V[r]):
                if not vb:
                    continue
                for c in range(cc):
                    out[(a * bb + b) * cc + c] += ua * vb * W[c][r]
    return out


def canon(vector):
    sign = next((1 if x > 0 else -1 for x in vector if x), 1)
    return tuple(sign*x for x in vector), sign


def verify(data, expected_n=None, expected_rank=None, strict=True):
    n, rank = schema(data, expected_n, expected_rank)
    expanded = {}
    intermediates = {}
    cost_by_stage = {}
    for name, base in [('u', n[0]*n[1]), ('v', n[1]*n[2]), ('w', rank)]:
        expanded[name], intermediates[name], cost_by_stage[name] = expand_stage(
            base, data[name + '_fresh'], data[name])
    U, V, W = expanded['u'], expanded['v'], expanded['w']
    final_max = max(abs(x) for rows in expanded.values() for row in rows for x in row)
    ternary = final_max <= 1
    activity = [all(any(row) for row in U), all(any(row) for row in V),
                all(any(W[c][r] for c in range(len(W))) for r in range(rank))]
    summands = []
    signed_summands = []
    for r in range(rank):
        cu, su = canon(U[r]); cv, sv = canon(V[r]); cw, sw = canon([row[r] for row in W])
        summands.append((cu, cv, cw))
        signed_summands.append((cu, cv, cw, su*sv*sw))
    distinct_up_to_sign = len(set(summands))
    distinct_signed = len(set(signed_summands))
    naive = sum(max(0, sum(x != 0 for x in row)-1) for row in U+V+W)
    cost = sum(cost_by_stage.values())
    wanted = expected_tensor(n)
    observed = tensor_of(U, V, W)
    mismatch = [q for q, (x,y) in enumerate(zip(observed,wanted)) if x != y]
    mod2_mismatch = sum((x-y) % 2 != 0 for x,y in zip(observed,wanted))
    literal_mismatches = 0
    literal_pairs = 0
    operations_total = 0
    for a in range(n[0]*n[1]):
        for b in range(n[1]*n[2]):
            avec = [int(q == a) for q in range(n[0]*n[1])]
            bvec = [int(q == b) for q in range(n[1]*n[2])]
            u, ca = literal_stage(avec, data['u_fresh'], data['u'])
            v, cb = literal_stage(bvec, data['v_fresh'], data['v'])
            products = [u[r]*v[r] for r in range(rank)]
            result, cw = literal_stage(products, data['w_fresh'], data['w'])
            cstart = (a*len(bvec)+b)*len(W)
            literal_mismatches += sum(x != y for x,y in zip(result, wanted[cstart:cstart+len(W)]))
            need(ca+cb+cw == cost, 'literal instruction count changed during execution')
            operations_total += ca+cb+cw
            literal_pairs += 1
    result = {
        'n': n, 'multiplications': rank, 'final_ternary': ternary, 'max_abs_final_coefficient': final_max,
        'active_u_v_w': activity, 'distinct_summands_up_to_sign': distinct_up_to_sign,
        'distinct_signed_summands': distinct_signed, 'binary_additions_by_stage': cost_by_stage,
        'binary_additions': cost, 'expanded_naive_additions': naive,
        'metadata_naive_matches': naive == data['complexity']['naive'],
        'metadata_reduced_matches': cost == data['complexity']['reduced'],
        'tensor_coefficients_checked': len(wanted), 'integer_tensor_mismatches': len(mismatch),
        'mod2_tensor_mismatches': mod2_mismatch, 'literal_basis_pairs': literal_pairs,
        'literal_output_coefficients_checked': literal_pairs*len(W),
        'literal_output_mismatches': literal_mismatches, 'literal_binary_operations_total': operations_total,
        'max_abs_intermediate_by_stage': {
            name: max((abs(x) for row in rows for x in row), default=0)
            for name, rows in intermediates.items()},
        'fresh_counts': {name: len(data[name+'_fresh']) for name in ('u','v','w')},
        'final_counts': {name: len(data[name]) for name in ('u','v','w')},
        'fresh_arity_sets': {name: sorted(set(map(len,data[name+'_fresh']))) for name in ('u','v','w')},
        'final_arity_sets': {name: sorted(set(map(len,data[name]))) for name in ('u','v','w')},
    }
    failures = []
    checks = [(ternary, 'final factor not ternary'), (all(activity), 'inactive multiplication'),
              (distinct_up_to_sign == rank, 'duplicate/proportional tensor summand'),
              (cost == data['complexity']['reduced'], 'reduced cost metadata mismatch'),
              (naive == data['complexity']['naive'], 'naive cost metadata mismatch'),
              (not mismatch, 'integer tensor mismatch'), (literal_mismatches == 0, 'literal execution mismatch')]
    for passed, reason in checks:
        if not passed:
            failures.append(reason)
    result['failures'] = failures
    result['pass'] = not failures
    if strict:
        need(not failures, ', '.join(failures))
    return result

def main():
    if len(sys.argv) != 2:
        print(json.dumps({'pass': False, 'error': 'usage: portable.py scheme.json'}))
        return 2
    try:
        data = read_json(pathlib.Path(sys.argv[1]))
        diagnostics = verify(data, expected_n=[5, 5, 5], expected_rank=93, strict=False)
    except Exception as error:
        print(json.dumps({'pass': False, 'error': str(error)}))
        return 1
    print(json.dumps(diagnostics, sort_keys=True))
    return 0 if diagnostics['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
