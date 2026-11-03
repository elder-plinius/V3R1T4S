import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../checker"))
from check_sem import check
# caterpillar_sem.py residue_lines > labelled : ELNR caterpillar construction. Walk the spine; at each spine vertex list
# its unseen neighbours (leaves, then next spine vertex). Label colour class of spine start with 1..a in order of first
# appearance, the other class a+1..n likewise; consecutive edges then have consecutive sums. Not a caterpillar -> left as is.
def label(n, es):
    adj = [[] for _ in range(n)]
    for u, v in es: adj[u].append(v); adj[v].append(u)
    spine = [v for v in range(n) if len(adj[v]) > 1]
    sp = set(spine)
    if any(sum(w in sp for w in adj[v]) > 2 for v in spine): return None
    ends = [v for v in spine if sum(w in sp for w in adj[v]) <= 1]
    path = [ends[0]]; prev = -1
    while True:
        nx = [w for w in adj[path[-1]] if w in sp and w != prev]
        if not nx: break
        prev = path[-1]; path.append(nx[0])
    if len(path) != len(spine): return None
    col = {path[0]: 0}; order = [path[0]]
    for i, s in enumerate(path):
        nb = [w for w in adj[s] if w not in sp] + ([path[i+1]] if i+1 < len(path) else [])
        for w in nb: col[w] = 1 - col[s]; order.append(w)
    # if spine of length 1 the leaves of an end were all listed; ensure all vertices seen
    if len(order) != n: return None
    X = [v for v in order if col[v] == 0]; Y = [v for v in order if col[v] == 1]
    f = [0]*n
    for i, v in enumerate(X): f[v] = i + 1
    for i, v in enumerate(Y): f[v] = len(X) + i + 1
    return f
for l in open(sys.argv[1]):
    p = l.rstrip("\n").split(";"); n = int(p[0]); es = [tuple(map(int, x.split("-"))) for x in p[1].split(",")]
    f = label(n, es)
    if f and check(n, es, f)[0]: print("%s;%s;%s;caterpillar" % (p[0], p[1], ",".join(map(str, f))))
    else: print("%s;%s;;UNLABELED caterpillar" % (p[0], p[1]))
