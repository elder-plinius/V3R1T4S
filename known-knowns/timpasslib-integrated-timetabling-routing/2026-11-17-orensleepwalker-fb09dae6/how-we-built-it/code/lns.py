"""Fixed-route large-neighbourhood search for TimPassLib.
Usage: python3 -I lns.py <inst_dir> <start_timetable.csv> <out_dir> <seconds> <seed> [workers=6] [iter_seconds=10] [size0=150]
Loop: free a neighbourhood of rigid event groups, hold every passenger route fixed, minimise sum w_a * x_a over the activities touching the freed events
with CP-SAT (x_a = periodic duration in [L, U], pi_j - pi_i = x_a - T*p_a), warm-started from the incumbent; accept strict improvements; recompute the
exact total (re-routing) after each acceptance. Writes out_dir/best.csv (event_id; time) whenever the exact total improves, and out_dir/log.jsonl."""
import sys, os, json, time, random, resource, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ptl
from ortools.sat.python import cp_model
try: resource.setrlimit(resource.RLIMIT_AS, (6 * 1024 ** 3, 6 * 1024 ** 3))
except Exception: pass

def solve_nb(I, pi, F, w, secs, workers, seed):
    T = I.T; m = cp_model.CpModel(); t = {e: m.NewIntVar(0, T - 1, '') for e in F}
    inc = [k for k, a in enumerate(I.acts) if a[2] in F or a[3] in F]
    obj = []; X = {}; Pv = {}
    for k in inc:
        _, typ, i, j, L, U = I.acts[k]
        ilo, ihi = (0, T - 1) if i in F else (pi[i], pi[i]); jlo, jhi = (0, T - 1) if j in F else (pi[j], pi[j])
        dmin, dmax = jlo - ihi, jhi - ilo
        plo, phi = -((dmax - L) // T), (U - dmin) // T
        x = m.NewIntVar(L, U, ''); p = m.NewIntVar(plo, phi, '')
        m.Add(x == (t[j] if j in F else pi[j]) - (t[i] if i in F else pi[i]) + T * p)
        d = ptl.dur(I, I.acts[k], pi); X[k] = x; Pv[k] = p
        m.AddHint(x, d); m.AddHint(p, (d - (pi[j] - pi[i])) // T)
        if w[k]: obj.append(w[k] * x)
    for e in F: m.AddHint(t[e], pi[e])
    cur = sum(w[k] * ptl.dur(I, I.acts[k], pi) for k in inc if w[k])
    m.Minimize(sum(obj)) if obj else None
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = secs; sv.parameters.num_workers = workers; sv.parameters.random_seed = seed
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return sv.StatusName(st), cur, cur, None
    new = {e: sv.Value(t[e]) for e in F}; val = sum(w[k] * sv.Value(X[k]) for k in inc if w[k])   # exact integer objective (ObjectiveValue() is a float)
    return sv.StatusName(st), cur, val, new

def neighbourhoods(I, G, w, rng, size):
    gid = {};
    for n, g in enumerate(G):
        for e in g: gid[e] = n
    gw = [0] * len(G); nb = collections.defaultdict(lambda: collections.defaultdict(int))
    for k, a in enumerate(I.acts):
        if w[k]:
            gi, gj = gid[a[2]], gid[a[3]]; gw[gi] += w[k]; gw[gj] += w[k]
            if gi != gj: nb[gi][gj] += w[k]; nb[gj][gi] += w[k]
    lines = collections.defaultdict(set); stops = collections.defaultdict(set)
    for e, (typ, stop, line) in I.ev.items(): lines[line].add(gid[e]); stops[stop].add(gid[e])
    pos = [n for n in range(len(G)) if gw[n]] or list(range(len(G)))
    def grow(start):
        S = set(start); ev = sum(len(G[n]) for n in S); front = list(S)
        while ev < size and front:
            u = front.pop(rng.randrange(len(front)))
            cand = sorted(nb[u].items(), key=lambda kv: -kv[1] * rng.random())[:4]
            for v, _ in cand:
                if v not in S and ev < size: S.add(v); ev += len(G[v]); front.append(v)
            if not cand and pos:
                v = rng.choice(pos)
                if v not in S: S.add(v); ev += len(G[v]); front.append(v)
        return S
    kind = rng.choice(['bfs', 'bfs', 'random', 'line', 'stop'])
    if kind == 'random':
        # weighted sampling without replacement (Efraimidis-Spirakis); stops when every passenger-carrying group is in (v1 looped forever then)
        S = set(); ev = 0
        for n in sorted(pos, key=lambda x: -(rng.random() ** (1.0 / gw[x])) if gw[x] else 0):
            if ev >= size: break
            S.add(n); ev += len(G[n])
    elif kind == 'line': S = grow(lines[rng.choice(list(lines))])
    elif kind == 'stop': S = grow(stops[rng.choice(list(stops))])
    else: S = grow([rng.choices(pos, weights=[gw[x] for x in pos])[0]])
    return kind, {e for n in S for e in G[n]}

def main():
    inst, start, out, secs, seed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 6; iter_s = float(sys.argv[7]) if len(sys.argv) > 7 else 10; size = int(sys.argv[8]) if len(sys.argv) > 8 else 150
    os.makedirs(out, exist_ok=True); rng = random.Random(seed)
    I = ptl.Inst(inst); pi = ptl.load_tt(start); assert ptl.feasible(I, pi), 'start timetable infeasible'
    G = ptl.groups(I); tot, w, un = ptl.evaluate_flows(I, pi); start_total = tot; best = tot
    log = open(os.path.join(out, 'log.jsonl'), 'w'); t0 = time.time(); it = acc = 0; stall = 0
    print(json.dumps(dict(start_total=tot, events=len(I.ev), groups=len(G), unreachable=un)), flush=True)
    while time.time() - t0 < secs:
        it += 1; kind, F = neighbourhoods(I, G, w, rng, size)
        st, cur, val, new = solve_nb(I, pi, F, w, min(iter_s, max(1.0, secs - (time.time() - t0))), workers, rng.randrange(10 ** 6))
        rec = dict(it=it, kind=kind, free=len(F), status=st, fixed_route_gain=cur - val, t=round(time.time() - t0, 1))
        if new is not None and val < cur:
            p2 = dict(pi); p2.update(new)
            if ptl.feasible(I, p2):
                tot2, w2, un2 = ptl.evaluate_flows(I, p2)
                if tot2 < tot and un2 == 0:
                    pi, tot, w = p2, tot2, w2; acc += 1; stall = 0; rec['total'] = tot
                    if tot < best: best = tot; ptl.save_tt(os.path.join(out, 'best.csv'), pi)
                else: rec['rejected'] = 'exact total did not improve'
            else: rec['rejected'] = 'infeasible'
        else:
            stall += 1
            if st == 'OPTIMAL': size = min(int(size * 1.15) + 1, len(I.ev))        # exhausted quickly: try bigger
            elif st != 'OPTIMAL' and stall % 5 == 0: size = max(30, int(size * 0.85))  # timed out: try smaller
        log.write(json.dumps(rec) + '\n'); log.flush()
    if not os.path.exists(os.path.join(out, 'best.csv')): ptl.save_tt(os.path.join(out, 'best_unchanged.csv'), pi)
    print(json.dumps(dict(start_total=start_total, best_total=best, improved_by=start_total - best, iterations=it, accepted=acc, seconds=round(time.time() - t0, 1), seed=seed, final_size=size)), flush=True)

if __name__ == '__main__':
    main()
