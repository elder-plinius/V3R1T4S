import sys
# merge: first-pass certificate lines (some UNLABELED) + restart results for those trees -> final certificate
first, second, out = sys.argv[1:4]
fix = {}
for l in open(second):
    p = l.rstrip("\n").split(";")
    if p[2]: fix[p[1]] = l
n_fixed = n_left = 0
with open(out, "w") as f:
    for l in open(first):
        p = l.rstrip("\n").split(";")
        if not p[2]:
            if p[1] in fix: f.write(fix[p[1]]); n_fixed += 1; continue
            n_left += 1
        f.write(l)
print("fixed_by_restart=%d still_unlabeled=%d" % (n_fixed, n_left))
