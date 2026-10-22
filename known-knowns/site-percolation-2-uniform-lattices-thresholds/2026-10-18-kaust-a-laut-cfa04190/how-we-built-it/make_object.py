"""Build the object folder for check_threshold.py: the #23 TM root series, the Monte Carlo block histograms (sizes
L2 >= 16) of #23 site, #23 bond and kagome site, and threshold_23_site.json with every number the checker verifies,
parsed from the saved outputs of run 2026-10-17-2357 (none typed by hand except the table cells, copied from the saved
wikitext lines 1150-1151), plus the sha256 of every data file.

usage: python make_object.py <workspace root> <output folder>
"""
import glob
import hashlib
import json
import os
import re
import shutil
import sys

ROOT, OUT = sys.argv[1], sys.argv[2]
RUN = os.path.join(ROOT, "runs", "2026-10-17-2357")
A = os.path.join(ROOT, "runs", "2026-10-16-1714", "attempts")
ol = open(os.path.join(RUN, "attempts", "timeline-aligner", "out", "one_look_output.txt"), encoding="utf-8").read()
ex = open(os.path.join(RUN, "attempts", "exact-polynomial", "out", "extrapolate_all_output.txt"), encoding="utf-8").read()


def section(n):
    return re.search(r"== %d\..*?(?=\n== |\none look finished)" % n, ol, re.S).group(0)


def mc(sec):
    m = re.search(r"primary L2>=16\s+p_MC ([0-9.]+) \+- ([0-9.]+)", sec)
    sizes = [(int(a), int(b)) for a, b in re.findall(r"L2 (\d+) M \d+ blocks (\d+)", sec) if int(a) >= 16]
    return {"p": float(m.group(1)), "sigma": float(m.group(2)), "L2": [s[0] for s in sizes], "blocks": [s[1] for s in sizes]}


def tm(name):
    blk = re.search(r"== %s\n(.*?)(?=\n== |\Z)" % name, ex, re.S).group(1)
    m = re.search(r"p_TM ([0-9.]+)\s+sigma_TM ([0-9.e+-]+)", blk)
    return {"n_max": int(re.search(r"n_max (\d+)", blk).group(1)), "p": float(m.group(1)), "sigma": float(m.group(2))}


def main():
    if os.path.exists(OUT):
        raise SystemExit("output exists")
    files = {}
    for src, dst in ((os.path.join(A, "exact-polynomial", "out", "r23_site_series.txt"), "tm/r23_site_series.txt"),
                     (os.path.join(A, "exact-polynomial", "out", "r23_bond_series.txt"), "tm/r23_bond_series.txt")):
        os.makedirs(os.path.dirname(os.path.join(OUT, dst)), exist_ok=True)
        shutil.copyfile(src, os.path.join(OUT, dst))
        files[dst] = None
    for ds in ("r23_site", "r23_bond", "kagome_site"):
        for p in sorted(glob.glob(os.path.join(A, "timeline-aligner", "mc", ds, "*.hist"))):
            L2 = int(re.search(r"_L\d+x(\d+)_s", p).group(1))
            if L2 < 16:
                continue
            dst = "mc/%s/%s" % (ds, os.path.basename(p))
            os.makedirs(os.path.join(OUT, "mc", ds), exist_ok=True)
            shutil.copyfile(p, os.path.join(OUT, dst))
            files[dst] = None
    for f in files:
        files[f] = hashlib.sha256(open(os.path.join(OUT, f), "rb").read()).hexdigest()
    t23 = tm("r23_site")
    J = {"claim": "site percolation threshold of two-uniform lattice #23, (1/2)(3^3,4^2) + (1/2)(4^4)",
         "claimed": {"p_c": round(t23["p"], 8), "sigma": round(t23["sigma"], 8)},
         "lattice": {"zbar": 4.5},
         "tm": {"site": t23, "bond": tm("r23_bond")},
         "mc": {"site": mc(section(5)), "bond": mc(section(7)), "kagome": mc(section(1))},
         "table": {"site": 0.5720, "site_sigma": 0.0002, "bond": 0.45844622},
         "files": files}
    with open(os.path.join(OUT, "threshold_23_site.json"), "w", newline="\n") as f:
        json.dump(J, f, indent=1, sort_keys=True)
        f.write("\n")
    print("object written: %d data files; claimed %s" % (len(files), J["claimed"]))


if __name__ == "__main__":
    main()
