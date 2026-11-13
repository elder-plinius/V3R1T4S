"""CP-SAT model for FJSSP-W. Usage: solve.py <instance.fjs> <seconds> <workers> <seed> <out.json> [hint.json]
One start per operation; one presence literal and optional fixed-size interval per eligible (machine, worker) pair;
one optional interval per (operation, machine) and per (operation, worker), linked to the pair literals; no-overlap per machine and per worker; job precedence; redundant cumulative of capacity min(machines, workers); minimise makespan."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'common' / 'code')); import fjsspw
from ortools.sat.python import cp_model
inst, secs, nw, seed, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
J, M, W, jobs = fjsspw.parse(inst)
H = sum(max(a.values()) for ops in jobs for a in ops)
m = cp_model.CpModel(); mk = m.NewIntVar(0, H, 'mk'); S = {}; D = {}; B = {}; byM = {}; byW = {}; ivs = []
for j, ops in enumerate(jobs):
    for o, alt in enumerate(ops):
        s = m.NewIntVar(0, H, ''); ds = sorted(set(alt.values()))
        d = m.NewIntVarFromDomain(cp_model.Domain.FromValues(ds), ''); S[j, o] = s; D[j, o] = d
        e = m.NewIntVar(0, H, ''); m.Add(e == s + d); lits = []; bm = {}; bw = {}
        for (mm, ww), dur in alt.items():
            b = m.NewBoolVar(''); B[j, o, mm, ww] = b; lits.append(b)
            bm.setdefault(mm, []).append(b); bw.setdefault(ww, []).append(b)
        m.AddExactlyOne(lits)
        m.Add(d == sum(B[j, o, mm, ww] * dur for (mm, ww), dur in alt.items()))
        for res, grp, by in ((0, bm, byM), (1, bw, byW)):   # one optional interval per (operation, machine) and per (operation, worker)
            for r, bs in grp.items():
                if len(bs) == 1: p = bs[0]
                else: p = m.NewBoolVar(''); m.Add(sum(bs) == p)
                by.setdefault(r, []).append(m.NewOptionalIntervalVar(s, d, e, p, ''))
        ivs.append(m.NewIntervalVar(s, d, e, ''))
        if o: m.Add(s >= S[j, o - 1] + D[j, o - 1])
    m.Add(mk >= S[j, len(ops) - 1] + D[j, len(ops) - 1])
for lst in byM.values(): m.AddNoOverlap(lst)
for lst in byW.values(): m.AddNoOverlap(lst)
m.AddCumulative(ivs, [1] * len(ivs), min(M, W))
m.Minimize(mk)
if len(sys.argv) > 6:
    for j, o, mm, ww, s, d in json.load(open(sys.argv[6]))['ops']:
        m.AddHint(S[j, o], s)
        for (a, b2), _ in jobs[j][o].items(): m.AddHint(B[j, o, a, b2], int((a, b2) == (mm, ww)))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = secs; sv.parameters.num_workers = nw; sv.parameters.random_seed = seed
t0 = time.time(); st = sv.Solve(m); res = {'instance': Path(inst).stem, 'status': sv.StatusName(st), 'seconds': round(time.time() - t0, 1),
    'time_limit': secs, 'workers': nw, 'seed': seed, 'ortools': __import__('ortools').__version__}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    ops = []
    for (j, o), s in S.items():
        (mm, ww), = [(a, b2) for (a, b2) in jobs[j][o] if sv.Value(B[j, o, a, b2])]
        ops.append([j, o, mm, ww, sv.Value(s), jobs[j][o][(mm, ww)]])
    res.update(ops=sorted(ops), makespan=int(sv.ObjectiveValue()), bound=int(sv.BestObjectiveBound()))
    ok, mk2, err = fjsspw.check(inst, res); res['checker'] = {'valid': ok, 'makespan': mk2, 'errors': err[:5]}
json.dump(res, open(out, 'w')); print(json.dumps({k: v for k, v in res.items() if k != 'ops'}))
