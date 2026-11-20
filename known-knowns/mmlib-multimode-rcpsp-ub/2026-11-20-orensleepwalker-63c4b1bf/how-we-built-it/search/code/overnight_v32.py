"""
Overnight MMLIB+ Campaign Runner (overnight_v32.py):
Combines our two battle-tested Phase B engines:
  - From-scratch (ref=8): hybrid_v3 (90s Pass 1 -> auto-promoted 210s Pass 2 on gain >= -1)
  - Warm-started (ref=1/5/7 & Pool 4 existing wins): hybrid_v3.2 (direct 140-240s, cpsat_mixes=5,
    2 independent Memetic+Multi-Temp Penalty SA waves, Dual-SGS, top-12 new-mode Fixed-Mode CP-SAT)

Execution order (highest EV first):
  1. Pool 4: 28 existing wins re-polish (warm-started directly from our own saved wins/*.json, 240s)
  2. Subpool 5A + 5B: 59 ref=8 from-scratch (42 mid-OS A=50 + 17 large-gap A=100)
  3. Pool 3: 119 low-OS A=50 M=6/9 (75 ref=7 + 44 ref=5, 150s)
  4. Subpools 5C, 5D, 5E, 5F, 5G: 298 remaining low/mid-OS (<0.55) instances
  5. Bandit probes: 15 random 5H (high-OS >=0.55) + 11 random 5I (gap=1 / other)
"""
import glob
import json
import os
import random
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
import hybrid_v3  # noqa: E402
import hybrid_v31_warm  # noqa: E402
import window_compress  # noqa: E402


def _set_mem_limit(gb: int = 4):
    limit = gb * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass


def load_best_wins_map():
    """Return {inst_id: (best_mk, json_path)} across all files in phaseB/wins/."""
    wins = {}
    for p in glob.glob(os.path.join(PHASEB_DIR, "wins", "*.json")):
        rec = json.load(open(p))
        iid = rec["id"]
        mk = int(rec["new_mk"])
        if iid not in wins or mk < wins[iid][0]:
            wins[iid] = (mk, p)
    return wins


def solve_warm_custom(args):
    """Run hybrid_v3.2 warm-start engine, optionally loading warm-start (m0, s0) from a saved win JSON."""
    inst_id, pool_tag, budget_sec, seed, existing_win_mk, win_json_path = args
    _set_mem_limit(4)
    t0 = time.time()
    ds = data.MMLibDataset()
    info = ds.meta(inst_id)
    I, X = ds.load_inst(inst_id)
    ub = info["ub"]

    if win_json_path is not None:
        rec_w = json.load(open(win_json_path))
        m0 = np.array(rec_w["modes"], dtype=np.int64)
        s0 = np.array(rec_w["starts"], dtype=np.int64)
        warm_flag = bool(rec_w.get("warm_start", False))
        target_ub = min(ub, int(rec_w["new_mk"]))
    else:
        bks = ds.load_bks_schedule(inst_id)
        assert bks is not None, f"Instance {inst_id} has no BKS schedule!"
        m0, s0 = bks[0].copy(), bks[1].copy()
        warm_flag = True
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

    new_cands = {}

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
            best_meth = "v32_repolish_meta" if win_json_path else "v32_warm_meta"
        if int(np.sum(m != m0)) >= 2:
            key = bytes(m.astype(np.uint8).tobytes())
            if key not in new_cands or mk < new_cands[key][0]:
                new_cands[key] = (int(mk), m.copy(), s.copy())

    # Stage 1: 2 Independent Memetic (cpsat_mixes=5) + Multi-Temp Penalty SA Waves (65% of budget)
    wave_budget = (budget_sec * 0.65) / 2.0
    for w_idx in range(2):
        w_seed = seed + w_idx * 7919
        init_sols = [(best_m, best_s)]
        for _ in range(8):
            m_pert = best_m.copy()
            k_mut = int(rng.integers(4, 16))
            for j in rng.choice(np.arange(1, X.n - 1), size=min(k_mut, X.n - 2), replace=False):
                m_pert[j] = int(rng.integers(1, X.nm[j] + 1))
            m_rep, ok = fast_meta.repair_modes_nr(m_pert, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
            if ok and int(np.sum(m_rep != m0)) >= 2:
                init_sols.append((m_rep, best_s))

        mk_m, m_m, s_m, st_m = fast_meta.memetic_search(
            X, time_budget=wave_budget * 0.55, seed=w_seed, init_solutions=init_sols[:7],
            pop_size=28, cpsat_mixes=5, cpsat_workers=1
        )
        total_evals += st_m.get("evals", 0)
        record_cand(mk_m, m_m, s_m)
        for mk_p, m_p, s_p in st_m.get("top_pop", []):
            record_cand(mk_p, m_p, s_p)

        sa_temps = [1.6, 4.0] if w_idx == 0 else [2.0, 5.0]
        per_sa = (wave_budget * 0.45) / len(sa_temps)
        for ti, t_val in enumerate(sa_temps):
            if ti == 0:
                sm, ss = best_m.copy(), best_s.copy()
            else:
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

    # Stage 2: Exact Fixed-Mode CP-SAT on top 12 genuinely NEW mode vectors
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
            best_meth = "v32_repolish+fixed_cpsat" if win_json_path else "v32_warm+fixed_cpsat"

    # Stage 3: Window Compression ONLY if best_m != m0
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
            warm_start=warm_flag, seed=seed, method=best_meth or "v32_warm", runtime_sec=dt
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
        "target_ub": target_ub,
        "warm": True,
        "pass": 2,
        "best_mk": best_mk,
        "gain": ub - best_mk,
        "delta_vs_target": target_ub - best_mk,
        "new_win": win_ok,
        "win_msg": win_msg,
        "method": best_meth,
        "secs": dt,
        "cp_tested": cp_tested,
        "cp_improved": cp_improved,
    }


