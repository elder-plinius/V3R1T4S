"""Multi-neighborhood CP-SAT Large Neighborhood Search (LNS) for MMLIB+."""
import os
import sys
import time
import numpy as np
from ortools.sat.python import cp_model

PHASEB_DIR = os.path.dirname(os.path.abspath(__file__))
SOLVER_CODE = os.path.abspath(os.path.join(PHASEB_DIR, "..", "code"))
if SOLVER_CODE not in sys.path:
    sys.path.insert(0, SOLVER_CODE)

import engine  # noqa: E402
import fast_meta  # noqa: E402


def solve_lns_subproblem(
    I: dict,
    X,
    modes: np.ndarray,
    starts: np.ndarray,
    cur_mk: int,
    free_mode_jobs: set,
    start_radius: int,
    time_limit: float,
    workers: int = 1,
    seed: int = 1,
    allow_tie: bool = False,
):
    """
    Solve an exact CP-SAT subproblem where:
    - Jobs in `free_mode_jobs` have FREE modes (optional intervals) and start times in
      [max(0, s - 2*R), min(H, s + 2*R)] (or [0, H] if R >= H).
    - Jobs NOT in `free_mode_jobs` have FIXED modes (mandatory intervals!) and start times in
      [max(0, s - R), min(H, s + R)].
    - Makespan S[n-1] <= cur_mk - 1 (or <= cur_mk if allow_tie=True), minimizing S[n-1].
    """
    n = I["n"]
    H = cur_mk if allow_tie else max(1, cur_mk - 1)
    m = cp_model.CpModel()

    S = [None] * n
    E = [None] * n
    X_vars = {}
    ivs = [[] for _ in I["Rcap"]]

    # Track fixed non-renewable consumption
    nr_fixed = [0] * len(I["Ncap"])

    for j in range(n):
        if j == 0:
            S[j] = m.NewConstant(0)
            E[j] = m.NewConstant(0)
            continue
        if j == n - 1:
            S[j] = m.NewIntVar(0, H, f"S_{j}")
            E[j] = S[j]
            continue

        sj_old = int(starts[j])
        if j in free_mode_jobs:
            min_d = min(row[0] for row in I["modes"][j])
            if H - min_d < 0:
                return None
            rad_l = start_radius * 2
            rad_r = max(4, start_radius)
            if rad_l >= H:
                lo, hi = 0, H - min_d
            else:
                hi = min(H - min_d, sj_old + rad_r)
                lo = min(hi, max(0, sj_old - rad_l))
            if hi < 0 or lo > hi:
                return None
            S[j] = m.NewIntVar(lo, hi, f"S_{j}")
            E[j] = m.NewIntVar(lo + min_d, H, f"E_{j}")
            xs = [m.NewBoolVar(f"x_{j}_{t}") for t in range(len(I["modes"][j]))]
            X_vars[j] = xs
            m.AddExactlyOne(xs)
            for t, (x, (d, r, _)) in enumerate(zip(xs, I["modes"][j])):
                iv = m.NewOptionalIntervalVar(S[j], d, E[j], x, f"iv_{j}_{t}")
                for k, q in enumerate(r):
                    if q:
                        ivs[k].append((iv, q))
        else:
            mj = int(modes[j]) - 1
            d, r, nr = I["modes"][j][mj]
            for k, q in enumerate(nr):
                nr_fixed[k] += q
            if H - d < 0:
                return None
            rad_l = start_radius
            rad_r = max(3, start_radius // 2)
            if rad_l >= H:
                lo, hi = 0, H - d
            else:
                hi = min(H - d, sj_old + rad_r)
                lo = min(hi, max(0, sj_old - rad_l))
            if hi < 0 or lo > hi:
                return None
            S[j] = m.NewIntVar(lo, hi, f"S_{j}")
            E[j] = m.NewIntVar(lo + d, hi + d, f"E_{j}")
            iv = m.NewIntervalVar(S[j], d, E[j], f"iv_{j}")
            for k, q in enumerate(r):
                if q:
                    ivs[k].append((iv, q))

    # Renewable cumulative constraints
    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)

    # Non-renewable knapsack constraints (only over free_mode_jobs)
    for k, c in enumerate(I["Ncap"]):
        rem_cap = c - nr_fixed[k]
        if rem_cap < 0:
            return None
        terms = []
        for j in free_mode_jobs:
            if j == 0 or j == n - 1:
                continue
            for t, x in enumerate(X_vars[j]):
                q = I["modes"][j][t][2][k]
                if q:
                    terms.append(x * q)
        if terms:
            m.Add(sum(terms) <= rem_cap)

    # Precedence constraints
    for j in range(n):
        for s in I["succ"][j]:
            m.Add(S[s] >= E[j])

    # Warm-start hints (clamped to new bounds)
    for j in range(1, n - 1):
        sj = min(int(starts[j]), H)
        m.AddHint(S[j], sj)
        if j in X_vars:
            mj = int(modes[j]) - 1
            for t, x in enumerate(X_vars[j]):
                m.AddHint(x, 1 if t == mj else 0)

    m.Minimize(S[n - 1])

    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(time_limit)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    new_modes = modes.copy()
    for j, xs in X_vars.items():
        for t, x in enumerate(xs):
            if sv.Value(x) == 1:
                new_modes[j] = t + 1
                break
    new_starts = np.array([sv.Value(S[j]) for j in range(n)], dtype=np.int64)
    new_mk = int(new_starts[n - 1])
    return new_mk, new_modes, new_starts, sv.StatusName(st)


