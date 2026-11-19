"""Check object/VALUE.txt against INDEX.csv and every file VALUE.txt pins (Python 3 standard library only).
Run from the package folder. Pins in VALUE.txt are 'path  sha256' with paths relative to object/."""
import csv, hashlib, os, sys
def h(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
# The one pinned file that is not shipped: the nauty geng executable the run used (third-party binary). Its pin is a
# record of which build produced the graph lists; a stranger builds nauty 2.8.8 instead (see RUN_IT_YOURSELF.md).
NOT_SHIPPED = {"tools/geng"}
row = list(csv.DictReader(open("INDEX.csv")))[0]
ok = h(row["file"]) == row["sha256"]
print(f"{row['file']} sha256 {'matches' if ok else 'DOES NOT MATCH'} INDEX.csv")
lines = open("object/VALUE.txt").read().splitlines()
vals = [l for l in lines if l.startswith("value: ")]
good = (vals == ["value: 71"] and row["value"] == "71" and "cell: A384209(11)" in lines
        and "witness_graph6: J?qrdjivb}_" in lines and "witness_start: 752" in lines
        and "graph_count: 1018997864" in lines)
print("value line:", vals, "INDEX value:", row["value"], "ok" if good else "MISMATCH"); ok &= good
start = next(i for i, l in enumerate(lines) if l.startswith("# sha256 pins")) + 1
n = 0; skipped = []
for l in lines[start:]:
    if not l.strip(): continue
    p, d = l.split()
    if len(d) != 64: print("bad pin line:", l); ok = False; continue
    if p in NOT_SHIPPED:
        if os.path.exists(os.path.join("object", p)): ok &= h(os.path.join("object", p)) == d
        skipped.append(p); continue
    fp = os.path.join("object", p)
    g = os.path.isfile(fp) and h(fp) == d; ok &= g; n += 1
    if not g: print("pin mismatch:", p)
print(f"{n} pinned files checked; recorded but not shipped: {', '.join(skipped) or 'none'}")
# Every shipped file under object/code and object/evidence must be pinned.
pinned = {l.split()[0] for l in lines[start:] if l.strip()}
for root, _, files in os.walk("object"):
    for f in files:
        r = os.path.relpath(os.path.join(root, f), "object").replace(os.sep, "/")
        if r != "VALUE.txt" and r not in pinned: print("unpinned file in object/:", r); ok = False
# The how-we-built-it/ and verify-it-yourself/ program copies must be the pinned programs.
for d, fs in (("how-we-built-it", ("lifeA11.c", "lifeB2.c", "stepper.py", "combine.py", "merge_orders.py", "compare_AB.py")),
              ("verify-it-yourself", ("lifeA11.c", "lifeB2.c", "stepper.py"))):
    for f in fs:
        g = h(os.path.join(d, f)) == h(os.path.join("object", "code", f)); ok &= g
        if not g: print("copy differs from pinned program:", d + "/" + f)
print("ok" if ok else "FAIL"); sys.exit(0 if ok else 1)