def build_overnight_queue(ds: data.MMLibDataset, wins_map: dict):
    """Build ordered list of (inst_id, pool_tag, engine_kind, budget_sec, win_json_path)."""
    won_ids = set(wins_map.keys())
    queue = []
    seen = set()

    def add(iid, tag, kind, budget, wpath=None):
        if iid not in seen:
            seen.add(iid)
            queue.append((iid, tag, kind, budget, wpath))

    # 1. Pool 4: Re-polish all 28 existing wins (240s, warm-started from our saved win JSON!)
    for iid in sorted(wins_map.keys(), key=lambda i: -(wins_map[i][0] - ds.meta(i)["lb"])):
        mk_cur, wpath = wins_map[iid]
        if mk_cur > ds.meta(iid)["lb"]:
            add(iid, "P4_repolish", "warm_v32", 240.0, wpath)

    # Classify all remaining open instances (not yet won)
    p3 = []
    s5a, s5b, s5c, s5d, s5e, s5f, s5g, s5h, s5i = [], [], [], [], [], [], [], [], []
    for i in ds.open_ids():
        if i in won_ids:
            continue
        r = ds.rows[i]
        ref = r.get("UB ref")
        os_val = float(r["OS"].replace(",", "."))
        m = ds.meta(i)
        gap = m["ub"] - m["lb"]
        act, modes = m["act"], m["modes"]

        is_p1 = (ref == "7" and os_val < 0.35 and act == 100 and modes >= 6 and 2 <= gap <= 18)
        is_p2 = (ref == "5" and 0.35 <= os_val < 0.55 and act == 100 and modes >= 6 and 2 <= gap <= 18)
        is_p3 = (ref in ("5", "7") and os_val < 0.35 and act == 50 and modes >= 6 and 3 <= gap <= 18)
        if is_p1 or is_p2:
            continue
        if is_p3:
            p3.append(m)
            continue

        if ref == "8" and 0.35 <= os_val < 0.55 and act == 50 and modes >= 6 and 3 <= gap <= 18:
            s5a.append(m)
        elif ref == "8" and os_val < 0.55 and act == 100 and modes >= 6 and gap > 18:
            s5b.append(m)
        elif ref == "7" and 0.35 <= os_val < 0.55 and act == 100 and modes >= 6 and 2 <= gap <= 18:
            s5c.append(m)
        elif ref == "5" and 0.35 <= os_val < 0.55 and act == 50 and modes >= 6 and 3 <= gap <= 18:
            s5d.append(m)
        elif ref == "7" and 0.35 <= os_val < 0.55 and act == 50 and modes >= 6 and 3 <= gap <= 18:
            s5e.append(m)
        elif ref == "8" and os_val < 0.55 and modes == 3 and gap >= 2:
            s5f.append(m)
        elif ref == "1" and os_val < 0.55 and gap >= 2:
            s5g.append(m)
        elif os_val >= 0.55 and modes >= 6 and gap >= 3:
            s5h.append(m)
        else:
            s5i.append(m)

    # 2. Subpool 5A (42) + 5B (17): ref=8 from-scratch -> hybrid_v3 (90s P1 -> auto 210s P2)
    s5a.sort(key=lambda c: (-c["modes"], c["rr"], abs((c["ub"] - c["lb"]) - 8), c["id"]))
    for c in s5a:
        add(c["id"], "5A_ref8_midOS50", "scratch_v3", 90.0)
    s5b.sort(key=lambda c: (-c["modes"], c["rr"], c["ub"] - c["lb"], c["id"]))
    for c in s5b:
        add(c["id"], "5B_ref8_bigGap100", "scratch_v3", 90.0)

    # 3. Pool 3 (119): low-OS A=50 M=6/9 (ref=5/7) -> warm_v32 (140s direct)
    p3.sort(key=lambda c: (-c["modes"], 0 if c["ub_ref"] == "5" else 1, c["rr"], -(c["ub"] - c["lb"]), c["id"]))
    for c in p3:
        add(c["id"], "P3_lowOS50", "warm_v32", 140.0)

    # 4. Subpools 5F (33 ref=8 M=3), 5G (42 ref=1 2011), 5D (41 ref=5 A=50), 5E (69 ref=7 A=50), 5C (113 ref=7 A=100)
    s5f.sort(key=lambda c: (-c["act"], c["rr"], -(c["ub"] - c["lb"]), c["id"]))
    for c in s5f:
        add(c["id"], "5F_ref8_M3", "scratch_v3", 90.0)

    s5g.sort(key=lambda c: (-c["act"], -c["modes"], -(c["ub"] - c["lb"]), c["id"]))
    for c in s5g:
        add(c["id"], "5G_ref1_2011", "warm_v32", 150.0)

    s5d.sort(key=lambda c: (-c["modes"], c["rr"], -(c["ub"] - c["lb"]), c["id"]))
    for c in s5d:
        add(c["id"], "5D_ref5_midOS50", "warm_v32", 130.0)

    s5e.sort(key=lambda c: (-c["modes"], c["rr"], -(c["ub"] - c["lb"]), c["id"]))
    for c in s5e:
        add(c["id"], "5E_ref7_midOS50", "warm_v32", 130.0)

    s5c.sort(key=lambda c: (-c["modes"], c["rr"], -(c["ub"] - c["lb"]), c["id"]))
    for c in s5c:
        add(c["id"], "5C_ref7_midOS100", "warm_v32", 180.0)

    # 5. Bandit probes: 15 random from 5H + 11 random from 5I (deterministic seed)
    py_rng = random.Random(20261120)
    h_picks = py_rng.sample(s5h, min(15, len(s5h)))
    for c in h_picks:
        kind = "warm_v32" if c["has_bks"] else "scratch_v3"
        add(c["id"], "5H_probe15", kind, 150.0 if kind == "warm_v32" else 90.0)

    i_picks = py_rng.sample(s5i, min(11, len(s5i)))
    for c in i_picks:
        kind = "warm_v32" if c["has_bks"] else "scratch_v3"
        add(c["id"], "5I_probe11", kind, 140.0 if kind == "warm_v32" else 90.0)

    return queue


