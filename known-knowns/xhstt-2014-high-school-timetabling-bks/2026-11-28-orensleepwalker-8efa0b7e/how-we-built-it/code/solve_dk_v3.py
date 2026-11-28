"""
XHSTT Danish Lectio 6-Worker Portfolio Engine DK-v3 (`DK-VG-09` & `DK-HG-12`)
(scans/2026-11-27-xhstt-charlie/solve_dk_v3.py)

Overnight 6-Worker Architecture (`num_workers = 6` full RINS + Feasibility Jump portfolio):
  1. For `DK-HG-12` (`12.2330` -> win is `<= 11.*` OR `12.<=2329`):
     - Prong HG-A (First 38% of budget, ~45m): PURE HARD-INFEASIBILITY EJECTION SNIPER (`hard <= 11`,
       100% of soft constraints stripped -> 15x smaller model!):
         * First runs a Whole-School `1,235`-Event Pure-Hard CP-SAT solve (`hard <= 11`, warm-hinted)!
         * Then runs massive `450-650` Event (`5-Day` & `Clique`) Pure-Hard Ejection Windows surfing
           `hard == 12` (`min_diff = 20`) and hunting `hard <= 11` (`45s` per 6w solve)!
     - Prong HG-B (Remaining 62%, ~75m): `6`-Worker Soft Sniper at `hard == 12` (`35-55s` windows over
       `3` Full Days, `95`-Event Cliques, and `7`-Day Edge Periods + Multi-Trajectory Tabu Restarts)!
  2. For `DK-VG-09` (`2.2323` -> win is `<= 2.2322`, `52` identical rooms = `0` room vars!):
     - Runs `3` diverse `6`-worker Tabu trajectories (`40m` each), rotating `3`-to-`4` Full-Day Windows
       (`18-24` slots = `~350` lessons, `50s` 6w solve), `100`-Event Coupled Cliques across all `60` slots
       (`40s` 6w solve), and `8`-Day Edge Periods (`35s` 6w solve)!
"""
import argparse
import collections
import copy
import json
import os
import random
import resource
import sys
import time

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from ortools.sat.python import cp_model

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CHARLIE_DIR)
import xhstt_io as xio  # noqa: E402
from xhstt_io import X  # noqa: E402
import solve_dk_cpsat as v1  # noqa: E402
import solve_dk_v2 as v2  # noqa: E402


