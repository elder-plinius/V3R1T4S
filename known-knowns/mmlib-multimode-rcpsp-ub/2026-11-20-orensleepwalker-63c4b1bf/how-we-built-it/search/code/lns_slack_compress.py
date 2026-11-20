"""
Two-Phase Plateau-Harvest + Cut-Compression CP-SAT LNS (lns_slack_compress.py).

Key insight: On hard MMLIB+ BKS schedules, non-renewable slack NR_rem is often [0, 0, ...],
so direct delta=1 window compression is starved of NR budget, while joint 45-job trade windows
time out in CP-SAT.

Solution: Keep |F| STRICTLY SMALL (14..22 jobs, all other n-|F| jobs are NewFixedSizeIntervalVar
constants!) and alternate three fast (1.5-3.5s) exact CP-SAT moves:
  1. NR_HARVEST (MK <= cur_mk): Minimize weighted NR usage of F (weighted by tightness 1/(1+NR_rem[k])),
     harvesting +5..+40 units of NR slack without worsening makespan!
  2. WORK_SHIFT (MK <= cur_mk): Minimize sum(E[j]) + renewable work of F, pulling jobs left and
     diversifying modes on the plateau.
  3. CUT_COMPRESS (MK <= cur_mk - 1): Pick a single cut time t_cut (all jobs finish<=t_cut fixed at s,
     all jobs start>=t_cut+1 fixed at s-1, ONLY the ~14..20 jobs straddling t_cut + neighbors in F)
     and spend the harvested NR slack to compress by delta=1!
  4. Also check FBI after every plateau move (sometimes a plateau mode change + FBI immediately drops MK!).
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


def build_preds(I):
    n = I["n"]
    preds = [[] for _ in range(n)]
    for u in range(n):
        for v in I["succ"][u]:
            preds[v].append(u)
    return preds


def plateau_move_cpsat(
    I: dict,
    preds,
    modes: np.ndarray,
    starts: np.ndarray,
    F: set,
    objective_kind: str,
    nr_rem: np.ndarray,
    time_limit: float = 2.5,
    workers: int = 1,
    seed: int = 1,
):
    """
    Fix all jobs outside F as NewFixedSizeIntervalVar at their exact starts[j].
    Free both modes and starts of F (bounded by fixed preds/succs), keeping MK <= cur_mk.
    Optimize `objective_kind` ('nr_harvest', 'earliness', 'diversify').
    """
    n = I["n"]
    mk = int(starts[n - 1])
    durs = [I["modes"][j][int(modes[j]) - 1][0] for j in range(n)]
    ends = [int(starts[j]) + durs[j] for j in range(n)]

    m = cp_model.CpModel()
    S_var = {}
    E_var = {}
    X_var = {}
    ivs = [[] for _ in I["Rcap"]]
    nr_fixed = [0] * len(I["Ncap"])

    for j in F:
        min_d = min(row[0] for row in I["modes"][j])
        max_d = max(row[0] for row in I["modes"][j])
        lo = 0
        hi = mk - min_d
        for p in preds[j]:
            if p not in F:
                lo = max(lo, ends[p])
        for s in I["succ"][j]:
            if s not in F:
                hi = min(hi, int(starts[s]) - min_d)
        if lo > hi:
            return None
        S_var[j] = m.NewIntVar(lo, hi, f"S_{j}")
        E_var[j] = m.NewIntVar(lo + min_d, min(mk, hi + max_d), f"E_{j}")
        xs = [m.NewBoolVar(f"x_{j}_{t}") for t in range(len(I["modes"][j]))]
        X_var[j] = xs
        m.AddExactlyOne(xs)
        for t, (x, (d, r, _)) in enumerate(zip(xs, I["modes"][j])):
            iv = m.NewOptionalIntervalVar(S_var[j], d, E_var[j], x, f"iv_{j}_{t}")
            for k, q in enumerate(r):
                if q:
                    ivs[k].append((iv, q))

    for j in range(1, n - 1):
        if j in F:
            continue
        mj = int(modes[j]) - 1
        d_old, r_old, nr_old = I["modes"][j][mj]
        for k, q in enumerate(nr_old):
            nr_fixed[k] += q
        if d_old > 0:
            iv = m.NewFixedSizeIntervalVar(int(starts[j]), d_old, f"fix_{j}")
            for k, q in enumerate(r_old):
                if q:
                    ivs[k].append((iv, q))

    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)

    for k, c in enumerate(I["Ncap"]):
        rem_cap = c - nr_fixed[k]
        if rem_cap < 0:
            return None
        terms = [x * I["modes"][j][t][2][k] for j, xs in X_var.items() for t, x in enumerate(xs) if I["modes"][j][t][2][k]]
        if terms:
            m.Add(sum(terms) <= rem_cap)

    for j in F:
        for s in I["succ"][j]:
            if s in F:
                m.Add(S_var[s] >= E_var[j])
            else:
                m.Add(E_var[j] <= int(starts[s]))
        for p in preds[j]:
            if p not in F:
                m.Add(S_var[j] >= ends[p])

    # Warm-start hint = current feasible schedule!
    for j in F:
        m.AddHint(S_var[j], int(starts[j]))
        mj = int(modes[j]) - 1
        for t, x in enumerate(X_var[j]):
            m.AddHint(x, 1 if t == mj else 0)

    # Objective
    if objective_kind == "nr_harvest" and len(I["Ncap"]) > 0:
        # Weight each NR resource inversely by its current slack
        w = [max(1, int(100 / (1 + max(0, int(nr_rem[k]))))) for k in range(len(I["Ncap"]))]
        obj_terms = []
        for j, xs in X_var.items():
            for t, x in enumerate(xs):
                cost = sum(w[k] * I["modes"][j][t][2][k] for k in range(len(I["Ncap"])))
                if cost:
                    obj_terms.append(x * cost)
        if obj_terms:
            m.Minimize(sum(obj_terms))
    elif objective_kind == "earliness":
        # Pull jobs left + slightly prefer lower renewable work
        obj_terms = [E_var[j] * 10 for j in F]
        for j, xs in X_var.items():
            for t, x in enumerate(xs):
                d, r, _ = I["modes"][j][t]
                rw = sum(d * q for q in r)
                if rw:
                    obj_terms.append(x * (rw // 5))
        m.Minimize(sum(obj_terms))
    else:  # diversify: maximize Hamming distance from current modes while keeping NR low
        obj_terms = []
        for j, xs in X_var.items():
            mj = int(modes[j]) - 1
            obj_terms.append(xs[mj] * 50)
            for t, x in enumerate(xs):
                nr_sum = sum(I["modes"][j][t][2])
                if nr_sum:
                    obj_terms.append(x * nr_sum)
        m.Minimize(sum(obj_terms))

    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(time_limit)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    new_modes = modes.copy()
    new_starts = starts.copy()
    for j in F:
        new_starts[j] = sv.Value(S_var[j])
        for t, x in enumerate(X_var[j]):
            if sv.Value(x) == 1:
                new_modes[j] = t + 1
                break
    return new_modes, new_starts, sv.StatusName(st)


def cut_compress_cpsat(
    I: dict,
    preds,
    modes: np.ndarray,
    starts: np.ndarray,
    t_cut: int,
    max_f_size: int = 20,
    delta: int = 1,
    time_limit: float = 3.0,
    workers: int = 1,
    seed: int = 1,
):
    """
    Exact single-cut compression at t_cut:
    - P: ends[j] <= t_cut -> fixed at starts[j]
    - S: starts[j] >= t_cut + delta -> fixed at starts[j] - delta
    - F: jobs straddling (t_cut, t_cut + delta) expanded to ~max_f_size with nearest boundary jobs!
    """
    n = I["n"]
    mk = int(starts[n - 1])
    new_mk = mk - delta
    if new_mk < 1 or t_cut < 1 or t_cut + delta >= mk:
        return None, "BAD_CUT"

    durs = [I["modes"][j][int(modes[j]) - 1][0] for j in range(n)]
    ends = [int(starts[j]) + durs[j] for j in range(n)]

    # Jobs strictly straddling [t_cut, t_cut + delta] MUST be in F
    F = set()
    for j in range(1, n - 1):
        if not (ends[j] <= t_cut or int(starts[j]) >= t_cut + delta):
            F.add(j)

    # Expand F with closest jobs to t_cut until |F| == max_f_size
    if len(F) < max_f_size:
        cands = []
        for j in range(1, n - 1):
            if j not in F:
                dist = min(abs(ends[j] - t_cut), abs(int(starts[j]) - (t_cut + delta)))
                cands.append((dist, j))
        cands.sort()
        for _, j in cands[: max_f_size - len(F)]:
            F.add(j)

    if len(F) > max_f_size + 12:
        return None, "TOO_BIG_F"

    P = {0}
    S = {n - 1}
    for j in range(1, n - 1):
        if j in F:
            continue
        if ends[j] <= t_cut:
            P.add(j)
        else:
            S.add(j)

    fixed_s = {}
    fixed_e = {}
    for j in P:
        fixed_s[j] = int(starts[j])
        fixed_e[j] = ends[j]
    for j in S:
        fixed_s[j] = int(starts[j]) - delta
        fixed_e[j] = ends[j] - delta

    # Verify P->S fixed precedences
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

    for j in F:
        min_d = min(row[0] for row in I["modes"][j])
        max_d = max(row[0] for row in I["modes"][j])
        lo = 0
        hi = new_mk - min_d
        for p in preds[j]:
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

    for j in range(1, n - 1):
        if j in F:
            continue
        mj = int(modes[j]) - 1
        d_old, r_old, nr_old = I["modes"][j][mj]
        for k, q in enumerate(nr_old):
            nr_fixed[k] += q
        if d_old > 0:
            iv = m.NewFixedSizeIntervalVar(fixed_s[j], d_old, f"fix_{j}")
            for k, q in enumerate(r_old):
                if q:
                    ivs[k].append((iv, q))

    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)

    for k, c in enumerate(I["Ncap"]):
        rem_cap = c - nr_fixed[k]
        if rem_cap < 0:
            return None, "NR_NEG"
        terms = [x * I["modes"][j][t][2][k] for j, xs in X_var.items() for t, x in enumerate(xs) if I["modes"][j][t][2][k]]
        if terms:
            m.Add(sum(terms) <= rem_cap)

    for j in F:
        for s in I["succ"][j]:
            if s in F:
                m.Add(S_var[s] >= E_var[j])
            elif s in fixed_s:
                m.Add(E_var[j] <= fixed_s[s])
        for p in preds[j]:
            if p in fixed_e:
                m.Add(S_var[j] >= fixed_e[p])

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


def run_slack_compress(args):
    inst_id, budget_sec, workers_per_inst, seed = args
    _set_mem_limit(4)
    t0_wall = time.time()
    ds = data.MMLibDataset()
    info = ds.meta(inst_id)
    I, X = ds.load_inst(inst_id)
    bks = ds.load_bks_schedule(inst_id)
    if not bks:
        return None
    preds = build_preds(I)
    topo = np.array(engine.topo(X), dtype=np.int64)

    cur_m, cur_s = bks[0].copy(), bks[1].copy()
    cur_mk = int(cur_s[-1])
    orig_ub = info["ub"]
    best_m, best_s, best_mk = cur_m.copy(), cur_s.copy(), cur_mk

    _, init_rem = fast_meta.check_nr_feasible(cur_m, X.nreq, X.ncap)
    max_rem_sum = int(init_rem.sum()) if len(init_rem) else 0
    init_rem_sum = max_rem_sum

    rng = np.random.default_rng(seed)
    real_jobs = np.arange(1, X.n - 1)
    n_modes = info["modes"]
    f_size = 22 if n_modes <= 3 else (18 if n_modes <= 6 else 15)

    step = 0
    cuts_tried = 0
    cuts_won = 0
    fbi_won = 0

    while time.time() - t0_wall < budget_sec:
        rem_t = budget_sec - (time.time() - t0_wall)
        if rem_t < 1.5:
            break
        step += 1

        # 1. Harvest NR slack or shift jobs left on the plateau (2/3 of steps)
        _, nr_rem = fast_meta.check_nr_feasible(cur_m, X.nreq, X.ncap)
        if step % 3 != 0:
            obj_kind = "nr_harvest" if (step % 3 == 1 and len(nr_rem) > 0) else ("earliness" if step % 6 == 2 else "diversify")
            # Pick f_size jobs: either time-local cluster or random
            if rng.random() < 0.6:
                t_c = int(rng.integers(0, max(1, cur_mk)))
                dists = np.abs(cur_s[real_jobs] - t_c) + rng.uniform(0, 2.0, size=len(real_jobs))
                F = set(int(j) for j in real_jobs[np.argsort(dists)[:f_size]])
            else:
                F = set(int(j) for j in rng.choice(real_jobs, size=min(f_size, len(real_jobs)), replace=False))
            res = plateau_move_cpsat(
                I, preds, cur_m, cur_s, F, obj_kind, nr_rem,
                time_limit=min(rem_t, 2.5), workers=workers_per_inst, seed=seed + step * 53
            )
            if res is not None:
                new_m, new_s, _ = res
                cur_m, cur_s = new_m, new_s
                _, nr_rem2 = fast_meta.check_nr_feasible(cur_m, X.nreq, X.ncap)
                if len(nr_rem2) and int(nr_rem2.sum()) > max_rem_sum:
                    max_rem_sum = int(nr_rem2.sum())
                # Immediately test FBI on the new schedule!
                o_new = fast_meta.order_from_starts(cur_s, topo)
                mk_fbi, st_fbi = fast_meta.eval_modes_order(
                    o_new, cur_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20
                )
                if mk_fbi < cur_mk:
                    cur_mk, cur_s = int(mk_fbi), st_fbi
                    fbi_won += 1
                    if cur_mk < best_mk:
                        best_mk, best_m, best_s = cur_mk, cur_m.copy(), cur_s.copy()
        else:
            # 2. Try single-cut compression at 2 random cuts using the harvested NR slack!
            for ci in range(2):
                rem_t = budget_sec - (time.time() - t0_wall)
                if rem_t < 1.5:
                    break
                t_cut = int(rng.integers(max(1, cur_mk // 6), max(2, cur_mk - cur_mk // 6)))
                cuts_tried += 1
                res, st = cut_compress_cpsat(
                    I, preds, cur_m, cur_s, t_cut, max_f_size=f_size + 2, delta=1,
                    time_limit=min(rem_t, 3.0), workers=workers_per_inst, seed=seed + step * 71 + ci
                )
                if res is not None:
                    new_mk, new_m, new_s = res
                    cur_mk, cur_m, cur_s = new_mk, new_m, new_s
                    cuts_won += 1
                    # Also run FBI
                    o_new = fast_meta.order_from_starts(cur_s, topo)
                    mk_fbi, st_fbi = fast_meta.eval_modes_order(
                        o_new, cur_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20
                    )
                    if mk_fbi < cur_mk:
                        cur_mk, cur_s = int(mk_fbi), st_fbi
                    if cur_mk < best_mk:
                        best_mk, best_m, best_s = cur_mk, cur_m.copy(), cur_s.copy()
                    break

    dt = round(time.time() - t0_wall, 2)
    win_ok = False
    win_msg = ""
    if best_mk < orig_ub:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, best_m, best_s, True, seed, "lns_slack_compress", dt
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
        "nr_slack": f"{init_rem_sum}->{max_rem_sum}",
        "steps": step,
        "cuts": f"{cuts_tried}/{cuts_won}",
        "fbi_won": fbi_won,
        "secs": dt,
    }


def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else "test12"
    budget_sec = float(sys.argv[2]) if len(sys.argv) > 2 else 35.0
    n_procs = min(4, int(sys.argv[3]) if len(sys.argv) > 3 else 2)
    workers_per_proc = max(1, 4 // n_procs)

    ds = data.MMLibDataset()
    if batch == "test12":
        picks = [766, 498, 1446, 1451, 3208, 3207, 2524, 2935, 3201, 3068, 3203, 2668]
    elif batch == "ref5_100":
        cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == "5" and ds.meta(i)["act"] == 100]
        cands.sort(key=lambda x: -(x["ub"] - x["lb"]) / x["lb"])
        picks = [c["id"] for c in cands[:40]]
    elif batch == "ref7_100":
        cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == "7" and ds.meta(i)["act"] == 100]
        cands.sort(key=lambda x: -(x["ub"] - x["lb"]) / x["lb"])
        picks = [c["id"] for c in cands[:40]]
    else:
        picks = [int(x) for x in batch.split(",")]

    print(f"lns_slack_compress ({batch}): {len(picks)} inst, budget={budget_sec}s, procs={n_procs}x{workers_per_proc}w", flush=True)
    tasks = [(iid, budget_sec, workers_per_proc, 70000 + idx) for idx, iid in enumerate(picks)]
    t0 = time.time()
    wins = []
    results = []
    with ProcessPoolExecutor(max_workers=n_procs) as ex:
        futs = {ex.submit(run_slack_compress, t): t[0] for t in tasks}
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
                f"{r['secs']:5.1f}s nr_slack={r['nr_slack']} steps={r['steps']:2d} cuts={r['cuts']} fbi={r['fbi_won']} {r['win_msg']}",
                flush=True,
            )

    print(f"\n=== SLACK COMPRESS SUMMARY ({time.time() - t0:.1f}s wall) ===", flush=True)
    print(f"Total: {len(results)} | Wins: {len(wins)} | Total gain: {sum(r['gain'] for r in wins)}", flush=True)
    out_path = os.path.join(PHASEB_DIR, "logs", f"slack_compress_{batch}.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
