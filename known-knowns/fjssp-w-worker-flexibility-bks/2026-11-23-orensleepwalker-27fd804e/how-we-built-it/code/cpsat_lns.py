"""
CP-SAT Large Neighborhood Search (LNS) Polish for FJSSP-W.
Takes an incumbent schedule (op_alt, est) from Numba Critical-Path Tabu Search and runs:
  1. Exact Fixed-Mode Rescheduling (all N ops keep their (m, w), CP-SAT optimizes global sequencing).
  2. Critical-Window / Critical-Subset Destroy & Repair (30-50 ops freed with top-K modes each;
     remaining ops keep fixed (m, w) while free to slide in time).
Total optional intervals stay ~1,000-1,500 even on 2.5 MB Behnke58 (250x smaller than full CP-SAT).
"""
import random
import time
import numpy as np
from ortools.sat.python import cp_model


def _compute_critical_ops(nb_inst, op_alt, est, mk):
    """Identify ops on or near the critical path (slack <= 2)."""
    N = int(nb_inst["N"])
    alt_d = nb_inst["alt_d"]
    job_succ = nb_inst["job_succ"]
    dur = np.array([int(alt_d[int(op_alt[u])]) for u in range(N)], dtype=np.int32)
    # Approximate slack via job-chain + makespan proximity
    # Also mark ops that finish at mk or feed into them
    crit = []
    for u in range(N):
        if int(est[u]) + int(dur[u]) >= mk - 2:
            crit.append(u)
    # Also include high-load window ops
    return crit


def solve_fixed_mode_cpsat(nb_inst, op_alt, est, cur_mk, time_limit_s=10.0, num_workers=1):
    """Exact sequencing with fixed (m, w) for all N ops, hinted with incumbent."""
    N = int(nb_inst["N"])
    M = int(nb_inst["M"])
    W = int(nb_inst["W"])
    job_pred = nb_inst["job_pred"]
    alt_m = nb_inst["alt_m"]
    alt_w = nb_inst["alt_w"]
    alt_d = nb_inst["alt_d"]

    model = cp_model.CpModel()
    horizon = int(cur_mk)
    starts = [model.NewIntVar(0, horizon, f"s_{u}") for u in range(N)]
    ends = [None] * N
    m_ints = [[] for _ in range(M)]
    w_ints = [[] for _ in range(W)]

    for u in range(N):
        a = int(op_alt[u])
        m = int(alt_m[a])
        w = int(alt_w[a])
        d = int(alt_d[a])
        e = model.NewIntVar(d, horizon, f"e_{u}")
        iv = model.NewIntervalVar(starts[u], d, e, f"iv_{u}")
        ends[u] = e
        m_ints[m].append(iv)
        w_ints[w].append(iv)
        model.AddHint(starts[u], int(est[u]))
        jp = int(job_pred[u])
        if jp != -1:
            model.Add(starts[u] >= ends[jp])

    for m in range(M):
        if len(m_ints[m]) > 1:
            model.AddNoOverlap(m_ints[m])
    for w in range(W):
        if len(w_ints[w]) > 1:
            model.AddNoOverlap(w_ints[w])

    mk_var = model.NewIntVar(0, horizon, "mk")
    model.AddMaxEquality(mk_var, ends)
    model.Minimize(mk_var)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit_s)
    solver.parameters.num_search_workers = int(num_workers)
    solver.parameters.use_strong_propagation_in_disjunctive = True

    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        new_mk = int(round(solver.ObjectiveValue()))
        if new_mk < cur_mk:
            new_est = np.array([int(solver.Value(starts[u])) for u in range(N)], dtype=np.int32)
            return new_mk, op_alt.copy(), new_est
    return cur_mk, op_alt, est


