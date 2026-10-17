"""Linear-graph utilities (opus-add). A graph has N inputs (ids 0..N-1), internal nodes (ids N.., topological),
and K sinks; each vertex lists in-edges (src, sign). cost = sum over internal and sinks of (indeg - 1)."""
import json, sys
sys.path.insert(0, '[addcomp]/tools')
from check_slp import expand

def read_graph(path):
    L = open(path).read().split('\n')
    _, N, K, M = L[0].split(); N, K, M = int(N), int(K), int(M)
    nodes, sinks = [], []
    for line in L[1:]:
        if not line.strip(): continue
        t = line.split(); d = int(t[1]); e = [(int(t[2 + 2*i]), int(t[3 + 2*i])) for i in range(d)]
        (nodes if t[0] == 'n' else sinks).append(e)
    assert len(nodes) == M and len(sinks) == K
    return N, nodes, sinks

def cost(g):
    N, nodes, sinks = g
    return sum(len(e) - 1 for e in nodes) + sum(len(e) - 1 for e in sinks)

def prune(g):
    """remove internal nodes with no out-edges (iteratively)."""
    N, nodes, sinks = g
    while True:
        used = set()
        for e in nodes + sinks:
            for s, _ in e: used.add(s)
        dead = [i for i in range(len(nodes)) if N + i not in used]
        if not dead: return (N, nodes, sinks)
        keep = [i for i in range(len(nodes)) if N + i in used]
        newid = {N + i: N + j for j, i in enumerate(keep)}
        f = lambda e: [(newid.get(s, s) if s >= N else s, c) for s, c in e]
        nodes = [f(nodes[i]) for i in keep]; sinks = [f(e) for e in sinks]

def transpose(g):
    N, nodes, sinks = prune(g)
    M, K = len(nodes), len(sinks)
    out = {}  # old vertex -> list of (target, sign); targets: ('n', i) or ('o', j)
    for i, e in enumerate(nodes):
        for s, c in e: out.setdefault(s, []).append((('n', i), c))
    for j, e in enumerate(sinks):
        for s, c in e: out.setdefault(s, []).append((('o', j), c))
    # new ids: old sink j -> j ; old node i -> K + (M-1-i) ; old input x -> new sink x
    def nid(t): return t[1] if t[0] == 'o' else K + (M - 1 - t[1])
    nn = []
    for i in range(M - 1, -1, -1):
        nn.append([(nid(t), c) for t, c in out.get(N + i, [])])
    ns = [[(nid(t), c) for t, c in out.get(x, [])] for x in range(N)]
    return (K, nn, ns)

def expand_graph(g):
    N, nodes, sinks = g
    vec = []
    def ex(e):
        o = {}
        for s, c in e:
            src = {s: 1} if s < N else vec[s - N]
            for k, v in src.items(): o[k] = o.get(k, 0) + c * v
        return {k: v for k, v in o.items() if v}
    for e in nodes: vec.append(ex(e))
    return [ex(e) for e in sinks]

def to_perminov(g, base):
    """graph over inputs 0..N-1 -> (fresh, rows) in Perminov's layout, fresh indices starting at `base` (= N).
    internal nodes of indegree 1 are inlined (sign copies)."""
    N, nodes, sinks = prune(g)
    assert base == N
    alias = {}   # old id -> list of (perminov index, sign) i.e. a single term
    fresh = []
    def sub(e):
        o = []
        for s, c in e:
            if s < N: o.append((s, c))
            else:
                t, sg = alias[s]; o.append((t, sg * c))
        return o
    for i, e in enumerate(nodes):
        f = sub(e)
        if len(f) == 0: raise ValueError('empty internal node')
        if len(f) == 1: alias[N + i] = f[0]
        else:
            alias[N + i] = (N + len(fresh), 1); fresh.append(f)
    rows = [sub(e) for e in sinks]
    J = lambda f: [{"index": int(a), "value": int(b)} for a, b in f]
    return [J(f) for f in fresh], [J(f) for f in rows]

def maps_of(d):
    n, m, p = d['n']; r = d['m']
    _, U = expand(d.get('u_fresh', []), d['u'], n*m, 'u')
    _, V = expand(d.get('v_fresh', []), d['v'], m*p, 'v')
    _, W = expand(d.get('w_fresh', []), d['w'], r, 'w')
    dense = lambda rows, N: [[row.get(j, 0) for j in range(N)] for row in rows]
    return dense(U, n*m), dense(V, m*p), dense(W, r)

def write_mat(M, path):
    with open(path, 'w') as f:
        f.write('%d %d\n' % (len(M), len(M[0])))
        for row in M: f.write(' '.join(map(str, row)) + '\n')

def T(M): return [list(x) for x in zip(*M)]
