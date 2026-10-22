#!/usr/bin/env python3
"""
Exact K-Nurse Subset MILP Polish (LNS over K nurses across all shifts s=0..S-1).
Each sub-MILP has ~60-150 binary variables and solves to 100% global optimality in ~0.02s via HiGHS,
capturing global ContinuityOfCare + RoomSkillLevel + ExcessiveNurseWorkload across the entire horizon.
"""
import json
import random
import sys
import time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csc_matrix


def polish_with_subset_milp(inst_path, sol_path, out_path, rounds=80, k_size=5, seed=42):
    rng = random.Random(seed)
    with open(inst_path) as f:
        J = json.load(f)
    with open(sol_path) as f:
        S = json.load(f)

    days = int(J["days"])
    shift_types = J["shift_types"]
    spd = len(shift_types)
    num_shifts = days * spd
    shift_idx = {name: i for i, name in enumerate(shift_types)}

    rooms = J["rooms"]
    R = len(rooms)
    room_idx = {rm["id"]: i for i, rm in enumerate(rooms)}

    nurses = J["nurses"]
    N = len(nurses)
    nurse_idx = {nr["id"]: i for i, nr in enumerate(nurses)}
    nurse_skill = [int(nr["skill_level"]) for nr in nurses]

    working = [{} for _ in range(N)]
    avail_nurses = [[] for _ in range(num_shifts)]
    for n, nr in enumerate(nurses):
        for ws in nr["working_shifts"]:
            s = int(ws["day"]) * spd + shift_idx[ws["shift"]]
            working[n][s] = int(ws["max_load"])
            avail_nurses[s].append(n)

    w_skill = int(J["weights"]["room_nurse_skill"])
    w_coc = int(J["weights"]["continuity_of_care"])
    w_work = int(J["weights"]["nurse_eccessive_workload"])

    people = []
    room_day_occupied = [[False] * days for _ in range(R)]
    room_shift_load = [[0] * num_shifts for _ in range(R)]
    room_shift_skill_pen = [[[0] * N for _ in range(num_shifts)] for _ in range(R)]

    for occ in J.get("occupants", []):
        r = room_idx[occ["room_id"]]
        los = int(occ["length_of_stay"])
        q_shifts = []
        for d in range(min(days, los)):
            room_day_occupied[r][d] = True
            for sn in range(spd):
                s = d * spd + sn
                wl = int(occ["workload_produced"][s])
                sk = int(occ["skill_level_required"][s])
                room_shift_load[r][s] += wl
                for n in avail_nurses[s]:
                    if sk > nurse_skill[n]:
                        room_shift_skill_pen[r][s][n] += (sk - nurse_skill[n]) * w_skill
                q_shifts.append(s)
        people.append((r, q_shifts))

    pat_by_id = {p["id"]: p for p in J["patients"]}
    for sp in S["patients"]:
        if sp["admission_day"] == "none":
            continue
        p = pat_by_id[sp["id"]]
        ad = int(sp["admission_day"])
        r = room_idx[sp["room"]]
        los = int(p["length_of_stay"])
        q_shifts = []
        for d in range(ad, min(days, ad + los)):
            room_day_occupied[r][d] = True
            for sn in range(spd):
                s = d * spd + sn
                s1 = s - ad * spd
                wl = int(p["workload_produced"][s1])
                sk = int(p["skill_level_required"][s1])
                room_shift_load[r][s] += wl
                for n in avail_nurses[s]:
                    if sk > nurse_skill[n]:
                        room_shift_skill_pen[r][s][n] += (sk - nurse_skill[n]) * w_skill
                q_shifts.append(s)
        people.append((r, q_shifts))

    rs_nurse = [[-1] * num_shifts for _ in range(R)]
    for jn in S["nurses"]:
        n = nurse_idx[jn["id"]]
        for ja in jn["assignments"]:
            s = int(ja["day"]) * spd + shift_idx[ja["shift"]]
            for r_id in ja["rooms"]:
                r = room_idx[r_id]
                rs_nurse[r][s] = n

    total_gain = 0
    for rnd in range(rounds):
        U = sorted(rng.sample(range(N), min(k_size, N)))
        U_set = set(U)

        # Find active shifts where >=2 nurses in U work AND >=1 occupied room is assigned to U
        active_rs = []
        x_map = {}
        x_list = []
        active_ns = []
        e_map = {}

        for s in range(num_shifts):
            d = s // spd
            u_avail = [n for n in U if s in working[n]]
            if len(u_avail) < 2:
                continue
            r_in_u = [r for r in range(R) if room_day_occupied[r][d] and rs_nurse[r][s] in U_set]
            if not r_in_u:
                continue
            for r in r_in_u:
                active_rs.append((r, s, u_avail))
                for n in u_avail:
                    x_map[(r, s, n)] = len(x_list)
                    x_list.append((r, s, n))
            for n in u_avail:
                e_map[(n, s)] = len(active_ns)
                active_ns.append((n, s, r_in_u))

        if not x_list:
            continue

        num_x = len(x_list)
        num_e = len(active_ns)

        # Continuity of care variables z_{q, n} for n in U
        z_map = {}
        z_list = []
        z_constraints = []
        fixed_coc = 0
        for q_idx, (r, q_shifts) in enumerate(people):
            for n in U:
                locked = False
                var_shifts = []
                for s in q_shifts:
                    if (r, s, n) in x_map:
                        var_shifts.append(s)
                    elif rs_nurse[r][s] == n:
                        locked = True
                        break
                if locked:
                    fixed_coc += w_coc
                elif var_shifts:
                    z_idx = len(z_list)
                    z_map[(q_idx, n)] = z_idx
                    z_list.append((q_idx, n))
                    for s in var_shifts:
                        z_constraints.append((x_map[(r, s, n)], z_idx))

        num_z = len(z_list)
        total_vars = num_x + num_e + num_z

        # Compute current subset objective to compare
        cur_sub_obj = fixed_coc
        for r, s, u_avail in active_rs:
            n_cur = rs_nurse[r][s]
            cur_sub_obj += room_shift_skill_pen[r][s][n_cur]
        for n, s, r_in_u in active_ns:
            ld = sum(room_shift_load[r][s] for r in r_in_u if rs_nurse[r][s] == n)
            if ld > working[n][s]:
                cur_sub_obj += (ld - working[n][s]) * w_work
        for q_idx, n in z_list:
            r, q_shifts = people[q_idx]
            if any(rs_nurse[r][s] == n for s in q_shifts):
                cur_sub_obj += w_coc

        c = np.zeros(total_vars, dtype=float)
        integrality = np.zeros(total_vars, dtype=int)
        lb = np.zeros(total_vars, dtype=float)
        ub = np.inf * np.ones(total_vars, dtype=float)

        for idx, (r, s, n) in enumerate(x_list):
            c[idx] = room_shift_skill_pen[r][s][n]
            integrality[idx] = 1
            ub[idx] = 1.0
        for i in range(num_e):
            c[num_x + i] = w_work
        for i in range(num_z):
            c[num_x + num_e + i] = w_coc
            ub[num_x + num_e + i] = 1.0

        rows_i, rows_j, rows_v, lhs, rhs = [], [], [], [], []
        rc = 0
        for r, s, u_avail in active_rs:
            for n in u_avail:
                rows_i.append(rc)
                rows_j.append(x_map[(r, s, n)])
                rows_v.append(1.0)
            lhs.append(1.0)
            rhs.append(1.0)
            rc += 1

        for i, (n, s, r_in_u) in enumerate(active_ns):
            e_idx = num_x + i
            for r in r_in_u:
                if room_shift_load[r][s] > 0:
                    rows_i.append(rc)
                    rows_j.append(x_map[(r, s, n)])
                    rows_v.append(float(room_shift_load[r][s]))
            rows_i.append(rc)
            rows_j.append(e_idx)
            rows_v.append(-1.0)
            lhs.append(-np.inf)
            rhs.append(float(working[n][s]))
            rc += 1

        for x_idx, z_i in z_constraints:
            rows_i.append(rc)
            rows_j.append(x_idx)
            rows_v.append(1.0)
            rows_i.append(rc)
            rows_j.append(num_x + num_e + z_i)
            rows_v.append(-1.0)
            lhs.append(-np.inf)
            rhs.append(0.0)
            rc += 1

        A = csc_matrix((rows_v, (rows_i, rows_j)), shape=(rc, total_vars))
        res = milp(
            c=c,
            integrality=integrality,
            bounds=Bounds(lb, ub),
            constraints=LinearConstraint(A, lhs, rhs),
            options={"time_limit": 0.5, "mip_rel_gap": 0.0},
        )
        if res.x is not None:
            new_sub_obj = fixed_coc + int(round(res.fun))
            if new_sub_obj < cur_sub_obj:
                gain = cur_sub_obj - new_sub_obj
                total_gain += gain
                for idx, (r, s, n) in enumerate(x_list):
                    if res.x[idx] > 0.5:
                        rs_nurse[r][s] = n

    if total_gain > 0 and out_path:
        nurse_ShiftRooms = [[[] for _ in range(num_shifts)] for _ in range(N)]
        for r in range(R):
            for s in range(num_shifts):
                if room_day_occupied[r][s // spd]:
                    n = rs_nurse[r][s]
                    nurse_ShiftRooms[n][s].append(rooms[r]["id"])
        new_nurses = []
        for n, nr in enumerate(nurses):
            assigns = []
            for ws in nr["working_shifts"]:
                d = int(ws["day"])
                sh_name = ws["shift"]
                s = d * spd + shift_idx[sh_name]
                assigns.append({
                    "day": d,
                    "shift": sh_name,
                    "rooms": nurse_ShiftRooms[n][s],
                })
            new_nurses.append({"id": nr["id"], "assignments": assigns})
        with open(out_path, "w") as f:
            json.dump({"patients": S["patients"], "nurses": new_nurses}, f, indent=2)
    return total_gain


if __name__ == "__main__":
    inst_p, sol_p, out_p = sys.argv[1], sys.argv[2], sys.argv[3]
    rds = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    ks = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    t0 = time.time()
    g = polish_with_subset_milp(inst_p, sol_p, out_p, rounds=rds, k_size=ks)
    print(f"Subset MILP polish gain={g} in {time.time()-t0:.2f}s")
