#!/usr/bin/env python3
"""Exact checker and reduced-addition counter for ternary matrix-multiplication SLPs
in Perminov's reduced-scheme JSON layout (written from the definition; standard library only).

Layout: "n": [n, m, p], "m": rank r.
  u_fresh: list of forms; fresh k gets index n*m + k; each form is [{"index": i, "value": c}, ...]
           over A-entries (0..n*m-1, A[i][j] -> i*m+j) and earlier fresh variables.
  u:       r forms (left factor of product q) over A-entries and u-fresh variables.
  v_fresh, v: same over B-entries (B[j][k] -> j*p+k), B is m x p.
  w_fresh: forms over products (0..r-1) and earlier w-fresh (index r + k).
  w:       n*p forms over products and w-fresh: the outputs.
Checks:
  1. coefficients are in {-1, +1} (ternary SLP: no other scalars), every index refers to an input or an
     EARLIER fresh variable (straight-line order), no empty form.
  2. symbolic: expands each map exactly over Z and verifies sum_q U[q]V[q]W[.,q] equals the matrix
     multiplication tensor exactly, for output order C[i][k] at i*p+k (C = A B) or at k*n+i (C^T); reports which.
  3. evaluation: runs the straight-line program itself on random integer matrices and compares with A*B.
Count (Perminov 'reduced'): every form of length L costs L-1 additions/subtractions (negation is free).
"""
import json, sys, random

def expand(fresh, rows, nin, name):
    vecs = []
    def vec_of(form, limit):
        if not form:
            raise ValueError('%s: empty form' % name)
        out = {}
        for t in form:
            i, c = t['index'], t['value']
            if c not in (1, -1):
                raise ValueError('%s: coefficient %r not +-1' % (name, c))
            if not (0 <= i < limit):
                raise ValueError('%s: index %d out of order/range (limit %d)' % (name, i, limit))
            src = {i: 1} if i < nin else vecs[i - nin]
            for k, v in src.items():
                out[k] = out.get(k, 0) + c * v
        return {k: v for k, v in out.items() if v}
    for f in fresh:
        vecs.append(vec_of(f, nin + len(vecs)))
    full = [vec_of(f, nin + len(vecs)) for f in rows]
    return vecs, full

def cost(fresh, rows):
    return sum(len(f) - 1 for f in fresh) + sum(len(f) - 1 for f in rows)

def run_slp(fresh, rows, inputs):
    vals = list(inputs)
    for f in fresh:
        vals.append(sum(t['value'] * vals[t['index']] for t in f))
    return [sum(t['value'] * vals[t['index']] for t in f) for f in rows]

def check(d, trials=20, seed=1):
    n, m, p = d['n']; r = d['m']
    res = {'format': '%dx%dx%d' % (n, m, p), 'rank': r}
    _, U = expand(d.get('u_fresh', []), d['u'], n * m, 'u')
    _, V = expand(d.get('v_fresh', []), d['v'], m * p, 'v')
    _, W = expand(d.get('w_fresh', []), d['w'], r, 'w')
    assert len(U) == r and len(V) == r and len(W) == n * p, 'row counts'
    # tensor T[(a,b,c)] = sum_q U[q][a] V[q][b] W[c][q]
    Wq = [dict() for _ in range(r)]
    for c, row in enumerate(W):
        for q, v in row.items():
            Wq[q][c] = v
    T = {}
    for q in range(r):
        for a, ua in U[q].items():
            for b, vb in V[q].items():
                uv = ua * vb
                for c, wc in Wq[q].items():
                    key = (a, b, c)
                    T[key] = T.get(key, 0) + uv * wc
    T = {k: v for k, v in T.items() if v}
    ok = None
    for name, cidx in (('C=AB', lambda i, k: i * p + k), ('C^T', lambda i, k: k * n + i)):
        ref = {}
        for i in range(n):
            for j in range(m):
                for k in range(p):
                    ref[(i * m + j, j * p + k, cidx(i, k))] = 1
        if ref == T:
            ok = name
    res['tensor_exact'] = ok
    # straight-line evaluation on random integer matrices
    rng = random.Random(seed)
    ev_ok = ok is not None
    for _ in range(trials):
        A = [rng.randint(-1000, 1000) for _ in range(n * m)]
        Bm = [rng.randint(-1000, 1000) for _ in range(m * p)]
        pu = run_slp(d.get('u_fresh', []), d['u'], A)
        pv = run_slp(d.get('v_fresh', []), d['v'], Bm)
        prods = [x * y for x, y in zip(pu, pv)]
        Cv = run_slp(d.get('w_fresh', []), d['w'], prods)
        for i in range(n):
            for k in range(p):
                want = sum(A[i * m + j] * Bm[j * p + k] for j in range(m))
                got = Cv[i * p + k] if ok == 'C=AB' else Cv[k * n + i]
                if got != want:
                    ev_ok = False
    res['eval_ok'] = ev_ok
    cu = cost(d.get('u_fresh', []), d['u']); cv = cost(d.get('v_fresh', []), d['v']); cw = cost(d.get('w_fresh', []), d['w'])
    res.update(adds_U=cu, adds_V=cv, adds_W=cw, adds_total=cu + cv + cw)
    res['naive_total'] = sum(len(x) - 1 for x in U) + sum(len(x) - 1 for x in V) + sum(len(x) - 1 for x in W)
    res['declared_reduced'] = d.get('complexity', {}).get('reduced')
    res['VALID'] = bool(ok and ev_ok)
    return res

if __name__ == '__main__':
    for path in sys.argv[1:]:
        d = json.load(open(path))
        try:
            print(json.dumps(dict(file=path.split('/')[-1], **check(d))))
        except Exception as e:
            print(json.dumps(dict(file=path.split('/')[-1], VALID=False, error=str(e))))
