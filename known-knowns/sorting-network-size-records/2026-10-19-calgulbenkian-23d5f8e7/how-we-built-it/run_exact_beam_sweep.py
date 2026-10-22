import os
import glob
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

with open("data/all_networks.json") as f:
    db = json.load(f)

frontier = {}
for e in db:
    n = int(e["n"])
    frontier.setdefault(n, []).append((int(e["size"]), int(e["depth"])))

def fgap(n, sz, dp):
    if n not in frontier:
        return 0
    best_s = 999999
    for s, d in frontier[n]:
        if d <= dp and s < best_s:
            best_s = s
    if best_s == 999999:
        return -999
    return sz - best_s + 1

os.makedirs("{TMP}/sn_exact_in", exist_ok=True)
os.makedirs("{TMP}/sn_exact_out", exist_ok=True)

tasks = []
# 1. All 48 Mason Hemmer Sort_LS_*.json (Oct 18, 2026)
for p in sorted(glob.glob("data/SorterHunter/Networks/Sorters_Low_Avg_Swaps/Sort_LS_*.json")):
    with open(p) as f:
        d = json.load(f)
    n = d["N"]
    if n < 18 or n > 64:
        continue
    ces = d.get("nw") or d.get("Comparators")
    tag = f"LS_N{n}L{d['L']}D{d['D']}"
    in_txt = f"{TMP}/sn_exact_in/{tag}.txt"
    with open(in_txt, "w") as out:
        out.write(f"{n} {len(ces)}\n")
        for u, v in ces:
            if u > v:
                u, v = v, u
            out.write(f"{u} {v}\n")
    tasks.append((n, tag, in_txt, 3, 8, 35000))

# 2. All Mason Hemmer Sort_*.json (N=18..64)
for p in sorted(glob.glob("data/SorterHunter/Networks/Sorters/Sort_[0-9]*.json")):
    with open(p) as f:
        d = json.load(f)
    n = d["N"]
    if n < 18 or n > 64:
        continue
    ces = d.get("nw") or d.get("Comparators")
    tag = f"MH_N{n}L{d['L']}D{d['D']}"
    in_txt = f"{TMP}/sn_exact_in/{tag}.txt"
    with open(in_txt, "w") as out:
        out.write(f"{n} {len(ces)}\n")
        for u, v in ces:
            if u > v:
                u, v = v, u
            out.write(f"{u} {v}\n")
    tasks.append((n, tag, in_txt, 2, 6, 35000))

tasks.sort(key=lambda x: x[0])
print(f"Running sn_exact_beam on {len(tasks)} networks...")

def run_one(t):
    n, tag, in_txt, max_k, bw, ts = t
    cmd = ["./sn_exact_beam", in_txt, str(max_k), "{TMP}/sn_exact_out", tag, str(bw), str(ts)]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    # Scan generated files for this tag
    hits = []
    for out_f in glob.glob(f"{TMP}/sn_exact_out/exact_{tag}_*.txt"):
        m = re.search(r"_n(\d+)_s(\d+)_d(\d+)_i(\d+)\.txt$", out_f)
        if not m:
            continue
        cn, cs, cd, ci = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        g = fgap(cn, cs, cd)
        if g <= 2:
            hits.append((g, cn, cs, cd, tag, out_f))
    return hits

with ThreadPoolExecutor(max_workers=12) as ex:
    for res in ex.map(run_one, tasks):
        for g, cn, cs, cd, tag, out_f in res:
            if g <= 0:
                print(f"  *** PARETO WIN! n={cn} ({cs}, {cd}) fgap={g} from {tag} -> {out_f}", flush=True)
            elif g == 1 and out_f.endswith("_i1.txt"):
                print(f"  [TIE] n={cn} ({cs}, {cd}) from {tag} -> {out_f}", flush=True)
            elif g == 2 and out_f.endswith("_i1.txt"):
                print(f"  [NEAR+1] n={cn} ({cs}, {cd}) from {tag} -> {out_f}", flush=True)
