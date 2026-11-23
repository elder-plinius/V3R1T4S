"""Stratified 20-instance Phase B pilot runner with strict resource caps (<=4 workers, 4GB RLIMIT_AS)."""
import json
import os
import resource
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# Enforce single-threaded math/numba inside each worker process BEFORE importing numpy/numba
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

PHASEB_DIR = os.path.dirname(os.path.abspath(__file__))
if PHASEB_DIR not in sys.path:
    sys.path.insert(0, PHASEB_DIR)

import data  # noqa: E402
import fast_meta  # noqa: E402
import cpsat_lns  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def solve_one_instance(args):
    inst_id, budget_sec, seed = args
    _set_mem_limit(4)
    t0 = time.time()
    ds = data.MMLibDataset()
    info = ds.meta(inst_id)
    I, X = ds.load_inst(inst_id)
    bks = ds.load_bks_schedule(inst_id)
    warm = bks is not None

    best_mk = None
    best_modes = None
    best_starts = None
    method_used = ""

    if warm:
        m0, s0 = bks
        best_mk = int(s0[-1])
        best_modes = m0.copy()
        best_starts = s0.copy()

        # Phase 1: Fast Memetic + Mode LS (25% of budget)
        t_meta = max(5.0, budget_sec * 0.25)
        mk_m, m_m, s_m, st_meta = fast_meta.memetic_search(
            X, time_budget=t_meta, seed=seed, init_solutions=[(m0, s0)],
            pop_size=16, target_mk=info["ub"] - 2, cpsat_mixes=2, cpsat_workers=1
        )
        if mk_m is not None and mk_m < best_mk:
            best_mk, best_modes, best_starts = mk_m, m_m, s_m
            method_used = "warm_memetic"

        # Phase 2: Adaptive CP-SAT LNS (remaining budget)
        rem = max(5.0, budget_sec - (time.time() - t0))
        mk_l, m_l, s_l, st_lns = cpsat_lns.cpsat_lns_loop(
            I, X, best_modes, best_starts, time_budget=rem, workers=1, seed=seed + 1000, ub_target=info["ub"] - 1
        )
        if mk_l is not None and mk_l < best_mk:
            best_mk, best_modes, best_starts = mk_l, m_l, s_l
            method_used = (method_used + "+cpsat_lns").lstrip("+")
    else:
        # From-scratch: Phase 1 Memetic GA (55% of budget) -> Phase 2 CP-SAT LNS (45% of budget)
        t_meta = max(8.0, budget_sec * 0.55)
        mk_m, m_m, s_m, st_meta = fast_meta.memetic_search(
            X, time_budget=t_meta, seed=seed, init_solutions=None,
            pop_size=24, target_mk=info["ub"] - 2, cpsat_mixes=5, cpsat_workers=1
        )
        if mk_m is not None:
            best_mk, best_modes, best_starts = mk_m, m_m, s_m
            method_used = "scratch_memetic"
            rem = max(5.0, budget_sec - (time.time() - t0))
            mk_l, m_l, s_l, st_lns = cpsat_lns.cpsat_lns_loop(
                I, X, best_modes, best_starts, time_budget=rem, workers=1, seed=seed + 1000, ub_target=info["ub"] - 1
            )
            if mk_l is not None and mk_l < best_mk:
                best_mk, best_modes, best_starts = mk_l, m_l, s_l
                method_used = "scratch_memetic+cpsat_lns"
        else:
            st_lns = {}

    dt = round(time.time() - t0, 2)
    win_ok = False
    win_msg = ""
    if best_modes is not None and best_starts is not None:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, best_modes, best_starts,
            warm_start=warm, seed=seed, method=method_used or ("warm_lns" if warm else "scratch"),
            runtime_sec=dt
        )
        if chk_mk is not None:
            best_mk = chk_mk

    return {
        "id": inst_id,
        "file": info["file"],
        "ub_ref": info["ub_ref"],
        "act": info["act"],
        "modes": info["modes"],
        "rr": info["rr"],
        "lb": info["lb"],
        "ub": info["ub"],
        "warm": warm,
        "best_mk": best_mk,
        "gain": (info["ub"] - best_mk) if best_mk is not None else None,
        "win": win_ok,
        "win_msg": win_msg,
        "method": method_used,
        "secs": dt,
        "meta_evals": st_meta.get("evals", 0),
        "lns_iters": st_lns.get("iters", 0) if isinstance(st_lns, dict) else 0,
        "lns_imps": st_lns.get("improvements", 0) if isinstance(st_lns, dict) else 0,
    }


