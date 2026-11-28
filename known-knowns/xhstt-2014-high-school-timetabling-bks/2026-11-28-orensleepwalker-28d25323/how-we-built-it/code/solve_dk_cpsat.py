"""
XHSTT Danish Lectio Subproblem CP-SAT Engine DK-v1 (`DK-HG-12` & `DK-VG-09`)
(scans/2026-11-27-xhstt-charlie/solve_dk_cpsat.py)

Exploits exact structural properties discovered in Step 1 Dissection:
  1. 100% of events in DK-HG-12 (1,235) and DK-VG-09 (918) have `dur == 1` and 100% preassigned
     Teacher & Student resources; ONLY `RoleRoom` (`Room`) and `Time` are decision variables.
  2. Rooms have ZERO cross-slot constraints (`AvoidClashes`, `AssignResource`, `PreferResources` only):
     - In `DK-VG-09`, all 918 events share the exact same 52-room pool (`sum_e x[e, q] <= 52` is 100%
       necessary & sufficient for exact 0-penalty room assignment — ZERO room variables in CP-SAT!).
     - In `DK-HG-12`, 5 events have empty allowed room set (`len == 0`, unavoidable +5 hard), ~65% use
       the general 70-room pool, and ~35% use specialized `{1..31}` room sets. Inside unlocked slots `q`,
       we model exact bipartite room matching ONLY on active slots (plus total room cap) and run exact
       `scipy.optimize.linear_sum_assignment` on modified slots afterward!
  3. Exact linear `LimitIdleTimes` (`idle = sum_p (pref[p] + suff[p] - any_d - b[p])`), exact
     `ClusterBusyTimes`, `LimitBusyTimes`, `SpreadEvents`, `AvoidClashes`, and `AssignTime`!
  4. Rotates 3 complementary LNS neighborhoods:
     - `N1_DayPair`: Unlocks 2 days (`10-12` slots, ~220 events) + all untimed/clashing events.
     - `N2_EdgePeriods`: Unlocks `10-12` first/last/scattered periods across days (directly compressing
       Student/Teacher `Idle` and `ClusterBusy` day spans!).
     - `N3_EventCluster`: Unlocks `80-110` high-penalty events across ALL `50-60` time slots!
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

import numpy as np
from ortools.sat.python import cp_model
from scipy.optimize import linear_sum_assignment

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CHARLIE_DIR)
import xhstt_io as xio  # noqa: E402
from xhstt_io import X  # noqa: E402


class DKCompiled:
    """Precompiles DK-HG-12 / DK-VG-09 static constraint structures for ultra-fast subproblem building."""

    def __init__(self, inst):
        self.inst = inst
        self.T = len(inst.times)
        self.eids = list(inst.eorder)
        self.E = len(self.eids)
        self.eix = {e: i for i, e in enumerate(self.eids)}

        self.rooms = [r for r, rt in inst.rtype.items() if rt == "Room"]
        self.R_cnt = len(self.rooms)
        self.rix = {r: i for i, r in enumerate(self.rooms)}

        # Preassigned non-Room resources (Teachers & Students) per event
        self.ev_fixed_res = []
        self.res_events = collections.defaultdict(list)
        self.room_role_idx = []
        for i, eid in enumerate(self.eids):
            ie = inst.events[eid]
            assert ie["dur"] == 1 and ie["pre_t"] is None
            f_res = []
            r_k = None
            for k, er in enumerate(ie["ers"]):
                if er["pre"] is not None:
                    f_res.append(er["pre"])
                    self.res_events[er["pre"]].append(i)
                elif er["role"] == "RoleRoom":
                    r_k = k
            assert r_k is not None
            self.ev_fixed_res.append(f_res)
            self.room_role_idx.append(r_k)

        # Allowed rooms per event (intersection of PreferResourcesConstraint W=1000)
        allowed = [set(self.rooms) for _ in range(self.E)]
        for c in inst.constraints:
            if c.tag == "PreferResourcesConstraint" and X.txt(c, "Role") == "RoleRoom" and X.txt(c, "Required") == "true":
                pref = set()
                rgs = c.find("ResourceGroups")
                if rgs is not None:
                    for g in rgs:
                        pref |= set(inst.rgroups[g.attrib["Reference"]])
                rs = c.find("Resources")
                if rs is not None:
                    pref |= {r.attrib["Reference"] for r in rs}
                for eid in inst.events_of(c.find("AppliesTo")):
                    allowed[self.eix[eid]] &= pref
        self.allowed_rooms = [sorted( self.rix[r] for r in allowed[i] ) for i in range(self.E)]
        distinct_nonempty = {tuple(a) for a in self.allowed_rooms if a}
        self.uniform_rooms = (len(distinct_nonempty) == 1 and all(len(a) > 0 for a in self.allowed_rooms))
        self.uniform_pool = list(next(iter(distinct_nonempty))) if self.uniform_rooms else None

        # Parse all constraints into fast indexed structures
        self.spread_rules = []   # (req, w, [(ts_set, lo, hi)], [ev_indices])
        self.clash_res = set()
        self.idle_rules = []     # (req, w, mn, mx, [sorted_ts_list], [res_ids])
        self.cluster_rules = []  # (req, w, mn, mx, [sorted_ts_list], [res_ids])
        self.busy_rules = []     # (req, w, mn, mx, [sorted_ts_list], [res_ids])
        self.assign_time_w = 1
        self.assign_res_w = 1

        for c in inst.constraints:
            k = c.tag
            req = X.txt(c, "Required") == "true"
            w = int(X.txt(c, "Weight"))
            ap = c.find("AppliesTo")
            mn = X.txt(c, "Minimum"); mn = int(mn) if mn is not None else None
            mx = X.txt(c, "Maximum"); mx = int(mx) if mx is not None else None
            if k == "AssignTimeConstraint":
                self.assign_time_w = w
            elif k == "AssignResourceConstraint":
                self.assign_res_w = w
            elif k == "PreferResourcesConstraint":
                pass
            elif k == "SpreadEventsConstraint":
                tgs = [(set(inst.tgroups[g.attrib["Reference"]]), int(X.txt(g, "Minimum")), int(X.txt(g, "Maximum"))) for g in c.find("TimeGroups")]
                grps = [[self.eix[eid] for eid in inst.egroups[g.attrib["Reference"]]] for g in ap.find("EventGroups")]
                self.spread_rules.append((req, w, tgs, grps))
            elif k == "AvoidClashesConstraint":
                for r in inst.resources_of(ap):
                    if inst.rtype[r] != "Room":
                        self.clash_res.add(r)
            elif k == "LimitIdleTimesConstraint":
                tgs = [sorted(inst.tgroups[g.attrib["Reference"]]) for g in c.find("TimeGroups")]
                self.idle_rules.append((req, w, mn, mx, tgs, inst.resources_of(ap)))
            elif k == "ClusterBusyTimesConstraint":
                tgs = [sorted(inst.tgroups[g.attrib["Reference"]]) for g in c.find("TimeGroups")]
                self.cluster_rules.append((req, w, mn, mx, tgs, inst.resources_of(ap)))
            elif k == "LimitBusyTimesConstraint":
                tgs = [sorted(inst.tgroups[g.attrib["Reference"]]) for g in c.find("TimeGroups")]
                self.busy_rules.append((req, w, mn, mx, tgs, inst.resources_of(ap)))
            else:
                raise ValueError(f"Unexpected DK constraint: {k}")

        # Identify days (contiguous blocks of 5 or 6 periods: D1..D10)
        self.days = [sorted(inst.tgroups[f"D{d}"]) for d in range(1, 11) if f"D{d}" in inst.tgroups]

    def extract_state(self, se):
        t_arr = [se[eid][0]["t"] for eid in self.eids]
        return t_arr

    def assign_rooms_slot(self, evs_in_slot):
        """Exact min-unassigned bipartite room matching for a single slot `q`."""
        if not evs_in_slot:
            return {}
        if self.uniform_rooms:
            pool = self.uniform_pool
            out = {}
            for idx, e_i in enumerate(evs_in_slot):
                out[e_i] = self.rooms[pool[idx]] if idx < len(pool) else None
            return out
        valid_evs = [e_i for e_i in evs_in_slot if self.allowed_rooms[e_i]]
        out = {e_i: None for e_i in evs_in_slot}
        if not valid_evs:
            return out
        BIG = 10000
        cost = np.full((len(valid_evs), self.R_cnt), BIG, dtype=np.int32)
        for row, e_i in enumerate(valid_evs):
            for r_i in self.allowed_rooms[e_i]:
                cost[row, r_i] = 0
        ri, ci = linear_sum_assignment(cost)
        for row, col in zip(ri, ci):
            if cost[row, col] == 0:
                out[valid_evs[row]] = self.rooms[col]
        return out

    def build_se_from_times(self, base_se, t_arr, changed_slots=None):
        """Reconstruct `se` and re-solve exact room matching on changed slots."""
        new_se = copy.deepcopy(base_se)
        by_slot = collections.defaultdict(list)
        for e_i, eid in enumerate(self.eids):
            tq = t_arr[e_i]
            new_se[eid][0]["t"] = tq
            if tq is None:
                # Untimed events do NOT occupy busy[room][q], so assign any allowed room to avoid +1 AssignResource!
                ar = self.allowed_rooms[e_i]
                new_se[eid][0]["res"][self.room_role_idx[e_i]] = self.rooms[ar[0]] if ar else None
            else:
                by_slot[tq].append(e_i)

        slots_to_match = range(self.T) if changed_slots is None else changed_slots
        for q in slots_to_match:
            rmap = self.assign_rooms_slot(by_slot[q])
            for e_i in by_slot[q]:
                eid = self.eids[e_i]
                new_se[eid][0]["res"][self.room_role_idx[e_i]] = rmap[e_i]
        return new_se


def solve_dk_subproblem(
    dk: DKCompiled, t_cur: list, free_evs: set, allowed_slots: set,
    cur_hard: int, secs: float = 8.0, workers: int = 2, seed: int = 1,
    allow_untimed: bool = True, min_diff: int = 0, hint_keep_prob: float = 1.0,
):
    """
    Exact Domain-Reduced Subproblem CP-SAT over `free_evs` and `allowed_slots`.
    Events outside `free_evs` stay fixed at `t_cur[e]`.
    """
    rng = random.Random(seed)
    free_list = sorted(free_evs)
    if not free_list:
        return t_cur, "EMPTY"
    slot_list = sorted(allowed_slots)
    slot_set = set(slot_list)

    # Precompute fixed busy counts `fixed_busy[r][q]` for all non-Room resources r
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
    x = {}          # (e_i, q) -> BoolVar
    u_var = {}      # e_i -> BoolVar (1 if untimed)
    ev_slots = {e_i: [] for e_i in free_list}
    slot_evs = {q: [] for q in slot_list}
    cur_lits = []

    for e_i in free_list:
        tq_cur = t_cur[e_i]
        # Ensure current slot of e_i is always an option if timed!
        cand_q = slot_list if (tq_cur is None or tq_cur in slot_set) else sorted(slot_set | {tq_cur})
        lits = []
        for q in cand_q:
            # Prune slots where a fixed event ALREADY uses one of e_i's clash resources (unless cur_hard allows clashes? No, never create new clashes on clash-free resources!)
            if any(fixed_busy[r][q] >= 1 for r in dk.ev_fixed_res[e_i] if r in dk.clash_res):
                if q != tq_cur:
                    continue
            v = m.NewBoolVar("")
            x[e_i, q] = v
            ev_slots[e_i].append((q, v))
            slot_evs.setdefault(q, []).append((e_i, v))
            lits.append(v)
            is_c = (tq_cur == q)
            if is_c:
                cur_lits.append(v)
            if hint_keep_prob > 0 and (hint_keep_prob >= 1.0 or rng.random() < hint_keep_prob):
                m.AddHint(v, 1 if is_c else 0)

        if allow_untimed or tq_cur is None or not lits:
            uv = m.NewBoolVar("")
            u_var[e_i] = uv
            lits.append(uv)
            if hint_keep_prob > 0 and (hint_keep_prob >= 1.0 or rng.random() < hint_keep_prob):
                m.AddHint(uv, 1 if tq_cur is None else 0)
        m.AddExactlyOne(lits)

    if min_diff > 0 and cur_lits:
        m.Add(sum(cur_lits) <= max(0, len(cur_lits) - min_diff))

    hard_terms = []
    soft_terms = []

    # 1. AssignTime hard cost (for free events; fixed untimed count is constant)
    fixed_untimed = sum(1 for e_i in range(dk.E) if e_i not in free_evs and t_cur[e_i] is None)
    if u_var:
        hard_terms.append(dk.assign_time_w * sum(u_var.values()))
    const_hard = dk.assign_time_w * fixed_untimed

    # 2. Room Matching / Capacity in touched slots!
    touched_slots = sorted(slot_evs.keys())
    if dk.uniform_rooms:
        cap = len(dk.uniform_pool)
        for q in touched_slots:
            rem_cap = cap - fixed_in_slot[q]
            expr = sum(v for _, v in slot_evs[q])
            if rem_cap >= len(slot_evs[q]):
                continue
            ov = m.NewIntVar(0, len(slot_evs[q]), "")
            m.Add(ov >= expr - max(0, rem_cap))
            hard_terms.append(dk.assign_res_w * ov)
        # Fixed slots untouched: uniform rooms had 0 unmatched in best_sol
    else:
        # DK-HG-12: Events with empty `allowed_rooms` ALWAYS pay +1 AssignResource whether timed or untimed!
        const_hard += dk.assign_res_w * sum(1 for e_i in range(dk.E) if len(dk.allowed_rooms[e_i]) == 0)

        untouched_set = set(range(dk.T)) - set(touched_slots)
        for q in untouched_set:
            nonempty_fix = [e_i for e_i in fixed_evs_by_slot[q] if len(dk.allowed_rooms[e_i]) > 0]
            rmap = dk.assign_rooms_slot(nonempty_fix)
            const_hard += dk.assign_res_w * sum(1 for r in rmap.values() if r is None)

        s70 = max((set(a) for a in dk.allowed_rooms if a), key=len)
        for q in touched_slots:
            fix_evs = fixed_evs_by_slot[q]
            # Specialized events (0 < len < len(s70)) in slot q (both fixed and free!)
            fix_spec = [e_i for e_i in fix_evs if 0 < len(dk.allowed_rooms[e_i]) < len(s70)]
            free_spec = [(e_i, v) for e_i, v in slot_evs[q] if 0 < len(dk.allowed_rooms[e_i]) < len(s70)]
            fix_gen_cnt = sum(1 for e_i in fix_evs if set(dk.allowed_rooms[e_i]) == s70)
            free_gen_lits = [v for e_i, v in slot_evs[q] if set(dk.allowed_rooms[e_i]) == s70]

            # Exact bipartite room variables for specialized events in slot q (`<= ~15` events x `~6` rooms = tiny!)
            r_used_in_s70 = []
            room_lits_by_r = collections.defaultdict(list)
            for e_i in fix_spec:
                rl = []
                for r_i in dk.allowed_rooms[e_i]:
                    rv = m.NewBoolVar("")
                    rl.append(rv)
                    room_lits_by_r[r_i].append(rv)
                    if r_i in s70:
                        r_used_in_s70.append(rv)
                unm = m.NewBoolVar("")
                m.AddExactlyOne(rl + [unm])
                hard_terms.append(dk.assign_res_w * unm)

            for e_i, v in free_spec:
                rl = []
                for r_i in dk.allowed_rooms[e_i]:
                    rv = m.NewBoolVar("")
                    m.Add(rv <= v)
                    rl.append(rv)
                    room_lits_by_r[r_i].append(rv)
                    if r_i in s70:
                        r_used_in_s70.append(rv)
                unm = m.NewBoolVar("")
                m.Add(sum(rl) + unm == v)
                hard_terms.append(dk.assign_res_w * unm)

            for r_i, r_lits in room_lits_by_r.items():
                if len(r_lits) > 1:
                    m.AddAtMostOne(r_lits)

            # General s70 pool capacity: fix_gen_cnt + sum(free_gen_lits) + sum(r_used_in_s70) <= len(s70) + ov
            tot_s70_ub = fix_gen_cnt + len(free_gen_lits) + len(r_used_in_s70)
            if tot_s70_ub > len(s70):
                ov = m.NewIntVar(0, tot_s70_ub, "")
                m.Add(ov >= fix_gen_cnt + sum(free_gen_lits) + sum(r_used_in_s70) - len(s70))
                hard_terms.append(dk.assign_res_w * ov)

    # Identify all non-Room resources `r` that have at least 1 free event in `free_evs`
    active_res = set()
    free_evs_of_res = collections.defaultdict(list)
    for e_i in free_list:
        for r in dk.ev_fixed_res[e_i]:
            active_res.add(r)
            free_evs_of_res[r].append(e_i)

    # 3. AvoidClashesConstraint (Req=True, W=1) + Busy indicator `b_ind[r, q]` (`1` iff resource `r` attends >=1 event at `q`)
    # First add fixed clashes on inactive resources or untouched slots
    b_ind = {}  # (r, q) -> int (0/1) or BoolVar
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
            else:
                if fb == 0 and len(lits) == 1:
                    b_ind[r, q] = lits[0]
                elif fb >= 1:
                    # fb >= 1 so resource r is ALREADY busy at q; any extra lit is a clash!
                    b_ind[r, q] = 1
                    const_hard += (fb - 1)
                    hard_terms.extend(lits)
                else:
                    # fb == 0, len(lits) >= 2: if cur_hard == 2 (DK-VG-09 has 0 clashes!), forbid clashes outright for speed;
                    # on DK-HG-12 allow slack `cl` only if needed, or forbid new clashes on currently clash-free slots!
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

    # 4. SpreadEventsConstraint
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

    # 5. LimitIdleTimesConstraint (exact linear `pref + suff - any_d - b` per day!)
    for req, w, mn, mx, tgs, res_list in dk.idle_rules:
        assert (mn in (None, 0)) and (mx == 0)  # Verified in dissection: min=0, max=0 on both DK-HG-12 & DK-VG-09!
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
                    v_only = [z for z in b_seq if not isinstance(z, int)]
                    m.AddMaxEquality(any_d, v_only)

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
                            m.Add(pv >= pref[p - 1])
                            m.Add(pv >= b_seq[p])
                            m.Add(pv <= pref[p - 1] + b_seq[p])
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
                            m.Add(sv_p >= suff[p + 1])
                            m.Add(sv_p >= b_seq[p])
                            m.Add(sv_p <= suff[p + 1] + b_seq[p])
                    suff[p] = sv_p

                idle_expr = sum(pref) + sum(suff) - P * any_d - sum(b_seq)
                target_list.append(w * idle_expr)

    # 6. ClusterBusyTimesConstraint
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
                elif all(isinstance(z, int) for z in b_seq):
                    pass
                else:
                    v_only = [z for z in b_seq if not isinstance(z, int)]
                    if len(v_only) == 1:
                        day_vars.append(v_only[0])
                    else:
                        dv = m.NewBoolVar("")
                        m.AddMaxEquality(dv, v_only)
                        day_vars.append(dv)
            add_dev_cost(const_days, day_vars, len(day_vars), mn, mx, req, w)

    # 7. LimitBusyTimesConstraint (IMPORTANT: in XHSTT spec & xhstt_eval.py line 224: `if m: d += out(m)` — only applies when day is BUSY `m > 0`!)
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
                    ov = m.NewIntVar(0, P, "")
                    m.Add(ov >= m_sum - mx)
                    target_list.append(w * ov)
                if mn is not None and mn > 0:
                    # Penalty is `mn - m_sum` ONLY when `m_sum >= 1` (`any_d == 1`)!
                    if any(z == 1 for z in b_seq if isinstance(z, int)):
                        uv = m.NewIntVar(0, mn, "")
                        m.Add(uv >= mn - m_sum)
                        target_list.append(w * uv)
                    else:
                        v_only = [z for z in b_seq if not isinstance(z, int)]
                        any_d = m.NewBoolVar("")
                        m.AddMaxEquality(any_d, v_only)
                        uv = m.NewIntVar(0, mn, "")
                        m.Add(uv >= mn * any_d - m_sum)
                        target_list.append(w * uv)

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


def event_penalty_weights(dk: DKCompiled, t_cur: list):
    """Score events by involvement in untimed/clash/idle/cluster/spread violations to focus N3."""
    sc = [1.0] * dk.E
    res_busy = collections.defaultdict(lambda: [0] * dk.T)
    for e_i, tq in enumerate(t_cur):
        if tq is None:
            sc[e_i] += 500.0
        else:
            for r in dk.ev_fixed_res[e_i]:
                res_busy[r][tq] += 1
    for e_i, tq in enumerate(t_cur):
        if tq is not None:
            for r in dk.ev_fixed_res[e_i]:
                if r in dk.clash_res and res_busy[r][tq] > 1:
                    sc[e_i] += 500.0
    # Idle & busy contributions
    bad_res_slots = collections.defaultdict(float)
    for _, w, _, _, tgs, res_list in dk.idle_rules:
        for r in res_list:
            b = res_busy[r]
            for ts in tgs:
                bt = [i for i, q in enumerate(ts) if b[q] > 0]
                if bt and (bt[-1] - bt[0] + 1 - len(bt)) > 0:
                    # Edge events on day with idle gap are prime candidates to move!
                    bad_res_slots[r, ts[bt[0]]] += w * 2.0
                    bad_res_slots[r, ts[bt[-1]]] += w * 2.0
    for _, w, tgs, grps in dk.spread_rules:
        for ev_grp in grps:
            for ts, lo, hi in tgs:
                c = sum(1 for e_i in ev_grp if t_cur[e_i] in ts)
                if c < lo or c > hi:
                    for e_i in ev_grp:
                        sc[e_i] += w * 2.0
    for e_i, tq in enumerate(t_cur):
        if tq is not None:
            for r in dk.ev_fixed_res[e_i]:
                sc[e_i] += bad_res_slots.get((r, tq), 0.0)
    return sc


def run_dk(tid: str, total_secs: float = 1200.0, workers: int = 2, seed: int = 101, mem_gb: float = 4.5):
    lim = int(mem_gb * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    deadline = t0 + total_secs
    _, inst_el, inst, start_se, start_val = xio.load_target(tid)
    dk = DKCompiled(inst)

    t_cur = dk.extract_state(start_se)
    cur_se = dk.build_se_from_times(start_se, t_cur)
    cur_val = X.evaluate_se(inst, cur_se)[:2]
    assert cur_val <= start_val, f"{tid} init mismatch: {cur_val} vs {start_val}"
    print(f"[{tid}] DK-v1 Start verified: {cur_val[0]}.{cur_val[1]} (target <= {xio.TARGETS[tid]['win_max']})", flush=True)

    best_val = cur_val
    best_se = copy.deepcopy(cur_se)
    best_t = list(t_cur)
    rng = random.Random(seed)

    step = 0
    plateau_moves = 0
    improvements = 0

    while time.time() + 6.0 < deadline:
        step += 1
        rem = deadline - time.time()
        mode = step % 4

        # Always include untimed & clashing events in free set so hard violations can clear at any step!
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

        if mode == 1:
            # N1: Unlock 2 full days (`10-12` slots)
            d_pair = rng.sample(dk.days, 2)
            sl = set(d_pair[0]) | set(d_pair[1])
            fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
            s_lim = min(14.0, max(3.0, rem - 2.0))
            ntag = "N1_2Days"
        elif mode == 2:
            # N2: Edge periods (first & last period of 5-6 days -> crushes LimitIdle & Cluster!)
            days_sub = rng.sample(dk.days, min(6, len(dk.days)))
            sl = set()
            for d_slots in days_sub:
                sl.add(d_slots[0])
                sl.add(d_slots[-1])
            fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
            s_lim = min(12.0, max(3.0, rem - 2.0))
            ntag = "N2_Edges"
        elif mode == 3:
            # N3: Penalty-biased cluster of ~85 events unlocked across ALL 50-60 slots!
            sc = event_penalty_weights(dk, t_cur)
            ranked = sorted(range(dk.E), key=lambda i: sc[i] * (0.6 + 0.8 * rng.random()), reverse=True)
            k_ev = 90 if dk.T == 60 else 80
            fe = set(ranked[:k_ev]) | broken_evs
            sl = set(range(dk.T))
            s_lim = min(14.0, max(3.0, rem - 2.0))
            ntag = f"N3_AllSlots({len(fe)}e)"
        else:
            # N4: Scattered 10-12 slots across week
            k_sl = 12 if dk.T == 60 else 10
            sl = set(rng.sample(range(dk.T), k_sl))
            fe = {e_i for e_i, tq in enumerate(t_cur) if tq in sl} | broken_evs
            s_lim = min(12.0, max(3.0, rem - 2.0))
            ntag = f"N4_Rand{k_sl}Slots"

        cand_t, st_info = solve_dk_subproblem(
            dk, t_cur, fe, sl, cur_hard=cur_val[0],
            secs=s_lim, workers=workers, seed=seed + step * 37,
            allow_untimed=True, min_diff=0, hint_keep_prob=1.0,
        )

        diff = sum(1 for a, b in zip(cand_t, t_cur) if a != b)
        if diff > 0:
            changed_q = {q for a, b in zip(cand_t, t_cur) if a != b for q in (a, b) if q is not None}
            cand_se = dk.build_se_from_times(cur_se, cand_t, changed_slots=changed_q)
            cand_val = X.evaluate_se(inst, cand_se)[:2]
            if cand_val <= cur_val:
                if cand_val < cur_val:
                    improvements += 1
                    print(f"  [{tid} S{step:3d} {ntag} {st_info}] IMPROVED {cur_val[0]}.{cur_val[1]} -> {cand_val[0]}.{cand_val[1]} (diff={diff}) | {time.time()-t0:.0f}s", flush=True)
                else:
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
                        v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"DK-v1 {ntag} seed={seed}")
                        assert v_chk == best_val
                        print(f"  *** [{tid}] STRICT WORLD RECORD WIN SAVED & VERIFIED: {best_val[0]}.{best_val[1]} -> {wpath} (sha={sha[:12]}) ***", flush=True)

        if step % 6 == 0:
            print(f"  [{tid} S{step:3d}] {ntag} {st_info} | cur={cur_val[0]}.{cur_val[1]} best={best_val[0]}.{best_val[1]} (imp={improvements}, plat={plateau_moves}) | {time.time()-t0:.0f}s", flush=True)

    win = xio.is_strict_win(tid, best_val)
    win_path, sha = None, None
    if win:
        win_path = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
        v_chk, per, sha = xio.write_and_verify_xml(inst_el, inst, best_se, win_path, desc=f"DK-v1 seed={seed}")
        assert v_chk == best_val
    else:
        tmp_p = os.path.join(xio.LOGS_DIR, f"_chk_{tid}_{os.getpid()}.xml")
        v_chk, per, _ = xio.write_and_verify_xml(inst_el, inst, best_se, tmp_p, desc="check")
        os.remove(tmp_p)
        assert v_chk == best_val

    return dict(
        engine="DK-v1_subproblem_cpsat", inst=tid,
        record=list(start_val), best=list(best_val), win=win,
        steps=step, improvements=improvements, plateau_moves=plateau_moves,
        diff_events=sum(1 for a, b in zip(best_t, dk.extract_state(start_se)) if a != b),
        win_path=win_path, sha256=sha, secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inst", choices=["DK-HG-12", "DK-VG-09"], required=True)
    parser.add_argument("--secs", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--out-json", type=str, default="")
    args = parser.parse_args()

    res = run_dk(args.inst, total_secs=args.secs, workers=args.workers, seed=args.seed)
    if args.out_json:
        open(args.out_json, "w").write(json.dumps(res))
    else:
        print(json.dumps(res, indent=2), flush=True)


if __name__ == "__main__":
    main()
