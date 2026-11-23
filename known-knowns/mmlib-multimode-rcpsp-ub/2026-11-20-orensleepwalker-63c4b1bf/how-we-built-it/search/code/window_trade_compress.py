"""
Exact Cross-Schedule NR-Trading Window Compression (window_trade_compress.py):
- Prefix P (finish <= t0): fixed at starts[j]
- Suffix S (start >= t1): fixed at starts[j] - delta (delta = 1)
- Free set F = F_win (jobs overlapping (t0, t1)) U F_don (8..14 high-NR / high-slack donor jobs from P & S!)
- ALL non-F jobs are NewFixedSizeIntervalVar (0 branching variables!) across the ENTIRE [0, MK-delta] horizon.
- ALL F jobs (22..35 jobs total) have FREE modes (all M modes!) AND FREE start times bounded by precedences!
- Result: F_win can directly trade non-renewable budget with F_don ANYWHERE in the project while keeping 70% of the schedule fixed as constants!
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


def compress_window_with_trade(
    I: dict,
    modes: np.ndarray,
    starts: np.ndarray,
    t0: int,
    t1: int,
    donor_jobs: set,
    delta: int = 1,
    time_limit: float = 4.0,
    workers: int = 1,
    seed: int = 1,
):
    n = I["n"]
    mk = int(starts[n - 1])
    new_mk = mk - delta
    if new_mk < 1 or t1 - delta < t0:
        return None, "BAD_WIN"

    durs = [I["modes"][j][int(modes[j]) - 1][0] for j in range(n)]
    ends = [int(starts[j]) + durs[j] for j in range(n)]

    P = set()
    S = set()
    F = set()
    for j in range(n):
        if j == 0:
            P.add(j)
        elif j == n - 1:
            S.add(j)
        elif j in donor_jobs:
            F.add(j)
        elif ends[j] <= t0:
            P.add(j)
        elif int(starts[j]) >= t1:
            S.add(j)
        else:
            F.add(j)

    if not F:
        return None, "EMPTY_F"

    fixed_s = {}
    fixed_e = {}
    for j in P:
        fixed_s[j] = int(starts[j])
        fixed_e[j] = ends[j]
    for j in S:
        fixed_s[j] = int(starts[j]) - delta
        fixed_e[j] = ends[j] - delta

    # Check fixed-to-fixed precedences (P->S is always valid if t0 <= t1 - delta)
    for j in P:
        for s in I["succ"][j]:
            if s in S and fixed_e[j] > fixed_s[s]:
                return None, "FIX_PREC"

    m = cp_model.CpModel()
    S_var = {}
    E_var = {}
    X_var = {}
    ivs = [[] for _ in I["Rcap"]]
    nr_fixed = [0] * len(I["Ncap"])

    # Precompute predecessor/successor fixed bounds for F jobs
    preds_of = [[] for _ in range(n)]
    for u in range(n):
        for v in I["succ"][u]:
            preds_of[v].append(u)

    for j in F:
        min_d = min(row[0] for row in I["modes"][j])
        max_d = max(row[0] for row in I["modes"][j])
        lo = 0
        hi = new_mk - min_d
        for p in preds_of[j]:
            if p in fixed_e:
                lo = max(lo, fixed_e[p])
        for s in I["succ"][j]:
            if s in fixed_s:
                hi = min(hi, fixed_s[s] - min_d)
        if lo > hi:
            return None, "BOUNDS_F"
        S_var[j] = m.NewIntVar(lo, hi, f"S_{j}")
        E_var[j] = m.NewIntVar(lo + min_d, min(new_mk, hi + max_d), f"E_{j}")
        xs = [m.NewBoolVar(f"x_{j}_{t}") for t in range(len(I["modes"][j]))]
        X_var[j] = xs
        m.AddExactlyOne(xs)
        for t, (x, (d, r, _)) in enumerate(zip(xs, I["modes"][j])):
            iv = m.NewOptionalIntervalVar(S_var[j], d, E_var[j], x, f"iv_{j}_{t}")
            for k, q in enumerate(r):
                if q:
                    ivs[k].append((iv, q))

    # Add ALL fixed jobs (P and S) as constant intervals
    for j in range(1, n - 1):
        if j in F:
            continue
        sj = fixed_s[j]
        mj = int(modes[j]) - 1
        d_old, r_old, nr_old = I["modes"][j][mj]
        for k, q in enumerate(nr_old):
            nr_fixed[k] += q
        if d_old > 0:
            iv = m.NewFixedSizeIntervalVar(sj, d_old, f"fix_{j}")
            for k, q in enumerate(r_old):
                if q:
                    ivs[k].append((iv, q))

    # Renewable cumulative
    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)

    # Non-renewable knapsack over F
    for k, c in enumerate(I["Ncap"]):
        rem_cap = c - nr_fixed[k]
        if rem_cap < 0:
            return None, "NR_NEG"
        terms = []
        for j, xs in X_var.items():
            for t, x in enumerate(xs):
                q = I["modes"][j][t][2][k]
                if q:
                    terms.append(x * q)
        if terms:
            m.Add(sum(terms) <= rem_cap)

    # Precedences involving F
    for j in F:
        for s in I["succ"][j]:
            if s in F:
                m.Add(S_var[s] >= E_var[j])
            elif s in fixed_s:
                m.Add(E_var[j] <= fixed_s[s])
        for p in preds_of[j]:
            if p in fixed_e:
                m.Add(S_var[j] >= fixed_e[p])

    # Warm-start hints for F
    for j in F:
        m.AddHint(S_var[j], min(int(starts[j]), new_mk))
        mj = int(modes[j]) - 1
        for t, x in enumerate(X_var[j]):
            m.AddHint(x, 1 if t == mj else 0)

    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(time_limit)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, sv.StatusName(st)

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
    return (new_mk, new_modes, new_starts), sv.StatusName(st)


def solve_trade_compress(args):
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
    rng = np.random.default_rng(seed)
    topo = np.array(engine.topo(X), dtype=np.int64)

    n_real = X.n - 2
    real_jobs = np.arange(1, X.n - 1)
    # Target F_win size ~ 12..18 jobs, plus 8..12 NR donors = 20..30 jobs total!
    tries = 0
    wins = 0
    statuses = {}

    while time.time() - t0_wall < budget_sec:
        rem = budget_sec - (time.time() - t0_wall)
        if rem < 1.5:
            break
        # Pick a cut window [t0, t1] whose width covers ~15-25% of cur_mk
        wf = float(rng.choice([0.12, 0.18, 0.25, 0.32]))
        W = max(4, int(cur_mk * wf))
        t0 = int(rng.integers(0, max(1, cur_mk - W + 1)))
        t1 = min(cur_mk, t0 + W)

        # Pick 8..12 NR-donor jobs outside [t0, t1], weighted by NR usage (and slack!)
        durs = np.array([X.dur[j, cur_m[j] - 1] for j in range(X.n)])
        outside = [int(j) for j in real_jobs if (cur_s[j] + durs[j] <= t0 or cur_s[j] >= t1)]
        n_don = min(len(outside), int(rng.integers(8, 14)))
        if n_don > 0:
            # Weight by current NR usage so they can give back NR budget!
            weights = np.array([sum(X.nreq[j, cur_m[j] - 1]) + 1.0 for j in outside], dtype=np.float64)
            probs = weights / weights.sum()
            donors = set(int(j) for j in rng.choice(outside, size=n_don, replace=False, p=probs))
        else:
            donors = set()

        sub_tl = min(rem, 4.5 if n_real <= 55 else 5.5)
        tries += 1
        res, st = compress_window_with_trade(
            I, cur_m, cur_s, t0, t1, donors, delta=1,
            time_limit=sub_tl, workers=workers_per_inst, seed=seed + tries * 41
        )
        statuses[st] = statuses.get(st, 0) + 1
        if res is not None:
            new_mk, new_m, new_s = res
            # Polish with FBI
            o_new = fast_meta.order_from_starts(new_s, topo)
            mk_fbi, st_fbi = fast_meta.eval_modes_order(
                o_new, new_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20
            )
            if mk_fbi < new_mk:
                new_mk, new_s = int(mk_fbi), st_fbi
            cur_mk, cur_m, cur_s = new_mk, new_m, new_s
            wins += 1

    dt = round(time.time() - t0_wall, 2)
    win_ok = False
    win_msg = ""
    if cur_mk < orig_ub:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, cur_m, cur_s, True, seed, "window_trade_compress", dt
        )
        if chk_mk is not None:
            cur_mk = chk_mk

    return {
        "id": inst_id,
        "file": info["file"],
        "ub_ref": info["ub_ref"],
        "act": info["act"],
        "modes": info["modes"],
        "lb": info["lb"],
        "ub": orig_ub,
        "best_mk": cur_mk,
        "gain": orig_ub - cur_mk,
        "win": win_ok,
        "win_msg": win_msg,
        "tries": tries,
        "wins": wins,
        "statuses": statuses,
        "secs": dt,
    }


def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else "top20"
    budget_sec = float(sys.argv[2]) if len(sys.argv) > 2 else 35.0
    n_procs = min(4, int(sys.argv[3]) if len(sys.argv) > 3 else 2)
    workers_per_proc = max(1, 4 // n_procs)

    ds = data.MMLibDataset()
    if batch == "top20":
        # 20 highest-gap warm-started instances across ref=1 (6), ref=5 (8), ref=7 (6), emphasizing A=100!
        picks = []
        for ref, act_pref, k in [("1", 100, 4), ("1", 50, 2), ("5", 100, 6), ("5", 50, 2), ("7", 100, 6)]:
            cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == ref and ds.meta(i)["act"] == act_pref]
            cands.sort(key=lambda x: -(x["ub"] - x["lb"]) / x["lb"])
            for c in cands[:k]:
                if c["id"] not in picks:
                    picks.append(c["id"])
    else:
        picks = [int(x) for x in batch.split(",")]

    print(f"window_trade_compress ({batch}): {len(picks)} inst, budget={budget_sec}s, procs={n_procs}x{workers_per_proc}w", flush=True)
    tasks = [(iid, budget_sec, workers_per_proc, 50000 + idx) for idx, iid in enumerate(picks)]
    t0 = time.time()
    wins = []
    results = []
    with ProcessPoolExecutor(max_workers=n_procs) as ex:
        futs = {ex.submit(solve_trade_compress, t): t[0] for t in tasks}
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
                f"{r['secs']:5.1f}s tries={r['tries']:2d} st={r['statuses']} {r['win_msg']}",
                flush=True,
            )

    print(f"\n=== TRADE COMPRESS SUMMARY ({time.time() - t0:.1f}s wall) ===", flush=True)
    print(f"Total: {len(results)} | Wins: {len(wins)} | Total gain: {sum(r['gain'] for r in wins)}", flush=True)
    out_path = os.path.join(PHASEB_DIR, "logs", f"trade_compress_{batch}.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
