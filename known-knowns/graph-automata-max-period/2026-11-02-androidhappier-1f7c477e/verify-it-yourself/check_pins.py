"""Check object/VALUE.txt against INDEX.csv and every file VALUE.txt pins (Python 3 standard library only)."""
import csv, hashlib, sys
def h(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
row = list(csv.DictReader(open("INDEX.csv")))[0]
ok = h(row["file"]) == row["sha256"]
print(f"{row['file']} sha256 {'matches' if ok else 'DOES NOT MATCH'} INDEX.csv")
lines = open("object/VALUE.txt").read().splitlines()
ok &= any(l == "value: 46" for l in lines) and row["value"] == "46"
start = lines.index("pinned files (sha256, path relative to the package folder):") + 1
n = 0
for l in lines[start:]:
    d, p = l.split(None, 1)
    good = h(p) == d; ok &= good; n += 1
    if not good: print("pin mismatch:", p)
print(f"{n} pinned files checked")
print("ok" if ok else "FAIL"); sys.exit(0 if ok else 1)
