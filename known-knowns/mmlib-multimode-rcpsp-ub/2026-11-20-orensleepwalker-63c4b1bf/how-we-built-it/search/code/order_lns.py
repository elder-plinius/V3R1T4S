"""
Order-Preserving CP-SAT LNS (order_lns.py) — inspired by Laborie & Godard (2007) CP Optimizer LNS.

Instead of pinning unselected jobs to rigid timestamps (which traps tight 90%-utilization schedules
in a vise), we:
  - Freeze the MODES of unselected jobs (mandatory intervals, zero optional branching).
  - Keep ALL start times S[j] FREE to ripple left across [0, MK - 1].
  - Add an Order-Preserving Backbone on unselected jobs:
      * S[u_i] <= S[u_{i+1}] along their sorted incumbent start-time order, AND
      * Optionally a subset of non-overlapping precedence links E[u] <= S[v] (when old_end[u] <= old_start[v])
        to keep the search tree compact while allowing smooth global compression!
  - Unfreeze BOTH modes AND relative order for F (14..24 jobs: critical window + NR donors, or random subset).
"""
import json
import os
import resource
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

PHASEB_DIR = os.path.dirname(os.path.abspath(__file__))
if PHASEB_DIR not in sys.path:
    sys.path.insert(0, PHASEB_DIR)

import numpy as np  # noqa: E402
from ortools.sat.python import cp_model  # noqa: E402
import data  # noqa: E402
import engine  # noqa: E402
import fast_meta  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def solve_order_lns_step(
    I: dict,
    modes: np.ndarray,
    starts: np.ndarray,
    F_free: set,
    target_H: int,
    add_disj_prob: float = 0.0,
    diversify: bool = False,
    time_limit: float = 6.0,
    workers: int = 2,
    seed: int = 1,
):
    n = I["n"]
    rng = np.random.default_rng(seed)
    durs_old = [I["modes"][j][int(modes[j]) - 1][0] for j in range(n)]
    ends_old = [int(starts[j]) + durs_old[j] for j in range(n)]

    m = cp_model.CpModel()
    S = [None] * n
    E = [None] * n
    X_var = {}
    ivs = [[] for _ in I["Rcap"]]
    nr_fixed = [0] * len(I["Ncap"])

    for j in range(n):
        if j == 0:
            S[j] = m.NewConstant(0)
            E[j] = m.NewConstant(0)
            continue
        if j == n - 1:
            S[j] = m.NewIntVar(0, target_H, "mk")
            E[j] = S[j]
            continue

        if j in F_free:
            min_d = min(row[0] for row in I["modes"][j])
            if target_H - min_d < 0:
                return None, "BAD_H"
            S[j] = m.NewIntVar(0, target_H - min_d, f"S_{j}")
            E[j] = m.NewIntVar(min_d, target_H, f"E_{j}")
            xs = [m.NewBoolVar(f"x_{j}_{t}") for t in range(len(I["modes"][j]))]
            X_var[j] = xs
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
            if target_H - d < 0:
                return None, "BAD_H"
            S[j] = m.NewIntVar(0, target_H - d, f"S_{j}")
            E[j] = m.NewIntVar(d, target_H, f"E_{j}")
            iv = m.NewIntervalVar(S[j], d, E[j], f"iv_{j}")
            for k, q in enumerate(r):
                if q:
                    ivs[k].append((iv, q))

    # Renewable cumulative
    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)

    # Non-renewable knapsack over F_free
    for k, c in enumerate(I["Ncap"]):
        rem_cap = c - nr_fixed[k]
        if rem_cap < 0:
            return None, "NR_NEG"
        terms = [x * I["modes"][j][t][2][k] for j, xs in X_var.items() for t, x in enumerate(xs) if I["modes"][j][t][2][k]]
        if terms:
            m.Add(sum(terms) <= rem_cap)

    # Original precedences
    for j in range(n):
        for s in I["succ"][j]:
            m.Add(S[s] >= E[j])

    # Order-Preserving Backbone on unselected jobs (not in F_free)
    fixed_jobs = [j for j in range(1, n - 1) if j not in F_free]
    fixed_jobs.sort(key=lambda j: (int(starts[j]), ends_old[j], j))
    for i in range(len(fixed_jobs) - 1):
        u = fixed_jobs[i]
        v = fixed_jobs[i + 1]
        m.Add(S[u] <= S[v])

    if add_disj_prob > 0.0:
        for i in range(len(fixed_jobs)):
            u = fixed_jobs[i]
            eu = ends_old[u]
            added = 0
            for idx2 in range(i + 1, min(len(fixed_jobs), i + 12)):
                v = fixed_jobs[idx2]
                if int(starts[v]) >= eu:
                    if rng.random() < add_disj_prob:
                        m.Add(E[u] <= S[v])
                    added += 1
                    if added >= 2:
                        break

    # Hints
    for j in range(1, n - 1):
        m.AddHint(S[j], min(int(starts[j]), target_H))
        if j in X_var:
            mj = int(modes[j]) - 1
            for t, x in enumerate(X_var[j]):
                m.AddHint(x, 1 if t == mj else 0)

    if diversify:
        # Lexicographic: primary S[n-1], secondary move away from current modes
        pen = [X_var[j][int(modes[j]) - 1] for j in X_var]
        m.Minimize(S[n - 1] * 1000 + sum(pen))
    else:
        m.Minimize(S[n - 1])

    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(time_limit)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, sv.StatusName(st)

    new_modes = modes.copy()
    for j, xs in X_var.items():
        for t, x in enumerate(xs):
            if sv.Value(x) == 1:
                new_modes[j] = t + 1
                break
    new_starts = np.array([sv.Value(S[j]) for j in range(n)], dtype=np.int64)
    return (int(new_starts[-1]), new_modes, new_starts), sv.StatusName(st)


