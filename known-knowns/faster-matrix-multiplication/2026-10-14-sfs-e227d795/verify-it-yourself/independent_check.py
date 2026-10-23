#!/usr/bin/env python3
"""Independent exact tensor, literal cost, execution, and reachability checker."""
import argparse
import hashlib
import json
from pathlib import Path


class Rejected(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


def integer(value):
    return type(value) is int


def read_form(form, available, where):
    require(type(form) is list and len(form) > 0, f'{where}: empty/non-list expression')
    result = []
    for term in form:
        require(type(term) is dict and set(term) == {'index', 'value'},
                f'{where}: unsupported term/hidden operation')
        index, sign = term['index'], term['value']
        require(integer(index) and 0 <= index < available,
                f'{where}: unavailable/forward index {index}')
        require(integer(sign) and sign in (-1, 1),
                f'{where}: nonunit scalar {sign}')
        result.append((index, sign))
    return result


def linear_stage(base, fresh, terminals, name):
    require(type(fresh) is list and type(terminals) is list, f'{name}: non-list stage')
    variables = [[int(i == j) for j in range(base)] for i in range(base)]
    decoded_fresh, decoded_roots = [], []
    costs = {'fresh': 0, 'terminal': 0}
    binary_gates = {}
    variable_nodes = [('variable', i) for i in range(base)]
    graph = {node: [] for node in variable_nodes}
    root_nodes = []
    binary_partial_max = 0

    def expand(form):
        out = [0] * base
        for index, sign in form:
            for j, value in enumerate(variables[index]):
                out[j] += sign * value
        return out

    def lower(form):
        nonlocal binary_partial_max
        prior = ('variable', form[0][0])
        partial = [form[0][1] * x for x in variables[form[0][0]]]
        for index, sign in form[1:]:
            node = ('gate', len(binary_gates))
            binary_gates[node] = [prior, ('variable', index)]
            graph[node] = binary_gates[node]
            prior = node
            partial = [x + sign * y for x, y in zip(partial, variables[index])]
            binary_partial_max = max(binary_partial_max, max(map(abs, partial)))
        return prior

    for number, raw in enumerate(fresh):
        form = read_form(raw, len(variables), f'{name}_fresh[{number}]')
        decoded_fresh.append(form)
        node = ('variable', len(variables))
        graph[node] = [lower(form)]
        variable_nodes.append(node)
        variables.append(expand(form))
        costs['fresh'] += len(form) - 1
    expanded_roots = []
    for number, raw in enumerate(terminals):
        form = read_form(raw, len(variables), f'{name}[{number}]')
        decoded_roots.append(form)
        node = ('root', number)
        graph[node] = [lower(form)]
        root_nodes.append(node)
        expanded_roots.append(expand(form))
        costs['terminal'] += len(form) - 1
    return {'base': base, 'variables': variables, 'fresh': decoded_fresh,
            'roots': decoded_roots, 'expanded': expanded_roots, 'costs': costs,
            'binary_gates': binary_gates, 'graph': graph, 'root_nodes': root_nodes,
            'binary_partial_max_absolute_coefficient': binary_partial_max}


def reachable(stage, selected_roots=None):
    roots = stage['roots'] if selected_roots is None else [stage['roots'][i] for i in selected_roots]
    pending = [index for root in roots for index, _ in root]
    reached = set()
    while pending:
        index = pending.pop()
        if index in reached:
            continue
        reached.add(index)
        if index >= stage['base']:
            pending.extend(i for i, _ in stage['fresh'][index - stage['base']])
    return reached


def canonical_sign(vector):
    first = next((x for x in vector if x), 0)
    return tuple(-x for x in vector) if first < 0 else tuple(vector)


def reached_binary_gates(stage, selected_roots=None):
    pending = stage['root_nodes'][:] if selected_roots is None else \
        [stage['root_nodes'][i] for i in selected_roots]
    seen = set()
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        pending.extend(stage['graph'][node])
    return len([node for node in seen if node[0] == 'gate'])


def evaluate_stage(stage, inputs):
    values = list(inputs)
    for form in stage['fresh']:
        values.append(sum(sign * values[index] for index, sign in form))
    return [sum(sign * values[index] for index, sign in form) for form in stage['roots']]


def analyze(scheme, basis=True, require_metadata=True):
    require(type(scheme) is dict, 'object must be dictionary')
    required = {'n', 'm', 'z2', 'complexity', 'u_fresh', 'u', 'v_fresh', 'v', 'w_fresh', 'w'}
    require(required <= set(scheme) <= required | {'research_method'},
            'missing keys or unsupported top-level operation')
    dims = scheme['n']
    require(type(dims) is list and len(dims) == 3 and
            all(integer(x) and 0 < x <= 8 for x in dims), 'invalid dimensions')
    n, inner, p = dims
    require(dims == [3, 4, 5], 'unexpected candidate format')
    rank = scheme['m']
    require(integer(rank) and rank == 47, 'unexpected rank')
    require(scheme['z2'] is False, 'candidate must operate over Z')
    require(len(scheme['u']) == rank and len(scheme['v']) == rank and
            len(scheme['w']) == n * p, 'terminal dimensions do not match')
    stages = {
        'U': linear_stage(n * inner, scheme['u_fresh'], scheme['u'], 'u'),
        'V': linear_stage(inner * p, scheme['v_fresh'], scheme['v'], 'v'),
        'W': linear_stage(rank, scheme['w_fresh'], scheme['w'], 'w')}
    u, v, w = (stages[x]['expanded'] for x in 'UVW')
    cost = {name: sum(stage['costs'].values()) for name, stage in stages.items()}
    total = sum(cost.values())
    naive = sum(max(0, sum(x != 0 for x in row) - 1)
                for matrix in (u, v, w) for row in matrix)
    if require_metadata:
        metadata = scheme['complexity']
        require(type(metadata) is dict and set(metadata) == {'naive', 'reduced'} and
                all(integer(x) for x in metadata.values()), 'invalid complexity metadata')
        require(metadata['reduced'] == total, f'metadata reduced {metadata["reduced"]} != literal {total}')
        require(metadata['naive'] == naive, f'metadata naive {metadata["naive"]} != expanded {naive}')
    violations = [{'stage': name, 'row': i, 'column': j, 'value': x}
                  for name, stage in stages.items() for i, row in enumerate(stage['expanded'])
                  for j, x in enumerate(row) if x not in (-1, 0, 1)]
    terminal_ternary = not violations

    reached_w = reachable(stages['W'])
    reached_products = sorted(reached_w & set(range(rank)))
    reach = {'W': reached_w}
    reach['U'] = reachable(stages['U'], reached_products)
    reach['V'] = reachable(stages['V'], reached_products)
    missing = {name: sorted(set(range(len(stage['variables']))) - reach[name])
               for name, stage in stages.items()}
    binary_reach = {name: reached_binary_gates(stage, None if name == 'W' else reached_products)
                    for name, stage in stages.items()}
    binary_counts = {name: len(stage['binary_gates']) for name, stage in stages.items()}
    require(binary_counts == cost, 'lowered binary DAG count disagrees with expression-length cost')
    active = [r for r in range(rank) if any(u[r]) and any(v[r]) and any(row[r] for row in w)]
    distinct = {(canonical_sign(u[r]), canonical_sign(v[r])) for r in active}

    mismatches = []
    nonzeros = 0
    even_errors = True
    for c in range(n * p):
        ci, ck = c % n, c // n
        for a in range(n * inner):
            ai, aj = divmod(a, inner)
            for b in range(inner * p):
                bj, bk = divmod(b, p)
                got = sum(w[c][r] * u[r][a] * v[r][b] for r in range(rank))
                expected = int(ai == ci and aj == bj and bk == ck)
                nonzeros += got != 0
                if got != expected:
                    mismatches.append({'c': c, 'a': a, 'b': b, 'got': got, 'expected': expected})
                    even_errors = even_errors and (got - expected) % 2 == 0
    basis_errors = []
    if basis:
        for a in range(n * inner):
            ua = evaluate_stage(stages['U'], [int(i == a) for i in range(n * inner)])
            for b in range(inner * p):
                vb = evaluate_stage(stages['V'], [int(i == b) for i in range(inner * p)])
                outputs = evaluate_stage(stages['W'], [x * y for x, y in zip(ua, vb)])
                expected = [int(c % n == a // inner and a % inner == b // p and c // n == b % p)
                            for c in range(n * p)]
                if outputs != expected:
                    basis_errors.append({'a': a, 'b': b, 'got': outputs, 'expected': expected})
    ok = terminal_ternary and not mismatches and not basis_errors and not any(missing.values()) and \
        len(active) == rank and len(distinct) == rank and binary_reach == binary_counts
    return {
        'pass': ok, 'format': dims, 'rank': rank, 'literal_additions': total,
        'stage_additions': cost, 'stage_cost_parts': {k: s['costs'] for k, s in stages.items()},
        'expanded_naive_additions': naive,
        'coefficient_count': n * p * n * inner * inner * p,
        'coefficient_mismatch_count': len(mismatches), 'coefficient_mismatch_first': mismatches[:5],
        'tensor_nonzero_count': nonzeros, 'tensor_matches_mod_2': not mismatches or even_errors,
        'basis_pair_count': n * inner * inner * p if basis else 0,
        'basis_mismatch_count': len(basis_errors), 'basis_mismatch_first': basis_errors[:2],
        'terminal_ternary': terminal_ternary, 'terminal_ternary_violations_first': violations[:5],
        'active_products': len(active), 'distinct_products_up_to_sign': len(distinct),
        'reached_variable_counts': {k: len(v) for k, v in reach.items()},
        'declared_variable_counts': {k: len(s['variables']) for k, s in stages.items()},
        'unreached_variable_indices': missing,
        'declared_binary_gate_counts': binary_counts, 'reachable_binary_gate_counts': binary_reach,
        'intermediate_max_absolute_coefficients': {
            k: max((abs(x) for row in s['variables'][s['base']:] for x in row), default=0)
            for k, s in stages.items()},
        'binary_partial_max_absolute_coefficients': {
            k: s['binary_partial_max_absolute_coefficient'] for k, s in stages.items()},
        'aliases_by_stage': {k: sum(len(row) == 1 for row in s['fresh']) for k, s in stages.items()},
        'terminal_shapes': {k: [len(s['expanded']), s['base']] for k, s in stages.items()}}


def checked_path(path):
    raw = Path(path).read_bytes()
    try:
        result = analyze(json.loads(raw))
    except (Rejected, ValueError, TypeError, KeyError) as error:
        result = {'pass': False, 'rejected': str(error)}
    result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    result = checked_path(args.path)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['pass'] else 1)
