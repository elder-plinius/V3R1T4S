#!/usr/bin/env python3
"""Independent exact checker written from the published reduced-format definition.
Uses only the standard library. Does not import, execute, or read claim/verify.py.
The two exact checks are tensor contraction and literal scalar SLP execution on
all A/B basis pairs. Every JSON term and allocated intermediate is validated.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

class Invalid(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise Invalid(message)

def int_only(value):
    return type(value) is int

def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result

def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_keys)

def vector_info(vector):
    return {'nonzeros': sum(x != 0 for x in vector),
            'min': min(vector), 'max': max(vector)}

def build_stage(name, base, fresh, final, final_count):
    need(type(fresh) is list, name + '_fresh must be a list')
    need(type(final) is list and len(final) == final_count,
         name + ' final-form count disagrees with dimensions/rank')
    pool = [[int(i == j) for j in range(base)] for i in range(base)]
    audit = []
    rows = []
    dependencies = {}
    seen_finals = []
    def form(row, tag, allocated):
        need(type(row) is list and len(row) > 0, tag + ': empty/non-list form')
        indices = set()
        vector = [0] * base
        signed_terms = []
        for term_no, term in enumerate(row):
            at = tag + '.term[' + str(term_no) + ']'
            need(type(term) is dict and set(term) == {'index','value'}, at + ': term schema')
            index, value = term['index'], term['value']
            need(int_only(index) and 0 <= index < len(pool), at + ': illegal or forward reference')
            need(int_only(value) and value in (-1,1), at + ': scalar is not +/-1')
            need(index not in indices, at + ': repeated sparse index')
            indices.add(index)
            signed_terms.append({'index': index, 'sign': value})
            for position in range(base):
                vector[position] += value * pool[index][position]
        cost = len(row) - 1
        audit.append({'tag': tag, 'allocated_index': allocated,
                      'available_before': len(pool), 'terms': signed_terms,
                      'kind': 'alias_or_sign' if len(row) == 1 else 'sum',
                      'binary_additions': cost, 'expanded': vector,
                      'expanded_summary': vector_info(vector)})
        return vector, indices
    for number, row in enumerate(fresh):
        allocated = base + number
        vector, deps = form(row, name + '_fresh[' + str(number) + ']', allocated)
        dependencies[allocated] = deps
        pool.append(vector)
    for number, row in enumerate(final):
        vector, deps = form(row, name + '[' + str(number) + ']', None)
        rows.append(vector)
        seen_finals.append(deps)
    live = set().union(*seen_finals)
    pending = list(live)
    while pending:
        index = pending.pop()
        for dep in dependencies.get(index, ()):
            if dep not in live:
                live.add(dep)
                pending.append(dep)
    dead = sorted(set(dependencies) - live)
    need(not dead, name + ': dead intermediate(s): ' + str(dead))
    return {'rows': rows, 'audit': audit, 'pool': pool,
            'cost': sum(item['binary_additions'] for item in audit),
            'fresh_cost': sum(item['binary_additions'] for item in audit[:len(fresh)]),
            'final_cost': sum(item['binary_additions'] for item in audit[len(fresh):]),
            'fresh_count': len(fresh), 'alias_count': sum(item['kind'] == 'alias_or_sign' for item in audit),
            'live_intermediates': sorted(set(dependencies) & live)}

def scalar_stage(base_values, fresh, final):
    pool = list(base_values)
    def execute(row):
        total = row[0]['value'] * pool[row[0]['index']]
        for term in row[1:]:
            total += term['value'] * pool[term['index']]
        return total
    for row in fresh:
        pool.append(execute(row))
    return [execute(row) for row in final]

def expected_tensor(n, middle, p):
    na, nb = n * middle, middle * p
    # Output order is flattened C^T: c = j*n+i, with A,B row-major.
    expected = [[[0 for b in range(nb)] for a in range(na)] for c in range(p*n)]
    for i in range(n):
        for j in range(p):
            for t in range(middle):
                expected[j*n+i][i*middle+t][t*p+j] = 1
    return expected

def check(scheme, expected_additions=None):
    need(type(scheme) is dict, 'scheme must be an object')
    required = {'n','m','z2','complexity','u_fresh','v_fresh','w_fresh','u','v','w'}
    need(required <= set(scheme), 'missing top-level semantic field(s)')
    # Additional descriptive metadata is inert; never inspect it for execution.
    need(type(scheme['n']) is list and len(scheme['n']) == 3 and
         all(int_only(x) and x > 0 for x in scheme['n']), 'invalid dimensions')
    n, middle, p = scheme['n']
    rank = scheme['m']
    need((n,middle,p) == (2,5,5), 'format must be (2,5,5)')
    need(int_only(rank) and rank == 40, 'rank must be 40')
    need(scheme['z2'] is False, 'integer, not Z2, semantics required')
    declared = scheme['complexity']
    need(type(declared) is dict and set(declared) == {'naive','reduced'} and
         all(int_only(x) and x >= 0 for x in declared.values()), 'complexity schema')
    na, nb, nc = n*middle, middle*p, n*p
    stages = {key: build_stage(key, base, scheme[key+'_fresh'], scheme[key], count)
              for key, base, count in [('u',na,rank),('v',nb,rank),('w',rank,nc)]}
    additions = sum(stage['cost'] for stage in stages.values())
    need(additions == declared['reduced'], 'declared reduced cost is wrong: actual ' + str(additions))
    if expected_additions is not None:
        need(additions == expected_additions, 'expected reduced cost is ' + str(expected_additions))
    u, v, w = (stages[key]['rows'] for key in ('u','v','w'))
    for key, matrix in [('u',u),('v',v),('w',w)]:
        for row_no, row in enumerate(matrix):
            need(all(coefficient in (-1,0,1) for coefficient in row),
                 key + '[' + str(row_no) + ']: expanded coefficients not ternary')
    naive = sum(max(sum(x != 0 for x in row)-1,0) for matrix in (u,v,w) for row in matrix)
    need(naive == declared['naive'], 'declared expanded naive cost is wrong: actual ' + str(naive))
    active = []
    rank_one_terms = []
    for k in range(rank):
        output_column = [w[c][k] for c in range(nc)]
        need(any(u[k]) and any(v[k]) and any(output_column), 'inactive product ' + str(k))
        active.append(k)
        term = tuple(output_column[c] * u[k][a] * v[k][b]
                     for c in range(nc) for a in range(na) for b in range(nb))
        need(any(term), 'zero rank-one product ' + str(k))
        rank_one_terms.append(term)
    duplicate_rank_one = [(i,j) for i in range(rank) for j in range(i+1,rank)
                          if rank_one_terms[i] == rank_one_terms[j]]
    opposite_rank_one = [(i,j) for i in range(rank) for j in range(i+1,rank)
                         if all(x == -y for x,y in zip(rank_one_terms[i],rank_one_terms[j]))]
    expected = expected_tensor(n,middle,p)
    actual = [[[sum(w[c][k] * u[k][a] * v[k][b] for k in range(rank))
                for b in range(nb)] for a in range(na)] for c in range(nc)]
    mismatches = [{'c_transposed_index': c, 'a_row_major_index': a,
                   'b_row_major_index': b, 'actual': actual[c][a][b],
                   'expected': expected[c][a][b]}
                  for c in range(nc) for a in range(na) for b in range(nb)
                  if actual[c][a][b] != expected[c][a][b]]
    need(not mismatches, 'integer tensor mismatch: ' + json.dumps(mismatches[:4]))
    basis_checks = 0
    for a in range(na):
        for b in range(nb):
            av = [int(a == q) for q in range(na)]
            bv = [int(b == q) for q in range(nb)]
            us = scalar_stage(av, scheme['u_fresh'], scheme['u'])
            vs = scalar_stage(bv, scheme['v_fresh'], scheme['v'])
            products = [us[k] * vs[k] for k in range(rank)]
            outputs = scalar_stage(products, scheme['w_fresh'], scheme['w'])
            for c in range(nc):
                need(outputs[c] == expected[c][a][b],
                     'literal scalar SLP mismatch at ' + str((a,b,c)))
                basis_checks += 1
    # Tensor-order digests use deterministic arrays including every zero coefficient.
    digest = lambda obj: hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()
    summary = {'pass': True, 'format': [n,middle,p], 'multiplications': rank,
               'active_products': len(active), 'duplicate_rank_one_terms': duplicate_rank_one,
               'opposite_rank_one_terms': opposite_rank_one,
               'additions': additions, 'naive_expanded_additions': naive,
               'cost_by_stage': {key: {field: stages[key][field] for field in
                                      ('cost','fresh_cost','final_cost','fresh_count','alias_count')}
                                 for key in ('u','v','w')},
               'checked_tensor_coefficients': nc*na*nb,
               'checked_basis_pairs': na*nb, 'checked_scalar_output_values': basis_checks,
               'expected_nonzero_coefficients': n*middle*p,
               'actual_nonzero_coefficients': sum(x != 0 for plane in actual for row in plane for x in row),
               'input_order': {'a': 'A[i,t] -> i*5+t', 'b': 'B[t,j] -> t*5+j'},
               'output_order': 'C[i,j] -> j*2+i',
               'expanded_final_coefficients_ternary': True,
               'tensor_digest': digest(actual), 'expanded_scheme_digest': digest([u,v,w]),
               'sequential_references_and_liveness_checked': True}
    audit = {'summary': summary, 'gate_audits': {key: stages[key]['audit'] for key in ('u','v','w')},
             'expanded_u': u, 'expanded_v': v, 'expanded_w': w,
             'complete_tensor': actual, 'expected_tensor': expected,
             'product_factor_support': [{'product':k,'u':vector_info(u[k]),'v':vector_info(v[k]),
                                         'w_column':vector_info([w[c][k] for c in range(nc)])}
                                        for k in range(rank)]}
    return summary, audit

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scheme')
    parser.add_argument('--expected-additions', type=int)
    parser.add_argument('--audit')
    args = parser.parse_args()
    try:
        summary, audit = check(load(args.scheme), args.expected_additions)
        summary['file_sha256'] = hashlib.sha256(Path(args.scheme).read_bytes()).hexdigest()
        if args.audit:
            Path(args.audit).write_text(json.dumps(audit,indent=2) + '\n')
        print(json.dumps(summary,indent=2))
    except (Invalid,KeyError,TypeError,IndexError,json.JSONDecodeError) as error:
        print(json.dumps({'pass':False,'error':str(error)},indent=2))
        sys.exit(1)

if __name__ == '__main__':
    main()