def solve_hg_pure_hard_ejection(
    dk: v1.DKCompiled, rtiers, cur_se, t_cur: list, free_evs: set, allowed_slots: set,
    max_hard_cap: int = 12, target_strict_hard: int = None,
    secs: float = 45.0, workers: int = 6, seed: int = 1, min_diff_cur: int = 0,
):
    """
    Ultra-slim PURE HARD-CONSTRAINT CP-SAT for DK-HG-12 (0 soft constraints -> 15x smaller!).
    Allows unlocking `500-1,235` events at once to hunt multi-hop `12 -> 11` hard ejection chains!
    """
    rng = random.Random(seed)
    free_list = sorted(free_evs)
    slot_list = sorted(allowed_slots)
    slot_set = set(slot_list)

    fixed_busy = collections.defaultdict(lambda: [0] * dk.T)
    fixed_evs_by_slot = [[] for _ in range(dk.T)]
    for e_i in range(dk.E):
        if e_i in free_evs:
            continue
        tq = t_cur[e_i]
        if tq is not None:
            fixed_evs_by_slot[tq].append(e_i)
            for r in dk.ev_fixed_res[e_i]:
                fixed_busy[r][tq] += 1

    m = cp_model.CpModel()
    x = {}
    u_var = {}
    ev_slots = {e_i: [] for e_i in free_list}
    slot_evs = collections.defaultdict(list)
    cur_lits = []

    for e_i in free_list:
        tq_cur = t_cur[e_i]
        cand_q = slot_list if (tq_cur is None or tq_cur in slot_set) else sorted(slot_set | {tq_cur})
        lits = []
        for q in cand_q:
            if q != tq_cur and any(fixed_busy[r][q] >= 1 for r in dk.ev_fixed_res[e_i] if r in dk.clash_res):
                continue
            v = m.NewBoolVar("")
            x[e_i, q] = v
            ev_slots[e_i].append((q, v))
            slot_evs[q].append((e_i, v))
            lits.append(v)
            if q == tq_cur:
                cur_lits.append(v)
                if min_diff_cur == 0 or rng.random() < 0.80:
                    m.AddHint(v, 1)
            elif min_diff_cur == 0 or rng.random() < 0.80:
                m.AddHint(v, 0)

        uv = m.NewBoolVar("")
        u_var[e_i] = uv
        lits.append(uv)
        if tq_cur is None:
            cur_lits.append(uv)
            if min_diff_cur == 0 or rng.random() < 0.80:
                m.AddHint(uv, 1)
        elif min_diff_cur == 0 or rng.random() < 0.80:
            m.AddHint(uv, 0)
        m.AddExactlyOne(lits)

    if min_diff_cur > 0 and cur_lits:
        m.Add(sum(cur_lits) <= max(0, len(cur_lits) - min_diff_cur))

    hard_terms = []
    const_hard = dk.assign_time_w * sum(1 for e_i in range(dk.E) if e_i not in free_evs and t_cur[e_i] is None)
    hard_terms.append(dk.assign_time_w * sum(u_var.values()))

    # Compressed Ore-Hall Room Matching
    tier = rtiers["tier"]
    s31, s70, s71 = rtiers["s31"], rtiers["s70"], rtiers["s71"]
    const_hard += dk.assign_res_w * sum(1 for e_i in range(dk.E) if tier[e_i] == -1)

    touched_slots = sorted(slot_evs.keys())
    for q in set(range(dk.T)) - set(touched_slots):
        nonempty_fix = [e_i for e_i in fixed_evs_by_slot[q] if tier[e_i] >= 0]
        rmap = dk.assign_rooms_slot(nonempty_fix)
        const_hard += dk.assign_res_w * sum(1 for r in rmap.values() if r is None)

    for q in touched_slots:
        fix_evs = fixed_evs_by_slot[q]
        fix_tiny = [e_i for e_i in fix_evs if tier[e_i] == 0]
        free_tiny = [(e_i, v) for e_i, v in slot_evs[q] if tier[e_i] == 0]
        used_s31, used_s70, used_s71 = [], [], []
        room_lits_by_r = collections.defaultdict(list)

        for e_i in fix_tiny:
            cur_r_name = cur_se[dk.eids[e_i]][0]["res"][dk.room_role_idx[e_i]]
            cur_r_i = dk.rix.get(cur_r_name, -1)
            rl = []
            for r_i in dk.allowed_rooms[e_i]:
                rv = m.NewBoolVar("")
                m.AddHint(rv, 1 if r_i == cur_r_i else 0)
                rl.append(rv); room_lits_by_r[r_i].append(rv)
                if r_i in s31: used_s31.append(rv)
                if r_i in s70: used_s70.append(rv)
                if r_i in s71: used_s71.append(rv)
            unm = m.NewBoolVar(""); m.AddHint(unm, 0); m.AddExactlyOne(rl + [unm])
            hard_terms.append(dk.assign_res_w * unm)

        for e_i, v in free_tiny:
            cur_r_name = cur_se[dk.eids[e_i]][0]["res"][dk.room_role_idx[e_i]]
            cur_r_i = dk.rix.get(cur_r_name, -1)
            is_here = (t_cur[e_i] == q)
            rl = []
            for r_i in dk.allowed_rooms[e_i]:
                rv = m.NewBoolVar(""); m.Add(rv <= v)
                m.AddHint(rv, 1 if (is_here and r_i == cur_r_i) else 0)
                rl.append(rv); room_lits_by_r[r_i].append(rv)
                if r_i in s31: used_s31.append(rv)
                if r_i in s70: used_s70.append(rv)
                if r_i in s71: used_s71.append(rv)
            unm = m.NewBoolVar(""); m.AddHint(unm, 0); m.Add(sum(rl) + unm == v)
            hard_terms.append(dk.assign_res_w * unm)

        for r_lits in room_lits_by_r.values():
            if len(r_lits) > 1:
                m.AddAtMostOne(r_lits)

        c31_fix = sum(1 for e_i in fix_evs if tier[e_i] == 31)
        c70_fix = sum(1 for e_i in fix_evs if tier[e_i] == 70)
        c71_fix = sum(1 for e_i in fix_evs if tier[e_i] == 71)
        l31 = [v for e_i, v in slot_evs[q] if tier[e_i] == 31]
        l70 = [v for e_i, v in slot_evs[q] if tier[e_i] == 70]
        l71 = [v for e_i, v in slot_evs[q] if tier[e_i] == 71]
        ub_all = c31_fix + c70_fix + c71_fix + len(l31) + len(l70) + len(l71) + len(used_s71)
        if (c31_fix + len(l31) + len(used_s31) > 31) or (ub_all > 70):
            def_q = m.NewIntVar(0, ub_all, ""); m.AddHint(def_q, 0)
            n31 = c31_fix + sum(l31) + sum(used_s31)
            n70 = n31 + c70_fix + sum(l70) + (sum(used_s70) - sum(used_s31))
            n71 = n70 + c71_fix + sum(l71) + (sum(used_s71) - sum(used_s70))
            m.Add(def_q >= n31 - 31); m.Add(def_q >= n70 - 70); m.Add(def_q >= n71 - 71)
            hard_terms.append(dk.assign_res_w * def_q)

    # Hard AvoidClashes + Hard SpreadEvents + Hard ClusterBusyTimes ONLY!
    active_res = set()
    free_evs_of_res = collections.defaultdict(list)
    for e_i in free_list:
        for r in dk.ev_fixed_res[e_i]:
            active_res.add(r)
            free_evs_of_res[r].append(e_i)

    b_ind = {}
    for r in dk.clash_res:
        if r not in active_res:
            const_hard += sum(c - 1 for c in fixed_busy[r] if c > 1)
            continue
        r_f_evs = free_evs_of_res[r]
        for q in range(dk.T):
            fb = fixed_busy[r][q]
            lits = [x[e_i, q] for e_i in r_f_evs if (e_i, q) in x]
            if not lits:
                if fb > 1:
                    const_hard += (fb - 1)
                b_ind[r, q] = 1 if fb > 0 else 0
            elif fb == 0 and len(lits) == 1:
                b_ind[r, q] = lits[0]
            elif fb >= 1:
                b_ind[r, q] = 1
                const_hard += (fb - 1)
                hard_terms.extend(lits)
            else:
                sh = sum(1 for e_i in r_f_evs if t_cur[e_i] == q)
                bv = m.NewBoolVar("")
                cl = m.NewIntVar(0, len(lits) - 1, "")
                m.AddHint(bv, 1 if sh >= 1 else 0)
                m.AddHint(cl, max(0, sh - 1))
                m.Add(sum(lits) == bv + cl)
                b_ind[r, q] = bv
                hard_terms.append(cl)

    # Hard SpreadEvents
    for req, w, tgs, grps in dk.spread_rules:
        if not req:
            continue
        for ev_grp in grps:
            if not any(e_i in free_evs for e_i in ev_grp):
                for ts, lo, hi in tgs:
                    cnt = sum(1 for e_i in ev_grp if t_cur[e_i] in ts)
                    const_hard += w * (max(0, lo - cnt) + max(0, cnt - hi))
                continue
            for ts, lo, hi in tgs:
                cv = sum(1 for e_i in ev_grp if (e_i not in free_evs) and (t_cur[e_i] in ts))
                vl = [x[e_i, q] for e_i in ev_grp if e_i in free_evs for q in ts if (e_i, q) in x]
                if not vl:
                    const_hard += w * (max(0, lo - cv) + max(0, cv - hi))
                else:
                    h_cnt = sum(1 for e_i in ev_grp if t_cur[e_i] in ts)
                    expr = cv + sum(vl)
                    if cv + len(vl) > hi:
                        ov = m.NewIntVar(0, cv + len(vl), ""); m.AddHint(ov, max(0, h_cnt - hi))
                        m.Add(ov >= expr - hi); hard_terms.append(w * ov)
                    if lo > 0 and cv < lo:
                        uv = m.NewIntVar(0, lo, ""); m.AddHint(uv, max(0, lo - h_cnt))
                        m.Add(uv >= lo - expr); hard_terms.append(w * uv)

    # Hard ClusterBusyTimes (Teacher max busy days!)
    for req, w, mn, mx, tgs, res_list in dk.cluster_rules:
        if not req:
            continue
        for r in res_list:
            if r not in active_res:
                c_d = sum(1 for ts in tgs if any(fixed_busy[r][q] > 0 for q in ts))
                const_hard += w * (max(0, (mn or 0) - c_d) + (max(0, c_d - mx) if mx is not None else 0))
                continue
            const_days = 0
            day_vars = []
            h_days = 0
            for ts in tgs:
                if any(fixed_busy[r][q] > 0 for q in ts):
                    const_days += 1
                    h_days += 1
                else:
                    v_only = [b_ind[r, q] for q in ts if not isinstance(b_ind.get((r, q), 0), int)]
                    any_h = any(t_cur[e_i] in ts for e_i in free_evs_of_res[r])
                    if any_h:
                        h_days += 1
                    if len(v_only) == 1:
                        day_vars.append(v_only[0])
                    elif len(v_only) > 1:
                        dv = m.NewBoolVar(""); m.AddHint(dv, 1 if any_h else 0)
                        m.AddMaxEquality(dv, v_only); day_vars.append(dv)
            if not day_vars:
                const_hard += w * (max(0, (mn or 0) - const_days) + (max(0, const_days - mx) if mx is not None else 0))
            else:
                expr = const_days + sum(day_vars)
                if mx is not None and const_days + len(day_vars) > mx:
                    ov = m.NewIntVar(0, const_days + len(day_vars), ""); m.AddHint(ov, max(0, h_days - mx))
                    m.Add(ov >= expr - mx); hard_terms.append(w * ov)

    tot_hard = const_hard + (sum(hard_terms) if hard_terms else 0)
    # Keep max_hard_cap (=12) so warm hint is accepted as incumbent for 6-worker RINS/DINS,
    # while Minimize(tot_hard) automatically posts tot_hard <= 11 after accepting the incumbent!
    m.Add(tot_hard <= int(max_hard_cap))
    m.Minimize(tot_hard)

    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return t_cur, f"{sv.StatusName(st)}({len(x)}v)"

    new_t = list(t_cur)
    for e_i in free_list:
        placed = None
        for q, v in ev_slots[e_i]:
            if sv.Value(v):
                placed = q
                break
        new_t[e_i] = placed
    return new_t, f"{sv.StatusName(st)}({len(x)}v,h={round(sv.ObjectiveValue())})"


