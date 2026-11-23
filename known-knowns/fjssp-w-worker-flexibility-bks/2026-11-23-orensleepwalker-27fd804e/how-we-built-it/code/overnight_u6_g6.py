"""
7-Hour Hard-Capped Overnight Chain (overnight_u6_g6.py):
Sequential 6-step campaign on the 12 remaining open FJSSP-W instances:
  1. U_S1_60m     : U1-U6 (6 insts), 60m CP-SAT (H = true_bar - 1)
  2. U_S2_90m     : U survivors, 90m CP-SAT
  3. U_S3_120m    : U survivors, 120m CP-SAT
  4. G_S4_pilot   : G2 (Behnke17) + G6 (Behnke60), 15m Mode-Pruned CP-SAT
  5. G_S5_sweep   : G1, G3, G4, G5 (if Step 4 passes), 15m Mode-Pruned CP-SAT
  6. G_S6_polish  : Qualifying non-winning G survivors (<= +8 gap & beat prev_best), 30m wider pruning

NO Telegram notifications. Hard wall-clock cap at 7h (25,140s); clamps wave budgets
and exits cleanly if remaining time < 120s. Saves wins to wins_extra2/.
DOES NOT modify best_wins/, best_wins_manifest.json, wins_extra/, or wins_extra_manifest.json.
"""
import argparse
import csv
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

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
INST_DIR = os.path.join(BASE, "runs/2026-11-11-2301/data/repo/instances/Example_Instances_FJSSP-WF")
CSV_PATH = os.path.join(BASE, "runs/2026-11-12-1955/data/best_known_live.csv")
CATALOG_PATH = os.path.join(OUT_DIR, "true_bar_catalog.json")
PR868_PATH = os.path.join(BASE, "scans/final_91_records.json")
WINS_EXTRA2_DIR = os.path.join(OUT_DIR, "wins_extra2")
LOGS_DIR = os.path.join(OUT_DIR, "logs")

HARD_CAP_S = 7 * 3600 - 60  # 25,140s = 419m hard ceiling

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)

import fjsspw  # noqa: E402
from ortools.sat.python import cp_model  # noqa: E402
from play2_cpsat_snipe import (  # noqa: E402
    FirstWinStopCallback,
    _build_snipe_model,
    _configure_solver,
    _extract_sched,
)

U_SPECS = [
    ("U1", "Hurinkrdata16"),
    ("U2", "BrandimarteMk2"),
    ("U3", "Hurinkrdata35"),
    ("U4", "Hurinkvdata24"),
    ("U5", "Hurinkvdata30"),
    ("U6", "Behnke14"),
]

G_SPECS = [
    ("G1", "Behnke16", 437),
    ("G2", "Behnke17", 419),
    ("G3", "Behnke18", 426),
    ("G4", "Behnke19", 434),
    ("G5", "Behnke20", 426),
    ("G6", "Behnke60", 394),
]


class WinBelowBarCallback(cp_model.CpSolverSolutionCallback):
    """Stop search immediately once makespan strictly beats target_bar; otherwise let CP-SAT minimize."""

    def __init__(self, mk_var, target_bar):
        super().__init__()
        self._mk_var = mk_var
        self._target_bar = int(target_bar)
        self.best_cb_mk = None

    def on_solution_callback(self):
        v = int(self.Value(self._mk_var))
        if self.best_cb_mk is None or v < self.best_cb_mk:
            self.best_cb_mk = v
        if v < self._target_bar:
            self.StopSearch()


