#!/usr/bin/env python3
"""Symbolic pass (sympy): execute the straight-line program on symbolic matrices A (n x m), B (m x p),
expand every output polynomial and compare with the entries of A*B (output C[i][k] stored at k*n+i, Perminov's
layout; also tries i*p+k). Independent of check_slp's tensor expansion. usage: sym_check.py scheme.json"""
import json, sys
import sympy as sp
d = json.load(open(sys.argv[1])); n, m, p = d['n']; r = d['m']
A = [sp.Symbol('a%d_%d' % (i, j)) for i in range(n) for j in range(m)]
B = [sp.Symbol('b%d_%d' % (j, k)) for j in range(m) for k in range(p)]
def run(fresh, rows, ins):
    vals = list(ins)
    for f in fresh: vals.append(sp.Add(*[t['value'] * vals[t['index']] for t in f]))
    return [sp.Add(*[t['value'] * vals[t['index']] for t in f]) for f in rows]
for key in ('u_fresh', 'v_fresh', 'w_fresh', 'u', 'v', 'w'):
    for f in d.get(key, []):
        for t in f: assert t['value'] in (1, -1), 'non-ternary coefficient'
pu = run(d.get('u_fresh', []), d['u'], A); pv = run(d.get('v_fresh', []), d['v'], B)
prods = [sp.expand(x * y) for x, y in zip(pu, pv)]
C = [sp.expand(c) for c in run(d.get('w_fresh', []), d['w'], prods)]
res = {}
for name, idx in (('C^T', lambda i, k: k * n + i), ('C=AB', lambda i, k: i * p + k)):
    ok = all(sp.expand(C[idx(i, k)] - sum(A[i * m + j] * B[j * p + k] for j in range(m))) == 0 for i in range(n) for k in range(p))
    res[name] = ok
adds = sum(len(f) - 1 for key in ('u_fresh', 'v_fresh', 'w_fresh', 'u', 'v', 'w') for f in d.get(key, []))
print(json.dumps(dict(file=sys.argv[1].split('/')[-1], format='%dx%dx%d' % (n, m, p), rank=r, products=len(prods), symbolic=res, reduced_additions=adds)))
