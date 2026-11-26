"""
Play 2 CP-SAT Final Cleanup (play2_cleanup_b5b7.py).
Tests all 54 remaining open small/medium FJSSP-W rows that never saw Play 2 CP-SAT,
using strictly ROUNDED table UBs (fixing the float-floor bug on hurinkedata55 = 5868).
DOES NOT modify best_wins/, best_wins_manifest.json, true_bar_catalog.json, or prior logs.

Tiers (54 instances total, ~20-30m typical wall time):
  1. C1_hurinkedata55 :  1 inst  (bar=5868, 240s, 4p x 2t, 4 GB)
  2. C2_B5_small      : 11 insts (B5 <=30 KB, 240s, 4p x 2t, 4 GB)
  3. C2_B5_med        :  2 insts (Behnke6, Hurinkvdata42, 360s, 2p x 3t, 5 GB)
  4. C3_B7a_le2pct    : 19 insts (Hurink <=2.0% gap, 240s, 4p x 2t, 4 GB)
  5. C4_B7b_gt2pct    : 21 insts (Hurink >2.0% gap, 240s, 4p x 2t, 4 GB)
"""
import csv
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


def build_buckets():
    rounded_ub = {}
    rounded_lb = {}
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f, delimiter=";"):
            k = r["Instance"].strip().lower()
            rounded_ub[k] = int(round(float(r["UB"])))
            rounded_lb[k] = int(round(float(r["LB"])))

    cat = json.load(open(CATALOG_PATH))
    f91 = json.load(open(PR868_PATH))
    pr868_all = {r["instance"].lower().replace(".fjs", "") for r in f91}
    filed_1081 = {
        os.path.basename(p).replace(".json", "").lower()
        for p in glob.glob(os.path.join(BASE, "runs/2026-11-13-0112/claim/object/*.json"))
    }
    won_all = {x["inst"].lower() for x in json.load(open(os.path.join(OUT_DIR, "best_wins_manifest.json")))}

    p2_done = set()
    with open(os.path.join(LOGS_DIR, "play2_cpsat.jsonl")) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            k = r["inst"].lower()
            if k != "hurinkedata55":
                p2_done.add(k)

    best_mk = {}
    for fn in ["halfday_v2.jsonl", "wave2_v2.jsonl", "pilot_v3.jsonl", "play1_v3.jsonl", "play1_v3_overtime.jsonl"]:
        lp = os.path.join(LOGS_DIR, fn)
        if not os.path.exists(lp):
            continue
        with open(lp) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                k = r["inst"].lower()
                if r.get("mk") is not None and (k not in best_mk or r["mk"] < best_mk[k]):
                    best_mk[k] = int(r["mk"])

    for rp in glob.glob(os.path.join(BASE, "runs/2026-11-12-*/attempts/cpsat/report.md")):
        with open(rp) as f:
            for line in f:
                m = re.match(r"\|\s*([a-zA-Z0-9_]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
                if m:
                    k = m.group(1).lower()
                    mk = int(m.group(3))
                    if k not in best_mk or mk < best_mk[k]:
                        best_mk[k] = mk

    c1 = []
    c2_small, c2_med = [], []
    c3_b7a, c4_b7b = [], []

    for k, r in cat.items():
        stem = r["fjs"].replace(".fjs", "").lower()
        if (
            r["is_opt"]
            or r["is_filed"]
            or k in pr868_all
            or stem in pr868_all
            or stem in filed_1081
            or k in won_all
            or k in p2_done
        ):
            continue

        rub = rounded_ub[k]
        rlb = rounded_lb[k]
        cb = r.get("comp_best")
        bar = min(rub, int(cb)) if cb is not None else rub
        kb = r["size_bytes"] // 1024
        rec = dict(
            inst=r["inst"],
            fjs=r["fjs"],
            lb=rlb,
            table_ub=rub,
            true_bar=bar,
            size_bytes=r["size_bytes"],
            kb=kb,
        )

        if k == "hurinkedata55":
            c1.append((0.0, kb, rec))
            continue

        fam = re.match(r"([a-zA-Z]+)", k).group(1)
        if fam in ("behnkegeiger", "dppaulli") and kb >= 100:
            continue

        bm = best_mk.get(k)
        if bm is None:
            continue
        gap = bm - bar
        pct = 100.0 * gap / max(1, bar)
        rec["prev_best_mk"] = bm
        rec["gap"] = gap
        rec["pct"] = round(pct, 2)

        if 3 <= gap <= 10:
            if kb <= 30:
                c2_small.append((pct, kb, rec))
            else:
                c2_med.append((pct, kb, rec))
        elif gap >= 11 and fam.startswith("hurink"):
            if pct <= 2.0:
                c3_b7a.append((pct, kb, rec))
            else:
                c4_b7b.append((pct, kb, rec))

    tiers = [
        ("C1_hurinkedata55", "C1_hurinkedata55", [x[2] for x in c1], 240.0, 4, 2, 4),
        ("C2_B5_small",      "C2_B5_converged",  [x[2] for x in sorted(c2_small, key=lambda x: (x[0], x[1], x[2]["fjs"]))], 240.0, 4, 2, 4),
        ("C2_B5_med",        "C2_B5_converged",  [x[2] for x in sorted(c2_med,   key=lambda x: (x[0], x[1], x[2]["fjs"]))], 360.0, 2, 3, 5),
        ("C3_B7a_le2pct",    "C3_B7a_le2pct",    [x[2] for x in sorted(c3_b7a,   key=lambda x: (x[0], x[1], x[2]["fjs"]))], 240.0, 4, 2, 4),
        ("C4_B7b_gt2pct",    "C4_B7b_gt2pct",    [x[2] for x in sorted(c4_b7b,   key=lambda x: (x[0], x[1], x[2]["fjs"]))], 240.0, 4, 2, 4),
    ]

    counts = tuple((t[0], len(t[2])) for t in tiers)
    assert counts == (
        ("C1_hurinkedata55", 1),
        ("C2_B5_small", 10),
        ("C2_B5_med", 3),
        ("C3_B7a_le2pct", 19),
        ("C4_B7b_gt2pct", 21),
    ), f"Unexpected cleanup tier counts: {counts}"
    assert tiers[0][2][0]["true_bar"] == 5868, f"hurinkedata55 bar={tiers[0][2][0]['true_bar']}"

    for tname, _, rows, *_ in tiers:
        for r in rows:
            fp = os.path.join(INST_DIR, r["fjs"])
            assert r["fjs"] and os.path.isfile(fp), f"Missing .fjs in {tname}: {fp}"

    return tiers


def solve_cleanup_one(task):
    lim = int(task["mem_gb"]) * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    rec = task["rec"]
    tier = task["tier"]
    logical_bucket = task["logical_bucket"]
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
            tier=tier,
            bucket=logical_bucket,
            inst=rec["inst"],
            name=inst_name,
            fjs=rec["fjs"],
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
        tier=tier,
        bucket=logical_bucket,
        inst=rec["inst"],
        name=inst_name,
        fjs=rec["fjs"],
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
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        msg_path = os.path.join(LOGS_DIR, "tg_play2_cleanup.txt")
        with open(msg_path, "w") as f:
            f.write(summary_text)
        subprocess.run([sys.executable, TG_SCRIPT, "--file", msg_path], check=False, timeout=20)
    except Exception as e:
        print(f"Telegram notify error (non-fatal): {e}", flush=True)


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_EXTRA_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "play2_cleanup.jsonl")

    t_all = time.time()
    tiers = build_buckets()
    all_results = []
    tier_summaries = []

    for ti, (tname, lbucket, rows, budget_s, procs, threads, mem_gb) in enumerate(tiers):
        t_t = time.time()
        print(f"\n=== START {tname} ({len(rows)} insts, {int(budget_s)}s each, {procs}p x {threads}t, {mem_gb}GB) ===", flush=True)
        tasks = [
            dict(
                tier=tname, logical_bucket=lbucket, rec=r,
                budget_s=budget_s, threads=threads, mem_gb=mem_gb,
                seed=950000 + ti * 1000 + i * 19,
            )
            for i, r in enumerate(rows)
        ]
        wins = proved = unknown = 0
        with ProcessPoolExecutor(max_workers=procs) as ex:
            futs = {ex.submit(solve_cleanup_one, t): t["rec"]["fjs"] for t in tasks}
            for fut in as_completed(futs):
                res = fut.result()
                all_results.append(res)
                with open(log_path, "a") as lf:
                    lf.write(json.dumps(res) + "\n")
                if res["outcome"] == "WIN":
                    wins += 1
                    print(f"  [{res['name']:16s}] WIN! mk={res['mk']:4d} < bar={res['true_bar']:4d} ({res['vs_bar']:+d}) | {res['secs']}s", flush=True)
                elif res["outcome"] == "PROVED_OPTIMAL_AT_BAR":
                    proved += 1
                    print(f"  [{res['name']:16s}] PROVED OPTIMAL at bar={res['true_bar']:4d} (INFEASIBLE <= {res['true_bar']-1}) | {res['secs']}s", flush=True)
                else:
                    unknown += 1
                    print(f"  [{res['name']:16s}] {res['outcome']} (bar={res['true_bar']:4d}) | {res['secs']}s", flush=True)
        wall_m = round((time.time() - t_t) / 60.0, 1)
        print(f"=== DONE {tname}: {len(rows)} done | wins={wins} | proved_opt={proved} | unknown={unknown} | {wall_m}m wall ===", flush=True)
        tier_summaries.append(dict(tier=tname, bucket=lbucket, done=len(rows), wins=wins, proved=proved, unknown=unknown, wall_m=wall_m))

    all_wins = sorted([r for r in all_results if r["beats_bar"]], key=lambda r: r["vs_bar"])
    total_wall_m = round((time.time() - t_all) / 60.0, 1)
    lines = [
        f"FJSSP-W Play 2 Cleanup COMPLETE ({total_wall_m}m wall, {len(all_results)} insts):",
        f"NEW EXTRA WINS (in wins_extra/): {len(all_wins)} ({sum(r['vs_bar'] for r in all_wins)} pts) | PROVED OPTIMAL: {sum(s['proved'] for s in tier_summaries)} | UNKNOWN: {sum(s['unknown'] for s in tier_summaries)}",
        "",
        "Buckets:",
    ]
    for ts in tier_summaries:
        lines.append(f"• {ts['tier']}: {ts['done']} done, {ts['wins']} wins, {ts['proved']} opt, {ts['unknown']} unk ({ts['wall_m']}m)")
    if all_wins:
        lines.append("")
        lines.append("New Wins:")
        for r in all_wins:
            lines.append(f"• {r['name']}: {r['mk']} vs bar {r['true_bar']} ({r['vs_bar']:+d})")

    summary_txt = "\n".join(lines)
    print("\n" + summary_txt, flush=True)
    send_telegram(summary_txt)


if __name__ == "__main__":
    main()
