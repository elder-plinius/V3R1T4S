"""Hub submission copies: the frozen files minus horizon -1 rows (outside hub-config tasks.json's horizons 0..29; kept in
result/forecasts only to cover hub-baseline's horizon -1 tasks). Every other row is copied unchanged.
usage: python make_submission.py <in dir> <out dir>"""
import os, sys, glob
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, "*-V3R1T4S-asofKA.csv"))):
    lines = open(f).read().splitlines()
    hdr = lines[0].split(","); hi = hdr.index("horizon")
    keep = [lines[0]] + [l for l in lines[1:] if l.split(",")[hi] != "-1"]
    open(os.path.join(dst, os.path.basename(f)), "w", newline="\n").write("\n".join(keep) + "\n")
    print(os.path.basename(f), len(lines) - 1, "->", len(keep) - 1)
