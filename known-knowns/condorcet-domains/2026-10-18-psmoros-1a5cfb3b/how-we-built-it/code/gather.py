"""Per n, the largest exact DP count among best/nN.npy and every file named in an IMPROVED line of the driver
summaries (guards against a lost update when two drivers offer to best/ at the same moment).  Recounts each file.
Usage: python gather.py LENSDIR"""
import glob
import os
import re
import subprocess
import sys

L = sys.argv[1]
LSX = os.path.join(L, "code", "lsx")
cand = {}
for s in glob.glob(os.path.join(L, "out", "*", "*_summary.txt")):
    for ln in open(s):
        m = re.search(r"IMPROVED n (\d+) \S+ -> (\d+) via .*\((/\S+)\)$", ln.strip())
        if m:
            cand.setdefault(int(m.group(1)), set()).add(m.group(3))
for f in glob.glob(os.path.join(L, "best", "n*.npy")):
    cand.setdefault(int(os.path.basename(f)[1:-4]), set()).add(f)
for n in sorted(cand):
    best = None
    for f in cand[n]:
        if not os.path.exists(f):
            continue
        out = subprocess.run([LSX, "count", str(n), f], capture_output=True, text=True).stdout.split()
        v = int(out[3])
        if best is None or v > best[0] or (v == best[0] and "/best/" in f):
            best = (v, f)
    print("n %d max %d file %s" % (n, best[0], best[1]))