def build_targets(include_u=True):
    """Assemble U1..U6 (if include_u) and G1..G6 and assert zero claim overlap across all prior sets."""
    rounded_ub, rounded_lb = {}, {}
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f, delimiter=";"):
            k = r["Instance"].strip().lower()
            rounded_ub[k] = int(round(float(r["UB"])))
            rounded_lb[k] = int(round(float(r["LB"])))

    cat = json.load(open(CATALOG_PATH))
    by_name = {v["fjs"][:-4]: v for v in cat.values()}
    pr868_all = {r["instance"].lower().replace(".fjs", "") for r in json.load(open(PR868_PATH))}
    filed_1081 = {
        os.path.basename(p).replace(".json", "").lower()
        for p in glob.glob(os.path.join(BASE, "runs/2026-11-13-0112/claim/object/*.json"))
    }
    won_best = {x["inst"].lower() for x in json.load(open(os.path.join(OUT_DIR, "best_wins_manifest.json")))}
    won_extra = {x["inst"].lower() for x in json.load(open(os.path.join(OUT_DIR, "wins_extra_manifest.json")))}
    won_extra2 = {
        os.path.basename(p).split("_mk")[0].lower()
        for p in glob.glob(os.path.join(WINS_EXTRA2_DIR, "*.json"))
    }

    def check_clean(name):
        r = by_name[name]
        k = r["inst"].lower()
        stem = r["fjs"].replace(".fjs", "").lower()
        assert stem == name.lower(), f"Stem mismatch {k}: {stem} vs {name}"
        assert not r["is_opt"] and rounded_lb[k] < rounded_ub[k], f"Already opt: {k}"
        assert not r["is_filed"], f"Already filed: {k}"
        assert k not in pr868_all and stem not in pr868_all, f"Overlap PR868: {k}"
        assert k not in filed_1081 and stem not in filed_1081, f"Overlap PR1081: {k}"
        assert k not in won_best and stem not in won_best, f"Overlap best_wins: {k}"
        assert k not in won_extra and stem not in won_extra, f"Overlap wins_extra: {k}"
        assert k not in won_extra2 and stem not in won_extra2, f"Overlap wins_extra2: {k}"
        fp = os.path.join(INST_DIR, r["fjs"])
        assert os.path.isfile(fp), f"Missing .fjs: {fp}"
        cb = r.get("comp_best")
        rub = rounded_ub[k]
        return dict(
            inst=r["inst"],
            name=name,
            fjs=r["fjs"],
            lb=rounded_lb[k],
            table_ub=rub,
            true_bar=min(rub, int(cb)) if cb is not None else rub,
            size_bytes=r["size_bytes"],
            kb=r["size_bytes"] // 1024,
        )

    u_targets = []
    if include_u:
        for lbl, nm in U_SPECS:
            rec = check_clean(nm)
            rec["label"] = lbl
            rec["mem_gb"] = 6 if rec["kb"] > 100 else 4
            u_targets.append(rec)

    g_targets = []
    for lbl, nm, prev_best in G_SPECS:
        rec = check_clean(nm)
        rec["label"] = lbl
        rec["prev_best"] = prev_best
        rec["mem_gb"] = 6
        g_targets.append(rec)

    return u_targets, g_targets


def prune_jobs(jobs, max_per_m=2, max_total=20, hard_cap=25):
    """
    Prune per-op (machine, worker) -> duration dicts:
    1. Keep fastest 1 worker per eligible machine so every machine stays represented
       (if > hard_cap machines exist on an op, keep the hard_cap fastest machines).
    2. Fill remaining slots up to max_total with the fastest 2nd..max_per_m-th workers per machine.
    Returns (pruned_jobs, stats_dict).
    """
    pruned = []
    raw_modes = 0
    kept_modes = 0
    max_op_modes = 0
    for ops in jobs:
        new_ops = []
        for alt in ops:
            raw_modes += len(alt)
            by_m = {}
            for (mm, ww), dur in alt.items():
                by_m.setdefault(mm, []).append((int(dur), int(ww), int(mm)))
            firsts = []
            extras = []
            for mm, items in by_m.items():
                items.sort()
                firsts.append(items[0])
                for it in items[1:max_per_m]:
                    extras.append(it)
            firsts.sort()
            extras.sort()
            if len(firsts) >= max_total:
                chosen = firsts[: min(len(firsts), hard_cap)]
            else:
                chosen = list(firsts) + extras[: max_total - len(firsts)]
            new_alt = {(mm, ww): dur for dur, ww, mm in chosen}
            new_ops.append(new_alt)
            kept_modes += len(new_alt)
            if len(new_alt) > max_op_modes:
                max_op_modes = len(new_alt)
        pruned.append(new_ops)
    return pruned, dict(raw_modes=raw_modes, kept_modes=kept_modes, max_op_modes=max_op_modes)


def _apply_rlimit(mem_gb):
    lim = int(mem_gb) * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass


