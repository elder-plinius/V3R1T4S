"""Split each record's penalty into a venue part (CA1, BR1, BR2, FA2: fixed once the home/away pattern is fixed) and an opponent part
(CA2, CA3, CA4, GA1, SE1). Written from the ITC2021 constraint definitions (Van Bulck et al. 2022). Self-check: venue + opponent must equal the
board's Best UB, and hard violations must be 0. Usage: python3 split.py -> data/split.json and a table."""
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
if __name__ == '__main__':
    board = json.load(open('data/board.json')); res = {}
    for o in board:
        nm = 'ITC2021_' + o['n'].replace(' ', '_'); import os
        if not os.path.exists('sol/%s.record.xml' % nm): continue
        v = evaluate('inst/%s.xml' % nm, 'sol/%s.record.xml' % nm); res[o['n']] = dict(v, ub=o['ub'], lb=o['lb'], ok=v['hard'] == 0 and v['venue'] + v['opp'] == o['ub'])
        print('%-10s UB %5d  venue %5d  opponent %5d  hard %d  %s  %s' % (o['n'], o['ub'], v['venue'], v['opp'], v['hard'], 'ok' if res[o['n']]['ok'] else 'MISMATCH', v['by']))
    json.dump(res, open('data/split.json', 'w'), indent=1)
    print('self-check ok on', sum(r['ok'] for r in res.values()), 'of', len(res))
