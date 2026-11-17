"""TimPassLib helpers for the fixed-route large-neighbourhood search (solver side; the independent evaluator is evaluate_independent.py).
Instance = dir with Config.csv, Events.csv, Activities.csv, OD.csv; timetable = 'event_id; time' lines.
Fixed-route idea: with every passenger's route held fixed, total travel time = sum_a w_a * d_a + const, where d_a is the periodic duration of
activity a and w_a the number of passengers using it (change arcs also pay the change penalty, a constant). Re-routing can only lower it."""
import heapq, collections

def rows(path):
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'): continue
        yield [x.strip().strip('"') for x in line.split(';')]

class Inst:
    def __init__(self, d):
        cfg = {r[0]: r[1] for r in rows(f'{d}/Config.csv')}
        self.T = int(cfg['period_length']); self.P = int(cfg['ean_change_penalty'])
        self.ev = {}                     # id -> (type, stop, line)
        for r in rows(f'{d}/Events.csv'): self.ev[int(r[0])] = (r[1], int(r[2]), int(r[3]) if len(r) > 3 and r[3].lstrip('-').isdigit() else -1)
        self.acts = []                   # (idx, type, i, j, L, U)
        for r in rows(f'{d}/Activities.csv'): self.acts.append((int(r[0]), r[1], int(r[2]), int(r[3]), int(r[4]), int(r[5])))
        self.od = collections.defaultdict(list)
        for r in rows(f'{d}/OD.csv'):
            if int(r[2]) > 0: self.od[int(r[0])].append((int(r[1]), int(r[2])))
        self.pax = ('drive', 'wait', 'change')
        self.adj = collections.defaultdict(list)   # event -> [(neighbour, activity position)]
        for k, a in enumerate(self.acts):
            if a[1] in self.pax: self.adj[a[2]].append((a[3], k))
        self.dep = collections.defaultdict(list); self.arr = collections.defaultdict(list)
        for e, (typ, stop, line) in self.ev.items(): (self.dep if typ == 'departure' else self.arr)[stop].append(e)

def load_tt(path):
    return {int(r[0]): int(r[1]) for r in rows(path)}

def save_tt(path, pi):
    with open(path, 'w') as fh:
        fh.write('# event_id; time\n')
        for e in sorted(pi): fh.write(f'{e}; {pi[e]}\n')

def dur(I, a, pi):
    return (pi[a[3]] - pi[a[2]] - a[4]) % I.T + a[4]

def feasible(I, pi):
    return all(dur(I, a, pi) <= a[5] for a in I.acts)

def evaluate_flows(I, pi):
    """Exact total (same definition as the criterion) and arc weights w[k] (passengers per activity position) from one shortest-path tree per origin."""
    d = [dur(I, a, pi) + (I.P if a[1] == 'change' else 0) for a in I.acts]
    w = [0] * len(I.acts); total = 0; unreachable = 0
    for o, dests in I.od.items():
        dist = {}; pred = {}; order = []
        h = [(0, e, -1) for e in I.dep[o]]; heapq.heapify(h)
        while h:
            dv, u, pk = heapq.heappop(h)
            if u in dist: continue
            dist[u] = dv; pred[u] = pk; order.append(u)
            for v, k in I.adj[u]:
                if v not in dist: heapq.heappush(h, (dv + d[k], v, k))
        node_dem = collections.defaultdict(int)
        for dst, c in dests:
            best = None
            for a in I.arr[dst]:
                if a in dist and (best is None or dist[a] < dist[best]): best = a
            if best is None: unreachable += c; continue
            total += c * dist[best]; node_dem[best] += c
        for u in reversed(order):
            q = node_dem.get(u, 0)
            if q and pred[u] >= 0:
                k = pred[u]; w[k] += q; node_dem[I.acts[k][2]] += q
    return total, w, unreachable

def groups(I):
    """Rigid groups: events joined by activities with L == U (their times move together)."""
    par = {e: e for e in I.ev}
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a in I.acts:
        if a[4] == a[5]: par[f(a[2])] = f(a[3])
    g = collections.defaultdict(list)
    for e in I.ev: g[f(e)].append(e)
    return list(g.values())

# ---- joint route + timetable helpers ----
def costs_current(I, pi):
    return [dur(I, a, pi) + (I.P if a[1] == 'change' else 0) for a in I.acts]

def tree(I, o, cost):
    """Multi-source Dijkstra from every departure event at stop o over passenger arcs with arc costs 'cost'. Returns dist, pred (activity position or -1)."""
    dist = {}; pred = {}; h = [(0, e, -1) for e in I.dep[o]]; heapq.heapify(h)
    while h:
        dv, u, pk = heapq.heappop(h)
        if u in dist: continue
        dist[u] = dv; pred[u] = pk
        for v, k in I.adj[u]:
            if v not in dist: heapq.heappush(h, (dv + cost[k], v, k))
    return dist, pred

def best_arrival(I, dist, dst):
    best = None
    for a in I.arr[dst]:
        if a in dist and (best is None or dist[a] < dist[best]): best = a
    return best

def path_arcs(I, pred, node):
    arcs = []
    while pred[node] >= 0:
        k = pred[node]; arcs.append(k); node = I.acts[k][2]
    return tuple(reversed(arcs))