def solve_u_one(task):
    """CP-SAT deadline snipe for U1-U6 (H = true_bar - 1)."""
    _apply_rlimit(task["mem_gb"])
    t0 = time.time()
    rec = task["rec"]
    stage = task["stage"]
    budget_s = float(task["budget_s"])
    threads = int(task["threads"])
    seed = int(task["seed"])

    fjs_path = os.path.join(INST_DIR, rec["fjs"])
    inst_name = rec["name"]
    true_bar = int(rec["true_bar"])
    table_ub = int(rec["table_ub"])

    J, M, W, jobs = fjsspw.parse(fjs_path)
    H = true_bar - 1
    m, _, S, B = _build_snipe_model(J, M, W, jobs, H)
    sv = _configure_solver(budget_s, threads, seed)
    st = sv.Solve(m, FirstWinStopCallback())

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        best_sched = _extract_sched(inst_name, jobs, S, B, sv)
        ok, cmk, errs = fjsspw.check(fjs_path, best_sched)
        assert ok and cmk <= H, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} H={H} errs={errs[:3]}"
        best_mk = int(cmk)
        final_status = sv.StatusName(st)

        rem_s = budget_s - (time.time() - t0)
        if st != cp_model.OPTIMAL and best_mk > int(rec["lb"]) and rem_s > 2.0:
            m2, _, S2, B2 = _build_snipe_model(J, M, W, jobs, best_mk - 1)
            sv2 = _configure_solver(min(15.0, rem_s), threads, seed + 7)
            st2 = sv2.Solve(m2)
            if st2 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                s2 = _extract_sched(inst_name, jobs, S2, B2, sv2)
                ok2, cmk2, errs2 = fjsspw.check(fjs_path, s2)
                assert ok2 and cmk2 <= best_mk - 1, f"Checker FAIL2 {inst_name}: ok={ok2} cmk={cmk2}"
                best_sched = s2
                best_mk = int(cmk2)
                final_status = sv2.StatusName(st2)

        os.makedirs(WINS_EXTRA2_DIR, exist_ok=True)
        win_path = os.path.join(WINS_EXTRA2_DIR, f"{inst_name}_mk{best_mk}_bar{true_bar}.json")
        with open(win_path, "w") as wf:
            json.dump(best_sched, wf)

        return dict(
            stage=stage, label=rec["label"], inst=rec["inst"], name=inst_name,
            lb=int(rec["lb"]), table_ub=table_ub, true_bar=true_bar,
            mk=best_mk, vs_bar=best_mk - true_bar, vs_table=best_mk - table_ub,
            beats_bar=True, outcome="WIN", cpsat_status=final_status,
            seed=seed, secs=round(time.time() - t0, 2), win_path=win_path,
        )

    outcome = "PROVED_OPTIMAL_AT_BAR" if st == cp_model.INFEASIBLE else sv.StatusName(st)
    return dict(
        stage=stage, label=rec["label"], inst=rec["inst"], name=inst_name,
        lb=int(rec["lb"]), table_ub=table_ub, true_bar=true_bar,
        mk=None, vs_bar=None, vs_table=None, beats_bar=False,
        outcome=outcome, cpsat_status=sv.StatusName(st),
        seed=seed, secs=round(time.time() - t0, 2), win_path=None,
    )


