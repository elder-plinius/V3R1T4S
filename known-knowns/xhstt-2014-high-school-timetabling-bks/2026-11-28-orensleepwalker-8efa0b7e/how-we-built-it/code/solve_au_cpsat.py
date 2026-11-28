"""
XHSTT AU-BG-98 Joint `(LinkBundle Time + Teacher + Room)` Subproblem CP-SAT Engine AU-v1
(scans/2026-11-27-xhstt-charlie/solve_au_cpsat.py)

Targets AU-BG-98 (`0.128` stored / `0.126` overview -> win needs `0.125` or lower):
  - `128 = AvoidSplitAssignments (110 = 11 splits x 10) + LimitBusyTimes (10 = 5 x 2) + SpreadEvents (8 = 8 x 1)`.
  - Preserves 100% of `SplitEvents`, `DistributeSplitEvents`, and `LinkEvents` by grouping co-timed
    linked sub-events into atomic `LinkBundles` moving in lockstep.
  - Uses exact integer x6 workload scaling (`lcm(1,2,3) = 6`) for `LimitWorkloadConstraint` (`0` float error).
  - Combines:
    1. `solve_global_teachers`: Exact school-wide Teacher Assignment CP-SAT across all 1,047 sub-events
       and 56 teachers at fixed lesson times (solves in ~2-8s!).
    2. `solve_au_joint_subproblem`: Joint `(Time + Teacher + Room)` CP-SAT over `35-55` `LinkBundles`
       and `8-14` department teachers, rotating:
       - `AU-N1 (SplitDept)`: Targets 1-2 of the 11 split courses + department teachers + their bundles.
       - `AU-N2 (SpreadBusy)`: Targets the 8 `SpreadEvents` + 10 `LimitBusyTimes` points directly (shaving
         just 3 points reaches `0.125`!).
       - `AU-N3 (PlateauRetime + GlobalTeachers)`: Drifts 45 bundles on equal-or-better score, then runs
         school-wide `solve_global_teachers` to check if any split course can unify!
"""
import argparse
import collections
import copy
import json
import math
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


