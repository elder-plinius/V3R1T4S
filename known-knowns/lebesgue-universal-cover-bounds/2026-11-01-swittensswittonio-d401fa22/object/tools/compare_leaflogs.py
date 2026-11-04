# compare per-leaf lower bounds of the interval verifier (new) and the previous rigorous-double verifier (old) on the leaves both logged (same hash selector on (seed, bit position)).
import sys, struct
def load(p):
    d = {}
    for l in open(p):
        t = l.split()
        if len(t) >= 4: d[(int(t[0]), int(t[1]))] = struct.unpack('<d', struct.pack('<Q', int(t[2], 16)))[0]
    return d
new, old = load(sys.argv[1]), load(sys.argv[2])
tn = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8344 + 1e-12
common = [k for k in new if k in old]
print("new logged", len(new), "old logged", len(old), "common", len(common))
diffs = sorted((new[k] - old[k], k) for k in common)
import statistics
ds = [x for x, _ in diffs]
print("new-old lower bound: min %.3e  p1 %.3e  median %.3e  p99 %.3e  max %.3e" % (ds[0], ds[len(ds)//100], statistics.median(ds), ds[-len(ds)//100], ds[-1]))
print("new-old < 0 (interval LB below double LB):", sum(1 for x in ds if x < 0), " ; |diff| > 1e-6:", sum(1 for x in ds if abs(x) > 1e-6))
print("min slack (LB - tau - 1e-12): new %.6e  old %.6e" % (min(new[k] for k in common) - tn, min(old[k] for k in common) - tn))
print("both >= threshold on all common leaves:", all(new[k] >= tn and old[k] >= tn for k in common))
print("worst 5 by slack difference (key, new, old):")
for x, k in diffs[:5]: print("  ", k, new[k], old[k], x)
