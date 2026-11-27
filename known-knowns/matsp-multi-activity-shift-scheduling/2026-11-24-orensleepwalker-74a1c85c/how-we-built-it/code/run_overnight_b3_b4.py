"""
Autonomous Overnight Runner for MATSP B3 + B4 + B5 overflow (subprocess-isolated, crash-proof).
Each target runs in its own fresh OS subprocess so:
  - 100% of HiGHS / CP-SAT memory is returned to the OS after every instance.
  - A single OOM or abort can NEVER kill other workers (zero BrokenProcessPool!).
  - Resuming skips all already-won instances automatically via charlie/wins/<stem>.xml.

Waves:
  - Wave 1-2: B3 (skipped automatically if already 18/18 won)
  - Wave 3:   B4 Tight Snipers (skipped if --skip-wave3 or already won)
  - Wave 4:   B4 Wide (9 targets, A=3..4)
  - Wave 5:   Up to 2 retry passes ONLY on B3+B4 non-wins (ties & near-misses; NEVER deepens wins)
  - Wave 6:   B5 overflow (70-100 staff, 36 targets, easiest-first) for remaining time
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
JSONL_PATH = os.path.join(LOGS_DIR, "overnight_b3_b4.jsonl")
MANIFEST_PATH = os.path.join(CHARLIE_DIR, "wins_manifest.json")
RANKED_TSV = os.path.join(SCOUT_DIR, "zero/ranked_open.tsv")
SOLVE_MTASK = os.path.join(CHARLIE_DIR, "solve_mtask.py")

sys.path.insert(0, CHARLIE_DIR)
sys.path.insert(0, os.path.join(SCOUT_DIR, "code"))

import matsp  # noqa: E402
import solve_1task as s1  # noqa: E402
import solve_mtask as sm  # noqa: E402


def load_b5_targets():
    b5 = []
    with open(RANKED_TSV) as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            iid, stem, rec, lpb = int(parts[0]), parts[1], int(parts[2]), int(parts[3])
            _, h_s, e_s, a_s = stem.split("_")
            h, nE, A = int(h_s), int(e_s), int(a_s)
            if 70 <= nE <= 100:
                b5.append((h, A, nE, iid, stem, rec, lpb))
    b5.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    return [(iid, stem, rec, lpb) for _, _, _, iid, stem, rec, lpb in b5]


B5_TARGETS = load_b5_targets()

ALL_META = {}
for bname, tlist in [
    ("B1", s1.B1_TARGETS),
    ("B2", s1.B2_TARGETS),
    ("B3", sm.B3_7_14_TARGETS + sm.B3_28_TARGETS),
    ("B4", sm.B4_TIGHT_TARGETS + sm.B4_WIDE_TARGETS),
    ("B5", B5_TARGETS),
]:
    for iid, stem, rec, lpb in tlist:
        ALL_META[stem] = (bname, iid, stem, rec, lpb)


def rebuild_manifest():
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


def load_previous_best():
    """Seed best_seen from existing overnight_b3_b4.jsonl so resumes know prior near-misses."""
    best_seen = {}
    if not os.path.exists(JSONL_PATH):
        return best_seen
    with open(JSONL_PATH) as jf:
        for line in jf:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            stem = r.get("stem")
            if not stem:
                continue
            bp = r.get("best_pen")
            s1b = r.get("s1_bd") or r.get("lp_bound")
            prev = best_seen.get(stem)
            if prev is None:
                best_seen[stem] = (bp, s1b, r["record"], r["id"], r["lp_bound"])
            else:
                old_bp, old_s1b, rec, iid, lpb = prev
                new_bp = bp if (bp is not None and (old_bp is None or bp < old_bp)) else old_bp
                new_s1b = max(old_s1b or 0, s1b or 0)
                best_seen[stem] = (new_bp, new_s1b, rec, iid, lpb)
    return best_seen


def run_single_subprocess(iid, stem, rec, lpb, s1_s, s2_s, s3_s, sa_rounds, sa_iters, threads, seed, mem_gb, timeout_s):
    out_json = os.path.join(LOGS_DIR, f"_res_{stem}_{seed}_{os.getpid()}.json")
    cmd = [
        sys.executable, "-u", SOLVE_MTASK,
        "--bucket", "single",
        "--id", str(iid), "--stem", stem, "--record", str(rec), "--lp", str(lpb),
        "--s1-secs", str(s1_s), "--s2-secs", str(s2_s), "--s3-secs", str(s3_s),
        "--sa-rounds", str(sa_rounds), "--sa-iters", str(sa_iters),
        "--threads", str(threads), "--seed", str(seed), "--mem-gb", str(mem_gb),
        "--out-json", out_json,
    ]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, check=False)
        if os.path.exists(out_json):
            with open(out_json) as jf:
                r = json.load(jf)
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


def run_wave(wave_name, targets, workers, threads, s1_s, s2_s, s3_s, sa_rounds, sa_iters, seed_base, deadline, skip_won=True):
    if time.time() >= deadline:
        print(f"[SKIP] {wave_name}: deadline reached", flush=True)
        return []
    if skip_won:
        targets = [t for t in targets if not already_won(t[1])]
        if not targets:
            print(f"[SKIP] {wave_name}: all targets already won!", flush=True)
            return []
    mem_gb = 6.0
    timeout_s = int(s1_s + s2_s + s3_s + sa_rounds * 25 + 180)
    t0 = time.time()
    print(f"\n=== {wave_name} ({len(targets)} targets, {workers}w x {threads}t, isolated subprocesses) ===", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {}
        for idx, (iid, stem, rec, lpb) in enumerate(targets):
            if time.time() >= deadline:
                break
            fut = ex.submit(
                run_single_subprocess, iid, stem, rec, lpb,
                s1_s, s2_s, s3_s, sa_rounds, sa_iters, threads,
                seed_base + iid * 31 + idx * 7, mem_gb, timeout_s,
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
                f"  [#{iid:3d} {stem:12s}] S1={r.get('s1_obj')} (bd={r.get('s1_bd')}, {r.get('s1_secs')}s) | "
                f"S2v={r.get('s2_viol')} | S3={r.get('s3_st')} | FINAL={r.get('best_pen')} vs {rec} ({tag}) | {r.get('secs')}s",
                flush=True,
            )
    n_wins, tot_d = rebuild_manifest()
    print(f"=== END {wave_name} in {(time.time()-t0)/60.0:.1f}m | Total verified wins (B1-B5): {n_wins} ({tot_d:+d} pts) ===", flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description="Autonomous Overnight Runner for MATSP B3 + B4 + B5")
    parser.add_argument("--max-hours", type=float, default=5.8)
    parser.add_argument("--skip-wave3", action="store_true", help="Skip initial Wave 3 (already ran before resume)")
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(WINS_DIR, exist_ok=True)
    t_start = time.time()
    deadline = t_start + args.max_hours * 3600.0

    best_seen = load_previous_best()
    n0, d0 = rebuild_manifest()
    print(
        f"=== OVERNIGHT RESUME ({time.strftime('%Y-%m-%d %H:%M:%S')}) | Budget: {args.max_hours:.2f}h | "
        f"Existing verified wins: {n0} ({d0:+d} pts) | B5 pool: {len(B5_TARGETS)} ===",
        flush=True,
    )

    def record_results(res_list):
        for r in res_list:
            stem = r["stem"]
            bp = r.get("best_pen")
            s1b = r.get("s1_bd") or r.get("lp_bound")
            prev = best_seen.get(stem)
            if prev is None:
                best_seen[stem] = (bp, s1b, r["record"], r["id"], r["lp_bound"])
            else:
                old_bp, old_s1b, rec, iid, lpb = prev
                new_bp = bp if (bp is not None and (old_bp is None or bp < old_bp)) else old_bp
                new_s1b = max(old_s1b or 0, s1b or 0)
                best_seen[stem] = (new_bp, new_s1b, rec, iid, lpb)

    # Wave 1-2: B3 (auto-skipped since 18/18 already won!)
    record_results(run_wave(
        "Wave1_B3_7_14", sm.B3_7_14_TARGETS,
        workers=3, threads=2, s1_s=60.0, s2_s=45.0, s3_s=25.0,
        sa_rounds=16, sa_iters=4_500_000, seed_base=10000, deadline=deadline, skip_won=True,
    ))
    record_results(run_wave(
        "Wave2_B3_28", sm.B3_28_TARGETS,
        workers=2, threads=2, s1_s=90.0, s2_s=75.0, s3_s=35.0,
        sa_rounds=16, sa_iters=5_000_000, seed_base=20000, deadline=deadline, skip_won=True,
    ))

    # Wave 3: B4 Tight Snipers (optional skip if already ran)
    if not args.skip_wave3:
        record_results(run_wave(
            "Wave3_B4_Tight", sm.B4_TIGHT_TARGETS,
            workers=2, threads=2, s1_s=90.0, s2_s=75.0, s3_s=40.0,
            sa_rounds=20, sa_iters=5_000_000, seed_base=30000, deadline=deadline, skip_won=True,
        ))

    # Wave 4: B4 Wide (9 targets, A=3..4)
    record_results(run_wave(
        "Wave4_B4_Wide", sm.B4_WIDE_TARGETS,
        workers=2, threads=2, s1_s=90.0, s2_s=75.0, s3_s=40.0,
        sa_rounds=18, sa_iters=5_000_000, seed_base=40000, deadline=deadline, skip_won=True,
    ))

    # Wave 5: Up to 2 retry passes ONLY on B3+B4 non-wins (ties & near-misses — NEVER deepen wins!)
    b3_b4_stems = {stem for _, stem, _, _ in sm.ALL_B3_B4}
    for retry_idx in (1, 2):
        if time.time() + 480 >= deadline:
            break
        non_wins = []
        for stem, (bp, s1b, rec, iid, lpb) in best_seen.items():
            if stem not in b3_b4_stems or already_won(stem):
                continue
            if s1b is not None and s1b >= rec:
                continue
            gap = (bp - rec) if bp is not None else 999999
            non_wins.append((gap, (iid, stem, rec, lpb)))
        non_wins.sort(key=lambda x: x[0])
        batch = [t for _, t in non_wins[:8]]
        if not batch:
            print(f"[Wave5_Retry_{retry_idx}] Zero open B3+B4 near-misses remaining!", flush=True)
            break
        record_results(run_wave(
            f"Wave5_NearMissRetry_{retry_idx}", batch,
            workers=2, threads=2, s1_s=90.0, s2_s=90.0, s3_s=45.0,
            sa_rounds=24, sa_iters=6_000_000, seed_base=60000 + retry_idx * 10000,
            deadline=deadline, skip_won=True,
        ))

    # Wave 6: Attack B5 (70-100 staff, easiest-first in chunks of 6) with all remaining time!
    b5_idx = 0
    chunk_num = 0
    while b5_idx < len(B5_TARGETS) and time.time() + 300 < deadline:
        chunk_num += 1
        chunk = B5_TARGETS[b5_idx : b5_idx + 6]
        b5_idx += 6
        run_wave(
            f"Wave6_B5_Chunk_{chunk_num}", chunk,
            workers=2, threads=2, s1_s=90.0, s2_s=75.0, s3_s=40.0,
            sa_rounds=16, sa_iters=4_500_000, seed_base=80000 + chunk_num * 1000,
            deadline=deadline, skip_won=True,
        )

    n_wins, tot_d = rebuild_manifest()
    elapsed_h = (time.time() - t_start) / 3600.0
    print(f"\n=== OVERNIGHT COMPLETE in {elapsed_h:.2f}h | Total verified wins (B1-B5): {n_wins} ({tot_d:+d} pts) ===", flush=True)


if __name__ == "__main__":
    main()
