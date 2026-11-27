"""Independent ITC2021 evaluator (Python standard library only), written from the ITC2021 constraint definitions without RobinX's code.
Usage: python3 verify.py <instance.xml> <timetable.xml> <best UB> -> prints the structure check, hard violations, penalty (venue + opponent
parts, per rule) and PASS if the timetable is a valid compact double round robin with 0 hard violations and a penalty strictly below <best UB>.
It reproduces the posted Best UB of all 42 open ITC2021 records exactly (the authors' check)."""
import sys
import re, json, itertools, xml.etree.ElementTree as ET
ids = lambda s: tuple(map(int, re.findall(r'\d+', s or '')))
VENUE = {'CA1', 'BR1', 'BR2', 'FA2'}
def load(inst, sol):
    r = ET.parse(inst).getroot(); n = len(r.findall('./Resources/Teams/team')); R = len(r.findall('./Resources/Slots/slot'))
    G = [(int(e.attrib['home']), int(e.attrib['away']), int(e.attrib['slot'])) for e in ET.parse(sol).findall('./Games/ScheduledMatch')]
    H = [[None] * n for _ in range(R)]
    for h, a, s in G: H[s][h] = 1; H[s][a] = 0
    return r, n, R, G, H
def evaluate(inst, sol):
    r, n, R, G, H = load(inst, sol); at = {(h, a): s for h, a, s in G}; out = {'hard': 0, 'venue': 0, 'opp': 0, 'by': {}}
    def games(team, group, slots, mode):
        c = 0
        for h, a, s in G:
            if s not in slots: continue
            if mode in ('H', 'HA') and h == team and a in group: c += 1
            if mode in ('A', 'HA') and a == team and h in group: c += 1
        return c
    def brk(t, s, mode):
        if s == 0 or H[s][t] != H[s - 1][t]: return 0
        return 1 if mode == 'HA' or (mode == 'H') == (H[s][t] == 1) else 0
    for e in r.find('Constraints').iter():
        a = e.attrib
        if 'type' not in a: continue
        k = e.tag; w = int(a['penalty']); lo = int(a.get('min', 0)); hi = int(a['max']) if 'max' in a else None
        dev = lambda c, lo_, hi_: max(0, lo_ - c) + (max(0, c - hi_) if hi_ is not None else 0)
        d = 0
        if k == 'CA1':
            for t in ids(a['teams']): d += dev(games(t, set(range(n)), set(ids(a['slots'])), a['mode']), lo, hi)
        elif k == 'CA2':
            for t in ids(a['teams1']): d += dev(games(t, set(ids(a['teams2'])), set(ids(a['slots'])), a['mode1']), lo, hi)
        elif k == 'CA3':
            L = int(a['intp'])
            for t in ids(a['teams1']):
                for s0 in range(R - L + 1): d += dev(games(t, set(ids(a['teams2'])), set(range(s0, s0 + L)), a['mode1']), lo, hi)
        elif k == 'CA4':
            T1, T2 = ids(a['teams1']), set(ids(a['teams2'])); sl = ids(a['slots'])
            groups = [set(sl)] if a['mode2'] == 'GLOBAL' else [{s} for s in sl]
            for g in groups: d += dev(sum(games(t, T2, g, a['mode1']) for t in T1), lo, hi)
        elif k == 'GA1':
            m = ids(a['meetings']); sl = set(ids(a['slots'])); d += dev(sum(1 for i, j in zip(m[::2], m[1::2]) if at.get((i, j)) in sl), lo, hi)
        elif k == 'BR1':
            sl = ids(a['slots'])
            for t in ids(a['teams']): d += max(0, sum(brk(t, s, a['mode2']) for s in sl) - int(a['intp']))
        elif k == 'BR2':
            d += max(0, sum(brk(t, s, 'HA') for t in ids(a['teams']) for s in ids(a['slots'])) - int(a['intp']))
        elif k == 'FA2':
            T = ids(a['teams']); sl = sorted(ids(a['slots'])); cum = {t: [0] * R for t in T}
            for t in T:
                c = 0
                for s in range(R): c += 1 if H[s][t] == 1 else 0; cum[t][s] = c
            for t, u in itertools.combinations(T, 2): d += max([0] + [abs(cum[t][s] - cum[u][s]) - int(a['intp']) for s in sl])
        elif k == 'SE1':
            T = ids(a['teams'])
            for t, u in itertools.combinations(T, 2):
                s1, s2 = at[(t, u)], at[(u, t)]; d += max(0, int(a['min']) - (abs(s1 - s2) - 1))
        else: raise SystemExit('unknown ' + k)
        if a['type'] == 'HARD': out['hard'] += d
        else:
            out['venue' if k in VENUE else 'opp'] += w * d; out['by'][k] = out['by'].get(k, 0) + w * d
    return out

def structure(inst, sol):
    """Independent structure check: compact double round robin (n even, 2(n-1) slots): every team plays exactly once per slot, every ordered
    pair meets exactly once, phased instances: every pair meets once in each half. Returns a list of problems (empty = valid)."""
    ir = ET.parse(inst).getroot(); n = len(ir.findall('./Resources/Teams/team')); R = len(ir.findall('./Resources/Slots/slot')); phased = ir.findtext('.//gameMode') == 'P'
    G = [(int(e.attrib['home']), int(e.attrib['away']), int(e.attrib['slot'])) for e in ET.parse(sol).findall('./Games/ScheduledMatch')]
    out = []
    if R != 2 * (n - 1): out.append('slot count')
    per = {}
    for h, a, s in G:
        if not (0 <= h < n and 0 <= a < n and h != a and 0 <= s < R): out.append('bad game %s' % ((h, a, s),)); continue
        for t in (h, a): per[t, s] = per.get((t, s), 0) + 1
    if any(per.get((t, s), 0) != 1 for t in range(n) for s in range(R)): out.append('a team does not play exactly once in some slot')
    pairs = {}
    for h, a, s in G: pairs[h, a] = pairs.get((h, a), 0) + 1
    if any(pairs.get((i, j), 0) != 1 for i in range(n) for j in range(n) if i != j): out.append('an ordered pair does not meet exactly once')
    if phased:
        half = {}
        for h, a, s in G:
            if s < R // 2: k = (min(h, a), max(h, a)); half[k] = half.get(k, 0) + 1
        if any(half.get((i, j), 0) != 1 for i in range(n) for j in range(i + 1, n)): out.append('phased: a pair does not meet exactly once in the first half')
    return out

if __name__ == '__main__':
    inst, sol, ub = sys.argv[1], sys.argv[2], int(sys.argv[3])
    s = structure(inst, sol)
    if s: print('structure: INVALID', s); print('FAIL'); sys.exit(1)
    v = evaluate(inst, sol); pen = v['venue'] + v['opp']
    print('structure: valid compact double round robin; hard violations %d; penalty %d (venue %d + opponent %d) %s; best UB %d' % (v['hard'], pen, v['venue'], v['opp'], v['by'], ub))
    ok = v['hard'] == 0 and pen < ub; print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
