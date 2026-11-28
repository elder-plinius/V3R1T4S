"""
XHSTT AU-BG-98 Engine AU-v3 — 6-Worker Zero-Room-Var Whole-School Re-Timer + Teacher-First 10-Split Solver
+ Class-Centric Joint LNS
(scans/2026-11-27-xhstt-charlie/solve_au_v3.py)

Breakthroughs built from Wave 1 & Room-Set Dissection:
  1. Zero-Room-Var Exact Interval-Coloring Formulation:
     Dissection proved AU-BG-98 has only 10 allowed room sets: `S0..S6` are 7 pairwise-DISJOINT pools
     (sizes 1,1,2,2,2,3,3 -> interval-graph coloring is 100% equivalent to `active(S_g, q) <= |S_g|`!),
     and `S7(5), S8(26), S9(30)` satisfy `S7 <= S9` and `|S7 u S8 u S9| = 31`.
     Enforcing linear per-slot clique bounds eliminates ALL ~500,000 `(bundle, time, room)` combinations,
     followed by a 0.2s exact CP-SAT Room Packer verified by `xhstt_eval.evaluate_se`!
  2. Hour 1 — Fixed-Teacher Whole-School `371`-Bundle Time Optimizer (`6` workers):
     - Step 1A: Runs Whole-School `371`-Bundle Time Optimizer on GOAL's `11`-split teachers (`150s`, 6w):
       if `Spread(8) + Busy(10) = 18` drops by >= 3 pts (`<= 15`), `110 + 15 = 125` (`0.125`) WINS IMMEDIATELY!
     - Step 1B: Loops over each of the `11` split courses `g_k`, solves minimal-perturbation Teacher
       Assignment unifying `g_k` (`<= 10` splits = `AvoidSplit <= 100`, giving +7 pts slack!), and runs
       6-worker Whole-School `371`-Bundle Time Optimizer (`240s` each) to hunt `0`-hard schedules with
       `total_soft <= 125`!
  3. Hour 2 — Class-Centric Joint `(Time + Teacher)` Zero-Room-Var LNS + Whole-School Time Polish (`6` workers):
     Unlocks 100% of the weekly timetable of the Class(es) in a split course PLUS the split department's
     teachers (`~110` bundles, 3x bigger than AU-v2!), followed by Whole-School Time Polish!
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
import solve_au_cpsat as v1  # noqa: E402
import solve_au_v2 as v2  # noqa: E402


def classify_au_room_demands(au: v1.AUCompiled):
    """Map each sub_i's movable Room roles into exact room pools for zero-room-var interval caps."""
    distinct = sorted(
        {frozenset(au.allowed_er[info["eid"], k]) for info in au.subs for k, er in enumerate(info["ers"]) if er["rtype"] == "Room" and er["pre"] is None},
        key=len,
    )
    # Disjoint pools (len <= 3) vs coupled classroom triad (S7 len 5, S8 len 26, S9 len 30)
    disjoint_pools = [s for s in distinct if len(s) <= 3]
    s7 = next(s for s in distinct if len(s) == 5)
    s8 = next(s for s in distinct if len(s) == 26)
    s9 = next(s for s in distinct if len(s) == 30)
    assert len(s7 | s8 | s9) == 31 and s7 <= s9

    # Preassigned room usage per slot
    bundle_pool_demands = [collections.Counter() for _ in range(au.B)]
    for sub_i, info in enumerate(au.subs):
        b_id = au.sub_to_bundle[sub_i]
        for k, er in enumerate(info["ers"]):
            if er["rtype"] == "Room" and er["pre"] is None:
                aset = frozenset(au.allowed_er[info["eid"], k])
                bundle_pool_demands[b_id][aset] += 1

    return {
        "disjoint_pools": disjoint_pools,
        "s7": s7, "s8": s8, "s9": s9,
        "bundle_demands": bundle_pool_demands,
    }


def assign_concrete_rooms_au(au: v1.AUCompiled, base_se, b_times: list, teacher_map: dict = None, secs: float = 5.0, workers: int = 6):
    """Given bundle start times `b_times` (and optional `teacher_map[(sub_i, k)] = r`), pack concrete rooms!"""
    new_se = copy.deepcopy(base_se)
    for b_id, b in enumerate(au.bundles):
        tq = b_times[b_id]
        for sub_i in b["members"]:
            info = au.subs[sub_i]
            new_se[info["eid"]][info["pos"]]["t"] = tq
    if teacher_map:
        for (sub_i, k), r in teacher_map.items():
            info = au.subs[sub_i]
            new_se[info["eid"]][info["pos"]]["res"][k] = r

    # Exact CP-SAT interval coloring over Room roles ONLY (~911 sub-room slots, solves in < 0.2s!)
    m = cp_model.CpModel()
    ry = {}
    occ_r = collections.defaultdict(lambda: collections.defaultdict(list))
    for sub_i, info in enumerate(au.subs):
        s_rec = au.get_sub_se(new_se, sub_i)
        tq = s_rec["t"]
        dur = info["dur"]
        eid = info["eid"]
        for k, er in enumerate(info["ers"]):
            if er["rtype"] != "Room":
                continue
            if er["pre"] is not None:
                r0 = er["pre"]
                for q in range(tq, tq + dur):
                    occ_r[r0][q].append(1)
                continue
            cur_r = s_rec["res"][k]
            cands = au.allowed_er[eid, k]
            lits = []
            for r in cands:
                v = m.NewBoolVar("")
                ry[sub_i, k, r] = v
                m.AddHint(v, 1 if r == cur_r else 0)
                lits.append(v)
                for q in range(tq, tq + dur):
                    occ_r[r][q].append(v)
            m.AddExactlyOne(lits)

    clash_slacks = []
    for r in au.rooms:
        if r not in au.clash_res:
            continue
        for q in range(au.T):
            items = occ_r[r][q]
            if not items:
                continue
            c1 = sum(z for z in items if isinstance(z, int))
            vl = [z for z in items if not isinstance(z, int)]
            if c1 >= 1:
                for z in vl:
                    m.Add(z == 0)
            elif len(vl) > 1:
                m.AddAtMostOne(vl)

    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, sv.StatusName(st)

    for (sub_i, k, r), v in ry.items():
        if sv.Value(v):
            info = au.subs[sub_i]
            new_se[info["eid"]][info["pos"]]["res"][k] = r
    return new_se, "OK"


