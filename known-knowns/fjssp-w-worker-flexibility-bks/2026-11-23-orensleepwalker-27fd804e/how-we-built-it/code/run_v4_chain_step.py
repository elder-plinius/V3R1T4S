"""
4-Step numba_ts_v4.py Chain Runner (run_v4_chain_step.py) on the 8 remaining open FJSSP-W targets:
  - Step 1 (--step 1): All open Gs (G1, G2, G4, G5), 15m (900s), max_workers=4
  - Step 2 (--step 2): All open Us (U1, U2, U3, U5), 15m (900s), max_workers=4
  - Step 3 (--step 3): Remaining survivors (Gs first, Us second), 30m (1800s), max_workers=4
  - Step 4 (--step 4): Remaining survivors (Gs first, Us second), 45m (2700s), max_workers=4

Saves any verified win (< true_bar) to wins_extra2/. Logs all runs to logs/v4_chain.jsonl.
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
os.environ["NUMBA_NUM_THREADS"] = "1"

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
INST_DIR = os.path.join(BASE, "runs/2026-11-11-2301/data/repo/instances/Example_Instances_FJSSP-WF")
CSV_PATH = os.path.join(BASE, "runs/2026-11-12-1955/data/best_known_live.csv")
CATALOG_PATH = os.path.join(OUT_DIR, "true_bar_catalog.json")
PR868_PATH = os.path.join(BASE, "scans/final_91_records.json")
WINS_EXTRA2_DIR = os.path.join(OUT_DIR, "wins_extra2")
LOGS_DIR = os.path.join(OUT_DIR, "logs")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
sys.path.insert(0, OUT_DIR)

import fjsspw  # noqa: E402
import numba_ts  # noqa: E402
import numba_ts_v4  # noqa: E402

POOL_SPECS = [
    dict(label="G1", group="G", name="Behnke16", prev_mk=425),
    dict(label="G2", group="G", name="Behnke17", prev_mk=419),
    dict(label="G4", group="G", name="Behnke19", prev_mk=434),
    dict(label="G5", group="G", name="Behnke20", prev_mk=426),
    dict(label="U1", group="U", name="Hurinkrdata16", prev_mk=1003),
    dict(label="U2", group="U", name="BrandimarteMk2", prev_mk=26),
    dict(label="U3", group="U", name="Hurinkrdata35", prev_mk=1577),
    dict(label="U5", group="U", name="Hurinkvdata30", prev_mk=1022),
]

STEP_BUDGET_S = {1: 900.0, 2: 900.0, 3: 1800.0, 4: 2700.0}


def build_open_pool(log_path):
    """Build current open targets from POOL_SPECS excluding anything won in wins_extra2/."""
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

    best_logged = {}
    if os.path.exists(log_path):
        with open(log_path) as lf:
            for line in lf:
                if not line.strip():
                    continue
                row = json.loads(line)
                nm = row["name"]
                if nm not in best_logged or row["mk"] < best_logged[nm]:
                    best_logged[nm] = int(row["mk"])

    pool = []
    for sp in POOL_SPECS:
        nm = sp["name"]
        c = by_name[nm]
        k = c["inst"].lower()
        stem = nm.lower()
        assert k not in pr868_all and stem not in pr868_all, f"Overlap PR868: {nm}"
        assert k not in filed_1081 and stem not in filed_1081, f"Overlap PR1081: {nm}"
        assert k not in won_best and stem not in won_best, f"Overlap best_wins: {nm}"
        assert k not in won_extra and stem not in won_extra, f"Overlap wins_extra: {nm}"
        if stem in won_extra2:
            continue
        fjs_path = os.path.join(INST_DIR, c["fjs"])
        assert os.path.isfile(fjs_path), f"Missing .fjs: {fjs_path}"
        rub = rounded_ub[k]
        cb = c.get("comp_best")
        true_bar = min(rub, int(cb)) if cb is not None else rub
        prev_best = min(sp["prev_mk"], best_logged.get(nm, sp["prev_mk"]))
        pool.append(dict(
            label=sp["label"],
            group=sp["group"],
            inst=c["inst"],
            name=nm,
            fjs=c["fjs"],
            lb=rounded_lb[k],
            table_ub=rub,
            true_bar=true_bar,
            prev_mk=sp["prev_mk"],
            best_so_far=prev_best,
        ))
    return pool


def run_one(cfg, step, budget_s, seed):
    lim = 4 * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    fjs_path = os.path.join(INST_DIR, cfg["fjs"])
    inst_name = cfg["name"]
    J, M, W, jobs = fjsspw.parse(fjs_path)
    nb = numba_ts.build_numba_instance(J, M, W, jobs)

    best_mk, best_state, stats = numba_ts_v4.cmrts_v4_search(
        inst_name, nb, time_budget_s=budget_s, seed0=seed
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
        step=step,
        label=cfg["label"],
        group=cfg["group"],
        inst=cfg["inst"],
        name=inst_name,
        lb=cfg["lb"],
        table_ub=cfg["table_ub"],
        true_bar=cfg["true_bar"],
        prev_mk=cfg["prev_mk"],
        best_before=cfg["best_so_far"],
        mk=int(best_mk),
        vs_prev=int(best_mk) - cfg["prev_mk"],
        vs_bar=int(best_mk) - cfg["true_bar"],
        beats_bar=beats_bar,
        valid=ok,
        seed=seed,
        stats=stats,
        secs=round(time.time() - t0, 2),
        win_path=win_path,
    )


def run_wave(wave_name, items, step, budget_s, log_path):
    if not items:
        return []
    print(
        f"  -- {wave_name}: {[x['label'] + ':' + x['name'] for x in items]} ({int(budget_s)}s each, {len(items)}w) --",
        flush=True,
    )
    res_list = []
    with ProcessPoolExecutor(max_workers=min(4, len(items))) as ex:
        futs = {}
        for idx, cfg in enumerate(items):
            seed = 820000 + step * 1000 + idx * 37
            futs[ex.submit(run_one, cfg, step, budget_s, seed)] = cfg
        for fut in as_completed(futs):
            r = fut.result()
            res_list.append(r)
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            tag = "WIN!" if r["beats_bar"] else ("TIE" if r["vs_bar"] == 0 else f"{r['vs_bar']:+d}")
            print(
                f"    [{r['label']} {r['name']:14s}] mk={r['mk']:4d} vs orig={r['prev_mk']:4d} ({r['vs_prev']:+4d}) | "
                f"bar={r['true_bar']:4d} ({tag}) | evals={r['stats']['evals']:,} | best@{r['stats']['best_at_s']}s | {r['secs']}s",
                flush=True,
            )
    return res_list


def main():
    parser = argparse.ArgumentParser(description="Run one step of the 4-step v4 chain on remaining Gs + Us")
    parser.add_argument("--step", type=int, required=True, choices=[1, 2, 3, 4])
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "v4_chain.jsonl")
    open_pool = build_open_pool(log_path)
    budget_s = STEP_BUDGET_S[args.step]

    if args.step == 1:
        selected = [x for x in open_pool if x["group"] == "G"]
        waves = [("Step 1 Gs", selected)]
    elif args.step == 2:
        selected = [x for x in open_pool if x["group"] == "U"]
        waves = [("Step 2 Us", selected)]
    else:
        gs = [x for x in open_pool if x["group"] == "G"]
        us = [x for x in open_pool if x["group"] == "U"]
        selected = gs + us
        if len(selected) <= 4:
            waves = [(f"Step {args.step} All Survivors (Gs+Us)", selected)]
        else:
            waves = [(f"Step {args.step} Wave 1 (Gs)", gs), (f"Step {args.step} Wave 2 (Us)", us)]

    t_all = time.time()
    print(
        f"=== V4 CHAIN STEP {args.step} ({len(selected)} targets, {int(budget_s)}s = {int(budget_s//60)}m budget) ===",
        flush=True,
    )
    if not selected:
        print(f"No open targets remain for Step {args.step}; exiting.", flush=True)
        return

    all_res = []
    for wname, items in waves:
        all_res.extend(run_wave(wname, items, args.step, budget_s, log_path))

    wins = [r for r in all_res if r["beats_bar"]]
    surv = [r for r in all_res if not r["beats_bar"]]
    print(
        f"=== DONE STEP {args.step} in {round((time.time() - t_all)/60.0, 2)}m: "
        f"{len(wins)} WIN(S), {len(surv)} SURVIVOR(S) ===",
        flush=True,
    )


if __name__ == "__main__":
    main()
