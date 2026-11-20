"""
Phase B Hybrid v3.2 Warm-Start Engine (hybrid_v32_warm.py):
Combines the best of v3 (global mode-basin injection via cpsat_mixes=5 + 2 independent Memetic waves)
with the best of v3.1 (warm-start perturbation seeding, multi-temperature Penalty SA, Dual-SGS,
and excluding untouched m0 from Stage 2 Fixed-Mode CP-SAT).

Runs:
  1. Batch A (P1_M9_rerun): 25 remaining M=9 Pool 1 instances (ref=7 low-OS, RR=6/8).
  2. Batch B (P2_ref5_midOS): 46 untouched Pool 2 instances (ref=5 CPO 2023, mid-OS 0.35..0.55, A=100, M=6/9).
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
import data  # noqa: E402
import engine  # noqa: E402
import fast_meta  # noqa: E402
import hybrid_v2  # noqa: E402
import hybrid_v31_warm  # noqa: E402
import window_compress  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def solve_warm_v32(args):
    inst_id, pool_tag, budget_sec, seed, existing_win_mk = args
    _set_mem_limit(4)
    t0 = time.time()
    ds = data.MMLibDataset()
    info = ds.meta(inst_id)
    I, X = ds.load_inst(inst_id)
    bks = ds.load_bks_schedule(inst_id)
    assert bks is not None, f"Instance {inst_id} has no BKS schedule!"
    m0, s0 = bks[0].copy(), bks[1].copy()
    ub = info["ub"]
    target_ub = min(ub, existing_win_mk) if existing_win_mk is not None else ub

    topo = np.array(engine.topo(X), dtype=np.int64)
    rng = np.random.default_rng(seed)

    best_mk = int(s0[-1])
    best_m = m0.copy()
    best_s = s0.copy()
    best_meth = ""
    total_evals = 0
    cp_tested = 0
    cp_improved = 0

    new_cands = {}  # bytes(m) -> (mk, m, s) for genuinely NEW mode vectors (Hamming >= 2 from m0)

    def record_cand(mk, m, s):
        nonlocal best_mk, best_m, best_s, best_meth
        if mk is None or m is None or s is None:
            return
        ok, _ = fast_meta.check_nr_feasible(m, X.nreq, X.ncap)
        if not ok:
            return
        o_c = fast_meta.order_from_starts(s, topo)
        mk_b, st_b = fast_meta.eval_both_sgs(o_c, m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20)
        if mk_b < mk:
            mk, s = int(mk_b), st_b
        if mk < best_mk:
            best_mk, best_m, best_s = int(mk), m.copy(), s.copy()
            best_meth = "v32_warm_meta"
        if int(np.sum(m != m0)) >= 2:
            key = bytes(m.astype(np.uint8).tobytes())
            if key not in new_cands or mk < new_cands[key][0]:
                new_cands[key] = (int(mk), m.copy(), s.copy())

    # --- STAGE 1: 2 Independent Memetic (cpsat_mixes=5!) + Multi-Temp Penalty SA Waves (65% of budget = ~156s) ---
    wave_budget = (budget_sec * 0.65) / 2.0
    for w_idx in range(2):
        w_seed = seed + w_idx * 7919
        # Seed with current best + 6 NR-repaired perturbations of m0
        init_sols = [(best_m, best_s)]
        for _ in range(8):
            m_pert = best_m.copy()
            k_mut = int(rng.integers(4, 16))
            for j in rng.choice(np.arange(1, X.n - 1), size=min(k_mut, X.n - 2), replace=False):
                m_pert[j] = int(rng.integers(1, X.nm[j] + 1))
            m_rep, ok = fast_meta.repair_modes_nr(m_pert, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
            if ok and int(np.sum(m_rep != m0)) >= 2:
                init_sols.append((m_rep, best_s))

        # 55% of wave -> Memetic GA WITH cpsat_mixes=5 (global mode-basin injection!)
        mk_m, m_m, s_m, st_m = fast_meta.memetic_search(
            X, time_budget=wave_budget * 0.55, seed=w_seed, init_solutions=init_sols[:7],
            pop_size=28, cpsat_mixes=5, cpsat_workers=1
        )
        total_evals += st_m.get("evals", 0)
        record_cand(mk_m, m_m, s_m)
        for mk_p, m_p, s_p in st_m.get("top_pop", []):
            record_cand(mk_p, m_p, s_p)

        # 45% of wave -> 2 Multi-Temp Penalty SA restarts (gentle + hot basin-hop)
        sa_temps = [1.6, 4.0] if w_idx == 0 else [2.0, 5.0]
        per_sa = (wave_budget * 0.45) / len(sa_temps)
        for ti, t_val in enumerate(sa_temps):
            if ti == 0:
                sm, ss = best_m.copy(), best_s.copy()
            else:
                # Start hot SA from a distinct top elite if available
                elites = sorted(new_cands.values(), key=lambda x: x[0])
                if elites:
                    pick_e = elites[min(w_idx, len(elites) - 1)]
                    sm, ss = pick_e[1].copy(), pick_e[2].copy()
                else:
                    sm, ss = best_m.copy(), best_s.copy()
            mk_s, m_s, s_s, cands_s, ev_s = hybrid_v31_warm.run_sa_penalty_temp(
                X, sm, ss, time_budget=per_sa, t_start_val=t_val, seed=w_seed + 2000 + ti * 313
            )
            total_evals += ev_s
            record_cand(mk_s, m_s, s_s)
            for mk_c, m_c, s_c in cands_s:
                record_cand(mk_c, m_c, s_c)

    # --- STAGE 2: Exact Fixed-Mode CP-SAT exclusively on top 12 genuinely NEW mode vectors ---
    ranked_new = sorted(new_cands.values(), key=lambda x: x[0])
    has_new_tight = any(c[0] <= best_mk for c in ranked_new)
    cp_end = t0 + budget_sec * (0.95 if has_new_tight else 0.99)
    for idx, (mk_c, m_c, s_c) in enumerate(ranked_new[:12]):
        rem = cp_end - time.time()
        if rem < 2.5:
            break
        H_try = best_mk - 1
        if H_try < info["lb"]:
            break
        sub_tl = min(rem, 8.0)
        cp_tested += 1
        mk_cp, s_cp, _ = hybrid_v2.solve_fixed_mode_cpsat(
            I, m_c, H=H_try, hint_starts=s_c, secs=sub_tl, workers=1, seed=seed + 5000 + idx * 19
        )
        if mk_cp is not None and mk_cp < best_mk:
            best_mk, best_m, best_s = int(mk_cp), m_c.copy(), s_cp
            cp_improved += 1
            best_meth = "v32_warm+fixed_cpsat"

    # --- STAGE 3: Window Compression ONLY if best_m != m0 ---
    rem = budget_sec - (time.time() - t0)
    if rem >= 4.0 and int(np.sum(best_m != m0)) >= 1:
        mk_w, m_w, s_w, _ = window_compress.slide_compress(
            I, X, best_m, best_s, time_budget=rem, workers=1, seed=seed + 8000
        )
        if mk_w < best_mk:
            best_mk, best_m, best_s = int(mk_w), m_w, s_w
            best_meth = (best_meth or "v32_warm") + "+win_compress"

    dt = round(time.time() - t0, 2)
    win_ok = False
    win_msg = ""
    if best_mk < target_ub:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, best_m, best_s,
            warm_start=True, seed=seed, method=best_meth or "v32_warm", runtime_sec=dt
        )
        if chk_mk is not None:
            best_mk = chk_mk

    return {
        "id": inst_id,
        "pool": pool_tag,
        "file": info["file"],
        "ub_ref": info["ub_ref"],
        "act": info["act"],
        "modes": info["modes"],
        "rr": info["rr"],
        "lb": info["lb"],
        "ub": ub,
        "warm": True,
        "best_mk": best_mk,
        "gain": ub - best_mk,
        "new_win": win_ok,
        "win_msg": win_msg,
        "method": best_meth,
        "secs": dt,
        "evals": total_evals,
        "new_modes_found": len(ranked_new),
        "cp_tested": cp_tested,
        "cp_improved": cp_improved,
    }


def build_p1m9_and_p2_queue(ds: data.MMLibDataset, existing_wins: dict):
    queue = []
    # Batch A: the 25 M=9 instances from v3.1 Pool 1 (RR=6 first, then RR=8)
    v31_log = os.path.join(PHASEB_DIR, "logs", "hybrid_v31_pool1.jsonl")
    p1_m9 = []
    for line in open(v31_log):
        r = json.loads(line)
        if r["modes"] == 9 and r["id"] not in existing_wins:
            p1_m9.append(r["id"])
    p1_m9.sort(key=lambda i: (ds.meta(i)["rr"], -(ds.meta(i)["ub"] - ds.meta(i)["lb"]), i))
    for iid in p1_m9:
        queue.append((iid, "P1_M9_rerun"))

    # Batch B: all 46 untouched Pool 2 (ref=5 CPO 2023, mid-OS 0.35..0.55, A=100, M>=6, gap 2..18)
    p2 = []
    for i in ds.open_ids():
        if i in existing_wins:
            continue
        r = ds.rows[i]
        os_val = float(r["OS"].replace(",", "."))
        m = ds.meta(i)
        if r.get("UB ref") == "5" and 0.35 <= os_val < 0.55 and m["act"] == 100 and m["modes"] >= 6 and 2 <= (m["ub"] - m["lb"]) <= 18:
            p2.append(m)
    p2.sort(key=lambda c: (-c["modes"], c["rr"], -(c["ub"] - c["lb"]), c["id"]))
    for c in p2:
        queue.append((c["id"], "P2_ref5_midOS"))

    return queue


def main():
    budget_sec = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
    n_workers = min(4, int(sys.argv[2]) if len(sys.argv) > 2 else 4)

    ds = data.MMLibDataset()
    existing_wins = hybrid_v31_warm.load_existing_wins()

    # Warmup Numba cache
    I0, X0 = ds.load_inst(1)
    m0, s0 = ds.load_bks_schedule(1)
    topo0 = np.array(engine.topo(X0), dtype=np.int64)
    o0 = fast_meta.order_from_starts(s0, topo0)
    fast_meta.eval_both_sgs(o0, m0, X0.dur, X0.req, X0.cap, X0.pp, X0.pi, X0.sp, X0.si, X0.H, 10)
    fast_meta.run_sa_penalty(X0, m0, s0, time_budget=0.1, seed=1)

    queue = build_p1m9_and_p2_queue(ds, existing_wins)
    n_a = sum(1 for _, t in queue if t == "P1_M9_rerun")
    n_b = sum(1 for _, t in queue if t == "P2_ref5_midOS")
    print(f"Hybrid v3.2 START: {len(queue)} total ({n_a} P1_M9_rerun + {n_b} P2_ref5_midOS), budget={budget_sec:.0f}s, workers={n_workers}", flush=True)

    log_path = os.path.join(PHASEB_DIR, "logs", "hybrid_v32_p1m9_p2.jsonl")
    t_start = time.time()
    tasks = [(iid, tag, budget_sec, 120000 + idx, existing_wins.get(iid)) for idx, (iid, tag) in enumerate(queue)]
    new_wins = 0
    new_gain = 0
    done = 0
    wins_by_pool = {"P1_M9_rerun": 0, "P2_ref5_midOS": 0}

    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futs = {ex.submit(solve_warm_v32, t): t[0] for t in tasks}
        for fut in as_completed(futs):
            r = fut.result()
            done += 1
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            if r["new_win"]:
                new_wins += 1
                new_gain += r["gain"]
                wins_by_pool[r["pool"]] = wins_by_pool.get(r["pool"], 0) + 1
                mark = "WIN!!!"
            else:
                mark = "      "
            elapsed_m = (time.time() - t_start) / 60.0
            print(
                f"{mark} [{elapsed_m:5.1f}m] ({done:2d}/{len(queue)}) {r['pool']:<14s} id={r['id']:4d} {r['file']:<14s} "
                f"ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} RR={r['rr']} LB={r['lb']:3d} UB={r['ub']:3d} -> "
                f"mk={r['best_mk']:3d} (gain={r['gain']:+2d}) {r['secs']:5.1f}s newM={r['new_modes_found']:3d} "
                f"cp={r['cp_tested']:2d}/{r['cp_improved']} {r['method']}",
                flush=True,
            )

    print(
        f"\n=== V3.2 COMPLETE ({(time.time() - t_start)/60.0:.1f}m wall) ===\n"
        f"Done: {done}/{len(queue)} | NEW wins: {new_wins} (P1_M9_rerun: {wins_by_pool['P1_M9_rerun']}, P2_ref5_midOS: {wins_by_pool['P2_ref5_midOS']}) | NEW gain: -{new_gain} pts",
        flush=True,
    )


if __name__ == "__main__":
    main()
