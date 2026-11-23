"""
Final 402/402 Boss Fight on U1 (Hurinkrdata16, bar=981, H <= 980):
  - Stage 1: 60m (3600s) 6-Core Hard-Capped Carlier CP-SAT (seed=930001) + Telegram update
  - Stage 2 (if Stage 1 is UNKNOWN): 90m (5400s) 6-Core Hard-Capped Carlier CP-SAT (seed=930002) + Telegram update

Saves any verified win (< 981) to wins_extra2/. Logs to logs/u1_carlier_60_90.jsonl.
DOES NOT modify best_wins/, best_wins_manifest.json, wins_extra/, or wins_extra_manifest.json.
"""
import json
import os
import subprocess
import sys
import time

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

BASE = "WORKSPACE"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(OUT_DIR, "logs")
TG_SCRIPT = os.path.join(BASE, "scans/2026-11-19-mmlib-solver/phaseB/tg_notify.py")

sys.path.insert(0, OUT_DIR)
from run_u1_u2_final_push import solve_hard_carlier_6w  # noqa: E402


def send_tg(tag, msg):
    os.makedirs(LOGS_DIR, exist_ok=True)
    p = os.path.join(LOGS_DIR, f"tg_{tag}.txt")
    with open(p, "w") as f:
        f.write(msg)
    proc = subprocess.run([sys.executable, TG_SCRIPT, "--file", p], check=False, timeout=30)
    print(f"Telegram ({tag}) exit={proc.returncode}", flush=True)


def main():
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, "u1_carlier_60_90.jsonl")
    with open(log_path, "w"):
        pass

    stages = [
        ("S1_60m", 3600.0, 930001),
        ("S2_90m", 5400.0, 930002),
    ]

    for s_name, budget_s, seed in stages:
        r = solve_hard_carlier_6w("U1", "Hurinkrdata16", "Hurinkrdata16.fjs", 981, budget_s, seed=seed, nw=6)
        r["stage"] = s_name
        with open(log_path, "a") as lf:
            lf.write(json.dumps(r) + "\n")

        if r["outcome"] == "WIN":
            msg = (
                f"FJSSP-W 402/402 (100%) COMPLETE! [{s_name}]\n"
                f"U1 Hurinkrdata16 WIN! mk={r['mk']} < bar=981 ({r['vs_bar']:+d}) in {r['secs']}s!\n"
                f"Total clean wins: 139 (88 best_wins + 39 wins_extra + 12 wins_extra2)."
            )
            send_tg(f"u1_{s_name}", msg)
            return
        elif r["outcome"] == "PROVED_OPTIMAL_AT_BAR":
            msg = (
                f"FJSSP-W 402/402 (100%) RESOLVED! [{s_name}]\n"
                f"U1 Hurinkrdata16 PROVED OPTIMAL at bar=981 (INFEASIBLE <= 980) in {r['secs']}s!\n"
                f"Total clean wins: 138 (88 + 39 + 11) | 68 newly proved optimal."
            )
            send_tg(f"u1_{s_name}", msg)
            return
        else:
            nxt = "Launching Stage 2 (90m)..." if s_name == "S1_60m" else "Both 60m & 90m finished UNKNOWN — ready for a different angle."
            msg = (
                f"FJSSP-W U1 Hurinkrdata16 [{s_name}] finished: {r['outcome']} (H <= 980, {r['secs']}s).\n"
                f"{nxt}"
            )
            send_tg(f"u1_{s_name}", msg)


if __name__ == "__main__":
    main()
