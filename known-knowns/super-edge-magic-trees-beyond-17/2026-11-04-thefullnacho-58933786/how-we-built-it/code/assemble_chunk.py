#!/usr/bin/env python3
"""assemble_chunk.py trees.txt out1 [out2 ...] : for each tree (in trees.txt order) take the first stage output whose
labeling passes check_sem.check; writes cert.txt (one line per labelled tree, the stage line plus ";s<stage>")
and residue.txt (trees left unlabelled); prints one stats line. Ignores truncated last lines."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_sem import check
trees, srcs = sys.argv[1], sys.argv[2:]
got = {}
for i, f in enumerate(srcs):
    if not os.path.exists(f): continue
    for l in open(f):
        if not l.endswith("\n"): continue
        p = l.rstrip("\n").split(";")
        if len(p) < 3 or not p[2]: continue
        k = p[0] + ";" + p[1]
        if k in got: continue
        try:
            n = int(p[0]); es = [tuple(map(int, x.split("-"))) for x in p[1].split(",")]; ls = list(map(int, p[2].split(",")))
            if check(n, es, ls)[0]: got[k] = (i, l.rstrip("\n"))
        except Exception: pass
per = [0]*len(srcs); res = 0; tot = 0
with open("cert.txt", "w") as c, open("residue.txt", "w") as r:
    for l in open(trees):
        k = l.rstrip("\n"); tot += 1
        if k in got: per[got[k][0]] += 1; c.write("%s;s%d\n" % (got[k][1], got[k][0]))
        else: res += 1; r.write(k + "\n")
print("trees %d labelled_per_stage %s residue %d" % (tot, per, res))