def solve_whole_school_fixed_teachers(
    au: v1.AUCompiled, rpools, base_se, teacher_map: dict,
    secs: float = 180.0, workers: int = 6, seed: int = 1, hint_times: list = None,
):
    """
    Whole-School `371`-Bundle Time Optimizer with FIXED Teachers (`teacher_map`) and ZERO Room Variables!
    Minimizes `10000 * hard_clashes + SpreadEvents(W=1) + LimitBusyTimes(W=2)` across 100% of the school!
    """
    m = cp_model.CpModel()
    xt = {}
    cand_t_map = {}

    # Effective fixed resources (Classes + fixed Teachers + preassigned Rooms) per bundle
    bundle_res = [set() for _ in range(au.B)]
    for sub_i, info in enumerate(au.subs):
        b_id = au.sub_to_bundle[sub_i]
        s_rec = au.get_sub_se(base_se, sub_i)
        for k, er in enumerate(info["ers"]):
            if er["rtype"] == "Room" and er["pre"] is None:
                continue
            r = teacher_map.get((sub_i, k), s_rec["res"][k]) if teacher_map else s_rec["res"][k]
            if r is not None:
                bundle_res[b_id].add(r)

    ht_chosen = []
    for b_id, b in enumerate(au.bundles):
        dur = b["dur"]
        cands = list(au.bundle_allowed_t[b_id])
        # Filter out times where ANY assigned Teacher/Class on bundle `b_id` is unavailable!
        valid = []
        for t in cands:
            if any(any((t + off) in au.unavail.get(r, ()) for off in range(dur)) for r in bundle_res[b_id]):
                continue
            valid.append(t)
        if not valid:
            return None, "EMPTY_BUNDLE_DOMAIN"
        cand_t_map[b_id] = valid
        lits = []
        ht = hint_times[b_id] if (hint_times is not None and hint_times[b_id] in valid) else valid[0]
        ht_chosen.append(ht)
        for t in valid:
            v = m.NewBoolVar("")
            xt[b_id, t] = v
            lits.append(v)
            m.AddHint(v, 1 if t == ht else 0)
        m.AddExactlyOne(lits)

    soft_terms = []
    hard_slacks = []

    # 1. Hard AvoidClashes on all Classes, Teachers, and preassigned Rooms (soft-slacked W=10000 for RINS warm start!)
    occ_res = collections.defaultdict(lambda: [[] for _ in range(au.T)])
    occ_hint = collections.defaultdict(lambda: [0] * au.T)
    for b_id, b in enumerate(au.bundles):
        dur = b["dur"]
        ht = ht_chosen[b_id]
        for r in bundle_res[b_id]:
            if r in au.clash_res:
                for q in range(ht, ht + dur):
                    occ_hint[r][q] += 1
        for t in cand_t_map[b_id]:
            v = xt[b_id, t]
            for r in bundle_res[b_id]:
                if r in au.clash_res:
                    for q in range(t, t + dur):
                        occ_res[r][q].append(v)

    busy_ind = {}
    for r, q_lists in occ_res.items():
        for q in range(au.T):
            ql = q_lists[q]
            if len(ql) == 1:
                busy_ind[r, q] = ql[0]
            elif len(ql) > 1:
                sh = occ_hint[r][q]
                bv = m.NewBoolVar("")
                m.AddHint(bv, 1 if sh >= 1 else 0)
                if teacher_map is None and sh <= 1:
                    m.AddAtMostOne(ql)
                    m.Add(bv == sum(ql))
                else:
                    cl = m.NewIntVar(0, len(ql) - 1, "")
                    m.AddHint(cl, max(0, sh - 1))
                    m.Add(sum(ql) == bv + cl)
                    soft_terms.append(10000 * cl)
                    hard_slacks.append(cl)
                busy_ind[r, q] = bv

    # 2. Exact Zero-Room-Var Interval-Coloring Capacities on `S0..S6` and `S7, S8, S9`!
    bdem = rpools["bundle_demands"]
    pool_occ = collections.defaultdict(lambda: [[] for _ in range(au.T)])
    pool_hint = collections.defaultdict(lambda: [0] * au.T)
    for b_id, b in enumerate(au.bundles):
        if not bdem[b_id]:
            continue
        dur = b["dur"]
        ht = ht_chosen[b_id]
        for pset, mult in bdem[b_id].items():
            for q in range(ht, ht + dur):
                pool_hint[pset][q] += mult
        for t in cand_t_map[b_id]:
            v = xt[b_id, t]
            for pset, mult in bdem[b_id].items():
                for q in range(t, t + dur):
                    pool_occ[pset][q].append(mult * v if mult > 1 else v)

    def add_cap_bound(expr_terms, cap_val, h_val):
        if not expr_terms:
            return
        if teacher_map is None and h_val <= cap_val:
            m.Add(sum(expr_terms) <= cap_val)
        else:
            ub = max(1, len(expr_terms) * 2)
            rc = m.NewIntVar(0, ub, "")
            m.AddHint(rc, max(0, h_val - cap_val))
            m.Add(sum(expr_terms) <= cap_val + rc)
            soft_terms.append(10000 * rc)
            hard_slacks.append(rc)

    for pset in rpools["disjoint_pools"]:
        cap = len(pset)
        for q in range(au.T):
            add_cap_bound(pool_occ[pset][q], cap, pool_hint[pset][q])

    s7, s8, s9 = rpools["s7"], rpools["s8"], rpools["s9"]
    for q in range(au.T):
        add_cap_bound(pool_occ[s7][q], 5, pool_hint[s7][q])
        add_cap_bound(pool_occ[s8][q], 26, pool_hint[s8][q])
        add_cap_bound(pool_occ[s7][q] + pool_occ[s9][q], 30, pool_hint[s7][q] + pool_hint[s9][q])
        add_cap_bound(
            pool_occ[s7][q] + pool_occ[s8][q] + pool_occ[s9][q],
            31,
            pool_hint[s7][q] + pool_hint[s8][q] + pool_hint[s9][q],
        )

    # 3. SpreadEventsConstraint
    for req, w, tgs, grps in au.spread_rules:
        for sub_grp in grps:
            for ts, lo, hi in tgs:
                vl = []
                h_cnt = 0
                for sub_i in sub_grp:
                    b_id = au.sub_to_bundle[sub_i]
                    if ht_chosen[b_id] in ts:
                        h_cnt += 1
                    vl.extend(xt[b_id, t] for t in ts if (b_id, t) in xt)
                if not vl:
                    continue
                expr = sum(vl)
                if req:
                    if teacher_map is None and lo <= h_cnt <= hi:
                        m.Add(expr >= lo); m.Add(expr <= hi)
                    else:
                        if len(vl) > hi:
                            ov = m.NewIntVar(0, len(vl), ""); m.AddHint(ov, max(0, h_cnt - hi))
                            m.Add(ov >= expr - hi); soft_terms.append(10000 * ov); hard_slacks.append(ov)
                        if lo > 0:
                            uv = m.NewIntVar(0, lo, ""); m.AddHint(uv, max(0, lo - h_cnt))
                            m.Add(uv >= lo - expr); soft_terms.append(10000 * uv); hard_slacks.append(uv)
                else:
                    if len(vl) > hi:
                        ov = m.NewIntVar(0, len(vl), ""); m.AddHint(ov, max(0, h_cnt - hi))
                        m.Add(ov >= expr - hi); soft_terms.append(w * ov)
                    if lo > 0:
                        uv = m.NewIntVar(0, lo, ""); m.AddHint(uv, max(0, lo - h_cnt))
                        m.Add(uv >= lo - expr); soft_terms.append(w * uv)

    # 4. LimitBusyTimesConstraint (W=2, min=0, max=7)
    for req, w, mn, mx, tgs, res_list in au.busy_rules:
        for r in res_list:
            if r not in occ_res:
                continue
            for ts in tgs:
                b_q = [busy_ind[r, q] for q in ts if (r, q) in busy_ind]
                if len(b_q) > mx:
                    h_b = sum(1 for q in ts if occ_hint[r][q] >= 1)
                    ov = m.NewIntVar(0, len(b_q), ""); m.AddHint(ov, max(0, h_b - mx))
                    m.Add(ov >= sum(b_q) - mx); soft_terms.append(w * ov)

    m.Minimize(sum(soft_terms) if soft_terms else 0)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, f"{sv.StatusName(st)}({len(xt)}v)"

    rem_hard = sum(int(round(sv.Value(hs))) for hs in hard_slacks)
    if rem_hard > 0:
        return None, f"HARD_REMAIN(h={rem_hard},obj={round(sv.ObjectiveValue())})"

    b_times = [next(t for t in cand_t_map[b_id] if sv.Value(xt[b_id, t])) for b_id in range(au.B)]
    packed_se, r_st = assign_concrete_rooms_au(au, base_se, b_times, teacher_map=teacher_map, secs=6.0, workers=workers)
    if packed_se is None:
        return None, f"ROOM_INFEAS({sv.StatusName(st)})"
    return packed_se, f"{sv.StatusName(st)}({len(xt)}v,sb={round(sv.ObjectiveValue())})"


