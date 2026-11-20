"""
Two-Stage Campaign (pilot_4w_and_ref1.py):
  Stage 1 (~20 min): 4-worker CP-SAT portfolio pilot (16 instances x 75s, 1 process x 4 CP-SAT workers):
    - 8 timed-out P3_lowOS50 (A=50, M=9, ref=5/7) instances: fast mode discovery + 4-worker Fixed-Mode CP-SAT + 4-worker Free-24-Mode CP-SAT.
    - 8 UB-tying 5F_ref8_M3 (M=3, ref=8) instances: fast metaheuristic to reach MK=UB + 4-worker Global CP-SAT (S[n-1] <= UB-1, warm-hinted).
  Stage 2 (~27 min): Sweep ALL remaining 44 ref=1 (2011) open instances with exact proven overnight v3.2 settings
    (4 parallel workers x 1 CP-SAT worker each, 150s/inst, cpsat_mixes=5, 2 waves).
"""
import glob
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
import hybrid_v2  # noqa: E402
import hybrid_v31_warm  # noqa: E402
import overnight_v32  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def solve_global_or_subset_4w(I, modes, starts, H_target, free_jobs, secs, seed):
    """4-worker CP-SAT with full portfolio (LNS + LP + probing) for S[n-1] <= H_target."""
    n = I["n"]
    m = cp_model.CpModel()
    S = [None] * n
    E = [None] * n
    Xv = {}
    ivs = [[] for _ in I["Rcap"]]
    nr_fixed = [0] * len(I["Ncap"])

    for j in range(n):
        if j == 0:
            S[j] = m.NewConstant(0)
            E[j] = m.NewConstant(0)
            continue
        if j == n - 1:
            S[j] = m.NewIntVar(0, H_target, "mk")
            E[j] = S[j]
            continue
        if j in free_jobs:
            min_d = min(row[0] for row in I["modes"][j])
            if H_target - min_d < 0:
                return None, "BAD_H"
            S[j] = m.NewIntVar(0, H_target - min_d, f"S_{j}")
            E[j] = m.NewIntVar(min_d, H_target, f"E_{j}")
            xs = [m.NewBoolVar(f"x_{j}_{t}") for t in range(len(I["modes"][j]))]
            Xv[j] = xs
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
            if H_target - d < 0:
                return None, "BAD_H"
            S[j] = m.NewIntVar(0, H_target - d, f"S_{j}")
            E[j] = m.NewIntVar(d, H_target, f"E_{j}")
            iv = m.NewIntervalVar(S[j], d, E[j], f"iv_{j}")
            for k, q in enumerate(r):
                if q:
                    ivs[k].append((iv, q))

    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)
    for k, c in enumerate(I["Ncap"]):
        rem = c - nr_fixed[k]
        if rem < 0:
            return None, "NR_NEG"
        terms = [x * I["modes"][j][t][2][k] for j, xs in Xv.items() for t, x in enumerate(xs) if I["modes"][j][t][2][k]]
        if terms:
            m.Add(sum(terms) <= rem)
    for j in range(n):
        for s in I["succ"][j]:
            m.Add(S[s] >= E[j])

    if starts is not None and modes is not None:
        for j in range(1, n - 1):
            m.AddHint(S[j], min(int(starts[j]), H_target))
            if j in Xv:
                mj = int(modes[j]) - 1
                for t, x in enumerate(Xv[j]):
                    m.AddHint(x, 1 if t == mj else 0)

    m.Minimize(S[n - 1])
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = 4
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        new_m = modes.copy() if modes is not None else np.ones(n, dtype=np.int64)
        for j, xs in Xv.items():
            for t, x in enumerate(xs):
                if sv.Value(x) == 1:
                    new_m[j] = t + 1
                    break
        new_s = np.array([sv.Value(S[j]) for j in range(n)], dtype=np.int64)
        return (int(new_s[-1]), new_m, new_s), sv.StatusName(st)
    return None, sv.StatusName(st)


