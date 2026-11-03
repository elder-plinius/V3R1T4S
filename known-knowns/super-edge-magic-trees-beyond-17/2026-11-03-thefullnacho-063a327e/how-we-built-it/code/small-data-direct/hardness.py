import sys, collections
# per-order hardness table from a sem_direct certificate: node counts, attempts, top-5 trees with their diameter and max degree
f = sys.argv[1]; rows = []
for line in open(f):
    p = line.rstrip("\n").split(";")
    if len(p) < 5: continue
    rows.append((int(p[3]), int(p[4]), p[1]))
rows.sort(reverse=True)
def diam(es):
    adj = collections.defaultdict(list)
    for e in es.split(","): a, b = map(int, e.split("-")); adj[a].append(b); adj[b].append(a)
    def far(s):
        d = {s: 0}; Q = [s]
        for x in Q:
            for y in adj[x]:
                if y not in d: d[y] = d[x] + 1; Q.append(y)
        m = max(d, key=d.get); return m, d[m]
    return far(far(0)[0])[1], max(len(v) for v in adj.values())
tot = sum(r[0] for r in rows); print("trees %d total_nodes %d mean_nodes %.1f max_attempts %d" % (len(rows), tot, tot/len(rows), max(r[1] for r in rows)))
for nodes, att, es in rows[:5]: print("nodes %d attempts %d diameter,maxdeg %s edges %s" % (nodes, att, diam(es), es))
