"""
Exact Frozen-Prefix + Shifted-Suffix CP-SAT Window Compression for MMLIB+.
Given a valid incumbent (modes, starts) with makespan MK:
  - Choose a window [t0, t1] (with 0 <= t0 < t1 <= MK).
  - Prefix P = {j : starts[j] + d[j] <= t0}: FIXED mode, FIXED start = starts[j].
  - Suffix S = {j : starts[j] >= t1}: FIXED mode, FIXED start = starts[j] - delta (delta >= 1).
  - Window F = all other jobs (overlapping (t0, t1)), PLUS optional NR-donor jobs from P/S
    whose mode is free (with start fixed or slightly flexible) so NR budget can be traded across the whole project!
  - Only jobs in F have decision variables! All P and S jobs are constants (0 branching!).
If feasible for delta=1 -> GUARANTEED strictly better schedule MK - 1!
"""
import os
import sys
import time
import numpy as np
from ortools.sat.python import cp_model

PHASEB_DIR = os.path.dirname(os.path.abspath(__file__))
SOLVER_CODE = os.path.abspath(os.path.join(PHASEB_DIR, "..", "code"))
if SOLVER_CODE not in sys.path:
    sys.path.insert(0, SOLVER_CODE)

import mm  # noqa: E402
import engine  # noqa: E402
import fast_meta  # noqa: E402


