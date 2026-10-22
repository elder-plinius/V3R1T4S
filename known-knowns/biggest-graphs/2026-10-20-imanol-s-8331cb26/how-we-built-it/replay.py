"""Replay frozen centers, joint cuts and two exact annealing chunks."""
from collections import deque
import hashlib
import json
from pathlib import Path
import numpy as np
from ddlib import adj_to_edges, edges_to_adj, exact_cost, load_graph, write_edges
from sa2 import sa2_run

r = Path(__file__).resolve().parent
n, edges = load_graph(r / 'baseline.edges')
centers = json.loads((r / 'centers.json').read_text())['chosen']
adjacency = [[] for _ in range(n)]
for a, b in edges:
    adjacency[a].append(b)
    adjacency[b].append(a)
distances = {v: 0 for v in centers}
queue = deque(centers)
while queue:
    v = queue.popleft()
    if distances[v] == 3:
        continue
    for u in adjacency[v]:
        if u not in distances:
            distances[u] = distances[v] + 1
            queue.append(u)
assert len(distances) == n and len(set(centers)) == 14
current = set(map(tuple, edges.tolist())) | {(v, n) for v in centers}
def score(es):
    aa, dd = edges_to_adj(n + 1, np.array(sorted(es), np.int64), 15)
    return int(exact_cost(aa, dd, n + 1, 4)[0])
for v in centers:
    if sum(v in e for e in current) <= 14:
        continue
    candidates = [e for e in current if v in e and n not in e]
    cost, edge = min((score(current - {e}), e) for e in candidates)
    current.remove(edge)
assert score(current) == 16
aa, dd = edges_to_adj(n + 1, np.array(sorted(current), np.int64), 14)
for seed, t0, t1 in [(222600, .15, .02), (222601, .5, .04)]:
    best, aa, dd, accepted, full, screened = sa2_run(aa, dd, n + 1, 4, 14, 5000, t0, t1, seed, .6, 0., .2, 10**12, 0)
    assert int(best) == int(exact_cost(aa, dd, n + 1, 4)[0])
    print(seed, int(best), flush=True)
    if seed == 222600:
        aa, dd = edges_to_adj(n + 1, adj_to_edges(aa, dd), 14)
assert int(best) == 0
out = r / 'rebuilt.edges'
write_edges(out, adj_to_edges(aa, dd), 'bounded insertion; cell=14,4; seed=222601; bad_pairs=0')
assert hashlib.sha256(out.read_bytes()).hexdigest() == '8331cb2690217f6bc34b22a833f9690d19c87b0fa71db0113b1a12011d47fdb7'
print('PASS exact replay')
