"""Collect best r per N from all run logs (lines '<N> <seed> r=... tab=... diff=...') and beaten files."""
import sys, glob, re, os

best = {}
tab = {}
for f in sys.argv[1:]:
    for line in open(f):
        m = re.match(r"(\d+) (\d+) r=([0-9.]+) tab=([0-9.]+)", line)
        if m:
            n = int(m.group(1)); r = float(m.group(3)); tab[n] = m.group(4)
            if r > best.get(n, (-1,))[0]:
                best[n] = (r,)
here = os.path.dirname(os.path.abspath(__file__))
for f in glob.glob(os.path.join(here, "..", "hsp4_N*.txt")):
    n = int(re.search(r"N(\d+)", f).group(1))
    head = open(f).readline()
    r = float(re.search(r"our r\* = ([0-9.]+)", head).group(1))
    best[n] = (r, "BEATEN")
cells = []
for n in sorted(best):
    b = best[n]
    flag = "yes" if len(b) > 1 else "no"
    cells.append(f"{n} | {tab.get(n, '')} | {b[0]:.12f} | {b[0] - float(tab[n]):+.2e} | {flag}")
per = int(os.environ.get("PER_ROW", "3"))
for i in range(0, len(cells), per):
    print("| " + " | ".join(cells[i:i + per]) + " |")
