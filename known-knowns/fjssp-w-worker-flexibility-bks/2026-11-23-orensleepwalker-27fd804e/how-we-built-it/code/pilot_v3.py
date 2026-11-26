"""
10-Minute 4-Instance Proof Pilot for FJSSP-W v3 Engine (pilot_v3.py).
Head-to-head test of numba_ts_v3.py against v2's exact scores on the 4 hardest
bottleneck Behnke targets (4 workers in parallel, 600s each -> ~10.2 min wall):
  1. Behnke60 (2363 KB, TrueBar=370 HUST, TableUB=431, v2=406)
  2. Behnke17 ( 289 KB, TrueBar=402,      TableUB=402, v2=419)
  3. Behnke33 ( 554 KB, TrueBar=219,      TableUB=219, v2=219 TIE)
  4. Behnke35 ( 555 KB, TrueBar=208,      TableUB=208, v2=212)

DO NOT RUN while another agent is running heavy CPU search.
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
WINS_DIR = os.path.join(OUT_DIR, "wins")
LOGS_DIR = os.path.join(OUT_DIR, "logs")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)

import fjsspw  # noqa: E402
import numba_ts  # noqa: E402
import numba_ts_v3  # noqa: E402


PILOT_TARGETS = [
    dict(inst="behnkegeiger60", fjs="Behnke60.fjs", lb=74, table_ub=431, true_bar=370, v2_mk=406, budget_s=600.0, seed=300001),
    dict(inst="behnkegeiger17", fjs="Behnke17.fjs", lb=73, table_ub=402, true_bar=402, v2_mk=419, budget_s=600.0, seed=300002),
    dict(inst="behnkegeiger33", fjs="Behnke33.fjs", lb=67, table_ub=219, true_bar=219, v2_mk=219, budget_s=600.0, seed=300003),
    dict(inst="behnkegeiger35", fjs="Behnke35.fjs", lb=71, table_ub=208, true_bar=208, v2_mk=212, budget_s=600.0, seed=300004),
]


def run_one(cfg):
    lim = 4 * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    fjs_path = os.path.join(INST_DIR, cfg["fjs"])
    inst_name = cfg["fjs"].replace(".fjs", "")
    J, M, W, jobs = fjsspw.parse(fjs_path)
    nb = numba_ts.build_numba_instance(J, M, W, jobs)

    best_mk, best_state, stats = numba_ts_v3.cmrts_v3_search(
        inst_name, nb, time_budget_s=cfg["budget_s"], seed0=cfg["seed"]
    )
    sched = numba_ts.to_schedule_json(inst_name, nb, best_state[0], best_state[12])
    ok, cmk, errs = fjsspw.check(fjs_path, sched)
    assert ok and cmk == best_mk, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} best={best_mk} errs={errs[:3]}"

    win_path = None
    beats_bar = best_mk < cfg["true_bar"]
    if beats_bar:
        os.makedirs(WINS_DIR, exist_ok=True)
        win_path = os.path.join(WINS_DIR, f"{inst_name}_mk{best_mk}_bar{cfg['true_bar']}.json")
        with open(win_path, "w") as wf:
            json.dump(sched, wf)

    return dict(
        bucket="P1_v3_pilot",
        inst=cfg["inst"],
        name=inst_name,
        fjs=cfg["fjs"],
        lb=cfg["lb"],
        table_ub=cfg["table_ub"],
        true_bar=cfg["true_bar"],
        v2_mk=cfg["v2_mk"],
        mk=int(best_mk),
        vs_v2=int(best_mk) - cfg["v2_mk"],
        vs_bar=int(best_mk) - cfg["true_bar"],
        beats_bar=beats_bar,
        valid=ok,
        seed=cfg["seed"],
        stats=stats,
        secs=round(time.time() - t0, 2),
        win_path=win_path,
    )


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "pilot_v3.jsonl")
    t_all = time.time()
    print("Launching 10-min 4-instance v3 proof pilot...", flush=True)
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(run_one, c): c["fjs"] for c in PILOT_TARGETS}
        for fut in as_completed(futs):
            r = fut.result()
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            tag = "WIN!" if r["beats_bar"] else ("TIE" if r["vs_bar"] == 0 else f"{r['vs_bar']:+d}")
            print(
                f"  [{r['name']:10s}] v3={r['mk']:4d} vs v2={r['v2_mk']:4d} ({r['vs_v2']:+3d}) | "
                f"bar={r['true_bar']:4d} ({tag}) | evals={r['stats']['evals']:,} | "
                f"ils={r['stats']['ils_kicks']} pr={r['stats']['pr_runs']} | {r['secs']}s",
                flush=True,
            )
    print(f"Pilot v3 complete in {round((time.time() - t_all)/60.0, 1)}m wall.", flush=True)


if __name__ == "__main__":
    main()
