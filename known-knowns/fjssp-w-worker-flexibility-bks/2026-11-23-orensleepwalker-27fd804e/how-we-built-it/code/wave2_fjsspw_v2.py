"""
Wave 2 FJSSP-W v2 5-Bucket Campaign (wave2_fjsspw_v2.py).
Uses Numba Critical-Path Iterated Tabu Search v2 (numba_ts_v2.py), 4 workers in parallel,
4 GB RLIMIT_AS per worker, single canonical fjsspw.check() validation, true-bar tracking
against table UB + GECCO 2026 competition zips, and Telegram notification on completion.

Buckets (119 instances total, ~146.0 min / 2.43 hrs wall time on 4 workers):
  1. W2_B1_hurinkedata    (30 insts, 270s each -> ~33.8m wall)
  2. W2_B2_hurinksdata    (30 insts, 270s each -> ~33.8m wall)
  3. W2_B3_hurink_rv_rem  (34 insts, 270s each -> ~38.2m wall)
  4. W2_B4_brandimarte    (13 insts, 300s each -> ~16.2m wall)
  5. W2_B5_v2_near_ties   (12 insts, 480s each -> ~24.0m wall)
"""
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
os.environ["NUMBA_NUM_THREADS"] = "1"

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
INST_DIR = os.path.join(BASE, "runs/2026-11-11-2301/data/repo/instances/Example_Instances_FJSSP-WF")
CATALOG_PATH = os.path.join(OUT_DIR, "true_bar_catalog.json")
PR868_PATH = os.path.join(BASE, "scans/final_91_records.json")
WAVE1_LOG = os.path.join(OUT_DIR, "logs/halfday_v2.jsonl")
WINS_DIR = os.path.join(OUT_DIR, "wins")
LOGS_DIR = os.path.join(OUT_DIR, "logs")
TG_SCRIPT = os.path.join(BASE, "scans/2026-11-19-mmlib-solver/phaseB/tg_notify.py")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)

import fjsspw  # noqa: E402
import numba_ts  # noqa: E402
import numba_ts_v2  # noqa: E402


def build_buckets():
    cat = json.load(open(CATALOG_PATH))
    f91 = json.load(open(PR868_PATH))
    pr868_all = {r["instance"].lower().replace(".fjs", "") for r in f91}

    ran_v2 = {}
    with open(WAVE1_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            k = r["inst"].lower()
            if k not in ran_v2 or r["mk"] < ran_v2[k]["mk"]:
                ran_v2[k] = r

    def is_open_untouched(k, r):
        stem = r["fjs"].replace(".fjs", "").lower()
        if r["is_opt"] or r["is_filed"]:
            return False
        if k in pr868_all or stem in pr868_all:
            return False
        if k in ran_v2:
            return False
        if r["size_bytes"] <= 0:
            return False
        return True

    w2_b1 = sorted(
        [r for k, r in cat.items() if k.startswith("hurinkedata") and is_open_untouched(k, r)],
        key=lambda r: -r["size_bytes"],
    )
    w2_b2 = sorted(
        [r for k, r in cat.items() if k.startswith("hurinksdata") and is_open_untouched(k, r)],
        key=lambda r: -r["size_bytes"],
    )
    w2_b3 = sorted(
        [
            r for k, r in cat.items()
            if (k.startswith("hurinkrdata") or k.startswith("hurinkvdata")) and is_open_untouched(k, r)
        ],
        key=lambda r: -r["size_bytes"],
    )
    w2_b4 = sorted(
        [r for k, r in cat.items() if k.startswith("brandimarte") and is_open_untouched(k, r)],
        key=lambda r: -r["size_bytes"],
    )
    w2_b5 = sorted(
        [
            cat[k] for k, res in ran_v2.items()
            if not res["beats_bar"] and 0 <= (res["mk"] - res["true_bar"]) <= 2
        ],
        key=lambda r: (ran_v2[r["inst"].lower()]["mk"] - r["true_bar"], -r["size_bytes"]),
    )

    buckets = [
        ("W2_B1_hurinkedata", w2_b1, 270.0),
        ("W2_B2_hurinksdata", w2_b2, 270.0),
        ("W2_B3_hurink_rv_rem", w2_b3, 270.0),
        ("W2_B4_brandimarte", w2_b4, 300.0),
        ("W2_B5_v2_near_ties", w2_b5, 480.0),
    ]

    total = sum(len(rows) for _, rows, _ in buckets)
    assert total == 119, f"Expected 119 tasks, got {total}: {[(n, len(rows)) for n, rows, _ in buckets]}"
    for bname, rows, _ in buckets:
        for r in rows:
            fjs_path = os.path.join(INST_DIR, r["fjs"])
            assert r["fjs"] and os.path.isfile(fjs_path), f"Missing .fjs in {bname}: {fjs_path}"

    return buckets


def run_worker(task):
    lim = 4 * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    bucket = task["bucket"]
    rec = task["rec"]
    budget_s = float(task["budget_s"])
    seed = int(task["seed"])

    fjs_path = os.path.join(INST_DIR, rec["fjs"])
    inst_name = rec["fjs"].replace(".fjs", "")
    J, M, W, jobs = fjsspw.parse(fjs_path)
    nb = numba_ts.build_numba_instance(J, M, W, jobs)

    best_mk, best_state, stats = numba_ts_v2.iterated_tabu_search(
        inst_name, nb, time_budget_s=budget_s, seed0=seed
    )
    best_alt = best_state[0]
    best_est = best_state[12]

    sched = numba_ts.to_schedule_json(inst_name, nb, best_alt, best_est)
    ok, cmk, errs = fjsspw.check(fjs_path, sched)
    assert ok and cmk == best_mk, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} best={best_mk} errs={errs[:3]}"

    true_bar = int(rec["true_bar"])
    table_ub = int(rec["table_ub"])
    beats_bar = best_mk < true_bar
    win_path = None
    if beats_bar:
        os.makedirs(WINS_DIR, exist_ok=True)
        win_path = os.path.join(WINS_DIR, f"{inst_name}_mk{best_mk}_bar{true_bar}.json")
        with open(win_path, "w") as wf:
            json.dump(sched, wf)

    return dict(
        bucket=bucket,
        inst=rec["inst"],
        name=inst_name,
        fjs=rec["fjs"],
        J=J,
        M=M,
        W=W,
        N=int(nb["N"]),
        lb=int(rec["lb"]),
        table_ub=table_ub,
        true_bar=true_bar,
        mk=int(best_mk),
        vs_bar=int(best_mk) - true_bar,
        vs_table=int(best_mk) - table_ub,
        beats_bar=beats_bar,
        valid=ok,
        seed=seed,
        stats=stats,
        secs=round(time.time() - t0, 2),
        win_path=win_path,
    )


