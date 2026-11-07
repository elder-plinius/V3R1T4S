"""Build cells.tsv: every attempted cell, table value, best value found, gap, BEATEN."""
import re, os
H = os.path.dirname(os.path.abspath(__file__)) + "/../"
best, table, stage = {}, {}, {}
for line in open(H + "runs/screen.log"):
    p = line.split()
    k = (int(p[0]), int(p[1]))
    best[k] = float(p[2].split("=")[1]); table[k] = p[3].split("=")[1]; stage[k] = "screen"
for fn, tag in (("runs/deep.log", "deep"), ("runs/mbh.log", "mbh"), ("runs/mbh2.log", "mbh2")):
    if not os.path.exists(H + fn):
        continue
    for line in open(H + fn):
        m = re.match(r"(\d+) (\d+) (?:FINAL|MBH-FINAL).*best=([0-9.]+)", line)
        if m:
            k = (int(m.group(1)), int(m.group(2)))
            v = float(m.group(3))
            if v < best[k]:
                best[k] = v; stage[k] = tag
with open(H + "cells.tsv", "w") as f:
    f.write("d\tN\ttable\tbest_found\tgap(best-table)\tstage\tBEATEN\n")
    for k in sorted(best):
        g = best[k] - float(table[k])
        f.write(f"{k[0]}\t{k[1]}\t{table[k]}\t{best[k]:.12f}\t{g:.3e}\t{stage[k]}\t{'yes' if g <= -1e-10 else 'no'}\n")
print(len(best))
