"""Fix-and-optimise LNS for ITC2021 (Andy, 2026-11-26). One full CP-SAT model is built once; each iteration fixes everything outside a
neighbourhood to the current timetable (variable domains), caps the objective at the current value (equal-cost moves allowed), hints the
current solution and solves exactly within a short time limit.
Modes: fixed = home/away pattern of the start timetable fixed, objective = opponent rules (CA2, CA3, CA4, GA1, SE1);
       open  = venues free too, objective = all soft rules (adds CA1, BR1, BR2, FA2 on venue variables).
Neighbourhoods: 'slots' (k consecutive slots free), 'teams' (all games of a set of teams free) and, every 25th iteration, 'global' (everything free, 45 s); window sizes adapt (grow after a proven-optimal
window without gain, shrink after an unresolved one).
Usage: python3 lns.py <instance.xml> <start.xml> <mode> <seconds> <out_prefix> <seed> [validate]
Writes <out_prefix>.state.xml (final timetable), <out_prefix>.best.xml (if it improved on the start), <out_prefix>.json (summary) and
<out_prefix>.log.jsonl (one line per iteration)."""
import sys, re, json, time, random, itertools, xml.etree.ElementTree as ET
from ortools.sat.python import cp_model
ids = lambda s: tuple(map(int, re.findall(r'\d+', s or '')))
inst, start, MODE, SEC, PFX, SEED = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5], int(sys.argv[6]); VALIDATE = len(sys.argv) > 7
T0 = time.time(); rng = random.Random(SEED)
r = ET.parse(inst).getroot(); n = len(r.findall('./Resources/Teams/team')); R = len(r.findall('./Resources/Slots/slot')); phased = r.findtext('.//gameMode') == 'P'
G0 = [(int(e.attrib['home']), int(e.attrib['away']), int(e.attrib['slot'])) for e in ET.parse(start).findall('./Games/ScheduledMatch')]
H0 = [[0] * n for _ in range(R)]
for h, a, s in G0: H0[s][h] = 1
m = cp_model.CpModel(); x = {}; hv = {}
for s in range(R):
    for i in range(n):
        for j in range(n):
            if i != j and (MODE == 'open' or (H0[s][i] and not H0[s][j])): x[s, i, j] = m.NewBoolVar('')
for s in range(R):
    for t in range(n):
        m.AddExactlyOne([x[s, t, j] for j in range(n) if (s, t, j) in x] + [x[s, j, t] for j in range(n) if (s, j, t) in x])
for i in range(n):
    for j in range(n):
        if i != j: m.AddExactlyOne([x[s, i, j] for s in range(R) if (s, i, j) in x])
