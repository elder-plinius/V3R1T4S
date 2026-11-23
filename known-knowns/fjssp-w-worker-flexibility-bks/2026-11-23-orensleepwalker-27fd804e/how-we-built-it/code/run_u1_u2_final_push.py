"""
Final Push on U1 (Hurinkrdata16, bar=981) & U2 (BrandimarteMk2, bar=26) — Victory or Proven Optimum:
  1. U1 Phase A (30m max, 6 cores): 60s v4 seed -> 7-op ALNS-CPSAT (25s steps, 55-75 op ruin)
     <-> numba_ts_v4 Tabu Polish Ping-Pong (re-polishing every new <= best_mk basin + every 5 iters).
     Stops immediately on mk <= 980.
  2. U2 Phase B (20m max, 6 cores): Hard-capped H = 25 Carlier Head-Body-Tail + [heads, 25-tails]
     domain-tightened 6-worker CP-SAT (max_lp + core + strong disjunctive propagation).
     Stops immediately on WIN (<= 25) or PROVED_OPTIMAL_AT_BAR (INFEASIBLE <= 25).
  3. U1 Phase C (15m max, 6 cores, if Phase A didn't win): Hard-capped H = 980 Carlier 6-worker CP-SAT.

Saves any verified win (< true_bar) to wins_extra2/. Logs to logs/u1_u2_final_push.jsonl.
DOES NOT modify best_wins/, best_wins_manifest.json, wins_extra/, or wins_extra_manifest.json.
"""
import json
import os
import random
import resource
import sys
import time

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
INST_DIR = os.path.join(BASE, "runs/2026-11-11-2301/data/repo/instances/Example_Instances_FJSSP-WF")
HYBRID_DIR = os.path.join(BASE, "scans/2026-11-15-goal-overnight")
WINS_EXTRA2_DIR = os.path.join(OUT_DIR, "wins_extra2")
LOGS_DIR = os.path.join(OUT_DIR, "logs")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)
sys.path.insert(0, HYBRID_DIR)

import numpy as np  # noqa: E402
from ortools.sat.python import cp_model  # noqa: E402
import fjsspw  # noqa: E402
import numba_ts  # noqa: E402
import numba_ts_v4  # noqa: E402
import hybrid_engine as he  # noqa: E402
from play2_cpsat_snipe import FirstWinStopCallback, _extract_sched  # noqa: E402


def save_win(inst_name, fjs_path, true_bar, mk, ops):
    sched = {"instance": inst_name, "ops": ops}
    ok, cmk, errs = fjsspw.check(fjs_path, sched)
    assert ok and cmk == mk < true_bar, f"Win check FAIL {inst_name}: ok={ok} cmk={cmk} mk={mk} errs={errs[:3]}"
    os.makedirs(WINS_EXTRA2_DIR, exist_ok=True)
    win_path = os.path.join(WINS_EXTRA2_DIR, f"{inst_name}_mk{mk}_bar{true_bar}.json")
    with open(win_path, "w") as wf:
        json.dump(sched, wf)
    return win_path