def select_pilot_20(ds: data.MMLibDataset):
    """Fixed deterministic stratified selection of 20 open instances across all 4 UB refs."""
    open_ids = sorted(ds.open_ids())
    picks = []
    for ref in ["1", "5", "7", "8"]:
        cands = [i for i in open_ids if ds.rows[i].get("UB ref") == ref]
        # Pick 3 with Act=50 (3, 6, 9 modes) and 2 with Act=100 (3/6, 9 modes)
        sub = []
        for act, modes in [(50, 3), (50, 6), (50, 9), (100, 3), (100, 9)]:
            m_cands = [i for i in cands if ds.meta(i)["act"] == act and ds.meta(i)["modes"] == modes and i not in sub]
            if not m_cands:
                m_cands = [i for i in cands if ds.meta(i)["act"] == act and i not in sub]
            if not m_cands:
                m_cands = [i for i in cands if i not in sub]
            if m_cands:
                sub.append(m_cands[0])
        picks.extend(sub[:5])
    return picks


def main():
    budget_sec = float(sys.argv[1]) if len(sys.argv) > 1 else 35.0
    n_workers = min(4, int(sys.argv[2]) if len(sys.argv) > 2 else 4)

    ds = data.MMLibDataset()
    # Warm up Numba cache once in main process before forking/spawning
    I0, X0 = ds.load_inst(1)
    fast_meta.memetic_search(X0, time_budget=0.5, seed=1, cpsat_mixes=1, cpsat_workers=1)

    pilot_ids = select_pilot_20(ds)
    print(f"Pilot 20 instances (budget={budget_sec}s/inst, workers={n_workers}): {pilot_ids}", flush=True)

    tasks = [(iid, budget_sec, 2026000 + idx) for idx, iid in enumerate(pilot_ids)]
    results = []
    t_start = time.time()
    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futs = {ex.submit(solve_one_instance, t): t[0] for t in tasks}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            tag = "WIN!!!" if r["win"] else "      "
            print(
                f"{tag} id={r['id']:4d} {r['file']:<14s} ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} "
                f"warm={int(r['warm'])} LB={r['lb']:3d} UB={r['ub']:3d} -> mk={str(r['best_mk']):>4s} "
                f"(gain={str(r['gain']):>3s}) {r['secs']:5.1f}s evals={r['meta_evals']:5d} lns={r['lns_iters']:2d}/{r['lns_imps']} {r['method']}",
                flush=True,
            )

    results.sort(key=lambda x: x["id"])
    wins = [r for r in results if r["win"]]
    print(f"\n=== PILOT SUMMARY ({time.time() - t_start:.1f}s wall) ===", flush=True)
    print(f"Total: {len(results)} | Wins: {len(wins)} | Total gain: {sum(r['gain'] for r in wins)}", flush=True)
    for ref in ["1", "5", "7", "8"]:
        sub = [r for r in results if r["ub_ref"] == ref]
        w = [r for r in sub if r["win"]]
        print(f"  ref={ref}: {len(w)}/{len(sub)} wins (total gain {sum(r['gain'] for r in w)})", flush=True)

    out_path = os.path.join(PHASEB_DIR, "logs", "pilot20_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved to {out_path}", flush=True)


if __name__ == "__main__":
    main()
