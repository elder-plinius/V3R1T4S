#!/usr/bin/env python3
"""Independent exact expansion and accounting of one submitted reduced SLP."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / 'claim' / 'scheme.json'
DEST = Path(__file__).resolve().parent
s = json.loads(SOURCE.read_text())
assert s['n'] == [2, 5, 5] and s['m'] == 40
assert s['z2'] is False

def expand_stage(name, width, outcount):
    assert len(s[name]) == outcount
    values = [[int(i == j) for j in range(width)] for i in range(width)]
    dependencies = []
    costs = []
    allrows = s.get(name + '_fresh', []) + s[name]
    nfresh = len(s.get(name + '_fresh', []))
    for pos, row in enumerate(allrows):
        assert isinstance(row, list)
        seen = set()
        output = [0] * width
        indices = []
        for term in row:
            assert set(term) == {'index', 'value'}
            i, sign = term['index'], term['value']
            assert type(i) is int and 0 <= i < len(values)
            assert i not in seen
            assert type(sign) is int and sign in (-1, 1)
            seen.add(i)
            indices.append(i)
            output = [a + sign*b for a, b in zip(output, values[i])]
        dependencies.append(indices)
        costs.append(max(0, len(row)-1))
        if pos < nfresh:
            values.append(output)
        else:
            # Final forms are outputs, not variables available to later forms.
            pass
    outputs = []
    for row in s[name]:
        outputs.append([sum(t['value'] * values[t['index']][j] for t in row) for j in range(width)])
    needed = {i for row in s[name] for i in (t['index'] for t in row)}
    for pos in reversed(range(nfresh)):
        if width+pos in needed:
            needed.update(dependencies[pos])
    unused_fresh = [pos for pos in range(nfresh) if width+pos not in needed]
    return outputs, {
        'base_inputs': width, 'fresh_forms': nfresh, 'output_forms': outcount,
        'fresh_additions': sum(costs[:nfresh]), 'output_additions': sum(costs[nfresh:]),
        'additions': sum(costs), 'unused_fresh': unused_fresh,
        'expanded_coefficient_set': sorted({c for row in outputs for c in row}),
        'reachable_base_indices': sorted(i for i in needed if i < width),
    }

u, uc = expand_stage('u', 10, 40)
v, vc = expand_stage('v', 25, 40)
w, wc = expand_stage('w', 40, 10)
bad = []
for ai in range(10):
    for bi in range(25):
        for out in range(10):
            i, j = out % 2, out // 2
            expected = int(ai // 5 == i and bi % 5 == j and ai % 5 == bi // 5)
            actual = sum(u[t][ai] * v[t][bi] * w[out][t] for t in range(40))
            if actual != expected:
                bad.append([ai, bi, out, actual, expected])
assert not bad, bad[:5]
nonzero_products = [t for t in range(40) if any(u[t]) and any(v[t])]
active_products = [t for t in range(40) if any(u[t]) and any(v[t]) and any(row[t] for row in w)]
pair_vectors = [[a*b for a in u[t] for b in v[t]] for t in range(40)]
duplicate_or_opposite_pairs = [[a,b] for a in range(40) for b in range(a+1,40)
    if pair_vectors[a] == pair_vectors[b] or pair_vectors[a] == [-x for x in pair_vectors[b]]]
result = {
    'input_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'format': s['n'], 'declared_products': s['m'],
    'verified_integer_coefficients': 2500, 'expected_nonzero_tensor_coefficients': 50,
    'exact_over_Z': True, 'ternary_SLP_terms_only': True,
    'stage_counts': {'u': uc, 'v': vc, 'w': wc},
    'total_additions': sum(c['additions'] for c in [uc,vc,wc]),
    'expanded_naive_additions': sum(max(0,sum(x != 0 for x in row)-1) for matrix in [u,v,w] for row in matrix),
    'nonzero_products': len(nonzero_products), 'active_products': len(active_products),
    'duplicate_or_opposite_product_pairs': duplicate_or_opposite_pairs,
    'statistical_null_required': False,
}
filename = 'check-result.json' if len(sys.argv) == 1 else 'baseline-check-result.json'
(DEST / filename).write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