def ops_to_numba_state(nb, ops):
    """Convert canonical [[j, o, mm(1-based), ww(1-based), s, d], ...] into Numba v4 state arrays."""
    N = int(nb["N"])
    M = int(nb["M"])
    W = int(nb["W"])
    op_job = nb["op_job"]
    op_idx = nb["op_idx"]
    alt_start = nb["alt_start"]
    alt_m = nb["alt_m"]
    alt_w = nb["alt_w"]
    alt_d = nb["alt_d"]

    jo_to_u = {(int(op_job[u]), int(op_idx[u])): u for u in range(N)}
    op_alt = np.empty(N, dtype=np.int32)
    op_m = np.empty(N, dtype=np.int32)
    op_w = np.empty(N, dtype=np.int32)
    dur = np.empty(N, dtype=np.int32)

    m_lists = [[] for _ in range(M)]
    w_lists = [[] for _ in range(W)]
    for j, o, mm, ww, s, d in ops:
        u = jo_to_u[(int(j), int(o))]
        m0 = int(mm) - 1
        w0 = int(ww) - 1
        a0, a1 = int(alt_start[u]), int(alt_start[u + 1])
        found_a = -1
        for a in range(a0, a1):
            if int(alt_m[a]) == m0 and int(alt_w[a]) == w0:
                found_a = a
                break
        assert found_a != -1, f"Mode not found for ({j},{o}) ({mm},{ww})"
        op_alt[u] = found_a
        op_m[u] = m0
        op_w[u] = w0
        dur[u] = int(alt_d[found_a])
        m_lists[m0].append((int(s), int(j), int(o), u))
        w_lists[w0].append((int(s), int(j), int(o), u))

    mh = np.full(M, -1, dtype=np.int32)
    mt = np.full(M, -1, dtype=np.int32)
    mp = np.full(N, -1, dtype=np.int32)
    ms = np.full(N, -1, dtype=np.int32)
    for m0 in range(M):
        m_lists[m0].sort()
        seq = [x[3] for x in m_lists[m0]]
        if seq:
            mh[m0] = seq[0]
            mt[m0] = seq[-1]
            for i in range(len(seq)):
                if i > 0:
                    mp[seq[i]] = seq[i - 1]
                if i + 1 < len(seq):
                    ms[seq[i]] = seq[i + 1]

    wh = np.full(W, -1, dtype=np.int32)
    wt = np.full(W, -1, dtype=np.int32)
    wp = np.full(N, -1, dtype=np.int32)
    ws = np.full(N, -1, dtype=np.int32)
    for w0 in range(W):
        w_lists[w0].sort()
        seq = [x[3] for x in w_lists[w0]]
        if seq:
            wh[w0] = seq[0]
            wt[w0] = seq[-1]
            for i in range(len(seq)):
                if i > 0:
                    wp[seq[i]] = seq[i - 1]
                if i + 1 < len(seq):
                    ws[seq[i]] = seq[i + 1]

    return op_alt, op_m, op_w, dur, mh, mt, wh, wt, mp, ms, wp, ws


def v4_polish_from_ops(inst_name, fjs_path, nb, ops, seed, max_iters=9000, max_no_improve=1300):
    """Run a targeted numba_ts_v4 tabu intensification directly from an ALNS schedule."""
    st = ops_to_numba_state(nb, ops)
    res = numba_ts_v4.tabu_search_v4_run(
        nb["N"], nb["M"], nb["W"], nb["job_pred"], nb["job_succ"],
        nb["alt_start"], nb["alt_m"], nb["alt_w"], nb["alt_d"],
        int(seed), int(max_iters), int(max_no_improve), 90,
        st[0], st[1], st[2], st[3], st[4], st[5], st[6], st[7], st[8], st[9], st[10], st[11],
    )
    mk = int(res[0])
    sched = numba_ts.to_schedule_json(inst_name, nb, res[1], res[2])
    ok, cmk, _ = fjsspw.check(fjs_path, sched)
    if ok and cmk == mk:
        return mk, sched["ops"]
    return None, None


