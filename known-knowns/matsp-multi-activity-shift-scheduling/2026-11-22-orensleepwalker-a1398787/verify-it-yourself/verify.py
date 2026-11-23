"""Standalone verifier for a shift-scheduling record claim (Python standard library only).
Usage: python3 verify_claim.py <instance .txt file> <solution .xml file> <record value>
Checks, from the instance file and the formal definition (ProblemDefinition.pdf of schedulingbenchmarks.org/matsp):
one shift per employee per calendar day; allowed start times (00:00, 06:00-10:00, 14:00-18:00, 20:00-23:45 in 15-minute steps; no
00:00 on the first calendar day; only 00:00 on the last); shift length 6-10 h in 15-minute steps; shifts inside the horizon; 14 h rest
before a shift on the next calendar day; each employee's total minutes within [min, max]; at most 5 working days in any 6 consecutive
calendar days; no run of 1-3 intervals of one task (the definition's literal pattern); one task per on-duty interval; cover at least
the minimum for every task and interval. Penalty = sum over tasks and intervals of max(0, cover - max)^2.
Solution files count calendar days from 0 (as the site's example file); cover lines count them from 1.
Prints the violations (if any), the penalty, and PASS if there are no violations and the penalty is strictly below the record."""
import sys, xml.etree.ElementTree as ET

def read_instance(text):
    sec = {}; cur = None
    for raw in text.splitlines():
        l = raw.strip()
        if not l or l.startswith('#'): continue
        if l.startswith('SECTION_'): cur = l; sec[cur] = []; continue
        sec[cur].append(l)
    h = int(sec['SECTION_HORIZON'][0]); A = int(sec['SECTION_TASKS'][0]); N = h * 96
    staff = {}
    for l in sec['SECTION_STAFF']:
        e, b, c = [x.strip() for x in l.split(',')]; staff[e] = (int(b), int(c))
    vmin = {a: [0] * N for a in range(1, A + 1)}; vmax = {a: [0] * N for a in range(1, A + 1)}
    for l in sec['SECTION_COVER']:
        d, tm, a, mn, mx = [x.strip() for x in l.split(',')]; hh, mm = map(int, tm.split('-')[0].split(':'))
        i = (int(d) - 1) * 96 + hh * 4 + mm // 15 - 24; vmin[int(a)][i] = int(mn); vmax[int(a)][i] = int(mx)
    return h, A, N, staff, vmin, vmax

def allowed(day, minute, h):
    if minute % 15 or (day == 1 and minute == 0): return False
    if day == h + 1: return minute == 0
    return minute == 0 or 360 <= minute <= 600 or 840 <= minute <= 1080 or 1200 <= minute <= 1425

def main(inst, sol, record):
    h, A, N, staff, vmin, vmax = read_instance(open(inst).read()); bad = []; cnt = {a: [0] * N for a in range(1, A + 1)}
    root = ET.fromstring(open(sol).read()); emps = {e.get('ID'): e for e in root.findall('Employee')}
    if set(emps) != set(staff): bad.append('employee set differs from the instance')
    for e, node in emps.items():
        occ = [0] * N; total = 0; byday = {}
        for s in node.findall('Shift'):
            d = int(s.find('Day').text) + 1; hh, mm, _ = map(int, s.find('Start').text.strip().split(':')); st = hh * 60 + mm
            tasks = [(int(t.find('ID').text), int(t.find('Length').text)) for t in s.findall('Task')]; L = sum(m for _, m in tasks)
            if d in byday: bad.append('%s: two shifts on calendar day %d' % (e, d))
            if not (1 <= d <= h + 1) or not allowed(d, st, h): bad.append('%s: start not allowed on day %d' % (e, d)); continue
            if L % 15 or not (360 <= L <= 600) or any(m <= 0 or m % 15 or not 1 <= a <= A for a, m in tasks): bad.append('%s: bad shift length or task block on day %d' % (e, d))
            t0 = (d - 1) * 96 + st // 15 - 24; u = t0 + L // 15
            if t0 < 0 or u > N: bad.append('%s: shift outside the horizon on day %d' % (e, d)); continue
            byday[d] = (t0, u); total += L; i = t0
            for a, m in tasks:
                for _ in range(m // 15):
                    if occ[i]: bad.append('%s: overlap at interval %d' % (e, i))
                    occ[i] = a; i += 1
        b, c = staff[e]
        if not b <= total <= c: bad.append('%s: total minutes %d outside [%d, %d]' % (e, total, b, c))
        for d in byday:
            if d + 1 in byday and byday[d][1] > byday[d + 1][0] - 56: bad.append('%s: less than 14 h rest after day %d' % (e, d))
        for d in range(1, h + 2 - 5):
            if sum(1 for k in range(d, d + 6) if k in byday) > 5: bad.append('%s: more than 5 working days in days %d-%d' % (e, d, d + 5))
        for a in range(1, A + 1):
            x = [1 if occ[i] == a else 0 for i in range(N)] + [0] * 5
            for i in range(N):
                for s in (1, 2, 3):
                    if x[i] == 0 and all(x[i + k] for k in range(1, s + 1)) and x[i + s + 1] == 0: bad.append('%s: task %d run of %d intervals' % (e, a, s))
            for i in range(N):
                if occ[i] == a: cnt[a][i] += 1
    pen = 0
    for a in range(1, A + 1):
        for i in range(N):
            if cnt[a][i] < vmin[a][i]: bad.append('cover below minimum: task %d interval %d' % (a, i))
            pen += max(0, cnt[a][i] - vmax[a][i]) ** 2
    for v in bad[:20]: print('VIOLATION', v)
    print('violations %d, penalty %d, record %d' % (len(bad), pen, record))
    ok = not bad and pen < record; print('PASS' if ok else 'FAIL'); return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], int(sys.argv[3])))
