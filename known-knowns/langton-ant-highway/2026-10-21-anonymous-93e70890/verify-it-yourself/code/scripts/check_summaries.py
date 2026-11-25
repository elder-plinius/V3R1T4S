#!/usr/bin/env python3
"""Check the 4096 user chunk summaries: contiguous coverage of [0, 2^36), every mask CAP, no UNCAP/OOB/fixups,
global max, and derive the hard-case list (per-chunk maxtcap_mask). Usage: python3 code/scripts/check_summaries.py [DIR]"""
import glob, os, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "data", "user-chunk-sums")
rows = {}
bad = 0
for f in sorted(glob.glob(os.path.join(d, "chunk_*.sum"))):
    lines = [l for l in open(f) if l.strip()]
    if len(lines) != 1: print("BAD line count", f); bad += 1; continue
    t = lines[0].split(); kv = dict(zip(t[0::2], t[1::2]))
    c = int(kv["chunk"])
    if c in rows: print("DUPLICATE chunk", c); bad += 1
    rows[c] = kv
if sorted(rows) != list(range(4096)): print("FAIL: chunks are not exactly 0..4095 (%d found)" % len(rows)); bad += 1
tot = cap = 0; gmax = (-1, None)
for c, kv in sorted(rows.items()):
    first, last, n = int(kv["first"]), int(kv["last"]), int(kv["lines"])
    ok = first == c << 24 and last == first + (1 << 24) - 1 and n == 1 << 24 and int(kv["CAP"]) == n \
        and kv["UNCAP"] == "0" and kv["OOB"] == "0" and kv["overflow_fixups"] == "0" and first <= int(kv["maxtcap_mask"]) <= last
    if not ok: print("FAIL chunk", c, kv); bad += 1
    tot += n; cap += int(kv["CAP"])
    if int(kv["maxtcap"]) > gmax[0]: gmax = (int(kv["maxtcap"]), int(kv["maxtcap_mask"]))
print("chunks %d masks %d CAP %d (2^36 = %d) global max tcap %d at mask %d" % (len(rows), tot, cap, 1 << 36, gmax[0], gmax[1]))
out = os.path.join(root, "work"); os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "hard_list.txt"), "w") as o, open(os.path.join(out, "hard_expected.txt"), "w") as e:
    for c, kv in sorted(rows.items()):
        o.write(kv["maxtcap_mask"] + "\n"); e.write("%d %s %s\n" % (c, kv["maxtcap_mask"], kv["maxtcap"]))
print("SUMMARIES: PASS" if bad == 0 and tot == cap == 1 << 36 else "SUMMARIES: FAIL")
sys.exit(0 if bad == 0 and tot == cap == 1 << 36 else 1)
