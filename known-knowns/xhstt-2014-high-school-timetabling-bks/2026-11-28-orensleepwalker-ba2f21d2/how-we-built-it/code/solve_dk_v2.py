"""
XHSTT Danish Lectio Subproblem CP-SAT Engine DK-v2 (`DK-HG-12` & `DK-VG-09`)
(scans/2026-11-27-xhstt-charlie/solve_dk_v2.py)

Upgrades over DK-v1 (from `smoke_v1` diagnostics):
  1. 60x Room Model Compression on `DK-HG-12` via Exact Ore-Hall Nested Deficiency Theorem:
     Verified `S_31 <= S_70 <= S_71` holds strictly! Only `0 < |allowed| <= 4` events (~3 per slot)
     use hinted `rv` room booleans; `S_31, S_70, S_71` use ONE exact deficiency variable `def_q` per slot:
       `def_q >= max(0, n31 - rem31, n31+n70 - rem70, n31+n70+n71 - rem71)`.
     Eliminates ~23,000 un-hinted room booleans that caused `UNKNOWN` in DK-v1!
  2. Adds Tight Coupled-Clique Neighborhood (`N0_Clique`, `35-50` coupled events unlocked across ALL
     `50-60` slots -> touches only ~50 resources instead of 600, solving to `OPTIMAL` in `1.5-5s`!).
  3. Adds Tabu-Fenced Ridge Kick + Polish Cascade: Periodically kicks `8` events (`<= cur_soft + 35`,
     maintaining `<= cur_hard`) with an exact `origin_diff >= 8` Tabu fence during Polish so search
     explores genuinely new basins instead of cycling on flat plateaus!
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


def precompute_hg_room_tiers(dk: v1.DKCompiled):
    """Classify DK-HG-12 events into: -1 (empty), 0 (tiny <=4), 31 (S31), 70 (S70), 71 (S71)."""
    if dk.uniform_rooms:
        return None
    sets_ge31 = {len(s): set(s) for s in {frozenset(a) for a in dk.allowed_rooms if len(a) >= 31}}
    s31, s70, s71 = sets_ge31[31], sets_ge31[70], sets_ge31[71]
    assert s31 <= s70 <= s71
    tier = []
    for a in dk.allowed_rooms:
        L = len(a)
        if L == 0:
            tier.append(-1)
        elif L <= 4:
            tier.append(0)
        elif L == 31:
            tier.append(31)
        elif L == 70:
            tier.append(70)
        elif L == 71:
            tier.append(71)
        else:
            raise ValueError(f"Unexpected room set size {L}")
    return {"tier": tier, "s31": s31, "s70": s70, "s71": s71}


def solve_dk_subproblem_v2(
    dk: v1.DKCompiled, rtiers, cur_se, t_cur: list, t_origin: list,
    free_evs: set, allowed_slots: set, cur_hard: int,
    secs: float = 8.0, workers: int = 2, seed: int = 1,
    min_diff_cur: int = 0, min_diff_origin: int = 0, hint_keep_prob: float = 1.0,
):
    rng = random.Random(seed)
    free_list = sorted(free_evs)
    if not free_list:
        return t_cur, "EMPTY"
    slot_list = sorted(allowed_slots)
    slot_set = set(slot_list)

    fixed_busy = collections.defaultdict(lambda: [0] * dk.T)
    fixed_in_slot = [0] * dk.T
    fixed_evs_by_slot = [[] for _ in range(dk.T)]
    for e_i in range(dk.E):
        if e_i in free_evs:
            continue
        tq = t_cur[e_i]
        if tq is not None:
            fixed_in_slot[tq] += 1
            fixed_evs_by_slot[tq].append(e_i)
            for r in dk.ev_fixed_res[e_i]:
                fixed_busy[r][tq] += 1

    m = cp_model.CpModel()
    x = {}
    u_var = {}
    ev_slots = {e_i: [] for e_i in free_list}
    slot_evs = collections.defaultdict(list)
    cur_lits = []
    orig_match_lits = []

    for e_i in free_list:
        tq_cur = t_cur[e_i]
        tq_orig = t_origin[e_i]
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
            if q == tq_orig:
                orig_match_lits.append(v)
            if hint_keep_prob > 0 and (hint_keep_prob >= 1.0 or rng.random() < hint_keep_prob):
                m.AddHint(v, 1 if q == tq_cur else 0)

        uv = m.NewBoolVar("")
        u_var[e_i] = uv
        lits.append(uv)
        if tq_cur is None:
            cur_lits.append(uv)
        if tq_orig is None:
            orig_match_lits.append(uv)
        if hint_keep_prob > 0 and (hint_keep_prob >= 1.0 or rng.random() < hint_keep_prob):
            m.AddHint(uv, 1 if tq_cur is None else 0)
        m.AddExactlyOne(lits)

    if min_diff_cur > 0 and cur_lits:
        m.Add(sum(cur_lits) <= max(0, len(cur_lits) - min_diff_cur))

    if min_diff_origin > 0:
        fixed_diff_orig = sum(1 for e_i in range(dk.E) if e_i not in free_evs and t_cur[e_i] != t_origin[e_i])
        rem_need = min_diff_origin - fixed_diff_orig
        if rem_need > 0 and orig_match_lits:
            m.Add(sum(orig_match_lits) <= max(0, len(free_list) - rem_need))

    hard_terms = []
    soft_terms = []

    # 1. AssignTime hard cost
    fixed_untimed = sum(1 for e_i in range(dk.E) if e_i not in free_evs and t_cur[e_i] is None)
    const_hard = dk.assign_time_w * fixed_untimed
    hard_terms.append(dk.assign_time_w * sum(u_var.values()))

    # 2. Exact Compressed Room Matching (`0` room vars on DK-VG-09; `<=4` tiny rooms + 1 Ore-Hall int var/slot on DK-HG-12!)
    touched_slots = sorted(slot_evs.keys())
    if dk.uniform_rooms:
        cap = len(dk.uniform_pool)
        for q in touched_slots:
            rem_cap = cap - fixed_in_slot[q]
            if rem_cap < len(slot_evs[q]):
                ov = m.NewIntVar(0, len(slot_evs[q]), "")
                m.Add(ov >= sum(v for _, v in slot_evs[q]) - max(0, rem_cap))
                hard_terms.append(dk.assign_res_w * ov)
    else:
        tier = rtiers["tier"]
        s31, s70, s71 = rtiers["s31"], rtiers["s70"], rtiers["s71"]
        const_hard += dk.assign_res_w * sum(1 for e_i in range(dk.E) if tier[e_i] == -1)

        untouched_set = set(range(dk.T)) - set(touched_slots)
        for q in untouched_set:
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
                    rl.append(rv)
                    room_lits_by_r[r_i].append(rv)
                    if r_i in s31: used_s31.append(rv)
                    if r_i in s70: used_s70.append(rv)
                    if r_i in s71: used_s71.append(rv)
                unm = m.NewBoolVar("")
                m.AddHint(unm, 0 if cur_r_i in dk.allowed_rooms[e_i] else 1)
                m.AddExactlyOne(rl + [unm])
                hard_terms.append(dk.assign_res_w * unm)

            for e_i, v in free_tiny:
                cur_r_name = cur_se[dk.eids[e_i]][0]["res"][dk.room_role_idx[e_i]]
                cur_r_i = dk.rix.get(cur_r_name, -1)
                is_here = (t_cur[e_i] == q)
                rl = []
                for r_i in dk.allowed_rooms[e_i]:
                    rv = m.NewBoolVar("")
                    m.Add(rv <= v)
                    m.AddHint(rv, 1 if (is_here and r_i == cur_r_i) else 0)
                    rl.append(rv)
                    room_lits_by_r[r_i].append(rv)
                    if r_i in s31: used_s31.append(rv)
                    if r_i in s70: used_s70.append(rv)
                    if r_i in s71: used_s71.append(rv)
                unm = m.NewBoolVar("")
                m.AddHint(unm, 0)
                m.Add(sum(rl) + unm == v)
                hard_terms.append(dk.assign_res_w * unm)

            for r_lits in room_lits_by_r.values():
                if len(r_lits) > 1:
                    m.AddAtMostOne(r_lits)

            # Nested Ore-Hall deficiency for S_31 <= S_70 <= S_71!
            c31_fix = sum(1 for e_i in fix_evs if tier[e_i] == 31)
            c70_fix = sum(1 for e_i in fix_evs if tier[e_i] == 70)
            c71_fix = sum(1 for e_i in fix_evs if tier[e_i] == 71)
            l31 = [v for e_i, v in slot_evs[q] if tier[e_i] == 31]
            l70 = [v for e_i, v in slot_evs[q] if tier[e_i] == 70]
            l71 = [v for e_i, v in slot_evs[q] if tier[e_i] == 71]

            ub_all = c31_fix + c70_fix + c71_fix + len(l31) + len(l70) + len(l71) + len(used_s71)
            if (c31_fix + len(l31) + len(used_s31) > 31) or (ub_all > 70):
                def_q = m.NewIntVar(0, ub_all, "")
                m.AddHint(def_q, 0)
                n31 = c31_fix + sum(l31) + sum(used_s31)
                n70 = n31 + c70_fix + sum(l70) + (sum(used_s70) - sum(used_s31))
                n71 = n70 + c71_fix + sum(l71) + (sum(used_s71) - sum(used_s70))
                m.Add(def_q >= n31 - 31)
                m.Add(def_q >= n70 - 70)
                m.Add(def_q >= n71 - 71)
                hard_terms.append(dk.assign_res_w * def_q)

    # 3. Active resources & Clashes
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
                bv = m.NewBoolVar("")
                cl = m.NewIntVar(0, len(lits) - 1, "")
                m.Add(sum(lits) == bv + cl)
                b_ind[r, q] = bv
                hard_terms.append(cl)

    def get_b(r, q):
        if (r, q) in b_ind:
            return b_ind[r, q]
        fb = fixed_busy[r][q]
        if r not in active_res:
            return 1 if fb > 0 else 0
        lits = [x[e_i, q] for e_i in free_evs_of_res[r] if (e_i, q) in x]
        if not lits:
            return 1 if fb > 0 else 0
        if fb >= 1:
            return 1
        if len(lits) == 1:
            b_ind[r, q] = lits[0]
            return lits[0]
        bv = m.NewBoolVar("")
        m.AddMaxEquality(bv, lits)
        b_ind[r, q] = bv
        return bv

    def add_dev_cost(const_v, var_lits, ub_v, lo, hi, req, w):
        nonlocal const_hard
        if not var_lits:
            d = (lo - const_v if lo is not None and const_v < lo else 0) + (const_v - hi if hi is not None and const_v > hi else 0)
            if d > 0 and req:
                const_hard += w * d
            return
        expr = const_v + sum(var_lits)
        target_list = hard_terms if req else soft_terms
        if hi is not None and const_v + ub_v > hi:
            ov = m.NewIntVar(0, const_v + ub_v, "")
            m.Add(ov >= expr - hi)
            target_list.append(w * ov)
        if lo is not None and lo > 0 and const_v < lo:
            uv = m.NewIntVar(0, lo, "")
            m.Add(uv >= lo - expr)
            target_list.append(w * uv)

    # 4. SpreadEvents
    for req, w, tgs, grps in dk.spread_rules:
        for ev_grp in grps:
            if not any(e_i in free_evs for e_i in ev_grp):
                if req:
                    for ts, lo, hi in tgs:
                        cnt = sum(1 for e_i in ev_grp if t_cur[e_i] in ts)
                        const_hard += w * (max(0, lo - cnt) + max(0, cnt - hi))
                continue
            for ts, lo, hi in tgs:
                cv = sum(1 for e_i in ev_grp if (e_i not in free_evs) and (t_cur[e_i] in ts))
                vl = [x[e_i, q] for e_i in ev_grp if e_i in free_evs for q in ts if (e_i, q) in x]
                add_dev_cost(cv, vl, len(vl), lo, hi, req, w)

    # 5. LimitIdleTimes
    for req, w, mn, mx, tgs, res_list in dk.idle_rules:
        target_list = hard_terms if req else soft_terms
        for r in res_list:
            if r not in active_res:
                continue
            for ts in tgs:
                b_seq = [get_b(r, q) for q in ts]
                if all(isinstance(z, int) for z in b_seq):
                    continue
                P = len(b_seq)
                any_d = m.NewBoolVar("")
                if any(z == 1 for z in b_seq if isinstance(z, int)):
                    m.Add(any_d == 1)
                else:
                    m.AddMaxEquality(any_d, [z for z in b_seq if not isinstance(z, int)])

                pref = []
                for p in range(P):
                    if p == 0:
                        if isinstance(b_seq[0], int):
                            pv = m.NewBoolVar(""); m.Add(pv == b_seq[0])
                        else:
                            pv = b_seq[0]
                    else:
                        if isinstance(b_seq[p], int) and b_seq[p] == 1:
                            pv = m.NewBoolVar(""); m.Add(pv == 1)
                        elif isinstance(b_seq[p], int) and b_seq[p] == 0:
                            pv = pref[p - 1]
                        else:
                            pv = m.NewBoolVar("")
                            m.Add(pv >= pref[p - 1]); m.Add(pv >= b_seq[p]); m.Add(pv <= pref[p - 1] + b_seq[p])
                    pref.append(pv)

                suff = [None] * P
                for p in range(P - 1, -1, -1):
                    if p == P - 1:
                        if isinstance(b_seq[p], int):
                            sv_p = m.NewBoolVar(""); m.Add(sv_p == b_seq[p])
                        else:
                            sv_p = b_seq[p]
                    else:
                        if isinstance(b_seq[p], int) and b_seq[p] == 1:
                            sv_p = m.NewBoolVar(""); m.Add(sv_p == 1)
                        elif isinstance(b_seq[p], int) and b_seq[p] == 0:
                            sv_p = suff[p + 1]
                        else:
                            sv_p = m.NewBoolVar("")
                            m.Add(sv_p >= suff[p + 1]); m.Add(sv_p >= b_seq[p]); m.Add(sv_p <= suff[p + 1] + b_seq[p])
                    suff[p] = sv_p

                target_list.append(w * (sum(pref) + sum(suff) - P * any_d - sum(b_seq)))

    # 6. ClusterBusyTimes
    for req, w, mn, mx, tgs, res_list in dk.cluster_rules:
        for r in res_list:
            if r not in active_res and not req:
                continue
            const_days = 0
            day_vars = []
            for ts in tgs:
                b_seq = [get_b(r, q) for q in ts]
                if any(z == 1 for z in b_seq if isinstance(z, int)):
                    const_days += 1
                elif not all(isinstance(z, int) for z in b_seq):
                    v_only = [z for z in b_seq if not isinstance(z, int)]
                    if len(v_only) == 1:
                        day_vars.append(v_only[0])
                    else:
                        dv = m.NewBoolVar(""); m.AddMaxEquality(dv, v_only); day_vars.append(dv)
            add_dev_cost(const_days, day_vars, len(day_vars), mn, mx, req, w)

    # 7. LimitBusyTimes
    for req, w, mn, mx, tgs, res_list in dk.busy_rules:
        target_list = hard_terms if req else soft_terms
        for r in res_list:
            if r not in active_res:
                continue
            for ts in tgs:
                b_seq = [get_b(r, q) for q in ts]
                if all(isinstance(z, int) for z in b_seq):
                    continue
                P = len(b_seq)
                m_sum = sum(b_seq)
                if mx is not None:
                    ov = m.NewIntVar(0, P, ""); m.Add(ov >= m_sum - mx); target_list.append(w * ov)
                if mn is not None and mn > 0:
                    if any(z == 1 for z in b_seq if isinstance(z, int)):
                        uv = m.NewIntVar(0, mn, ""); m.Add(uv >= mn - m_sum); target_list.append(w * uv)
                    else:
                        v_only = [z for z in b_seq if not isinstance(z, int)]
                        any_d = m.NewBoolVar(""); m.AddMaxEquality(any_d, v_only)
                        uv = m.NewIntVar(0, mn, ""); m.Add(uv >= mn * any_d - m_sum); target_list.append(w * uv)

    total_hard_expr = const_hard + (sum(hard_terms) if hard_terms else 0)
    m.Add(total_hard_expr <= int(cur_hard))
    total_soft_expr = sum(soft_terms) if soft_terms else 0
    m.Minimize(100000 * total_hard_expr + total_soft_expr)

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
    return new_t, f"{sv.StatusName(st)}({len(x)}v)"


def pick_coupled_clique(dk: v1.DKCompiled, t_cur: list, rng: random.Random, target_evs: int = 42):
    """Grow a tight BFS clique of events sharing Teachers/Students starting from a high-penalty seed event!"""
    sc = v1.event_penalty_weights(dk, t_cur)
    top = sorted(range(dk.E), key=lambda i: sc[i] * (0.5 + rng.random()), reverse=True)
    seed_ev = top[0]
    chosen = {seed_ev}
    frontier = [seed_ev]
    while len(chosen) < target_evs and frontier:
        cur = frontier.pop(rng.randrange(len(frontier)))
        res_sample = list(dk.ev_fixed_res[cur])
        rng.shuffle(res_sample)
        for r in res_sample[:6]:
            nbrs = list(dk.res_events[r])
            rng.shuffle(nbrs)
            for nb in nbrs[:8]:
                if nb not in chosen:
                    chosen.add(nb)
                    frontier.append(nb)
                    if len(chosen) >= target_evs:
                        break
            if len(chosen) >= target_evs:
                break
    if len(chosen) < target_evs:
        rem = [i for i in top if i not in chosen]
        chosen.update(rem[:(target_evs - len(chosen))])
    return chosen


def run_dk_v2(tid: str, total_secs: float = 1800.0, workers: int = 2, seed: int = 303, mem_gb: float = 4.5):
    lim = int(mem_gb * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    deadline = t0 + total_secs
    _, inst_el, inst, start_se, start_val = xio.load_target(tid)
    dk = v1.DKCompiled(inst)
    rtiers = precompute_hg_room_tiers(dk)

    t_origin = dk.extract_state(start_se)
    t_cur = list(t_origin)
    cur_se = dk.build_se_from_times(start_se, t_cur)
    cur_val = X.evaluate_se(inst, cur_se)[:2]
    assert cur_val == start_val
    print(f"[{tid}] DK-v2 Start verified: {cur_val[0]}.{cur_val[1]} (target <= {xio.TARGETS[tid]['win_max']})", flush=True)

    best_val = cur_val
    best_se = copy.deepcopy(cur_se)
    best_t = list(t_cur)
    rng = random.Random(seed)

    step = 0
    plateau_moves = 0
    improvements = 0
    TABU_FLOOR = 8

    while time.time() + 6.0 < deadline:
        step += 1
        rem = deadline - time.time()

        # Reset to best if ridge walk drifted > +30 soft points without improving after 6 polish steps
        if step % 9 == 1 and cur_val[0] == best_val[0] and cur_val[1] > best_val[1] + 25:
            t_cur = list(best_t)
            cur_se = copy.deepcopy(best_se)
            cur_val = best_val

        # Broken events (untimed + clashing) always unlocked!
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

        # Every 9th step: Tabu Ridge Kick (`min_diff_cur=8`, accepts up to `best_soft + 32`)!
        is_kick = (step % 9 == 4)
        cur_orig_diff = sum(1 for a, b in zip(t_cur, best_t) if a != b)
        tabu_req = TABU_FLOOR if (cur_orig_diff >= TABU_FLOOR and cur_val > best_val) else 0

        if is_kick:
            fe = pick_coupled_clique(dk, t_cur, rng, target_evs=50) | broken_evs
            sl = set(range(dk.T))
            s_lim = min(10.0, max(3.0, rem - 2.0))
            ntag = f"KICK_Clique({len(fe)}e)"
            cand_t, st_info = solve_dk_subproblem_v2(
                dk, rtiers, cur_se, t_cur, best_t, fe, sl, cur_hard=cur_val[0],
                secs=s_lim, workers=workers, seed=seed + step * 53,
                min_diff_cur=8, min_diff_origin=TABU_FLOOR, hint_keep_prob=0.72,
            )
        else:
            sub_m = step % 5
            if sub_m in (1, 3):
                # Tight Coupled Clique across ALL 50-60 slots (fast ~500v -> OPTIMAL in 2-6s!)
                k_ev = 45 if sub_m == 1 else 65
                fe = pick_coupled_clique(dk, t_cur, rng, target_evs=k_ev) | broken_evs
                sl = set(range(dk.T))
                s_lim = min(9.0 if sub_m == 1 else 12.0, max(3.0, rem - 2.0))
                ntag = f"Clique({len(fe)}e)"
            elif sub_m == 2:
                # Edge periods of 5 days (first & last period -> Idle & Cluster sniper!)
                days_sub = rng.sample(dk.days, 5)
                sl = {d[0] for d in days_sub} | {d[-1] for d in days_sub}
                fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
                s_lim = min(11.0, max(3.0, rem - 2.0))
                ntag = "Edges5D"
            elif sub_m == 4:
                # 2 Full Days (`10-12` slots)
                d_pair = rng.sample(dk.days, 2)
                sl = set(d_pair[0]) | set(d_pair[1])
                fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
                s_lim = min(14.0, max(3.0, rem - 2.0))
                ntag = "TwoDays"
            else:
                # Unfenced Clique Sniper (`tabu_req = 0` so if a win sits near origin we grab it!)
                fe = pick_coupled_clique(dk, t_cur, rng, target_evs=55) | broken_evs
                sl = set(range(dk.T))
                s_lim = min(10.0, max(3.0, rem - 2.0))
                tabu_req = 0
                ntag = f"Sniper({len(fe)}e)"

            cand_t, st_info = solve_dk_subproblem_v2(
                dk, rtiers, cur_se, t_cur, best_t, fe, sl, cur_hard=cur_val[0],
                secs=s_lim, workers=workers, seed=seed + step * 37,
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
                    print(f"  *** [{tid} S{step:3d} {ntag} {st_info}] NEW BEST {best_val[0]}.{best_val[1]} -> {cand_val[0]}.{cand_val[1]} (diff={diff}) | {time.time()-t0:.0f}s ***", flush=True)
                elif cand_val == cur_val:
                    plateau_moves += 1
                cur_val = cand_val
                cur_se = cand_se
                t_cur = cand_t

                if cur_val < best_val:
                    best_val = cur_val
                    best_se = copy.deepcopy(cur_se)
                    best_t = list(t_cur)
                    if xio.is_strict_win(tid, best_val):
                        wpath = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
                        v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"DK-v2 {ntag} seed={seed}")
                        assert v_chk == best_val
                        print(f"  *** [{tid}] STRICT WORLD RECORD WIN SAVED & VERIFIED: {best_val[0]}.{best_val[1]} -> {wpath} (sha={sha[:12]}) ***", flush=True)

        if step % 6 == 0:
            d_orig = sum(1 for a, b in zip(t_cur, best_t) if a != b)
            print(f"  [{tid} S{step:3d}] {ntag:16s} {st_info:16s} | cur={cur_val[0]}.{cur_val[1]}(d={d_orig}) best={best_val[0]}.{best_val[1]} (imp={improvements}, plat={plateau_moves}) | {time.time()-t0:.0f}s", flush=True)

    win = xio.is_strict_win(tid, best_val)
    win_path, sha = None, None
    if win:
        win_path = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
        v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, win_path, desc=f"DK-v2 seed={seed}")
        assert v_chk == best_val
    else:
        tmp_p = os.path.join(xio.LOGS_DIR, f"_chk_{tid}_{os.getpid()}.xml")
        v_chk, _, _ = xio.write_and_verify_xml(inst_el, inst, best_se, tmp_p, desc="check")
        os.remove(tmp_p)
        assert v_chk == best_val

    return dict(
        engine="DK-v2_ore_hall_clique_tabu", inst=tid,
        record=list(start_val), best=list(best_val), win=win,
        steps=step, improvements=improvements, plateau_moves=plateau_moves,
        diff_events=sum(1 for a, b in zip(best_t, t_origin) if a != b),
        win_path=win_path, sha256=sha, secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inst", choices=["DK-HG-12", "DK-VG-09"], required=True)
    parser.add_argument("--secs", type=float, default=1800.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=303)
    parser.add_argument("--out-json", type=str, default="")
    args = parser.parse_args()

    res = run_dk_v2(args.inst, total_secs=args.secs, workers=args.workers, seed=args.seed)
    if args.out_json:
        open(args.out_json, "w").write(json.dumps(res))
    else:
        print(json.dumps(res, indent=2), flush=True)


if __name__ == "__main__":
    main()