class AUCompiled:
    def __init__(self, inst, start_se):
        self.inst = inst
        self.T = len(inst.times)
        self.teachers = [r for r, rt in inst.rtype.items() if rt == "Teacher"]
        self.rooms = [r for r, rt in inst.rtype.items() if rt == "Room"]
        self.classes = [r for r, rt in inst.rtype.items() if rt == "Class"]

        self.lcm_dur = math.lcm(*(ie["dur"] for ie in inst.events.values()))

        # Flatten all 1,047 sub-events into indexed records: `sub_i -> (eid, sub_pos, dur, scaleL)`
        self.subs = []
        self.eid_to_subs = collections.defaultdict(list)
        for eid in inst.eorder:
            ie = inst.events[eid]
            for pos, s in enumerate(start_se[eid]):
                sub_i = len(self.subs)
                self.subs.append(dict(
                    sub_i=sub_i, eid=eid, pos=pos, dur=s["dur"], pre_t=ie["pre_t"],
                    ers=ie["ers"], scale6=self.lcm_dur // ie["dur"],
                ))
                self.eid_to_subs[eid].append(sub_i)
        self.S = len(self.subs)

        # Build atomic LinkBundles via Union-Find on sub-events sharing a LinkEventsConstraint & (t, dur)
        parent = list(range(self.S))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for c in inst.constraints:
            if c.tag == "LinkEventsConstraint":
                for g in c.find("AppliesTo").find("EventGroups"):
                    eids = inst.egroups[g.attrib["Reference"]]
                    if len(eids) < 2:
                        continue
                    ref_subs = sorted(self.eid_to_subs[eids[0]], key=lambda i: start_se[self.subs[i]["eid"]][self.subs[i]["pos"]]["t"])
                    for other_eid in eids[1:]:
                        oth_subs = sorted(self.eid_to_subs[other_eid], key=lambda i: start_se[self.subs[i]["eid"]][self.subs[i]["pos"]]["t"])
                        assert len(ref_subs) == len(oth_subs)
                        for a, b in zip(ref_subs, oth_subs):
                            assert self.subs[a]["dur"] == self.subs[b]["dur"]
                            union(a, b)

        b_map = collections.defaultdict(list)
        for sub_i in range(self.S):
            b_map[find(sub_i)].append(sub_i)
        self.bundles = []
        self.sub_to_bundle = [0] * self.S
        for members in b_map.values():
            b_id = len(self.bundles)
            dur = self.subs[members[0]]["dur"]
            pre_ts = {self.subs[i]["pre_t"] for i in members if self.subs[i]["pre_t"] is not None}
            assert len(pre_ts) <= 1
            pre_t = next(iter(pre_ts)) if pre_ts else None
            self.bundles.append(dict(b_id=b_id, members=members, dur=dur, pre_t=pre_t))
            for i in members:
                self.sub_to_bundle[i] = b_id
        self.B = len(self.bundles)

        # Allowed start times per bundle (from PreferTimesConstraint Req=True & horizon)
        pref_times_by_eid_dur = {}
        for c in inst.constraints:
            if c.tag == "PreferTimesConstraint" and X.txt(c, "Required") == "true":
                ts = inst.timeset(c)
                dd = X.txt(c, "Duration"); dd = int(dd) if dd is not None else None
                for eid in inst.events_of(c.find("AppliesTo")):
                    pref_times_by_eid_dur.setdefault((eid, dd), set(range(self.T)))
                    pref_times_by_eid_dur[eid, dd] &= ts

        # Unavailable times per resource (Req=True)
        self.unavail = collections.defaultdict(set)
        for c in inst.constraints:
            if c.tag == "AvoidUnavailableTimesConstraint" and X.txt(c, "Required") == "true":
                un = inst.timeset(c)
                for r in inst.resources_of(c.find("AppliesTo")):
                    self.unavail[r] |= un

        self.bundle_allowed_t = []
        for b in self.bundles:
            dur = b["dur"]
            if b["pre_t"] is not None:
                self.bundle_allowed_t.append([b["pre_t"]])
                continue
            valid = set(range(0, self.T - dur + 1))
            for sub_i in b["members"]:
                eid = self.subs[sub_i]["eid"]
                if (eid, None) in pref_times_by_eid_dur:
                    valid &= pref_times_by_eid_dur[eid, None]
                if (eid, dur) in pref_times_by_eid_dur:
                    valid &= pref_times_by_eid_dur[eid, dur]
                # Preassigned resources cannot hit unavailable times
                for er in self.subs[sub_i]["ers"]:
                    if er["pre"] is not None and er["pre"] in self.unavail:
                        un = self.unavail[er["pre"]]
                        valid = {t for t in valid if not any((t + off) in un for off in range(dur))}
            self.bundle_allowed_t.append(sorted(valid))

        # Allowed resources per `(eid, k)` slot (PreferResourcesConstraint Req=True)
        by_type = collections.defaultdict(list)
        for r, rt in inst.rtype.items():
            by_type[rt].append(r)

        allowed_er = {}
        for eid, ie in inst.events.items():
            for k, er in enumerate(ie["ers"]):
                if er["pre"] is not None:
                    allowed_er[eid, k] = [er["pre"]]
                else:
                    allowed_er[eid, k] = set(by_type[er["rtype"]])

        for c in inst.constraints:
            if c.tag == "PreferResourcesConstraint" and X.txt(c, "Required") == "true":
                role = X.txt(c, "Role")
                pref = set()
                rgs = c.find("ResourceGroups")
                if rgs is not None:
                    for g in rgs:
                        pref |= set(inst.rgroups[g.attrib["Reference"]])
                rs = c.find("Resources")
                if rs is not None:
                    pref |= {r.attrib["Reference"] for r in rs}
                for eid in inst.events_of(c.find("AppliesTo")):
                    for k, er in enumerate(inst.events[eid]["ers"]):
                        if er["role"] == role and er["pre"] is None:
                            allowed_er[eid, k] &= pref

        self.allowed_er = {key: sorted(val) if isinstance(val, set) else val for key, val in allowed_er.items()}

        # Parse AvoidSplitAssignments, SpreadEvents, LimitBusyTimes, LimitWorkload, AvoidClashes
        self.split_rules = []   # (req, w, role, [sub_indices_with_role_k: list of (sub_i, k)])
        self.spread_rules = []  # (req, w, [(ts_set, lo, hi)], [[sub_i, ...]])
        self.busy_rules = []    # (req, w, mn, mx, [sorted_ts], [res_ids])
        self.wload_max6 = {}    # r -> max_workload * 6
        self.wload_min6 = {}    # r -> min_workload * 6
        self.clash_res = set()

        for c in inst.constraints:
            k = c.tag
            req = X.txt(c, "Required") == "true"
            w = int(X.txt(c, "Weight"))
            ap = c.find("AppliesTo")
            mn = X.txt(c, "Minimum"); mn = int(mn) if mn is not None else None
            mx = X.txt(c, "Maximum"); mx = int(mx) if mx is not None else None
            if k == "AvoidSplitAssignmentsConstraint":
                role = X.txt(c, "Role")
                for g in ap.find("EventGroups"):
                    items = []
                    pre_set = set()
                    for eid in inst.egroups[g.attrib["Reference"]]:
                        ri = next((idx for idx, er in enumerate(inst.events[eid]["ers"]) if er["role"] == role), None)
                        if ri is not None:
                            if inst.events[eid]["ers"][ri]["pre"] is not None:
                                pre_set.add(inst.events[eid]["ers"][ri]["pre"])
                            else:
                                for sub_i in self.eid_to_subs[eid]:
                                    items.append((sub_i, ri))
                    if items:
                        self.split_rules.append((req, w, role, g.attrib["Reference"], items, pre_set))
            elif k == "SpreadEventsConstraint":
                tgs = [(set(inst.tgroups[g.attrib["Reference"]]), int(X.txt(g, "Minimum")), int(X.txt(g, "Maximum"))) for g in c.find("TimeGroups")]
                grps = [[sub_i for eid in inst.egroups[g.attrib["Reference"]] for sub_i in self.eid_to_subs[eid]] for g in ap.find("EventGroups")]
                self.spread_rules.append((req, w, tgs, grps))
            elif k == "LimitBusyTimesConstraint":
                tgs = [sorted(inst.tgroups[g.attrib["Reference"]]) for g in c.find("TimeGroups")]
                self.busy_rules.append((req, w, mn, mx, tgs, inst.resources_of(ap)))
            elif k == "LimitWorkloadConstraint":
                assert req
                for r in inst.resources_of(ap):
                    if mx is not None:
                        self.wload_max6[r] = min(self.wload_max6.get(r, 10**12), self.lcm_dur * mx)
                    if mn is not None and mn > 0:
                        self.wload_min6[r] = max(self.wload_min6.get(r, 0), self.lcm_dur * mn)
            elif k == "AvoidClashesConstraint":
                self.clash_res.update(inst.resources_of(ap))

    def get_sub_se(self, se, sub_i):
        info = self.subs[sub_i]
        return se[info["eid"]][info["pos"]]


