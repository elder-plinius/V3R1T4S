"""
Play 2 Escalation Campaign (play2_escalate_28.py).
Runs a 3-stage escalating CP-SAT deadline-snipe campaign (10m -> 20m -> 40m)
on the 28 remaining non-giant open FJSSP-W targets:
  - 2 small DPpaulli rows (DPpaulli1, DPpaulli7) never tested with Play 2 CP-SAT
  - 9 UNKNOWN survivors from Play 2 CP-SAT
  - 17 UNKNOWN survivors from Play 2 Cleanup

Does NOT modify best_wins/, best_wins_manifest.json, or prior logs.
Saves all verified wins strictly beating true_bar to wins_extra/.
"""
import argparse
import csv
import glob
import json
import os
import resource
import subprocess
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
WINS_EXTRA_DIR = os.path.join(OUT_DIR, "wins_extra")
LOGS_DIR = os.path.join(OUT_DIR, "logs")
TG_SCRIPT = os.path.join(BASE, "scans/2026-11-19-mmlib-solver/phaseB/tg_notify.py")

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

STAGES = [
    ("S1_10m", 600.0),
    ("S2_20m", 1200.0),
    ("S3_40m", 2400.0),
]


def _read_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def build_targets():
    """Assemble and validate the exact 28 non-giant open targets with zero claim overlap."""
    rounded_ub = {}
    rounded_lb = {}
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f, delimiter=";"):
            k = r["Instance"].strip().lower()
            rounded_ub[k] = int(round(float(r["UB"])))
            rounded_lb[k] = int(round(float(r["LB"])))

    cat = json.load(open(CATALOG_PATH))
    pr868_all = {r["instance"].lower().replace(".fjs", "") for r in json.load(open(PR868_PATH))}
    filed_1081 = {
        os.path.basename(p).replace(".json", "").lower()
        for p in glob.glob(os.path.join(BASE, "runs/2026-11-13-0112/claim/object/*.json"))
    }
    won_best = {x["inst"].lower() for x in json.load(open(os.path.join(OUT_DIR, "best_wins_manifest.json")))}
    won_extra = {
        os.path.basename(p).split("_mk")[0].lower()
        for p in glob.glob(os.path.join(WINS_EXTRA_DIR, "*.json"))
    }

    p2_unk = [
        (r["inst"].lower(), "play2_unknown")
        for r in _read_jsonl(os.path.join(LOGS_DIR, "play2_cpsat.jsonl"))
        if r.get("outcome") == "UNKNOWN"
    ]
    cl_unk = [
        (r["inst"].lower(), "cleanup_unknown")
        for r in _read_jsonl(os.path.join(LOGS_DIR, "play2_cleanup.jsonl"))
        if r.get("outcome") == "UNKNOWN"
    ]
    assert len(p2_unk) == 9, f"Expected 9 Play 2 UNKNOWN rows, got {len(p2_unk)}"
    assert len(cl_unk) == 17, f"Expected 17 Cleanup UNKNOWN rows, got {len(cl_unk)}"

    raw_keys = [("dppaulli1", "dppaulli_untried"), ("dppaulli7", "dppaulli_untried")] + p2_unk + cl_unk
    targets_by_key = {}
    for k, src in raw_keys:
        assert k not in targets_by_key, f"Duplicate target key: {k}"
        r = cat[k]
        stem = r["fjs"].replace(".fjs", "").lower()
        assert not r["is_opt"], f"Target already optimal: {k}"
        assert not r["is_filed"], f"Target already filed: {k}"
        assert k not in pr868_all and stem not in pr868_all, f"Overlap with PR #868: {k}"
        assert k not in filed_1081 and stem not in filed_1081, f"Overlap with PR #1081: {k}"
        assert k not in won_best and stem not in won_best, f"Overlap with best_wins_manifest: {k}"
        assert k not in won_extra and stem not in won_extra, f"Overlap with wins_extra: {k}"

        rub = rounded_ub[k]
        rlb = rounded_lb[k]
        cb = r.get("comp_best")
        bar = min(rub, int(cb)) if cb is not None else rub
        fp = os.path.join(INST_DIR, r["fjs"])
        assert r["fjs"] and os.path.isfile(fp), f"Missing .fjs for {k}: {fp}"

        targets_by_key[k] = dict(
            inst=r["inst"],
            fjs=r["fjs"],
            lb=rlb,
            table_ub=rub,
            true_bar=bar,
            size_bytes=r["size_bytes"],
            kb=r["size_bytes"] // 1024,
            source=src,
        )

    targets = sorted(targets_by_key.values(), key=lambda x: (x["kb"], x["fjs"]))
    assert len(targets) == 28, f"Expected 28 targets, got {len(targets)}"
    return targets