def run_dk_v3(tid: str, total_secs: float = 7200.0, workers: int = 6, seed: int = 2001, mem_gb: float = 5.0):
    lim = int(mem_gb * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    deadline = t0 + total_secs
    os.makedirs(xio.LOGS_DIR, exist_ok=True)
    with open(os.path.join(xio.LOGS_DIR, "active_pids.jsonl"), "a") as pf:
        pf.write(json.dumps({"event": "start", "engine": "DK-v3", "inst": tid, "pid": os.getpid(), "pgid": os.getpgrp(), "secs": total_secs, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}) + "\n")
    _, inst_el, inst, start_se, start_val = xio.load_target(tid)
    dk = v1.DKCompiled(inst)
    rtiers = v2.precompute_hg_room_tiers(dk)

    t_origin = dk.extract_state(start_se)
    t_cur = list(t_origin)
    cur_se = dk.build_se_from_times(start_se, t_cur)
    cur_val = X.evaluate_se(inst, cur_se)[:2]
    assert cur_val == start_val
    print(f"[{tid}] DK-v3 (6w) Start verified: {cur_val[0]}.{cur_val[1]} (budget={total_secs:.0f}s; win <= {xio.TARGETS[tid]['win_max']})", flush=True)

    best_val = cur_val
    best_se = copy.deepcopy(cur_se)
    best_t = list(t_cur)
    rng = random.Random(seed)

    def save_if_best(cand_t, cand_se, cand_val, tag_lbl):
        nonlocal best_val, best_se, best_t
        if cand_val < best_val:
            print(f"  *** [{tid} {tag_lbl}] NEW BEST {best_val[0]}.{best_val[1]} -> {cand_val[0]}.{cand_val[1]} | {time.time()-t0:.0f}s ***", flush=True)
            best_val = cand_val
            best_se = copy.deepcopy(cand_se)
            best_t = list(cand_t)
            if xio.is_strict_win(tid, best_val):
                wpath = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
                v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"DK-v3 {tag_lbl} seed={seed}")
                assert v_chk == best_val
                print(f"  *** [{tid}] STRICT WORLD RECORD WIN SAVED & VERIFIED: {best_val[0]}.{best_val[1]} -> {wpath} (sha={sha[:12]}) ***", flush=True)

    # =========================================================================
    # PRONG HG-A (`DK-HG-12` ONLY, ~38% of budget): Pure Hard Ejection (`12 -> 11`)
    # =========================================================================
    hga_steps = 0
    if tid == "DK-HG-12":
        hga_deadline = t0 + total_secs * 0.38
        print(f"[{tid}] Prong HG-A: Pure Hard-Infeasibility Ejection Sniper (target hard <= 11)...", flush=True)

        # Step A1: Whole-School `1,235`-Event Pure-Hard Sniper (`hard <= 11` directly!)
        ws_secs = min(420.0, max(20.0, (hga_deadline - time.time()) * 0.20))
        cand_t, st_ws = solve_hg_pure_hard_ejection(
            dk, rtiers, cur_se, t_cur, set(range(dk.E)), set(range(dk.T)),
            max_hard_cap=best_val[0], target_strict_hard=best_val[0] - 1,
            secs=ws_secs, workers=workers, seed=seed, min_diff_cur=0,
        )
        print(f"  [{tid} HG-A WholeSchool1235] {st_ws} | {time.time()-t0:.0f}s", flush=True)
        if sum(1 for a, b in zip(cand_t, t_cur) if a != b) > 0:
            cse = dk.build_se_from_times(cur_se, cand_t)
            cv = X.evaluate_se(inst, cse)[:2]
            save_if_best(cand_t, cse, cv, "HGA-WholeSchool")
            if cv[0] <= cur_val[0]:
                t_cur, cur_se, cur_val = cand_t, cse, cv

        # Step A2: Large `450-650` Event Pure-Hard Ejection Windows surfing `hard == 12` & sniping `hard <= 11`!
        ej_t = list(best_t)
        ej_se = copy.deepcopy(best_se)
        ej_h = best_val[0]
        while time.time() + 15.0 < hga_deadline:
            hga_steps += 1
            rem_a = hga_deadline - time.time()
            broken = {e_i for e_i, tq in enumerate(ej_t) if tq is None}
            rb = collections.defaultdict(lambda: collections.defaultdict(list))
            for e_i, tq in enumerate(ej_t):
                if tq is not None:
                    for r in dk.ev_fixed_res[e_i]:
                        if r in dk.clash_res:
                            rb[r][tq].append(e_i)
            for r, qm in rb.items():
                for q, el in qm.items():
                    if len(el) > 1:
                        broken.update(el)

            if hga_steps % 2 == 1:
                # 5 Full Days (`25` slots = ~615 events!) with `min_diff=18` surf + `<= ej_h`!
                d_sub = rng.sample(dk.days, 5)
                sl = {q for d in d_sub for q in d}
                fe = {e_i for e_i, tq in enumerate(ej_t) if tq in sl} | broken
                ct, st_a = solve_hg_pure_hard_ejection(
                    dk, rtiers, ej_se, ej_t, fe, set(range(dk.T)),
                    max_hard_cap=ej_h, target_strict_hard=None,
                    secs=min(40.0, max(5.0, rem_a - 2.0)), workers=workers, seed=seed + hga_steps * 43, min_diff_cur=18,
                )
            else:
                # Strict `hard <= ej_h - 1` sniper over `550` coupled events across ALL 50 slots!
                fe = v2.pick_coupled_clique(dk, ej_t, rng, target_evs=520) | broken
                ct, st_a = solve_hg_pure_hard_ejection(
                    dk, rtiers, ej_se, ej_t, fe, set(range(dk.T)),
                    max_hard_cap=ej_h, target_strict_hard=ej_h - 1,
                    secs=min(45.0, max(5.0, rem_a - 2.0)), workers=workers, seed=seed + hga_steps * 43, min_diff_cur=0,
                )

            diff_a = sum(1 for a, b in zip(ct, ej_t) if a != b)
            if diff_a > 0:
                chg_q = {q for a, b in zip(ct, ej_t) if a != b for q in (a, b) if q is not None}
                cse = dk.build_se_from_times(ej_se, ct, changed_slots=chg_q)
                cv = X.evaluate_se(inst, cse)[:2]
                if cv[0] <= ej_h:
                    ej_t, ej_se, ej_h = ct, cse, cv[0]
                    save_if_best(ct, cse, cv, f"HGA-S{hga_steps}")
            if hga_steps % 4 == 0:
                d0 = sum(1 for a, b in zip(ej_t, best_t) if a != b)
                print(f"  [{tid} HG-A S{hga_steps:2d}] {st_a:22s} | ej_hard={ej_h}(d={d0}) best={best_val[0]}.{best_val[1]} | {time.time()-t0:.0f}s", flush=True)

    # =========================================================================
    # MAIN 6-WORKER SOFT+HARD PORTFOLIO LNS (3 Diverse Trajectories)
    # =========================================================================
    t_cur = list(best_t)
    cur_se = copy.deepcopy(best_se)
    cur_val = best_val
    rem_total = max(10.0, deadline - time.time())
    traj_len = max(120.0, rem_total / 3.0)
    next_traj_reset = time.time() + traj_len
    traj_id = 1

    step = 0
    improvements = 0
    plateau_moves = 0
    TABU_FLOOR = 10

    print(f"[{tid}] Starting 6-Worker Deep Portfolio LNS ({rem_total/60.0:.1f}m remaining)...", flush=True)

    while time.time() + 10.0 < deadline:
        step += 1
        rem = deadline - time.time()

        if time.time() >= next_traj_reset and rem > 120.0:
            traj_id += 1
            next_traj_reset = time.time() + traj_len
            t_cur = list(best_t)
            cur_se = copy.deepcopy(best_se)
            cur_val = best_val
            print(f"[{tid}] --- Trajectory #{traj_id} fresh restart from {best_val[0]}.{best_val[1]} | {time.time()-t0:.0f}s ---", flush=True)

        if step % 8 == 4 and cur_val > best_val:
            t_cur = list(best_t)
            cur_se = copy.deepcopy(best_se)
            cur_val = best_val

        broken_evs = {e_i for e_i, tq in enumerate(t_cur) if tq is None}
        res_b = collections.defaultdict(lambda: collections.defaultdict(list))
        for e_i, tq in enumerate(t_cur):
            if tq is not None:
                for r in dk.ev_fixed_res[e_i]:
                    if r in dk.clash_res:
                        res_b[r][tq].append(e_i)
        for r, qmap in res_b.items():
            for q, el in qmap.items():
                if len(el) > 1:
                    broken_evs.update(el)

        is_kick = (step % 8 == 5)
        cur_orig_diff = sum(1 for a, b in zip(t_cur, best_t) if a != b)
        tabu_req = TABU_FLOOR if (cur_orig_diff >= TABU_FLOOR and cur_val > best_val) else 0

        if is_kick:
            fe = v2.pick_coupled_clique(dk, t_cur, rng, target_evs=75) | broken_evs
            sl = set(range(dk.T))
            s_lim = min(28.0, max(4.0, rem - 2.0))
            ntag = f"KICK_6W({len(fe)}e)"
            cand_t, st_info = v2.solve_dk_subproblem_v2(
                dk, rtiers, cur_se, t_cur, best_t, fe, sl, cur_hard=cur_val[0],
                secs=s_lim, workers=workers, seed=seed + traj_id * 1000 + step * 53,
                min_diff_cur=10, min_diff_origin=TABU_FLOOR, hint_keep_prob=0.72,
            )
        else:
            sub_m = step % 5
            if sub_m == 1:
                # 3 Full Days (`15-18` slots = `~280-360` lessons, 50s 6-worker solve!)
                n_d = 3
                d_grp = rng.sample(dk.days, n_d)
                sl = {q for d in d_grp for q in d}
                fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
                s_lim = min(48.0, max(5.0, rem - 2.0))
                ntag = "ThreeDays6W"
            elif sub_m == 2:
                # 95-Event Coupled Clique across ALL 50-60 slots (`38s` 6w solve!)
                fe = v2.pick_coupled_clique(dk, t_cur, rng, target_evs=95) | broken_evs
                sl = set(range(dk.T))
                s_lim = min(38.0, max(5.0, rem - 2.0))
                ntag = f"Clique95({len(fe)}e)"
            elif sub_m == 3:
                # 7-Day Edge Periods (`14` boundary slots -> crushes Idle & Cluster!)
                days_sub = rng.sample(dk.days, 7)
                sl = {d[0] for d in days_sub} | {d[-1] for d in days_sub}
                fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
                s_lim = min(36.0, max(5.0, rem - 2.0))
                ntag = "Edges7D_6W"
            elif sub_m == 4:
                # 2 Consecutive Neighbor Days (`TGNeighborDays` SpreadEvents + Idle!)
                d0 = rng.randrange(0, len(dk.days) - 1)
                sl = set(dk.days[d0]) | set(dk.days[d0 + 1])
                fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
                s_lim = min(36.0, max(5.0, rem - 2.0))
                ntag = f"NbrDays({d0+1},{d0+2})"
            else:
                # Unfenced 80-Event Clique Sniper (`tabu_req = 0`!)
                fe = v2.pick_coupled_clique(dk, t_cur, rng, target_evs=80) | broken_evs
                sl = set(range(dk.T))
                s_lim = min(35.0, max(5.0, rem - 2.0))
                tabu_req = 0
                ntag = f"Sniper80({len(fe)}e)"

            cand_t, st_info = v2.solve_dk_subproblem_v2(
                dk, rtiers, cur_se, t_cur, best_t, fe, sl, cur_hard=cur_val[0],
                secs=s_lim, workers=workers, seed=seed + traj_id * 1000 + step * 37,
                min_diff_cur=0, min_diff_origin=tabu_req, hint_keep_prob=1.0,
            )

        diff = sum(1 for a, b in zip(cand_t, t_cur) if a != b)
        if diff > 0:
            changed_q = {q for a, b in zip(cand_t, t_cur) if a != b for q in (a, b) if q is not None}
            cand_se = dk.build_se_from_times(cur_se, cand_t, changed_slots=changed_q)
            cand_val = X.evaluate_se(inst, cand_se)[:2]

            accept = (cand_val <= cur_val) or (is_kick and cand_val[0] <= best_val[0] and cand_val[1] <= best_val[1] + 35)
            if accept:
                if cand_val < best_val:
                    improvements += 1
                elif cand_val == cur_val:
                    plateau_moves += 1
                cur_val = cand_val
                cur_se = cand_se
                t_cur = cand_t
                save_if_best(t_cur, cur_se, cur_val, ntag)

        if step % 4 == 0:
            d_orig = sum(1 for a, b in zip(t_cur, best_t) if a != b)
            print(f"  [{tid} T{traj_id} S{step:3d}] {ntag:18s} {st_info:18s} | cur={cur_val[0]}.{cur_val[1]}(d={d_orig}) best={best_val[0]}.{best_val[1]} (imp={improvements}, plat={plateau_moves}) | {time.time()-t0:.0f}s", flush=True)

    win = xio.is_strict_win(tid, best_val)
    win_path, sha = None, None
    if win:
        win_path = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
        v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, win_path, desc=f"DK-v3 seed={seed}")
        assert v_chk == best_val
    else:
        tmp_p = os.path.join(xio.LOGS_DIR, f"_chk_{tid}_{os.getpid()}.xml")
        v_chk, _, _ = xio.write_and_verify_xml(inst_el, inst, best_se, tmp_p, desc="check")
        os.remove(tmp_p)
        assert v_chk == best_val

    with open(os.path.join(xio.LOGS_DIR, "active_pids.jsonl"), "a") as pf:
        pf.write(json.dumps({"event": "done", "engine": "DK-v3", "inst": tid, "pid": os.getpid(), "pgid": os.getpgrp(), "best": list(best_val), "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}) + "\n")
    return dict(
        engine="DK-v3_6w_portfolio_sniper", inst=tid,
        record=list(start_val), best=list(best_val), win=win,
        hga_steps=hga_steps, steps=step, improvements=improvements, plateau_moves=plateau_moves,
        diff_events=sum(1 for a, b in zip(best_t, t_origin) if a != b),
        win_path=win_path, sha256=sha, secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inst", choices=["DK-HG-12", "DK-VG-09"], required=True)
    parser.add_argument("--secs", type=float, default=7200.0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--seed", type=int, default=2001)
    parser.add_argument("--out-json", type=str, default="")
    args = parser.parse_args()

    res = run_dk_v3(args.inst, total_secs=args.secs, workers=args.workers, seed=args.seed)
    if args.out_json:
        open(args.out_json, "w").write(json.dumps(res))
    else:
        print(json.dumps(res, indent=2), flush=True)


if __name__ == "__main__":
    main()
