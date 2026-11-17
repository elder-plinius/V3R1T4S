"""Sum the per-k lines of the shard outputs (shard0..3.txt) and compare with the unsharded run of 2026-10-29 where it
finished (k = 26, 27). Usage: sum_shards.py OUTDIR [REFERENCE_FILES...]"""
import re, sys, glob, os
pat = re.compile(r"k=(\d+) admissible_r=(\d+) enumerated_pairs\(q\(q rho-p\)<U\)=(\d+) window_candidates=(\d+) product_solutions=(\d+)")
tot = {}
for fn in sorted(glob.glob(os.path.join(sys.argv[1], "shard[0-9].txt"))):
    for l in open(fn):
        m = pat.match(l)
        if m:
            k = int(m.group(1)); t = tot.setdefault(k, [0, 0, 0, 0, 0])
            for j in range(4): t[j] += int(m.group(j + 2))
            t[4] += 1
ref = {}
for fn in sys.argv[2:]:
    for l in open(fn):
        m = pat.match(l)
        if m: ref[int(m.group(1))] = tuple(int(m.group(j)) for j in (2, 3, 4, 5))
for k, v in sorted(tot.items()):
    line = "k=%d shards=%d admissible_r=%d enumerated_pairs=%d window_candidates=%d product_solutions=%d" % (k, v[4], v[0], v[1], v[2], v[3])
    if k in ref: line += "  | unsharded 2026-10-29: %s -> %s" % (ref[k], "EQUAL" if ref[k] == tuple(v[:4]) else "DIFFERENT")
    print(line)
