"""
Phase B Hybrid v2 Solver:
1. For from-scratch (ref=8, no BKS):
   - Fast Numba Memetic GA + Strategic-Oscillation Penalty SA to discover top K distinct low-makespan mode vectors.
   - Exact Fixed-Mode CP-SAT on the top K distinct mode vectors (since SGS+FBI can be +3..+15 above exact optimum for a mode vector!).
   - Exact Frozen-Prefix + Shifted-Suffix CP-SAT Window Compression on the best schedule found.
2. For warm-started (ref=1, 5, 7):
   - First check Fixed-BKS CP-SAT (quick 2s).
   - Run Memetic GA + Penalty SA to discover NEW distinct mode vectors close to UB, and test top K distinct NEW mode vectors with Exact Fixed-Mode CP-SAT (`S[n-1] <= UB - 1`)!
   - Run Window Compression + Free-K-Mode CP-SAT LNS on the best schedule.
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
import window_compress  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def solve_fixed_mode_cpsat(I, modes, H, hint_starts=None, secs=4.0, workers=1, seed=1):
    n = I["n"]
    m = cp_model.CpModel()
    S = [None] * n
    E = [None] * n
    S[0] = m.NewConstant(0)
    E[0] = m.NewConstant(0)
    S[n - 1] = m.NewIntVar(0, H, "mk")
    E[n - 1] = S[n - 1]
    ivs = [[] for _ in I["Rcap"]]
    for j in range(1, n - 1):
        d, r, _ = I["modes"][j][int(modes[j]) - 1]
        if d > H:
            return None, None, "INFEAS_D"
        S[j] = m.NewIntVar(0, H - d, f"S_{j}")
        E[j] = m.NewIntVar(d, H, f"E_{j}")
        iv = m.NewIntervalVar(S[j], d, E[j], f"iv_{j}")
        for k, q in enumerate(r):
            if q:
                ivs[k].append((iv, q))
    for k, c in enumerate(I["Rcap"]):
        if ivs[k]:
            m.AddCumulative([a for a, _ in ivs[k]], [q for _, q in ivs[k]], c)
    for j in range(n):
        for s in I["succ"][j]:
            m.Add(S[s] >= E[j])
    if hint_starts is not None:
        for j in range(1, n - 1):
            m.AddHint(S[j], min(int(hint_starts[j]), H))
    m.Minimize(S[n - 1])
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        starts = np.array([sv.Value(S[j]) for j in range(n)], dtype=np.int64)
        return int(starts[-1]), starts, sv.StatusName(st)
    return None, None, sv.StatusName(st)


def collect_top_mode_vectors(X, time_budget, seed, init_solutions=None, top_k=5):
    """Run Memetic GA + Penalty SA and return top_k distinct feasible (mk, modes, starts)."""
    t0 = time.time()
    cands = {}  # bytes(modes) -> (mk, modes, starts)

    def rec(mk, modes, starts):
        if mk is None or modes is None or starts is None:
            return
        ok, _ = fast_meta.check_nr_feasible(modes, X.nreq, X.ncap)
        if not ok:
            return
        key = bytes(modes.astype(np.uint8).tobytes())
        if key not in cands or mk < cands[key][0]:
            cands[key] = (int(mk), modes.copy(), starts.copy())

    # 1. Memetic GA (60% of meta budget)
    mk_m, m_m, s_m, st_m = fast_meta.memetic_search(
        X, time_budget=time_budget * 0.6, seed=seed, init_solutions=init_solutions,
        pop_size=24, cpsat_mixes=4, cpsat_workers=1
    )
    rec(mk_m, m_m, s_m)

    # 2. Penalty SA starting from best (40% of meta budget)
    if m_m is not None:
        # Also run 2 independent short Penalty SA trajectories with different seeds to collect diverse mode vectors
        rem = max(2.0, time_budget - (time.time() - t0))
        for si in range(2):
            mk_s, m_s, s_s, _ = fast_meta.run_sa_penalty(
                X, m_m, s_m, time_budget=rem / 2.0, seed=seed + 500 + si * 137
            )
            rec(mk_s, m_s, s_s)

    # Also add 2 fresh CP-SAT mode_mix vectors if we have few distinct candidates
    avoid = [v[1] for v in cands.values()]
    for mi in range(2):
        if len(cands) >= top_k:
            break
        m_mix, _ = engine.mode_mix(X, secs=1.5, workers=1, seed=seed + 900 + mi, avoid=avoid)
        if m_mix is None:
            break
        avoid.append(m_mix)
        mk_ms, s_ms = engine.multistart(X, m_mix, 150, seed=seed + 950 + mi)
        rec(mk_ms, m_mix, s_ms)

    ranked = sorted(cands.values(), key=lambda x: x[0])
    return ranked[:top_k], st_m.get("evals", 0)


def solve_instance_v2(args):
    inst_id, budget_sec, seed = args
    _set_mem_limit(4)
    t0 = time.time()
    ds = data.MMLibDataset()
    info = ds.meta(inst_id)
    I, X = ds.load_inst(inst_id)
    bks = ds.load_bks_schedule(inst_id)
    warm = bks is not None
    ub = info["ub"]

    best_mk = None
    best_m = None
    best_s = None
    best_meth = ""
    cp_tested = 0
    cp_improved = 0

    if warm:
        m0, s0 = bks
        best_mk, best_m, best_s = int(s0[-1]), m0.copy(), s0.copy()
        init_sols = [(m0, s0)]
    else:
        init_sols = None

    # Stage 1: Metaheuristic mode-vector discovery (50% of budget)
    top_cands, meta_evals = collect_top_mode_vectors(
        X, time_budget=budget_sec * 0.50, seed=seed, init_solutions=init_sols, top_k=5
    )
    topo = np.array(engine.topo(X), dtype=np.int64)
    polished_cands = []
    for mk, m, s in top_cands:
        # Also evaluate with BOTH Serial SGS + Parallel SGS + FBI!
        o_c = fast_meta.order_from_starts(s, topo)
        mk_b, s_b = fast_meta.eval_both_sgs(o_c, m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20)
        if mk_b < mk:
            mk, s = int(mk_b), s_b
        polished_cands.append((mk, m, s))
        if best_mk is None or mk < best_mk:
            best_mk, best_m, best_s = mk, m, s
            best_meth = "warm_meta" if warm else "scratch_meta"
    top_cands = sorted(polished_cands, key=lambda x: x[0])

    # Stage 2: Exact Fixed-Mode CP-SAT on each of the top distinct mode vectors!
    # Target horizon = min(ub - 1, best_mk - 1) if close, or best_mk - 1
    for idx, (mk_c, m_c, s_c) in enumerate(top_cands):
        rem = budget_sec - (time.time() - t0)
        if rem < 3.0:
            break
        # If warm-started and this is the exact BKS mode vector, give it 2.5s; otherwise 4.5s
        H_try = best_mk - 1 if best_mk is not None else mk_c - 1
        if H_try < info["lb"]:
            break
        sub_tl = min(rem * 0.45, 4.5 if info["act"] <= 55 else 6.0)
        cp_tested += 1
        mk_cp, s_cp, st_name = solve_fixed_mode_cpsat(
            I, m_c, H=H_try, hint_starts=s_c, secs=sub_tl, workers=1, seed=seed + 2000 + idx
        )
        if mk_cp is not None and (best_mk is None or mk_cp < best_mk):
            best_mk, best_m, best_s = mk_cp, m_c.copy(), s_cp
            cp_improved += 1
            best_meth = ("warm" if warm else "scratch") + "+fixed_cpsat"

    # Stage 3: Window Compression on best schedule found (remaining budget)
    rem = budget_sec - (time.time() - t0)
    if best_m is not None and rem >= 4.0:
        mk_w, m_w, s_w, st_w = window_compress.slide_compress(
            I, X, best_m, best_s, time_budget=rem, workers=1, seed=seed + 3000
        )
        if mk_w < best_mk:
            best_mk, best_m, best_s = mk_w, m_w, s_w
            best_meth = (best_meth or ("warm" if warm else "scratch")) + "+win_compress"

    dt = round(time.time() - t0, 2)
    win_ok = False
    win_msg = ""
    if best_m is not None and best_s is not None:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, best_m, best_s,
            warm_start=warm, seed=seed, method=best_meth or "v2", runtime_sec=dt
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
        "ub": ub,
        "warm": warm,
        "best_mk": best_mk,
        "gain": (ub - best_mk) if best_mk is not None else None,
        "win": win_ok,
        "win_msg": win_msg,
        "method": best_meth,
        "secs": dt,
        "meta_evals": meta_evals,
        "cp_tested": cp_tested,
        "cp_improved": cp_improved,
    }


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "ref8_20"
    budget_sec = float(sys.argv[2]) if len(sys.argv) > 2 else 45.0
    n_workers = min(4, int(sys.argv[3]) if len(sys.argv) > 3 else 4)

    ds = data.MMLibDataset()
    # Warm up Numba cache
    I0, X0 = ds.load_inst(1)
    m0, s0 = ds.load_bks_schedule(1)
    fast_meta.run_sa_penalty(X0, m0, s0, time_budget=0.1, seed=1)

    if mode == "ref8_20":
        # 20 diverse ref=8 (2018, no BKS) instances with moderate-to-large gaps (starting with the promising ones!)
        cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == "8"]
        # Pick 10 with gap in [3..15] (sweet spot where UB is reachable from scratch!) and 10 with gap in [16..35]
        sweet = [c["id"] for c in cands if 3 <= (c["ub"] - c["lb"]) <= 15]
        large = [c["id"] for c in cands if 16 <= (c["ub"] - c["lb"]) <= 35]
        # Ensure 2701, 541, 1087 are included
        picks = [2701, 541, 1087]
        for lst, k in [(sweet, 12), (large, 5)]:
            for iid in lst:
                if iid not in picks and len(picks) < 20:
                    picks.append(iid)
                if len(picks) >= 20:
                    break
    elif mode == "ref8_100":
        # 20 diverse ref=8 (2018, no BKS) A=100 M=9 & M=6 instances with moderate gaps [2..16]
        cands = [
            ds.meta(i) for i in ds.open_ids()
            if ds.rows[i].get("UB ref") == "8" and ds.meta(i)["act"] == 100 and ds.meta(i)["modes"] >= 6
        ]
        # Prioritize moderate gaps (2..16) where 2018 UB is most reachable & beatable!
        cands.sort(key=lambda c: (abs((c["ub"] - c["lb"]) - 7), -c["modes"], c["id"]))
        picks = [2701]
        for c in cands:
            if c["id"] not in picks:
                picks.append(c["id"])
            if len(picks) >= 20:
                break
    elif mode == "wave_low_os_ref8":
        # ALL ref=8 low-OS (<0.35) A=100 M>=6 gap 2..18 (excluding the 5 already won)
        already = {2161, 2170, 2177, 2178, 2714}
        cands = []
        for i in ds.open_ids():
            if i in already:
                continue
            r = ds.rows[i]
            if r.get("UB ref") != "8":
                continue
            os_val = float(r["OS"].replace(",", "."))
            c = ds.meta(i)
            if c["act"] == 100 and c["modes"] >= 6 and os_val < 0.35 and 2 <= (c["ub"] - c["lb"]) <= 18:
                cands.append(c)
        # Prioritize RR=6, M=6/9, then RR=4 near-misses, then RR=8
        cands.sort(key=lambda c: (0 if c["rr"] == 6 else (1 if c["rr"] == 4 else 2), 0 if c["modes"] == 6 else 1, abs((c["ub"] - c["lb"]) - 7), c["id"]))
        picks = [c["id"] for c in cands]
    elif mode == "wave_low_os_ref5_and_50":
        # All ref=5 low-OS A=100 M>=6 (warm-started!) + ref=8 low-OS A=50 M>=6 gap 3..15
        cands = []
        for i in ds.open_ids():
            r = ds.rows[i]
            os_val = float(r["OS"].replace(",", "."))
            c = ds.meta(i)
            if os_val >= 0.35 or c["modes"] < 6:
                continue
            if r.get("UB ref") == "5" and c["act"] == 100 and 2 <= (c["ub"] - c["lb"]) <= 18:
                cands.append((0, c))
            elif r.get("UB ref") == "8" and c["act"] == 50 and 3 <= (c["ub"] - c["lb"]) <= 15:
                cands.append((1, c))
        cands.sort(key=lambda x: (x[0], x[1]["rr"], abs((x[1]["ub"] - x[1]["lb"]) - 7), x[1]["id"]))
        picks = [x[1]["id"] for x in cands]
    elif mode == "wave1_rr4_100":
        # All ref=8 A=100 instances with RR==4 (2R+2N) — our 80% win-rate goldmine!
        cands = [
            ds.meta(i) for i in ds.open_ids()
            if ds.rows[i].get("UB ref") == "8" and ds.meta(i)["act"] == 100 and ds.meta(i)["rr"] == 4
        ]
        # Skip the 4 already won in ref8_100
        already = {2161, 2170, 2177, 2178}
        cands = [c for c in cands if c["id"] not in already]
        cands.sort(key=lambda c: (0 if c["modes"] == 6 else (1 if c["modes"] == 9 else 2), -(c["ub"] - c["lb"]), c["id"]))
        picks = [c["id"] for c in cands]
    elif mode == "wave2_rr4_50_rr6_100":
        # All ref=8 A=50 RR==4 (M=6,9) + A=100 RR==6 M=6
        cands = [
            ds.meta(i) for i in ds.open_ids()
            if ds.rows[i].get("UB ref") == "8"
            and (
                (ds.meta(i)["act"] == 50 and ds.meta(i)["rr"] == 4 and ds.meta(i)["modes"] >= 6)
                or (ds.meta(i)["act"] == 100 and ds.meta(i)["rr"] == 6 and ds.meta(i)["modes"] == 6)
            )
        ]
        cands.sort(key=lambda c: (0 if c["rr"] == 4 else 1, -c["modes"], -(c["ub"] - c["lb"]), c["id"]))
        picks = [c["id"] for c in cands]
    elif mode == "wave3_rr6_100_9":
        # All ref=8 A=100 RR==6 M=9 + A=100 RR==8 M=6,9
        cands = [
            ds.meta(i) for i in ds.open_ids()
            if ds.rows[i].get("UB ref") == "8"
            and ds.meta(i)["act"] == 100
            and ds.meta(i)["rr"] >= 6
            and ds.meta(i)["modes"] >= 6
        ]
        cands.sort(key=lambda c: (c["rr"], -c["modes"], abs((c["ub"] - c["lb"]) - 8), c["id"]))
        picks = [c["id"] for c in cands]
    elif mode == "ref8_sweet_60":
        cands = [ds.meta(i) for i in ds.open_ids() if ds.rows[i].get("UB ref") == "8"]
        # Sort by Act=50 first or moderate gap [2..15]
        cands.sort(key=lambda c: (abs((c["ub"] - c["lb"]) - 8), c["act"], c["id"]))
        picks = [c["id"] for c in cands[:60]]
    else:
        # Comma-separated IDs
        picks = [int(x) for x in mode.split(",")]

    print(f"Hybrid v2 ({mode}): {len(picks)} instances, budget={budget_sec}s/inst, workers={n_workers}", flush=True)
    tasks = [(iid, budget_sec, 30000 + idx) for idx, iid in enumerate(picks)]
    results = []
    t_start = time.time()
    wins = []
    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futs = {ex.submit(solve_instance_v2, t): t[0] for t in tasks}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            tag = "WIN!!!" if r["win"] else "      "
            if r["win"]:
                wins.append(r)
            print(
                f"{tag} id={r['id']:4d} {r['file']:<14s} ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} "
                f"LB={r['lb']:3d} UB={r['ub']:3d} -> mk={str(r['best_mk']):>4s} (gain={str(r['gain']):>3s}) "
                f"{r['secs']:5.1f}s cp={r['cp_tested']}/{r['cp_improved']} {r['method']}",
                flush=True,
            )

    print(f"\n=== HYBRID V2 SUMMARY ({time.time() - t_start:.1f}s wall) ===", flush=True)
    print(f"Total: {len(results)} | Wins: {len(wins)} | Total gain: {sum(r['gain'] for r in wins)}", flush=True)
    out_path = os.path.join(PHASEB_DIR, "logs", f"hybrid_v2_{mode}.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
