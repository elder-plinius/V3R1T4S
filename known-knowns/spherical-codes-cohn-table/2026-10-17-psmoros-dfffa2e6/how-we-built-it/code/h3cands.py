"""H3 candidate list: converged rows (d, N) (unstarred, not NMO, in plain.csv, not taken, not kissing-range with
c <= 1/2) and a source row (d, N+k), k = 1..3, present on the index (any status). Score = gap / step with
gap = c(N+k) - c(N) and step = c(N) - c(previous row in d). A small score means the bigger code is almost as good,
so removing k points and re-polishing may beat c(N). Output: score, d, N, k, c(N), c(N+k), holder(N), holder(N+k)."""
import csv, collections, sys
B = "WORKDIR/runs/2026-10-16-0024/data/sc/bar_table.tsv"
TAKEN = {(29, 114), (30, 74), (29, 72), (28, 70), (30, 117), (29, 145), (26, 232), (27, 68)}
R = {}
for r in csv.DictReader(open(B), delimiter="\t"):
    R[(int(r["d"]), int(r["N"]))] = r
byd = collections.defaultdict(list)
for (d, N) in R: byd[d].append(N)
out = []
for d in byd:
    Ns = sorted(byd[d])
    for i, N in enumerate(Ns):
        r = R[(d, N)]
        if r["star"] == "1" or r["nmo"] == "1" or (d, N) in TAKEN: continue
        if r["cos_plain"] in ("", "None"): continue
        c = float(r["cos_index"])
        if 9 <= d <= 23 and c <= 0.5: continue
        if i == 0: continue
        step = c - float(R[(d, Ns[i - 1])]["cos_index"])
        for k in (1, 2, 3):
            h = R.get((d, N + k))
            if h is None: continue
            gap = float(h["cos_index"]) - c
            out.append((gap / max(step, 1e-12), d, N, k, c, float(h["cos_index"]), r["ref"][:12], h["ref"][:12], h["nmo"], h["star"]))
out.sort()
maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 400
for o in out[:maxn]:
    print("%.3e\t%d\t%d\t%d\t%.12f\t%.12f\t%s\t%s\t%s\t%s" % o)
