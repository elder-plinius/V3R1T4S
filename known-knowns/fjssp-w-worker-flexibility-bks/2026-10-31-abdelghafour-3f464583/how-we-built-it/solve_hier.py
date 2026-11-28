"""Second FJSSP-W formulation (lens cpsat-hier): hierarchical choice (machine interval, then worker interval inside it),
a redundant cumulative of capacity min(machines, workers), no cap on the makespan, longer runs.
Usage: solve_hier.py instance.fjs UB seconds workers out.json   -> one result line; writes out.json if a schedule < UB is found."""
import json, os, sys, time
from ortools.sat.python import cp_model
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'cpsat', 'code'))
from fjsspw_check import read_instance

inst, ub, secs, workers, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
n_mach, n_work, jobs = read_instance(inst)
H = sum(max(opt.values()) for ops in jobs for opt in ops)
mdl = cp_model.CpModel()
mk = mdl.NewIntVar(0, H, 'mk')
by_m, by_w, all_iv, pick, start = {}, {}, [], {}, {}
for j, ops in enumerate(jobs, 1):
    prev = None
    for o, opt in enumerate(ops, 1):
        lo = min(opt.values())
        s = mdl.NewIntVar(0, H, ''); e = mdl.NewIntVar(lo, H, ''); start[(j, o)] = s
        dop = mdl.NewIntVar(lo, max(opt.values()), '')
        all_iv.append(mdl.NewIntervalVar(s, dop, e, ''))
        machines = sorted({m for m, _ in opt})
        mlits = []
        for m in machines:
            pairs = {w: d for (mm, w), d in opt.items() if mm == m}
            bm = mdl.NewBoolVar(''); mlits.append(bm)
            by_m.setdefault(m, []).append(mdl.NewOptionalIntervalVar(s, dop, e, bm, ''))
            wlits = []
            for w, d in pairs.items():
                bw = mdl.NewBoolVar(''); wlits.append(bw); pick[(j, o, m, w)] = bw
                mdl.Add(dop == d).OnlyEnforceIf(bw)
                by_w.setdefault(w, []).append(mdl.NewOptionalIntervalVar(s, d, e, bw, ''))
            mdl.Add(sum(wlits) == bm)
        mdl.AddExactlyOne(mlits)
        if prev is not None:
            mdl.Add(s >= prev)
        prev = e
    mdl.Add(mk >= prev)
for ivs in list(by_m.values()) + list(by_w.values()):
    mdl.AddNoOverlap(ivs)
mdl.AddCumulative(all_iv, [1] * len(all_iv), min(n_mach, n_work))
mdl.Minimize(mk)
sv = cp_model.CpSolver()
sv.parameters.max_time_in_seconds = secs
sv.parameters.num_workers = workers
t0 = time.time(); st = sv.Solve(mdl)
name = os.path.basename(inst)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    val = sv.Value(mk)
    if val < ub:
        rows = [[j, o, m, w, sv.Value(start[(j, o)])] for (j, o, m, w), b in pick.items() if sv.Value(b)]
        json.dump({'ops': rows}, open(out, 'w'))
    print('%s ub=%d status=%s makespan=%d bound=%d time=%.1f' % (name, ub, sv.StatusName(st), val, int(sv.BestObjectiveBound()), time.time() - t0))
else:
    print('%s ub=%d status=%s makespan=none bound=unknown time=%.1f' % (name, ub, sv.StatusName(st), time.time() - t0))
