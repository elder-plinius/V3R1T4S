"""
Play 2 FJSSP-W Exact CP-SAT Deadline Snipe (play2_cpsat_snipe.py).
Tests all remaining <= 500 KB open instances in gap [0, 2] plus B6 untouched Fattahi
using the canonical FJSSP-W CP-SAT formulation hard-capped at H = true_bar - 1.

Outcomes per instance:
  - WIN: found feasible schedule with makespan <= true_bar - 1 (verified via fjsspw.check())
  - PROVED_OPTIMAL_AT_BAR: CP-SAT proved INFEASIBLE below true_bar (optimal = true_bar!)
  - UNKNOWN: time budget reached without proof or improvement

Tiers (69 instances total, ~80m typical / ~114m max wall):
  1. P2_B6_fattahi :  9 insts, 120s, 4 procs x 2 threads, 4 GB RLIMIT_AS
  2. P2_small      : 45 insts, 240s, 4 procs x 2 threads, 4 GB RLIMIT_AS
  3. P2_med        : 10 insts, 480s, 2 procs x 3 threads, 5 GB RLIMIT_AS
  4. P2_behnke20   :  5 insts, 600s, 2 procs x 3 threads, 6 GB RLIMIT_AS
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

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
INST_DIR = os.path.join(BASE, "runs/2026-11-11-2301/data/repo/instances/Example_Instances_FJSSP-WF")
CATALOG_PATH = os.path.join(OUT_DIR, "true_bar_catalog.json")
PR868_PATH = os.path.join(BASE, "scans/final_91_records.json")
WINS_DIR = os.path.join(OUT_DIR, "wins")
LOGS_DIR = os.path.join(OUT_DIR, "logs")
TG_SCRIPT = os.path.join(BASE, "scans/2026-11-19-mmlib-solver/phaseB/tg_notify.py")

sys.path.insert(0, os.path.join(BASE, "runs/2026-11-12-1955/attempts/common/code"))
import fjsspw  # noqa: E402
from ortools.sat.python import cp_model  # noqa: E402


class FirstWinStopCallback(cp_model.CpSolverSolutionCallback):
    """Stop Phase A immediately on the first feasible schedule <= true_bar - 1."""

    def __init__(self):
        super().__init__()
        self.found = False

    def on_solution_callback(self):
        self.found = True
        self.StopSearch()


def build_tiers():
    cat = json.load(open(CATALOG_PATH))
    f91 = json.load(open(PR868_PATH))
    pr868_all = {r["instance"].lower().replace(".fjs", "") for r in f91}
    filed_1081 = {
        os.path.basename(p).replace(".json", "").lower()
        for p in glob.glob(os.path.join(BASE, "runs/2026-11-13-0112/claim/object/*.json"))
    }
    won_all = {x["inst"].lower() for x in json.load(open(os.path.join(OUT_DIR, "best_wins_manifest.json")))}

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
                if k not in best_mk or r["mk"] < best_mk[k]:
                    best_mk[k] = r["mk"]

    for rp in glob.glob(os.path.join(BASE, "runs/2026-11-12-*/attempts/cpsat/report.md")):
        with open(rp) as f:
            for line in f:
                m = re.match(r"\|\s*([a-zA-Z0-9_]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
                if m:
                    k = m.group(1).lower()
                    mk = int(m.group(3))
                    if k not in best_mk or mk < best_mk[k]:
                        best_mk[k] = mk

    b6_fattahi, p2_small, p2_med, p2_behnke = [], [], [], []
    for k, r in cat.items():
        stem = r["fjs"].replace(".fjs", "").lower()
        if (
            r["is_opt"]
            or r["is_filed"]
            or k in pr868_all
            or stem in pr868_all
            or stem in filed_1081
            or k in won_all
        ):
            continue
        kb = r["size_bytes"] // 1024
        bar = int(r["true_bar"])
        if k.startswith("fattahi"):
            b6_fattahi.append((kb, 0, r))
            continue
        bm = best_mk.get(k)
        if bm is None:
            continue
        gap = bm - bar
        if 0 <= gap <= 2 and kb <= 500:
            if kb <= 30:
                p2_small.append((gap, kb, r))
            elif kb <= 150:
                p2_med.append((gap, kb, r))
            else:
                p2_behnke.append((gap, kb, r))

    tiers = [
        ("P2_B6_fattahi", [x[2] for x in sorted(b6_fattahi, key=lambda x: (x[0], x[2]["fjs"]))], 120.0, 4, 2, 4),
        ("P2_small",      [x[2] for x in sorted(p2_small,   key=lambda x: (x[0], x[1], x[2]["fjs"]))], 240.0, 4, 2, 4),
        ("P2_med",        [x[2] for x in sorted(p2_med,     key=lambda x: (x[0], x[1], x[2]["fjs"]))], 480.0, 2, 3, 5),
        ("P2_behnke20",   [x[2] for x in sorted(p2_behnke,  key=lambda x: (x[0], x[1], x[2]["fjs"]))], 600.0, 2, 3, 6),
    ]

    counts = tuple((t[0], len(t[1])) for t in tiers)
    assert counts == (
        ("P2_B6_fattahi", 9),
        ("P2_small", 45),
        ("P2_med", 10),
        ("P2_behnke20", 5),
    ), f"Unexpected tier counts: {counts}"

    for tname, rows, _, _, _, _ in tiers:
        for r in rows:
            fp = os.path.join(INST_DIR, r["fjs"])
            assert r["fjs"] and os.path.isfile(fp), f"Missing .fjs in {tname}: {fp}"

    return tiers


def _build_snipe_model(J, M, W, jobs, H):
    m = cp_model.CpModel()
    mk = m.NewIntVar(0, H, "mk")
    S, D, B = {}, {}, {}
    byM, byW = {}, {}
    ivs = []

    for j, ops in enumerate(jobs):
        for o, alt in enumerate(ops):
            s = m.NewIntVar(0, H, "")
            ds = sorted(set(alt.values()))
            d = m.NewIntVarFromDomain(cp_model.Domain.FromValues(ds), "")
            S[j, o] = s
            D[j, o] = d
            e = m.NewIntVar(0, H, "")
            m.Add(e == s + d)

            lits = []
            bm, bw = {}, {}
            for (mm, ww), dur in alt.items():
                b = m.NewBoolVar("")
                B[j, o, mm, ww] = b
                lits.append(b)
                bm.setdefault(mm, []).append(b)
                bw.setdefault(ww, []).append(b)
            m.AddExactlyOne(lits)
            m.Add(d == sum(B[j, o, mm, ww] * dur for (mm, ww), dur in alt.items()))

            for grp, by in ((bm, byM), (bw, byW)):
                for r_id, bs in grp.items():
                    if len(bs) == 1:
                        p = bs[0]
                    else:
                        p = m.NewBoolVar("")
                        m.Add(sum(bs) == p)
                    by.setdefault(r_id, []).append(m.NewOptionalIntervalVar(s, d, e, p, ""))
            ivs.append(m.NewIntervalVar(s, d, e, ""))
            if o > 0:
                m.Add(s >= S[j, o - 1] + D[j, o - 1])
        m.Add(mk >= S[j, len(ops) - 1] + D[j, len(ops) - 1])

    for lst in byM.values():
        m.AddNoOverlap(lst)
    for lst in byW.values():
        m.AddNoOverlap(lst)
    m.AddCumulative(ivs, [1] * len(ivs), min(M, W))
    m.Minimize(mk)
    return m, mk, S, B


def _configure_solver(secs, threads, seed):
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(threads)
    sv.parameters.random_seed = int(seed)
    sv.parameters.use_strong_propagation_in_disjunctive = True
    sv.parameters.use_overload_checker_in_cumulative = True
    sv.parameters.use_hard_precedences_in_cumulative = True
    return sv


def _extract_sched(inst_name, jobs, S, B, sv):
    ops = []
    for (j, o), s_var in S.items():
        (mm, ww), = [(a, b2) for (a, b2) in jobs[j][o] if sv.Value(B[j, o, a, b2])]
        ops.append([j, o, mm, ww, int(sv.Value(s_var)), int(jobs[j][o][(mm, ww)])])
    ops.sort()
    return {"instance": inst_name, "ops": ops}


def solve_snipe_one(task):
    lim = int(task["mem_gb"]) * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    rec = task["rec"]
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
    m, mk_var, S, B = _build_snipe_model(J, M, W, jobs, H)

    # Phase A: find first win <= H (or prove INFEASIBLE <= H)
    sv = _configure_solver(budget_s, threads, seed)
    cb = FirstWinStopCallback()
    st = sv.Solve(m, cb)

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        best_sched = _extract_sched(inst_name, jobs, S, B, sv)
        ok, cmk, errs = fjsspw.check(fjs_path, best_sched)
        assert ok and cmk <= H, f"Checker FAIL {inst_name}: ok={ok} cmk={cmk} H={H} errs={errs[:3]}"
        best_mk = int(cmk)
        final_status = sv.StatusName(st)

        # Phase B: short 15s grace polish strictly below best_mk if still > lb and budget remains
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

        os.makedirs(WINS_DIR, exist_ok=True)
        win_path = os.path.join(WINS_DIR, f"{inst_name}_mk{best_mk}_bar{true_bar}.json")
        with open(win_path, "w") as wf:
            json.dump(best_sched, wf)

        return dict(
            bucket=tier,
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
            stats=dict(evals=0, secs=round(time.time() - t0, 2)),
            secs=round(time.time() - t0, 2),
            win_path=win_path,
        )

    outcome = "PROVED_OPTIMAL_AT_BAR" if st == cp_model.INFEASIBLE else sv.StatusName(st)
    return dict(
        bucket=tier,
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
        stats=dict(evals=0, secs=round(time.time() - t0, 2)),
        secs=round(time.time() - t0, 2),
        win_path=None,
    )


def send_telegram(summary_text):
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        msg_path = os.path.join(LOGS_DIR, "tg_play2_cpsat.txt")
        with open(msg_path, "w") as f:
            f.write(summary_text)
        subprocess.run([sys.executable, TG_SCRIPT, "--file", msg_path], check=False, timeout=20)
    except Exception as e:
        print(f"Telegram notify error (non-fatal): {e}", flush=True)


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "play2_cpsat.jsonl")

    t_all = time.time()
    tiers = build_tiers()
    all_results = []
    tier_summaries = []

    for ti, (tname, rows, budget_s, procs, threads, mem_gb) in enumerate(tiers):
        t_t = time.time()
        print(f"\n=== START {tname} ({len(rows)} insts, {int(budget_s)}s each, {procs}p x {threads}t, {mem_gb}GB) ===", flush=True)
        tasks = [
            dict(
                tier=tname, rec=r, budget_s=budget_s, threads=threads, mem_gb=mem_gb,
                seed=900000 + ti * 10000 + i * 17,
            )
            for i, r in enumerate(rows)
        ]
        wins = 0
        proved = 0
        unknown = 0
        with ProcessPoolExecutor(max_workers=procs) as ex:
            futs = {ex.submit(solve_snipe_one, t): t["rec"]["fjs"] for t in tasks}
            for fut in as_completed(futs):
                res = fut.result()
                all_results.append(res)
                with open(log_path, "a") as lf:
                    lf.write(json.dumps(res) + "\n")
                if res["outcome"] == "WIN":
                    wins += 1
                    print(
                        f"  [{res['name']:16s}] WIN! mk={res['mk']:4d} < bar={res['true_bar']:4d} ({res['vs_bar']:+d}) | {res['secs']}s",
                        flush=True,
                    )
                elif res["outcome"] == "PROVED_OPTIMAL_AT_BAR":
                    proved += 1
                    print(
                        f"  [{res['name']:16s}] PROVED OPTIMAL at bar={res['true_bar']:4d} (INFEASIBLE <= {res['true_bar']-1}) | {res['secs']}s",
                        flush=True,
                    )
                else:
                    unknown += 1
                    print(
                        f"  [{res['name']:16s}] {res['outcome']} (bar={res['true_bar']:4d}) | {res['secs']}s",
                        flush=True,
                    )
        wall_m = round((time.time() - t_t) / 60.0, 1)
        print(f"=== DONE {tname}: {len(rows)} done | wins={wins} | proved_opt={proved} | unknown={unknown} | {wall_m}m wall ===", flush=True)
        tier_summaries.append(dict(tier=tname, done=len(rows), wins=wins, proved=proved, unknown=unknown, wall_m=wall_m))

    all_wins = sorted([r for r in all_results if r["beats_bar"]], key=lambda r: r["vs_bar"])
    total_wall_m = round((time.time() - t_all) / 60.0, 1)
    lines = [
        f"FJSSP-W Play 2 CP-SAT Snipe COMPLETE ({total_wall_m}m wall, {len(all_results)} insts):",
        f"NEW PLAY 2 WINS: {len(all_wins)} ({sum(r['vs_bar'] for r in all_wins)} pts) | PROVED OPTIMAL AT BAR: {sum(s['proved'] for s in tier_summaries)} | UNKNOWN: {sum(s['unknown'] for s in tier_summaries)}",
        "",
        "Tiers:",
    ]
    for ts in tier_summaries:
        lines.append(f"• {ts['tier']}: {ts['done']} done, {ts['wins']} wins, {ts['proved']} opt, {ts['unknown']} unk ({ts['wall_m']}m)")
    if all_wins:
        lines.append("")
        lines.append("Play 2 Wins:")
        for r in all_wins:
            lines.append(f"• {r['name']}: {r['mk']} vs bar {r['true_bar']} ({r['vs_bar']:+d})")

    summary_txt = "\n".join(lines)
    print("\n" + summary_txt, flush=True)
    send_telegram(summary_txt)


if __name__ == "__main__":
    main()
