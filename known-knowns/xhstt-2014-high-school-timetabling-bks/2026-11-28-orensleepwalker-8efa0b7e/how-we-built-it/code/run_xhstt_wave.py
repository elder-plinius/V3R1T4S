"""
Parallel Wave Runner for XHSTT-2014 Targets (`AU-BG-98`, `DK-HG-12`, `DK-VG-09`)
(scans/2026-11-27-xhstt-charlie/run_xhstt_wave.py)
Records exact PIDs & PGIDs in `logs/<wave>_pids.json` per TASK_CHARLIE_xhstt.md rules.
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CHARLIE_DIR, "logs")
PID_LOCK = threading.Lock()


def launch_one(wave_name: str, tid: str, secs: float, workers: int, seed: int, ver: str = "v2"):
    out_j = os.path.join(LOGS_DIR, f"_{wave_name}_{tid}.json")
    log_f = os.path.join(LOGS_DIR, f"{wave_name}_{tid}.log")
    pids_path = os.path.join(LOGS_DIR, f"{wave_name}_pids.json")

    au_script = "solve_au_v2.py" if ver == "v2" else "solve_au_cpsat.py"
    dk_script = "solve_dk_v2.py" if ver == "v2" else "solve_dk_cpsat.py"

    if tid == "AU-BG-98":
        cmd = [
            sys.executable, "-u", os.path.join(CHARLIE_DIR, au_script),
            "--secs", str(secs), "--workers", str(workers), "--seed", str(seed), "--out-json", out_j,
        ]
    else:
        cmd = [
            sys.executable, "-u", os.path.join(CHARLIE_DIR, dk_script),
            "--inst", tid, "--secs", str(secs), "--workers", str(workers), "--seed", str(seed), "--out-json", out_j,
        ]

    with open(log_f, "w") as lf:
        p = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
        with PID_LOCK:
            try:
                pids = json.load(open(pids_path)) if os.path.exists(pids_path) else {}
            except Exception:
                pids = {}
            pids[tid] = {"pid": p.pid, "pgid": os.getpgid(p.pid), "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
            open(pids_path, "w").write(json.dumps(pids, indent=2) + "\n")
        print(f"  [STARTED] {tid:10s} | pid={p.pid} pgid={os.getpgid(p.pid)} -> {log_f}", flush=True)
        rc = p.wait(timeout=int(secs + 180))

    if os.path.exists(out_j):
        r = json.load(open(out_j))
        os.remove(out_j)
        return r
    return dict(inst=tid, win=False, error=f"rc={rc}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wave", type=str, required=True)
    parser.add_argument("--targets", type=str, default="AU-BG-98:201,DK-HG-12:301,DK-VG-09:401")
    parser.add_argument("--secs", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    pids_path = os.path.join(LOGS_DIR, f"{args.wave}_pids.json")
    jsonl_path = os.path.join(LOGS_DIR, f"{args.wave}.jsonl")
    if os.path.exists(pids_path):
        os.remove(pids_path)

    items = []
    for raw in args.targets.split(","):
        tid, sd = raw.strip().split(":")
        items.append((tid.strip(), int(sd)))

    t0 = time.time()
    print(f"=== XHSTT WAVE {args.wave} START ({time.strftime('%Y-%m-%d %H:%M:%S')}) | {len(items)} targets x {args.secs:.0f}s ===", flush=True)
    with ThreadPoolExecutor(max_workers=len(items)) as ex:
        futs = {ex.submit(launch_one, args.wave, tid, args.secs, args.workers, sd): tid for tid, sd in items}
        for fut in as_completed(futs):
            r = fut.result()
            r["wave"] = args.wave
            r["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            with open(jsonl_path, "a") as jf:
                jf.write(json.dumps(r) + "\n")
            tag = "WIN!!" if r.get("win") else "no_win"
            print(
                f"  [DONE] {r['inst']:10s} | rec={r.get('record')} -> best={r.get('best')} ({tag}) | "
                f"steps={r.get('steps')} imp={r.get('improvements')} plat={r.get('plateau_moves')} | {r.get('secs')}s",
                flush=True,
            )
    if os.path.exists(pids_path):
        os.remove(pids_path)
    print(f"=== XHSTT WAVE {args.wave} COMPLETE in {(time.time()-t0)/60.0:.1f}m ===", flush=True)


if __name__ == "__main__":
    main()