def solve_escalate_one(task):
    """Run CP-SAT hard-capped at H = true_bar - 1 with optional Phase B polish."""
    lim = int(task["mem_gb"]) * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    rec = task["rec"]
    stage = task["stage"]
    tier = task["tier"]
    budget_s = float(task["budget_s"])
    threads = int(task["threads"])
    seed = int(task["seed"])

    fjs_path = os.path.join(INST_DIR, rec["fjs"])
    inst_name = rec["fjs"].replace(".fjs", "")
    true_bar = int(rec["true_bar"])
    table_ub = int(rec["table_ub"])

    J, M, W, jobs = fjsspw.parse(fjs_path)
    H = true_bar - 1
    m, _, S, B = _build_snipe_model(J, M, W, jobs, H)

    sv = _configure_solver(budget_s, threads, seed)
    cb = FirstWinStopCallback()
    st = sv.Solve(m, cb)

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        best_sched = _extract_sched(inst_name, jobs, S, B, sv)
        ok, cmk, errs = fjsspw.check(fjs_path, best_sched)
        assert ok and cmk <= H, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} H={H} errs={errs[:3]}"
        best_mk = int(cmk)
        final_status = sv.StatusName(st)

        rem_s = budget_s - (time.time() - t0)
        if st != cp_model.OPTIMAL and best_mk > int(rec["lb"]) and rem_s > 2.0:
            H2 = best_mk - 1
            m2, _, S2, B2 = _build_snipe_model(J, M, W, jobs, H2)
            sv2 = _configure_solver(min(15.0, rem_s), threads, seed + 7)
            st2 = sv2.Solve(m2)
            if st2 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                s2 = _extract_sched(inst_name, jobs, S2, B2, sv2)
                ok2, cmk2, errs2 = fjsspw.check(fjs_path, s2)
                assert ok2 and cmk2 <= H2, f"Checker FAIL2 {inst_name}: ok={ok2} cmk={cmk2} errs={errs2[:3]}"
                best_sched = s2
                best_mk = int(cmk2)
                final_status = sv2.StatusName(st2)

        os.makedirs(WINS_EXTRA_DIR, exist_ok=True)
        win_path = os.path.join(WINS_EXTRA_DIR, f"{inst_name}_mk{best_mk}_bar{true_bar}.json")
        with open(win_path, "w") as wf:
            json.dump(best_sched, wf)

        return dict(
            stage=stage,
            tier=tier,
            source=rec["source"],
            inst=rec["inst"],
            name=inst_name,
            fjs=rec["fjs"],
            kb=rec["kb"],
            lb=int(rec["lb"]),
            table_ub=table_ub,
            true_bar=true_bar,
            mk=best_mk,
            vs_bar=best_mk - true_bar,
            vs_table=best_mk - table_ub,
            beats_bar=True,
            outcome="WIN",
            cpsat_status=final_status,
            valid=True,
            seed=seed,
            secs=round(time.time() - t0, 2),
            win_path=win_path,
        )

    outcome = "PROVED_OPTIMAL_AT_BAR" if st == cp_model.INFEASIBLE else sv.StatusName(st)
    return dict(
        stage=stage,
        tier=tier,
        source=rec["source"],
        inst=rec["inst"],
        name=inst_name,
        fjs=rec["fjs"],
        kb=rec["kb"],
        lb=int(rec["lb"]),
        table_ub=table_ub,
        true_bar=true_bar,
        mk=None,
        vs_bar=None,
        vs_table=None,
        beats_bar=False,
        outcome=outcome,
        cpsat_status=sv.StatusName(st),
        valid=False,
        seed=seed,
        secs=round(time.time() - t0, 2),
        win_path=None,
    )


