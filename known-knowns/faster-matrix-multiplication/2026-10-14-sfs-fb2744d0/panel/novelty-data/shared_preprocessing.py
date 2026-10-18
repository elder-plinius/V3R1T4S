"""Independent, deterministic signed-pair CSE for public ternary factors.

This is a constructive upper bound, never a lower-bound/optimality claim.
"""
from collections import Counter
from itertools import combinations
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent

def canonical(row):
    if not row:
        return (), 1
    sign = row[min(row)]
    assert sign in (-1, 1)
    return tuple(sorted((i, s * sign) for i, s in row.items())), sign

def circuit(rows, inputs):
    work = {}
    for row in rows:
        key, _ = canonical(row)
        work[key] = dict(key)
    fresh = []
    while True:
        pairs = Counter()
        for row in work.values():
            for a, b in combinations(sorted(row), 2):
                pairs[(a, b, row[a] * row[b])] += 1
        if not pairs:
            break
        pair, frequency = min(pairs.items(), key=lambda item: (-item[1], item[0]))
        if frequency <= 1:
            break
        a, b, relation = pair
        new_id = inputs + len(fresh)
        fresh.append([{'index': a, 'value': 1}, {'index': b, 'value': relation}])
        replacement = {}
        for row in work.values():
            row = dict(row)
            if a in row and b in row and row[a] * row[b] == relation:
                coefficient = row[a]
                del row[a]
                del row[b]
                row[new_id] = coefficient
            key, _ = canonical(row)
            replacement[key] = dict(key)
        work = replacement
    # The work rows are canonicalized. Re-evaluate each desired output in terms
    # of new variables by applying every substitution in chronological order.
    pair_operations = list(fresh)
    outputs = []
    completed = {}
    for original in rows:
        row = dict(original)
        for k, operation in enumerate(pair_operations):
            a, b = operation[0]['index'], operation[1]['index']
            relation = operation[1]['value']
            if a in row and b in row and row[a] * row[b] == relation:
                coefficient = row[a]
                del row[a]
                del row[b]
                row[inputs + k] = coefficient
        key, sign = canonical(row)
        if key in completed:
            outputs.append([{'index': completed[key], 'value': sign}])
        elif len(row) > 1:
            completed[key] = inputs + len(fresh)
            fresh.append([{'index': i, 'value': s} for i, s in key])
            outputs.append([{'index': completed[key], 'value': sign}])
        else:
            outputs.append([{'index': i, 'value': s} for i, s in sorted(row.items())])
    return fresh, outputs

def parse_linear(expression, side, rank=40):
    row = {}
    pattern = r'([+-]?)' + (r'A_(\d+)_(\d+)' if side == 'u' else r'B_(\d+)_(\d+)' if side == 'v' else r'm_(\d+)')
    terms = re.findall(pattern, expression)
    for term in terms:
        sign = -1 if term[0] == '-' else 1
        i = ((int(term[1])-1)*5 + int(term[2])-1) if side != 'w' else int(term[1])-1
        assert i not in row
        row[i] = sign
    assert terms
    return row

def lille_scheme():
    raw = (ROOT / 'Lille-2x5x5-raw.mpl').read_text()
    products = re.findall(r'm_(\d+)=\(([^()]*)\)\*\(([^()]*)\)',raw)
    outputs = re.findall(r'C_(\d+)_(\d+)=([^,\n]+)',raw)
    assert len(products)==40 and len(outputs)==10
    out = {'n':[2,5,5], 'm':40, 'z2':False}
    out['u'] = [parse_linear(a,'u') for _,a,_ in products]
    out['v'] = [parse_linear(b,'v') for _,_,b in products]
    keyed = {(int(i)-1,int(j)-1):parse_linear(e,'w') for i,j,e in outputs}
    out['w'] = [keyed[i,j] for j in range(5) for i in range(2)]
    return out

def from_dense(scheme):
    a,b,c=scheme['n']
    result={'n':scheme['n'],'m':scheme['m'],'z2':False}
    result['u']=[{i:s for i,s in enumerate(row) if s} for row in scheme['u']]
    result['v']=[{i:s for i,s in enumerate(row) if s} for row in scheme['v']]
    result['w']=[{k:scheme['w'][k][j] for k in range(scheme['m']) if scheme['w'][k][j]} for j in range(a*c)]
    # Catalog's third tensor factor represents the transposed output, as in
    # the supplied Perminov-format SLP. Independent coefficient checks below
    # confirm this indexing for every circuit used in the comparison.
    return result

def reduce(scheme):
    a,b,c=scheme['n'];inputs={'u':a*b,'v':b*c,'w':scheme['m']}
    result={key:scheme[key] for key in ['n','m','z2']}
    counts={}
    for side in 'uvw':
        assert all(s in (-1,1) for row in scheme[side] for s in row.values())
        fresh, outputs = circuit(scheme[side], inputs[side])
        result[side+'_fresh']=fresh;result[side]=outputs
        counts[side]=sum(max(len(row)-1,0) for row in fresh+outputs)
    result['complexity']={'reduced':sum(counts.values())}
    return result,counts

if __name__=='__main__':
    results=[]
    sources=[('Lille-2x5x5-raw.mpl',lille_scheme())]
    for file in ROOT.glob('catalog-*.json'):
        if file.name.endswith('.fetch.json'):continue
        s=json.loads(file.read_text())
        if s.get('n') != [2,5,5] or s.get('m') != 40 or not s.get('u') or isinstance(s['u'][0][0],dict):continue
        if 'Z' not in s.get('fields',[]):continue
        dense=from_dense(s)
        if any(value not in (-1,1) for side in 'uvw' for row in dense[side] for value in row.values()):
            continue
        sources.append((file.name,dense))
    for name,scheme in sources:
        reduced,counts=reduce(scheme)
        filename='shared-'+name.replace('.mpl','.json')
        (ROOT/filename).write_text(json.dumps(reduced,indent=2)+'\n')
        results.append({'source':name,'output':filename,'counts':counts,'total':sum(counts.values())})
    (ROOT/'shared-preprocessing-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
