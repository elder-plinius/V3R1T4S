"""
Phase B Hybrid v3 Solver (3-hour autonomous campaign):
Upgrades over hybrid_v2:
  1. Serial + Parallel SGS (eval_both_sgs) applied across all elite mode vectors (not just top 3).
  2. Extracts full top-10 distinct feasible mode vectors from Memetic GA population + multi-seed
     Strategic-Oscillation Penalty SA + diversified mode_mix.
  3. Tests up to 8-10 distinct mode vectors in Exact Fixed-Mode CP-SAT (6-10s each).
  4. Adaptive Two-Pass budget:
     - Pass 1 (90s): broad exploration; if an instance hits gain >= -1 (tie or 1 away from UB),
       automatically promoted to Pass 2!
     - Pass 2 (210s, 3 independent seeds): deep multi-seed diversification + top-10 Fixed-Mode CP-SAT
       + Window Compression.
  5. Strict built-in wall-clock deadline (--deadline-epoch) + <=4 workers + 4GB RLIMIT_AS + mm.check() gate.
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
import window_compress  # noqa: E402
import hybrid_v2  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def collect_diverse_modes_v3(X, time_budget, seed, init_solutions=None, top_k=10, n_sa_restarts=3):
    """Run Memetic GA + multi-seed Penalty SA + PSGS/SSGS polish to collect top_k distinct mode vectors."""
    t0 = time.time()
    topo = np.array(engine.topo(X), dtype=np.int64)
    cands = {}  # bytes(modes) -> (mk, modes, starts)
    total_evals = 0

    def rec(mk, modes, starts):
        if mk is None or modes is None or starts is None:
            return
        ok, _ = fast_meta.check_nr_feasible(modes, X.nreq, X.ncap)
        if not ok:
            return
        # Polish with BOTH Serial SGS and Parallel SGS + FBI!
        o_c = fast_meta.order_from_starts(starts, topo)
        mk_b, st_b = fast_meta.eval_both_sgs(o_c, modes, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20)
        if mk_b < mk:
            mk, starts = int(mk_b), st_b
        key = bytes(modes.astype(np.uint8).tobytes())
        if key not in cands or mk < cands[key][0]:
            cands[key] = (int(mk), modes.copy(), starts.copy())

    # 1. Memetic GA (50% of meta budget) — extract its entire top-10 elite population!
    mk_m, m_m, s_m, st_m = fast_meta.memetic_search(
        X, time_budget=time_budget * 0.50, seed=seed, init_solutions=init_solutions,
        pop_size=28, cpsat_mixes=5, cpsat_workers=1
    )
    total_evals += st_m.get("evals", 0)
    rec(mk_m, m_m, s_m)
    for mk_p, m_p, s_p in st_m.get("top_pop", []):
        rec(mk_p, m_p, s_p)

    # 2. Multi-seed Strategic-Oscillation Penalty SA (50% of meta budget)
    ranked_so_far = sorted(cands.values(), key=lambda x: x[0])
    rem = max(3.0, time_budget - (time.time() - t0))
    if ranked_so_far:
        per_sa = rem / float(n_sa_restarts)
        for si in range(n_sa_restarts):
            if time.time() - t0 >= time_budget:
                break
            # Start each SA restart from a different top elite (0, 1, 2) for basin diversity!
            base = ranked_so_far[min(si, len(ranked_so_far) - 1)]
            mk_s, m_s, s_s, st_s = fast_meta.run_sa_penalty(
                X, base[1], base[2], time_budget=per_sa, seed=seed + 1000 + si * 271
            )
            total_evals += st_s.get("evals", 0)
            rec(mk_s, m_s, s_s)

    ranked = sorted(cands.values(), key=lambda x: x[0])
    return ranked[:top_k], total_evals


def solve_instance_v3(args):
    inst_id, pass_num, budget_sec, seed, existing_win_mk = args
    _set_mem_limit(4)
    t0 = time.time()
    ds = data.MMLibDataset()
    info = ds.meta(inst_id)
    I, X = ds.load_inst(inst_id)
    bks = ds.load_bks_schedule(inst_id)
    warm = bks is not None
    ub = info["ub"]
    target_ub = min(ub, existing_win_mk) if existing_win_mk is not None else ub

    best_mk = None
    best_m = None
    best_s = None
    best_meth = ""
    cp_tested = 0
    cp_improved = 0
    total_evals = 0

    if warm:
        m0, s0 = bks
        best_mk, best_m, best_s = int(s0[-1]), m0.copy(), s0.copy()
        init_sols = [(m0, s0)]
    else:
        init_sols = None

    # Pass 1 (90s): 1 meta trajectory -> top 8 fixed CP-SAT -> window compress
    # Pass 2 (180-240s): 2 independent meta trajectories -> top 10 fixed CP-SAT -> window compress
    n_meta_waves = 1 if pass_num == 1 else 2
    meta_total = budget_sec * (0.52 if pass_num == 1 else 0.56)
    all_cands = {}

    for w_idx in range(n_meta_waves):
        w_seed = seed + w_idx * 7919
        w_init = init_sols if w_idx == 0 else ([(best_m, best_s)] if best_m is not None else None)
        cands, ev = collect_diverse_modes_v3(
            X, time_budget=meta_total / n_meta_waves, seed=w_seed,
            init_solutions=w_init, top_k=10, n_sa_restarts=(2 if pass_num == 1 else 3)
        )
        total_evals += ev
        for mk, m, s in cands:
            key = bytes(m.astype(np.uint8).tobytes())
            if key not in all_cands or mk < all_cands[key][0]:
                all_cands[key] = (mk, m, s)
            if best_mk is None or mk < best_mk:
                best_mk, best_m, best_s = mk, m, s
                best_meth = f"v3p{pass_num}_{'warm' if warm else 'scratch'}_meta"

    top_cands = sorted(all_cands.values(), key=lambda x: x[0])[: (8 if pass_num == 1 else 10)]

    # Stage 2: Exact Fixed-Mode CP-SAT across top 8-10 distinct mode vectors!
    cp_per_cand = 5.5 if pass_num == 1 else 8.5
    cp_budget_end = t0 + budget_sec * 0.88
    for idx, (mk_c, m_c, s_c) in enumerate(top_cands):
        rem = cp_budget_end - time.time()
        if rem < 2.5:
            break
        H_try = (best_mk - 1) if best_mk is not None else (mk_c - 1)
        if H_try < info["lb"]:
            break
        sub_tl = min(rem, cp_per_cand)
        cp_tested += 1
        mk_cp, s_cp, st_name = hybrid_v2.solve_fixed_mode_cpsat(
            I, m_c, H=H_try, hint_starts=s_c, secs=sub_tl, workers=1, seed=seed + 2000 + idx * 17
        )
        if mk_cp is not None and (best_mk is None or mk_cp < best_mk):
            best_mk, best_m, best_s = mk_cp, m_c.copy(), s_cp
            cp_improved += 1
            best_meth = f"v3p{pass_num}_{'warm' if warm else 'scratch'}+fixed_cpsat"

    # Stage 3: Window Compression polish on best schedule found
    rem = budget_sec - (time.time() - t0)
    if best_m is not None and rem >= 4.0:
        mk_w, m_w, s_w, _ = window_compress.slide_compress(
            I, X, best_m, best_s, time_budget=rem, workers=1, seed=seed + 4000
        )
        if mk_w < best_mk:
            best_mk, best_m, best_s = mk_w, m_w, s_w
            best_meth = (best_meth or f"v3p{pass_num}") + "+win_compress"

    dt = round(time.time() - t0, 2)
    win_ok = False
    win_msg = ""
    if best_m is not None and best_s is not None and best_mk < target_ub:
        win_ok, chk_mk, win_msg = data.verify_and_save_win(
            ds, inst_id, I, best_m, best_s,
            warm_start=warm, seed=seed, method=best_meth or f"v3p{pass_num}", runtime_sec=dt
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
        "warm": warm,
        "pass": pass_num,
        "best_mk": best_mk,
        "gain": (ub - best_mk) if best_mk is not None else None,
        "new_win": win_ok,
        "win_msg": win_msg,
        "method": best_meth,
        "secs": dt,
        "evals": total_evals,
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


def build_campaign_queue(ds: data.MMLibDataset, existing_wins: dict):
    """Build ordered queue of (inst_id, start_pass, tag) per agreed priority order."""
    # Collect Wave 1-3 ties (gain=0) and near-misses (gain=-1)
    ties, near1 = set(), set()
    for lf in glob.glob(os.path.join(PHASEB_DIR, "logs", "hybrid_v2_*.json")):
        for rec in json.load(open(lf)):
            iid = rec["id"]
            if iid in existing_wins:
                continue
            if rec.get("gain") == 0:
                ties.add(iid)
            elif rec.get("gain") == -1:
                near1.add(iid)
    near1 -= ties

    queue = []
    seen = set()

    def add_item(iid, start_pass, tag):
        if iid not in seen:
            seen.add(iid)
            queue.append((iid, start_pass, tag))

    # Pool 1: 59 existing gain=0 ties -> straight to Pass 2 (180s-210s)
    ties_sorted = sorted(ties, key=lambda i: (-ds.meta(i)["act"], -ds.meta(i)["modes"], -(ds.meta(i)["ub"] - ds.meta(i)["lb"]), i))
    for iid in ties_sorted:
        add_item(iid, 2, "P1_ties")

    # Pool 2: 52 untouched ref=8 mid-OS (0.35..0.55) A=100 M>=6 gap 2..18 -> Pass 1 (90s) + auto Pass 2 (210s)
    p2 = []
    for i in ds.open_ids():
        if i in existing_wins or i in seen:
            continue
        r = ds.rows[i]
        os_val = float(r["OS"].replace(",", "."))
        m = ds.meta(i)
        if r.get("UB ref") == "8" and 0.35 <= os_val < 0.55 and m["act"] == 100 and m["modes"] >= 6 and 2 <= (m["ub"] - m["lb"]) <= 18:
            p2.append(m)
    p2.sort(key=lambda c: (c["rr"], -c["modes"], abs((c["ub"] - c["lb"]) - 7), c["id"]))
    for c in p2:
        add_item(c["id"], 1, "P2_ref8_midOS")

    # Pool 3: 59 existing gain=-1 near-misses -> Pass 2 (180s-210s)
    near1_sorted = sorted(near1, key=lambda i: (-ds.meta(i)["act"], -ds.meta(i)["modes"], -(ds.meta(i)["ub"] - ds.meta(i)["lb"]), i))
    for iid in near1_sorted:
        add_item(iid, 2, "P3_near1")

    # Pool 4: 104 untouched ref=7 (Tian 2026) low-OS (<0.35) A=100 M>=6 gap 2..18 -> Pass 1 (90s) + auto Pass 2
    p4 = []
    for i in ds.open_ids():
        if i in existing_wins or i in seen:
            continue
        r = ds.rows[i]
        os_val = float(r["OS"].replace(",", "."))
        m = ds.meta(i)
        if r.get("UB ref") == "7" and os_val < 0.35 and m["act"] == 100 and m["modes"] >= 6 and 2 <= (m["ub"] - m["lb"]) <= 18:
            p4.append(m)
    p4.sort(key=lambda c: (c["rr"], -c["modes"], -(c["ub"] - c["lb"]), c["id"]))
    for c in p4:
        add_item(c["id"], 1, "P4_ref7_lowOS")

    # Pool 5: 46 untouched ref=5 (CPO 2023) mid-OS (0.35..0.55) A=100 M>=6 gap 2..18
    p5 = []
    for i in ds.open_ids():
        if i in existing_wins or i in seen:
            continue
        r = ds.rows[i]
        os_val = float(r["OS"].replace(",", "."))
        m = ds.meta(i)
        if r.get("UB ref") == "5" and 0.35 <= os_val < 0.55 and m["act"] == 100 and m["modes"] >= 6 and 2 <= (m["ub"] - m["lb"]) <= 18:
            p5.append(m)
    p5.sort(key=lambda c: (c["rr"], -c["modes"], -(c["ub"] - c["lb"]), c["id"]))
    for c in p5:
        add_item(c["id"], 1, "P5_ref5_midOS")

    return queue


def main():
    duration_min = float(sys.argv[1]) if len(sys.argv) > 1 else 173.0
    n_workers = min(4, int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    pass1_sec = 90.0
    pass2_sec = 210.0

    t_start = time.time()
    deadline = t_start + duration_min * 60.0

    ds = data.MMLibDataset()
    existing_wins = load_existing_wins()

    # Warm up Numba cache once in main process before spawning workers
    I0, X0 = ds.load_inst(1)
    m0, s0 = ds.load_bks_schedule(1)
    topo0 = np.array(engine.topo(X0), dtype=np.int64)
    o0 = fast_meta.order_from_starts(s0, topo0)
    fast_meta.eval_both_sgs(o0, m0, X0.dur, X0.req, X0.cap, X0.pp, X0.pi, X0.sp, X0.si, X0.H, 10)
    fast_meta.run_sa_penalty(X0, m0, s0, time_budget=0.1, seed=1)

    queue = build_campaign_queue(ds, existing_wins)
    print(
        f"Hybrid v3 Campaign START: duration={duration_min:.1f}m, workers={n_workers}, "
        f"pass1={pass1_sec:.0f}s, pass2={pass2_sec:.0f}s, queue={len(queue)}, existing_wins={len(existing_wins)}",
        flush=True,
    )

    log_path = os.path.join(PHASEB_DIR, "logs", "hybrid_v3_campaign.jsonl")
    pending = list(queue)
    promoted = []  # Pass-2 promotions from Pass-1 near-misses
    seed_counter = 90000
    completed = 0
    new_wins = 0
    new_gain = 0

    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        active = {}  # future -> (iid, pass_num, tag)

        def submit_next():
            nonlocal seed_counter
            rem_wall = deadline - time.time()
            # Prefer promoted Pass-2 tasks if enough wall time remains
            if promoted and rem_wall >= pass2_sec + 30.0:
                iid, pnum, tag = promoted.pop(0)
            elif pending:
                iid, pnum, tag = pending[0]
                need = (pass2_sec if pnum == 2 else pass1_sec) + 30.0
                if rem_wall < need:
                    return False
                pending.pop(0)
            else:
                return False
            seed_counter += 1
            budget = pass2_sec if pnum == 2 else pass1_sec
            ex_mk = existing_wins.get(iid)
            fut = ex.submit(solve_instance_v3, (iid, pnum, budget, seed_counter, ex_mk))
            active[fut] = (iid, pnum, tag)
            return True

        # Fill initial worker slots
        for _ in range(n_workers):
            if not submit_next():
                break

        while active:
            # Wait for the next completed future
            done_fut = next(as_completed(active))
            iid, pnum, tag = active.pop(done_fut)
            try:
                r = done_fut.result()
            except Exception as exc:
                print(f"ERROR id={iid} p{pnum} ({tag}): {exc}", flush=True)
                submit_next()
                continue

            completed += 1
            r["pool"] = tag
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")

            if r["new_win"]:
                new_wins += 1
                new_gain += r["gain"]
                existing_wins[iid] = r["best_mk"]
                mark = "WIN!!!"
            else:
                mark = "      "

            # Auto-promote Pass 1 near-misses (gain >= -1, not yet won) to Pass 2!
            promo_str = ""
            if pnum == 1 and not r["new_win"] and r["gain"] is not None and r["gain"] >= -1:
                promoted.append((iid, 2, tag + "_P2"))
                promo_str = " [->P2]"

            elapsed_m = (time.time() - t_start) / 60.0
            print(
                f"{mark} [{elapsed_m:5.1f}m] {tag:<15s} p{pnum} id={r['id']:4d} {r['file']:<14s} "
                f"ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} LB={r['lb']:3d} UB={r['ub']:3d} -> "
                f"mk={str(r['best_mk']):>4s} (gain={str(r['gain']):>3s}) {r['secs']:5.1f}s "
                f"cp={r['cp_tested']:2d}/{r['cp_improved']} {r['method']}{promo_str}",
                flush=True,
            )

            # Submit next task if before deadline
            submit_next()

    print(
        f"\n=== HYBRID V3 CAMPAIGN COMPLETE ({(time.time() - t_start)/60.0:.1f}m wall) ===\n"
        f"Tasks completed: {completed} | NEW wins: {new_wins} | NEW gain: -{new_gain} pts | Total wins on disk: {len(existing_wins)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
