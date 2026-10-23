#!/usr/bin/env python3
"""Parse primary Lille tensor with literal integer arrays; no Maple execution."""
import ast
import json
import re
from pathlib import Path

DEST = Path(__file__).resolve().parent
raw = (DEST / 'lille-2x5x5-tensor.mpl').read_text()
tensor = raw[raw.index('Tensor:=TriadSet('):raw.index('map(expand,A.B-')]
matches = re.findall(r'Matrix\((\d+),\s*(\d+),\s*(\[\[.*?\]\])\)', tensor)
assert len(matches) == 120
matrices = []
for height, width, literal in matches:
    rows = ast.literal_eval(literal)
    assert len(rows) == int(height) and all(len(row) == int(width) for row in rows)
    assert all(type(x) is int for row in rows for x in row)
    matrices.append(rows)
u, v, wt = [], [], []
for i in range(0,120,3):
    assert [len(matrices[i]),len(matrices[i+1]),len(matrices[i+2])] == [2,5,5]
    u.append([x for row in matrices[i] for x in row])
    v.append([x for row in matrices[i+1] for x in row])
    wt.append([x for row in matrices[i+2] for x in row])
w = [[wt[t][out] for t in range(40)] for out in range(10)]
for ai in range(10):
    for bi in range(25):
        for out in range(10):
            i,j = out%2,out//2
            expected = int(ai//5 == i and bi%5 == j and ai%5 == bi//5)
            assert sum(u[t][ai]*v[t][bi]*w[out][t] for t in range(40)) == expected
result = {'exact_over_Z':True,'products':40,
    'coefficient_sets':{side:sorted({x for row in matrix for x in row}) for side,matrix in [('u',u),('v',v),('w',w)]},
    'unshared_addition_counts':{side:sum(max(0,sum(x!=0 for x in row)-1) for row in matrix) for side,matrix in [('u',u),('v',v),('w',w)]},
    'page_complexity_variant_present':False,
    'interpretation':'The linked tensor is ternary and exact; its unshared count is not a published reduced SLP minimum.'}
result['unshared_additions'] = sum(result['unshared_addition_counts'].values())
(DEST / 'lille-check-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
