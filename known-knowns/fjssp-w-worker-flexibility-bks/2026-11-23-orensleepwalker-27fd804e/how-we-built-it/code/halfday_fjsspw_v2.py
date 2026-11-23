"""
Half-Day FJSSP-W v2 5-Bucket Campaign (halfday_fjsspw_v2.py).
Uses Numba Critical-Path Iterated Tabu Search v2 (numba_ts_v2.py), 4 workers in parallel,
4 GB RLIMIT_AS per worker, canonical fjsspw.check() validation, true-bar tracking against
table UB + GECCO 2026 competition zips, and Telegram notification on completion.

Buckets (~3.7 - 4.0 hrs total wall time):
  1. B1_behnke_giants   (15 insts, 600s each -> ~40 min)
  2. B2_behnke_medlarge (10 insts, 480s each -> ~24 min)
  3. B3_dppaulli_open   (17 insts, 480s each -> ~40 min)
  4. B4_hurink_vr_top40 (40 insts, 360s each -> ~60 min)
  5. B5_deep_polish     (top 20 wins & <=+3% near-misses from B1-B4, 720s each -> ~60 min)
"""
import json
import os
import re
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

    def sort_num(r):
        m = re.search(r"(\d+)$", r["inst"])
        return int(m.group(1)) if m else 0

    b1 = sorted(
        [r for k, r in cat.items() if re.match(r"behnkegeiger(1[6-9]|20|3[6-9]|40|5[6-9]|60)$", k)],
        key=lambda r: (-r["size_bytes"], sort_num(r)),
    )
    b2 = sorted(
        [r for k, r in cat.items() if re.match(r"behnkegeiger(1[1-5]|3[1-5])$", k)],
        key=lambda r: (-r["size_bytes"], sort_num(r)),
    )
    b3 = sorted(
        [r for k, r in cat.items() if k.startswith("dppaulli") and not r["is_opt"] and not r["is_filed"] and r["size_bytes"] > 0],
        key=lambda r: -r["size_bytes"],
    )
    b4_all = [
        r for k, r in cat.items()
        if (k.startswith("hurinkvdata") or k.startswith("hurinkrdata"))
        and not r["is_opt"] and not r["is_filed"] and r["size_bytes"] > 0
    ]
    b4 = sorted(b4_all, key=lambda r: -r["size_bytes"])[:40]

    return [
        ("B1_behnke_giants", b1, 600.0),
        ("B2_behnke_medlarge", b2, 480.0),
        ("B3_dppaulli_open", b3, 480.0),
        ("B4_hurink_vr_top40", b4, 360.0),
    ]


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
        J=J, M=M, W=W, N=int(nb["N"]),
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
        msg_path = os.path.join(LOGS_DIR, "tg_halfday_v2.txt")
        with open(msg_path, "w") as f:
            f.write(summary_text)
        subprocess.run([sys.executable, TG_SCRIPT, "--file", msg_path], check=False, timeout=20)
    except Exception as e:
        print(f"Telegram notify error (non-fatal): {e}", flush=True)


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "halfday_v2.jsonl")

    t_all = time.time()
    buckets = build_buckets()
    all_results = []
    bucket_summaries = []

    for bi, (bname, rows, budget_s) in enumerate(buckets):
        res_list, bsum = run_bucket(bname, rows, budget_s, seed_base=10000 * (bi + 1), log_path=log_path)
        all_results.extend(res_list)
        bucket_summaries.append(bsum)

    # Bucket 5: Deep Polish top 20 (all winners first, then closest near-misses <= +3% of true_bar)
    cat = json.load(open(CATALOG_PATH))
    best_by_inst = {}
    for r in all_results:
        k = r["inst"].lower()
        if k not in best_by_inst or r["mk"] < best_by_inst[k]["mk"]:
            best_by_inst[k] = r

    winners = [r for r in best_by_inst.values() if r["beats_bar"]]
    near = [
        r for r in best_by_inst.values()
        if not r["beats_bar"] and (r["mk"] - r["true_bar"]) <= max(3, int(0.03 * r["true_bar"]))
    ]
    # Prioritize giant Behnke winners, then other winners, then closest near-misses by relative gap
    winners.sort(key=lambda r: (0 if r["bucket"] == "B1_behnke_giants" else 1, r["vs_bar"]))
    near.sort(key=lambda r: ((r["mk"] - r["true_bar"]) / max(1, r["true_bar"]), r["mk"] - r["true_bar"]))
    b5_selected = (winners + near)[:20]
    b5_rows = [cat[r["inst"].lower()] for r in b5_selected]

    if b5_rows:
        res5, bsum5 = run_bucket("B5_deep_polish", b5_rows, 720.0, seed_base=50000, log_path=log_path)
        all_results.extend(res5)
        bucket_summaries.append(bsum5)

    # Compute final unique wins strictly beating true_bar
    final_best = {}
    for r in all_results:
        k = r["inst"].lower()
        if k not in final_best or r["mk"] < final_best[k]["mk"]:
            final_best[k] = r
    final_wins = sorted([r for r in final_best.values() if r["beats_bar"]], key=lambda r: r["vs_bar"])
    total_wall_m = round((time.time() - t_all) / 60.0, 1)

    lines = [
        f"FJSSP-W Half-Day v2 Campaign COMPLETE ({total_wall_m}m wall, {len(all_results)} tasks):",
        f"UNIQUE WINS BEATING TRUE PUBLIC BAR: {len(final_wins)} (total gain {sum(r['vs_bar'] for r in final_wins)} pts vs true bar, {sum(r['vs_table'] for r in final_wins)} pts vs table UB)",
        "",
        "Buckets:",
    ]
    for bs in bucket_summaries:
        lines.append(f"• {bs['bucket']}: {bs['done']} done, {bs['wins']} wins, {bs['ties']} ties ({bs['wall_m']}m)")
    if final_wins:
        lines.append("")
        lines.append("Top Wins (vs True Bar):")
        for r in final_wins[:15]:
            lines.append(f"• {r['name']}: {r['mk']} vs bar {r['true_bar']} ({r['vs_bar']:+d}; table {r['table_ub']} {r['vs_table']:+d})")

    summary_txt = "\n".join(lines)
    print("\n" + summary_txt, flush=True)
    send_telegram(summary_txt)


if __name__ == "__main__":
    main()