def run_u1_pingpong(budget_s=1800.0, seed=920001):
    """Phase 1: 60s v4 seed -> 30m 6-core ALNS-CPSAT <-> v4 Tabu Ping-Pong on U1 Hurinkrdata16 (bar=981)."""
    t0 = time.time()
    inst_name = "Hurinkrdata16"
    fjs_path = os.path.join(INST_DIR, "Hurinkrdata16.fjs")
    target_bar = 981
    J, M, W, jobs = fjsspw.parse(fjs_path)
    nb = numba_ts.build_numba_instance(J, M, W, jobs)

    print("=== U1 PHASE A: 60s v4 seed -> 30m 6-Core ALNS-CPSAT <-> v4 Ping-Pong (bar=981) ===", flush=True)
    seed_mk, seed_state, _ = numba_ts_v4.cmrts_v4_search(inst_name, nb, time_budget_s=60.0, seed0=seed)
    seed_sched = numba_ts.to_schedule_json(inst_name, nb, seed_state[0], seed_state[12])
    ok, cmk, errs = fjsspw.check(fjs_path, seed_sched)
    assert ok and cmk == seed_mk, f"Seed check FAIL: {errs[:3]}"
    best_mk = int(seed_mk)
    best_ops = seed_sched["ops"]
    print(f"  [U1] v4 60s seed: mk={best_mk}", flush=True)

    if best_mk < target_bar:
        wp = save_win(inst_name, fjs_path, target_bar, best_mk, best_ops)
        return dict(phase="U1_PingPong", name=inst_name, true_bar=target_bar, mk=best_mk,
                    outcome="WIN", beats_bar=True, win_path=wp, secs=round(time.time() - t0, 1))

    elite_pool = [(best_mk, best_ops)]
    seen_sigs = {tuple((r[0], r[1], r[2], r[3]) for r in sorted(best_ops))}
    op_names = [
        "CritWindowCompress",
        "BottleneckResourceRuin",
        "CritAndJobRuin",
        "CritEdgeFlip",
        "CritWorkerShift",
        "FreeMWFixedOrder",
        "PathRelinkingCrossover",
    ]
    rng = random.Random(seed)
    flipped_tabu = set()
    lns_iter = 0
    events = [f"v4 seed -> {best_mk}"]
    t_loop = time.time()

    while (time.time() - t_loop) < budget_s and best_mk >= target_bar:
        rem = budget_s - (time.time() - t_loop)
        if rem < 5.0:
            break
        lns_iter += 1
        op_name = op_names[(lns_iter - 1) % len(op_names)]

        if len(elite_pool) > 1 and rng.random() < 0.30:
            base_mk, base_ops = rng.choice(elite_pool[:min(6, len(elite_pool))])
        else:
            base_mk, base_ops = best_mk, best_ops

        slack, es, lf, m_seq, w_seq, crit_ops, crit_edges = he.get_dag_analysis(J, M, W, jobs, base_ops, base_mk)
        all_ops = [(j, o) for j in range(J) for o in range(len(jobs[j]))]
        n_total = len(all_ops)
        step_secs = min(25.0, max(6.0, rem))

        forced_edges = None
        forbidden_mw = None
        window_bounds = None
        compress_obj = (lns_iter % 2 == 1)
        allow_slack = 0

        if op_name == "CritWindowCompress":
            w_idx = (lns_iter // len(op_names)) % 4
            fracs = [(0.35, 1.0), (0.15, 0.80), (0.0, 0.65), (0.25, 0.90)][w_idx]
            Ta, Tb = int(base_mk * fracs[0]), int(base_mk * fracs[1])
            window_bounds = (Ta, Tb)
            op_map = {(j, o): (mm, ww, s, d) for j, o, mm, ww, s, d in base_ops}
            ruin_set = set(crit_ops) | {k for k, (_, _, s, d) in op_map.items() if s + d > Ta and s < Tb}
            if len(ruin_set) > 75:
                ruin_set = set(crit_ops) | set(sorted(ruin_set - set(crit_ops), key=lambda k: slack[k])[:max(10, 75 - len(crit_ops))])
        elif op_name == "CritAndJobRuin":
            op_map = {(j, o): (mm, ww, s, d) for j, o, mm, ww, s, d in base_ops}
            tight_j = [j for j in range(J) if op_map[(j, len(jobs[j]) - 1)][2] + op_map[(j, len(jobs[j]) - 1)][3] >= base_mk - 8]
            other_j = [j for j in range(J) if j not in tight_j]
            chosen_j = set(tight_j[:4] + rng.sample(other_j, min(len(other_j), max(2, 8 - len(tight_j[:4])))))
            ruin_set = set(crit_ops) | {(j, o) for j in chosen_j for o in range(len(jobs[j]))}
        elif op_name == "CritEdgeFlip" and crit_edges:
            avail_edges = [e for e in crit_edges if (e[2], e[3]) not in flipped_tabu]
            if not avail_edges:
                flipped_tabu.clear()
                avail_edges = crit_edges
            chosen_e = rng.choice(avail_edges)
            u_flip, v_flip = chosen_e[2], chosen_e[3]
            flipped_tabu.add((u_flip, v_flip))
            forced_edges = [(u_flip, v_flip)]
            t_center = es[u_flip]
            op_map = {(j, o): (mm, ww, s, d) for j, o, mm, ww, s, d in base_ops}
            near = sorted(all_ops, key=lambda k: (abs(op_map[k][2] - t_center) + slack[k]))
            ruin_set = set(crit_ops) | set(near[:65])
            allow_slack = 4
        elif op_name == "CritWorkerShift":
            op_map = {(j, o): (mm, ww, s, d) for j, o, mm, ww, s, d in base_ops}
            flex_crit = [u for u in crit_ops if len(jobs[u[0]][u[1]]) > 1]
            if flex_crit:
                u_shift = rng.choice(flex_crit)
                forbidden_mw = {u_shift: (op_map[u_shift][0], op_map[u_shift][1])}
            low_slack = [k for k, _ in sorted(slack.items(), key=lambda x: x[1])[:65]]
            ruin_set = set(crit_ops) | set(low_slack)
            allow_slack = 3
        elif op_name == "BottleneckResourceRuin":
            op_map = {(j, o): (mm, ww, s, d) for j, o, mm, ww, s, d in base_ops}
            m_crit_cnt, w_crit_cnt = {}, {}
            for u in crit_ops:
                mm, ww = op_map[u][0], op_map[u][1]
                m_crit_cnt[mm] = m_crit_cnt.get(mm, 0) + 1
                w_crit_cnt[ww] = w_crit_cnt.get(ww, 0) + 1
            top_m = {m_id for m_id, _ in sorted(m_crit_cnt.items(), key=lambda x: -x[1])[:2]}
            top_w = {w_id for w_id, _ in sorted(w_crit_cnt.items(), key=lambda x: -x[1])[:3]}
            ruin_set = set(crit_ops) | {k for k, (mm, ww, _, _) in op_map.items() if mm in top_m or ww in top_w}
            if len(ruin_set) > 72:
                ruin_set = set(crit_ops) | set(sorted(ruin_set - set(crit_ops), key=lambda k: slack[k])[:max(10, 72 - len(crit_ops))])
        elif op_name == "FreeMWFixedOrder":
            low_slack = [k for k, _ in sorted(slack.items(), key=lambda x: x[1])[:72]]
            ruin_set = set(crit_ops) | set(low_slack)
        else:
            if len(elite_pool) >= 2:
                _, s1 = elite_pool[0]
                _, s2 = rng.choice(elite_pool[1:])
                m1 = {(j, o): (mm, ww) for j, o, mm, ww, _, _ in s1}
                m2 = {(j, o): (mm, ww) for j, o, mm, ww, _, _ in s2}
                diff_ops = {k for k in m1 if m1[k] != m2[k]}
                low_slack = [k for k, _ in sorted(slack.items(), key=lambda x: x[1])[:45]]
                ruin_set = set(crit_ops) | diff_ops | set(low_slack)
                if len(ruin_set) > 75:
                    ruin_set = set(crit_ops) | set(sorted(ruin_set - set(crit_ops), key=lambda k: slack[k])[:max(10, 75 - len(crit_ops))])
            else:
                low_slack = [k for k, _ in sorted(slack.items(), key=lambda x: x[1])[:65]]
                ruin_set = set(crit_ops) | set(low_slack)

        cand_mk, cand_ops = he.solve_lns_subproblem(
            J, M, W, jobs, base_ops, base_mk, ruin_set, op_name,
            forced_edges=forced_edges, forbidden_mw=forbidden_mw,
            window_bounds=window_bounds, compress_obj=compress_obj,
            allow_slack=allow_slack, secs=step_secs, nw=6, seed=seed * 100 + lns_iter,
        )

        need_v4_polish = (lns_iter % 5 == 0)
        polish_src = best_ops

        if cand_ops is not None:
            ok, mk_c, _ = fjsspw.check(fjs_path, {"ops": cand_ops})
            if ok:
                sig = tuple((r[0], r[1], r[2], r[3]) for r in sorted(cand_ops))
                is_new = sig not in seen_sigs
                if is_new and mk_c <= best_mk + 2:
                    seen_sigs.add(sig)
                    elite_pool.append((mk_c, cand_ops))
                    elite_pool.sort(key=lambda x: x[0])
                    if len(elite_pool) > 15:
                        elite_pool.pop()
                if mk_c < best_mk:
                    best_mk, best_ops = mk_c, cand_ops
                    msg = f"ALNS({op_name}) iter {lns_iter} -> {best_mk} at {round(time.time()-t_loop,1)}s"
                    events.append(msg)
                    print(f"    [U1] {msg}", flush=True)
                    polish_src = best_ops
                    need_v4_polish = True
                    if best_mk < target_bar:
                        break
                elif mk_c == best_mk and (compress_obj or is_new):
                    best_ops = cand_ops
                    polish_src = cand_ops
                    if is_new:
                        need_v4_polish = True

        # Ping-pong: run v4 Tabu Polish directly on the newly discovered ALNS basin!
        if need_v4_polish and best_mk >= target_bar:
            pmk, pops = v4_polish_from_ops(inst_name, fjs_path, nb, polish_src, seed + lns_iter * 17)
            if pmk is not None and pmk < best_mk:
                best_mk, best_ops = pmk, pops
                msg = f"v4-Polish after iter {lns_iter} -> {best_mk} at {round(time.time()-t_loop,1)}s"
                events.append(msg)
                print(f"    [U1] {msg}", flush=True)
                sig = tuple((r[0], r[1], r[2], r[3]) for r in sorted(pops))
                if sig not in seen_sigs:
                    seen_sigs.add(sig)
                    elite_pool.append((best_mk, best_ops))
                    elite_pool.sort(key=lambda x: x[0])
                if best_mk < target_bar:
                    break

    # Save best tie schedule for future reference
    with open(os.path.join(LOGS_DIR, "u1_best_schedule.json"), "w") as bf:
        json.dump({"instance": inst_name, "mk": best_mk, "ops": best_ops}, bf)

    beats = best_mk < target_bar
    wp = save_win(inst_name, fjs_path, target_bar, best_mk, best_ops) if beats else None
    return dict(
        phase="U1_PingPong", name=inst_name, true_bar=target_bar, mk=best_mk,
        vs_bar=best_mk - target_bar, alns_iters=lns_iter,
        outcome="WIN" if beats else "UNKNOWN", beats_bar=beats, win_path=wp,
        secs=round(time.time() - t0, 1), events=events,
    )


def solve_hard_carlier_6w(label, inst_name, fjs_name, true_bar, budget_s, seed, nw=6):
    """
    Hard-capped H = true_bar - 1 exact 6-core CP-SAT with:
      - H-conditioned Carlier heads/tails domain tightening [heads[j,o], H - tails[j,o]]
      - Non-dominated Carlier Head-Body-Tail linear cuts per machine (A + B + load <= H)
      - Machine & worker total load cuts (<= H) + Cumulative + strong disjunctive propagation
      - 6-worker full OR-Tools portfolio (max_lp + core + probing + LNS)
    """
    t0 = time.time()
    fjs_path = os.path.join(INST_DIR, fjs_name)
    J, M, W, jobs = fjsspw.parse(fjs_path)
    H = int(true_bar) - 1

    print(f"\n=== HARD CARLIER 6-CORE ({label} {inst_name}, H <= {H}, {int(budget_s)}s, {nw}w) ===", flush=True)
    heads, tails = he.compute_heads_tails(J, M, W, jobs, H_ub=H)
    lb_init = max(heads[j, len(ops) - 1] + min(ops[-1].values()) for j, ops in enumerate(jobs))
    if lb_init > H:
        print(f"  [{label} {inst_name}] PROVED OPTIMAL at presolve (lb_init={lb_init} > H={H})!", flush=True)
        return dict(
            phase=f"{label}_HardCarlier6w", name=inst_name, true_bar=true_bar, H=H,
            mk=None, outcome="PROVED_OPTIMAL_AT_BAR", cpsat_status="INFEASIBLE",
            beats_bar=False, win_path=None, secs=round(time.time() - t0, 2),
        )

    m = cp_model.CpModel()
    mk = m.NewIntVar(lb_init, H, "mk")
    S, D, E, B = {}, {}, {}, {}
    byM, byW, ivs = {}, {}, []
    m_op_terms = {r: {} for r in range(1, M + 1)}
    w_loads = {r: [] for r in range(1, W + 1)}

    for j, ops in enumerate(jobs):
        for o, alt in enumerate(ops):
            min_d = min(alt.values())
            lo_s = int(heads[j, o])
            hi_e = int(H - tails[j, o])
            if lo_s + min_d > hi_e:
                print(f"  [{label} {inst_name}] PROVED OPTIMAL at domain tighten ({j},{o}: {lo_s}+{min_d} > {hi_e})!", flush=True)
                return dict(
                    phase=f"{label}_HardCarlier6w", name=inst_name, true_bar=true_bar, H=H,
                    mk=None, outcome="PROVED_OPTIMAL_AT_BAR", cpsat_status="INFEASIBLE",
                    beats_bar=False, win_path=None, secs=round(time.time() - t0, 2),
                )
            s = m.NewIntVar(lo_s, hi_e - min_d, "")
            e = m.NewIntVar(lo_s + min_d, hi_e, "")
            ds = sorted(set(alt.values()))
            d = m.NewIntVarFromDomain(cp_model.Domain.FromValues(ds), "")
            m.Add(e == s + d)
            S[j, o] = s
            D[j, o] = d
            E[j, o] = e

            lits, bm, bw = [], {}, {}
            for (mm, ww), dur in alt.items():
                b = m.NewBoolVar("")
                B[j, o, mm, ww] = b
                lits.append(b)
                bm.setdefault(mm, []).append(b)
                bw.setdefault(ww, []).append(b)
                m_op_terms[mm].setdefault((j, o), []).append((dur, b * dur))
                w_loads[ww].append(b * dur)
            m.AddExactlyOne(lits)
            m.Add(d == sum(B[j, o, mm, ww] * dur for (mm, ww), dur in alt.items()))

            for grp, by in ((bm, byM), (bw, byW)):
                for r_id, bs in grp.items():
                    if len(bs) == len(lits):
                        by.setdefault(r_id, []).append(m.NewIntervalVar(s, d, e, ""))
                    elif len(bs) == 1:
                        by.setdefault(r_id, []).append(m.NewOptionalIntervalVar(s, d, e, bs[0], ""))
                    else:
                        p = m.NewBoolVar("")
                        m.Add(sum(bs) == p)
                        by.setdefault(r_id, []).append(m.NewOptionalIntervalVar(s, d, e, p, ""))
            ivs.append(m.NewIntervalVar(s, d, e, ""))
            if o > 0:
                m.Add(s >= E[j, o - 1])
        m.Add(mk >= E[j, len(ops) - 1])

    # Carlier Head-Body-Tail linear cuts conditioned on H = true_bar - 1
    n_cuts = 0
    for r, op_dict in m_op_terms.items():
        if not op_dict:
            continue
        all_terms = [t for pairs in op_dict.values() for _, t in pairs]
        m.Add(sum(all_terms) <= mk)
        n_cuts += 1
        ops_r = [
            (j, o, heads[j, o], tails[j, o], max(d for d, _ in pairs), [t for _, t in pairs])
            for (j, o), pairs in op_dict.items()
        ]
        As = sorted(set(x[2] for x in ops_r))
        Bs = sorted(set(x[3] for x in ops_r))
        seen_subs = set()
        for A in As:
            for B_val in Bs:
                if A == 0 and B_val == 0:
                    continue
                sub = tuple((x[0], x[1]) for x in ops_r if x[2] >= A and x[3] >= B_val)
                if len(sub) >= 2 and sub not in seen_subs:
                    max_load = sum(x[4] for x in ops_r if x[2] >= A and x[3] >= B_val)
                    if A + B_val + max_load > H:
                        seen_subs.add(sub)
                        sub_terms = [t for x in ops_r if x[2] >= A and x[3] >= B_val for t in x[5]]
                        m.Add(A + B_val + sum(sub_terms) <= mk)
                        n_cuts += 1

    for r, wlist in w_loads.items():
        if wlist:
            m.Add(sum(wlist) <= mk)
            n_cuts += 1

    for lst in byM.values():
        m.AddNoOverlap(lst)
    for lst in byW.values():
        m.AddNoOverlap(lst)
    m.AddCumulative(ivs, [1] * len(ivs), min(M, W))
    m.Minimize(mk)

    print(f"  [{label} {inst_name}] Model built: lb_init={lb_init}, H={H}, carlier_cuts={n_cuts}", flush=True)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(budget_s)
    sv.parameters.num_workers = int(nw)
    sv.parameters.random_seed = int(seed)
    sv.parameters.use_strong_propagation_in_disjunctive = True
    sv.parameters.use_overload_checker_in_cumulative = True
    sv.parameters.use_hard_precedences_in_cumulative = True

    st = sv.Solve(m, FirstWinStopCallback())
    st_name = sv.StatusName(st)

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sched = _extract_sched(inst_name, jobs, S, B, sv)
        ok, cmk, errs = fjsspw.check(fjs_path, sched)
        assert ok and cmk <= H, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} H={H} errs={errs[:3]}"
        wp = save_win(inst_name, fjs_path, true_bar, int(cmk), sched["ops"])
        print(f"  [{label} {inst_name}] WIN!! mk={cmk} < bar={true_bar} ({cmk-true_bar:+d}) in {round(time.time()-t0,1)}s!", flush=True)
        return dict(
            phase=f"{label}_HardCarlier6w", name=inst_name, true_bar=true_bar, H=H,
            mk=int(cmk), vs_bar=int(cmk) - true_bar, outcome="WIN", cpsat_status=st_name,
            beats_bar=True, win_path=wp, secs=round(time.time() - t0, 1),
        )

    outcome = "PROVED_OPTIMAL_AT_BAR" if st == cp_model.INFEASIBLE else st_name
    print(f"  [{label} {inst_name}] {outcome} (status={st_name}) in {round(time.time()-t0,1)}s", flush=True)
    return dict(
        phase=f"{label}_HardCarlier6w", name=inst_name, true_bar=true_bar, H=H,
        mk=None, outcome=outcome, cpsat_status=st_name,
        beats_bar=False, win_path=None, secs=round(time.time() - t0, 1),
    )


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "u1_u2_final_push.jsonl")
    with open(log_path, "w"):
        pass

    t_all = time.time()

    # 1. U1 ALNS-CPSAT <-> v4 Ping-Pong (30m)
    r1 = run_u1_pingpong(budget_s=1800.0, seed=920001)
    with open(log_path, "a") as lf:
        lf.write(json.dumps(r1) + "\n")

    # 2. U2 Hard-Capped H=25 Carlier 6-Core CP-SAT (20m)
    r2 = solve_hard_carlier_6w("U2", "BrandimarteMk2", "BrandimarteMk2.fjs", 26, 1200.0, seed=920002, nw=6)
    with open(log_path, "a") as lf:
        lf.write(json.dumps(r2) + "\n")

    # 3. U1 Hard-Capped H=980 Carlier 6-Core CP-SAT (15m) if Phase 1 didn't win
    if not r1["beats_bar"]:
        r3 = solve_hard_carlier_6w("U1", "Hurinkrdata16", "Hurinkrdata16.fjs", 981, 900.0, seed=920003, nw=6)
        with open(log_path, "a") as lf:
            lf.write(json.dumps(r3) + "\n")

    print(f"\nFINAL PUSH COMPLETE in {round((time.time() - t_all)/60.0, 2)}m wall.", flush=True)


if __name__ == "__main__":
    main()
