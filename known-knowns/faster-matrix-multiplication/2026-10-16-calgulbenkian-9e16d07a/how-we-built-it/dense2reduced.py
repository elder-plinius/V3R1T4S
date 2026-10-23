#!/usr/bin/env python3
"""Convert Perminov's dense scheme JSON (u, v, w per product) to the reduced layout without fresh variables,
fixing the output order to C^T (C[i][k] at k*n+i). usage: dense2reduced.py in.json out.json"""
import json, sys
sys.path.insert(0, '[addcomp]/tools')
from check_slp import check
d = json.load(open(sys.argv[1])); n, m, p = d['n']; r = d['m']
F = lambda row: [{"index": i, "value": int(v)} for i, v in enumerate(row) if v]
U = [F(x) for x in d['u']]; V = [F(x) for x in d['v']]
W = [[{"index": q, "value": int(d['w'][q][c])} for q in range(r) if d['w'][q][c]] for c in range(n * p)]
out = {"n": [n, m, p], "m": r, "z2": False, "u_fresh": [], "u": U, "v_fresh": [], "v": V, "w_fresh": [], "w": W}
c = check(out)
if c['tensor_exact'] == 'C=AB':
    W2 = [None] * (n * p)
    for i in range(n):
        for k in range(p): W2[k * n + i] = W[i * p + k]
    out['w'] = W2; c = check(out)
assert c['VALID'] and c['tensor_exact'] == 'C^T', c
out['complexity'] = {"naive": c['naive_total'], "reduced": c['adds_total']}
json.dump(out, open(sys.argv[2], 'w')); print(json.dumps(c))
