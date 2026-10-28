#!/usr/bin/env python3
"""
Standalone exact deterministic checker for the Integrated Healthcare Timetabling Problem (IHTP / IHTC-2024).
Implements the exact mathematical specification of all 9 hard constraints and 8 soft cost components
matching the official IHTP_Validator.cc (Version 0.0, 23/05/24) using only the Python standard library.
"""
import hashlib
import json
import sys


def evaluate_ihtp(inst_data, sol_data):
    weights = inst_data["weights"]
    w_age = int(weights["room_mixed_age"])
    w_skill = int(weights["room_nurse_skill"])
    w_coc = int(weights["continuity_of_care"])
    w_work = int(weights["nurse_eccessive_workload"])
    w_ot = int(weights["open_operating_theater"])
    w_trans = int(weights["surgeon_transfer"])
    w_delay = int(weights["patient_delay"])
    w_unsched = int(weights["unscheduled_optional"])

    days = int(inst_data["days"])
    shift_types = inst_data["shift_types"]
    spd = len(shift_types)
    shifts = days * spd
    shift_map = {s: i for i, s in enumerate(shift_types)}

    age_groups = inst_data["age_groups"]
    age_map = {a: i for i, a in enumerate(age_groups)}

    rooms = inst_data["rooms"]
    R = len(rooms)
    room_map = {rm["id"]: i for i, rm in enumerate(rooms)}
    room_cap = [int(rm["capacity"]) for rm in rooms]

    surgeons = inst_data["surgeons"]
    U = len(surgeons)
    surg_map = {sg["id"]: i for i, sg in enumerate(surgeons)}
    surg_max = [[int(x) for x in sg["max_surgery_time"]] for sg in surgeons]

    ots = inst_data["operating_theaters"]
    T = len(ots)
    ot_map = {ot["id"]: i for i, ot in enumerate(ots)}
    ot_avail = [[int(x) for x in ot["availability"]] for ot in ots]

    nurses = inst_data["nurses"]
    N = len(nurses)
    nurse_map = {nr["id"]: i for i, nr in enumerate(nurses)}
    nurse_skill = [int(nr["skill_level"]) for nr in nurses]
    nurse_working = [[False] * shifts for _ in range(N)]
    nurse_max_load = [[0] * shifts for _ in range(N)]
    nurse_work_shifts = [[] for _ in range(N)]
    for n, nr in enumerate(nurses):
        for ws in nr["working_shifts"]:
            s = int(ws["day"]) * spd + shift_map[ws["shift"]]
            nurse_working[n][s] = True
            nurse_max_load[n][s] = int(ws["max_load"])
            nurse_work_shifts[n].append(s)

    occupants = inst_data.get("occupants", [])
    O = len(occupants)
    patients = inst_data["patients"]
    P = len(patients)
    pat_map = {p["id"]: i for i, p in enumerate(patients)}

    # Room-day patient lists (0..P-1 for patients, P..P+O-1 for occupants)
    room_day_list = [[[] for _ in range(days)] for _ in range(R)]
    room_day_a = [[0] * days for _ in range(R)]
    room_day_b = [[0] * days for _ in range(R)]

    for o_idx, occ in enumerate(occupants):
        q = P + o_idx
        r = room_map[occ["room_id"]]
        los = int(occ["length_of_stay"])
        g_is_a = (occ["gender"] == "A")
        for d in range(min(days, los)):
            room_day_list[r][d].append(q)
            if g_is_a:
                room_day_a[r][d] += 1
            else:
                room_day_b[r][d] += 1

    admission_day = [-1] * P
    assigned_room = [-1] * P
    assigned_ot = [-1] * P

    ot_day_list = [[[] for _ in range(days)] for _ in range(T)]
    ot_day_load = [[0] * days for _ in range(T)]
    surg_day_load = [[0] * days for _ in range(U)]
    surg_day_ot_cnt = [[[0] * T for _ in range(days)] for _ in range(U)]

    seen_patients = set()
    for jp in sol_data["patients"]:
        pid = jp["id"]
        if pid not in pat_map:
            raise ValueError(f"Unknown patient id {pid}")
        p = pat_map[pid]
        if p in seen_patients:
            raise ValueError(f"Patient {pid} assigned twice")
        seen_patients.add(p)
        if jp["admission_day"] != "none":
            ad = int(jp["admission_day"])
            if jp["room"] not in room_map:
                raise ValueError(f"Unknown room id {jp['room']}")
            if jp["operating_theater"] not in ot_map:
                raise ValueError(f"Unknown OT id {jp['operating_theater']}")
            r = room_map[jp["room"]]
            t = ot_map[jp["operating_theater"]]
            admission_day[p] = ad
            assigned_room[p] = r
            assigned_ot[p] = t

            los = int(patients[p]["length_of_stay"])
            g_is_a = (patients[p]["gender"] == "A")
            for d in range(ad, min(days, ad + los)):
                if 0 <= d < days:
                    room_day_list[r][d].append(p)
                    if g_is_a:
                        room_day_a[r][d] += 1
                    else:
                        room_day_b[r][d] += 1
            if 0 <= ad < days:
                dur = int(patients[p]["surgery_duration"])
                u = surg_map[patients[p]["surgeon_id"]]
                ot_day_list[t][ad].append(p)
                ot_day_load[t][ad] += dur
                surg_day_load[u][ad] += dur
                surg_day_ot_cnt[u][ad][t] += 1

    if len(seen_patients) != P:
        raise ValueError(f"Expected {P} patients in solution, found {len(seen_patients)}")

    room_shift_nurse = [[-1] * shifts for _ in range(R)]
    nurse_shift_rooms = [[[] for _ in range(shifts)] for _ in range(N)]
    patient_shift_nurse = []
    for p in range(P):
        patient_shift_nurse.append([-1] * (int(patients[p]["length_of_stay"]) * spd))
    for o in range(O):
        patient_shift_nurse.append([-1] * (int(occupants[o]["length_of_stay"]) * spd))

    for jn in sol_data["nurses"]:
        nid = jn["id"]
        if nid not in nurse_map:
            raise ValueError(f"Unknown nurse id {nid}")
        n = nurse_map[nid]
        for ja in jn["assignments"]:
            d = int(ja["day"])
            if not (0 <= d < days) or ja["shift"] not in shift_map:
                raise ValueError(f"Invalid day/shift in assignment for nurse {nid}")
            sn = shift_map[ja["shift"]]
            s = d * spd + sn
            if not nurse_working[n][s]:
                raise ValueError(f"Assigning non-working nurse {nid} to shift {s}")
            for r_id in ja["rooms"]:
                if r_id not in room_map:
                    raise ValueError(f"Unknown room id {r_id}")
                r = room_map[r_id]
                if room_shift_nurse[r][s] != -1:
                    raise ValueError(f"Room {r_id} assigned to multiple nurses on shift {s}")
                room_shift_nurse[r][s] = n
                nurse_shift_rooms[n][s].append(r)
                for q in room_day_list[r][d]:
                    if q < P:
                        s1 = s - admission_day[q] * spd
                    else:
                        s1 = s
                    patient_shift_nurse[q][s1] = n

    # Compute 9 Hard Constraint Violations
    v_gender = 0
    v_cap = 0
    for r in range(R):
        for d in range(days):
            v_gender += min(room_day_a[r][d], room_day_b[r][d])
            if len(room_day_list[r][d]) > room_cap[r]:
                v_cap += len(room_day_list[r][d]) - room_cap[r]

    v_compat = 0
    v_mand = 0
    v_ad = 0
    for p, pat in enumerate(patients):
        ad = admission_day[p]
        if ad == -1:
            if pat["mandatory"]:
                v_mand += 1
        else:
            r = assigned_room[p]
            incompat = pat.get("incompatible_room_ids") or []
            if rooms[r]["id"] in incompat:
                v_compat += 1
            rel = int(pat["surgery_release_day"])
            last = int(pat["surgery_due_day"]) if pat["mandatory"] else (days - 1)
            if ad < rel or ad > last:
                v_ad += 1

    v_surg_ot = 0
    for u in range(U):
        for d in range(days):
            if surg_day_load[u][d] > surg_max[u][d]:
                v_surg_ot += surg_day_load[u][d] - surg_max[u][d]

    v_ot_over = 0
    for t in range(T):
        for d in range(days):
            if ot_day_load[t][d] > ot_avail[t][d]:
                v_ot_over += ot_day_load[t][d] - ot_avail[t][d]

    v_nurse_pres = 0
    v_uncov = 0
    for r in range(R):
        for s in range(shifts):
            n = room_shift_nurse[r][s]
            if n != -1 and not nurse_working[n][s]:
                v_nurse_pres += 1
            if n == -1 and len(room_day_list[r][s // spd]) > 0:
                v_uncov += 1

    violations = {
        "RoomGenderMix": v_gender,
        "PatientRoomCompatibility": v_compat,
        "SurgeonOvertime": v_surg_ot,
        "OperatingTheaterOvertime": v_ot_over,
        "MandatoryUnscheduledPatients": v_mand,
        "AdmissionDay": v_ad,
        "RoomCapacity": v_cap,
        "NursePresence": v_nurse_pres,
        "UncoveredRoom": v_uncov,
    }
    total_violations = sum(violations.values())

    # Compute 8 Soft Costs (unweighted & weighted)
    c_age = 0
    for r in range(R):
        for d in range(days):
            plist = room_day_list[r][d]
            if plist:
                ags = [
                    age_map[patients[q]["age_group"]] if q < P else age_map[occupants[q - P]["age_group"]]
                    for q in plist
                ]
                c_age += max(ags) - min(ags)

    c_skill = 0
    for r in range(R):
        for s in range(shifts):
            d = s // spd
            n = room_shift_nurse[r][s]
            if n == -1:
                continue
            ns = nurse_skill[n]
            for q in room_day_list[r][d]:
                if q < P:
                    s1 = s - admission_day[q] * spd
                    req = int(patients[q]["skill_level_required"][s1])
                else:
                    req = int(occupants[q - P]["skill_level_required"][s])
                if req > ns:
                    c_skill += req - ns

    c_coc = 0
    for o in range(O):
        q = P + o
        los_s = int(occupants[o]["length_of_stay"]) * spd
        distinct = {n for n in patient_shift_nurse[q][:los_s] if n != -1}
        c_coc += len(distinct)
    for p in range(P):
        if admission_day[p] != -1:
            st = len(patient_shift_nurse[p])
            lim = min(st, (days - admission_day[p]) * spd)
            distinct = {n for n in patient_shift_nurse[p][:lim] if n != -1}
            c_coc += len(distinct)

    c_work = 0
    for n in range(N):
        for s in nurse_work_shifts[n]:
            d = s // spd
            load = 0
            for r in nurse_shift_rooms[n][s]:
                for q in room_day_list[r][d]:
                    if q < P:
                        s1 = s - admission_day[q] * spd
                        load += int(patients[q]["workload_produced"][s1])
                    else:
                        load += int(occupants[q - P]["workload_produced"][s])
            if load > nurse_max_load[n][s]:
                c_work += load - nurse_max_load[n][s]

    c_ot = 0
    for t in range(T):
        for d in range(days):
            if len(ot_day_list[t][d]) > 0:
                c_ot += 1

    c_trans = 0
    for u in range(U):
        for d in range(days):
            cnt = sum(1 for t in range(T) if surg_day_ot_cnt[u][d][t] > 0)
            if cnt > 1:
                c_trans += cnt - 1

    c_delay = 0
    c_unsched = 0
    for p, pat in enumerate(patients):
        ad = admission_day[p]
        if ad == -1:
            if not pat["mandatory"]:
                c_unsched += 1
        else:
            rel = int(pat["surgery_release_day"])
            if ad > rel:
                c_delay += ad - rel

    costs_weighted = {
        "RoomAgeMix": c_age * w_age,
        "RoomSkillLevel": c_skill * w_skill,
        "ContinuityOfCare": c_coc * w_coc,
        "ExcessiveNurseWorkload": c_work * w_work,
        "OpenOperatingTheater": c_ot * w_ot,
        "SurgeonTransfer": c_trans * w_trans,
        "PatientDelay": c_delay * w_delay,
        "ElectiveUnscheduledPatients": c_unsched * w_unsched,
    }
    total_cost = sum(costs_weighted.values())
    return total_violations, total_cost, violations, costs_weighted


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: author_checker_ihtp_check.py <instance.json> <solution.json> [expected_cost]")
        print("FAIL")
        sys.exit(1)
    inst_file = sys.argv[1]
    sol_file = sys.argv[2]
    try:
        exp_cost = int(sys.argv[3]) if len(sys.argv) >= 4 else None
        raw = open(sol_file, "rb").read()
        sha = hashlib.sha256(raw).hexdigest()
        inst_data = json.load(open(inst_file))
        sol_data = json.loads(raw.decode("utf-8"))
        viol, cost, v_map, c_map = evaluate_ihtp(inst_data, sol_data)
    except Exception as e:
        print(f"ERROR: {e}")
        print("FAIL")
        sys.exit(1)

    print(f"File: {sol_file} ({len(raw)} bytes, sha256={sha})")
    print(f"Total violations = {viol}")
    for k, v in v_map.items():
        if v != 0:
            print(f"  VIOLATION {k}: {v}")
    print("Costs breakdown:")
    for k, v in c_map.items():
        print(f"  {k:30s}: {v}")
    print(f"Total cost = {cost}")

    if viol != 0:
        print("FAIL: hard constraint violations > 0")
        print("FAIL")
        sys.exit(1)
    if exp_cost is not None and cost != exp_cost:
        print(f"FAIL: cost {cost} != expected {exp_cost}")
        print("FAIL")
        sys.exit(1)
    print("IHTP_CHECK: PASS")
    print("PASS")
