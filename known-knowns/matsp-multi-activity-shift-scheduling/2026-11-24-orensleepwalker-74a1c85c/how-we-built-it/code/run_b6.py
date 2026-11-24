"""
Autonomous 2-Hour Runner for MATSP B6 (XL, 110-150 staff, 46 targets).
Uses isolated OS subprocesses (2w x 2t), skips slow Stage 3 HiGHS (s3_secs=0 -> 0.05s greedy
multi-task painter + fast Numba SA), and uses lp_radius=0 on 14d/28d for fast Stage 1.

Waves:
  - Wave 1: B6 7-day  (15 targets)
  - Wave 2: B6 14-day (15 targets)
  - Wave 3: B6 28-day (16 targets, ordered by A ascending; #219 A=14 last)
  - Wave 4: Near-miss & S1-timeout retry pass ONLY on non-wins until --max-hours deadline.

Updates charlie/wins_manifest.json across ALL B1-B6 verified wins after every wave.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOUT_DIR = os.path.dirname(CHARLIE_DIR)
WINS_DIR = os.path.join(CHARLIE_DIR, "wins")
LOGS_DIR = os.path.join(CHARLIE_DIR, "logs")
JSONL_PATH = os.path.join(LOGS_DIR, "run_b6.jsonl")
MANIFEST_PATH = os.path.join(CHARLIE_DIR, "wins_manifest.json")
RANKED_TSV = os.path.join(SCOUT_DIR, "zero/ranked_open.tsv")
SOLVE_MTASK = os.path.join(CHARLIE_DIR, "solve_mtask.py")

sys.path.insert(0, CHARLIE_DIR)
sys.path.insert(0, os.path.join(SCOUT_DIR, "code"))

import matsp  # noqa: E402
import solve_1task as s1  # noqa: E402
import solve_mtask as sm  # noqa: E402
import run_overnight_b3_b4 as ov  # noqa: E402


def load_b6_targets():
    b6_7, b6_14, b6_28 = [], [], []
    with open(RANKED_TSV) as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            iid, stem, rec, lpb = int(parts[0]), parts[1], int(parts[2]), int(parts[3])
            _, h_s, e_s, a_s = stem.split("_")
            h, nE, A = int(h_s), int(e_s), int(a_s)
            if nE >= 110:
                entry = (A, nE, iid, stem, rec, lpb)
                if h == 7:
                    b6_7.append(entry)
                elif h == 14:
                    b6_14.append(entry)
                else:
                    b6_28.append(entry)
    for lst in (b6_7, b6_14, b6_28):
        lst.sort(key=lambda x: (x[0], x[1], x[2]))
    strip = lambda lst: [(iid, stem, rec, lpb) for _, _, iid, stem, rec, lpb in lst]
    return strip(b6_7), strip(b6_14), strip(b6_28)


B6_7, B6_14, B6_28 = load_b6_targets()
ALL_B6 = B6_7 + B6_14 + B6_28

ALL_META = dict(ov.ALL_META)
for iid, stem, rec, lpb in ALL_B6:
    ALL_META[stem] = ("B6", iid, stem, rec, lpb)


def rebuild_manifest_all():
    if not os.path.isdir(WINS_DIR):
        return 0, 0
    rows = []
    tot_delta = 0
    with zipfile.ZipFile(sm.ZIP_PATH) as zf:
        for fn in sorted(os.listdir(WINS_DIR)):
            if not fn.endswith(".xml") or fn.startswith("."):
                continue
            stem = fn[:-4]
            if stem not in ALL_META:
                continue
            bucket, iid, _, rec, lp = ALL_META[stem]
            xml_path = os.path.join(WINS_DIR, fn)
            xml_txt = open(xml_path).read()
            raw_txt = zf.read(f"instances1_225/txt/{stem}.txt").decode("utf-8")
            I = matsp.read_instance(raw_txt)
            S, _ = matsp.read_solution(xml_txt)
            bad, pen = matsp.evaluate(I, S)
            if len(bad) == 0 and pen < rec:
                sha = hashlib.sha256(xml_txt.encode("utf-8")).hexdigest()
                delta = pen - rec
                tot_delta += delta
                rows.append(dict(
                    bucket=bucket, id=iid, stem=stem, lp_bound=lp, record=rec,
                    our_pen=pen, delta=delta, gap_to_lp=pen - lp,
                    violations=0, verify_claim="PASS", sha256=sha, xml_path=xml_path,
                ))
    rows.sort(key=lambda r: (r["bucket"], r["id"]))
    tmp = MANIFEST_PATH + ".tmp"
    with open(tmp, "w") as mf:
        mf.write(json.dumps(rows, indent=2) + "\n")
    os.replace(tmp, MANIFEST_PATH)
    return len(rows), tot_delta


def already_won(stem):
    return os.path.exists(os.path.join(WINS_DIR, f"{stem}.xml"))


def run_single(iid, stem, rec, lpb, s1_s, s2_s, sa_rounds, sa_iters, lp_radius, threads, seed, timeout_s):
    out_json = os.path.join(LOGS_DIR, f"_b6_{stem}_{seed}_{os.getpid()}.json")
    cmd = [
        sys.executable, "-u", SOLVE_MTASK,
        "--bucket", "single",
        "--id", str(iid), "--stem", stem, "--record", str(rec), "--lp", str(lpb),
        "--s1-secs", str(s1_s), "--s2-secs", str(s2_s), "--s3-secs", "0",
        "--sa-rounds", str(sa_rounds), "--sa-iters", str(sa_iters),
        "--lp-radius", str(lp_radius),
        "--threads", str(threads), "--seed", str(seed), "--mem-gb", "6.0",
        "--out-json", out_json,
    ]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, check=False)
        if os.path.exists(out_json):
            r = json.load(open(out_json))
            os.remove(out_json)
            return r
        err = (proc.stderr or proc.stdout or "").strip().splitlines()
        msg = err[-1] if err else f"rc={proc.returncode}"
        return dict(id=iid, stem=stem, record=rec, lp_bound=lpb,
                    best_pen=None, vs_rec=None, win=False, error=f"rc={proc.returncode}: {msg[:120]}",
                    secs=round(time.time() - t0, 1))
    except subprocess.TimeoutExpired:
        if os.path.exists(out_json):
            os.remove(out_json)
        return dict(id=iid, stem=stem, record=rec, lp_bound=lpb,
                    best_pen=None, vs_rec=None, win=False, error=f"TIMEOUT({timeout_s}s)",
                    secs=round(time.time() - t0, 1))
    except Exception as exc:
        if os.path.exists(out_json):
            os.remove(out_json)
        return dict(id=iid, stem=stem, record=rec, lp_bound=lpb,
                    best_pen=None, vs_rec=None, win=False, error=repr(exc),
                    secs=round(time.time() - t0, 1))


def run_wave(wave_name, targets, workers, threads, s1_s, s2_s, sa_rounds, sa_iters, lp_radius, seed_base, deadline):
    if time.time() >= deadline:
        print(f"[SKIP] {wave_name}: deadline reached", flush=True)
        return []
    targets = [t for t in targets if not already_won(t[1])]
    if not targets:
        print(f"[SKIP] {wave_name}: all targets already won!", flush=True)
        return []
    timeout_s = int(s1_s + s2_s + sa_rounds * 22 + 180)
    t0 = time.time()
    print(f"\n=== {wave_name} ({len(targets)} targets, {workers}w x {threads}t, lpr={lp_radius}) ===", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {}
        for idx, (iid, stem, rec, lpb) in enumerate(targets):
            if time.time() >= deadline:
                break
            fut = ex.submit(
                run_single, iid, stem, rec, lpb,
                s1_s, s2_s, sa_rounds, sa_iters, lp_radius, threads,
                seed_base + iid * 37 + idx * 11, timeout_s,
            )
            futs[fut] = (iid, stem, rec, lpb)
        for fut in as_completed(futs):
            iid, stem, rec, lpb = futs[fut]
            r = fut.result()
            r["wave"] = wave_name
            r["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            results.append(r)
            with open(JSONL_PATH, "a") as jf:
                jf.write(json.dumps(r) + "\n")
            vs = r.get("vs_rec")
            tag = "WIN!!" if r.get("win") else (f"{vs:+d}" if vs is not None else f"ERR({r.get('error', r.get('s1_status', '?'))})")
            print(
                f"  [#{iid:3d} {stem:14s}] S1={r.get('s1_obj')} ({r.get('s1_secs')}s) | "
                f"S2v={r.get('s2_viol')} | FINAL={r.get('best_pen')} vs {rec} ({tag}) | {r.get('secs')}s",
                flush=True,
            )
    n_wins, tot_d = rebuild_manifest_all()
    print(f"=== END {wave_name} in {(time.time()-t0)/60.0:.1f}m | Total verified wins (B1-B6): {n_wins} ({tot_d:+d} pts) ===", flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="Autonomous 2-Hour Runner for MATSP B6 (46 XL targets)")
    parser.add_argument("--max-hours", type=float, default=2.0)
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_DIR, exist_ok=True)
    t_start = time.time()
    deadline = t_start + args.max_hours * 3600.0
    n0, d0 = rebuild_manifest_all()
    print(
        f"=== B6 RUN START ({time.strftime('%Y-%m-%d %H:%M:%S')}) | Budget: {args.max_hours:.2f}h | "
        f"B6 targets: {len(B6_7)} (7d) + {len(B6_14)} (14d) + {len(B6_28)} (28d) = {len(ALL_B6)} | "
        f"Prior wins: {n0} ({d0:+d} pts) ===",
        flush=True,
    )

    best_seen = {}

    def record(res_list):
        for r in res_list:
            stem = r["stem"]
            bp = r.get("best_pen")
            prev = best_seen.get(stem)
            if prev is None or (bp is not None and (prev[0] is None or bp < prev[0])):
                best_seen[stem] = (bp, r["record"], r["id"], r["lp_bound"])

    # Wave 1: B6 7-day (15 targets)
    record(run_wave(
        "B6_Wave1_7d", B6_7,
        workers=2, threads=2, s1_s=60.0, s2_s=45.0, sa_rounds=16, sa_iters=4_500_000,
        lp_radius=1, seed_base=110000, deadline=deadline,
    ))

    # Wave 2: B6 14-day (15 targets, lp_radius=0 for fast Stage 1)
    record(run_wave(
        "B6_Wave2_14d", B6_14,
        workers=2, threads=2, s1_s=90.0, s2_s=60.0, sa_rounds=16, sa_iters=4_500_000,
        lp_radius=0, seed_base=120000, deadline=deadline,
    ))

    # Wave 3: B6 28-day (16 targets, lp_radius=0 for fast Stage 1)
    record(run_wave(
        "B6_Wave3_28d", B6_28,
        workers=2, threads=2, s1_s=140.0, s2_s=75.0, sa_rounds=16, sa_iters=4_500_000,
        lp_radius=0, seed_base=130000, deadline=deadline,
    ))

    # Wave 4: Near-miss & S1-timeout retries ONLY on B6 non-wins if time remains
    if time.time() + 300 < deadline:
        non_wins = []
        for stem, (bp, rec, iid, lpb) in best_seen.items():
            if already_won(stem):
                continue
            gap = (bp - rec) if bp is not None else 999999
            non_wins.append((gap, (iid, stem, rec, lpb)))
        non_wins.sort(key=lambda x: x[0])
        batch = [t for _, t in non_wins]
        if batch:
            run_wave(
                "B6_Wave4_Retry", batch,
                workers=2, threads=2, s1_s=220.0, s2_s=90.0, sa_rounds=22, sa_iters=5_500_000,
                lp_radius=0, seed_base=140000, deadline=deadline,
            )

    n_wins, tot_d = rebuild_manifest_all()
    elapsed_m = (time.time() - t_start) / 60.0
    print(f"\n=== B6 RUN COMPLETE in {elapsed_m:.1f}m | Total verified wins (B1-B6): {n_wins} ({tot_d:+d} pts) ===", flush=True)


if __name__ == "__main__":
    main()
