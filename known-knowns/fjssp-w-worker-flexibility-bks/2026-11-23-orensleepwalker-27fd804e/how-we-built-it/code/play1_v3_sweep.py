"""
Play 1 FJSSP-W v3 Sweep (play1_v3_sweep.py) — strictly indexed to Master Board B1..B7.
Runs numba_ts_v3.py (CMRTS v3: clean est/tail buffers, joint idle-slot insertion,
load-aware mode scanning, N5 critical-block swaps, Elite Pool Path Relinking)
on 4 parallel workers, 4 GB RLIMIT_AS per worker, canonical fjsspw.check(),
and Telegram notification on completion.

Buckets (45 instances total, ~80 min / 1.33 hrs wall time on 4 workers):
  1. B3_behnke_rem    ( 4 insts: Behnke32, 34, 11, 46; 600s each -> ~10m wall)
  2. B4_dppaulli_rem  ( 7 insts: remaining open DPpaulli; 480s each -> ~16m wall)
  3. B5_midgap_3to10  (34 insts: mid-gap +3..+10; 360s each -> ~54m wall)
"""
import glob
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
PR868_PATH = os.path.join(BASE, "scans/final_91_records.json")
WINS_DIR = os.path.join(OUT_DIR, "wins")
LOGS_DIR = os.path.join(OUT_DIR, "logs")
TG_SCRIPT = os.path.join(BASE, "scans/2026-11-19-mmlib-solver/phaseB/tg_notify.py")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)

import fjsspw  # noqa: E402
import numba_ts  # noqa: E402
import numba_ts_v3  # noqa: E402


def build_buckets():
    cat = json.load(open(CATALOG_PATH))
    f91 = json.load(open(PR868_PATH))
    pr868_all = {r["instance"].lower().replace(".fjs", "") for r in f91}
    filed_1081 = {
        os.path.basename(p).replace(".json", "").lower()
        for p in glob.glob(os.path.join(BASE, "runs/2026-11-13-0112/claim/object/*.json"))
    }
    won_v2 = {x["inst"].lower() for x in json.load(open(os.path.join(OUT_DIR, "best_wins_manifest.json")))}
    # Also exclude the 2 new pilot_v3 wins (Behnke33, Behnke35) and hard-wall Behnke16-20, 60
    skip_b3 = {"behnkegeiger33", "behnkegeiger35", "behnkegeiger16", "behnkegeiger17",
               "behnkegeiger18", "behnkegeiger19", "behnkegeiger20", "behnkegeiger60"}

    v2_best = {}
    for lp in [os.path.join(LOGS_DIR, "halfday_v2.jsonl"), os.path.join(LOGS_DIR, "wave2_v2.jsonl")]:
        with open(lp) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                k = r["inst"].lower()
                if k not in v2_best or r["mk"] < v2_best[k]:
                    v2_best[k] = r["mk"]

    cp_best = {}
    for rp in glob.glob(os.path.join(BASE, "runs/2026-11-12-*/attempts/cpsat/report.md")):
        with open(rp) as f:
            for line in f:
                m = re.match(r"\|\s*([a-zA-Z0-9_]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
                if m:
                    k = m.group(1).lower()
                    mk = int(m.group(3))
                    if k not in cp_best or mk < cp_best[k]:
                        cp_best[k] = mk

    b3, b4, b5 = [], [], []
    for k, r in cat.items():
        stem = r["fjs"].replace(".fjs", "").lower()
        if r["is_opt"] or r["is_filed"] or k in pr868_all or stem in pr868_all or stem in filed_1081 or k in won_v2:
            continue
        fam = re.match(r"([a-zA-Z]+)", k).group(1)
        bar = r["true_bar"]
        kb = r["size_bytes"] // 1024
        cands = [x for x in (v2_best.get(k), cp_best.get(k)) if x is not None]
        gap = (min(cands) - bar) if cands else None

        # Exact B1..B7 partitioning
        if gap is not None and 0 <= gap <= 2 and kb <= 500:
            continue  # B1 / B2 (Play 2)
        elif fam == "behnkegeiger" and kb >= 100:
            if k not in skip_b3:
                b3.append((gap if gap is not None else 999, -kb, r))
        elif fam == "dppaulli":
            b4.append((gap if gap is not None else 999, -kb, r))
        elif gap is not None and 3 <= gap <= 10:
            b5.append((gap, -kb, r))

    b3_rows = [x[2] for x in sorted(b3, key=lambda x: (x[0], x[1]))]
    b4_rows = [x[2] for x in sorted(b4, key=lambda x: (x[0], x[1]))]
    b5_rows = [x[2] for x in sorted(b5, key=lambda x: (x[0], x[1]))]

    buckets = [
        ("B3_behnke_rem", b3_rows, 600.0),
        ("B4_dppaulli_rem", b4_rows, 480.0),
        ("B5_midgap_3to10", b5_rows, 360.0),
    ]

    assert [(n, len(rows)) for n, rows, _ in buckets] == [
        ("B3_behnke_rem", 4),
        ("B4_dppaulli_rem", 7),
        ("B5_midgap_3to10", 34),
    ], f"Unexpected bucket counts: {[(n, len(rows)) for n, rows, _ in buckets]}"

    for bname, rows, _ in buckets:
        for r in rows:
            fp = os.path.join(INST_DIR, r["fjs"])
            assert r["fjs"] and os.path.isfile(fp), f"Missing .fjs in {bname}: {fp}"

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

    best_mk, best_state, stats = numba_ts_v3.cmrts_v3_search(
        inst_name, nb, time_budget_s=budget_s, seed0=seed
    )
    sched = numba_ts.to_schedule_json(inst_name, nb, best_state[0], best_state[12])
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
        dict(bucket=bucket_name, rec=r, budget_s=budget_s, seed=seed_base + i * 1013)
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
                f"evals={res['stats']['evals']:,} | ils={res['stats']['ils_kicks']} pr={res['stats']['pr_runs']} | {res['secs']}s",
                flush=True,
            )
    wall_m = round((time.time() - t_b) / 60.0, 1)
    print(f"=== DONE {bucket_name}: {len(out)} done | wins={wins} | ties={ties} | {wall_m}m wall ===", flush=True)
    return out, dict(bucket=bucket_name, done=len(out), wins=wins, ties=ties, wall_m=wall_m)


