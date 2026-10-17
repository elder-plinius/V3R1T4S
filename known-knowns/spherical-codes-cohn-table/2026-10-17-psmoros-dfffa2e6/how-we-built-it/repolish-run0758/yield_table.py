#!/usr/bin/env python3
"""repolish lens: yield per method (config) from every out/<pass>/results_*.jsonl (float64 gains vs the 08:02Z table).
A row-run 'improves' if its output beats the table by the row's bar (1e-6 for our rows, 1e-9 otherwise).
usage: yield_table.py > out/yield.tsv"""
import glob, json, collections
L = "WORKSPACE/runs/2026-10-16-0758/attempts/repolish"
S = collections.defaultdict(lambda: [0, 0, 0.0, set(), set()])
best = {}
for f in sorted(glob.glob(L + "/out/*/results_*.jsonl")):
    pas = f.split("/out/")[1].split("/")[0]
    for l in open(f):
        r = json.loads(l)
        tag = r.get("tag", "")
        key = "%s %s %s" % (pas, r["config"], "star-control" if tag == "star" else tag)
        bar = 1e-6 if tag == "ours" else 1e-9
        s = S[key]
        s[0] += 1; s[1] += r["gain_vs_table"] >= bar; s[2] += r["cpu"]
        s[3].add((r["d"], r["N"]))
        if r["gain_vs_table"] >= bar:
            s[4].add((r["d"], r["N"]))
        if tag != "star":
            k = (r["d"], r["N"])
            best[k] = max(best.get(k, -1), r["gain_vs_table"])
print("pass config tag\trow_runs\timproved_runs\tcpu_s\tdistinct_rows\tdistinct_improved\timproved_per_cpu_min")
for k in sorted(S):
    s = S[k]
    print("%s\t%d\t%d\t%.1f\t%d\t%d\t%.2f" % (k, s[0], s[1], s[2], len(s[3]), len(s[4]),
                                               len(s[4]) / (s[2] / 60) if s[2] > 0 else 0))
tot = sum(v[2] for v in S.values())
print("TOTAL distinct rows tried %d, with best float gain >= 1e-6: %d, CPU-s all row-runs %.1f" % (
    len(best), sum(1 for g in best.values() if g >= 1e-6), tot))
