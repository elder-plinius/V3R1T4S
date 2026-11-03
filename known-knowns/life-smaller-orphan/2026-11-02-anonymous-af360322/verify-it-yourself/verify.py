#!/usr/bin/env python3
"""Standalone checks for the 'no 5 x w Life orphan, w <= 8' certificate table (Python standard library only).
Definition: a target pattern on an h x w box is an orphan under Life (B3/S23) if no pattern on the surrounding
(h+2) x (w+2) box has, after one generation, exactly the target on the h x w box (cells outside are free).
Part A checks object/certificate.tsv: for each encoding (tcnf, mcnf) and each box 5x7 and 5x8 the cube split on
target column 4 lists every value 0..31 exactly once (2^5 values of a 5-cell column = exhaustive cover), every cube
ended with CaDiCaL exit 20 (UNSAT) and an LRAT proof that lrat-check accepted (c_VERIFIED). It also requires the
tcnf 5x4 and 5x6 splits. Part B re-derives the definition independently with a column-transfer subset automaton
(dp.py) and checks it against controls: rules with known small orphans give exactly the known first widths, and Life
has no orphan of height 2 (w <= 8) or height 3 (w <= 5). Part B does not re-solve the 5 x 8 instance (that needs the
SAT runs in how-we-built-it/, hours of CPU)."""
import sys, os, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dp import first_orphan_width
def main(path):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    g = collections.defaultdict(list)
    for r in rows:
        if r["rule"] != "8/12": print("bad rule", r); return False
        if r["result"] != "20" or r["check"] != "c_VERIFIED": print("cube not UNSAT+verified:", r); return False
        g[(r["route"], int(r["h"]), int(r["w"]), int(r["cube_col"]))].append(int(r["val"]))
    need = {("tcnf",5,8,4):32, ("mcnf",5,8,4):32, ("tcnf",5,7,4):32, ("mcnf",5,7,4):32, ("tcnf",5,6,3):32, ("tcnf",5,4,2):32}
    for k, n in need.items():
        vals = sorted(g.get(k, []))
        ok = vals == list(range(n))
        print("cover", k, "cubes", len(vals), "of", n, "OK" if ok else "BAD")
        if not ok: return False
    # mcnf cubes add only unit clauses on the fixed column, so their clause count is identical within a box
    for k in g:
        if k[0] == "mcnf":
            cl = {r["clauses"] for r in rows if r["route"] == "mcnf" and (int(r["h"]), int(r["w"])) == k[1:3]}
            print("mcnf", k[1:3], "clause counts", sorted(cl))
            if len(cl) != 1: return False
    for (bm, sm, h, W, want) in [(64,1,2,6,2),(17,1,2,6,5),(64,4,2,7,6),(8,0,2,7,6),(8,12,2,8,None),(8,12,3,5,None)]:
        got = first_orphan_width(h, bm, sm, W)
        print("control B%d/S%d (masks) height %d up to width %d: first orphan width %s, expected %s" % (bm, sm, h, W, got, want))
        if got != want: return False
    return True
if __name__ == "__main__":
    ok = main(sys.argv[1]); print("verify.py", "OK" if ok else "FAILED"); sys.exit(0 if ok else 1)