def generate_unify_teacher_candidates(au: v1.AUCompiled, base_se, target_gid: str, max_cands: int = 2, seed: int = 1):
    """
    Generate minimal-perturbation valid Teacher Assignments (`PreferResources + LimitWorkload + Hard AvoidSplit`)
    where `target_gid` is FORCED UN-SPLIT (`1` teacher) and total soft splits `<= 10` (`AvoidSplit <= 100`)!
    """
    m = cp_model.CpModel()
    y = {}
    wload_t = collections.defaultdict(list)
    wload_c = collections.defaultdict(int)
    diff_lits = []

    bundle_fixed_res = [set() for _ in range(au.B)]
    for sub_i, info in enumerate(au.subs):
        b_id = au.sub_to_bundle[sub_i]
        s_rec = au.get_sub_se(base_se, sub_i)
        for k, er in enumerate(info["ers"]):
            if er["rtype"] == "Room" and er["pre"] is None:
                continue
            if er["pre"] is not None or er["rtype"] != "Teacher":
                r = s_rec["res"][k]
                if r is not None:
                    bundle_fixed_res[b_id].add(r)

    bundle_base_valid = []
    for b_id, b in enumerate(au.bundles):
        dur = b["dur"]
        bv_t = [
            t for t in au.bundle_allowed_t[b_id]
            if not any(any((t + off) in au.unavail.get(r, ()) for off in range(dur)) for r in bundle_fixed_res[b_id])
        ]
        bundle_base_valid.append(bv_t)

    bundle_y_by_r = [collections.defaultdict(list) for _ in range(au.B)]
    fixed_slot_occ = collections.defaultdict(lambda: collections.defaultdict(list))

    for sub_i, info in enumerate(au.subs):
        b_id = au.sub_to_bundle[sub_i]
        dur = au.bundles[b_id]["dur"]
        bv_t = bundle_base_valid[b_id]
        s_rec = au.get_sub_se(base_se, sub_i)
        for k, er in enumerate(info["ers"]):
            wl = info["dur"] * er["workload"] * info["scale6"]
            if er["pre"] is not None or er["rtype"] != "Teacher":
                r = s_rec["res"][k]
                if r in au.teachers:
                    wload_c[r] += wl
                    if len(bv_t) == 1:
                        for q in range(bv_t[0], bv_t[0] + dur):
                            fixed_slot_occ[r][q].append(1)
                continue
            cur_r = s_rec["res"][k]
            lits = []
            for r in au.allowed_er[info["eid"], k]:
                if r in bundle_fixed_res[b_id] and r in au.clash_res:
                    continue
                if not any(not any((t + off) in au.unavail.get(r, ()) for off in range(dur)) for t in bv_t):
                    continue
                v = m.NewBoolVar("")
                y[sub_i, k, r] = v
                m.AddHint(v, 1 if r == cur_r else 0)
                lits.append(v)
                wload_t[r].append(wl * v)
                bundle_y_by_r[b_id][r].append(v)
                if len(bv_t) == 1:
                    for q in range(bv_t[0], bv_t[0] + dur):
                        fixed_slot_occ[r][q].append(v)
                if r != cur_r:
                    diff_lits.append(v)
            if not lits:
                return []
            m.AddExactlyOne(lits)

    # Guarantee intra-bundle AvoidClashes AND at least 1 jointly valid start time per LinkBundle!
    for b_id, b in enumerate(au.bundles):
        if not bundle_y_by_r[b_id]:
            continue
        for r, rlits in bundle_y_by_r[b_id].items():
            if r in au.clash_res and len(rlits) > 1:
                m.AddAtMostOne(rlits)
        dur = b["dur"]
        vt_list = []
        for t in bundle_base_valid[b_id]:
            vt = m.NewBoolVar("")
            vt_list.append(vt)
            for r, rlits in bundle_y_by_r[b_id].items():
                if any((t + off) in au.unavail.get(r, ()) for off in range(dur)):
                    for lv in rlits:
                        m.Add(vt + lv <= 1)
        m.Add(sum(vt_list) >= 1)

    for r, qm in fixed_slot_occ.items():
        if r not in au.clash_res:
            continue
        for q, items in qm.items():
            c1 = sum(z for z in items if isinstance(z, int))
            vl = [z for z in items if not isinstance(z, int)]
            if c1 >= 1:
                for z in vl:
                    m.Add(z == 0)
            elif len(vl) > 1:
                m.AddAtMostOne(vl)

    for r in au.teachers:
        ex = wload_c[r] + sum(wload_t[r])
        if r in au.wload_max6:
            m.Add(ex <= au.wload_max6[r])
        if r in au.wload_min6:
            m.Add(ex >= au.wload_min6[r])

    split_devs = []
    for req, w, role, gid, items, pre_set in au.split_rules:
        by_r = collections.defaultdict(list)
        for sub_i, k in items:
            for r in au.allowed_er[au.subs[sub_i]["eid"], k]:
                if (sub_i, k, r) in y:
                    by_r[r].append(y[sub_i, k, r])
        if not by_r:
            continue
        uvs = [1 for _ in pre_set]
        for r, lvs in by_r.items():
            if r in pre_set:
                continue
            uv = m.NewBoolVar("")
            for lv in lvs:
                m.Add(uv >= lv)
            m.Add(uv <= sum(lvs))
            uvs.append(uv)
        if req or gid == target_gid:
            m.Add(sum(uvs) <= 1)
        else:
            dv = m.NewIntVar(0, len(uvs), "")
            m.Add(dv >= sum(uvs) - 1)
            split_devs.append(w * dv)

    tot_split_cost = sum(split_devs) if split_devs else 0
    m.Add(tot_split_cost <= 100)  # Strictly <= 10 splits (at least -10 pts below 110)!
    # Minimal perturbation first (`25 * diff + split_cost`) so hint_times stays 98% clash-free!
    m.Minimize(25 * sum(diff_lits) + tot_split_cost)

    out = []
    for c_i in range(max_cands):
        sv = cp_model.CpSolver()
        sv.parameters.max_time_in_seconds = 5.0
        sv.parameters.num_workers = 6
        sv.parameters.random_seed = seed + c_i * 31
        st = sv.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        tmap = {}
        diff_chosen = []
        for (sub_i, k, r), v in y.items():
            if sv.Value(v):
                tmap[sub_i, k] = r
                if au.get_sub_se(base_se, sub_i)["res"][k] != r:
                    diff_chosen.append(v)
        sp_val = int(round(sv.Value(tot_split_cost)))
        n_chg = len(diff_chosen)
        out.append((tmap, sp_val, n_chg))
        # Diversity cut: forbid picking the exact same set of changed teachers next time
        if diff_chosen:
            m.Add(sum(diff_chosen) <= len(diff_chosen) - 1)
        else:
            break
    return out