def solve_global_teachers(au: AUCompiled, cur_se, secs: float = 12.0, workers: int = 2, seed: int = 1):
    """Exact school-wide Teacher Re-Optimization across all 1,047 sub-events at fixed lesson times."""
    m = cp_model.CpModel()
    y = {}  # (sub_i, k, r) -> BoolVar for movable Teacher roles
    slot_lits_by_t = collections.defaultdict(lambda: collections.defaultdict(list))  # r -> q -> [lits]
    wload_terms_6 = collections.defaultdict(list)
    wload_const_6 = collections.defaultdict(int)

    for sub_i, info in enumerate(au.subs):
        s_rec = au.get_sub_se(cur_se, sub_i)
        tq = s_rec["t"]
        dur = info["dur"]
        eid = info["eid"]
        for k, er in enumerate(info["ers"]):
            wl6 = dur * er["workload"] * info["scale6"]
            if er["pre"] is not None or er["rtype"] != "Teacher":
                r_fixed = s_rec["res"][k]
                if r_fixed is not None and au.inst.rtype.get(r_fixed) == "Teacher":
                    wload_const_6[r_fixed] += wl6
                    for q in range(tq, tq + dur):
                        slot_lits_by_t[r_fixed][q].append(1)
                continue
            cur_r = s_rec["res"][k]
            cands = au.allowed_er[eid, k]
            lits = []
            for r in cands:
                # Filter out teachers unavailable during [tq .. tq + dur - 1]
                un = au.unavail.get(r, ())
                if any((tq + off) in un for off in range(dur)):
                    continue
                v = m.NewBoolVar("")
                y[sub_i, k, r] = v
                m.AddHint(v, 1 if r == cur_r else 0)
                lits.append(v)
                wload_terms_6[r].append(wl6 * v)
                for q in range(tq, tq + dur):
                    slot_lits_by_t[r][q].append(v)
            if not lits:
                return cur_se, "INFEASIBLE_DOMAIN"
            m.AddExactlyOne(lits)

    # 1. Teacher AvoidClashes
    for r in au.teachers:
        if r in au.clash_res:
            for q in range(au.T):
                items = slot_lits_by_t[r][q]
                if not items:
                    continue
                c_ones = sum(z for z in items if isinstance(z, int))
                v_lits = [z for z in items if not isinstance(z, int)]
                if c_ones >= 1:
                    for vl in v_lits:
                        m.Add(vl == 0)
                elif len(v_lits) > 1:
                    m.AddAtMostOne(v_lits)

    # 2. Teacher LimitWorkload (exact integer x6)
    for r in au.teachers:
        expr6 = wload_const_6[r] + sum(wload_terms_6[r])
        if r in au.wload_max6:
            m.Add(expr6 <= au.wload_max6[r])
        if r in au.wload_min6:
            m.Add(expr6 >= au.wload_min6[r])

    obj_terms = []

    # 3. AvoidSplitAssignments (Hard = 1 teacher, Soft = 10 * (distinct_teachers - 1))
    for req, w, role, gid, items, pre_set in au.split_rules:
        # Collect candidate teachers appearing across `items`
        cand_r = set(pre_set)
        by_r = collections.defaultdict(list)
        for sub_i, k in items:
            eid = au.subs[sub_i]["eid"]
            if au.inst.events[eid]["ers"][k]["rtype"] != "Teacher":
                continue
            for r in au.allowed_er[eid, k]:
                if (sub_i, k, r) in y:
                    cand_r.add(r)
                    by_r[r].append(y[sub_i, k, r])
        if not by_r:
            continue
        used_vars = []
        for r in sorted(cand_r):
            if r in pre_set:
                used_vars.append(1)
            elif by_r[r]:
                uv = m.NewBoolVar("")
                for lv in by_r[r]:
                    m.Add(uv >= lv)
                m.Add(uv <= sum(by_r[r]))
                used_vars.append(uv)
        if req:
            m.Add(sum(used_vars) <= 1)
        else:
            dev = m.NewIntVar(0, len(used_vars), "")
            m.Add(dev >= sum(used_vars) - 1)
            obj_terms.append(w * dev)

    # 4. Teacher LimitBusyTimes (soft W=2, min=0, max=7)
    for req, w, mn, mx, tgs, res_list in au.busy_rules:
        assert not req and (mn in (None, 0))
        for r in res_list:
            if au.inst.rtype.get(r) != "Teacher":
                continue
            for ts in tgs:
                b_q = []
                for q in ts:
                    items = slot_lits_by_t[r][q]
                    if not items:
                        continue
                    if any(isinstance(z, int) and z > 0 for z in items):
                        b_q.append(1)
                    else:
                        vl = [z for z in items if not isinstance(z, int)]
                        if len(vl) == 1:
                            b_q.append(vl[0])
                        elif len(vl) > 1:
                            # Since AvoidClashes enforces AtMostOne(vl), sum(vl) IS in {0, 1}!
                            bv = m.NewBoolVar("")
                            m.Add(bv == sum(vl))
                            b_q.append(bv)
                if len(b_q) > mx:
                    ov = m.NewIntVar(0, len(b_q), "")
                    m.Add(ov >= sum(b_q) - mx)
                    obj_terms.append(w * ov)

    m.Minimize(sum(obj_terms) if obj_terms else 0)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return cur_se, sv.StatusName(st)

    new_se = copy.deepcopy(cur_se)
    for (sub_i, k, r), v in y.items():
        if sv.Value(v):
            info = au.subs[sub_i]
            new_se[info["eid"]][info["pos"]]["res"][k] = r
    return new_se, f"{sv.StatusName(st)}({len(y)}v)"


