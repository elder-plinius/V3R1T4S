"""Fixed-pattern re-solve (Andy, 2026-11-25): keep a schedule's home/away pattern, re-optimise the opponents exactly with CP-SAT.
Modelled: every game slot (one game per team per slot, each directed pair once), phased seasons (each pair once per half), and the
opponent rules CA2, CA3, CA4, GA1, SE1 (hard as constraints, soft in the objective). Venue rules (CA1, BR1, BR2, FA2) are fixed by the
pattern. Warm start: the given schedule itself. Usage: python3 resolve.py <instance.xml> <schedule.xml> <seconds> <workers> <out.xml> [seed]
Prints one JSON line: status, objective (opponent penalty), bound."""
import sys, re, json, itertools, xml.etree.ElementTree as ET
from ortools.sat.python import cp_model
ids = lambda s: tuple(map(int, re.findall(r'\d+', s or '')))
inst, sol, SEC, WK, OUT = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]; SEED = int(sys.argv[6]) if len(sys.argv) > 6 else 1
r = ET.parse(inst).getroot(); n = len(r.findall('./Resources/Teams/team')); R = len(r.findall('./Resources/Slots/slot')); phased = r.findtext('.//gameMode') == 'P'
G0 = [(int(e.attrib['home']), int(e.attrib['away']), int(e.attrib['slot'])) for e in ET.parse(sol).findall('./Games/ScheduledMatch')]
H = [[0] * n for _ in range(R)]
for h, a, s in G0: H[s][h] = 1
m = cp_model.CpModel(); x = {}
for s in range(R):
    for i in range(n):
        for j in range(n):
            if i != j and H[s][i] and not H[s][j]: x[s, i, j] = m.NewBoolVar('')
for h, a, s in G0: m.AddHint(x[s, h, a], 1)
for (s, i, j), v in x.items():
    if (i, j, s) not in set(G0): pass
hint = {(s, h, a) for h, a, s in G0}
for k, v in x.items():
    if k not in hint: m.AddHint(v, 0)
for s in range(R):
    for t in range(n): m.AddExactlyOne([x[s, t, j] for j in range(n) if (s, t, j) in x] + [x[s, j, t] for j in range(n) if (s, j, t) in x])
for i in range(n):
    for j in range(n):
        if i != j: m.AddExactlyOne([x[s, i, j] for s in range(R) if (s, i, j) in x])
if phased:
    for i, j in itertools.combinations(range(n), 2):
        m.AddExactlyOne([x[s, i, j] for s in range(R // 2) if (s, i, j) in x] + [x[s, j, i] for s in range(R // 2) if (s, j, i) in x])
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
for e in r.find('Constraints').iter():
    a = e.attrib
    if 'type' not in a or e.tag in ('CA1', 'BR1', 'BR2', 'FA2'): continue
    k = e.tag; hard = a['type'] == 'HARD'; w = int(a['penalty']); lo = int(a.get('min', 0)); hi = int(a['max']) if 'max' in a else None
    if k == 'CA2':
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
m.Minimize(sum(obj))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = SEC; sv.parameters.num_workers = WK; sv.parameters.random_seed = SEED
st = sv.Solve(m); res = {'status': sv.StatusName(st), 'objective': None, 'bound': sv.BestObjectiveBound(), 'secs': round(sv.WallTime(), 1)}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    res['objective'] = int(round(sv.ObjectiveValue()))
    root = ET.Element('Solution'); md = ET.SubElement(root, 'MetaData'); ET.SubElement(md, 'InstanceName').text = r.findtext('.//InstanceName') or ''
    gs = ET.SubElement(root, 'Games')
    for (s, i, j), v in sorted(x.items()):
        if sv.Value(v): ET.SubElement(gs, 'ScheduledMatch', home=str(i), away=str(j), slot=str(s))
    ET.indent(root); ET.ElementTree(root).write(OUT, encoding='UTF-8', xml_declaration=True)
print(json.dumps(res))