def solve_au_zero_room_joint_subproblem(
    au: v1.AUCompiled, rpools, cur_se, free_bundles: set, free_teachers: set,
    secs: float = 35.0, workers: int = 6, seed: int = 1, min_time_diff: int = 0,
):
    """
    Zero-Room-Var Joint `(LinkBundle Time + Teacher)` Subproblem CP-SAT!
    3-4x faster & larger than AU-v2 because all 45 Rooms are handled via exact interval capacities!
    """
    m = cp_model.CpModel()
    rng = random.Random(seed)
    b_cur_t = [au.get_sub_se(cur_se, b["members"][0])["t"] for b in au.bundles]

    xt = {}
    cand_t_map = {}
    cur_t_lits = []
    for b_id in sorted(free_bundles):
        t0_cur = b_cur_t[b_id]
        cands = au.bundle_allowed_t[b_id]
        if t0_cur not in cands:
            cands = sorted(set(cands) | {t0_cur})
        cand_t_map[b_id] = cands
        lits = []
        for t in cands:
            v = m.NewBoolVar("")
            xt[b_id, t] = v
            lits.append(v)
            if t == t0_cur:
                cur_t_lits.append(v)
                if min_time_diff == 0 or rng.random() < 0.72:
                    m.AddHint(v, 1)
            elif min_time_diff == 0 or rng.random() < 0.72:
                m.AddHint(v, 0)
        m.AddExactlyOne(lits)

    if min_time_diff > 0 and cur_t_lits:
        m.Add(sum(cur_t_lits) <= max(0, len(cur_t_lits) - min_time_diff))

    # Room interval caps (fixed + free bundles)
    bdem = rpools["bundle_demands"]
    fix_pool = collections.defaultdict(lambda: [0] * au.T)
    var_pool = collections.defaultdict(lambda: [[] for _ in range(au.T)])
    for b_id, b in enumerate(au.bundles):
        if not bdem[b_id]:
            continue
        dur = b["dur"]
        if b_id not in free_bundles:
            t0 = b_cur_t[b_id]
            for pset, mult in bdem[b_id].items():
                for q in range(t0, t0 + dur):
                    fix_pool[pset][q] += mult
        else:
            for t in cand_t_map[b_id]:
                v = xt[b_id, t]
                for pset, mult in bdem[b_id].items():
                    for q in range(t, t + dur):
                        var_pool[pset][q].append(mult * v if mult > 1 else v)

    for pset in rpools["disjoint_pools"]:
        cap = len(pset)
        for q in range(au.T):
            if var_pool[pset][q]:
                m.Add(fix_pool[pset][q] + sum(var_pool[pset][q]) <= cap)
    s7, s8, s9 = rpools["s7"], rpools["s8"], rpools["s9"]
    for q in range(au.T):
        if not (var_pool[s7][q] or var_pool[s8][q] or var_pool[s9][q]):
            continue
        e7 = fix_pool[s7][q] + (sum(var_pool[s7][q]) if var_pool[s7][q] else 0)
        e8 = fix_pool[s8][q] + (sum(var_pool[s8][q]) if var_pool[s8][q] else 0)
        e9 = fix_pool[s9][q] + (sum(var_pool[s9][q]) if var_pool[s9][q] else 0)
        m.Add(e7 <= 5)
        m.Add(e8 <= 26)
        m.Add(e7 + e9 <= 30)
        m.Add(e7 + e8 + e9 <= 31)

    # Non-Room resources (Classes + Teachers + preassigned Rooms)
    yr = {}
    fixed_occ = collections.defaultdict(lambda: [0] * au.T)
    var_occ = collections.defaultdict(lambda: collections.defaultdict(list))
    wload_const6 = collections.defaultdict(int)
    wload_terms6 = collections.defaultdict(list)

    for sub_i, info in enumerate(au.subs):
        b_id = au.sub_to_bundle[sub_i]
        s_rec = au.get_sub_se(cur_se, sub_i)
        t_cur_s = s_rec["t"]
        dur = info["dur"]
        eid = info["eid"]
        time_is_free = (b_id in free_bundles)

        for k, er in enumerate(info["ers"]):
            if er["rtype"] == "Room" and er["pre"] is None:
                continue  # Handled by zero-room-var interval capacities!
            cur_r = s_rec["res"][k]
            wl6 = dur * er["workload"] * info["scale6"]

            if er["pre"] is not None:
                cands = [er["pre"]]
            elif er["rtype"] == "Teacher" and (time_is_free or cur_r in free_teachers):
                cands = [r for r in au.allowed_er[eid, k] if (r in free_teachers or r == cur_r)]
            else:
                cands = [cur_r]

            if (not time_is_free) and len(cands) == 1:
                r0 = cands[0]
                if r0 is not None:
                    wload_const6[r0] += wl6
                    for q in range(t_cur_s, t_cur_s + dur):
                        fixed_occ[r0][q] += 1
            elif not time_is_free:
                rlits = []
                for r in cands:
                    un = au.unavail.get(r, ())
                    if any((t_cur_s + off) in un for off in range(dur)):
                        continue
                    rv = m.NewBoolVar("")
                    yr[sub_i, k, r] = rv
                    m.AddHint(rv, 1 if r == cur_r else 0)
                    rlits.append(rv)
                    wload_terms6[r].append(wl6 * rv)
                    for q in range(t_cur_s, t_cur_s + dur):
                        var_occ[r][q].append(rv)
                if not rlits:
                    return cur_se, "EMPTY_RES"
                m.AddExactlyOne(rlits)
            else:
                if len(cands) == 1:
                    r0 = cands[0]
                    wload_const6[r0] += wl6
                    un = au.unavail.get(r0, ())
                    for t in cand_t_map[b_id]:
                        if any((t + off) in un for off in range(dur)):
                            m.Add(xt[b_id, t] == 0)
                        else:
                            for q in range(t, t + dur):
                                var_occ[r0][q].append(xt[b_id, t])
                else:
                    rlits = []
                    for r in cands:
                        rv = m.NewBoolVar("")
                        yr[sub_i, k, r] = rv
                        m.AddHint(rv, 1 if r == cur_r else 0)
                        rlits.append(rv)
                        wload_terms6[r].append(wl6 * rv)
                        un = au.unavail.get(r, ())
                        for t in cand_t_map[b_id]:
                            tv = xt[b_id, t]
                            if any((t + off) in un for off in range(dur)):
                                m.AddBoolOr([rv.Not(), tv.Not()])
                            else:
                                z = m.NewBoolVar("")
                                m.AddBoolAnd([rv, tv]).OnlyEnforceIf(z)
                                m.AddBoolOr([rv.Not(), tv.Not()]).OnlyEnforceIf(z.Not())
                                m.AddHint(z, 1 if (r == cur_r and t == t_cur_s) else 0)
                                for q in range(t, t + dur):
                                    var_occ[r][q].append(z)
                    m.AddExactlyOne(rlits)

    for r in au.clash_res:
        if au.inst.rtype.get(r) == "Room":
            continue
        for q in range(au.T):
            fb = fixed_occ[r][q]
            vl = var_occ[r][q]
            if not vl:
                continue
            if fb >= 1:
                for z in vl:
                    m.Add(z == 0)
            elif len(vl) > 1:
                m.AddAtMostOne(vl)

    for r in au.teachers:
        if not wload_terms6[r]:
            continue
        expr6 = wload_const6[r] + sum(wload_terms6[r])
        if r in au.wload_max6:
            m.Add(expr6 <= au.wload_max6[r])
        if r in au.wload_min6:
            m.Add(expr6 >= au.wload_min6[r])

    obj_terms = []
    for req, w, role, gid, items, pre_set in au.split_rules:
        if not any(any((sub_i, k, r) in yr for r in au.allowed_er[au.subs[sub_i]["eid"], k]) for sub_i, k in items):
            continue
        fixed_r_set = set(pre_set)
        by_r = collections.defaultdict(list)
        for sub_i, k in items:
            eid = au.subs[sub_i]["eid"]
            has_var = False
            for r in au.allowed_er[eid, k]:
                if (sub_i, k, r) in yr:
                    by_r[r].append(yr[sub_i, k, r])
                    has_var = True
            if not has_var:
                cr = au.get_sub_se(cur_se, sub_i)["res"][k]
                if cr is not None:
                    fixed_r_set.add(cr)
        used_vars = []
        for r in sorted(fixed_r_set | set(by_r.keys())):
            if r in fixed_r_set:
                used_vars.append(1)
            else:
                uv = m.NewBoolVar("")
                for lv in by_r[r]:
                    m.Add(uv >= lv)
                m.Add(uv <= sum(by_r[r]))
                used_vars.append(uv)
        if req:
            m.Add(sum(used_vars) <= 1)
        else:
            dev = m.NewIntVar(0, len(used_vars), ""); m.Add(dev >= sum(used_vars) - 1); obj_terms.append(w * dev)

    for req, w, tgs, grps in au.spread_rules:
        for sub_grp in grps:
            if not any(au.sub_to_bundle[sub_i] in free_bundles for sub_i in sub_grp):
                continue
            for ts, lo, hi in tgs:
                cv = sum(1 for sub_i in sub_grp if au.sub_to_bundle[sub_i] not in free_bundles and b_cur_t[au.sub_to_bundle[sub_i]] in ts)
                vl = [xt[au.sub_to_bundle[sub_i], t] for sub_i in sub_grp if au.sub_to_bundle[sub_i] in free_bundles for t in ts if (au.sub_to_bundle[sub_i], t) in xt]
                if not vl:
                    continue
                expr = cv + sum(vl)
                if req:
                    m.Add(expr >= lo); m.Add(expr <= hi)
                else:
                    if cv + len(vl) > hi:
                        ov = m.NewIntVar(0, cv + len(vl), ""); m.Add(ov >= expr - hi); obj_terms.append(w * ov)
                    if lo > 0 and cv < lo:
                        uv = m.NewIntVar(0, lo, ""); m.Add(uv >= lo - expr); obj_terms.append(w * uv)

    for req, w, mn, mx, tgs, res_list in au.busy_rules:
        for r in res_list:
            if not any(var_occ[r][q] for q in range(au.T)):
                continue
            for ts in tgs:
                b_q = []
                for q in ts:
                    if fixed_occ[r][q] >= 1:
                        b_q.append(1)
                    elif var_occ[r][q]:
                        vl = var_occ[r][q]
                        if len(vl) == 1:
                            b_q.append(vl[0])
                        else:
                            bv = m.NewBoolVar(""); m.Add(bv == sum(vl)); b_q.append(bv)
                if len(b_q) > mx:
                    ov = m.NewIntVar(0, len(b_q), ""); m.Add(ov >= sum(b_q) - mx); obj_terms.append(w * ov)

    m.Minimize(sum(obj_terms) if obj_terms else 0)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return cur_se, f"{sv.StatusName(st)}({len(xt)}t,{len(yr)}r)"

    b_times = list(b_cur_t)
    for b_id in free_bundles:
        b_times[b_id] = next(t for t in cand_t_map[b_id] if sv.Value(xt[b_id, t]))
    tmap = {}
    for (sub_i, k, r), rv in yr.items():
        if sv.Value(rv):
            tmap[sub_i, k] = r
    packed_se, r_st = assign_concrete_rooms_au(au, cur_se, b_times, teacher_map=tmap, secs=5.0, workers=workers)
    if packed_se is None:
        return cur_se, f"ROOM_INFEAS({len(xt)}t)"
    return packed_se, f"{sv.StatusName(st)}({len(xt)}t,{len(yr)}r)"