def solve_au_joint_subproblem(
    au: AUCompiled, cur_se, free_bundles: set, free_teachers: set,
    secs: float = 12.0, workers: int = 2, seed: int = 1, min_time_diff: int = 0,
):
    """
    Exact Joint `(LinkBundle Time + Teacher + Room)` 0-Hard Subproblem CP-SAT!
      - Bundles in `free_bundles` can move start time `t` AND reassign movable Teacher/Room roles.
      - Fixed bundles (`b_id not in free_bundles`) keep their start time `t` and Room, while any movable
        Teacher role currently assigned to `free_teachers` can ALSO swap among `free_teachers`!
    """
    m = cp_model.CpModel()
    rng = random.Random(seed)

    # Current bundle start times
    b_cur_t = [au.get_sub_se(cur_se, b["members"][0])["t"] for b in au.bundles]
    free_sub_time = {sub_i for b_id in free_bundles for sub_i in au.bundles[b_id]["members"]}

    # 1. Bundle start-time variables `xt[b_id, t]` for `b_id in free_bundles`
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

    # 2. Resource assignment & `(sub_i, k, r, t)` joint occupancy!
    # Identify which `(sub_i, k)` roles have movable resources in this subproblem:
    #   - If `sub_i in free_sub_time`: ALL movable roles (Teacher & Room) are unlocked (among `free_teachers | {cur_r}` for Teachers, and all allowed Rooms for Rooms).
    #   - If `sub_i not in free_sub_time`: movable Teacher role is unlocked IFF `cur_r in free_teachers` (restricted to `free_teachers`!).
    yr = {}  # (sub_i, k, r) -> BoolVar
    fixed_occ = collections.defaultdict(lambda: [0] * au.T)  # r -> q -> count
    var_occ = collections.defaultdict(lambda: collections.defaultdict(list))  # r -> q -> [BoolVar]
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
            cur_r = s_rec["res"][k]
            wl6 = dur * er["workload"] * info["scale6"]

            # Decide candidate resources for (sub_i, k)
            if er["pre"] is not None:
                cands = [er["pre"]]
            elif time_is_free:
                if er["rtype"] == "Teacher":
                    cands = [r for r in au.allowed_er[eid, k] if (r in free_teachers or r == cur_r)]
                else:
                    cands = au.allowed_er[eid, k]
            else:
                if er["rtype"] == "Teacher" and cur_r in free_teachers:
                    cands = [r for r in au.allowed_er[eid, k] if (r in free_teachers or r == cur_r)]
                else:
                    cands = [cur_r]

            if (not time_is_free) and len(cands) == 1:
                r0 = cands[0]
                if r0 is not None:
                    wload_const6[r0] += wl6
                    for q in range(t_cur_s, t_cur_s + dur):
                        fixed_occ[r0][q] += 1
                continue

            if not time_is_free:
                # Fixed time `t_cur_s`, movable teacher among `cands`
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
                    return cur_se, "EMPTY_FIXED_T_RES"
                m.AddExactlyOne(rlits)
            else:
                # Free time `xt[b_id, t]` AND resource `cands`!
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

    # 3. Hard AvoidClashes across ALL clash resources `r` and slots `q`!
    for r in au.clash_res:
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

    # 4. Hard LimitWorkload (exact integer x6)
    for r in au.teachers:
        if not wload_terms6[r]:
            continue
        expr6 = wload_const6[r] + sum(wload_terms6[r])
        if r in au.wload_max6:
            m.Add(expr6 <= au.wload_max6[r])
        if r in au.wload_min6:
            m.Add(expr6 >= au.wload_min6[r])

    obj_terms = []

    # 5. Hard & Soft AvoidSplitAssignments
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
                cur_r = au.get_sub_se(cur_se, sub_i)["res"][k]
                if cur_r is not None:
                    fixed_r_set.add(cur_r)
        all_r = sorted(fixed_r_set | set(by_r.keys()))
        used_vars = []
        for r in all_r:
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
            dev = m.NewIntVar(0, len(used_vars), "")
            m.Add(dev >= sum(used_vars) - 1)
            obj_terms.append(w * dev)

    # 6. Soft SpreadEvents (W=1)
    for req, w, tgs, grps in au.spread_rules:
        for sub_grp in grps:
            if not any(au.sub_to_bundle[sub_i] in free_bundles for sub_i in sub_grp):
                continue
            for ts, lo, hi in tgs:
                cv = 0
                vl = []
                for sub_i in sub_grp:
                    b_id = au.sub_to_bundle[sub_i]
                    if b_id not in free_bundles:
                        if b_cur_t[b_id] in ts:
                            cv += 1
                    else:
                        vl.extend(xt[b_id, t] for t in ts if (b_id, t) in xt)
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

    # 7. Soft LimitBusyTimes (W=2, min=0, max=7)
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
                            bv = m.NewBoolVar("")
                            m.Add(bv == sum(vl))
                            b_q.append(bv)
                if len(b_q) > mx:
                    ov = m.NewIntVar(0, len(b_q), "")
                    m.Add(ov >= sum(b_q) - mx)
                    obj_terms.append(w * ov)

    m.Minimize(sum(obj_terms) if obj_terms else 0)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return cur_se, f"{sv.StatusName(st)}({len(xt)}t,{len(yr)}r)"

    new_se = copy.deepcopy(cur_se)
    for b_id in free_bundles:
        new_t = next(t for t in cand_t_map[b_id] if sv.Value(xt[b_id, t]))
        for sub_i in au.bundles[b_id]["members"]:
            info = au.subs[sub_i]
            new_se[info["eid"]][info["pos"]]["t"] = new_t
    for (sub_i, k, r), rv in yr.items():
        if sv.Value(rv):
            info = au.subs[sub_i]
            new_se[info["eid"]][info["pos"]]["res"][k] = r
    return new_se, f"{sv.StatusName(st)}({len(xt)}t,{len(yr)}r)"