def run_pilot_one(ds: data.MMLibDataset, iid: int, tag: str, budget_sec: float, seed: int):
    t0 = time.time()
    info = ds.meta(iid)
    I, X = ds.load_inst(iid)
    bks = ds.load_bks_schedule(iid)
    warm = bks is not None
    ub = info["ub"]
    rng = np.random.default_rng(seed)
    topo = np.array(engine.topo(X), dtype=np.int64)

    best_mk = ub if warm else None
    best_m = bks[0].copy() if warm else None
    best_s = bks[1].copy() if warm else None
    meth = ""
    statuses = []

    if warm:
        # P3_lowOS50 (A=50, M=9):
        # 1) 25s fast Memetic (cpsat_mixes=5) -> collect top 3 genuinely new mode vectors
        mk_m, m_m, s_m, st_m = fast_meta.memetic_search(
            X, time_budget=25.0, seed=seed, init_solutions=[(best_m, best_s)],
            pop_size=24, cpsat_mixes=5, cpsat_workers=1
        )
        cands = {}
        for mk_p, m_p, s_p in st_m.get("top_pop", []):
            if int(np.sum(m_p != bks[0])) >= 2:
                key = bytes(m_p.astype(np.uint8).tobytes())
                if key not in cands or mk_p < cands[key][0]:
                    cands[key] = (mk_p, m_p, s_p)
        if mk_m is not None and mk_m < best_mk:
            best_mk, best_m, best_s = int(mk_m), m_m.copy(), s_m.copy()
            meth = "pilot4w_meta"

        # 2) 4-worker Fixed-Mode CP-SAT on top 2 new mode vectors (12s each)
        for idx, (mk_c, m_c, s_c) in enumerate(sorted(cands.values(), key=lambda x: x[0])[:2]):
            rem = budget_sec - (time.time() - t0)
            if rem < 10.0:
                break
            mk_cp, s_cp, st_name = hybrid_v2.solve_fixed_mode_cpsat(
                I, m_c, H=best_mk - 1, hint_starts=s_c, secs=min(12.0, rem * 0.4), workers=4, seed=seed + 100 + idx
            )
            statuses.append(f"fix:{st_name}")
            if mk_cp is not None and mk_cp < best_mk:
                best_mk, best_m, best_s = int(mk_cp), m_c.copy(), s_cp
                meth = "pilot4w_fixed_cpsat"

        # 3) Remaining (~25s): 4-worker Global/Free-26-Mode CP-SAT (S[n-1] <= best_mk - 1)
        rem = budget_sec - (time.time() - t0)
        if rem >= 5.0:
            real = np.arange(1, X.n - 1)
            k_free = min(len(real), 26)
            free_set = set(int(j) for j in rng.choice(real, size=k_free, replace=False))
            res, st_name = solve_global_or_subset_4w(I, best_m, best_s, best_mk - 1, free_set, rem, seed + 500)
            statuses.append(f"sub26:{st_name}")
            if res is not None and res[0] < best_mk:
                best_mk, best_m, best_s = res[0], res[1], res[2]
                meth = "pilot4w_sub26_cpsat"
    else:
        # 5F_ref8_M3 (M=3, from-scratch):
        # 1) 25s fast Memetic -> reach MK=UB warm hint
        mk_m, m_m, s_m, _ = fast_meta.memetic_search(
            X, time_budget=25.0, seed=seed, init_solutions=None,
            pop_size=24, cpsat_mixes=5, cpsat_workers=1
        )
        if mk_m is not None:
            best_mk, best_m, best_s = int(mk_m), m_m.copy(), s_m.copy()
            meth = "pilot4w_scratch_meta"

        # 2) Remaining (~50s): 4-worker GLOBAL CP-SAT over ALL M=3 modes + starts (S[n-1] <= ub - 1)!
        rem = budget_sec - (time.time() - t0)
        if rem >= 5.0:
            all_real = set(range(1, X.n - 1))
            res, st_name = solve_global_or_subset_4w(I, best_m, best_s, ub - 1, all_real, rem, seed + 700)
            statuses.append(f"glob:{st_name}")
            if res is not None and (best_mk is None or res[0] < best_mk):
                best_mk, best_m, best_s = res[0], res[1], res[2]
                meth = "pilot4w_global_cpsat"

    dt = round(time.time() - t0, 1)
    win_ok = False
    win_msg = ""
    if best_m is not None and best_s is not None and best_mk < ub:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, iid, I, best_m, best_s, warm_start=warm, seed=seed, method=meth or "pilot4w", runtime_sec=dt
        )
        if chk_mk is not None:
            best_mk = chk_mk

    return {
        "id": iid, "pool": tag, "file": info["file"], "ub_ref": info["ub_ref"],
        "act": info["act"], "modes": info["modes"], "rr": info["rr"],
        "lb": info["lb"], "ub": ub, "warm": warm, "best_mk": best_mk,
        "gain": (ub - best_mk) if best_mk is not None else None,
        "new_win": win_ok, "win_msg": win_msg, "method": meth,
        "statuses": statuses, "secs": dt,
    }