def compress_window(
    I: dict,
    modes: np.ndarray,
    starts: np.ndarray,
    t0: int,
    t1: int,
    delta: int = 1,
    nr_donors: set = None,
    time_limit: float = 4.0,
    workers: int = 1,
    seed: int = 1,
):
    """
    Attempt to compress window [t0, t1] by `delta` time units.
    Returns (new_mk, new_modes, new_starts, status_name) if strictly improved, else None.
    """
    n = I["n"]
    mk = int(starts[n - 1])
    new_mk = mk - delta
    if new_mk < 1 or t1 - delta < t0:
        return None

    durs = [I["modes"][j][int(modes[j]) - 1][0] for j in range(n)]
    ends = [int(starts[j]) + durs[j] for j in range(n)]

    # Partition jobs:
    # 0 is always in P (start=0, end=0); n-1 is always in S (start=mk-delta)
    P = set()
    S = set()
    F = set()
    for j in range(n):
        if j == 0:
            P.add(j)
        elif j == n - 1:
            S.add(j)
        elif ends[j] <= t0:
            P.add(j)
        elif int(starts[j]) >= t1:
            S.add(j)
        else:
            F.add(j)

    if not F:
        return None

    # Validate that no direct precedence goes from S to P or P to S with violation
    # P->S: ends[p] <= t0 <= t1 - delta <= starts[s] - delta -> ALWAYS VALID!
    # Check if any job in P or S is an NR donor (free mode, fixed/tight start)
    donors = set()
    if nr_donors:
        for j in nr_donors:
            if j in P or j in S:
                if j != 0 and j != n - 1:
                    donors.add(j)

    # Compute fixed start/end for non-F jobs
    fixed_s = {}
    fixed_e = {}
    for j in P:
        fixed_s[j] = int(starts[j])
        fixed_e[j] = ends[j]
    for j in S:
        fixed_s[j] = int(starts[j]) - delta
        fixed_e[j] = ends[j] - delta

    # Check if any fixed P->S precedence is violated (shouldn't happen since t0 <= t1 - delta)
    for j in P:
        for s in I["succ"][j]:
            if s in S and fixed_e[j] > fixed_s[s]:
                return None

    m = cp_model.CpModel()
    S_var = {}
    E_var = {}
    X_var = {}
    ivs = [[] for _ in I["Rcap"]]
    nr_fixed = [0] * len(I["Ncap"])

    # Determine time range where F jobs can live
    # Actually, F jobs can start as early as max(ends[p] for p in pred(j)&P) and end <= min(starts[s]-delta for s in succ(j)&S)
    # To keep cumulative compact, restrict F jobs to [max(0, t0 - margin), min(new_mk, t1 - delta + margin)]
    # Better yet: let F jobs move freely in [0, new_mk] bounded by precedences, and only include P/S intervals that could overlap!
    margin = max(6, (t1 - t0) // 2)
    win_lo = max(0, t0 - margin)
    win_hi = min(new_mk, t1 - delta + margin)

    # Add F jobs (free start + free mode)
    for j in F:
        min_d = min(row[0] for row in I["modes"][j])
        lo = win_lo
        hi = win_hi - min_d
        # Tighten from P preds and S succs
        for s in I["succ"][j]:
            if s in S:
                hi = min(hi, fixed_s[s] - min_d)
        if lo > hi:
            return None
        S_var[j] = m.NewIntVar(lo, hi, f"S_{j}")
        E_var[j] = m.NewIntVar(lo + min_d, min(win_hi, hi + max(row[0] for row in I["modes"][j])), f"E_{j}")
        xs = [m.NewBoolVar(f"x_{j}_{t}") for t in range(len(I["modes"][j]))]
        X_var[j] = xs
        m.AddExactlyOne(xs)
        for t, (x, (d, r, _)) in enumerate(zip(xs, I["modes"][j])):
            iv = m.NewOptionalIntervalVar(S_var[j], d, E_var[j], x, f"iv_{j}_{t}")
            for k, q in enumerate(r):
                if q:
                    ivs[k].append((iv, q))

    # Add P and S jobs:
    # - Non-donor jobs: fixed constant intervals ONLY if they overlap [win_lo, win_hi]!
    # - Donor jobs: free mode (only modes whose dur <= available slack before successors!), fixed start = fixed_s[j]
    #   Wait: if a donor job is outside [win_lo, win_hi], changing its mode might violate renewable capacity outside [win_lo, win_hi]
    #   UNLESS we only allow donor modes with req[k] <= current_req[k] and dur <= current_dur, OR we include all jobs overlapping donor!
    #   Simple & 100% EXACT rule: for donor jobs, only allow modes with dur <= old_dur AND req[r] <= old_req[r] for all r!
    #   Wait: that's a dominance-safe NR donor! Even better: if donor is inside [win_lo, win_hi], all modes are allowed because all overlapping jobs are in cumulative!
    for j in range(n):
        if j in F:
            continue
        if j == 0 or j == n - 1:
            continue
        sj = fixed_s[j]
        ej = fixed_e[j]
        mj = int(modes[j]) - 1
        d_old, r_old, nr_old = I["modes"][j][mj]

        if j in donors:
            # Find modes safe w.r.t. fixed external schedule (dur <= d_old and req <= r_old)
            safe_modes = []
            for t, (d, r, nr) in enumerate(I["modes"][j]):
                if d <= d_old and all(r[k] <= r_old[k] for k in range(len(r))):
                    safe_modes.append(t)
            if len(safe_modes) > 1:
                xs = [m.NewBoolVar(f"dx_{j}_{t}") for t in safe_modes]
                X_var[j] = (safe_modes, xs)
                m.AddExactlyOne(xs)
                if ej > win_lo and sj < win_hi:
                    for idx_t, t in enumerate(safe_modes):
                        d, r, _ = I["modes"][j][t]
                        iv = m.NewOptionalFixedSizeIntervalVar(sj, d, xs[idx_t], f"div_{j}_{t}")
                        for k, q in enumerate(r):
                            if q:
                                ivs[k].append((iv, q))
                continue

        # Standard fixed job
        for k, q in enumerate(nr_old):
            nr_fixed[k] += q
        if ej > win_lo and sj < win_hi and d_old > 0:
            iv = m.NewFixedSizeIntervalVar(sj, d_old, f"fix_{j}")
            for k, q in enumerate(r_old):
                if q:
                    ivs[k].append((iv, q))

    # Renewable cumulative constraints
    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)

    # Non-renewable knapsack constraints
    for k, c in enumerate(I["Ncap"]):
        rem_cap = c - nr_fixed[k]
        if rem_cap < 0:
            return None
        terms = []
        for j, x_info in X_var.items():
            if j in F:
                for t, x in enumerate(x_info):
                    q = I["modes"][j][t][2][k]
                    if q:
                        terms.append(x * q)
            else:
                safe_modes, xs = x_info
                for idx_t, t in enumerate(safe_modes):
                    q = I["modes"][j][t][2][k]
                    if q:
                        terms.append(xs[idx_t] * q)
        if terms:
            m.Add(sum(terms) <= rem_cap)

    # Precedence constraints involving F
    for j in range(n):
        for s in I["succ"][j]:
            if j in F and s in F:
                m.Add(S_var[s] >= E_var[j])
            elif j in P and s in F:
                m.Add(S_var[s] >= fixed_e[j])
            elif j in F and s in S:
                m.Add(E_var[j] <= fixed_s[s])
            elif j in F and s in P:
                # Impossible in valid schedule unless 0-dur, handle cleanly
                m.Add(E_var[j] <= fixed_s[s])
            elif j in S and s in F:
                m.Add(S_var[s] >= fixed_e[j])

    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(time_limit)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    new_modes = modes.copy()
    new_starts = np.zeros(n, dtype=np.int64)
    for j in P:
        new_starts[j] = fixed_s[j]
    for j in S:
        new_starts[j] = fixed_s[j]
    for j in F:
        new_starts[j] = sv.Value(S_var[j])
        for t, x in enumerate(X_var[j]):
            if sv.Value(x) == 1:
                new_modes[j] = t + 1
                break
    for j in donors:
        if j in X_var and j not in F:
            safe_modes, xs = X_var[j]
            for idx_t, t in enumerate(safe_modes):
                if sv.Value(xs[idx_t]) == 1:
                    new_modes[j] = t + 1
                    break

    return new_mk, new_modes, new_starts, sv.StatusName(st)


