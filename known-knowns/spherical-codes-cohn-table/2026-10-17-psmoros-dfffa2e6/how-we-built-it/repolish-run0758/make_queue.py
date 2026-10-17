#!/usr/bin/env python3
"""repolish lens: build the pass-1 queue of our own rows (class 'ours') and the starred control queue.
Order: rows whose near-max set within 1e-6 is small relative to the Maxwell count M first (k1e-6 / M ascending);
rows already converged to 1e-9 (k1e-9 >= M/2) last with a short cap (H14 pre-filter test).
floor = table(d, N-1) + 1e-11 when the table step from N-1 to N exceeds 1.2e-6 (so a 1e-6 gain need not delete the
(N-1) row); otherwise no floor.
usage: make_queue.py CAP CAP_CONVERGED EARLY > out/queue_ours.tsv"""
import csv, sys
RUN = "WORKSPACE/runs/2026-10-16-0758"
L = RUN + "/attempts/repolish"
cap, capc, early = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
T = {}
for r in csv.DictReader(open(RUN + "/data/sc/index_parsed.tsv"), delimiter="\t"):
    T[(int(r["d"]), int(r["N"]))] = float(r["cos"])
S = list(csv.DictReader(open(L + "/out/survey.tsv"), delimiter="\t"))
rows = []
for r in S:
    if r["class"] != "ours":
        continue
    d, N, M = int(r["d"]), int(r["N"]), int(r["M"])
    conv = int(r["k1e-9"]) >= M / 2
    score = (1 if conv else 0, int(r["k1e-6"]) / M)
    fl = ""
    if (d, N - 1) in T and T[(d, N)] - T[(d, N - 1)] > 1.2e-6:
        fl = "%.15f" % (T[(d, N - 1)] + 1e-11)
    rows.append((score, d, N, RUN + "/data/seeds/" + r["seed"], "ours", early, capc if conv else cap, fl))
rows.sort()
print("d\tN\tseed\ttag\tearly\tcap\tfloor\tscore")
for sc, d, N, sp, tag, e, c, fl in rows:
    print("%d\t%d\t%s\t%s\t%g\t%g\t%s\t%d:%.4f" % (d, N, sp, tag, e, c, fl, sc[0], sc[1]))