def run_order_lns(args):
    inst_id, budget_sec, workers_per_inst, seed = args
    _set_mem_limit(4)
    t0_wall = time.time()
    ds = data.MMLibDataset()
    info = ds.meta(inst_id)
    I, X = ds.load_inst(inst_id)
    bks = ds.load_bks_schedule(inst_id)
    if not bks:
        return None
    cur_m, cur_s = bks[0].copy(), bks[1].copy()
    cur_mk = int(cur_s[-1])
    orig_ub = info["ub"]
    best_m, best_s, best_mk = cur_m.copy(), cur_s.copy(), cur_mk
    rng = np.random.default_rng(seed)
    real_jobs = np.arange(1, X.n - 1)
    n_real = len(real_jobs)

    # Self-adaptive neighborhood size k_free!
    k_free = min(n_real, 22 if info["act"] <= 55 else 24)
    k_max_seen = k_free
    tries = 0
    wins = 0
    statuses = {}

    while time.time() - t0_wall < budget_sec:
        rem = budget_sec - (time.time() - t0_wall)
        if rem < 1.8:
            break

        # Every 5th step, do a fast plateau diversification step (target_H = cur_mk)
        is_div = (tries > 0 and tries % 5 == 0)
        k_use = min(n_real, max(10, k_free // 2)) if is_div else min(n_real, k_free)

        # Neighborhood selection: window+NR, critical+NR, or random
        mode_pick = tries % 3
        if k_use >= n_real:
            F_free = set(int(j) for j in real_jobs)
        elif mode_pick == 0:
            t_c = int(rng.integers(0, max(1, cur_mk)))
            dists = np.abs(cur_s[real_jobs] - t_c) + rng.uniform(0, 2.0, size=n_real)
            F_free = set(int(j) for j in real_jobs[np.argsort(dists)[: k_use // 2]])
            others = [int(j) for j in real_jobs if j not in F_free]
            if others and len(F_free) < k_use:
                weights = np.array([sum(X.nreq[j, cur_m[j] - 1]) + 1.0 for j in others], dtype=np.float64)
                extra = rng.choice(others, size=min(k_use - len(F_free), len(others)), replace=False, p=weights / weights.sum())
                F_free.update(int(j) for j in extra)
        elif mode_pick == 1:
            crit = fast_meta.compute_critical_mask(cur_s, cur_m, X.dur, X.pp, X.pi, X.sp, X.si)
            cjobs = [int(j) for j in real_jobs if crit[j] == 1]
            rng.shuffle(cjobs)
            F_free = set(cjobs[: k_use // 2])
            others = [int(j) for j in real_jobs if j not in F_free]
            if others and len(F_free) < k_use:
                weights = np.array([sum(X.nreq[j, cur_m[j] - 1]) + 1.0 for j in others], dtype=np.float64)
                extra = rng.choice(others, size=min(k_use - len(F_free), len(others)), replace=False, p=weights / weights.sum())
                F_free.update(int(j) for j in extra)
        else:
            F_free = set(int(j) for j in rng.choice(real_jobs, size=k_use, replace=False))

        sub_tl = min(rem, 2.5 if is_div else (5.0 if info["act"] <= 55 else 6.0))
        t_step = time.time()
        tries += 1
        res, st = solve_order_lns_step(
            I, cur_m, cur_s, F_free,
            target_H=(cur_mk if is_div else cur_mk - 1),
            add_disj_prob=0.0,
            diversify=is_div,
            time_limit=sub_tl, workers=workers_per_inst, seed=seed + tries * 61
        )
        dt_step = time.time() - t_step
        statuses[st] = statuses.get(st, 0) + 1

        if res is not None:
            new_mk, new_m, new_s = res
            cur_mk, cur_m, cur_s = new_mk, new_m, new_s
            if new_mk < best_mk:
                best_mk, best_m, best_s = new_mk, new_m.copy(), new_s.copy()
                wins += 1
        elif not is_div:
            # Self-adapt k_free to the exact tractability frontier!
            if st == "INFEASIBLE":
                if dt_step < 1.5:
                    k_free = min(n_real, int(k_free * 1.35) + 5)
                else:
                    k_free = min(n_real, k_free + 4)
                if k_free > k_max_seen:
                    k_max_seen = k_free
            elif st == "UNKNOWN":
                k_free = max(12, int(k_free * 0.85))

    dt = round(time.time() - t0_wall, 2)
    win_ok = False
    win_msg = ""
    if best_mk < orig_ub:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, best_m, best_s, True, seed, "adaptive_order_lns", dt
        )
        if chk_mk is not None:
            best_mk = chk_mk

    return {
        "id": inst_id,
        "file": info["file"],
        "ub_ref": info["ub_ref"],
        "act": info["act"],
        "modes": info["modes"],
        "lb": info["lb"],
        "ub": orig_ub,
        "best_mk": best_mk,
        "gain": orig_ub - best_mk,
        "win": win_ok,
        "win_msg": win_msg,
        "k_end": f"{k_free}/{k_max_seen}",
        "tries": tries,
        "wins": wins,
        "statuses": statuses,
        "secs": dt,
    }


def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else "ref5_60"
    budget_sec = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
    n_procs = min(4, int(sys.argv[3]) if len(sys.argv) > 3 else 2)
    workers_per_proc = max(1, 4 // n_procs)

    ds = data.MMLibDataset()
    if batch == "ref5_60":
        # Top 60 ref=5 (2023) open instances with A=100, prioritizing M=9 & M=6 & moderate-to-large gaps!
        cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == "5" and ds.meta(i)["act"] == 100]
        cands.sort(key=lambda x: (-x["modes"], -(x["ub"] - x["lb"]), x["id"]))
        picks = [c["id"] for c in cands[:60]]
    elif batch == "ref7_60":
        cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == "7" and ds.meta(i)["act"] == 100]
        cands.sort(key=lambda x: (-x["modes"], -(x["ub"] - x["lb"]), x["id"]))
        picks = [c["id"] for c in cands[:60]]
    elif batch == "ref1_all":
        cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == "1"]
        cands.sort(key=lambda x: (-x["act"], -(x["ub"] - x["lb"]), x["id"]))
        picks = [c["id"] for c in cands]
    else:
        picks = [int(x) for x in batch.split(",")]

    print(f"adaptive_order_lns ({batch}): {len(picks)} inst, budget={budget_sec}s, procs={n_procs}x{workers_per_proc}w", flush=True)
    tasks = [(iid, budget_sec, workers_per_proc, 85000 + idx) for idx, iid in enumerate(picks)]
    t0 = time.time()
    wins = []
    results = []
    with ProcessPoolExecutor(max_workers=n_procs) as ex:
        futs = {ex.submit(run_order_lns, t): t[0] for t in tasks}
        for fut in as_completed(futs):
            r = fut.result()
            if not r:
                continue
            results.append(r)
            tag = "WIN!!!" if r["win"] else "      "
            if r["win"]:
                wins.append(r)
            print(
                f"{tag} id={r['id']:4d} {r['file']:<14s} ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} "
                f"LB={r['lb']:3d} UB={r['ub']:3d} -> mk={r['best_mk']:3d} (gain={r['gain']:+3d}) "
                f"{r['secs']:5.1f}s k={r['k_end']:<6s} tries={r['tries']:2d} st={r['statuses']} {r['win_msg']}",
                flush=True,
            )

    print(f"\n=== ADAPTIVE ORDER LNS SUMMARY ({time.time() - t0:.1f}s wall) ===", flush=True)
    print(f"Total: {len(results)} | Wins: {len(wins)} | Total gain: {sum(r['gain'] for r in wins)}", flush=True)
    out_path = os.path.join(PHASEB_DIR, "logs", f"adaptive_order_lns_{batch}.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
