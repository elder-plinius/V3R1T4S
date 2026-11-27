"""Phase 2d: exact opponent assignment for Early 9 with the home/away pattern (HAP) fixed to a given schedule's, minimising every penalty
that is not a break (breaks are fixed by the HAP). Rules other than CA1/BR1/BR2 (HAP-only, already satisfied by the fixed HAP) are modelled:
CA2 hard, CA3 soft, GA1 hard and soft, FA2 soft (HAP-only: computed as a constant). Usage: python3 opponents.py <schedule.xml> <seconds> <workers> [cap|-] [out.xml]"""
import sys, re, xml.etree.ElementTree as ET
from ortools.sat.python import cp_model
ids = lambda s: tuple(map(int, re.findall(r'\d+', s or '')))
root = ET.parse('../2026-11-25-itc2021-early9/data/Early_9.instance.xml'); C = root.find('Constraints')
n = 18; R = 34; sol, SEC, WK = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); cap = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != '-' else None; OUT = sys.argv[5] if len(sys.argv) > 5 else None
H = [[0] * n for _ in range(R)]
for e in ET.parse(sol).findall('./Games/ScheduledMatch'): H[int(e.attrib['slot'])][int(e.attrib['home'])] = 1
m = cp_model.CpModel(); x = {}
for s in range(R):
    for i in range(n):
        for j in range(n):
            if i != j and H[s][i] and not H[s][j]: x[s, i, j] = m.NewBoolVar('')
G = lambda s, i, j: x.get((s, i, j))
for s in range(R):
    for t in range(n): m.AddExactlyOne([G(s, t, j) for j in range(n) if G(s, t, j) is not None] + [G(s, j, t) for j in range(n) if G(s, j, t) is not None])
for i in range(n):
    for j in range(n):
        if i != j: m.AddExactlyOne([G(s, i, j) for s in range(R) if G(s, i, j) is not None])
def games(i, group, slots, mode):
    out = []
    for s in slots:
        for j in group:
            if j == i: continue
            if mode in ('H', 'HA') and G(s, i, j) is not None: out.append(G(s, i, j))
            if mode in ('A', 'HA') and G(s, j, i) is not None: out.append(G(s, j, i))
    return out
obj = []; nrules = 0
for e in C.iter():
    a = e.attrib
    if 'type' not in a or e.tag in ('CA1', 'BR1', 'BR2', 'FA2'): continue
    hard = a['type'] == 'HARD'; w = int(a['penalty']); lo = int(a.get('min', 0)); hi = int(a.get('max', 10 ** 6))
    def rule(lits):
        global nrules
        nrules += 1; e_ = sum(lits)
        if hard: m.Add(e_ <= hi); m.Add(e_ >= lo); return
        over = m.NewIntVar(0, len(lits), ''); m.Add(over >= e_ - hi); under = m.NewIntVar(0, max(lo, 0), ''); m.Add(under >= lo - e_)
        obj.append(w * over); obj.append(w * under)
    if e.tag == 'CA2':
        for i in ids(a['teams1']): rule(games(i, ids(a['teams2']), ids(a['slots']), a['mode1']))
    elif e.tag == 'CA3':
        L = int(a['intp'])
        for i in ids(a['teams1']):
            for r0 in range(R - L + 1): rule(games(i, ids(a['teams2']), range(r0, r0 + L), a['mode1']))
    elif e.tag == 'GA1':
        p = ids(a['meetings']); rule([G(s, i, j) for s in ids(a['slots']) for i, j in zip(p[::2], p[1::2]) if G(s, i, j) is not None])
    else: raise SystemExit('unexpected ' + e.tag)
m.Minimize(sum(obj))
if cap is not None: m.Add(sum(obj) <= cap)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = SEC; sv.parameters.num_workers = WK; sv.parameters.random_seed = 1
st = sv.Solve(m); print('rules', nrules, 'vars', len(x), '| status', sv.StatusName(st), 'objective', sv.ObjectiveValue() if st in (2, 4) else None, 'bound', sv.BestObjectiveBound(), 'time %.0f' % sv.WallTime())
if OUT and st in (2, 4):
    r = ET.Element('Solution'); md = ET.SubElement(r, 'MetaData'); ET.SubElement(md, 'InstanceName').text = 'ITC2021 Early 9'
    gs = ET.SubElement(r, 'Games')
    for (s_, i, j), var in sorted(x.items()):
        if sv.Value(var): ET.SubElement(gs, 'ScheduledMatch', home=str(i), away=str(j), slot=str(s_))
    ET.indent(r); ET.ElementTree(r).write(OUT, encoding='UTF-8', xml_declaration=True); print('saved', OUT)
