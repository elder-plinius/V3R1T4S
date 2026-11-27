"""Break-count lower bound for an ITC2021 instance, Python standard library only (Andy, 2026-11-27).
Argument (every step holds for every feasible timetable of a compact double round robin with n teams, n even, 2(n-1) slots):
 1. Each team plays n-1 home games; a break at slot s > 0 means the same venue as at slot s-1.
 2. For each team separately, its own HARD venue rules (CA1 with mode H or A, BR1, and venues forced by HARD GA1 rules that require one listed
    game in one slot) allow no pattern with fewer than f_t breaks (found by exhaustive search over patterns with 0, 1, 2, ... breaks).
 3. A pattern with 0 breaks is HAHA... or AHAH...; two teams with the same pattern can never meet, so at most one team uses each, and only
    teams whose rules allow that pattern.
 4. In every slot the teams that break split evenly between home-home and away-away (the number of home teams is n/2 in consecutive slots),
    so the total number of breaks is even.
 So total breaks >= min over the choice of the (at most two) zero-break teams of sum over the other teams of max(1, f_t), rounded up to even.
 With a soft BR2 rule over all teams and slots (max intp, penalty w), the penalty is at least w * max(0, total - intp).
Usage: python3 break_floor_stdlib.py <instance.xml> -> prints the team floors, the break bound and the penalty bound."""
import sys, re, xml.etree.ElementTree as ET
ids = lambda s: tuple(map(int, re.findall(r'\d+', s or '')))
r = ET.parse(sys.argv[1]).getroot(); n = len(r.findall('./Resources/Teams/team')); R = len(r.findall('./Resources/Slots/slot')); C = r.find('Constraints')
assert R == 2 * (n - 1) and n % 2 == 0
ca1 = {t: [] for t in range(n)}; br1 = {t: [] for t in range(n)}; forced = {t: {} for t in range(n)}
for e in C.iter():
    a = e.attrib
    if a.get('type') != 'HARD': continue
    if e.tag == 'CA1':
        assert a['mode'] in ('H', 'A')
        for t in ids(a['teams']): ca1[t].append((set(ids(a['slots'])), 1 if a['mode'] == 'H' else 0, int(a.get('min', 0)), int(a['max'])))
    elif e.tag == 'BR1':
        assert a['mode2'] == 'HA'
        for t in ids(a['teams']): br1[t].append((set(ids(a['slots'])), int(a['intp'])))
    elif e.tag == 'GA1':
        p = ids(a['meetings']); sl = ids(a['slots'])
        if len(p) == 2 and len(sl) == 1 and int(a.get('min', 0)) >= 1: forced[p[0]][sl[0]] = 1; forced[p[1]][sl[0]] = 0
def exists(t, B, start=None):
    """Is there a pattern for team t with exactly B breaks satisfying its hard venue rules (and the given first venue)?"""
    seq = []
    def ok():
        k = len(seq); s = k - 1
        if s in forced[t] and seq[s] != forced[t][s]: return False
        if sum(seq) > n - 1 or k - sum(seq) > n - 1: return False
        for sl, v, lo, hi in ca1[t]:
            c = sum(1 for x in sl if x < k and seq[x] == v)
            if c > hi or c + sum(1 for x in sl if x >= k) < lo: return False
        for sl, mx in br1[t]:
            if sum(1 for x in sl if 0 < x < k and seq[x] == seq[x - 1]) > mx: return False
        return True
    def rec(b):
        if len(seq) == R: return b == B
        for v in ((start,) if not seq and start is not None else (0, 1)):
            nb = b + (1 if seq and seq[-1] == v else 0)
            if nb > B or (R - len(seq) - 1) < 0: continue
            seq.append(v)
            if ok() and rec(nb): seq.pop(); return True
            seq.pop()
        return False
    return rec(0)
floor = []
for t in range(n):
    B = 0
    while not exists(t, B): B += 1
    floor.append(B)
zh = [exists(t, 0, 1) for t in range(n)]; za = [exists(t, 0, 0) for t in range(n)]
best = None
for th in [None] + [t for t in range(n) if zh[t]]:
    for ta in [None] + [t for t in range(n) if za[t]]:
        if th is not None and th == ta: continue
        tot = sum(0 if t in (th, ta) else max(1, floor[t]) for t in range(n)); best = tot if best is None else min(best, tot)
even = best + best % 2
pen = 0
for e in C.iter():
    a = e.attrib
    if e.tag == 'BR2' and a.get('type') == 'SOFT' and len(ids(a['teams'])) == n and set(ids(a['slots'])) >= set(range(1, R)):
        pen += int(a['penalty']) * max(0, even - int(a['intp']))
print('team break floors:', floor); print('teams allowed the zero-break pattern starting home / away:', sum(zh), '/', sum(za))
print('total breaks >= %d, even -> %d; penalty lower bound from BR2: %d' % (best, even, pen))
