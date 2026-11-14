"""Parse MINLPLib pricing050.gms (GAMS scalar format) into a JSON model. Exact decimal strings kept.
Model: max objvar, e1: sum(-c_i x_i) - objvar = 0  =>  objvar = -sum c_i x_i
e2..e6: sum( s*a*x_i*exp(-b*x_i^p) ) =L= rhs ;  bounds lo/up per variable."""
import re, json, sys
src = sys.argv[1]; out = sys.argv[2]
t = open(src).read()
body = t.split('Equations',1)[1]
eqs = {}
for m in re.finditer(r'(e\d+)\.\.(.*?)=(L|E|G)=\s*([-+0-9.eE]+)\s*;', body, flags=re.S):
    eqs[m.group(1)] = (re.sub(r'\s+', ' ', m.group(2)).replace('exp (', 'exp(').replace('sqr (', 'sqr(').replace('power (', 'power(').replace('( ', '(').replace('- ', '-').replace(' ,', ','), m.group(3), m.group(4))
assert len(eqs) == 6, eqs.keys()
lin = eqs['e1'][0]
cost = {}
for m in re.finditer(r'([-+])\s*(?:([0-9.]+)\s*\*\s*)?(x\d+|objvar)', lin):
    s, a, v = m.groups()
    a = a or '1'
    cost[v] = ('-' if s == '-' else '') + a
assert cost.pop('objvar') == '-1'
rows = []
term_re = re.compile(r'([-+])\s*(?:([0-9.]+)\s*\*\s*)?(x\d+)\s*\*\s*exp\(\s*-\s*([0-9.]+)\s*\*\s*(?:(sqr)\((x\d+)\)|power\((x\d+),\s*(\d+)\)|(x\d+))\)')
for k in ['e2','e3','e4','e5','e6']:
    e, sense, rhs = eqs[k]
    terms = []
    pos = 0
    for m in term_re.finditer(e):
        s, a, v, b, sq, v1, v2, pw, v3 = m.groups()
        p = 2 if sq else (int(pw) if pw else 1)
        vv = v1 or v2 or v3
        assert vv == v, (v, vv)
        terms.append({'sign': s, 'a': a or '1', 'var': v, 'b': b, 'p': p})
    stripped = term_re.sub('', e).strip()
    assert stripped == '', (k, stripped[:200])
    rows.append({'name': k, 'sense': sense, 'rhs': rhs, 'terms': terms})
bounds = {}
for m in re.finditer(r'(x\d+)\.lo\s*=\s*([-0-9.eE]+);\s*\1\.up\s*=\s*([-0-9.eE]+);', t):
    bounds[m.group(1)] = (m.group(2), m.group(3))
vars_ = re.findall(r'x\d+', t.split('Variables',1)[1].split(';',1)[0])
json.dump({'vars': vars_, 'cost_in_e1': cost, 'rows': rows, 'bounds': bounds}, open(out, 'w'), indent=1)
print('vars', len(vars_), 'cost nz', len(cost), 'rows', [(r['name'], len(r['terms']), r['sense'], r['rhs']) for r in rows], 'bounds', len(bounds))
print('signs', sorted({tt['sign'] for r in rows for tt in r['terms']}), 'types', sorted({(tt['b'], tt['p']) for r in rows for tt in r['terms']}))
