"""Lead agent check (author evidence): for every warm-started win, (a) how many jobs' modes differ from the posted best-known
schedule it started from, and (b) the best makespan obtainable by re-timing the POSTED modes only (fixed-mode RCPSP solved by
CP-SAT, 60 s, 4 workers), i.e. what a 'local polish' of the published object can give. A win is not a mere polish if (b) cannot
reach the win's makespan."""
import json, sys, os, zipfile
from ortools.sat.python import cp_model
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(R, 'code')); import mm
W = json.load(open(os.path.join(R, 'data/selected_wins.json'))); Z = zipfile.ZipFile(os.path.join(R, 'data/MMplus.zip'))
posted = {}
for l in open(os.path.join(R, 'data/MMplus_2_BKS.csv'), encoding='utf-8-sig'):
    p = l.strip().split(';')
    if p[0].isdigit() and len(p) > 5:
        v = [int(x) for x in p[4:] if x]; k = len(v) // 2 - 1; posted[p[0]] = ([1] + v[:k] + [1], v[k:])
for i, w in W.items():
    if not w['warm_start']: continue
    I = mm.read(Z.read('MMplus/' + w['file']).decode()); n = I['n']; pm, ps = posted[i]
    diff = sum(a != b for a, b in zip(pm, w['modes']))
    m = cp_model.CpModel(); H = w['ub']; S = [m.NewIntVar(0, H, '') for _ in range(n)]; ivs = []
    d = [I['modes'][j][pm[j] - 1][0] for j in range(n)]; q = [I['modes'][j][pm[j] - 1][1] for j in range(n)]
    for j in range(n): ivs.append(m.NewIntervalVar(S[j], d[j], S[j] + d[j], ''))
    for k, c in enumerate(I['Rcap']): m.AddCumulative([ivs[j] for j in range(n) if q[j][k]], [q[j][k] for j in range(n) if q[j][k]], c)
    for j in range(n):
        for s in I['succ'][j]: m.Add(S[s] >= S[j] + d[j])
        m.AddHint(S[j], ps[j])
    m.Minimize(S[n - 1]); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 60; sv.parameters.num_workers = 4; st = sv.Solve(m)
    best = int(sv.ObjectiveValue()); bound = int(sv.BestObjectiveBound())
    verdict = 'not a polish (re-timing posted modes cannot reach %d)' % w['makespan'] if bound > w['makespan'] else ('POLISH REACHES IT' if best <= w['makespan'] else 'undecided')
    print('%s %-14s UB %d ours %d | modes changed %d of %d | posted modes re-timed: best %d, bound %d (%s) -> %s' % (i, w['file'], w['ub'], w['makespan'], diff, n - 2, best, bound, sv.StatusName(st), verdict), flush=True)
