"""
Cleanup Runner for the final 14 open MATSP instances across B4 + B5 + B6:
  Wave A (6 targets): 28d S1-timeouts (#193, #202, #212, #217, #218, #219)
                      using direct LP-rounded Stage 1 (s1_secs=0) + Stage 2 + 24x6M SA.
  Wave B (8 targets): Counting-tight snipers (#23, #98, #168, #173, #108, #113, #128, #143)
                      using Stage 1 MIP + upgraded Stage 2 (min-work surplus tie-breaker)
                      + 32x10M deep SA with ultra-cold 0.005 polish.
"""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CHARLIE_DIR, "logs")
JSONL_PATH = os.path.join(LOGS_DIR, "cleanup14.jsonl")
SOLVE_MTASK = os.path.join(CHARLIE_DIR, "solve_mtask.py")

sys.path.insert(0, CHARLIE_DIR)
import run_b6  # noqa: E402

WAVE_A = [
    # (iid, stem, rec, lp, s1, s2, s3, rounds, iters, lpr)
    (193, "193_28_90_6",   14741, 12749, 0, 75, 0, 24, 6_000_000, 0),
    (202, "202_28_110_6",  19760, 14997, 0, 75, 0, 24, 6_000_000, 0),
    (212, "212_28_130_7",  22831, 17191, 0, 75, 0, 24, 6_000_000, 0),
    (217, "217_28_140_7",  22719, 17158, 0, 75, 0, 24, 6_000_000, 0),
    (218, "218_28_140_10", 21729, 19997, 0, 75, 0, 24, 6_000_000, 0),
    (219, "219_28_140_14", 18990, 18988, 0, 75, 0, 24, 6_000_000, 0),
]

WAVE_B = [
    (23,  "23_7_50_4",     1927,  1905,  45, 90, 25, 36, 10_000_000, 1),
    (98,  "98_14_50_4",    3867,  3855,  60, 90, 0,  32, 10_000_000, 0),
    (168, "168_28_40_3",   6000,  5890,  60, 90, 0,  32, 10_000_000, 0),
    (173, "173_28_50_4",   7399,  7393,  75, 90, 0,  32, 10_000_000, 0),
    (108, "108_14_70_5",   5103,  4947,  60, 90, 0,  32, 10_000_000, 0),
    (113, "113_14_80_6",   6356,  6026,  60, 90, 0,  32, 10_000_000, 0),
    (128, "128_14_110_8",  8715,  8067,  60, 90, 0,  32, 10_000_000, 0),
    (143, "143_14_140_10", 11255, 10231, 60, 90, 0,  32, 10_000_000, 0),
]


def run_one(job, seed):
    iid, stem, rec, lp, s1, s2, s3, rds, iters, lpr = job
    out_j = os.path.join(LOGS_DIR, f"_c14_{stem}_{seed}_{os.getpid()}.json")
    cmd = [
        sys.executable, "-u", SOLVE_MTASK,
        "--bucket", "single",
        "--id", str(iid), "--stem", stem, "--record", str(rec), "--lp", str(lp),
        "--s1-secs", str(s1), "--s2-secs", str(s2), "--s3-secs", str(s3),
        "--sa-rounds", str(rds), "--sa-iters", str(iters),
        "--lp-radius", str(lpr), "--threads", "2", "--seed", str(seed), "--mem-gb", "6.0",
        "--out-json", out_j,
    ]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900, check=False)
        if os.path.exists(out_j):
            r = json.load(open(out_j))
            os.remove(out_j)
            return r
        err = (proc.stderr or proc.stdout or "").strip().splitlines()
        return dict(id=iid, stem=stem, record=rec, lp_bound=lp, best_pen=None, vs_rec=None, win=False,
                    error=(err[-1] if err else f"rc={proc.returncode}")[:120], secs=round(time.time() - t0, 1))
    except Exception as exc:
        if os.path.exists(out_j):
            os.remove(out_j)
        return dict(id=iid, stem=stem, record=rec, lp_bound=lp, best_pen=None, vs_rec=None, win=False,
                    error=repr(exc), secs=round(time.time() - t0, 1))


def run_wave(name, jobs, seed_base):
    t0 = time.time()
    print(f"\n=== {name} ({len(jobs)} targets, 2w x 2t) ===", flush=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_one, j, seed_base + j[0] * 41): j for j in jobs}
        for fut in as_completed(futs):
            r = fut.result()
            r["wave"] = name
            r["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            with open(JSONL_PATH, "a") as jf:
                jf.write(json.dumps(r) + "\n")
            vs = r.get("vs_rec")
            tag = "WIN!!" if r.get("win") else (f"{vs:+d}" if vs is not None else f"ERR({r.get('error', r.get('s1_status', '?'))})")
            print(
                f"  [#{r['id']:3d} {r['stem']:14s}] S1={r.get('s1_obj')} ({r.get('s1_st')}, {r.get('s1_secs')}s) | "
                f"S2v={r.get('s2_viol')} | FINAL={r.get('best_pen')} vs {r['record']} ({tag}) | {r.get('secs')}s",
                flush=True,
            )
    n_wins, tot_d = run_b6.rebuild_manifest_all()
    print(f"=== END {name} in {(time.time()-t0)/60.0:.1f}m | Total verified wins (B1-B6): {n_wins} ({tot_d:+d} pts) ===", flush=True)


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    t_all = time.time()
    run_wave("Cleanup14_WaveA_LP_Rounded_28d", WAVE_A, 210000)
    run_wave("Cleanup14_WaveB_TightSnipers", WAVE_B, 220000)
    n_wins, tot_d = run_b6.rebuild_manifest_all()
    print(f"\n=== CLEANUP14 COMPLETE in {(time.time()-t_all)/60.0:.1f}m | Total verified wins: {n_wins}/123 ({tot_d:+d} pts) ===", flush=True)


if __name__ == "__main__":
    main()
