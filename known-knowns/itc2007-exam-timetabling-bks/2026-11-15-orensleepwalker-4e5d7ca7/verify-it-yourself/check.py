"""Independent ITC-2007 examination-track checker (written from the track specification).
Usage: python3 -I check.py <instance.exam> <solution.sol>   -> prints a JSON line.
Hard: no student in two exams in one period; room capacity per period; exam duration <= period duration;
period constraints (EXAM_COINCIDENCE same period, EXCLUSION different periods, AFTER: first strictly later than second);
ROOM_EXCLUSIVE (exam alone in its room and period).
Soft (per student, per pair of that student's exams): two in a row (same day, adjacent periods) x w2r; two in a day
(same day, not adjacent) x w2d; period spread (0 < period distance <= spread) x 1; non-mixed durations: per room and
period (distinct durations - 1) x wnmd; front load: each of the 'a' largest exams placed in the last 'b' periods x wfl;
plus the period penalty and room penalty of every exam."""
import sys, json, collections, itertools

def parse_instance(path):
    sec = None; exams = []; periods = []; rooms = []; phc = []; rhc = []; w = {}
    for raw in open(path):
        line = raw.strip()
        if not line: continue
        if line.startswith('['):
            sec = line.strip('[]').split(':')[0]; continue
        parts = [p.strip() for p in line.split(',') if p.strip() != '']
        if sec == 'Exams':
            exams.append((int(parts[0]), [int(x) for x in parts[1:]]))
        elif sec == 'Periods':
            periods.append((parts[0], parts[1], int(parts[2]), int(parts[3])))
        elif sec == 'Rooms':
            rooms.append((int(parts[0]), int(parts[1])))
        elif sec == 'PeriodHardConstraints':
            phc.append((int(parts[0]), parts[1], int(parts[2])))
        elif sec == 'RoomHardConstraints':
            rhc.append((int(parts[0]), parts[1]))
        elif sec == 'InstitutionalWeightings':
            w[parts[0]] = [int(x) for x in parts[1:]]
    return exams, periods, rooms, phc, rhc, w

def parse_solution(path):
    out = []
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith('{') or line.startswith('#'): continue  # some posted files carry a JSON header line
        p, r = [int(x.strip()) for x in line.split(',')[:2]]
        out.append((p, r))
    return out

def evaluate(inst_path, sol_path):
    exams, periods, rooms, phc, rhc, w = parse_instance(inst_path)
    sol = parse_solution(sol_path)
    hard = collections.Counter(); notes = []
    if len(sol) != len(exams):
        return dict(feasible=False, error='solution has %d lines for %d exams' % (len(sol), len(exams)))
    P = len(periods); R = len(rooms)
    for e, (p, r) in enumerate(sol):
        if not (0 <= p < P and 0 <= r < R): hard['index'] += 1
    if hard['index']:  # fix 2026-11-15 (claim run 2026-11-15-0303, contrarian lens): reject instead of crashing
        return dict(feasible=False, hard=dict(hard), error='period or room index out of range')
    day = [periods[p][0] for p in range(P)]
    # day position: periods are given in time order; adjacency = same day and consecutive indices
    size = [len(set(s)) for _, s in exams]
    # student conflicts and per-student pairs
    by_student = collections.defaultdict(list)
    for e, (_, studs) in enumerate(exams):
        for s in set(studs): by_student[s].append(e)
    two_row = two_day = spread = 0; g = w.get('PERIODSPREAD', [0])[0]
    for s, es in by_student.items():
        for a, b in itertools.combinations(es, 2):
            pa, pb = sol[a][0], sol[b][0]
            if pa == pb: hard['conflict'] += 1; continue
            d = abs(pa - pb)
            if day[pa] == day[pb]:
                if d == 1: two_row += 1
                else: two_day += 1
            if d <= g: spread += 1
    # rooms: capacity, mixed durations, exclusivity
    occ = collections.defaultdict(list)
    for e, (p, r) in enumerate(sol): occ[(p, r)].append(e)
    nmd = 0
    for (p, r), es in occ.items():
        if sum(size[e] for e in es) > rooms[r][0]: hard['room_capacity'] += 1
        nmd += len({exams[e][0] for e in es}) - 1
    for e, (p, r) in enumerate(sol):
        if exams[e][0] > periods[p][2]: hard['period_duration'] += 1
    for a, typ, b in phc:
        pa, pb = sol[a][0], sol[b][0]
        if typ == 'EXAM_COINCIDENCE' and pa != pb: hard['coincidence'] += 1
        elif typ == 'EXCLUSION' and pa == pb: hard['exclusion'] += 1
        elif typ == 'AFTER' and not (pa > pb): hard['after'] += 1
    for e, typ in rhc:
        if typ == 'ROOM_EXCLUSIVE' and len(occ[sol[e]]) > 1: hard['room_exclusive'] += 1
    fl_a, fl_b, fl_w = (w.get('FRONTLOAD', [0, 0, 0]) + [0, 0, 0])[:3]
    largest = sorted(range(len(exams)), key=lambda e: (-size[e], e))[:fl_a]
    front = sum(1 for e in largest if sol[e][0] >= P - fl_b)
    ppen = sum(periods[p][3] for p, _ in sol); rpen = sum(rooms[r][1] for _, r in sol)
    comp = dict(two_in_a_row=two_row * w.get('TWOINAROW', [0])[0], two_in_a_day=two_day * w.get('TWOINADAY', [0])[0],
                period_spread=spread, non_mixed_durations=nmd * w.get('NONMIXEDDURATIONS', [0])[0],
                front_load=front * fl_w, period_penalty=ppen, room_penalty=rpen)
    return dict(feasible=sum(hard.values()) == 0, hard=dict(hard), total=sum(comp.values()), components=comp,
                exams=len(exams), periods=P, rooms=R)

if __name__ == '__main__':
    print(json.dumps(evaluate(sys.argv[1], sys.argv[2])))