def run_au_v3(total_secs: float = 7200.0, workers: int = 6, seed: int = 1001, mem_gb: float = 5.0):
    lim = int(mem_gb * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    tid = "AU-BG-98"
    t0 = time.time()
    deadline = t0 + total_secs
    os.makedirs(xio.LOGS_DIR, exist_ok=True)
    with open(os.path.join(xio.LOGS_DIR, "active_pids.jsonl"), "a") as pf:
        pf.write(json.dumps({"event": "start", "engine": "AU-v3", "inst": tid, "pid": os.getpid(), "pgid": os.getpgrp(), "secs": total_secs, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}) + "\n")
    _, inst_el, inst, start_se, start_val = xio.load_target(tid)
    au = v1.AUCompiled(inst, start_se)
    rpools = classify_au_room_demands(au)

    cur_se = copy.deepcopy(start_se)
    cur_val = X.evaluate_se(inst, cur_se)[:2]
    best_val = cur_val
    best_se = copy.deepcopy(cur_se)
    print(f"[{tid}] AU-v3 (6w) Start verified: {cur_val[0]}.{cur_val[1]} (budget={total_secs:.0f}s; win <= 0.125)", flush=True)

    def check_record(cand_se, label):
        nonlocal best_val, best_se
        if cand_se is None:
            return None
        cv = X.evaluate_se(inst, cand_se)[:2]
        if cv < best_val:
            print(f"  *** [{tid} {label}] NEW BEST {best_val[0]}.{best_val[1]} -> {cv[0]}.{cv[1]} | {time.time()-t0:.0f}s ***", flush=True)
            best_val = cv
            best_se = copy.deepcopy(cand_se)
            if xio.is_strict_win(tid, best_val):
                wpath = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
                v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"AU-v3 {label} seed={seed}")
                assert v_chk == best_val
                print(f"  *** [{tid}] STRICT WORLD RECORD WIN SAVED & VERIFIED: {best_val[0]}.{best_val[1]} -> {wpath} (sha={sha[:12]}) ***", flush=True)
            else:
                npath = os.path.join(xio.LOGS_DIR, f"NEAR_{tid}_{best_val[0]}_{best_val[1]}.xml")
                v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, npath, desc=f"AU-v3 near-miss {label} seed={seed}")
                assert v_chk == best_val
                print(f"  *** [{tid}] NEAR-MISS (<0.128) SAVED & VERIFIED: {best_val[0]}.{best_val[1]} -> {npath} (sha={sha[:12]}) ***", flush=True)
        return cv

    # =========================================================================
    # HOUR 1 (50% of budget): Whole-School Fixed-Teacher Sniper + 10-Split Loop
    # =========================================================================
    h1_deadline = t0 + total_secs * 0.50

    # Step 1A: Whole-School `371`-Bundle Re-Timing on GOAL's `11`-Split Teachers (`Spread+Busy` sniper!)
    ws_secs = min(180.0, max(15.0, (h1_deadline - time.time()) * 0.12))
    ht0 = [au.get_sub_se(best_se, b["members"][0])["t"] for b in au.bundles]
    cand_ws, st_ws = solve_whole_school_fixed_teachers(au, rpools, best_se, None, secs=ws_secs, workers=workers, seed=seed, hint_times=ht0)
    cv_ws = check_record(cand_ws, f"H1A-WholeSchool({st_ws})")
    print(f"[{tid}] H1A Whole-School Fixed-Teacher ({st_ws}) -> {cv_ws} | {time.time()-t0:.0f}s", flush=True)
    if cand_ws is not None and cv_ws <= cur_val:
        cur_se, cur_val = cand_ws, cv_ws

    # Step 1B: Loop over all 11 split courses, unify 1 (`AvoidSplit <= 100`), solve Whole-School 371-Bundle Time!
    split_depts, _, _, _ = v1.find_split_and_penalty_targets(au, best_se)
    print(f"[{tid}] H1B Testing 10-Split Teacher-First + Whole-School Time across {len(split_depts)} split courses...", flush=True)
    for idx_sp, (gid, used_rs, _, _) in enumerate(split_depts):
        if time.time() + 25.0 >= h1_deadline:
            break
        cands = generate_unify_teacher_candidates(au, best_se, gid, max_cands=2, seed=seed + idx_sp * 71)
        for c_j, (tmap, sp_cost, n_chg) in enumerate(cands):
            if time.time() + 20.0 >= h1_deadline:
                break
            rem_h1 = h1_deadline - time.time()
            per_solve = min(210.0, max(20.0, rem_h1 / max(1, (len(split_depts) - idx_sp))))
            ht_ref = [au.get_sub_se(best_se, b["members"][0])["t"] for b in au.bundles]
            cand_10, st_10 = solve_whole_school_fixed_teachers(
                au, rpools, best_se, tmap, secs=per_solve, workers=workers, seed=seed + idx_sp * 131 + c_j, hint_times=ht_ref,
            )
            cv_10 = check_record(cand_10, f"H1B-Unify({gid}#c{c_j})")
            print(f"  [{tid} H1B {gid}#c{c_j}] split_cost={sp_cost} t_chg={n_chg} -> {st_10} eval={cv_10} | {time.time()-t0:.0f}s", flush=True)
            # If feasible 0-hard and close (`<= 0.132`), polish with Global Teachers + Whole-School!
            if cand_10 is not None and cv_10[0] == 0 and cv_10[1] <= 134 and time.time() + 20.0 < h1_deadline:
                _, _, pm = X.evaluate_se(inst, cand_10)
                t_cap = pm.get(("AvoidSplitAssignmentsConstraint", False), 0) + pm.get(("LimitBusyTimesConstraint", False), 0)
                cand_gt, _ = v2.solve_global_teachers_v2(au, cand_10, max_obj_cap=t_cap, secs=12.0, workers=workers, seed=seed + 999)
                check_record(cand_gt, f"H1B-GT({gid})")

    # =========================================================================
    # HOUR 2 (Remaining 50%): Class-Centric Zero-Room-Var Joint LNS (`~110` bundles, `6w`)
    # =========================================================================
    rng = random.Random(seed + 500)
    cur_se = copy.deepcopy(best_se)
    cur_val = best_val

    # Map each Class resource to all bundles attended by that Class!
    class_bundles = collections.defaultdict(set)
    sub_classes = collections.defaultdict(set)
    for sub_i, info in enumerate(au.subs):
        b_id = au.sub_to_bundle[sub_i]
        for er in info["ers"]:
            if er["pre"] is not None and au.inst.rtype.get(er["pre"]) == "Class":
                class_bundles[er["pre"]].add(b_id)
                sub_classes[sub_i].add(er["pre"])

    step = 0
    improvements = 0
    plateau_moves = 0

    while time.time() + 15.0 < deadline:
        step += 1
        rem = deadline - time.time()
        if step % 7 == 1 and cur_val[1] > best_val[1] + 6:
            cur_se = copy.deepcopy(best_se)
            cur_val = best_val

        split_depts, sb_bundles, sb_teachers, res_bundles = v1.find_split_and_penalty_targets(au, cur_se)
        is_kick = (step % 7 == 4)
        mode = step % 3

        if is_kick:
            mov_b = [b_id for b_id in range(au.B) if au.bundles[b_id]["pre_t"] is None]
            f_bundles = set(rng.sample(mov_b, min(90, len(mov_b))))
            f_teachers = set(rng.sample(au.teachers, 16))
            ntag = "H2_KICK(90b,16T,d>=12)"
            cand_se, st_s = solve_au_zero_room_joint_subproblem(
                au, rpools, cur_se, f_bundles, f_teachers,
                secs=min(30.0, max(5.0, rem - 2.0)), workers=workers, seed=seed + step * 53, min_time_diff=12,
            )
        elif mode == 1 and split_depts:
            # CLASS-CENTRIC SPLIT WINDOW: Unlock 100% of the split course's Class timetable + Dept teachers!
            gid, used_rs, all_cands, b_ids = rng.choice(split_depts)
            cls_involved = {c for b_id in b_ids for sub_i in au.bundles[b_id]["members"] for c in sub_classes[sub_i]}
            f_bundles = set(b_ids)
            for c in cls_involved:
                f_bundles |= {b_id for b_id in class_bundles[c] if au.bundles[b_id]["pre_t"] is None}
            f_teachers = set(all_cands)
            dept_b = [b_id for r in f_teachers for b_id in res_bundles[r] if au.bundles[b_id]["pre_t"] is None and b_id not in f_bundles]
            rng.shuffle(dept_b)
            f_bundles.update(dept_b[:max(0, 108 - len(f_bundles))])
            if len(f_bundles) > 115:
                keep = set(b_ids)
                rest = list(f_bundles - keep)
                rng.shuffle(rest)
                f_bundles = keep | set(rest[:(115 - len(keep))])
            ntag = f"ClassDept({gid[:10]},{len(f_bundles)}b,{len(f_teachers)}T)"
            cand_se, st_s = solve_au_zero_room_joint_subproblem(
                au, rpools, cur_se, f_bundles, f_teachers,
                secs=min(42.0, max(5.0, rem - 2.0)), workers=workers, seed=seed + step * 41, min_time_diff=0,
            )
        elif mode == 2:
            # Whole-School Fixed-Teacher `371`-Bundle Polish on current drifted schedule!
            ht_cur = [au.get_sub_se(cur_se, b["members"][0])["t"] for b in au.bundles]
            ws_cand, st_s = solve_whole_school_fixed_teachers(
                au, rpools, cur_se, None, secs=min(38.0, max(5.0, rem - 8.0)), workers=workers, seed=seed + step * 67, hint_times=ht_cur,
            )
            cand_se = ws_cand if ws_cand is not None else cur_se
            cv_m, _, pm = X.evaluate_se(inst, cand_se)
            if cv_m == 0 and time.time() + 8.0 < deadline:
                t_cap = pm.get(("AvoidSplitAssignmentsConstraint", False), 0) + pm.get(("LimitBusyTimesConstraint", False), 0)
                cand_se2, st_g = v2.solve_global_teachers_v2(au, cand_se, max_obj_cap=t_cap, secs=8.0, workers=workers, seed=seed + step * 99)
                if X.evaluate_se(inst, cand_se2)[:2] <= X.evaluate_se(inst, cand_se)[:2]:
                    cand_se = cand_se2
                    st_s += f"+GT({st_g[:3]})"
            ntag = "WholeSchool371+GT"
        else:
            # Large `110`-Bundle Spread+Busy + Multi-Class Window
            f_bundles = {b_id for b_id in sb_bundles if au.bundles[b_id]["pre_t"] is None}
            f_teachers = set(sb_teachers)
            extra_b = [b_id for b_id in range(au.B) if b_id not in f_bundles and au.bundles[b_id]["pre_t"] is None]
            rng.shuffle(extra_b)
            f_bundles.update(extra_b[:max(0, 108 - len(f_bundles))])
            if len(f_bundles) > 108:
                f_bundles = set(rng.sample(sorted(f_bundles), 108))
            t_in_b = [r for b_id in f_bundles for sub_i in au.bundles[b_id]["members"] for r in au.get_sub_se(cur_se, sub_i)["res"] if r in au.teachers]
            rng.shuffle(t_in_b)
            f_teachers.update(t_in_b[:max(0, 18 - len(f_teachers))])
            ntag = f"SpreadBusy108({len(f_bundles)}b,{len(f_teachers)}T)"
            cand_se, st_s = solve_au_zero_room_joint_subproblem(
                au, rpools, cur_se, f_bundles, f_teachers,
                secs=min(38.0, max(5.0, rem - 2.0)), workers=workers, seed=seed + step * 41, min_time_diff=0,
            )

        cand_val = X.evaluate_se(inst, cand_se)[:2]
        accept = (cand_val <= cur_val) or (is_kick and cand_val[0] == 0 and cand_val[1] <= best_val[1] + 8)
        if accept:
            t_changed = sum(
                1 for sub_i in range(au.S)
                if au.get_sub_se(cand_se, sub_i)["t"] != au.get_sub_se(cur_se, sub_i)["t"]
                or au.get_sub_se(cand_se, sub_i)["res"] != au.get_sub_se(cur_se, sub_i)["res"]
            )
            if cand_val < best_val:
                improvements += 1
            elif cand_val == cur_val and t_changed > 0:
                plateau_moves += 1
            cur_val = cand_val
            cur_se = cand_se
            check_record(cur_se, ntag)

        if step % 3 == 0:
            d_orig = sum(
                1 for sub_i in range(au.S)
                if au.get_sub_se(cur_se, sub_i)["t"] != au.get_sub_se(best_se, sub_i)["t"]
                or au.get_sub_se(cur_se, sub_i)["res"] != au.get_sub_se(best_se, sub_i)["res"]
            )
            print(f"  [{tid} S{step:3d}] {ntag:28s} {st_s:22s} | cur={cur_val[0]}.{cur_val[1]}(d={d_orig}) best={best_val[0]}.{best_val[1]} (imp={improvements}, plat={plateau_moves}) | {time.time()-t0:.0f}s", flush=True)

    win = xio.is_strict_win(tid, best_val)
    win_path, sha = None, None
    if win:
        win_path = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
        v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, win_path, desc=f"AU-v3 seed={seed}")
        assert v_chk == best_val
    else:
        tmp_p = os.path.join(xio.LOGS_DIR, f"_chk_{tid}_{os.getpid()}.xml")
        v_chk, _, _ = xio.write_and_verify_xml(inst_el, inst, best_se, tmp_p, desc="check")
        os.remove(tmp_p)
        assert v_chk == best_val

    with open(os.path.join(xio.LOGS_DIR, "active_pids.jsonl"), "a") as pf:
        pf.write(json.dumps({"event": "done", "engine": "AU-v3", "inst": tid, "pid": os.getpid(), "pgid": os.getpgrp(), "best": list(best_val), "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}) + "\n")
    return dict(
        engine="AU-v3_6w_zero_room_twophase", inst=tid,
        record=list(start_val), best=list(best_val), win=win,
        steps=step, improvements=improvements, plateau_moves=plateau_moves,
        win_path=win_path, sha256=sha, secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--secs", type=float, default=7200.0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--seed", type=int, default=1001)
    parser.add_argument("--out-json", type=str, default="")
    args = parser.parse_args()

    res = run_au_v3(total_secs=args.secs, workers=args.workers, seed=args.seed)
    if args.out_json:
        open(args.out_json, "w").write(json.dumps(res))
    else:
        print(json.dumps(res, indent=2), flush=True)


if __name__ == "__main__":
    main()
