"""
XHSTT AU-BG-98 Engine AU-v2 — Scaled-Up 65-85 LinkBundle Joint CP-SAT + Tabu Ridge-Kick & Complete-Hint Global Teachers
(scans/2026-11-27-xhstt-charlie/solve_au_v2.py)

Upgrades over AU-v1 (from `smoke_v1` diagnostics):
  1. Complete-Hint Global Teacher Re-Optimizer (`solve_global_teachers_v2`): Hints ALL derived `uv`,
     `dev`, `bv`, and `ov` variables from `cur_se` + enforces upper bound `<= cur_teacher_soft` so CP-SAT
     starts at `0.128` at `t = 0.02s` instead of `0.176`!
  2. Larger Joint Subproblems (`60-80` `LinkBundles` + `14-20` Teachers): Since `38` bundles solved to
     `OPTIMAL` in ~6s in `smoke_v1`, scaling up to `60-80` bundles (~20% of the school!) unlocks coupled
     cross-class swap chains needed to unify the 11 split courses (`-10` pts each) or shave `3` `Spread+Busy` pts!
  3. Tabu-Fenced Ridge-Kick (`min_time_diff=10`, accepts `<= 0.136`) + Polish Cascade (`origin_diff >= 8`)
     + School-Wide Global Teacher Sniper!
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


def solve_global_teachers_v2(au: v1.AUCompiled, cur_se, max_obj_cap: int = 128, secs: float = 10.0, workers: int = 2, seed: int = 1):
    """Complete-hinted school-wide Teacher Re-Optimizer capped at `max_obj_cap`."""
    m = cp_model.CpModel()
    y = {}
    slot_lits_by_t = collections.defaultdict(lambda: collections.defaultdict(list))
    slot_cur_busy = collections.defaultdict(lambda: [0] * au.T)
    wload_terms_6 = collections.defaultdict(list)
    wload_const_6 = collections.defaultdict(int)

    for sub_i, info in enumerate(au.subs):
        s_rec = au.get_sub_se(cur_se, sub_i)
        tq = s_rec["t"]
        dur = info["dur"]
        eid = info["eid"]
        for k, er in enumerate(info["ers"]):
            wl6 = dur * er["workload"] * info["scale6"]
            cur_r = s_rec["res"][k]
            if cur_r is not None and au.inst.rtype.get(cur_r) == "Teacher":
                for q in range(tq, tq + dur):
                    slot_cur_busy[cur_r][q] = 1
            if er["pre"] is not None or er["rtype"] != "Teacher":
                if cur_r is not None and au.inst.rtype.get(cur_r) == "Teacher":
                    wload_const_6[cur_r] += wl6
                    for q in range(tq, tq + dur):
                        slot_lits_by_t[cur_r][q].append(1)
                continue
            cands = au.allowed_er[eid, k]
            lits = []
            for r in cands:
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

    for r in au.teachers:
        expr6 = wload_const_6[r] + sum(wload_terms_6[r])
        if r in au.wload_max6:
            m.Add(expr6 <= au.wload_max6[r])
        if r in au.wload_min6:
            m.Add(expr6 >= au.wload_min6[r])

    obj_terms = []
    for req, w, role, gid, items, pre_set in au.split_rules:
        cand_r = set(pre_set)
        cur_used_r = set(pre_set)
        by_r = collections.defaultdict(list)
        for sub_i, k in items:
            eid = au.subs[sub_i]["eid"]
            if au.inst.events[eid]["ers"][k]["rtype"] != "Teacher":
                continue
            cr = au.get_sub_se(cur_se, sub_i)["res"][k]
            if cr is not None:
                cur_used_r.add(cr)
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
                m.AddHint(uv, 1 if r in cur_used_r else 0)
                for lv in by_r[r]:
                    m.Add(uv >= lv)
                m.Add(uv <= sum(by_r[r]))
                used_vars.append(uv)
        if req:
            m.Add(sum(used_vars) <= 1)
        else:
            dev = m.NewIntVar(0, len(used_vars), "")
            m.AddHint(dev, max(0, len(cur_used_r) - 1))
            m.Add(dev >= sum(used_vars) - 1)
            obj_terms.append(w * dev)

    for req, w, mn, mx, tgs, res_list in au.busy_rules:
        for r in res_list:
            if au.inst.rtype.get(r) != "Teacher":
                continue
            for ts in tgs:
                b_q = []
                cur_cnt = 0
                for q in ts:
                    items = slot_lits_by_t[r][q]
                    if not items:
                        continue
                    cb = slot_cur_busy[r][q]
                    cur_cnt += cb
                    if any(isinstance(z, int) and z > 0 for z in items):
                        b_q.append(1)
                    else:
                        vl = [z for z in items if not isinstance(z, int)]
                        if len(vl) == 1:
                            b_q.append(vl[0])
                        elif len(vl) > 1:
                            bv = m.NewBoolVar("")
                            m.AddHint(bv, cb)
                            m.Add(bv == sum(vl))
                            b_q.append(bv)
                if len(b_q) > mx:
                    ov = m.NewIntVar(0, len(b_q), "")
                    m.AddHint(ov, max(0, cur_cnt - mx))
                    m.Add(ov >= sum(b_q) - mx)
                    obj_terms.append(w * ov)

    tot_obj = sum(obj_terms) if obj_terms else 0
    m.Add(tot_obj <= int(max_obj_cap))
    m.Minimize(tot_obj)

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


def run_au_v2(total_secs: float = 1800.0, workers: int = 2, seed: int = 404, mem_gb: float = 4.5):
    lim = int(mem_gb * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    tid = "AU-BG-98"
    t0 = time.time()
    deadline = t0 + total_secs
    _, inst_el, inst, start_se, start_val = xio.load_target(tid)
    au = v1.AUCompiled(inst, start_se)

    cur_se = copy.deepcopy(start_se)
    cur_val = X.evaluate_se(inst, cur_se)[:2]
    assert cur_val == start_val
    print(f"[{tid}] AU-v2 Start verified: {cur_val[0]}.{cur_val[1]} ({au.B} LinkBundles; win <= 0.125)", flush=True)

    best_val = cur_val
    best_se = copy.deepcopy(cur_se)
    rng = random.Random(seed)

    # Phase 0: Complete-Hinted Global Teacher Re-Optimizer
    _, _, per0 = X.evaluate_se(inst, cur_se)
    t_soft_cap = per0.get(("AvoidSplitAssignmentsConstraint", False), 0) + per0.get(("LimitBusyTimesConstraint", False), 0)
    cand_se, st0 = solve_global_teachers_v2(au, cur_se, max_obj_cap=t_soft_cap, secs=min(20.0, total_secs * 0.12), workers=workers, seed=seed)
    v0 = X.evaluate_se(inst, cand_se)[:2]
    print(f"[{tid}] Phase-0 Global-Teachers ({st0}) -> {v0[0]}.{v0[1]} | {time.time()-t0:.1f}s", flush=True)
    if v0 <= cur_val:
        cur_val, cur_se = v0, cand_se
        if cur_val < best_val:
            best_val, best_se = cur_val, copy.deepcopy(cur_se)
            if xio.is_strict_win(tid, best_val):
                wpath = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
                v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"AU-v2 Phase0 seed={seed}")
                assert v_chk == best_val
                print(f"  *** [{tid}] PHASE-0 STRICT WIN: {best_val[0]}.{best_val[1]} -> {wpath} ***", flush=True)

    step = 0
    improvements = 0
    plateau_moves = 0

    while time.time() + 10.0 < deadline:
        step += 1
        rem = deadline - time.time()
        if step % 8 == 1 and cur_val[1] > best_val[1] + 6:
            cur_val, cur_se = best_val, copy.deepcopy(best_se)

        split_depts, sb_bundles, sb_teachers, res_bundles = v1.find_split_and_penalty_targets(au, cur_se)
        is_kick = (step % 8 == 4)
        mode = step % 3

        if is_kick:
            mov_b = [b_id for b_id in range(au.B) if au.bundles[b_id]["pre_t"] is None]
            f_bundles = set(rng.sample(mov_b, 55))
            f_teachers = set(rng.sample(au.teachers, 12))
            ntag = "AU_KICK(55b,12T,d>=10)"
            cand_se, st_s = v1.solve_au_joint_subproblem(
                au, cur_se, f_bundles, f_teachers,
                secs=min(14.0, max(3.0, rem - 2.0)), workers=workers, seed=seed + step * 53, min_time_diff=10,
            )
        elif mode == 1 and split_depts:
            # Scaled-up Split-Department Cluster (`65` bundles + `16` teachers!)
            k_sp = min(len(split_depts), 2)
            chosen_sp = rng.sample(split_depts, k_sp)
            f_teachers, f_bundles = set(), set()
            for _, used_rs, all_cands, b_ids in chosen_sp:
                f_bundles |= b_ids
                f_teachers |= used_rs
                extra_t = list(all_cands - f_teachers)
                rng.shuffle(extra_t)
                f_teachers.update(extra_t[:10])
            t_pool_b = list({b_id for r in f_teachers for b_id in res_bundles[r]} - f_bundles)
            rng.shuffle(t_pool_b)
            f_bundles.update(t_pool_b[:max(0, 64 - len(f_bundles))])
            if len(f_bundles) < 64:
                mov_b = [b_id for b_id in range(au.B) if b_id not in f_bundles and au.bundles[b_id]["pre_t"] is None]
                rng.shuffle(mov_b)
                f_bundles.update(mov_b[:(64 - len(f_bundles))])
            ntag = f"SplitBig({len(f_bundles)}b,{len(f_teachers)}T)"
            cand_se, st_s = v1.solve_au_joint_subproblem(
                au, cur_se, f_bundles, f_teachers,
                secs=min(18.0, max(3.0, rem - 2.0)), workers=workers, seed=seed + step * 41, min_time_diff=0,
            )
        elif mode == 2 and sb_bundles:
            # Scaled-up Spread+Busy Sniper (`68` bundles + `14` teachers!)
            f_bundles = set(sb_bundles)
            f_teachers = set(sb_teachers)
            extra_b = [b_id for b_id in range(au.B) if b_id not in f_bundles and au.bundles[b_id]["pre_t"] is None]
            rng.shuffle(extra_b)
            f_bundles.update(extra_b[:max(0, 68 - len(f_bundles))])
            if len(f_bundles) > 68:
                f_bundles = set(rng.sample(sorted(f_bundles), 68))
            t_in_b = [r for b_id in f_bundles for sub_i in au.bundles[b_id]["members"] for r in au.get_sub_se(cur_se, sub_i)["res"] if r in au.teachers]
            rng.shuffle(t_in_b)
            f_teachers.update(t_in_b[:max(0, 14 - len(f_teachers))])
            ntag = f"SpreadBusyBig({len(f_bundles)}b,{len(f_teachers)}T)"
            cand_se, st_s = v1.solve_au_joint_subproblem(
                au, cur_se, f_bundles, f_teachers,
                secs=min(18.0, max(3.0, rem - 2.0)), workers=workers, seed=seed + step * 41, min_time_diff=0,
            )
        else:
            # 2-Day Window Re-Time (`~70` bundles) + Complete-Hinted Global Teacher Re-Polish!
            d_pair = rng.sample(range(5), 2)
            sl = {d * 8 + p for d in d_pair for p in range(8)}
            in_days = [b_id for b_id in range(au.B) if au.bundles[b_id]["pre_t"] is None and au.get_sub_se(cur_se, au.bundles[b_id]["members"][0])["t"] in sl]
            rng.shuffle(in_days)
            f_bundles = set(in_days[:68])
            f_teachers = set(rng.sample(au.teachers, 14))
            cand_se, st_s = v1.solve_au_joint_subproblem(
                au, cur_se, f_bundles, f_teachers,
                secs=min(15.0, max(3.0, rem - 6.0)), workers=workers, seed=seed + step * 41, min_time_diff=0,
            )
            cv_mid, _, per_mid = X.evaluate_se(inst, cand_se)
            if cv_mid == 0 and time.time() + 6.0 < deadline:
                t_cap = per_mid.get(("AvoidSplitAssignmentsConstraint", False), 0) + per_mid.get(("LimitBusyTimesConstraint", False), 0)
                cand_se2, st_g = solve_global_teachers_v2(au, cand_se, max_obj_cap=t_cap, secs=min(7.0, max(2.0, deadline - time.time() - 1.0)), workers=workers, seed=seed + step * 99)
                if X.evaluate_se(inst, cand_se2)[:2] <= (cv_mid, sum(v for (_, rq), v in per_mid.items() if not rq)):
                    cand_se = cand_se2
                    st_s += f"+GT({st_g[:3]})"
            ntag = f"TwoDayGT({len(f_bundles)}b)"

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
                print(f"  *** [{tid} S{step:3d} {ntag} {st_s}] NEW BEST {best_val[0]}.{best_val[1]} -> {cand_val[0]}.{cand_val[1]} (chg={t_changed}) | {time.time()-t0:.0f}s ***", flush=True)
            elif cand_val == cur_val and t_changed > 0:
                plateau_moves += 1
            cur_val = cand_val
            cur_se = cand_se

            if cur_val < best_val:
                best_val = cur_val
                best_se = copy.deepcopy(cur_se)
                if xio.is_strict_win(tid, best_val):
                    wpath = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
                    v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, wpath, desc=f"AU-v2 {ntag} seed={seed}")
                    assert v_chk == best_val
                    print(f"  *** [{tid}] STRICT WORLD RECORD WIN SAVED & VERIFIED: {best_val[0]}.{best_val[1]} -> {wpath} (sha={sha[:12]}) ***", flush=True)

        if step % 4 == 0:
            d_orig = sum(
                1 for sub_i in range(au.S)
                if au.get_sub_se(cur_se, sub_i)["t"] != au.get_sub_se(best_se, sub_i)["t"]
                or au.get_sub_se(cur_se, sub_i)["res"] != au.get_sub_se(best_se, sub_i)["res"]
            )
            print(f"  [{tid} S{step:3d}] {ntag:24s} {st_s:20s} | cur={cur_val[0]}.{cur_val[1]}(d={d_orig}) best={best_val[0]}.{best_val[1]} (imp={improvements}, plat={plateau_moves}) | {time.time()-t0:.0f}s", flush=True)

    win = xio.is_strict_win(tid, best_val)
    win_path, sha = None, None
    if win:
        win_path = os.path.join(xio.WINS_DIR, f"WIN_{tid}_{best_val[0]}_{best_val[1]}.xml")
        v_chk, _, sha = xio.write_and_verify_xml(inst_el, inst, best_se, win_path, desc=f"AU-v2 seed={seed}")
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
        engine="AU-v2_scaled_joint_tabu", inst=tid,
        record=list(start_val), best=list(best_val), win=win,
        steps=step, improvements=improvements, plateau_moves=plateau_moves,
        diff_subs=diff_subs, win_path=win_path, sha256=sha, secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--secs", type=float, default=1800.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=404)
    parser.add_argument("--out-json", type=str, default="")
    args = parser.parse_args()

    res = run_au_v2(total_secs=args.secs, workers=args.workers, seed=args.seed)
    if args.out_json:
        open(args.out_json, "w").write(json.dumps(res))
    else:
        print(json.dumps(res, indent=2), flush=True)


if __name__ == "__main__":
    main()