def solve_g_one(task):
    """Attack 1 Mode-Pruned CP-SAT (minimize mk <= upper_cap - 1, stop early if < true_bar)."""
    _apply_rlimit(task["mem_gb"])
    t0 = time.time()
    rec = task["rec"]
    stage = task["stage"]
    budget_s = float(task["budget_s"])
    threads = int(task["threads"])
    seed = int(task["seed"])
    max_per_m = int(task["max_per_m"])
    max_total = int(task["max_total"])
    hard_cap = int(task["hard_cap"])
    upper_cap = int(task["upper_cap"])

    fjs_path = os.path.join(INST_DIR, rec["fjs"])
    inst_name = rec["name"]
    true_bar = int(rec["true_bar"])
    table_ub = int(rec["table_ub"])

    J, M, W, jobs = fjsspw.parse(fjs_path)
    pjobs, pstats = prune_jobs(jobs, max_per_m=max_per_m, max_total=max_total, hard_cap=hard_cap)

    H = upper_cap - 1
    m, mk_var, S, B = _build_snipe_model(J, M, W, pjobs, H)
    sv = _configure_solver(budget_s, threads, seed)
    cb = WinBelowBarCallback(mk_var, true_bar)
    st = sv.Solve(m, cb)

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        best_sched = _extract_sched(inst_name, pjobs, S, B, sv)
        ok, cmk, errs = fjsspw.check(fjs_path, best_sched)
        assert ok and cmk <= H, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} H={H} errs={errs[:3]}"
        best_mk = int(cmk)
        final_status = sv.StatusName(st)
        try:
            best_bound = int(round(sv.BestObjectiveBound()))
        except Exception:
            best_bound = None

        if best_mk < true_bar:
            rem_s = budget_s - (time.time() - t0)
            if st != cp_model.OPTIMAL and best_mk > int(rec["lb"]) and rem_s > 2.0:
                m2, _, S2, B2 = _build_snipe_model(J, M, W, pjobs, best_mk - 1)
                sv2 = _configure_solver(min(15.0, rem_s), threads, seed + 7)
                st2 = sv2.Solve(m2)
                if st2 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                    s2 = _extract_sched(inst_name, pjobs, S2, B2, sv2)
                    ok2, cmk2, errs2 = fjsspw.check(fjs_path, s2)
                    assert ok2 and cmk2 <= best_mk - 1, f"Checker FAIL2 {inst_name}: ok={ok2} cmk={cmk2}"
                    best_sched = s2
                    best_mk = int(cmk2)
                    final_status = sv2.StatusName(st2)

            os.makedirs(WINS_EXTRA2_DIR, exist_ok=True)
            win_path = os.path.join(WINS_EXTRA2_DIR, f"{inst_name}_mk{best_mk}_bar{true_bar}.json")
            with open(win_path, "w") as wf:
                json.dump(best_sched, wf)
            outcome = "WIN"
            beats_bar = True
        else:
            win_path = None
            outcome = "IMPROVED_NO_WIN"
            beats_bar = False

        return dict(
            stage=stage, label=rec["label"], inst=rec["inst"], name=inst_name,
            lb=int(rec["lb"]), table_ub=table_ub, true_bar=true_bar,
            prev_best=rec["prev_best"], upper_cap=upper_cap,
            mk=best_mk, vs_bar=best_mk - true_bar, vs_table=best_mk - table_ub,
            vs_prev=best_mk - rec["prev_best"], best_bound=best_bound,
            beats_bar=beats_bar, outcome=outcome, cpsat_status=final_status,
            kept_modes=pstats["kept_modes"], max_op_modes=pstats["max_op_modes"],
            seed=seed, secs=round(time.time() - t0, 2), win_path=win_path,
        )

    outcome = "INFEASIBLE_PRUNED" if st == cp_model.INFEASIBLE else sv.StatusName(st)
    return dict(
        stage=stage, label=rec["label"], inst=rec["inst"], name=inst_name,
        lb=int(rec["lb"]), table_ub=table_ub, true_bar=true_bar,
        prev_best=rec["prev_best"], upper_cap=upper_cap,
        mk=None, vs_bar=None, vs_table=None, vs_prev=None, best_bound=None,
        beats_bar=False, outcome=outcome, cpsat_status=sv.StatusName(st),
        kept_modes=pstats["kept_modes"], max_op_modes=pstats["max_op_modes"],
        seed=seed, secs=round(time.time() - t0, 2), win_path=None,
    )


def run_waves(stage_name, fn, tasks, max_workers, deadline, log_path):
    """Run tasks in explicit waves of <= max_workers, clamping wave budget to remaining deadline."""
    all_res = []
    stopped_cap = False
    for w0 in range(0, len(tasks), max_workers):
        rem_s = deadline - time.time()
        if rem_s < 120.0:
            stopped_cap = True
            print(f"  [CAP] Only {rem_s:.1f}s left before 7h hard cap; stopping before {stage_name} wave.", flush=True)
            break
        batch = tasks[w0 : w0 + max_workers]
        for t in batch:
            t["budget_s"] = min(float(t["budget_s"]), max(60.0, rem_s - 20.0))
        eff_b = int(batch[0]["budget_s"])
        print(
            f"  -- Wave {w0 // max_workers + 1}: {[t['rec']['label'] + ':' + t['rec']['name'] for t in batch]} ({eff_b}s budget, {len(batch)}w x {batch[0]['threads']}t) --",
            flush=True,
        )
        with ProcessPoolExecutor(max_workers=len(batch)) as ex:
            futs = [ex.submit(fn, t) for t in batch]
            for fut in as_completed(futs):
                res = fut.result()
                all_res.append(res)
                with open(log_path, "a") as lf:
                    lf.write(json.dumps(res) + "\n")
                if res["outcome"] == "WIN":
                    print(
                        f"    [{res['label']} {res['name']:15s}] WIN! mk={res['mk']} < bar={res['true_bar']} ({res['vs_bar']:+d}) | {res['secs']}s",
                        flush=True,
                    )
                elif res["outcome"] == "IMPROVED_NO_WIN":
                    print(
                        f"    [{res['label']} {res['name']:15s}] IMPROVED mk={res['mk']} (was {res['prev_best']}, bar={res['true_bar']}, gap={res['vs_bar']:+d}) | {res['secs']}s",
                        flush=True,
                    )
                else:
                    print(
                        f"    [{res['label']} {res['name']:15s}] {res['outcome']} (bar={res['true_bar']}) | {res['secs']}s",
                        flush=True,
                    )
    return all_res, stopped_cap


