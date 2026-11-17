"""Independent TimPassLib evaluator (written from the bank's verification description).
Usage: python3 -I evaluate.py <instance_dir> <timetable.csv>   -> prints a JSON line.
Feasibility: for every activity (i -> j, bounds [L, U]) the periodic duration d = ((pi_j - pi_i - L) mod T) + L must be <= U.
Objective: for every OD pair (origin stop, destination stop, customers), the shortest path over drive, wait and change
activities (cost d, plus ean_change_penalty on each change) from any departure event at the origin stop to any arrival
event at the destination stop; total = sum of customers x shortest path. Sync, headway and turnaround carry no passengers."""
import sys, json, heapq, collections

def rows(path):
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'): continue
        yield [x.strip().strip('"') for x in line.split(';')]

def evaluate(inst, tt):
    cfg = {r[0]: r[1] for r in rows(f'{inst}/Config.csv')}
    T = int(cfg['period_length']); P = int(cfg['ean_change_penalty'])
    ev = {int(r[0]): (r[1], int(r[2])) for r in rows(f'{inst}/Events.csv')}
    pi = {int(r[0]): int(r[1]) for r in rows(tt)}
    errors = []
    if set(pi) != set(ev): errors.append('timetable events differ from Events.csv: %d vs %d' % (len(pi), len(ev)))
    if any(not (0 <= v < T) for v in pi.values()): errors.append('times outside 0..T-1')
    adj = collections.defaultdict(list); n_act = 0; infeasible = 0
    for r in rows(f'{inst}/Activities.csv'):
        typ, i, j, L, U = r[1], int(r[2]), int(r[3]), int(r[4]), int(r[5]); n_act += 1
        if i not in pi or j not in pi: continue
        d = (pi[j] - pi[i] - L) % T + L
        if d > U:
            infeasible += 1
            if infeasible <= 5: errors.append(f'activity {r[0]} ({typ}) duration {d} > upper {U}')
        if typ in ('drive', 'wait', 'change'):
            adj[i].append((j, d + (P if typ == 'change' else 0)))
    dep = collections.defaultdict(list); arr = collections.defaultdict(set)
    for e, (typ, stop) in ev.items():
        (dep[stop].append(e) if typ == 'departure' else arr[stop].add(e))
    od = collections.defaultdict(list)
    for r in rows(f'{inst}/OD.csv'):
        if int(r[2]) > 0: od[int(r[0])].append((int(r[1]), int(r[2])))
    total = 0; unreachable = 0; pax = 0
    for o, dests in od.items():
        dist = {}; h = [(0, e) for e in dep[o]]; heapq.heapify(h)
        while h:
            dv, u = heapq.heappop(h)
            if u in dist: continue
            dist[u] = dv
            for v, w in adj[u]:
                if v not in dist: heapq.heappush(h, (dv + w, v))
        for d, c in dests:
            best = min((dist[a] for a in arr[d] if a in dist), default=None)
            if best is None: unreachable += c; continue
            total += c * best; pax += c
    return dict(feasible=(not errors), infeasible_activities=infeasible, total=total, passengers=pax,
                unreachable_passengers=unreachable, activities=n_act, events=len(ev), period=T, change_penalty=P, errors=errors[:5])

if __name__ == '__main__':
    print(json.dumps(evaluate(sys.argv[1], sys.argv[2])))
