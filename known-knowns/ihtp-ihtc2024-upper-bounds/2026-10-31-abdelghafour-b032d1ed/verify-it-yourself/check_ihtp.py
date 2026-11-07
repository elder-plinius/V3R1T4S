"""Independent IHTP evaluator, a line-by-line port of the organisers' IHTP_Validator.cc (v0.0, 23/05/24).
Usage: python3 ihtp_eval.py instance.json solution.json  -> prints violations, costs, totals.
Our numbers are never claims; only the official validator's output is."""
import json, sys

def evaluate(inst_path, sol_path):
    I = json.load(open(inst_path)); S = json.load(open(sol_path))
    W = I['weights']
    w = [W['room_mixed_age'], W['room_nurse_skill'], W['continuity_of_care'], W['nurse_eccessive_workload'],
         W['open_operating_theater'], W['surgeon_transfer'], W['patient_delay'], W['unscheduled_optional']]
    D = I['days']; shn = I['shift_types']; spd = len(shn); NS = D * spd
    ag = {a: i for i, a in enumerate(I['age_groups'])}
    rid = {r['id']: i for i, r in enumerate(I['rooms'])}; R = len(rid)
    tid = {t['id']: i for i, t in enumerate(I['operating_theaters'])}; T = len(tid)
    uid = {u['id']: i for i, u in enumerate(I['surgeons'])}; U = len(uid)
    pid = {p['id']: i for i, p in enumerate(I['patients'])}; P = len(pid)
    nid = {n['id']: i for i, n in enumerate(I['nurses'])}; N = len(nid)
    occ = I['occupants']; O = len(occ)
    pat = I['patients']; nur = I['nurses']
    cap = [r['capacity'] for r in I['rooms']]
    lvl = [n['skill_level'] for n in nur]
    working = [dict() for _ in range(N)]  # shift -> max_load
    for n, x in enumerate(nur):
        for ws in x['working_shifts']:
            working[n][ws['day'] * spd + shn.index(ws['shift'])] = ws['max_load']
    # per person (patients then occupants): gender, age, los, wl, skill
    gen = [p['gender'] for p in pat] + [o['gender'] for o in occ]
    age = [ag[p['age_group']] for p in pat] + [ag[o['age_group']] for o in occ]
    los = [p['length_of_stay'] for p in pat] + [o['length_of_stay'] for o in occ]
    wl = [p['workload_produced'] for p in pat] + [o['workload_produced'] for o in occ]
    sk = [p['skill_level_required'] for p in pat] + [o['skill_level_required'] for o in occ]
    adm = [-1] * P; room = [-1] * P; ot = [-1] * P
    rd = [[[] for _ in range(D)] for _ in range(R)]
    for o in range(O):
        r = rid[occ[o]['room_id']]
        for d in range(occ[o]['length_of_stay']):
            rd[r][d].append(P + o)
    for x in S['patients']:
        if x['admission_day'] == 'none':
            continue
        p = pid[x['id']]
        if adm[p] != -1:
            raise ValueError('patient assigned twice')
        adm[p] = x['admission_day']; room[p] = rid[x['room']]; ot[p] = tid[x['operating_theater']]
        for d in range(adm[p], min(D, adm[p] + los[p])):
            rd[room[p]][d].append(p)
    rsn = [[-1] * NS for _ in range(R)]
    nsr = [[[] for _ in range(NS)] for _ in range(N)]
    for x in S['nurses']:
        n = nid[x['id']]
        for a in x['assignments']:
            s = a['day'] * spd + shn.index(a['shift'])
            if s not in working[n]:
                raise ValueError('non-working nurse assigned')
            for rr in a['rooms']:
                r = rid[rr]; rsn[r][s] = n; nsr[n][s].append(r)

    def rel(p, s):  # shift index relative to the person's own arrays
        return s - adm[p] * spd if p < P else s

    otload = [[0] * D for _ in range(T)]; otcnt = [[0] * D for _ in range(T)]
    uload = [[0] * D for _ in range(U)]; uth = [[set() for _ in range(D)] for _ in range(U)]
    for p in range(P):
        if adm[p] == -1: continue
        u = uid[pat[p]['surgeon_id']]; dur = pat[p]['surgery_duration']
        otload[ot[p]][adm[p]] += dur; otcnt[ot[p]][adm[p]] += 1
        uload[u][adm[p]] += dur; uth[u][adm[p]].add(ot[p])
    V = {}
    V['RoomGenderMix'] = sum(min(sum(gen[q] == 'A' for q in rd[r][d]), sum(gen[q] != 'A' for q in rd[r][d])) for r in range(R) for d in range(D))
    V['PatientRoomCompatibility'] = sum(1 for p in range(P) if room[p] != -1 and I['rooms'][room[p]]['id'] in (pat[p]['incompatible_room_ids'] or []))
    V['SurgeonOvertime'] = sum(max(0, uload[u][d] - I['surgeons'][u]['max_surgery_time'][d]) for u in range(U) for d in range(D))
    V['OperatingTheaterOvertime'] = sum(max(0, otload[t][d] - I['operating_theaters'][t]['availability'][d]) for t in range(T) for d in range(D))
    V['MandatoryUnscheduledPatients'] = sum(1 for p in range(P) if adm[p] == -1 and pat[p]['mandatory'])
    V['AdmissionDay'] = sum(1 for p in range(P) if adm[p] != -1 and (adm[p] < pat[p]['surgery_release_day'] or adm[p] > (pat[p]['surgery_due_day'] if pat[p]['mandatory'] else D - 1)))
    V['RoomCapacity'] = sum(max(0, len(rd[r][d]) - cap[r]) for r in range(R) for d in range(D))
    V['NursePresence'] = 0  # assignments to non-working shifts raise above, as in the validator
    V['UncoveredRoom'] = sum(1 for r in range(R) for s in range(NS) if rsn[r][s] == -1 and rd[r][s // spd])
    C = {}
    C['RoomAgeMix'] = sum(max(age[q] for q in rd[r][d]) - min(age[q] for q in rd[r][d]) for r in range(R) for d in range(D) if rd[r][d])
    C['RoomSkillLevel'] = sum(max(0, sk[q][rel(q, s)] - lvl[rsn[r][s]]) for r in range(R) for s in range(NS) for q in rd[r][s // spd] if rsn[r][s] != -1)
    coc = 0
    for q in list(range(P)) + list(range(P, P + O)):
        if q < P and adm[q] == -1: continue
        start = adm[q] if q < P else 0
        seen = set()
        for d in range(start, min(D, start + los[q])):
            for s in range(d * spd, (d + 1) * spd):
                if rsn[room[q] if q < P else rid[occ[q - P]['room_id']]][s] != -1:
                    seen.add(rsn[room[q] if q < P else rid[occ[q - P]['room_id']]][s])
        coc += len(seen)
    C['ContinuityOfCare'] = coc
    C['ExcessiveNurseWorkload'] = sum(max(0, sum(wl[q][rel(q, s)] for r in nsr[n][s] for q in rd[r][s // spd]) - working[n][s]) for n in range(N) for s in working[n])
    C['OpenOperatingTheater'] = sum(1 for t in range(T) for d in range(D) if otcnt[t][d] > 0)
    C['SurgeonTransfer'] = sum(max(0, len(uth[u][d]) - 1) for u in range(U) for d in range(D))
    C['PatientDelay'] = sum(adm[p] - pat[p]['surgery_release_day'] for p in range(P) if adm[p] != -1 and adm[p] > pat[p]['surgery_release_day'])
    C['ElectiveUnscheduledPatients'] = sum(1 for p in range(P) if adm[p] == -1 and not pat[p]['mandatory'])
    total = sum(v * wi for v, wi in zip(C.values(), w))
    return V, C, w, sum(V.values()), total


if __name__ == '__main__':
    # usage: check_ihtp.py instance.json solution.json   (prints the cost breakdown, then PASS or FAIL)
    try:
        V, C, w, tv, tc = evaluate(sys.argv[1], sys.argv[2])
    except Exception as e:
        print('error:', e); print('FAIL'); sys.exit(1)
    for k, v in V.items(): print('%-30s %5d' % (k, v))
    for (k, v), wi in zip(C.items(), w): print('%-30s %8d (%3d X %d)' % (k, v * wi, wi, v))
    print('Total violations = %d' % tv); print('Total cost = %d' % tc)
    ok = tv == 0 and tc == 28812 and tc < 29042
    print('expected 0 violations and cost 28812 (< table 29042):', 'yes' if ok else 'no')
    print('PASS' if ok else 'FAIL')
