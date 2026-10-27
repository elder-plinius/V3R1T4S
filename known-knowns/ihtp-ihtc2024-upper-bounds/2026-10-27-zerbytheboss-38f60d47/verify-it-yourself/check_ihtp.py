#!/usr/bin/env python3
"""Standalone pure-Python (stdlib-only) exact port of IHTP_Validator.cc (Version 0.0, 23/05/24).

Verifies all 9 hard constraint categories + read-time duplicate/presence invariants and
all 8 weighted soft objective components for the Integrated Healthcare Timetabling Competition 2024.
"""
import csv
import hashlib
import json
import os
import sys
import tempfile
import urllib.request
import zipfile


def load_instance_json(instance_name):
    """Load official IHTC-2024 instance JSON from local cache or official GitHub Pages archive."""
    local_candidates = [
        os.environ.get("IHTP_INSTANCE_FILE", ""),
        os.path.join(tempfile.gettempdir(), f"ihtp_{instance_name}.json"),
    ]
    for p in local_candidates:
        if p and os.path.isfile(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)

    is_m = instance_name.startswith("m")
    zip_url = (
        "https://ihtc2024.github.io/assets/files/ihtc2024_final_instances.zip"
        if is_m
        else "https://ihtc2024.github.io/assets/files/ihtc2024_competition_instances.zip"
    )
    zip_cache = os.path.join(
        tempfile.gettempdir(),
        "ihtc2024_final_instances.zip" if is_m else "ihtc2024_competition_instances.zip",
    )
    if not os.path.isfile(zip_cache):
        req = urllib.request.Request(zip_url, headers={"User-Agent": "V3R1T4S-IHTP-Verifier/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(zip_cache, "wb") as f:
            f.write(data)
    with zipfile.ZipFile(zip_cache, "r") as zf:
        for member in zf.namelist():
            if member.endswith(f"{instance_name}.json") and not os.path.basename(member).startswith("."):
                raw = zf.read(member)
                cache_out = os.path.join(tempfile.gettempdir(), f"ihtp_{instance_name}.json")
                with open(cache_out, "wb") as f:
                    f.write(raw)
                return json.loads(raw.decode("utf-8", errors="replace"))
    raise FileNotFoundError(f"Could not find {instance_name}.json in {zip_url}")


def evaluate_ihtp(j_in, j_sol):
    """Exact 1-to-1 port of IHTP_Input and IHTP_Output in IHTP_Validator.cc."""
    w_map = j_in["weights"]
    weights = [
        int(w_map["room_mixed_age"]),
        int(w_map["room_nurse_skill"]),
        int(w_map["continuity_of_care"]),
        int(w_map["nurse_eccessive_workload"]),
        int(w_map["open_operating_theater"]),
        int(w_map["surgeon_transfer"]),
        int(w_map["patient_delay"]),
        int(w_map["unscheduled_optional"]),
    ]

    days = int(j_in["days"])
    shift_names = list(j_in["shift_types"])
    shifts_per_day = len(shift_names)
    shifts = days * shifts_per_day
    age_group_names = list(j_in["age_groups"])

    shift_idx = {name: i for i, name in enumerate(shift_names)}
    age_idx = {name: i for i, name in enumerate(age_group_names)}

    surgeons = j_in["surgeons"]
    surgeon_idx = {s["id"]: i for i, s in enumerate(surgeons)}
    surgeon_max_time = [[int(x) for x in s["max_surgery_time"]] for s in surgeons]

    ots = j_in["operating_theaters"]
    ot_idx = {ot["id"]: i for i, ot in enumerate(ots)}
    ot_avail = [[int(x) for x in ot["availability"]] for ot in ots]

    rooms = j_in["rooms"]
    room_idx = {r["id"]: i for i, r in enumerate(rooms)}
    room_cap = [int(r["capacity"]) for r in rooms]
    num_rooms = len(rooms)

    occupants = j_in["occupants"]
    num_occ = len(occupants)
    occ_gender = [0 if o["gender"] == "A" else 1 for o in occupants]
    occ_age = [age_idx[o["age_group"]] for o in occupants]
    occ_los = [int(o["length_of_stay"]) for o in occupants]
    occ_workload = [[int(x) for x in o["workload_produced"]] for o in occupants]
    occ_skill = [[int(x) for x in o["skill_level_required"]] for o in occupants]
    occ_room = [room_idx[o["room_id"]] for o in occupants]

    patients = j_in["patients"]
    num_pat = len(patients)
    pat_mandatory = [bool(p["mandatory"]) for p in patients]
    pat_gender = [0 if p["gender"] == "A" else 1 for p in patients]
    pat_age = [age_idx[p["age_group"]] for p in patients]
    pat_los = [int(p["length_of_stay"]) for p in patients]
    pat_release = [int(p["surgery_release_day"]) for p in patients]
    pat_due = [int(p["surgery_due_day"]) if p["mandatory"] else -1 for p in patients]
    pat_last_day = [pat_due[i] if pat_mandatory[i] else days - 1 for i in range(num_pat)]
    pat_dur = [int(p["surgery_duration"]) for p in patients]
    pat_surgeon = [surgeon_idx[p["surgeon_id"]] for p in patients]
    pat_incompat = [[False] * num_rooms for _ in range(num_pat)]
    for i, p in enumerate(patients):
        if p.get("incompatible_room_ids"):
            for rid in p["incompatible_room_ids"]:
                pat_incompat[i][room_idx[rid]] = True
    pat_workload = [[int(x) for x in p["workload_produced"]] for p in patients]
    pat_skill = [[int(x) for x in p["skill_level_required"]] for p in patients]
    pat_idx = {p["id"]: i for i, p in enumerate(patients)}

    nurses = j_in["nurses"]
    num_nurses = len(nurses)
    nurse_idx = {n["id"]: i for i, n in enumerate(nurses)}
    nurse_skill = [int(n["skill_level"]) for n in nurses]
    nurse_working_shifts = [[] for _ in range(num_nurses)]
    nurse_is_working = [[False] * shifts for _ in range(num_nurses)]
    nurse_max_load = [[0] * shifts for _ in range(num_nurses)]
    for n_i, n in enumerate(nurses):
        for ws in n["working_shifts"]:
            s = int(ws["day"]) * shifts_per_day + shift_idx[ws["shift"]]
            nurse_working_shifts[n_i].append(s)
            nurse_is_working[n_i][s] = True
            nurse_max_load[n_i][s] = int(ws["max_load"])

    # Output state
    admission_day = [-1] * num_pat
    room = [-1] * num_pat
    operating_room = [-1] * num_pat
    patient_shift_nurse = [
        [-1] * (pat_los[p] * shifts_per_day) for p in range(num_pat)
    ] + [
        [-1] * (occ_los[o] * shifts_per_day) for o in range(num_occ)
    ]

    room_day_patient_list = [[[] for _ in range(days)] for _ in range(num_rooms)]
    room_day_a = [[0] * days for _ in range(num_rooms)]
    room_day_b = [[0] * days for _ in range(num_rooms)]
    room_shift_nurse = [[-1] * shifts for _ in range(num_rooms)]
    nurse_shift_room_list = [[[] for _ in range(shifts)] for _ in range(num_nurses)]

    ot_day_patient_list = [[[] for _ in range(days)] for _ in range(len(ots))]
    surgeon_day_load = [[0] * days for _ in range(len(surgeons))]
    surgeon_day_theater_count = [
        [[0] * len(ots) for _ in range(days)] for _ in range(len(surgeons))
    ]

    # UpdatewithOccupantsInfo()
    for i in range(num_occ):
        o = i + num_pat
        r = occ_room[i]
        for d in range(occ_los[i]):
            room_day_patient_list[r][d].append(o)
            if occ_gender[i] == 0:
                room_day_a[r][d] += 1
            else:
                room_day_b[r][d] += 1

    # ReadJSON patients
    for j_p in j_sol["patients"]:
        if j_p["admission_day"] != "none":
            p = pat_idx[j_p["id"]]
            if admission_day[p] != -1:
                raise ValueError(f"Patient {p} assigned twice in the solution")
            ad = int(j_p["admission_day"])
            r = room_idx[j_p["room"]]
            t = ot_idx[j_p["operating_theater"]]
            if ad < 0 or ad >= days:
                raise ValueError(f"Invalid admission_day {ad} for patient {p}")
            admission_day[p] = ad
            room[p] = r
            operating_room[p] = t
            for d in range(ad, min(days, ad + pat_los[p])):
                room_day_patient_list[r][d].append(p)
                if pat_gender[p] == 0:
                    room_day_a[r][d] += 1
                else:
                    room_day_b[r][d] += 1
            ot_day_patient_list[t][ad].append(p)
            u = pat_surgeon[p]
            surgeon_day_load[u][ad] += pat_dur[p]
            surgeon_day_theater_count[u][ad][t] += 1

    # ReadJSON nurses
    for j_n in j_sol["nurses"]:
        cn = nurse_idx[j_n["id"]]
        for asg in j_n["assignments"]:
            d = int(asg["day"])
            s = d * shifts_per_day + shift_idx[asg["shift"]]
            for rid in asg["rooms"]:
                r = room_idx[rid]
                if not nurse_is_working[cn][s]:
                    raise ValueError(f"Assigning non-working nurse {cn} to shift {s}")
                room_shift_nurse[r][s] = cn
                nurse_shift_room_list[cn][s].append(r)
                for p in room_day_patient_list[r][d]:
                    if p < num_pat:
                        s1 = s - admission_day[p] * shifts_per_day
                    else:
                        s1 = s
                    patient_shift_nurse[p][s1] = cn

    # Violations
    v_gender = sum(
        min(room_day_a[r][d], room_day_b[r][d])
        for r in range(num_rooms)
        for d in range(days)
    )
    v_compat = sum(
        1 for p in range(num_pat) if room[p] != -1 and pat_incompat[p][room[p]]
    )
    v_surg_ot = sum(
        max(0, surgeon_day_load[s][d] - surgeon_max_time[s][d])
        for s in range(len(surgeons))
        for d in range(days)
    )
    v_ot_over = 0
    for t in range(len(ots)):
        for d in range(days):
            tm = sum(pat_dur[p] for p in ot_day_patient_list[t][d])
            if tm > ot_avail[t][d]:
                v_ot_over += tm - ot_avail[t][d]
    v_mand = sum(1 for p in range(num_pat) if admission_day[p] == -1 and pat_mandatory[p])
    v_ad_day = sum(
        1
        for p in range(num_pat)
        if admission_day[p] != -1
        and (admission_day[p] < pat_release[p] or admission_day[p] > pat_last_day[p])
    )
    v_cap = sum(
        max(0, len(room_day_patient_list[r][d]) - room_cap[r])
        for r in range(num_rooms)
        for d in range(days)
    )
    v_nurse_pres = sum(
        1
        for r in range(num_rooms)
        for s in range(shifts)
        if room_shift_nurse[r][s] != -1 and not nurse_is_working[room_shift_nurse[r][s]][s]
    )
    v_uncov = sum(
        1
        for r in range(num_rooms)
        for s in range(shifts)
        if room_shift_nurse[r][s] == -1
        and len(room_day_patient_list[r][s // shifts_per_day]) > 0
    )

    violations = {
        "RoomGenderMix": v_gender,
        "PatientRoomCompatibility": v_compat,
        "SurgeonOvertime": v_surg_ot,
        "OperatingTheaterOvertime": v_ot_over,
        "MandatoryUnscheduledPatients": v_mand,
        "AdmissionDay": v_ad_day,
        "RoomCapacity": v_cap,
        "NursePresence": v_nurse_pres,
        "UncoveredRoom": v_uncov,
    }
    total_violations = sum(violations.values())

    # Soft costs
    c_age = 0
    for r in range(num_rooms):
        for d in range(days):
            plist = room_day_patient_list[r][d]
            if plist:
                ages = [
                    pat_age[p] if p < num_pat else occ_age[p - num_pat] for p in plist
                ]
                c_age += max(ages) - min(ages)

    c_skill = 0
    for r in range(num_rooms):
        for s in range(shifts):
            d = s // shifts_per_day
            n = room_shift_nurse[r][s]
            nskill = nurse_skill[n] if n != -1 else 0
            for p in room_day_patient_list[r][d]:
                if p < num_pat:
                    s1 = s - admission_day[p] * shifts_per_day
                    req = pat_skill[p][s1]
                else:
                    req = occ_skill[p - num_pat][s]
                if req > nskill:
                    c_skill += req - nskill

    c_coc = 0
    for o in range(num_occ):
        seen = set()
        for s in range(occ_los[o] * shifts_per_day):
            n = patient_shift_nurse[o + num_pat][s]
            if n != -1:
                seen.add(n)
        c_coc += len(seen)
    for p in range(num_pat):
        if admission_day[p] != -1:
            seen = set()
            lim = min(
                len(patient_shift_nurse[p]),
                (days - admission_day[p]) * shifts_per_day,
            )
            for s in range(lim):
                n = patient_shift_nurse[p][s]
                if n != -1:
                    seen.add(n)
            c_coc += len(seen)

    c_work = 0
    for n in range(num_nurses):
        for s in nurse_working_shifts[n]:
            d = s // shifts_per_day
            load = 0
            for r in nurse_shift_room_list[n][s]:
                for p in room_day_patient_list[r][d]:
                    if p < num_pat:
                        s1 = s - admission_day[p] * shifts_per_day
                        load += pat_workload[p][s1]
                    else:
                        load += occ_workload[p - num_pat][s]
            if load > nurse_max_load[n][s]:
                c_work += load - nurse_max_load[n][s]

    c_open_ot = sum(
        1
        for t in range(len(ots))
        for d in range(days)
        if len(ot_day_patient_list[t][d]) > 0
    )
    c_trans = 0
    for s in range(len(surgeons)):
        for d in range(days):
            cnt = sum(1 for t in range(len(ots)) if surgeon_day_theater_count[s][d][t] > 0)
            if cnt > 1:
                c_trans += cnt - 1
    c_delay = sum(
        admission_day[p] - pat_release[p]
        for p in range(num_pat)
        if admission_day[p] != -1 and admission_day[p] > pat_release[p]
    )
    c_opt = sum(
        1 for p in range(num_pat) if admission_day[p] == -1 and not pat_mandatory[p]
    )

    raw_costs = [
        ("RoomAgeMix", c_age, weights[0]),
        ("RoomSkillLevel", c_skill, weights[1]),
        ("ContinuityOfCare", c_coc, weights[2]),
        ("ExcessiveNurseWorkload", c_work, weights[3]),
        ("OpenOperatingTheater", c_open_ot, weights[4]),
        ("SurgeonTransfer", c_trans, weights[5]),
        ("PatientDelay", c_delay, weights[6]),
        ("ElectiveUnscheduledPatients", c_opt, weights[7]),
    ]
    weighted_costs = {name: val * w for name, val, w in raw_costs}
    total_cost = sum(weighted_costs.values())
    return {
        "total_violations": total_violations,
        "violations": violations,
        "total_cost": total_cost,
        "weighted_costs": weighted_costs,
        "raw_costs": {name: val for name, val, _ in raw_costs},
    }






def verify_pkg(pkg_root):
    idx_path = os.path.join(pkg_root, "INDEX.csv")
    if not os.path.isfile(idx_path):
        print("FAIL: missing INDEX.csv")
        return False
    with open(idx_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        print("FAIL: expected 1 row in INDEX.csv")
        return False
    row = rows[0]
    inst = row["cell"].strip()
    expected_cost = int(row["value"].strip())
    tbl_val = int(row["table_value"].strip())
    obj_rel = row["file"].strip()
    expected_sha = row["sha256"].strip()

    obj_path = os.path.join(pkg_root, obj_rel)
    if not os.path.isfile(obj_path):
        print(f"FAIL: missing {obj_rel}")
        return False
    raw = open(obj_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != expected_sha:
        print(f"FAIL: sha256 mismatch ({sha} != {expected_sha})")
        return False

    try:
        j_sol = json.loads(raw.decode("utf-8"))
        j_in = load_instance_json(inst)
        res = evaluate_ihtp(j_in, j_sol)
    except Exception as e:
        print(f"FAIL: validation exception ({e})")
        return False

    if res["total_violations"] != 0:
        print(f"FAIL: total_violations={res['total_violations']}")
        return False
    if res["total_cost"] != expected_cost:
        print(f"FAIL: total_cost={res['total_cost']} != {expected_cost}")
        return False
    if not (res["total_cost"] < tbl_val):
        print("FAIL: does not beat table_value")
        return False

    delta = res["total_cost"] - tbl_val
    print(
        f"VERIFIED: instance={inst} total_violations={res['total_violations']} "
        f"total_cost={res['total_cost']} bks={tbl_val} delta={delta} "
        f"weighted_costs={json.dumps(res['weighted_costs'], sort_keys=True)}"
    )
    print("PASS")
    return True


if __name__ == "__main__":
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not verify_pkg(pkg_root):
        print("FAIL")
        sys.exit(1)
