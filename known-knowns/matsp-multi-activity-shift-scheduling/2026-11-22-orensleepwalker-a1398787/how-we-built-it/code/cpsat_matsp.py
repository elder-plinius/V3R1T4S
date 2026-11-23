"""Exact CP-SAT model of the multi-activity shift scheduling problem (scout pilot), from ProblemDefinition.pdf.
Usage: python3 cpsat_matsp.py <instance stem, e.g. 1_7_10_1> <seconds> <workers> [best_known]
Per employee and calendar day: presence z, start t (allowed starts only, absolute interval index), length n in 24..40, end u = t + n.
on[e][i] = 1 iff interval i lies in the shift of its own calendar day or of the previous one (rest makes them exclusive).
Per interval one activity among A when on duty; runs of 1-3 intervals of an activity are forbidden as in the definition.
Hard: horizon end, 14 h rest, min/max minutes, 5 working days in any 6, cover >= minimum. Objective: sum of y^2, y = max(0, cover - max).
Writes out/<stem>.cpsat.xml in the site's solution format and checks it with code/matsp.py."""
import sys, os, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import matsp
from ortools.sat.python import cp_model
stem, secs, workers = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); best = int(sys.argv[4]) if len(sys.argv) > 4 else None
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
Z = zipfile.ZipFile(os.path.join(D, 'raw/instances1_225.zip')); I = matsp.read_instance(Z.read('instances1_225/txt/%s.txt' % stem).decode())
h, A, N = I['h'], I['A'], I['N']; E = sorted(I['staff'], key=int); days = range(1, h + 2)
def starts(d):  # allowed start minutes of calendar day d (1-based)
    return [m for m in range(0, 1440, 15) if matsp.allowed_start(d, m, h)]
idx = lambda d, m: (d - 1) * 96 + m // 15 - 24
m = cp_model.CpModel(); on = {}; X = {}; shift = {}
for e in E:
    for d in days:
        S = [idx(d, s) for s in starts(d) if idx(d, s) >= 0 and idx(d, s) + 24 <= N]
        if not S: continue
        z = m.NewBoolVar(''); t = m.NewIntVarFromDomain(cp_model.Domain.FromValues(S), ''); n = m.NewIntVar(24, 40, ''); u = m.NewIntVar(0, N, '')
        m.Add(u == t + n); shift[e, d] = (z, t, n, u)
    on_e = [[] for _ in range(N)]
    for (ee, d), (z, t, n, u) in shift.items():
        if ee != e: continue
        lo = idx(d, 0) if d > 1 else 0
        for i in range(max(0, lo), min(N, idx(d, 1425) + 40)):
            c = m.NewBoolVar(''); a1 = m.NewBoolVar(''); a2 = m.NewBoolVar('')
            m.Add(t <= i).OnlyEnforceIf(a1); m.Add(t > i).OnlyEnforceIf(a1.Not())
            m.Add(u > i).OnlyEnforceIf(a2); m.Add(u <= i).OnlyEnforceIf(a2.Not())
            m.AddBoolAnd([z, a1, a2]).OnlyEnforceIf(c); m.AddBoolOr([z.Not(), a1.Not(), a2.Not()]).OnlyEnforceIf(c.Not())
            on_e[i].append(c)
    for i in range(N):
        v = m.NewBoolVar(''); m.Add(sum(on_e[i]) == v); on[e, i] = v
    mins = []
    for d in days:
        if (e, d) not in shift: continue
        z, t, n, u = shift[e, d]; w = m.NewIntVar(0, 40, ''); m.Add(w == n).OnlyEnforceIf(z); m.Add(w == 0).OnlyEnforceIf(z.Not()); mins.append(w)
        if (e, d + 1) in shift:
            z2, t2, _, _ = shift[e, d + 1]; m.Add(u <= t2 - 56).OnlyEnforceIf([z, z2])
    b, c = I['staff'][e]; m.Add(sum(mins) * 15 >= b); m.Add(sum(mins) * 15 <= c)
    zs = {d: shift[e, d][0] for d in days if (e, d) in shift}
    for d in range(1, h + 2 - 5): m.Add(sum(zs[k] for k in range(d, d + 6) if k in zs) <= 5)
    for i in range(N):
        if A == 1: X[e, i, 1] = on[e, i]
        else:
            xs = [m.NewBoolVar('') for _ in range(A)]
            for a in range(A): X[e, i, a + 1] = xs[a]
            m.Add(sum(xs) == on[e, i])
    if A > 1:
        for a in range(1, A + 1):
            x = [X[e, i, a] for i in range(N)]
            for i in range(N):
                for s in (1, 2, 3):
                    if i + s + 1 < N: m.AddBoolOr([x[i]] + [x[i + k].Not() for k in range(1, s + 1)] + [x[i + s + 1]])
                    elif i + s < N: m.AddBoolOr([x[i]] + [x[i + k].Not() for k in range(1, s + 1)])
obj = []
for a in range(1, A + 1):
    for i in range(N):
        cov = sum(X[e, i, a] for e in E); m.Add(cov >= I['vmin'][a][i])
        y = m.NewIntVar(0, len(E), ''); m.Add(y >= cov - I['vmax'][a][i]); sq = m.NewIntVar(0, len(E) ** 2, ''); m.AddMultiplicationEquality(sq, [y, y]); obj.append(sq)
m.Minimize(sum(obj))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = secs; sv.parameters.num_workers = workers; sv.parameters.random_seed = 1
t0 = time.time(); st = sv.Solve(m); name = sv.StatusName(st); res = None
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<Solution>', '<ProblemFile>%s.ros</ProblemFile>' % stem, '<Penalty>%d</Penalty>' % int(sv.ObjectiveValue())]
    for e in E:
        out.append('<Employee ID="%s">' % e)
        for d in days:
            if (e, d) not in shift or not sv.Value(shift[e, d][0]): continue
            t = sv.Value(shift[e, d][1]); n = sv.Value(shift[e, d][2]); mm = (t + 24) % 96 * 15
            blocks = []
            for i in range(t, t + n):
                a = next(a for a in range(1, A + 1) if sv.Value(X[e, i, a]))
                if blocks and blocks[-1][0] == a: blocks[-1][1] += 15
                else: blocks.append([a, 15])
            out.append('<Shift><Day>%d</Day><Start>%02d:%02d:00</Start>%s</Shift>' % (d - 1, mm // 60, mm % 60, ''.join('<Task><ID>%d</ID><Length>%d</Length></Task>' % (a, l) for a, l in blocks)))
        out.append('</Employee>')
    out.append('</Solution>'); p = os.path.join(D, 'out', stem + '.cpsat.xml'); open(p, 'w').write('\n'.join(out) + '\n')
    S, _ = matsp.read_solution(open(p).read()); bad, pen = matsp.evaluate(I, S); res = (pen, len(bad), bad[:2])
print('%s best_known %s | CP-SAT %s objective %s bound %s | checker penalty, violations: %s | %.0fs' % (stem, best, name, int(sv.ObjectiveValue()) if res else None, int(sv.BestObjectiveBound()), res, time.time() - t0), flush=True)