def find_split_and_penalty_targets(au: AUCompiled, se):
    """Identify current split courses + teachers + bundles involved in soft violations."""
    split_depts = []
    for req, w, role, gid, items, pre_set in au.split_rules:
        if req:
            continue
        rs = set(pre_set)
        b_ids = set()
        for sub_i, k in items:
            r = au.get_sub_se(se, sub_i)["res"][k]
            if r is not None:
                rs.add(r)
            b_ids.add(au.sub_to_bundle[sub_i])
        if len(rs) > 1:
            # Also collect all allowed teachers for this split course!
            all_cands = set(rs)
            for sub_i, k in items:
                all_cands.update(au.allowed_er[au.subs[sub_i]["eid"], k])
            split_depts.append((gid, rs, all_cands, b_ids))

    # Bundles involved in SpreadEvents & LimitBusyTimes soft violations
    spread_busy_bundles = set()
    spread_busy_teachers = set()
    for req, w, tgs, grps in au.spread_rules:
        if req:
            continue
        for sub_grp in grps:
            for ts, lo, hi in tgs:
                c = sum(1 for sub_i in sub_grp if au.get_sub_se(se, sub_i)["t"] in ts)
                if c < lo or c > hi:
                    for sub_i in sub_grp:
                        spread_busy_bundles.add(au.sub_to_bundle[sub_i])

    busy = collections.defaultdict(lambda: [0] * au.T)
    res_bundles = collections.defaultdict(set)
    for sub_i, info in enumerate(au.subs):
        s_rec = au.get_sub_se(se, sub_i)
        for r in s_rec["res"]:
            if r is not None:
                res_bundles[r].add(au.sub_to_bundle[sub_i])
                for q in range(s_rec["t"], s_rec["t"] + info["dur"]):
                    busy[r][q] += 1
    for req, w, mn, mx, tgs, res_list in au.busy_rules:
        if req:
            continue
        for r in res_list:
            for ts in tgs:
                if sum(1 for q in ts if busy[r][q] > 0) > mx:
                    spread_busy_teachers.add(r)
                    spread_busy_bundles |= res_bundles[r]

    return split_depts, spread_busy_bundles, spread_busy_teachers, res_bundles