def pick_neighborhood(X, modes, starts, cur_mk, kind: str, k_free: int, rng):
    """Select `k_free` jobs whose modes will be unfrozen."""
    n = X.n
    real_jobs = np.arange(1, n - 1)
    k_free = min(k_free, n - 2)

    if kind == "fixed_mode":
        return set()

    if kind == "window":
        # Pick a random time window [t0, t1] and take k_free jobs closest to t_center
        t_center = int(rng.integers(0, max(1, cur_mk)))
        durs = np.array([X.dur[j, modes[j] - 1] for j in real_jobs])
        mids = starts[real_jobs] + durs // 2
        dists = np.abs(mids - t_center) + rng.uniform(0, 1.5, size=len(real_jobs))
        chosen = real_jobs[np.argsort(dists)[:k_free]]
        return set(int(j) for j in chosen)

    if kind == "critical_plus_nr":
        # Pick critical jobs + random jobs that consume NR (so they can trade NR budget!)
        crit = fast_meta.compute_critical_mask(starts, modes, X.dur, X.pp, X.pi, X.sp, X.si)
        crit_jobs = [int(j) for j in real_jobs if crit[j] == 1]
        rng.shuffle(crit_jobs)
        chosen = list(crit_jobs[: max(1, (k_free * 2) // 3)])
        chosen_set = set(chosen)
        others = [int(j) for j in real_jobs if j not in chosen_set]
        # Prefer jobs with positive NR usage so they can give back NR budget
        nr_use = np.array([sum(X.nreq[j, modes[j] - 1]) for j in others], dtype=np.float64) + 0.5
        probs = nr_use / nr_use.sum()
        need = k_free - len(chosen)
        if need > 0 and others:
            extra = rng.choice(others, size=min(need, len(others)), replace=False, p=probs)
            chosen_set.update(int(j) for j in extra)
        return chosen_set

    if kind == "tail":
        # Focus on the last 40% of the schedule + some NR donors
        t_cut = int(cur_mk * 0.6)
        tail_jobs = [int(j) for j in real_jobs if starts[j] >= t_cut]
        rng.shuffle(tail_jobs)
        chosen_set = set(tail_jobs[: max(1, (k_free * 2) // 3)])
        others = [int(j) for j in real_jobs if j not in chosen_set]
        need = k_free - len(chosen_set)
        if need > 0 and others:
            extra = rng.choice(others, size=min(need, len(others)), replace=False)
            chosen_set.update(int(j) for j in extra)
        return chosen_set

    # Fallback: random subset
    chosen = rng.choice(real_jobs, size=k_free, replace=False)
    return set(int(j) for j in chosen)


def cpsat_lns_loop(
    I: dict,
    X,
    init_modes: np.ndarray,
    init_starts: np.ndarray,
    time_budget: float,
    workers: int = 1,
    seed: int = 1,
    ub_target: int = -1,
):
    """
    Adaptive CP-SAT LNS + fast Numba FBI/mode-LS polishing loop.
    Returns: (best_mk, best_modes, best_starts, stats)
    """
    t0 = time.time()
    rng = np.random.default_rng(seed)
    topo = np.array(engine.topo(X), dtype=np.int64)

    best_modes = np.asarray(init_modes, dtype=np.int64).copy()
    best_starts = np.asarray(init_starts, dtype=np.int64).copy()
    best_mk = int(best_starts[-1])

    # Immediate FBI polish on initial schedule
    o0 = fast_meta.order_from_starts(best_starts, topo)
    mk_fbi, st_fbi = fast_meta.eval_modes_order(o0, best_modes, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20)
    if mk_fbi < best_mk:
        best_mk, best_starts = int(mk_fbi), st_fbi

    n_real = X.n - 2
    n_modes = X.dur.shape[1]
    # Scale neighborhood size to keep CP-SAT subproblems snappy
    if n_real <= 55:
        base_k = 24 if n_modes <= 3 else (18 if n_modes <= 6 else 14)
        radii = [best_mk, 14, 8]
    else:
        base_k = 22 if n_modes <= 3 else (16 if n_modes <= 6 else 12)
        radii = [12, 8, 20]

    kinds = ["fixed_mode", "critical_plus_nr", "window", "tail", "random"]
    iters = 0
    improvements = 0
    step_log = []

    while time.time() - t0 < time_budget:
        rem = time_budget - (time.time() - t0)
        if rem < 0.8:
            break

        kind = kinds[iters % len(kinds)] if iters > 0 else "fixed_mode"
        # After first fixed_mode check, only retry fixed_mode when modes changed
        if iters > 0 and kind == "fixed_mode":
            kind = kinds[1 + (iters % (len(kinds) - 1))]

        k_free = 0 if kind == "fixed_mode" else int(rng.integers(max(8, base_k - 5), base_k + 6))
        rad = best_mk if (kind == "fixed_mode" and n_real <= 55) else radii[iters % len(radii)]
        sub_tl = min(rem, 3.0 if kind == "fixed_mode" else (4.0 if n_real <= 55 else 5.0))

        free_set = pick_neighborhood(X, best_modes, best_starts, best_mk, kind, k_free, rng)
        res = solve_lns_subproblem(
            I, X, best_modes, best_starts, best_mk, free_set, rad, sub_tl,
            workers=workers, seed=seed + iters * 97, allow_tie=False
        )
        iters += 1

        if res is not None:
            new_mk, new_modes, new_starts, status = res
            if new_mk < best_mk:
                improvements += 1
                best_mk, best_modes, best_starts = new_mk, new_modes, new_starts
                step_log.append((round(time.time() - t0, 1), kind, k_free, rad, new_mk))
                # Immediately polish with fast Numba multistart + mode LS!
                mk_ms, st_ms = engine.multistart(X, best_modes, 300, seed=seed + iters * 13)
                if mk_ms < best_mk:
                    best_mk, best_starts = int(mk_ms), st_ms
                    step_log.append((round(time.time() - t0, 1), "ms_polish", 0, 0, best_mk))
                o_cur = fast_meta.order_from_starts(best_starts, topo)
                mk_ls, _, m_ls, st_ls, _ = fast_meta.mode_local_search(
                    o_cur, best_modes, best_starts, best_mk, X.dur, X.req, X.nreq, X.nm,
                    X.cap, X.ncap, X.pp, X.pi, X.sp, X.si, X.H, topo, 300, 6, seed + iters * 29
                )
                if mk_ls < best_mk:
                    best_mk, best_modes, best_starts = int(mk_ls), m_ls, st_ls
                    step_log.append((round(time.time() - t0, 1), "mode_ls", 0, 0, best_mk))
                # Try one quick fixed_mode exact solve on the improved mode vector
                rem2 = time_budget - (time.time() - t0)
                if rem2 >= 2.0:
                    res2 = solve_lns_subproblem(
                        I, X, best_modes, best_starts, best_mk, set(), best_mk if n_real <= 55 else 15,
                        min(rem2, 2.5), workers=workers, seed=seed + iters * 101, allow_tie=False
                    )
                    if res2 is not None and res2[0] < best_mk:
                        best_mk, best_modes, best_starts = res2[0], res2[1], res2[2]
                        step_log.append((round(time.time() - t0, 1), "fixed_exact", 0, 0, best_mk))

    return best_mk, best_modes, best_starts, {
        "iters": iters,
        "improvements": improvements,
        "secs": round(time.time() - t0, 2),
        "steps": step_log,
    }
