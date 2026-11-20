"""
Phase B Hybrid v3.1 Warm-Start Specialist (hybrid_v31_warm.py):
Built specifically for warm-started pools (Pool 1: ref=7 Tian 2026 low-OS, Pool 2: ref=5 mid-OS, etc.):
  1. Single deep 240s pass (no redundant 90s Pass 1).
  2. Warm-start perturbation seeding (15-20 NR-repaired perturbations of m0, skipping slow cold mode_mix).
  3. Multi-temperature Penalty SA restarts (2 gentle local walks + 3 hot basin-hopping restarts).
  4. Dual-SGS (Serial + Parallel SGS + FBI) across all collected elite mode vectors.
  5. Excludes untouched BKS mode vector m0 from Stage 2; runs Exact Fixed-Mode CP-SAT (7-9s each)
     exclusively on top 10-12 genuinely NEW mode vectors (Hamming distance >= 2 from m0).
  6. Skips idle Window Compression on unchanged m0; puts those seconds into extra CP-SAT candidates.
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
import window_compress  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def run_sa_penalty_temp(X, init_modes, init_starts, time_budget: float, t_start_val: float, seed: int):
    """Run Strategic-Oscillation Penalty SA with an explicit starting temperature."""
    t0 = time.time()
    topo = np.array(engine.topo(X), dtype=np.int64)
    best_m = np.asarray(init_modes, dtype=np.int64).copy()
    best_st = np.asarray(init_starts, dtype=np.int64).copy()
    best_o = fast_meta.order_from_starts(best_st, topo)
    best_mk, best_st = fast_meta.eval_both_sgs(
        best_o, best_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 15
    )
    best_o = fast_meta.order_from_starts(best_st, topo)

    total_evals = 1
    chunk_iters = 22000 if X.n <= 60 else 14000
    round_idx = 0
    # Also track best STRICTLY NEW mode vector (differs from init_modes in >= 2 positions)
    new_cands = {}

    while time.time() - t0 < time_budget:
        mk, o, m, st, ev, _ = fast_meta.sa_penalty_numba(
            best_o, best_m, X.dur, X.req, X.nreq, X.nm, X.cap, X.ncap,
            X.pp, X.pi, X.sp, X.si, X.H, topo, chunk_iters, float(t_start_val), 0.08, seed + round_idx * 997
        )
        total_evals += ev
        round_idx += 1
        ok, _ = fast_meta.check_nr_feasible(m, X.nreq, X.ncap)
        if ok:
            mk_b, st_b = fast_meta.eval_both_sgs(
                o, m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 15
            )
            key = bytes(m.astype(np.uint8).tobytes())
            if key not in new_cands or mk_b < new_cands[key][0]:
                new_cands[key] = (int(mk_b), m.copy(), st_b.copy())
            if mk_b < best_mk:
                best_mk, best_o, best_m, best_st = int(mk_b), fast_meta.order_from_starts(st_b, topo), m.copy(), st_b.copy()

    return best_mk, best_m, best_st, list(new_cands.values()), total_evals


def solve_warm_v31(args):
    inst_id, budget_sec, seed, existing_win_mk = args
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

    # Pool of genuinely NEW feasible mode vectors (Hamming distance >= 2 from m0)
    new_cands = {}  # bytes(m) -> (mk, m, s)

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
            best_meth = "v31_warm_meta"
        hamming = int(np.sum(m != m0))
        if hamming >= 2:
            key = bytes(m.astype(np.uint8).tobytes())
            if key not in new_cands or mk < new_cands[key][0]:
                new_cands[key] = (int(mk), m.copy(), s.copy())

    # --- STAGE 1A: Warm-start perturbation-seeded Memetic GA (25% of budget, NO cold mode_mix!) ---
    init_sols = [(m0, s0)]
    for pi in range(18):
        m_pert = m0.copy()
        k_mut = int(rng.integers(4, 16))
        jobs_mut = rng.choice(np.arange(1, X.n - 1), size=min(k_mut, X.n - 2), replace=False)
        for j in jobs_mut:
            m_pert[j] = int(rng.integers(1, X.nm[j] + 1))
        m_rep, ok = fast_meta.repair_modes_nr(m_pert, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
        if ok and int(np.sum(m_rep != m0)) >= 2:
            init_sols.append((m_rep, s0))

    mk_m, m_m, s_m, st_m = fast_meta.memetic_search(
        X, time_budget=budget_sec * 0.25, seed=seed, init_solutions=init_sols[:12],
        pop_size=30, cpsat_mixes=0, cpsat_workers=1
    )
    total_evals += st_m.get("evals", 0)
    record_cand(mk_m, m_m, s_m)
    for mk_p, m_p, s_p in st_m.get("top_pop", []):
        record_cand(mk_p, m_p, s_p)

    # --- STAGE 1B: 5 Multi-Temperature Penalty SA Restarts (35% of budget) ---
    # 2 gentle local-basin walks + 3 hot basin-hopping restarts
    sa_temps = [1.4, 1.8, 3.2, 4.2, 5.2]
    sa_total = budget_sec * 0.35
    per_sa = sa_total / len(sa_temps)
    for idx_t, t_val in enumerate(sa_temps):
        if time.time() - t0 >= budget_sec * 0.62:
            break
        # Start gentle walks from current best; start hot walks from perturbed m0 or top new candidate
        if idx_t < 2:
            start_m, start_s = best_m.copy(), best_s.copy()
        else:
            m_pert = best_m.copy()
            k_mut = int(rng.integers(6, 18))
            for j in rng.choice(np.arange(1, X.n - 1), size=min(k_mut, X.n - 2), replace=False):
                m_pert[j] = int(rng.integers(1, X.nm[j] + 1))
            m_rep, ok = fast_meta.repair_modes_nr(m_pert, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
            start_m = m_rep if ok else best_m.copy()
            start_s = best_s.copy()

        mk_s, m_s, s_s, cands_s, ev_s = run_sa_penalty_temp(
            X, start_m, start_s, time_budget=per_sa, t_start_val=t_val, seed=seed + 2000 + idx_t * 313
        )
        total_evals += ev_s
        record_cand(mk_s, m_s, s_s)
        for mk_c, m_c, s_c in cands_s:
            record_cand(mk_c, m_c, s_c)

    # --- STAGE 2: Exact Fixed-Mode CP-SAT exclusively on genuinely NEW mode vectors (35%-40% of budget) ---
    ranked_new = sorted(new_cands.values(), key=lambda x: x[0])
    # Check if we have a new UB-tying or winning mode vector (to decide if Stage 3 window compress is worth 10s)
    has_new_tight = any(c[0] <= best_mk for c in ranked_new)
    cp_end = t0 + budget_sec * (0.94 if has_new_tight else 0.99)
    max_cp_cands = 12
    for idx, (mk_c, m_c, s_c) in enumerate(ranked_new[:max_cp_cands]):
        rem = cp_end - time.time()
        if rem < 2.5:
            break
        H_try = best_mk - 1
        if H_try < info["lb"]:
            break
        sub_tl = min(rem, 8.0)
        cp_tested += 1
        mk_cp, s_cp, st_name = hybrid_v2.solve_fixed_mode_cpsat(
            I, m_c, H=H_try, hint_starts=s_c, secs=sub_tl, workers=1, seed=seed + 5000 + idx * 19
        )
        if mk_cp is not None and mk_cp < best_mk:
            best_mk, best_m, best_s = int(mk_cp), m_c.copy(), s_cp
            cp_improved += 1
            best_meth = "v31_warm+fixed_cpsat"

    # --- STAGE 3: Window Compression ONLY if best_m != m0 (never idle on unchanged BKS!) ---
    rem = budget_sec - (time.time() - t0)
    if rem >= 4.0 and int(np.sum(best_m != m0)) >= 1:
        mk_w, m_w, s_w, _ = window_compress.slide_compress(
            I, X, best_m, best_s, time_budget=rem, workers=1, seed=seed + 8000
        )
        if mk_w < best_mk:
            best_mk, best_m, best_s = int(mk_w), m_w, s_w
            best_meth = (best_meth or "v31_warm") + "+win_compress"

    dt = round(time.time() - t0, 2)
    win_ok = False
    win_msg = ""
    if best_mk < target_ub:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, best_m, best_s,
            warm_start=True, seed=seed, method=best_meth or "v31_warm", runtime_sec=dt
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


def load_existing_wins():
    wins = {}
    for p in glob.glob(os.path.join(PHASEB_DIR, "wins", "*.json")):
        rec = json.load(open(p))
        iid = rec["id"]
        if iid not in wins or rec["new_mk"] < wins[iid]:
            wins[iid] = rec["new_mk"]
    return wins


def build_pool1_remaining(ds: data.MMLibDataset, existing_wins: dict):
    """Return all ref=7 low-OS (<0.35) A=100 M>=6 gap 2..18 that did NOT already complete P2 in v3."""
    p2_done = set()
    v3_log = os.path.join(PHASEB_DIR, "logs", "hybrid_v3_campaign.jsonl")
    if os.path.exists(v3_log):
        for line in open(v3_log):
            r = json.loads(line)
            if r.get("pool") == "P4_ref7_lowOS_P2":
                p2_done.add(r["id"])

    cands = []
    for i in ds.open_ids():
        if i in existing_wins or i in p2_done:
            continue
        r = ds.rows[i]
        os_val = float(r["OS"].replace(",", "."))
        m = ds.meta(i)
        if r.get("UB ref") == "7" and os_val < 0.35 and m["act"] == 100 and m["modes"] >= 6 and 2 <= (m["ub"] - m["lb"]) <= 18:
            cands.append(m)
    cands.sort(key=lambda c: (c["rr"], -c["modes"], -(c["ub"] - c["lb"]), c["id"]))
    return [c["id"] for c in cands]


def main():
    budget_sec = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0
    n_workers = min(4, int(sys.argv[2]) if len(sys.argv) > 2 else 4)

    ds = data.MMLibDataset()
    existing_wins = load_existing_wins()

    # Warmup Numba cache
    I0, X0 = ds.load_inst(1)
    m0, s0 = ds.load_bks_schedule(1)
    topo0 = np.array(engine.topo(X0), dtype=np.int64)
    o0 = fast_meta.order_from_starts(s0, topo0)
    fast_meta.eval_both_sgs(o0, m0, X0.dur, X0.req, X0.cap, X0.pp, X0.pi, X0.sp, X0.si, X0.H, 10)
    fast_meta.run_sa_penalty(X0, m0, s0, time_budget=0.1, seed=1)

    picks = build_pool1_remaining(ds, existing_wins)
    print(f"Hybrid v3.1 Pool 1 START: {len(picks)} remaining ref=7 low-OS instances, budget={budget_sec:.0f}s, workers={n_workers}", flush=True)

    log_path = os.path.join(PHASEB_DIR, "logs", "hybrid_v31_pool1.jsonl")
    t_start = time.time()
    tasks = [(iid, budget_sec, 110000 + idx, existing_wins.get(iid)) for idx, iid in enumerate(picks)]
    new_wins = 0
    new_gain = 0
    done = 0

    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        futs = {ex.submit(solve_warm_v31, t): t[0] for t in tasks}
        for fut in as_completed(futs):
            r = fut.result()
            done += 1
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            if r["new_win"]:
                new_wins += 1
                new_gain += r["gain"]
                mark = "WIN!!!"
            else:
                mark = "      "
            elapsed_m = (time.time() - t_start) / 60.0
            print(
                f"{mark} [{elapsed_m:5.1f}m] ({done:2d}/{len(picks)}) id={r['id']:4d} {r['file']:<14s} "
                f"ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} RR={r['rr']} LB={r['lb']:3d} UB={r['ub']:3d} -> "
                f"mk={r['best_mk']:3d} (gain={r['gain']:+2d}) {r['secs']:5.1f}s newM={r['new_modes_found']:3d} "
                f"cp={r['cp_tested']:2d}/{r['cp_improved']} {r['method']}",
                flush=True,
            )

    print(
        f"\n=== POOL 1 COMPLETE ({(time.time() - t_start)/60.0:.1f}m wall) ===\n"
        f"Done: {done}/{len(picks)} | NEW Pool 1 wins: {new_wins} | NEW gain: -{new_gain} pts",
        flush=True,
    )


if __name__ == "__main__":
    main()