if phased:
    for i, j in itertools.combinations(range(n), 2):
        m.AddExactlyOne([x[s, i, j] for s in range(R // 2) if (s, i, j) in x] + [x[s, j, i] for s in range(R // 2) if (s, j, i) in x])
if MODE == 'open':
    for t in range(n):
        for s in range(R):
            hv[t, s] = m.NewBoolVar(''); m.Add(hv[t, s] == sum(x[s, t, j] for j in range(n) if (s, t, j) in x))
    br = {}
    for t in range(n):
        for s in range(1, R):
            b = m.NewBoolVar(''); m.Add(hv[t, s] == hv[t, s - 1]).OnlyEnforceIf(b); m.Add(hv[t, s] != hv[t, s - 1]).OnlyEnforceIf(b.Not()); br[t, s] = b
def games(t, group, slots, mode):
    out = []
    for s in slots:
        for j in group:
            if j == t: continue
            if mode in ('H', 'HA') and (s, t, j) in x: out.append(x[s, t, j])
            if mode in ('A', 'HA') and (s, j, t) in x: out.append(x[s, j, t])
    return out
obj = []
def rule(expr, nmax, lo, hi, hard, w):
    if hard:
        if hi is not None: m.Add(expr <= hi)
        if lo: m.Add(expr >= lo)
        return
    if hi is not None and nmax > hi:
        o = m.NewIntVar(0, nmax, ''); m.Add(o >= expr - hi); obj.append(w * o)
    if lo:
        u = m.NewIntVar(0, lo, ''); m.Add(u >= lo - expr); obj.append(w * u)
VENUE = ('CA1', 'BR1', 'BR2', 'FA2')
for e in r.find('Constraints').iter():
    a = e.attrib
    if 'type' not in a: continue
    k = e.tag; hard = a['type'] == 'HARD'; w = int(a['penalty']); lo = int(a.get('min', 0)); hi = int(a['max']) if 'max' in a else None
    if k in VENUE and MODE == 'fixed': continue
    if k == 'CA1':
        for t in ids(a['teams']):
            sl = ids(a['slots']); L = [hv[t, s] if a['mode'] == 'H' else 1 - hv[t, s] for s in sl]; rule(sum(L), len(L), lo, hi, hard, w)
    elif k == 'BR1':
        mx = int(a['intp']); sl = [s for s in ids(a['slots']) if s > 0]
        for t in ids(a['teams']): rule(sum(br[t, s] for s in sl), len(sl), 0, mx, hard, w)
    elif k == 'BR2':
        L = [br[t, s] for t in ids(a['teams']) for s in ids(a['slots']) if s > 0]; rule(sum(L), len(L), 0, int(a['intp']), hard, w)
    elif k == 'FA2':
        T = ids(a['teams']); sl = sorted(ids(a['slots'])); ip = int(a['intp'])
        for t, u in itertools.combinations(T, 2):
            d = m.NewIntVar(0, R, '')
            for s in sl:
                diff = sum(hv[t, q] for q in range(s + 1)) - sum(hv[u, q] for q in range(s + 1))
                m.Add(d >= diff - ip); m.Add(d >= -diff - ip)
            if hard: m.Add(d == 0)
            else: obj.append(w * d)
    elif k == 'CA2':
        for t in ids(a['teams1']): L = games(t, set(ids(a['teams2'])), set(ids(a['slots'])), a['mode1']); rule(sum(L), len(L), lo, hi, hard, w)
    elif k == 'CA3':
        Lw = int(a['intp'])
        for t in ids(a['teams1']):
            for s0 in range(R - Lw + 1): L = games(t, set(ids(a['teams2'])), set(range(s0, s0 + Lw)), a['mode1']); rule(sum(L), len(L), lo, hi, hard, w)
    elif k == 'CA4':
        T1, T2 = ids(a['teams1']), set(ids(a['teams2'])); sl = ids(a['slots'])
        for g in ([set(sl)] if a['mode2'] == 'GLOBAL' else [{s} for s in sl]):
            L = [v for t in T1 for v in games(t, T2, g, a['mode1'])]; rule(sum(L), len(L), lo, hi, hard, w)
    elif k == 'GA1':
        p = ids(a['meetings']); sl = set(ids(a['slots'])); L = [x[s, i, j] for i, j in zip(p[::2], p[1::2]) for s in sl if (s, i, j) in x]
        rule(sum(L), len(L), lo, hi, hard, w)
    elif k == 'SE1':
        mn = int(a['min'])
        for i, j in itertools.combinations(ids(a['teams']), 2):
            S1 = sum(s * x[s, i, j] for s in range(R) if (s, i, j) in x); S2 = sum(s * x[s, j, i] for s in range(R) if (s, j, i) in x)
            d = m.NewIntVar(-R, R, ''); m.Add(d == S1 - S2); ad = m.NewIntVar(0, R, ''); m.AddAbsEquality(ad, d)
            if hard: m.Add(ad - 1 >= mn)
            else: dev = m.NewIntVar(0, mn, ''); m.Add(dev >= mn - (ad - 1)); obj.append(w * dev)
    else: raise SystemExit('unknown ' + k)
UBT = 10 ** 7; total = m.NewIntVar(0, UBT, 'total'); m.Add(total == sum(obj)); m.Minimize(total)
NV = len(m.proto.variables); TI = total.Index()
xi = {k: v.Index() for k, v in x.items()}; hi_ = {k: v.Index() for k, v in hv.items()}
cur0 = {(s, h, a) for h, a, s in G0}
def solve(fix, cap, hint, secs, workers=6):
    mm = m.clone(); p = mm.proto
    for idx, val in fix.items(): d = p.variables[idx].domain; d[0] = val; d[1] = val
    d = p.variables[TI].domain; d[1] = cap
    if hint is not None: p.solution_hint.vars.extend(list(range(NV))); p.solution_hint.values.extend(list(hint))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = secs; sv.parameters.num_workers = workers; sv.parameters.random_seed = rng.randrange(10 ** 6)
    st = sv.Solve(mm); return st, (list(sv.ResponseProto().solution) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None), sv
# full assignment of the start timetable
fix0 = {idx: (1 if k in cur0 else 0) for k, idx in xi.items()}
st, sol, sv = solve(fix0, UBT, None, 120)
if sol is None: print(json.dumps({'error': 'start timetable infeasible in the model', 'status': sv.StatusName(st)})); sys.exit(2)
cur = sol; cv = cur[TI]; start_val = cv; best = cv
if VALIDATE: print(json.dumps({'start_objective': cv, 'n': n, 'R': R, 'mode': MODE, 'vars': NV, 'build_secs': round(time.time() - T0, 1)})); sys.exit(0)
def write(sol, path):
    root = ET.Element('Solution'); md = ET.SubElement(root, 'MetaData'); ET.SubElement(md, 'InstanceName').text = r.findtext('.//InstanceName') or ''
    gs = ET.SubElement(root, 'Games')
    for (s, i, j), idx in sorted(xi.items()):
        if sol[idx]: ET.SubElement(gs, 'ScheduledMatch', home=str(i), away=str(j), slot=str(s))
    ET.indent(root); ET.ElementTree(root).write(path, encoding='UTF-8', xml_declaration=True)
size = {'slots': 3, 'teams': 3}; lim = {'slots': (2, max(3, R // 2)), 'teams': (2, max(3, n - 2))}
stats = dict(iterations=0, optimal=0, unresolved=0, improved=0, plateau_moves=0)
LOG = open(PFX + '.log.jsonl', 'w'); deadline = T0 + SEC
while time.time() < deadline - 2:
    kind = 'global' if stats['iterations'] % 25 == 0 else rng.choice(['slots', 'teams']); k = size.get(kind, 0)
    if kind == 'global':
        free = set(xi); freeh = set(hi_)
    elif kind == 'slots':
        s0 = rng.randrange(0, R - k + 1); W = set(range(s0, s0 + k)); free = {key for key in xi if key[0] in W}; freeh = {key for key in hi_ if key[1] in W}
    else:
        T = set(rng.sample(range(n), k)); free = {key for key in xi if key[1] in T or key[2] in T}; freeh = {key for key in hi_ if key[0] in T}
    fix = {idx: cur[idx] for key, idx in xi.items() if key not in free}
    fix.update({idx: cur[idx] for key, idx in hi_.items() if key not in freeh})
    secs = min(45.0 if kind == 'global' else 15.0, max(1.0, deadline - time.time() - 1))
    st, sol, sv = solve(fix, cv, cur, secs)
    stats['iterations'] += 1; opt = st == cp_model.OPTIMAL; stats['optimal' if opt else 'unresolved'] += 1
    moved = False; nv = cv
    if sol is not None:
        nv = sol[TI]; changed = any(sol[idx] != cur[idx] for idx in xi.values())
        if nv < cv: stats['improved'] += 1
        elif changed: stats['plateau_moves'] += 1
        if nv < cv or changed: cur = sol; moved = True
        if nv < best: best = nv; write(cur, PFX + '.best.xml')
        cv = cur[TI]
    if kind != 'global':
        if opt and nv >= cv: size[kind] = min(lim[kind][1], size[kind] + 1)
        elif not opt: size[kind] = max(lim[kind][0], size[kind] - 1)
    LOG.write(json.dumps(dict(t=round(time.time() - T0, 1), kind=kind, k=k, status=sv.StatusName(st), value=cv, moved=moved)) + '\n'); LOG.flush()
write(cur, PFX + '.state.xml')
res = dict(mode=MODE, start=start_val, final=cv, best=best, secs=round(time.time() - T0), **stats)
res['unresolved_share'] = round(stats['unresolved'] / max(1, stats['iterations']), 3)
json.dump(res, open(PFX + '.json', 'w')); print(json.dumps(res))
