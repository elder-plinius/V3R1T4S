"""
15-Minute Pilot for Option 1 + Option 2 Combo (numba_ts_v4.py) on G3 (Behnke18) + G6 (Behnke60).
Usage:
  .venv-research/bin/python pilot_v4_g3_g6.py --smoke   # 25s smoke test on G3 (Behnke18)
  .venv-research/bin/python -u pilot_v4_g3_g6.py       # 900s parallel pilot on G3 + G6

Saves any verified win (< true_bar) to wins_extra2/.
DOES NOT modify best_wins/, best_wins_manifest.json, wins_extra/, or wins_extra_manifest.json.
"""
import argparse
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

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
INST_DIR = os.path.join(BASE, "runs/2026-11-11-2301/data/repo/instances/Example_Instances_FJSSP-WF")
WINS_EXTRA2_DIR = os.path.join(OUT_DIR, "wins_extra2")
LOGS_DIR = os.path.join(OUT_DIR, "logs")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)

import fjsspw  # noqa: E402
import numba_ts  # noqa: E402
import numba_ts_v4  # noqa: E402

TARGETS = [
    dict(label="G3", inst="behnkegeiger18", fjs="Behnke18.fjs", lb=80, table_ub=399, true_bar=399, prev_mk=407, seed=810001),
    dict(label="G6", inst="behnkegeiger60", fjs="Behnke60.fjs", lb=74, table_ub=431, true_bar=370, prev_mk=394, seed=810002),
]


def run_one(cfg, budget_s):
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

    best_mk, best_state, stats = numba_ts_v4.cmrts_v4_search(
        inst_name, nb, time_budget_s=budget_s, seed0=cfg["seed"]
    )
    sched = numba_ts.to_schedule_json(inst_name, nb, best_state[0], best_state[12])
    ok, cmk, errs = fjsspw.check(fjs_path, sched)
    assert ok and cmk == best_mk, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} best={best_mk} errs={errs[:3]}"

    win_path = None
    beats_bar = best_mk < cfg["true_bar"]
    if beats_bar:
        os.makedirs(WINS_EXTRA2_DIR, exist_ok=True)
        win_path = os.path.join(WINS_EXTRA2_DIR, f"{inst_name}_mk{best_mk}_bar{cfg['true_bar']}.json")
        with open(win_path, "w") as wf:
            json.dump(sched, wf)

    return dict(
        label=cfg["label"],
        inst=cfg["inst"],
        name=inst_name,
        lb=cfg["lb"],
        table_ub=cfg["table_ub"],
        true_bar=cfg["true_bar"],
        prev_mk=cfg["prev_mk"],
        mk=int(best_mk),
        vs_prev=int(best_mk) - cfg["prev_mk"],
        vs_bar=int(best_mk) - cfg["true_bar"],
        beats_bar=beats_bar,
        valid=ok,
        seed=cfg["seed"],
        stats=stats,
        secs=round(time.time() - t0, 2),
        win_path=win_path,
    )


def main():
    parser = argparse.ArgumentParser(description="Option 1+2 Combo (numba_ts_v4) Pilot on G3 + G6")
    parser.add_argument("--smoke", action="store_true", help="25s smoke test on G3 (Behnke18)")
    parser.add_argument("--budget", type=float, default=900.0, help="Seconds per instance (default 900s)")
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    if args.smoke:
        print("SMOKE TEST: running 25s v4 (incl CP-SAT seeds) on G3 Behnke18...", flush=True)
        r = run_one(TARGETS[0], 25.0)
        print(
            f"SMOKE OK | {r['label']} {r['name']} | mk={r['mk']} (prev={r['prev_mk']}, bar={r['true_bar']}) | "
            f"cpsat_diag(maxM,avgD,initMK)={r['stats']['cpsat_diag']} | "
            f"evals={r['stats']['evals']:,} | starts={r['stats']['starts']} | secs={r['secs']}",
            flush=True,
        )
        return

    log_path = os.path.join(LOGS_DIR, "pilot_v4_g3_g6.jsonl")
    with open(log_path, "w"):
        pass

    t_all = time.time()
    print(f"Launching {int(args.budget)}s parallel v4 pilot on G3 (Behnke18) + G6 (Behnke60)...", flush=True)
    with ProcessPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_one, c, args.budget): c["fjs"] for c in TARGETS}
        for fut in as_completed(futs):
            r = fut.result()
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            tag = "WIN!" if r["beats_bar"] else ("TIE" if r["vs_bar"] == 0 else f"{r['vs_bar']:+d}")
            print(
                f"  [{r['label']} {r['name']:10s}] v4={r['mk']:4d} vs prev={r['prev_mk']:4d} ({r['vs_prev']:+3d}) | "
                f"bar={r['true_bar']:4d} ({tag}) | cpsat_diag={r['stats']['cpsat_diag'][:3]} | "
                f"evals={r['stats']['evals']:,} | best@{r['stats']['best_at_s']}s | {r['secs']}s",
                flush=True,
            )
    print(f"Pilot v4 complete in {round((time.time() - t_all)/60.0, 2)}m wall.", flush=True)


if __name__ == "__main__":
    main()
