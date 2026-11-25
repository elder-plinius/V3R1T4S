#!/usr/bin/env python3
"""Check object/ against verify-it-yourself/OBJECT_SHA256 and recompute every number in object/RESULT.txt
from object/chunk_sums/ and object/sample/ (Python standard library only). Run from the package folder."""
import hashlib, os, sys
bad = []
for line in open("verify-it-yourself/OBJECT_SHA256"):
    h, f = line.split(None, 1); f = f.strip()
    if not os.path.isfile(f) or hashlib.sha256(open(f, "rb").read()).hexdigest() != h:
        bad.append("object file changed or missing: " + f)
listed = {l.split(None, 1)[1].strip() for l in open("verify-it-yourself/OBJECT_SHA256")}
for d, _, fs in os.walk("object"):
    for x in fs:
        p = os.path.join(d, x)
        if p not in listed: bad.append("unlisted object file: " + p)
# recompute
rows = {}
for part in sorted(os.listdir("object/chunk_sums")):
    for l in open(os.path.join("object/chunk_sums", part)):
        t = l.split(); kv = dict(zip(t[0::2], t[1::2])); rows[int(kv["chunk"])] = kv
calc = {}
calc["chunks"] = len(rows)
calc["masks"] = sum(int(k["lines"]) for k in rows.values())
calc["captured"] = sum(int(k["CAP"]) for k in rows.values())
calc["uncap"] = sum(int(k["UNCAP"]) for k in rows.values())
calc["oob"] = sum(int(k["OOB"]) for k in rows.values())
mx = max(rows.values(), key=lambda k: int(k["maxtcap"]))
calc["max_tcap"] = int(mx["maxtcap"]); calc["max_tcap_mask"] = int(mx["maxtcap_mask"])
contig = sorted(rows) == list(range(4096)) and all(int(rows[c]["first"]) == c << 24 and int(rows[c]["lines"]) == 1 << 24 for c in rows)
calc["contiguous"] = "yes" if contig else "no"
units = {}
for part in sorted(x for x in os.listdir("object/sample") if x.startswith("sample_units")):
    for l in open(os.path.join("object/sample", part)):
        t = l.split(); kv = dict(zip(t[0::2], t[1::2])); units[(int(kv["pass"]), int(kv["chunk"]))] = kv
calc["sample_units"] = len(units)
calc["sample_masks"] = sum(int(k["n"]) for k in units.values())
calc["sample_cap"] = sum(int(k["CAP"]) for k in units.values())
smx = max(units.values(), key=lambda k: int(k["maxtcap"]))
calc["sample_max_tcap"] = int(smx["maxtcap"]); calc["sample_max_tcap_mask"] = int(smx["maxtcap_mask"])
calc["sample_units_over_chunk_max"] = sum(1 for (p, c), k in units.items() if int(k["maxtcap"]) > int(rows[c]["maxtcap"]))
hard = [l.split() for l in open("object/hard_cases/hard_lantx2.txt")]
calc["hard_cases"] = len(hard)
calc["hard_cases_equal"] = sum(1 for c, h in enumerate(hard) if h[0] == rows[c]["maxtcap_mask"] and h[1] == rows[c]["maxtcap"] and h[5] == "CAP")
res = {}
for l in open("object/RESULT.txt"):
    if ":" in l and not l.startswith("#"):
        k, v = l.split(":", 1); res[k.strip()] = v.strip()
for k, v in calc.items():
    if res.get(k) != str(v): bad.append("RESULT.txt %s = %r but recomputed %r" % (k, res.get(k), v))
for k in res:
    if k not in calc and k not in ("box", "convention", "cap", "seed"): bad.append("RESULT.txt has an unchecked key " + k)
for b in bad: print("BAD:", b)
print("object check: %d problems; recomputed %s" % (len(bad), calc))
sys.exit(1 if bad else 0)
