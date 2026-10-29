#!/usr/bin/env python3
"""split_parts.py dir : for u.txt v.txt w.txt in dir, if a file is > 1,000,000 bytes, replace it by balanced parts
X.part1.txt ... (cut at line boundaries, each <= 1,000,000 bytes; cat of the parts = the original). Writes SHA256SUMS
with the sha256 of the assembled u.txt/v.txt/w.txt and of every file left in the folder."""
import sys, os, hashlib
d = sys.argv[1]
LIM = 1_000_000
sums = []
for w in "uvw":
    p = os.path.join(d, w + ".txt")
    b = open(p, "rb").read()
    sums.append((w + ".txt (assembled)", hashlib.sha256(b).hexdigest()))
    if len(b) <= LIM:
        continue
    n = -(-len(b) // LIM)
    while True:
        cuts = [0]
        for k in range(1, n):
            t = b.find(b"\n", len(b) * k // n)
            cuts.append(t + 1)
        cuts.append(len(b))
        parts = [b[cuts[i]:cuts[i + 1]] for i in range(n)]
        if max(len(x) for x in parts) <= LIM and all(parts):
            break
        n += 1
    assert b"".join(parts) == b
    for i, x in enumerate(parts, 1):
        open(os.path.join(d, "%s.part%d.txt" % (w, i)), "wb").write(x)
    os.remove(p)
with open(os.path.join(d, "SHA256SUMS"), "w") as f:
    for name, h in sums:
        f.write("%s  %s\n" % (h, name))
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".txt"):
            f.write("%s  %s\n" % (hashlib.sha256(open(os.path.join(d, fn), "rb").read()).hexdigest(), fn))
print(open(os.path.join(d, "SHA256SUMS")).read(), end="")
