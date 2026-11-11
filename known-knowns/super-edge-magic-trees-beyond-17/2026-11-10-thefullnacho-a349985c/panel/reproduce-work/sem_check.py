#!/usr/bin/env python3
"""Independent checker (REPRODUCE skeptic), written from CLAIM.md before reading checkers/.

Definition checked (CLAIM.md): "for each n in 18..25, the file ... gives every unlabeled tree on n vertices
(A000055(n) of them ...) with a bijection from its vertices to {1..n} whose n-1 edge sums are consecutive integers".
Line format: "n;u-v,u-v,...;l0,l1,...,l(n-1)[;extra fields]", vertices 0..n-1, li = label of vertex i.

Per line: field0 == n; exactly n-1 edges, endpoints in 0..n-1, no loops, no repeated edge, connected (so a tree);
exactly n labels forming a permutation of 1..n; the n-1 sums l(u)+l(v) are pairwise distinct and max-min == n-2.
Distinctness: canonical form = AHU parenthesis code rooted at the center (bicentral: the two halves' codes, sorted),
packed into an int. Keys are spilled into NB bucket files by a hash of the key; each bucket is then deduplicated
on its own (bounded memory). Count must equal A000055(n) computed here (rooted-tree recurrence + Otter).

usage: sem_check.py N FILE WORKDIR [NB]
"""
import sys, os, lzma, hashlib
from array import array


def a000081(m):
    a = [0, 1]
    for k in range(1, m):
        s = 0
        for j in range(1, k + 1):
            dsum = sum(d * a[d] for d in range(1, j + 1) if j % d == 0)
            s += dsum * a[k - j + 1]
        assert s % k == 0
        a.append(s // k)
    return a  # a[n] = rooted trees on n nodes


def a000055(n):
    a = a000081(n + 1)
    s = sum(a[k] * a[n - k] for k in range(0, n + 1))
    if n % 2 == 0:
        s -= a[n // 2]
    assert s % 2 == 0
    return a[n] - s // 2


def canon(n, adj):
    # center by leaf peeling
    deg = [len(x) for x in adj]
    layer = [v for v in range(n) if deg[v] <= 1]
    removed = len(layer)
    while removed < n:
        nxt = []
        for v in layer:
            for w in adj[v]:
                deg[w] -= 1
                if deg[w] == 1:
                    nxt.append(w)
        removed += len(nxt)
        layer = nxt
    if len(layer) == 1:
        return int('1' + rooted(layer[0], -1, adj), 2)
    c1, c2 = layer
    x = rooted(c1, c2, adj)
    y = rooted(c2, c1, adj)
    if y < x:
        x, y = y, x
    return int('11' + x + y, 2)  # bit length 2n+2 (unicentral keys have 2n+1), so the two cases never collide


def rooted(r, block, adj):
    # iterative AHU: code(v) = '1' + sorted(children codes) + '0'
    order = [r]
    par = {r: block}
    i = 0
    while i < len(order):
        v = order[i]; i += 1
        p = par[v]
        for w in adj[v]:
            if w != p:
                par[w] = v
                order.append(w)
    code = {}
    kids = {v: [] for v in order}
    for v in reversed(order):
        ch = kids[v]
        ch.sort()
        c = '1' + ''.join(ch) + '0'
        if v != r:
            kids[par[v]].append(c)
        else:
            return c


def check_line(n, line):
    f = line.rstrip('\n').split(';')
    if len(f) < 3:
        return 'too few fields', None
    if f[0] != str(n):
        return 'bad n field', None
    es = f[1].split(',')
    if len(es) != n - 1:
        return 'edge count %d' % len(es), None
    labs = f[2].split(',')
    if len(labs) != n:
        return 'label count', None
    try:
        lab = [int(t) for t in labs]
    except ValueError:
        return 'bad label', None
    if sorted(lab) != list(range(1, n + 1)):
        return 'labels not a bijection onto 1..n', None
    adj = [[] for _ in range(n)]
    seen = set()
    sums = []
    for e in es:
        p = e.split('-')
        if len(p) != 2:
            return 'bad edge', None
        try:
            u = int(p[0]); v = int(p[1])
        except ValueError:
            return 'bad edge', None
        if not (0 <= u < n and 0 <= v < n) or u == v:
            return 'edge out of range/loop', None
        k = (u, v) if u < v else (v, u)
        if k in seen:
            return 'repeated edge', None
        seen.add(k)
        adj[u].append(v); adj[v].append(u)
        sums.append(lab[u] + lab[v])
    # connectivity
    st = [0]; vis = [False] * n; vis[0] = True; cnt = 1
    while st:
        v = st.pop()
        for w in adj[v]:
            if not vis[w]:
                vis[w] = True; cnt += 1; st.append(w)
    if cnt != n:
        return 'not connected', None
    if len(set(sums)) != n - 1 or max(sums) - min(sums) != n - 2:
        return 'edge sums not consecutive', None
    return None, canon(n, adj)


def bucket_of(key, nb):
    return ((key * 0x9E3779B97F4A7C15) >> 32) % nb


def main():
    n = int(sys.argv[1]); path = sys.argv[2]; work = sys.argv[3]
    nb = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    os.makedirs(work, exist_ok=True)
    expect = a000055(n)
    opener = lzma.open if path.endswith('.xz') else open
    bufs = [array('Q') for _ in range(nb)]
    bfiles = [open(os.path.join(work, 'n%d_b%d.keys' % (n, b)), 'wb') for b in range(nb)]
    lines = 0; bad = 0; firstbad = []
    with opener(path, 'rt') as fh:
        for line in fh:
            lines += 1
            err, key = check_line(n, line)
            if err:
                bad += 1
                if len(firstbad) < 5:
                    firstbad.append((lines, err))
                continue
            bufs[bucket_of(key, nb)].append(key)
            if lines % 1000000 == 0:
                for b in range(nb):
                    bufs[b].tofile(bfiles[b]); bufs[b] = array('Q')
                print('n=%d progress %d lines' % (n, lines), file=sys.stderr, flush=True)
    for b in range(nb):
        bufs[b].tofile(bfiles[b]); bfiles[b].close()
    bufs = None
    distinct = 0
    for b in range(nb):
        fn = os.path.join(work, 'n%d_b%d.keys' % (n, b))
        arr = array('Q')
        with open(fn, 'rb') as g:
            arr.frombytes(g.read())
        s = set(arr)
        distinct += len(s)
        del s, arr
        os.remove(fn)
    ok = (bad == 0 and lines == expect and distinct == lines)
    print('n=%d lines=%d invalid=%d distinct_canonical=%d A000055=%d -> %s%s' % (
        n, lines, bad, distinct, expect, 'OK' if ok else 'FAIL',
        '' if not firstbad else ' firstbad=%s' % firstbad), flush=True)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
