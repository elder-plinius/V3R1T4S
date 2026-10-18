#!/usr/bin/env python3
"""
Run CLSS Coupled Seam Surgery (seam_surgery_ihtp v2) with fixed settings
(nra_sec=1.5, coupled_sec=1.0, seed=42) across all 60 IHTC-2024 instances (i01..i30, m01..m30),
and validate every improved solution with the official IHTP_Validator.
"""
import concurrent.futures
import json
import os
import re
import subprocess
import time

WORK_DIR = os.environ.get("IHTC_WORK", ".")
OUT_DIR = os.path.join(WORK_DIR, "solutions_improved")
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(WORK_DIR, "index.html")) as f:
    html = f.read()
ROWS = re.findall(r"<td>([im]\d+)</td>\s*<td[^>]*>(\d+)</td>", html)


def run_one(item):
    inst_id, table_cost_str = item
    table_cost = int(table_cost_str)
    sub = "public" if inst_id.startswith("i") else "hidden"
    inst_path = os.path.join(WORK_DIR, "instances", f"{inst_id}.json")
    sol_path = os.path.join(WORK_DIR, "repo", "assets", "files", "solutions", sub, "IHTP", f"sol_{inst_id}.json")
    out_sol = os.path.join(OUT_DIR, f"sol_{inst_id}.json")

    t0 = time.time()
    out = subprocess.check_output([
        os.path.join(WORK_DIR, "seam_surgery_ihtp"),
        inst_path,
        sol_path,
        out_sol,
        "1.5",
        "1.0",
        "42",
    ]).decode().strip()
    dt = time.time() - t0

    m = re.search(r"orig=(\d+) \(nra=(\d+)\) after_nra=(\d+) final=(\d+) \(nra=(\d+)\) viol=(\d+) gain=(\d+)", out)
    orig_cost = int(m.group(1))
    after_nra = int(m.group(3))
    final_cost = int(m.group(4))
    viol = int(m.group(6))
    gain = int(m.group(7))

    val_viol = -1
    val_cost = orig_cost
    bar = min(table_cost, orig_cost)
    strict_win = False
    if gain > 0 and os.path.exists(out_sol):
        v_out = subprocess.check_output([os.path.join(WORK_DIR, "IHTP_Validator"), inst_path, out_sol]).decode()
        val_viol = int(re.search(r"Total violations = (\d+)", v_out).group(1))
        val_cost = int(re.search(r"Total cost = (\d+)", v_out).group(1))
        if val_viol == 0 and val_cost < bar:
            strict_win = True

    return {
        "id": inst_id,
        "table_cost": table_cost,
        "posted_sol_cost": orig_cost,
        "bar": bar,
        "after_nra": after_nra,
        "final_cost": val_cost if gain > 0 else orig_cost,
        "viol": val_viol if gain > 0 else 0,
        "gain_vs_bar": bar - (val_cost if gain > 0 else orig_cost),
        "strict_win": strict_win,
        "wall_s": round(dt, 2),
    }


if __name__ == "__main__":
    t_start = time.time()
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for res in ex.map(run_one, ROWS):
            results.append(res)
            if res["strict_win"]:
                print(
                    f"[WIN] {res['id']}: bar={res['bar']} (table={res['table_cost']}) -> "
                    f"{res['final_cost']} (gain={res['gain_vs_bar']}, after_nra={res['after_nra']}, viol={res['viol']}, {res['wall_s']}s)",
                    flush=True,
                )

    wins = [r for r in results if r["strict_win"]]
    i_wins = [r for r in wins if r["id"].startswith("i")]
    m_wins = [r for r in wins if r["id"].startswith("m")]
    print(f"\n=== SUMMARY (seed=42, nra_sec=1.5, coupled_sec=1.0, total_wall={time.time()-t_start:.1f}s) ===")
    print(f"Total strict wins: {len(wins)} / 60 (public i-instances: {len(i_wins)}, hidden m-instances: {len(m_wins)})")
    for w in sorted(wins, key=lambda x: -x["gain_vs_bar"]):
        print(f"  {w['id']}: {w['bar']} -> {w['final_cost']} (-{w['gain_vs_bar']}) [viol={w['viol']}]")

    with open("benchmark_60_results.json", "w") as f:
        json.dump(results, f, indent=2)