def main():
    n_workers = min(4, int(sys.argv[1]) if len(sys.argv) > 1 else 4)
    ds = data.MMLibDataset()
    wins_map = load_best_wins_map()

    # Warmup Numba cache once in main process
    I0, X0 = ds.load_inst(1)
    m0, s0 = ds.load_bks_schedule(1)
    topo0 = np.array(engine.topo(X0), dtype=np.int64)
    o0 = fast_meta.order_from_starts(s0, topo0)
    fast_meta.eval_both_sgs(o0, m0, X0.dur, X0.req, X0.cap, X0.pp, X0.pi, X0.sp, X0.si, X0.H, 10)
    fast_meta.run_sa_penalty(X0, m0, s0, time_budget=0.1, seed=1)

    queue = build_overnight_queue(ds, wins_map)
    from collections import Counter
    pool_counts = Counter(t for _, t, _, _, _ in queue)
    print(f"Overnight v3.2 Campaign START: {len(queue)} tasks, workers={n_workers}, existing_wins={len(wins_map)}", flush=True)
    for k, v in pool_counts.items():
        print(f"  {k:<20s}: {v}", flush=True)

    log_path = os.path.join(PHASEB_DIR, "logs", "overnight_v32.jsonl")
    t_start = time.time()
    pending = list(queue)
    promoted = []  # Pass-2 promotions for scratch_v3 near-misses
    seed_counter = 200000
    done = 0
    new_wins = 0
    repolish_wins = 0
    total_gain = 0

    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        active = {}

        def submit_next():
            nonlocal seed_counter
            if promoted:
                iid, tag, kind, budget, wpath = promoted.pop(0)
            elif pending:
                iid, tag, kind, budget, wpath = pending.pop(0)
            else:
                return False
            seed_counter += 1
            ex_mk = wins_map[iid][0] if iid in wins_map else None
            if kind == "warm_v32":
                fut = ex.submit(solve_warm_custom, (iid, tag, budget, seed_counter, ex_mk, wpath))
            elif kind == "scratch_v3":
                fut = ex.submit(hybrid_v3.solve_instance_v3, (iid, 1, budget, seed_counter, ex_mk))
            else:  # scratch_v3_p2
                fut = ex.submit(hybrid_v3.solve_instance_v3, (iid, 2, 210.0, seed_counter, ex_mk))
            active[fut] = (iid, tag, kind)
            return True

        for _ in range(n_workers):
            if not submit_next():
                break

        while active:
            done_fut = next(as_completed(active))
            iid, tag, kind = active.pop(done_fut)
            try:
                r = done_fut.result()
            except Exception as exc:
                print(f"ERROR id={iid} ({tag}, {kind}): {exc}", flush=True)
                submit_next()
                continue

            done += 1
            r["pool"] = tag
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")

            if r.get("new_win"):
                if tag == "P4_repolish":
                    repolish_wins += 1
                    total_gain += r.get("delta_vs_target", 1)
                else:
                    new_wins += 1
                    total_gain += r.get("gain", 1)
                wins_map[iid] = (r["best_mk"], r.get("win_msg", ""))
                mark = "WIN!!!"
            else:
                mark = "      "

            promo_str = ""
            if kind == "scratch_v3" and not r.get("new_win") and r.get("gain") is not None and r["gain"] >= -1:
                promoted.append((iid, tag + "_P2", "scratch_v3_p2", 210.0, None))
                promo_str = " [->P2]"

            elapsed_m = (time.time() - t_start) / 60.0
            print(
                f"{mark} [{elapsed_m:5.1f}m] ({done:3d}) {tag:<19s} id={r['id']:4d} {r['file']:<14s} "
                f"ref={r['ub_ref']} A={r['act']:3d} M={r['modes']} LB={r['lb']:3d} UB={r['ub']:3d} -> "
                f"mk={str(r['best_mk']):>4s} (gain={str(r['gain']):>3s}) {r['secs']:5.1f}s "
                f"cp={r['cp_tested']:2d}/{r['cp_improved']} {r['method']}{promo_str}",
                flush=True,
            )
            submit_next()

    print(
        f"\n=== OVERNIGHT V3.2 COMPLETE ({(time.time() - t_start)/60.0:.1f}m wall) ===\n"
        f"Tasks done: {done} | NEW instances beaten: {new_wins} | Existing wins improved further: {repolish_wins} | Extra pts gained: -{total_gain} | Total unique wins on disk: {len(wins_map)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