def main():
    _set_mem_limit(4)
    ds = data.MMLibDataset()
    wins_map = overnight_v32.load_best_wins_map()

    # Warmup Numba
    I0, X0 = ds.load_inst(1)
    m0, s0 = ds.load_bks_schedule(1)
    topo0 = np.array(engine.topo(X0), dtype=np.int64)
    o0 = fast_meta.order_from_starts(s0, topo0)
    fast_meta.eval_both_sgs(o0, m0, X0.dur, X0.req, X0.cap, X0.pp, X0.pi, X0.sp, X0.si, X0.H, 10)
    fast_meta.run_sa_penalty(X0, m0, s0, time_budget=0.1, seed=1)

    # ===== STAGE 1: 20-MINUTE 4-WORKER PILOT (16 instances x 75s) =====
    ov_rows = [json.loads(l) for l in open(os.path.join(PHASEB_DIR, "logs", "overnight_v32.jsonl"))]
    # 8 timed-out P3_lowOS50 (A=50, M=9, secs >= 120)
    p3_to = [r["id"] for r in ov_rows if r["pool"] == "P3_lowOS50" and r["modes"] == 9 and r["secs"] >= 120 and r["id"] not in wins_map]
    p3_picks = p3_to[:8]
    # 8 UB-tying 5F_ref8_M3 (prefer A=50 first since global CP-SAT on A=50 M=3 is super fast, plus A=100)
    f5_ties = [r["id"] for r in ov_rows if r["pool"] == "5F_ref8_M3_P2" and r["gain"] == 0 and r["id"] not in wins_map]
    f5_ties.sort(key=lambda i: (ds.meta(i)["act"], -(ds.meta(i)["ub"] - ds.meta(i)["lb"]), i))
    f5_picks = f5_ties[:8]

    pilot_queue = [(iid, "pilot4w_P3") for iid in p3_picks] + [(iid, "pilot4w_5F") for iid in f5_picks]
    print(f"=== STAGE 1: 4-WORKER CP-SAT PILOT ({len(pilot_queue)} inst x 75s = ~20m) ===", flush=True)
    t_s1 = time.time()
    s1_log = os.path.join(PHASEB_DIR, "logs", "pilot_4w_lbbd.jsonl")
    s1_wins = 0
    for idx, (iid, tag) in enumerate(pilot_queue):
        r = run_pilot_one(ds, iid, tag, 75.0, 300000 + idx)
        with open(s1_log, "a") as lf:
            lf.write(json.dumps(r) + "\n")
        if r["new_win"]:
            s1_wins += 1
            wins_map[iid] = (r["best_mk"], r["win_msg"])
            mark = "WIN!!!"
        else:
            mark = "      "
        print(
            f"{mark} [{(time.time()-t_s1)/60:4.1f}m] ({idx+1:2d}/{len(pilot_queue)}) {tag:<11s} id={r['id']:4d} {r['file']:<14s} "
            f"ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} LB={r['lb']:2d} UB={r['ub']:2d} -> mk={str(r['best_mk']):>3s} "
            f"(gain={str(r['gain']):>3s}) {r['secs']:4.1f}s st={r['statuses']} {r['method']}",
            flush=True,
        )
    print(f"=== STAGE 1 COMPLETE ({(time.time()-t_s1)/60:.1f}m wall) | Pilot wins: {s1_wins}/{len(pilot_queue)} ===\n", flush=True)

    # ===== STAGE 2: SWEEP ALL REMAINING 44 ref=1 (2011) INSTANCES WITH PROVEN OVERNIGHT V3.2 SETTINGS =====
    ref1_done = {r["id"] for r in ov_rows if r["pool"] == "5G_ref1_2011"}
    ref1_rem = [
        ds.meta(i) for i in ds.open_ids()
        if ds.rows[i].get("UB ref") == "1" and i not in wins_map and i not in ref1_done
    ]
    ref1_rem.sort(key=lambda c: (-c["act"], -c["modes"], -(c["ub"] - c["lb"]), c["id"]))
    print(f"=== STAGE 2: REMAINING ref=1 (2011) SWEEP ({len(ref1_rem)} inst x 150s, 4 workers, v3.2 settings) ===", flush=True)

    t_s2 = time.time()
    s2_log = os.path.join(PHASEB_DIR, "logs", "sweep_ref1_rem_v32.jsonl")
    tasks = [(c["id"], "ref1_rem_v32", 150.0, 310000 + idx, None, None) for idx, c in enumerate(ref1_rem)]
    s2_wins = 0
    s2_done = 0
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(overnight_v32.solve_warm_custom, t): t[0] for t in tasks}
        for fut in as_completed(futs):
            r = fut.result()
            s2_done += 1
            with open(s2_log, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            if r["new_win"]:
                s2_wins += 1
                mark = "WIN!!!"
            else:
                mark = "      "
            print(
                f"{mark} [{(time.time()-t_s2)/60:4.1f}m] ({s2_done:2d}/{len(ref1_rem)}) id={r['id']:4d} {r['file']:<14s} "
                f"ref=1 A={r['act']:3d} M={r['modes']} RR={r['rr']} LB={r['lb']:3d} UB={r['ub']:3d} -> "
                f"mk={r['best_mk']:3d} (gain={r['gain']:+2d}) {r['secs']:5.1f}s cp={r['cp_tested']:2d}/{r['cp_improved']} {r['method']}",
                flush=True,
            )

    print(
        f"\n=== ALL DONE ({(time.time()-t_s1)/60:.1f}m total wall) ===\n"
        f"Stage 1 (4w pilot): {s1_wins}/{len(pilot_queue)} wins | Stage 2 (ref=1 rem): {s2_wins}/{len(ref1_rem)} wins",
        flush=True,
    )


if __name__ == "__main__":
    main()
