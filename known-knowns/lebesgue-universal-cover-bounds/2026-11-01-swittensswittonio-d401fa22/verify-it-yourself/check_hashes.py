"""Check the sha256 of every file in object/ against verify-it-yourself/object.sha256 (standard library only)."""
import hashlib, os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
listed = {}
for line in open(os.path.join(root, "verify-it-yourself", "object.sha256"), encoding="utf-8"):
    line = line.strip()
    if line:
        h, p = line.split(None, 1)
        listed[os.path.normpath(p.lstrip("*"))] = h
found = {}
for d, _, fs in os.walk(os.path.join(root, "object")):
    for f in fs:
        p = os.path.join(d, f)
        found[os.path.normpath(os.path.relpath(p, os.path.join(root, "object")))] = hashlib.sha256(open(p, "rb").read()).hexdigest()
bad = [p for p in listed if found.get(p) != listed[p]] + [p for p in found if p not in listed]
if bad:
    print("object/ hash mismatch:", ", ".join(sorted(set(bad))[:5]))
    sys.exit(1)
print("object/: %d files, all sha256 match" % len(found))