def send_telegram(summary_text):
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        msg_path = os.path.join(LOGS_DIR, "tg_play1_v3.txt")
        with open(msg_path, "w") as f:
            f.write(summary_text)
        subprocess.run([sys.executable, TG_SCRIPT, "--file", msg_path], check=False, timeout=20)
    except Exception as e:
        print(f"Telegram notify error (non-fatal): {e}", flush=True)


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "play1_v3.jsonl")

    t_all = time.time()
    buckets = build_buckets()
    all_results = []
    bucket_summaries = []

    for bi, (bname, rows, budget_s) in enumerate(buckets):
        res_list, bsum = run_bucket(
            bname, rows, budget_s, seed_base=400000 * (bi + 1), log_path=log_path
        )
        all_results.extend(res_list)
        bucket_summaries.append(bsum)

    final_wins = sorted([r for r in all_results if r["beats_bar"]], key=lambda r: r["vs_bar"])
    total_wall_m = round((time.time() - t_all) / 60.0, 1)

    lines = [
        f"FJSSP-W Play 1 (v3) COMPLETE ({total_wall_m}m wall, {len(all_results)} tasks):",
        f"NEW PLAY 1 WINS: {len(final_wins)} (gain {sum(r['vs_bar'] for r in final_wins)} pts vs true bar)",
        "",
        "Buckets:",
    ]
    for bs in bucket_summaries:
        lines.append(f"• {bs['bucket']}: {bs['done']} done, {bs['wins']} wins, {bs['ties']} ties ({bs['wall_m']}m)")
    if final_wins:
        lines.append("")
        lines.append("Play 1 Wins:")
        for r in final_wins[:15]:
            lines.append(f"• {r['name']}: {r['mk']} vs bar {r['true_bar']} ({r['vs_bar']:+d})")

    summary_txt = "\n".join(lines)
    print("\n" + summary_txt, flush=True)
    send_telegram(summary_txt)


if __name__ == "__main__":
    main()
