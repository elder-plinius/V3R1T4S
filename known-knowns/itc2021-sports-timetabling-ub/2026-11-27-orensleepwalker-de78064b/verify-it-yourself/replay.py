"""Fresh-session replay of the five saved CP-SAT certificate models (one worker, the recorded seed; OR-Tools)."""
import sys
from ortools.sat.python import cp_model
for name, path, seed in [l.split() for l in open(sys.argv[1]) if l.strip()]:
    m = cp_model.CpModel(); assert m.proto.parse_text_format(open(path).read())
    sv = cp_model.CpSolver(); sv.parameters.num_workers = 1; sv.parameters.random_seed = int(seed); sv.parameters.linearization_level = 2; sv.parameters.max_time_in_seconds = 600
    st = sv.Solve(m); print('%-10s %s objective %s bound %s %.1fs' % (name, sv.StatusName(st), round(sv.ObjectiveValue()) if st in (2, 4) else None, round(sv.BestObjectiveBound()), sv.WallTime()), flush=True)