def run_bucket(bucket_name, rows, budget_s, seed_base, log_path):
    t_b = time.time()
    print(f"\n=== START {bucket_name} ({len(rows)} insts, {int(budget_s)}s each) ===", flush=True)
    tasks = [
        dict(bucket=bucket_name, rec=r, budget_s=budget_s, seed=seed_base + i * 1009)
        for i, r in enumerate(rows)
    ]
    out = []
    wins = 0
    ties = 0
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(run_worker, t): t["rec"]["fjs"] for t in tasks}
        for fut in as_completed(futs):
            res = fut.result()
            out.append(res)
            with open(log_path, "a") as lf:
                lf.write(json.dumps(res) + "\n")
            if res["beats_bar"]:
                wins += 1
                tag = f"WIN ({res['vs_bar']:+d} vs bar, {res['vs_table']:+d} vs table)"
            elif res["vs_bar"] == 0:
                ties += 1
                tag = "TIE"
            else:
                tag = f"{res['vs_bar']:+d}"
            print(
                f"  [{res['name']:16s}] mk={res['mk']:4d} | bar={res['true_bar']:4d} ({tag}) | "
                f"evals={res['stats']['evals']:,} | ils={res['stats']['ils_kicks']} | {res['secs']}s",
                flush=True,
            )
    wall_m = round((time.time() - t_b) / 60.0, 1)
    print(f"=== DONE {bucket_name}: {len(out)} done | wins={wins} | ties={ties} | {wall_m}m wall ===", flush=True)
    return out, dict(bucket=bucket_name, done=len(out), wins=wins, ties=ties, wall_m=wall_m)


def send_telegram(summary_text):
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        msg_path = os.path.join(LOGS_DIR, "tg_wave2_v2.txt")
        with open(msg_path, "w") as f:
            f.write(summary_text)
        subprocess.run([sys.executable, TG_SCRIPT, "--file", msg_path], check=False, timeout=20)
    except Exception as e:
        print(f"Telegram notify error (non-fatal): {e}", flush=True)


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "wave2_v2.jsonl")

    t_all = time.time()
    buckets = build_buckets()
    all_results = []
    bucket_summaries = []

    for bi, (bname, rows, budget_s) in enumerate(buckets):
        res_list, bsum = run_bucket(
            bname, rows, budget_s, seed_base=100000 * (bi + 1), log_path=log_path
        )
        all_results.extend(res_list)
        bucket_summaries.append(bsum)

    final_best = {}
    for r in all_results:
        k = r["inst"].lower()
        if k not in final_best or r["mk"] < final_best[k]["mk"]:
            final_best[k] = r
    final_wins = sorted([r for r in final_best.values() if r["beats_bar"]], key=lambda r: r["vs_bar"])
    total_wall_m = round((time.time() - t_all) / 60.0, 1)

    lines = [
        f"FJSSP-W Wave 2 v2 Campaign COMPLETE ({total_wall_m}m wall, {len(all_results)} tasks):",
        f"WAVE 2 UNIQUE WINS BEATING TRUE BAR: {len(final_wins)} (gain {sum(r['vs_bar'] for r in final_wins)} pts vs true bar, {sum(r['vs_table'] for r in final_wins)} pts vs table UB)",
        "",
        "Buckets:",
    ]
    for bs in bucket_summaries:
        lines.append(f"• {bs['bucket']}: {bs['done']} done, {bs['wins']} wins, {bs['ties']} ties ({bs['wall_m']}m)")
    if final_wins:
        lines.append("")
        lines.append("Top Wave 2 Wins (vs True Bar):")
        for r in final_wins[:15]:
            lines.append(
                f"• {r['name']}: {r['mk']} vs bar {r['true_bar']} ({r['vs_bar']:+d}; table {r['table_ub']} {r['vs_table']:+d})"
            )

    summary_txt = "\n".join(lines)
    print("\n" + summary_txt, flush=True)
    send_telegram(summary_txt)


if __name__ == "__main__":
    main()
