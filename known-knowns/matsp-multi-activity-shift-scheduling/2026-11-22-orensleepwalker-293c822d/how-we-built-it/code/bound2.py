"""Operation Flatline, phase 0 "Benchmark" (Andy, 2026-11-22): a shift-structure lower bound for every open instance.
Solved as an LP (GLOP; continuous counts, convex piecewise-linear cost) or a MIP (SCIP; integer counts). Relaxation (every real schedule maps onto a feasible point of it with no larger cost, so its optimum, and any proven bound on it,
is a lower bound on the true penalty):
  - integer counts c[d,s,l] of shifts by calendar day d, allowed start s and length l (24..40 intervals), finishing in the horizon;
  - per day at most |E| shifts; total worked intervals between sum ceil(min/15) and sum floor(max/15) over employees;
  - staff on duty T_i = number of counted shifts covering interval i, with V_i <= T_i <= |E| (V_i = total minimum cover);
  - cost of interval i given T_i: the cheapest task split, i.e. fill every task to its max first, then spread the excess
    E = max(0, T_i - sum_a max_ia) evenly over the A tasks: (A - r) q^2 + r (q + 1)^2 with q, r = divmod(E, A).
  Dropped: employee identities, 14 h rest, 5 in 6 days, per-employee min/max, task minimum cover and the 1-hour task runs.
Writes zero/bound2.jsonl (resumable): status, relaxation objective, proven bound, counting bound, record."""
import sys, os, json, time, zipfile, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'code')); import matsp
SECS = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0; WORKERS = int(sys.argv[2]) if len(sys.argv) > 2 else 6
SOLVER = sys.argv[3] if len(sys.argv) > 3 else 'GLOP'
Z = zipfile.ZipFile(os.path.join(H, '..', 'raw/instances1_225.zip')); OUT = os.path.join(H, 'bound2.jsonl')
split = json.load(open(os.path.join(H, 'split.json'))); scr = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open(os.path.join(H, 'screen.tsv')) if l[0].isdigit()}
done = {json.loads(l)['id'] for l in open(OUT)} if os.path.exists(OUT) else set()
idx = lambda d, m: (d - 1) * 96 + m // 15 - 24
for num in split['open']:
    if num in done or num in (80, 155): continue
    stem = scr[str(num)][1]; I = matsp.read_instance(Z.read('instances1_225/txt/%s.txt' % stem).decode())
    h, A, N, nE = I['h'], I['A'], I['N'], len(I['staff'])
    Wcap = [sum(I['vmax'][a][i] for a in range(1, A + 1)) for i in range(N)]; Vmin = [sum(I['vmin'][a][i] for a in range(1, A + 1)) for i in range(N)]
    wmin = sum(math.ceil(b / 15) for b, c in I['staff'].values()); wmax = sum(c // 15 for b, c in I['staff'].values())
    from ortools.linear_solver import pywraplp
    sv = pywraplp.Solver.CreateSolver(SOLVER); inf = sv.infinity(); cover = [[] for _ in range(N)]; work = []; perday = {}
    integer = SOLVER in ('SCIP', 'CBC')
    for d in range(1, h + 2):
        for s0 in range(0, 1440, 15):
            if not matsp.allowed_start(d, s0, h): continue
            t = idx(d, s0)
            if t < 0: continue
            for l in range(24, 41):
                if t + l > N: continue
                c = sv.IntVar(0, nE, '') if integer else sv.NumVar(0, nE, ''); work.append((c, l)); perday.setdefault(d, []).append(c)
                for i in range(t, t + l): cover[i].append(c)
    for d, cs in perday.items(): sv.Add(sv.Sum(cs) <= nE)
    tw = sv.Sum([c * l for c, l in work]); sv.Add(tw >= wmin); sv.Add(tw <= wmax)
    obj = []
    for i in range(N):
        T = sv.Sum(cover[i]) if cover[i] else 0
        if cover[i]: sv.Add(T >= Vmin[i]); sv.Add(T <= nE)
        elif Vmin[i] > 0: raise SystemExit('uncoverable interval')
        if Wcap[i] >= nE or not cover[i]: continue
        y = sv.NumVar(0, inf, ''); obj.append(y)
        def g(v):
            e = max(0, v - Wcap[i]); q, r = divmod(e, A); return (A - r) * q * q + r * (q + 1) * (q + 1)
        v = Wcap[i]   # epigraph of the convex piecewise-linear interpolation: one line per slope change (every A units)
        while v < nE:
            sl = g(v + 1) - g(v); sv.Add(y >= g(v) + sl * (T - v)); v += A
    sv.Minimize(sv.Sum(obj)); sv.SetTimeLimit(int(SECS * 1000))
    if SOLVER == 'SCIP': sv.SetNumThreads(WORKERS)
    t0 = time.time(); st = sv.Solve()
    names = {0: 'OPTIMAL', 1: 'FEASIBLE', 2: 'INFEASIBLE', 3: 'UNBOUNDED', 4: 'ABNORMAL', 6: 'NOT_SOLVED'}
    ok = st in (0, 1); bnd = sv.Objective().BestBound() if integer else (sv.Objective().Value() if st == 0 else 0)
    rec = dict(id=num, stem=stem, record=int(scr[str(num)][2]), counting_bound=int(scr[str(num)][8]), solver=SOLVER, status=names.get(st, str(st)),
               relax_obj=round(sv.Objective().Value(), 3) if ok else None, bound=int(math.ceil(bnd - 1e-6)) if ok or integer else 0, secs=round(time.time() - t0, 1))
    rec['new_bound'] = max(rec['bound'], rec['counting_bound'])
    open(OUT, 'a').write(json.dumps(rec) + '\n'); print(rec, flush=True)
print('done', flush=True)