def solve_lns_window_cpsat(nb_inst, op_alt, est, cur_mk, free_ops, max_k_modes=25,
                           time_limit_s=12.0, num_workers=1, rng=None):
    """
    Destroy & Repair CP-SAT:
      - ops in free_ops can choose from up to max_k_modes (incumbent + fastest + least-loaded)
      - all other ops keep their incumbent (m, w) but can slide in time
    """
    if rng is None:
        rng = random.Random(42)

    N = int(nb_inst["N"])
    M = int(nb_inst["M"])
    W = int(nb_inst["W"])
    job_pred = nb_inst["job_pred"]
    alt_start = nb_inst["alt_start"]
    alt_m = nb_inst["alt_m"]
    alt_w = nb_inst["alt_w"]
    alt_d = nb_inst["alt_d"]

    free_set = set(int(u) for u in free_ops)

    # Compute current machine & worker total load (for selecting low-load alternative modes)
    m_load = np.zeros(M, dtype=np.int32)
    w_load = np.zeros(W, dtype=np.int32)
    for u in range(N):
        a = int(op_alt[u])
        d = int(alt_d[a])
        m_load[int(alt_m[a])] += d
        w_load[int(alt_w[a])] += d

    model = cp_model.CpModel()
    horizon = int(cur_mk)
    starts = [model.NewIntVar(0, horizon, f"s_{u}") for u in range(N)]
    ends = [model.NewIntVar(0, horizon, f"e_{u}") for u in range(N)]
    m_ints = [[] for _ in range(M)]
    w_ints = [[] for _ in range(W)]
    free_pres = {}  # u -> list of (a, pres_var)

    for u in range(N):
        cur_a = int(op_alt[u])
        model.AddHint(starts[u], int(est[u]))
        model.AddHint(ends[u], int(est[u]) + int(alt_d[cur_a]))

        if u not in free_set:
            m = int(alt_m[cur_a])
            w = int(alt_w[cur_a])
            d = int(alt_d[cur_a])
            iv = model.NewIntervalVar(starts[u], d, ends[u], f"f_{u}")
            m_ints[m].append(iv)
            w_ints[w].append(iv)
        else:
            a0 = int(alt_start[u])
            a1 = int(alt_start[u + 1])
            n_alts = a1 - a0
            if n_alts <= max_k_modes:
                cand_alts = list(range(a0, a1))
            else:
                # Always include incumbent + fastest + lowest (d + 0.1*(m_load+w_load))
                chosen = {cur_a}
                # Top fastest
                for a in range(a0, min(a1, a0 + max_k_modes // 2)):
                    chosen.add(a)
                # Score remaining by duration + resource load
                scored = []
                for a in range(a0, a1):
                    if a in chosen:
                        continue
                    sc = int(alt_d[a]) * 10 + int(m_load[int(alt_m[a])] + w_load[int(alt_w[a])]) // 4
                    scored.append((sc, a))
                scored.sort()
                need = max_k_modes - len(chosen)
                for _, a in scored[:need]:
                    chosen.add(a)
                cand_alts = sorted(chosen)

            pres_list = []
            for a in cand_alts:
                m = int(alt_m[a])
                w = int(alt_w[a])
                d = int(alt_d[a])
                p = model.NewBoolVar(f"p_{u}_{a}")
                model.AddHint(p, 1 if a == cur_a else 0)
                iv = model.NewOptionalIntervalVar(starts[u], d, ends[u], p, f"o_{u}_{a}")
                m_ints[m].append(iv)
                w_ints[w].append(iv)
                pres_list.append((a, p))
            model.AddExactlyOne([p for _, p in pres_list])
            free_pres[u] = pres_list

    for u in range(N):
        jp = int(job_pred[u])
        if jp != -1:
            model.Add(starts[u] >= ends[jp])

    for m in range(M):
        if len(m_ints[m]) > 1:
            model.AddNoOverlap(m_ints[m])
    for w in range(W):
        if len(w_ints[w]) > 1:
            model.AddNoOverlap(w_ints[w])

    mk_var = model.NewIntVar(0, horizon, "mk")
    model.AddMaxEquality(mk_var, ends)
    model.Minimize(mk_var)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit_s)
    solver.parameters.num_search_workers = int(num_workers)
    solver.parameters.use_strong_propagation_in_disjunctive = True

    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        new_mk = int(round(solver.ObjectiveValue()))
        if new_mk < cur_mk:
            new_alt = op_alt.copy()
            new_est = np.array([int(solver.Value(starts[u])) for u in range(N)], dtype=np.int32)
            for u, pres_list in free_pres.items():
                for a, p in pres_list:
                    if solver.Value(p) == 1:
                        new_alt[u] = a
                        break
            return new_mk, new_alt, new_est
    return cur_mk, op_alt, est


def lns_polish(nb_inst, op_alt, est, cur_mk, time_budget_s=90.0, seed=42):
    """Run iterative Fixed-Mode + Critical-Window CP-SAT LNS within time_budget_s."""
    t0 = time.time()
    rng = random.Random(seed)
    N = int(nb_inst["N"])
    alt_d = nb_inst["alt_d"]
    alt_m = nb_inst["alt_m"]
    alt_w = nb_inst["alt_w"]

    best_mk = int(cur_mk)
    best_alt = op_alt.copy()
    best_est = est.copy()
    rounds = 0
    improvements = 0

    # Round 0: Global Exact Fixed-Mode Rescheduling
    if time.time() - t0 < time_budget_s - 5:
        nmk, nalt, nest = solve_fixed_mode_cpsat(nb_inst, best_alt, best_est, best_mk, time_limit_s=10.0)
        rounds += 1
        if nmk < best_mk:
            best_mk, best_alt, best_est = nmk, nalt, nest
            improvements += 1

    # Iterative Destroy & Repair rounds
    while time.time() - t0 < time_budget_s - 4:
        rem = time_budget_s - (time.time() - t0)
        tl = min(12.0, max(4.0, rem))
        mode_type = rounds % 3

        if mode_type == 0:
            # Time-window destroy: pick window [t_start, t_end]
            win_w = max(15, int(best_mk * rng.uniform(0.18, 0.35)))
            t_start = rng.randint(0, max(0, best_mk - win_w))
            t_end = t_start + win_w
            cands = [
                u for u in range(N)
                if int(best_est[u]) <= t_end and int(best_est[u]) + int(alt_d[int(best_alt[u])]) >= t_start
            ]
            target_sz = min(45 if N >= 250 else 35, len(cands))
            free_ops = rng.sample(cands, target_sz) if len(cands) > target_sz else cands
        elif mode_type == 1:
            # Bottleneck-machine + bottleneck-worker destroy
            m_max = np.zeros(int(nb_inst["M"]), dtype=np.int32)
            for u in range(N):
                a = int(best_alt[u])
                fin = int(best_est[u]) + int(alt_d[a])
                m = int(alt_m[a])
                if fin > m_max[m]:
                    m_max[m] = fin
            top_ms = list(np.argsort(-m_max)[:4])
            chosen_m = rng.choice(top_ms)
            cands = [u for u in range(N) if int(alt_m[int(best_alt[u])]) == chosen_m]
            # Add some late-finishing ops
            late = sorted(range(N), key=lambda u: -(int(best_est[u]) + int(alt_d[int(best_alt[u])])))[:25]
            pool = list(set(cands + late))
            target_sz = min(45 if N >= 250 else 35, len(pool))
            free_ops = rng.sample(pool, target_sz) if len(pool) > target_sz else pool
        else:
            # Random jobs destroy (4-8 complete jobs)
            J = int(nb_inst["J"])
            op_job = nb_inst["op_job"]
            k_jobs = min(J, rng.randint(4, 8))
            chosen_jobs = set(rng.sample(range(J), k_jobs))
            free_ops = [u for u in range(N) if int(op_job[u]) in chosen_jobs]
            if len(free_ops) > 50:
                free_ops = rng.sample(free_ops, 50)

        if not free_ops:
            rounds += 1
            continue

        k_modes = 25 if N >= 250 else 35
        nmk, nalt, nest = solve_lns_window_cpsat(
            nb_inst, best_alt, best_est, best_mk, free_ops,
            max_k_modes=k_modes, time_limit_s=tl, num_workers=1, rng=rng,
        )
        rounds += 1
        if nmk < best_mk:
            best_mk, best_alt, best_est = nmk, nalt, nest
            improvements += 1
            # Follow up with quick fixed-mode rescheduling
            if time.time() - t0 < time_budget_s - 6:
                fmk, falt, fest = solve_fixed_mode_cpsat(nb_inst, best_alt, best_est, best_mk, time_limit_s=6.0)
                if fmk < best_mk:
                    best_mk, best_alt, best_est = fmk, falt, fest
                    improvements += 1

    return best_mk, best_alt, best_est, dict(rounds=rounds, improvements=improvements, secs=round(time.time() - t0, 2))