def main():
    parser = argparse.ArgumentParser(description="7-hour hard-capped overnight U1-U6 + G1-G6 chain")
    parser.add_argument("--dry-run", action="store_true", help="Verify targets, pruned modes, and exit")
    parser.add_argument("--step4-only", action="store_true", help="Run ONLY Step 4 (G_S4_pilot_15m on G2 + G6)")
    args = parser.parse_args()

    u_targets, g_targets = build_targets(include_u=not args.step4_only)
    if args.dry_run:
        print("DRY RUN OK: 12 targets (0 overlap with best_wins / wins_extra / PR868 / PR1081)")
        print("U1-U6 (CP-SAT 60m -> 90m -> 120m):")
        for t in u_targets:
            print(f"  {t['label']} {t['name']:15s} | {t['kb']:4d} KB | bar={t['true_bar']:4d} | lb={t['lb']:4d} | mem={t['mem_gb']}GB")
        print("G1-G6 (Attack 1 Mode-Pruned CP-SAT, max_per_m=2, max_total=20, hard_cap=25):")
        for t in g_targets:
            _, _, _, jobs = fjsspw.parse(os.path.join(INST_DIR, t["fjs"]))
            _, st = prune_jobs(jobs, max_per_m=2, max_total=20, hard_cap=25)
            ratio = st["raw_modes"] / max(1, st["kept_modes"])
            print(
                f"  {t['label']} {t['name']:15s} | {t['kb']:4d} KB | bar={t['true_bar']:4d} | prev={t['prev_best']:4d} (+{t['prev_best']-t['true_bar']}) | modes {st['raw_modes']:6d}->{st['kept_modes']:5d} ({ratio:4.1f}x, max/op={st['max_op_modes']})"
            )
        return

    os.makedirs(LOGS_DIR, exist_ok=True)
    if args.step4_only:
        s4_log = os.path.join(LOGS_DIR, "g_s4_pilot_15m.jsonl")
        with open(s4_log, "w"):
            pass
        t0 = time.time()
        g_by_label = {g["label"]: g for g in g_targets}
        p_recs = [g_by_label["G2"], g_by_label["G6"]]
        p_tasks = [
            dict(
                stage="G_S4_pilot_15m", rec=r, budget_s=900.0, threads=3, mem_gb=6,
                max_per_m=2, max_total=20, hard_cap=25, upper_cap=r["prev_best"],
                seed=6100 + i,
            )
            for i, r in enumerate(p_recs)
        ]
        print("=== STEP 4 ONLY: G_S4_pilot_15m (G2 Behnke17 + G6 Behnke60, 900s, 2w x 3t, 6GB) ===", flush=True)
        p_res, _ = run_waves("G_S4_pilot_15m", solve_g_one, p_tasks, 2, t0 + 3600.0, s4_log)
        pilot_passed = False
        for r in p_res:
            if (
                r["beats_bar"]
                or (r["name"] == "Behnke17" and r["mk"] is not None and r["mk"] <= 410)
                or (r["name"] == "Behnke60" and r["mk"] is not None and r["mk"] <= 382)
            ):
                pilot_passed = True
        wall_m = round((time.time() - t0) / 60.0, 2)
        out_summary = dict(
            wall_m=wall_m,
            pilot_passed=pilot_passed,
            results=p_res,
        )
        print("\n=== STEP 4 PILOT SUMMARY ===", flush=True)
        print(json.dumps(out_summary, indent=2), flush=True)
        return
    log_path = os.path.join(LOGS_DIR, "overnight_u6_g6.jsonl")
    with open(log_path, "w"):
        pass

    t0 = time.time()
    deadline = t0 + HARD_CAP_S
    stopped_at_cap = False
    stopped_reason = None

    print(f"START overnight_u6_g6.py | Hard cap = {HARD_CAP_S/3600:.2f}h ({HARD_CAP_S}s)", flush=True)

    # --- STEPS 1-3: U1-U6 (60m -> 90m -> 120m) ---
    u_remaining = sorted(u_targets, key=lambda r: (-r["kb"], r["name"]))
    u_wins = []
    u_proved = []
    for s_idx, (s_name, budget_s) in enumerate([("U_S1_60m", 3600.0), ("U_S2_90m", 5400.0), ("U_S3_120m", 7200.0)], 1):
        if not u_remaining:
            print(f"\nNo U survivors before {s_name}; moving on.", flush=True)
            break
        rem_s = deadline - time.time()
        if rem_s < 120.0:
            stopped_at_cap = True
            stopped_reason = f"before {s_name}"
            break
        print(f"\n=== STEP {s_idx}: {s_name} ({len(u_remaining)} insts, {int(budget_s)}s budget, rem_cap={rem_s/60:.1f}m) ===", flush=True)
        tasks = [
            dict(
                stage=s_name, rec=r, budget_s=budget_s, threads=2, mem_gb=r["mem_gb"],
                seed=5000 + s_idx * 100 + i,
            )
            for i, r in enumerate(u_remaining)
        ]
        res, hit_cap = run_waves(s_name, solve_u_one, tasks, 3, deadline, log_path)
        done_by_name = {r["name"]: r for r in res}
        next_u = []
        for r in u_remaining:
            out = done_by_name.get(r["name"])
            if out is None:
                next_u.append(r)  # didn't start due to cap
            elif out["outcome"] == "WIN":
                u_wins.append(out)
            elif out["outcome"] == "PROVED_OPTIMAL_AT_BAR":
                u_proved.append(out)
            else:
                next_u.append(r)
        u_remaining = next_u
        if hit_cap:
            stopped_at_cap = True
            stopped_reason = f"during {s_name}"
            break

    # --- STEPS 4-6: G1-G6 Attack 1 Mode-Pruned CP-SAT ---
    g_by_label = {g["label"]: g for g in g_targets}
    g_best_seen = {g["name"]: g["prev_best"] for g in g_targets}
    g_wins = []
    g_results = []
    pilot_passed = False
    sweep_ran = False

    if not stopped_at_cap:
        rem_s = deadline - time.time()
        if rem_s < 120.0:
            stopped_at_cap = True
            stopped_reason = "before Step 4 G_S4_pilot_15m"
        else:
            # Step 4: 15m Pilot on G2 + G6
            print(f"\n=== STEP 4: G_S4_pilot_15m (G2 Behnke17 + G6 Behnke60, rem_cap={rem_s/60:.1f}m) ===", flush=True)
            p_recs = [g_by_label["G2"], g_by_label["G6"]]
            p_tasks = [
                dict(
                    stage="G_S4_pilot_15m", rec=r, budget_s=900.0, threads=3, mem_gb=6,
                    max_per_m=2, max_total=20, hard_cap=25, upper_cap=g_best_seen[r["name"]],
                    seed=6100 + i,
                )
                for i, r in enumerate(p_recs)
            ]
            p_res, hit_cap = run_waves("G_S4_pilot_15m", solve_g_one, p_tasks, 2, deadline, log_path)
            g_results.extend(p_res)
            for r in p_res:
                if r["mk"] is not None and r["mk"] < g_best_seen[r["name"]]:
                    g_best_seen[r["name"]] = r["mk"]
                if r["beats_bar"]:
                    g_wins.append(r)
                # Pilot pass trigger: win (< bar) OR >=50% gap closed (G2 <= 410, G6 <= 382)
                if r["beats_bar"] or (r["name"] == "Behnke17" and r["mk"] is not None and r["mk"] <= 410) or (r["name"] == "Behnke60" and r["mk"] is not None and r["mk"] <= 382):
                    pilot_passed = True
            print(f"Step 4 pilot_passed={pilot_passed}", flush=True)
            if hit_cap:
                stopped_at_cap = True
                stopped_reason = "during G_S4_pilot_15m"

    if not stopped_at_cap and pilot_passed:
        rem_s = deadline - time.time()
        if rem_s < 120.0:
            stopped_at_cap = True
            stopped_reason = "before Step 5 G_S5_sweep_15m"
        else:
            # Step 5: 15m Sweep on G1, G3, G4, G5
            print(f"\n=== STEP 5: G_S5_sweep_15m (G1, G3, G4, G5, rem_cap={rem_s/60:.1f}m) ===", flush=True)
            s_recs = [g_by_label[lbl] for lbl in ("G1", "G3", "G4", "G5")]
            s_tasks = [
                dict(
                    stage="G_S5_sweep_15m", rec=r, budget_s=900.0, threads=3, mem_gb=6,
                    max_per_m=2, max_total=20, hard_cap=25, upper_cap=g_best_seen[r["name"]],
                    seed=6200 + i,
                )
                for i, r in enumerate(s_recs)
            ]
            s_res, hit_cap = run_waves("G_S5_sweep_15m", solve_g_one, s_tasks, 2, deadline, log_path)
            sweep_ran = True
            g_results.extend(s_res)
            for r in s_res:
                if r["mk"] is not None and r["mk"] < g_best_seen[r["name"]]:
                    g_best_seen[r["name"]] = r["mk"]
                if r["beats_bar"]:
                    g_wins.append(r)
            if hit_cap:
                stopped_at_cap = True
                stopped_reason = "during G_S5_sweep_15m"

    if not stopped_at_cap and sweep_ran:
        won_g_names = {r["name"] for r in g_wins}
        qual = [
            g for g in g_targets
            if g["name"] not in won_g_names
            and g_best_seen[g["name"]] < g["prev_best"]
            and (g_best_seen[g["name"]] - g["true_bar"]) <= 8
        ]
        if qual:
            rem_s = deadline - time.time()
            if rem_s < 120.0:
                stopped_at_cap = True
                stopped_reason = "before Step 6 G_S6_polish_30m"
            else:
                print(f"\n=== STEP 6: G_S6_polish_30m ({[q['name'] for q in qual]}, rem_cap={rem_s/60:.1f}m) ===", flush=True)
                q_tasks = [
                    dict(
                        stage="G_S6_polish_30m", rec=r, budget_s=1800.0, threads=3, mem_gb=6,
                        max_per_m=3, max_total=28, hard_cap=32, upper_cap=g_best_seen[r["name"]],
                        seed=6300 + i,
                    )
                    for i, r in enumerate(qual)
                ]
                q_res, hit_cap = run_waves("G_S6_polish_30m", solve_g_one, q_tasks, 2, deadline, log_path)
                g_results.extend(q_res)
                for r in q_res:
                    if r["mk"] is not None and r["mk"] < g_best_seen[r["name"]]:
                        g_best_seen[r["name"]] = r["mk"]
                    if r["beats_bar"]:
                        g_wins.append(r)
                if hit_cap:
                    stopped_at_cap = True
                    stopped_reason = "during G_S6_polish_30m"
        else:
            print("\nStep 6 skipped: no non-winning giant met (beat prev_best AND gap <= +8).", flush=True)

    wall_m = round((time.time() - t0) / 60.0, 1)
    summary = dict(
        wall_m=wall_m,
        stopped_at_cap=stopped_at_cap,
        stopped_reason=stopped_reason,
        u_wins=[(r["name"], r["mk"], r["true_bar"], r["stage"]) for r in u_wins],
        u_proved=[(r["name"], r["true_bar"], r["stage"]) for r in u_proved],
        u_remaining=[r["name"] for r in u_remaining],
        pilot_passed=pilot_passed,
        sweep_ran=sweep_ran,
        g_wins=[(r["name"], r["mk"], r["true_bar"], r["stage"]) for r in g_wins],
        g_best_seen=g_best_seen,
    )
    with open(os.path.join(LOGS_DIR, "overnight_u6_g6_summary.json"), "w") as sf:
        json.dump(summary, sf, indent=2)
    print("\n=== OVERNIGHT CHAIN SUMMARY ===", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
