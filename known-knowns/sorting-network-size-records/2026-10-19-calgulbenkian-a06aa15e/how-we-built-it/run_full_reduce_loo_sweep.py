import json
import glob
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

def main():
    subprocess.run(["clang", "-O3", "sn_reduce_scan.c", "-o", "sn_reduce_scan"], check=True)
    cands_dir = "{TMP}/sn_cands_v3"
    parents_dir = "{TMP}/sn_parents_v3"
    opt_dir = "{TMP}/sn_opt_v3"
    for d in [cands_dir, parents_dir, opt_dir]:
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)

    nets = json.load(open("data/all_networks.json"))
    pareto = {}
    for x in nets:
        pareto.setdefault(x["n"], []).append((x["size"], x["depth"]))

    def min_gap(n, s, d):
        pts = [s0 for s0, d0 in pareto.get(n, []) if d0 <= d]
        if not pts:
            return -999
        return s - (min(pts) - 1)

    def is_dominated(n, s, d):
        for s0, d0 in pareto.get(n, []):
            if s0 <= s and d0 <= d:
                return True
        return False

    parents = []
    seen_hashes = set()

    def add_parent(tag, n, ces):
        if n < 14:
            return
        h = (n, tuple( (min(u, v), max(u, v)) for u, v in ces ))
        if h in seen_hashes:
            return
        seen_hashes.add(h)
        pfile = os.path.join(parents_dir, f"{tag}.txt")
        with open(pfile, "w") as f:
            f.write(f"{n} {len(ces)}\n")
            for u, v in ces:
                f.write(f"{min(u, v)} {max(u, v)}\n")
        parents.append((tag, n, len(ces), pfile))

    for x in nets:
        add_parent(x["id"], x["n"], x["ces"])

    for jpath in sorted(glob.glob("data/SorterHunter/Networks/*/*.json")):
        try:
            jd = json.load(open(jpath))
            n = jd.get("N") or jd.get("n")
            ces = jd.get("nw") or jd.get("ces")
            if n and ces:
                tag = os.path.splitext(os.path.basename(jpath))[0]
                add_parent(tag, n, ces)
        except Exception:
            pass

    for mpath in sorted(glob.glob("{TMP}/win_merge_*.txt")):
        with open(mpath) as f:
            lines = [l.strip() for l in f if l.strip()]
        n, m = map(int, lines[0].split())
        ces = [list(map(int, l.split())) for l in lines[1:m+1]]
        tag = os.path.splitext(os.path.basename(mpath))[0]
        add_parent(tag, n, ces)

    print(f"Total unique parent networks (n>=14): {len(parents)}")

    def run_scan(item):
        tag, n, sz, pfile = item
        subprocess.run(["./sn_reduce_scan", pfile, "5", cands_dir, tag],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with ThreadPoolExecutor(max_workers=12) as ex:
        list(ex.map(run_scan, parents))

    all_cands = sorted(glob.glob(os.path.join(cands_dir, "cand_*.txt")))
    print(f"Generated {len(all_cands)} candidate files in {cands_dir}")

    # Filter candidates within +2 of beating Pareto frontier (gap <= 2)
    filtered = []
    seen_cand_files = set()
    for path in all_cands:
        m = re.search(r"_n(\d+)_s(\d+)_d(\d+)_i(\d+)\.txt$", path)
        if not m:
            continue
        n, s, d, idx = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        if n < 13:
            continue
        gap = min_gap(n, s, d)
        if gap <= 2:
            filtered.append((gap, n, s, d, path))

    print(f"Filtered to {len(filtered)} candidates with est gap <= +2")

    def eval_opt(item):
        gap, n, s, d, path = item
        out_path = os.path.join(opt_dir, "opt_" + os.path.basename(path))
        p = subprocess.run(["./sn_optimizer", path, "250000", out_path, "0"],
                           capture_output=True, text=True)
        line = p.stdout.strip()
        m = re.search(r"final=\((\d+),\s*(\d+)\)", line)
        if not m:
            return None
        fs, fd = int(m.group(1)), int(m.group(2))
        fgap = min_gap(n, fs, fd)
        dom = is_dominated(n, fs, fd)
        return (fgap, dom, n, fs, fd, os.path.basename(path), out_path, line)

    with ThreadPoolExecutor(max_workers=12) as ex:
        results = [r for r in ex.map(eval_opt, filtered) if r is not None]

    results.sort()
    wins = [r for r in results if not r[1]]
    ties = [r for r in results if r[0] == 1]
    near = [r for r in results if r[0] == 2]

    print(f"=== SUMMARY: {len(wins)} WINS (non-dominated!), {len(ties)} EXACT TIES (fgap=+1), {len(near)} NEAR+1 (fgap=+2) ===")
    for fgap, dom, n, fs, fd, bname, opath, line in wins:
        print(f"WIN! fgap={fgap:+d} dom={dom} n={n} final=({fs},{fd}) {bname} | {line}")
    print("--- Top 40 Ties / Near ---")
    for fgap, dom, n, fs, fd, bname, opath, line in (ties + near)[:40]:
        print(f"fgap={fgap:+d} dom={dom} n={n} final=({fs},{fd}) {bname} | {line}")

if __name__ == "__main__":
    main()