def slide_compress(
    I: dict,
    X,
    init_modes: np.ndarray,
    init_starts: np.ndarray,
    time_budget: float = 30.0,
    workers: int = 1,
    seed: int = 1,
):
    """Slide exact compression windows across [0, MK] with multiple window widths."""
    t_start = time.time()
    rng = np.random.default_rng(seed)
    cur_m = np.asarray(init_modes, dtype=np.int64).copy()
    cur_s = np.asarray(init_starts, dtype=np.int64).copy()
    cur_mk = int(cur_s[-1])
    topo = np.array(engine.topo(X), dtype=np.int64)

    n_real = X.n - 2
    # All jobs as potential safe NR donors
    all_donors = set(range(1, X.n - 1))

    # Try window widths targeting 18..40 jobs
    widths_frac = [0.25, 0.35, 0.45, 0.60]
    wins = 0
    tries = 0
    log = []

    while time.time() - t_start < time_budget:
        improved_round = False
        for wf in widths_frac:
            if time.time() - t_start >= time_budget:
                break
            W = max(6, int(cur_mk * wf))
            step = max(4, W // 2)
            # Generate window starts covering [0, cur_mk]
            starts_w = list(range(0, max(1, cur_mk - W + 1), step))
            if cur_mk - W > 0 and (not starts_w or starts_w[-1] < cur_mk - W):
                starts_w.append(cur_mk - W)
            rng.shuffle(starts_w)

            for t0 in starts_w:
                rem = time_budget - (time.time() - t_start)
                if rem < 0.8:
                    break
                t1 = min(cur_mk, t0 + W)
                sub_tl = min(rem, 3.5 if n_real <= 55 else 4.5)
                tries += 1
                res = compress_window(
                    I, cur_m, cur_s, t0, t1, delta=1, nr_donors=all_donors,
                    time_limit=sub_tl, workers=workers, seed=seed + tries * 31
                )
                if res is not None:
                    new_mk, new_m, new_s, status = res
                    # Double check with FBI to see if it compresses even further!
                    o_new = fast_meta.order_from_starts(new_s, topo)
                    mk_fbi, st_fbi = fast_meta.eval_modes_order(
                        o_new, new_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20
                    )
                    if mk_fbi < new_mk:
                        new_mk, new_s = int(mk_fbi), st_fbi
                    cur_mk, cur_m, cur_s = new_mk, new_m, new_s
                    wins += 1
                    improved_round = True
                    log.append((round(time.time() - t_start, 1), t0, t1, cur_mk, status))
                    break
            if improved_round:
                break
        if not improved_round:
            # Try one wider random window pass with larger time limit
            rem = time_budget - (time.time() - t_start)
            if rem < 2.0:
                break
            t0 = int(rng.integers(0, max(1, cur_mk // 3)))
            t1 = min(cur_mk, t0 + int(cur_mk * 0.7))
            tries += 1
            res = compress_window(
                I, cur_m, cur_s, t0, t1, delta=1, nr_donors=all_donors,
                time_limit=min(rem, 6.0), workers=workers, seed=seed + tries * 37
            )
            if res is not None:
                cur_mk, cur_m, cur_s, status = res
                wins += 1
                log.append((round(time.time() - t_start, 1), t0, t1, cur_mk, status))
            else:
                break

    return cur_mk, cur_m, cur_s, {
        "tries": tries,
        "wins": wins,
        "secs": round(time.time() - t_start, 2),
        "log": log,
    }