def run_au(total_secs: float = 1200.0, workers: int = 2, seed: int = 202, mem_gb: float = 4.5):
    lim = int(mem_gb * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    tid = "AU-BG-98"
    t0 = time.time()
    deadline = t0 + total_secs
    _, inst_el, inst, start_se, start_val = xio.load_target(tid)
    au = AUCompiled(inst, start_se)

    cur_se = copy.deepcopy(start_se)
    cur_val = X.evaluate_se(inst, cur_se)[:2]
    assert cur_val == start_val
    print(f"[{tid}] AU-v1 Start verified: {cur_val[0]}.{cur_val[1]} ({au.B} LinkBundles, {au.S} subs; win <= 0.125)", flush=True)

    best_val = cur_val
    best_se = copy.deepcopy(cur_se)
    rng = random.Random(seed)

    # Phase 0: School-wide Teacher Re-Optimization at fixed start times
    cand_se, st0 = solve_global_teachers(au, cur_se, secs=min(20.0, total_secs * 0.15), workers=workers, seed=seed)
    v0 = X.evaluate_se(inst, cand_se)[:2]
    print(f"[{tid}] Phase-0 Global-Teachers ({st0}) -> {v0[0]}.{v0[1]} | {time.time()-t0:.1f}s", flush=True)
    if v0 <= cur_val:
        cur_val, cur_se = v0, cand_se
        if cur_val < best_val:
            best_val, best_se = cur_val, copy.deepcopy(cur_se)
            if xio.is_strict_win(tid, best_val):
                wpath = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
                v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"AU-v1 Phase0 seed={seed}")
                assert v_chk == best_val
                print(f"  *** [{tid}] PHASE-0 STRICT WIN: {best_val[0]}.{best_val[1]} -> {wpath} ***", flush=True)

    step = 0
    improvements = 0
    plateau_moves = 0

    while time.time() + 8.0 < deadline:
        step += 1
        rem = deadline - time.time()
        split_depts, sb_bundles, sb_teachers, res_bundles = find_split_and_penalty_targets(au, cur_se)
        mode = step % 3

        if mode == 1 and split_depts:
            # AU-N1: Pick 1-2 split courses + their candidate teachers + ~35 bundles of those teachers!
            k_sp = min(len(split_depts), 2 if step % 2 == 1 else 1)
            chosen_sp = rng.sample(split_depts, k_sp)
            f_teachers = set()
            f_bundles = set()
            for _, used_rs, all_cands, b_ids in chosen_sp:
                f_bundles |= b_ids
                f_teachers |= used_rs
                extra_t = list(all_cands - f_teachers)
                rng.shuffle(extra_t)
                f_teachers.update(extra_t[:6])
            t_pool_b = list({b_id for r in f_teachers for b_id in res_bundles[r]} - f_bundles)
            rng.shuffle(t_pool_b)
            f_bundles.update(t_pool_b[:max(0, 38 - len(f_bundles))])
            ntag = f"AU-N1_Split({len(f_bundles)}b,{len(f_teachers)}T)"
            cand_se, st_s = solve_au_joint_subproblem(
                au, cur_se, f_bundles, f_teachers,
                secs=min(15.0, max(3.0, rem - 2.0)), workers=workers, seed=seed + step * 41,
            )
        elif mode == 2 and sb_bundles:
            # AU-N2: Spread + Busy direct sniper (shaving 3 pts of the 18 Spread+Busy pts hits 0.125!)
            f_bundles = set(sb_bundles)
            f_teachers = set(sb_teachers)
            if len(f_bundles) > 40:
                f_bundles = set(rng.sample(sorted(f_bundles), 40))
            else:
                extra_b = [b_id for b_id in range(au.B) if b_id not in f_bundles and au.bundles[b_id]["pre_t"] is None]
                rng.shuffle(extra_b)
                f_bundles.update(extra_b[:(38 - len(f_bundles))])
            # Add teachers teaching `f_bundles` (up to 10)
            t_in_b = [r for b_id in f_bundles for sub_i in au.bundles[b_id]["members"] for r in au.get_sub_se(cur_se, sub_i)["res"] if r in au.teachers]
            rng.shuffle(t_in_b)
            f_teachers.update(t_in_b[:max(0, 10 - len(f_teachers))])
            ntag = f"AU-N2_SpreadBusy({len(f_bundles)}b,{len(f_teachers)}T)"
            cand_se, st_s = solve_au_joint_subproblem(
                au, cur_se, f_bundles, f_teachers,
                secs=min(14.0, max(3.0, rem - 2.0)), workers=workers, seed=seed + step * 41,
            )
        else:
            # AU-N3: Plateau re-timing of ~40 bundles (`min_time_diff=4` every 6th step!) + Global School-Wide Teacher Re-Polish!
            mov_b = [b_id for b_id in range(au.B) if au.bundles[b_id]["pre_t"] is None]
            f_bundles = set(rng.sample(mov_b, min(42, len(mov_b))))
            f_teachers = set(rng.sample(au.teachers, 8))
            mdiff = 4 if (step % 6 == 0) else 0
            cand_se, st_s = solve_au_joint_subproblem(
                au, cur_se, f_bundles, f_teachers,
                secs=min(11.0, max(3.0, rem - 5.0)), workers=workers, seed=seed + step * 41, min_time_diff=mdiff,
            )
            cv_mid = X.evaluate_se(inst, cand_se)[:2]
            if cv_mid[0] == 0 and cv_mid[1] <= best_val[1] + 4 and time.time() + 5.0 < deadline:
                cand_se2, st_g = solve_global_teachers(au, cand_se, secs=min(7.0, max(2.0, deadline - time.time() - 1.0)), workers=workers, seed=seed + step * 99)
                if X.evaluate_se(inst, cand_se2)[:2] <= cv_mid:
                    cand_se = cand_se2
                    st_s += f"+GT({st_g[:3]})"
            ntag = f"AU-N3_DriftGT(d>={mdiff})"

        cand_val = X.evaluate_se(inst, cand_se)[:2]
        # Accept improvements, plateau moves, or tiny <= best+2 ridge steps on N3 kicks!
        allow_ridge = (mode == 0 and step % 6 == 0 and cand_val[0] == 0 and cand_val[1] <= best_val[1] + 2)
        if cand_val <= cur_val or allow_ridge:
            t_changed = sum(
                1 for sub_i in range(au.S)
                if au.get_sub_se(cand_se, sub_i)["t"] != au.get_sub_se(cur_se, sub_i)["t"]
                or au.get_sub_se(cand_se, sub_i)["res"] != au.get_sub_se(cur_se, sub_i)["res"]
            )
            if cand_val < cur_val and cand_val < best_val:
                improvements += 1
                print(f"  [{tid} S{step:3d} {ntag} {st_s}] IMPROVED {cur_val[0]}.{cur_val[1]} -> {cand_val[0]}.{cand_val[1]} (chg={t_changed}) | {time.time()-t0:.0f}s", flush=True)
            elif t_changed > 0:
                plateau_moves += 1
            cur_val = cand_val
            cur_se = cand_se

            if cur_val < best_val:
                best_val = cur_val
                best_se = copy.deepcopy(cur_se)
                if xio.is_strict_win(tid, best_val):
                    wpath = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
                    v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"AU-v1 {ntag} seed={seed}")
                    assert v_chk == best_val
                    print(f"  *** [{tid}] STRICT WORLD RECORD WIN SAVED & VERIFIED: {best_val[0]}.{best_val[1]} -> {wpath} (sha={sha[:12]}) ***", flush=True)
        elif step % 5 == 0 and cur_val > best_val:
            cur_val, cur_se = best_val, copy.deepcopy(best_se)

        if step % 5 == 0:
            print(f"  [{tid} S{step:3d}] {ntag} {st_s} | cur={cur_val[0]}.{cur_val[1]} best={best_val[0]}.{best_val[1]} (imp={improvements}, plat={plateau_moves}) | {time.time()-t0:.0f}s", flush=True)

    win = xio.is_strict_win(tid, best_val)
    win_path, sha = None, None
    if win:
        win_path = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
        v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, win_path, desc=f"AU-v1 seed={seed}")
        assert v_chk == best_val
    else:
        tmp_p = os.path.join(xio.LOGS_DIR, f"_chk_{tid}_{os.getpid()}.xml")
        v_chk, _, _ = xio.write_and_verify_xml(inst_el, inst, best_se, tmp_p, desc="check")
        os.remove(tmp_p)
        assert v_chk == best_val

    diff_subs = sum(
        1 for sub_i in range(au.S)
        if au.get_sub_se(best_se, sub_i)["t"] != au.get_sub_se(start_se, sub_i)["t"]
        or au.get_sub_se(best_se, sub_i)["res"] != au.get_sub_se(start_se, sub_i)["res"]
    )
    return dict(
        engine="AU-v1_joint_bundle_cpsat", inst=tid,
        record=list(start_val), best=list(best_val), win=win,
        steps=step, improvements=improvements, plateau_moves=plateau_moves,
        diff_subs=diff_subs, win_path=win_path, sha256=sha, secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--secs", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=202)
    parser.add_argument("--out-json", type=str, default="")
    args = parser.parse_args()

    res = run_au(total_secs=args.secs, workers=args.workers, seed=args.seed)
    if args.out_json:
        open(args.out_json, "w").write(json.dumps(res))
    else:
        print(json.dumps(res, indent=2), flush=True)


if __name__ == "__main__":
    main()
