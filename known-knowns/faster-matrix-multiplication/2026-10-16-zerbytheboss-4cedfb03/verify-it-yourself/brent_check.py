#!/usr/bin/env python3
"""Direct Brent-equation check over Z for a Perminov-layout ternary scheme (standard library only).
Expands u/v/w forms (with fresh variables) to integer matrices, then tests all (n1*n2)*(n2*n3)*(n3*n1) Brent
equations sum_r U[r][a] V[r][b] W[r][c] == [a=(i,j), b=(j,k), c=(k,i)] ; also checks entries in {-1,0,1}, rank, and the
reduced addition count. Exit 0 and last line 'BRENT_OK ...' on success."""
import json, sys
def expand(n_in, fresh, out):
    vs = [[1 if j == i else 0 for j in range(n_in)] for i in range(n_in)]
    for e in fresh:
        assert len(e) == 2 and e[0]['index'] != e[1]['index'] and all(t['value'] in (-1, 1) for t in e)
        v = [0] * n_in
        for t in e:
            assert 0 <= t['index'] < len(vs)
            for k in range(n_in): v[k] += t['value'] * vs[t['index']][k]
        vs.append(v)
    mat = []
    for e in out:
        seen = set(); v = [0] * n_in
        for t in e:
            assert t['value'] in (-1, 1) and t['index'] not in seen and 0 <= t['index'] < len(vs)
            seen.add(t['index'])
            for k in range(n_in): v[k] += t['value'] * vs[t['index']][k]
        mat.append(v)
    return mat
def count(f, o): return len(f) + sum(max(0, len(e) - 1) for e in o)
d = json.load(open(sys.argv[1])); n1, n2, n3 = d['n']; m = d['m']
U = expand(n1 * n2, d['u_fresh'], d['u']); V = expand(n2 * n3, d['v_fresh'], d['v'])
WT = expand(m, d['w_fresh'], d['w'])
assert len(U) == m and len(V) == m and len(WT) == n1 * n3
W = [[WT[c][r] for c in range(n1 * n3)] for r in range(m)]
tern = all(x in (-1, 0, 1) for M in (U, V, W) for row in M for x in row)
bad = 0
for a in range(n1 * n2):
    i1, j1 = divmod(a, n2)
    for b in range(n2 * n3):
        j2, k1 = divmod(b, n3)
        for c in range(n3 * n1):
            k2, i2 = divmod(c, n1)
            t = 1 if (i1 == i2 and j1 == j2 and k1 == k2) else 0
            if sum(U[r][a] * V[r][b] * W[r][c] for r in range(m)) != t: bad += 1
cr = count(d['u_fresh'], d['u']) + count(d['v_fresh'], d['v']) + count(d['w_fresh'], d['w'])
print('format %dx%dx%d rank %d equations %d brent_bad %d ternary %s cr %d' % (n1, n2, n3, m, n1*n2*n2*n3*n3*n1, bad, tern, cr))
ok = bad == 0 and tern and cr == int(sys.argv[2]) and m == int(sys.argv[3])
print('BRENT_OK' if ok else 'BRENT_FAIL', 'brent_bad=%d' % bad)
sys.exit(0 if ok else 1)
