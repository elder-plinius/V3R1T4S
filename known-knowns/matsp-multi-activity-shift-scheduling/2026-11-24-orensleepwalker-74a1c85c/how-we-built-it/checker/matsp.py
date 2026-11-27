"""Multi-activity shift scheduling (Qu and Curtois) evaluator, standard library only, written from ProblemDefinition.pdf.
read_instance(txt) -> dict(h, tasks, staff {id: (min_minutes, max_minutes)}, vmin[a][i], vmax[a][i]) with intervals i = 0..h*96-1
  counted from 06:00 on calendar day 1 (cover lines are 'Day, HH:MM-HH:MM, TaskID, Min, Max' with calendar days from 1).
read_solution(xml) -> {employee id: [(calendar day, start minute of day, [(task id, minutes), ...]), ...]}
evaluate(I, S) -> (hard_violations list, penalty) where penalty = sum over intervals and activities of y^2, y = max(0, assigned - max),
  and the hard constraints are those of the definition:
  1 at most one shift per employee per calendar day; 2 shifts end within the horizon; 3 at least 14 h rest before a shift on the next
  calendar day; 4 total minutes within [min, max]; 5 at most 5 working days in any 6 consecutive calendar days; 6 no activity run of
  1-3 intervals bounded by intervals without that activity (literal pattern of the definition, i in 0..h*96); 7 activities only inside
  shifts, one per interval (implied by the format; overlapping shifts are reported); 8 assigned staff >= minimum demand everywhere.
  Shift rules: start at 00:00, 06:00-10:00, 14:00-18:00 or 20:00-23:45 (15-minute steps), never 00:00 on calendar day 1, only 00:00 on
  the last calendar day; length 6-10 h in 15-minute steps; task blocks in 15-minute steps."""
import re, xml.etree.ElementTree as ET

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
    vmin = {a: [0] * N for a in range(1, A + 1)}; vmax = {a: [0] * N for a in range(1, A + 1)}; seen = 0
    for l in sec['SECTION_COVER']:
        d, tm, a, mn, mx = [x.strip() for x in l.split(',')]; hh, mm = map(int, tm.split('-')[0].split(':'))
        i = (int(d) - 1) * 96 + hh * 4 + mm // 15 - 24
        assert 0 <= i < N, (l, i); vmin[int(a)][i] = int(mn); vmax[int(a)][i] = int(mx); seen += 1
    return dict(h=h, A=A, N=N, staff=staff, vmin=vmin, vmax=vmax, cover_lines=seen)

def read_solution(text):
    root = ET.fromstring(text); S = {}
    for emp in root.findall('Employee'):
        sh = []
        for s in emp.findall('Shift'):
            day = int(s.find('Day').text) + 1  # solution files count calendar days from 0, cover lines from 1
            hh, mm, ss = map(int, s.find('Start').text.strip().split(':'))
            tasks = [(int(t.find('ID').text), int(t.find('Length').text)) for t in s.findall('Task')]
            sh.append((day, hh * 60 + mm, tasks))
        S[emp.get('ID')] = sh
    pen = root.find('Penalty'); return S, (int(pen.text) if pen is not None else None)

def allowed_start(day, minute, h):
    if minute % 15: return False
    if day == 1 and minute == 0: return False
    if day == h + 1: return minute == 0
    return minute == 0 or 360 <= minute <= 600 or 840 <= minute <= 1080 or 1200 <= minute <= 1425

def evaluate(I, S):
    h, A, N = I['h'], I['A'], I['N']; bad = []; cnt = {a: [0] * N for a in range(1, A + 1)}
    if set(S) != set(I['staff']): bad.append('employee set differs from the instance')
    for e, shifts in S.items():
        days = [d for d, _, _ in shifts]
        if len(days) != len(set(days)): bad.append('%s: two shifts on one day' % e)
        byday = {}; total = 0; occ = [0] * N
        for d, st, tasks in shifts:
            if not (1 <= d <= h + 1): bad.append('%s: day %d outside' % (e, d)); continue
            if not allowed_start(d, st, h): bad.append('%s: start %d on day %d not allowed' % (e, st, d))
            L = sum(m for _, m in tasks)
            if L % 15 or not (360 <= L <= 600) or any(m <= 0 or m % 15 for _, m in tasks): bad.append('%s: day %d bad length or blocks %d' % (e, d, L))
            t0 = (d - 1) * 96 + st // 15 - 24; u = t0 + L // 15
            if t0 < 0 or u > N: bad.append('%s: day %d shift outside the horizon' % (e, d)); continue
            byday[d] = (t0, u); total += L; i = t0
            for a, m in tasks:
                if not (1 <= a <= A): bad.append('%s: unknown task %d' % (e, a))
                for _ in range(m // 15):
                    if occ[i]: bad.append('%s: overlap at interval %d' % (e, i))
                    occ[i] = a; i += 1
        b, c = I['staff'][e]
        if not (b <= total <= c): bad.append('%s: total %d outside [%d, %d]' % (e, total, b, c))
        for d in byday:
            if d + 1 in byday and byday[d][1] > byday[d + 1][0] - 56: bad.append('%s: rest < 14 h after day %d' % (e, d))
        for d in range(1, h + 2 - 5):
            if sum(1 for k in range(d, d + 6) if k in byday) > 5: bad.append('%s: more than 5 shifts in days %d-%d' % (e, d, d + 5))
        for a in range(1, A + 1):
            x = [1 if occ[i] == a else 0 for i in range(N)] + [0, 0, 0, 0, 0]
            for i in range(0, N):
                for s in (1, 2, 3):
                    if x[i] == 0 and all(x[i + k] for k in range(1, s + 1)) and x[i + s + 1] == 0: bad.append('%s: task %d run of %d intervals at %d' % (e, a, s, i + 1))
            for i in range(N):
                if occ[i] == a: cnt[a][i] += 1
    pen = 0
    for a in range(1, A + 1):
        for i in range(N):
            if cnt[a][i] < I['vmin'][a][i]: bad.append('cover below minimum: task %d interval %d (%d < %d)' % (a, i, cnt[a][i], I['vmin'][a][i]))
            y = max(0, cnt[a][i] - I['vmax'][a][i]); pen += y * y
    return bad, pen
