"""
Play 1 v3 Overtime Pass (play1_v3_overtime.py).
Runs the 8 late-improving uncracked Play 1 instances on 4 parallel workers (4 GB RLIMIT_AS):
  - 3 B3 Behnke (Behnke32, Behnke11, Behnke46): 1200s (20 min) each
  - 5 B5 Hurink/Brandimarte (Hurinkrdata27, BrandimarteMk11, Hurinkrdata17, Hurinkvdata18, Hurinkvdata11): 900s (15 min) each
Total wall time on 4 workers: ~35 min.
Supports --round2 <comma_separated_names> to automatically run a 2x pass (2400s / 1800s) on selected survivors.
"""
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

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
INST_DIR = os.path.join(BASE, "runs/2026-11-11-2301/data/repo/instances/Example_Instances_FJSSP-WF")
CATALOG_PATH = os.path.join(OUT_DIR, "true_bar_catalog.json")
WINS_DIR = os.path.join(OUT_DIR, "wins")
LOGS_DIR = os.path.join(OUT_DIR, "logs")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)

import fjsspw  # noqa: E402
import numba_ts  # noqa: E402
import numba_ts_v3  # noqa: E402


OVERTIME_SPECS = [
    ("behnkegeiger32",  "B3_behnke_rem",   1200.0, 219),
    ("behnkegeiger11",  "B3_behnke_rem",   1200.0, 230),
    ("behnkegeiger46",  "B3_behnke_rem",   1200.0, 107),
    ("hurinkrdata27",   "B5_midgap_3to10",  900.0, 773),
    ("brandimarte11",   "B5_midgap_3to10",  900.0, 587),
    ("hurinkrdata17",   "B5_midgap_3to10",  900.0, 1023),
    ("hurinkvdata18",   "B5_midgap_3to10",  900.0, 1039),
    ("hurinkvdata11",   "B5_midgap_3to10",  900.0, 720),
]


def build_tasks(round2_arg=None):
    cat = json.load(open(CATALOG_PATH))
    round_tag = "ot_r1"
    mult = 1.0
    seed_base = 700000
    only_set = None

    if round2_arg:
        round_tag = "ot_r2_2x"
        mult = 2.0
        seed_base = 800000
        only_set = {x.strip().lower().replace(".fjs", "") for x in round2_arg.split(",") if x.strip()}

    tasks = []
    for i, (k, bname, base_s, prev_mk) in enumerate(OVERTIME_SPECS):
        assert k in cat, f"Missing catalog key: {k}"
        rec = cat[k]
        stem = rec["fjs"].replace(".fjs", "").lower()
        if only_set is not None and k not in only_set and stem not in only_set:
            continue
        fp = os.path.join(INST_DIR, rec["fjs"])
        assert os.path.isfile(fp), f"Missing .fjs: {fp}"
        tasks.append(dict(
            bucket=f"{bname}_{round_tag}",
            round_tag=round_tag,
            rec=rec,
            budget_s=base_s * mult,
            prev_mk=prev_mk,
            seed=seed_base + i * 1019,
        ))

    assert len(tasks) > 0, f"No matching tasks for round2_arg={round2_arg}"
    tasks.sort(key=lambda t: -t["budget_s"])
    return round_tag, tasks


def run_one(task):
    lim = 4 * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    rec = task["rec"]
    fjs_path = os.path.join(INST_DIR, rec["fjs"])
    inst_name = rec["fjs"].replace(".fjs", "")
    J, M, W, jobs = fjsspw.parse(fjs_path)
    nb = numba_ts.build_numba_instance(J, M, W, jobs)

    best_mk, best_state, stats = numba_ts_v3.cmrts_v3_search(
        inst_name, nb, time_budget_s=task["budget_s"], seed0=task["seed"]
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
        bucket=task["bucket"],
        round=task["round_tag"],
        inst=rec["inst"],
        name=inst_name,
        fjs=rec["fjs"],
        lb=int(rec["lb"]),
        table_ub=table_ub,
        true_bar=true_bar,
        prev_mk=task["prev_mk"],
        mk=int(best_mk),
        vs_prev=int(best_mk) - task["prev_mk"],
        vs_bar=int(best_mk) - true_bar,
        vs_table=int(best_mk) - table_ub,
        beats_bar=beats_bar,
        valid=ok,
        seed=task["seed"],
        stats=stats,
        secs=round(time.time() - t0, 2),
        win_path=win_path,
    )


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "play1_v3_overtime.jsonl")

    round2_arg = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--round2":
        round2_arg = sys.argv[2]

    round_tag, tasks = build_tasks(round2_arg=round2_arg)
    print(f"=== START {round_tag} ({len(tasks)} insts, 4 workers) ===", flush=True)
    t_all = time.time()
    wins = 0
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(run_one, t): t["rec"]["fjs"] for t in tasks}
        for fut in as_completed(futs):
            r = fut.result()
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            if r["beats_bar"]:
                wins += 1
            pct = 100.0 * r["stats"]["best_at_s"] / max(1.0, r["secs"])
            tag = f"WIN ({r['vs_bar']:+d})" if r["beats_bar"] else ("TIE" if r["vs_bar"] == 0 else f"{r['vs_bar']:+d}")
            print(
                f"  [{r['name']:16s}] mk={r['mk']:4d} (prev={r['prev_mk']}, {r['vs_prev']:+d}) | "
                f"bar={r['true_bar']:4d} ({tag}) | best_at={r['stats']['best_at_s']:.1f}s/{r['secs']:.0f}s ({pct:.0f}%) | "
                f"evals={r['stats']['evals']:,}",
                flush=True,
            )
    print(f"=== DONE {round_tag}: {len(tasks)} done | wins={wins} | {round((time.time()-t_all)/60.0, 1)}m wall ===", flush=True)


if __name__ == "__main__":
    main()
