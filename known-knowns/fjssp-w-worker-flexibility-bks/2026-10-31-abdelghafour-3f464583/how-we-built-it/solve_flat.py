"""CP-SAT model for FJSSP-W: one optional interval per eligible (operation, machine, worker) triple, exactly one chosen,
no-overlap per machine and per worker, job precedence, minimise makespan with makespan <= UB - 1 as a hard cap.
Usage: solve.py instance.fjs UB seconds workers out.json   -> prints one result line; writes out.json if a schedule is found."""
import json, sys, time
from ortools.sat.python import cp_model
sys.path.insert(0, __import__('os').path.dirname(__file__))
from fjsspw_check import read_instance

inst, ub, secs, workers, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
n_mach, n_work, jobs = read_instance(inst)
cap = ub - 1 if len(sys.argv) < 7 else sum(max(opt.values()) for ops in jobs for opt in ops)  # 7th arg "nocap": search the full horizon
mdl = cp_model.CpModel()
mk = mdl.NewIntVar(0, cap, 'mk')
by_m, by_w, choice, start = {}, {}, {}, {}
prev_end = None
for j, ops in enumerate(jobs, 1):
    prev_end = None
    for o, opt in enumerate(ops, 1):
        lo, hi = min(opt.values()), max(opt.values())
        s = mdl.NewIntVar(0, cap - lo, 's%d_%d' % (j, o))
        e = mdl.NewIntVar(lo, cap, 'e%d_%d' % (j, o))
        start[(j, o)] = s
        lits = []
        for (m, w), d in opt.items():
            b = mdl.NewBoolVar('')
            iv = mdl.NewOptionalIntervalVar(s, d, e, b, '')
            by_m.setdefault(m, []).append(iv); by_w.setdefault(w, []).append(iv)
            lits.append(b); choice[(j, o, m, w)] = b
        mdl.AddExactlyOne(lits)
        if prev_end is not None:
            mdl.Add(s >= prev_end)
        prev_end = e
    mdl.Add(mk >= prev_end)
for ivs in list(by_m.values()) + list(by_w.values()):
    mdl.AddNoOverlap(ivs)
mdl.Minimize(mk)
sv = cp_model.CpSolver()
sv.parameters.max_time_in_seconds = secs
sv.parameters.num_workers = workers
t0 = time.time()
st = sv.Solve(mdl)
name = __import__('os').path.basename(inst)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    rows = [[j, o, m, w, sv.Value(start[(j, o)])] for (j, o, m, w), b in choice.items() if sv.Value(b)]
    json.dump({'ops': rows}, open(out, 'w'))
    print('%s ub=%d status=%s makespan=%d bound=%d time=%.1f' % (name, ub, sv.StatusName(st), sv.Value(mk), int(sv.BestObjectiveBound()), time.time() - t0))
else:
    print('%s ub=%d status=%s makespan=none bound=%s time=%.1f' % (name, ub, sv.StatusName(st), 'infeasible_below_ub' if st == cp_model.INFEASIBLE else 'unknown', time.time() - t0))