def send_telegram(summary_text):
    """Persist notification text and send via workspace tg_notify.py."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    msg_path = os.path.join(LOGS_DIR, "tg_play2_escalate_28.txt")
    with open(msg_path, "w") as f:
        f.write(summary_text)
    proc = subprocess.run([sys.executable, TG_SCRIPT, "--file", msg_path], check=False, timeout=30)
    print(f"Telegram notify exit={proc.returncode}", flush=True)


def run_pool_batch(stage_name, tier_name, recs, budget_s, procs, threads, mem_gb, stage_idx, seed_offset, log_path):
    """Execute one homogeneous worker pool batch and append JSONL outcomes."""
    if not recs:
        return [], 0, 0, []
    print(
        f"  --- {stage_name}/{tier_name}: {len(recs)} insts, {int(budget_s)}s, {procs}p x {threads}t, {mem_gb}GB ---",
        flush=True,
    )
    tasks = [
        dict(
            stage=stage_name,
            tier=tier_name,
            rec=r,
            budget_s=budget_s,
            threads=threads,
            mem_gb=mem_gb,
            seed=1000 * stage_idx + seed_offset + idx + 42,
        )
        for idx, r in enumerate(recs)
    ]
    results = []
    wins = proved = 0
    survivors = []
    with ProcessPoolExecutor(max_workers=procs) as ex:
        futs = {ex.submit(solve_escalate_one, t): t["rec"] for t in tasks}
        for fut in as_completed(futs):
            rec = futs[fut]
            res = fut.result()
            results.append(res)
            with open(log_path, "a") as lf:
                lf.write(json.dumps(res) + "\n")
            if res["outcome"] == "WIN":
                wins += 1
                print(
                    f"    [{res['name']:16s}] WIN! mk={res['mk']:4d} < bar={res['true_bar']:4d} ({res['vs_bar']:+d}) | {res['secs']}s",
                    flush=True,
                )
            elif res["outcome"] == "PROVED_OPTIMAL_AT_BAR":
                proved += 1
                print(
                    f"    [{res['name']:16s}] PROVED OPTIMAL at bar={res['true_bar']:4d} (INFEASIBLE <= {res['true_bar']-1}) | {res['secs']}s",
                    flush=True,
                )
            else:
                survivors.append(rec)
                print(
                    f"    [{res['name']:16s}] {res['outcome']} (bar={res['true_bar']:4d}) | {res['secs']}s",
                    flush=True,
                )
    return results, wins, proved, survivors


def main():
    parser = argparse.ArgumentParser(description="Play 2 Escalation (10m -> 20m -> 40m) on 28 non-giant FJSSP-W rows")
    parser.add_argument("--dry-run", action="store_true", help="Verify targets, bars, and zero overlap then exit")
    args = parser.parse_args()

    targets = build_targets()
    if args.dry_run:
        print(f"DRY RUN OK: {len(targets)} verified targets (0 overlap with best_wins / wins_extra / PR868 / PR1081)")
        for i, t in enumerate(targets, 1):
            tier = "large" if t["kb"] > 100 else "small_med"
            print(
                f"  {i:2d}. {t['fjs'][:-4]:16s} | {t['kb']:3d} KB | {tier:9s} | bar={t['true_bar']:4d} (tbl={t['table_ub']:4d}, lb={t['lb']:4d}) | {t['source']}"
            )
        return

    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_EXTRA_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "play2_escalate_28.jsonl")
    with open(log_path, "w"):
        pass

    t_all = time.time()
    remaining = targets
    stage_summaries = []
    all_wins = []
    total_proved = 0

    for stage_idx, (stage_name, budget_s) in enumerate(STAGES, 1):
        if not remaining:
            print(f"\nNo UNKNOWN survivors left before {stage_name}; stopping early.", flush=True)
            break

        t_stage = time.time()
        print(f"\n=== START {stage_name} ({len(remaining)} insts, {int(budget_s)}s budget) ===", flush=True)
        small_med = sorted([r for r in remaining if r["kb"] <= 100], key=lambda r: (r["kb"], r["fjs"]))
        large = sorted([r for r in remaining if r["kb"] > 100], key=lambda r: (r["kb"], r["fjs"]))

        r_sm, w_sm, p_sm, surv_sm = run_pool_batch(
            stage_name, "small_med", small_med, budget_s, 3, 2, 4, stage_idx, 0, log_path
        )
        r_lg, w_lg, p_lg, surv_lg = run_pool_batch(
            stage_name, "large", large, budget_s, 2, 3, 6, stage_idx, len(small_med), log_path
        )

        stage_res = r_sm + r_lg
        stage_wins = w_sm + w_lg
        stage_proved = p_sm + p_lg
        next_remaining = sorted(surv_sm + surv_lg, key=lambda r: (r["kb"], r["fjs"]))
        wall_m = round((time.time() - t_stage) / 60.0, 1)

        all_wins.extend(r for r in stage_res if r["beats_bar"])
        total_proved += stage_proved
        stage_summaries.append(
            dict(
                stage=stage_name,
                tested=len(remaining),
                wins=stage_wins,
                proved=stage_proved,
                unknown=len(next_remaining),
                wall_m=wall_m,
            )
        )
        print(
            f"=== DONE {stage_name}: {len(remaining)} tested | wins={stage_wins} | proved_opt={stage_proved} | unknown={len(next_remaining)} | {wall_m}m wall ===",
            flush=True,
        )
        remaining = next_remaining

    all_wins_sorted = sorted(all_wins, key=lambda r: r["vs_bar"])
    total_wall_m = round((time.time() - t_all) / 60.0, 1)
    total_extra = len(glob.glob(os.path.join(WINS_EXTRA_DIR, "*.json")))
    total_clean_wins = 88 + total_extra
    resolved_total = 368 + len(all_wins_sorted) + total_proved
    still_open = 402 - resolved_total

    lines = [
        f"FJSSP-W Play 2 Escalation COMPLETE ({total_wall_m}m wall):",
        f"New wins: {len(all_wins_sorted)} ({sum(r['vs_bar'] for r in all_wins_sorted)} pts) | Proved optimal: {total_proved} | Surviving UNKNOWN: {len(remaining)}",
        f"Board: {resolved_total}/402 resolved | {total_clean_wins} clean wins (88 best_wins + {total_extra} wins_extra) | {still_open} open ({len(remaining)} UNKNOWN + 6 Behnke giants)",
        "",
        "Stages:",
    ]
    for ss in stage_summaries:
        lines.append(
            f"• {ss['stage']}: {ss['tested']} tested -> {ss['wins']} wins, {ss['proved']} opt, {ss['unknown']} unk ({ss['wall_m']}m)"
        )
    if all_wins_sorted:
        lines.append("")
        lines.append("New Wins:")
        for r in all_wins_sorted:
            lines.append(f"• {r['name']} ({r['stage']}): {r['mk']} vs bar {r['true_bar']} ({r['vs_bar']:+d})")
    if remaining:
        lines.append("")
        lines.append("Still UNKNOWN after 40m:")
        lines.append(", ".join(r["fjs"][:-4] for r in remaining))

    summary_txt = "\n".join(lines)
    print("\n" + summary_txt, flush=True)
    send_telegram(summary_txt)


if __name__ == "__main__":
    main()
