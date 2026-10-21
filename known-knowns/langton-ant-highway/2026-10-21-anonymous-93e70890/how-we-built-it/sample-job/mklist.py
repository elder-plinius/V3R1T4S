# Extract the 4096 per-chunk (maxtcap_mask, maxtcap) from data-user/langton6x6-out6/chunk_*.sum
import glob, os, re, sys
d = sys.argv[1]
rows = []
for f in glob.glob(os.path.join(d, "chunk_*.sum")):
    for line in open(f):
        t = line.split()
        kv = dict(zip(t[0::2], t[1::2]))
        rows.append((int(kv["chunk"]), int(kv["maxtcap_mask"]), int(kv["maxtcap"]), int(kv["CAP"]), int(kv["UNCAP"]), int(kv["OOB"]), int(kv["lines"]), int(kv["first"])))
rows.sort()
assert [r[0] for r in rows] == list(range(4096)), "chunks not 0..4095"
for c, m, t, cap, unc, oob, n, first in rows:
    assert first == c << 24 and n == 1 << 24 and cap == n and unc == 0 and oob == 0
    assert first <= m < first + n
with open("output/hard_list.txt", "w") as o:
    for r in rows: o.write("%d\n" % r[1])
with open("output/hard_expected.txt", "w") as o:
    for r in rows: o.write("%d %d %d\n" % (r[0], r[1], r[2]))
print("chunks", len(rows), "total masks", sum(r[6] for r in rows), "all CAP", sum(r[3] for r in rows) == 1 << 36,
      "max", max(rows, key=lambda r: r[2])[1:3])
