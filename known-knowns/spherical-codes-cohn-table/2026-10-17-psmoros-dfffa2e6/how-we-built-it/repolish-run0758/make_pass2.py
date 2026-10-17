#!/usr/bin/env python3
"""repolish lens: pass-2 queue. Rows of class 'ours' whose best pass-1 output (out/p1, p3, p4, p5) improves the
08:02Z table by MIN_GAIN <= gain < 1e-6 (or that never got a real try), continued from that output state.
Order: gain descending (closest to the 1e-6 bar first); rows that stalled before their cap go last.
usage: make_pass2.py CAP MIN_GAIN [PASSES] > out/queue_pass2.tsv
PASSES: comma list of output folders to read (default p1,p3,p4,p5); with 'moving' as 4th argument only rows whose
latest run hit its cap (still descending) are queued, and the two fixed extra rows are not added."""
import csv, glob, json, sys
RUN = "WORKSPACE/runs/2026-10-16-0758"
L = RUN + "/attempts/repolish"
cap, ming = float(sys.argv[1]), float(sys.argv[2])
passes = sys.argv[3].split(",") if len(sys.argv) > 3 else ["p1", "p3", "p4", "p5"]
moving_only = len(sys.argv) > 4 and sys.argv[4] == "moving"
q = {(int(r["d"]), int(r["N"])): r for r in csv.DictReader(open(L + "/out/queue_ours.tsv"), delimiter="\t")}
best = {}
for p in passes:
    for f in glob.glob(L + "/out/%s/results_*.jsonl" % p):
        for l in open(f):
            r = json.loads(l)
            k = (r["d"], r["N"])
            if k not in best or r["out_c"] < best[k]["out_c"]:
                best[k] = r
rows = []
for k, r in best.items():
    g = r["gain_vs_table"]
    if ming <= g < 1e-6 and r.get("file"):
        stalled = r["cpu"] < 0.9 * r["cap"]
        if moving_only and stalled:
            continue
        fp = r["file"] if r["file"].startswith("/") else L + "/" + r["file"]
        rows.append(((1 if stalled else 0, -g), k, fp))
for k in ([] if moving_only else [(26, 178), (32, 208)]):  # bookkeeping slip in R5 queue / killed mid-row under R1
    if k in q and not (k in best and best[k]["gain_vs_table"] >= 1e-6):
        rows.append(((0, 0.0), k, q[k]["seed"]))
rows.sort()
print("d\tN\tseed\ttag\tearly\tcap\tfloor\tnote")
for sc, (d, N), fp in rows:
    print("%d\t%d\t%s\tours\t1.5e-6\t%g\t%s\t%s" % (d, N, fp, cap, q[(d, N)]["floor"],
                                                  "stalled" if sc[0] else "gain %.3e" % -sc[1]))
