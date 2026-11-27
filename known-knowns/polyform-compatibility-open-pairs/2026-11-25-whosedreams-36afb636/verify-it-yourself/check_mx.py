#!/usr/bin/env python3
"""Standalone check of the M-X bounded-UNSAT package (Python 3.8+, standard library only, no network).

What it checks (it does NOT re-run the SAT solver or drat-trim; see RUN_IT_YOURSELF.md for that):
 1. object/ files match verify-it-yourself/OBJECT_SHA256.
 2. object/mx_k2_20_bounded_unsat.json is internally consistent: k = 2..20 exactly once, area = 7k, the board
    size follows the stated formula, every k is 'unsat' with proof_verified true, its p3_label matches the
    numbers, and its CNF and proof sha256s are the lines of object/SHA256SUMS-files.txt (38 lines, nothing
    else); the archive sha256 equals object/SHA256SUMS-archive.txt.
 3. The two pieces, rebuilt from their definition in indep_compat.py (own coordinates, own symmetry group):
    the lattice code finds exactly 24 free heptiamonds; X is the only one with exactly 4 aspects (3-fold
    rotation, no mirror); M has 6 aspects; the object's M and X cells (package coordinates), mapped by a
    converter that is checked to preserve edge adjacency, are congruent to these.
 4. The placement counts n_placements_M / n_placements_X for every k equal an independent count of the
    congruent copies of M and X that fit inside that k's board.
 5. Positive and negative controls (M-B listed 2, M-C listed 6), then an independent exhaustive search without any board: for k = 2..KMAX (default 4) there is no connected
    figure that is both a union of k non-overlapping copies of M and a union of k copies of X. A
    disconnected common figure with k tiles would contain a connected one with fewer tiles, so this
    rules out every common figure with at most KMAX tiles of each kind.
Last line: PASS or FAIL.
"""
import hashlib, json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import indep_compat as ic

fails = []
def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# 1
pins = {}
for line in open(os.path.join(HERE, "OBJECT_SHA256")):
    if line.strip():
        h, f = line.split()
        pins[f] = h
objfiles = sorted("object/" + f for f in os.listdir(os.path.join(PKG, "object")))
check(sorted(pins) == objfiles, "OBJECT_SHA256 lists exactly the files in object/")
for f in objfiles:
    check(pins.get(f) == sha(os.path.join(PKG, f)), "sha256 of %s" % f)

# 2
try:
    o = json.load(open(os.path.join(PKG, "object", "mx_k2_20_bounded_unsat.json")))
except ValueError as e:
    check(False, "object JSON parses (%s)" % e)
    print("FAIL"); sys.exit(1)
ref = {}
lines = [l for l in open(os.path.join(PKG, "object", "SHA256SUMS-files.txt")) if l.strip()]
for l in lines:
    h, p = l.split()
    ref[p] = h
check(len(lines) == 38 and len(ref) == 38, "SHA256SUMS-files.txt has 38 distinct files")
ks = [e["k"] for e in o["per_k"]]
check(ks == list(range(2, 21)), "per_k covers k = 2..20 once each")
check(o["pair"] == "M-X", "pair is M-X")
used = set()
for e in o["per_k"]:
    k = e["k"]
    side = max(6, int(math.ceil(2.0 * math.sqrt(7 * k)))) + 2
    ok = (e["area"] == 7 * k and e["board_rows"] == side and e["board_cols"] == side + 2
          and e["status"] == "unsat" and e["proof_verified"] is True)
    lab = ("bounded UNSAT: no figure with k=%d tiles (area %d) inside a %dx%d board (disconnected figures also "
           "forbidden by model coverage); table=unrestricted" % (k, 7 * k, side, side + 2))
    ok = ok and e["p3_label"] == lab
    ok = ok and ref.get(e["cnf_path"]) == e["cnf_sha256"] and ref.get(e["proof_path"]) == e["proof_sha256"]
    ok = ok and e["cnf_path"].endswith("/k%d/prove/problem.cnf" % k) and e["proof_path"].endswith("/k%d/prove/proof.drat" % k)
    used.update([e["cnf_path"], e["proof_path"]])
    check(ok, "k=%d: area, board %dx%d, unsat+verified, label, sha256s" % (k, side, side + 2))
check(used == set(ref), "every file in SHA256SUMS-files.txt belongs to exactly one k")
arc = open(os.path.join(PKG, "object", "SHA256SUMS-archive.txt")).read().split()
check(len(arc) == 2 and arc[1] == o["archive"]["file"] and arc[0] == o["archive"]["sha256"], "archive sha256 matches SHA256SUMS-archive.txt")
check(isinstance(o["archive"]["bytes"], int) and o["archive"]["bytes"] > 0, "archive size recorded")

# 3
def conv(rc):
    r, c = rc
    s = 2 if (r + c) & 1 else 1
    a, p = -r, c + 1
    b = (s - a + p) // 2
    return (a, b, s - a - b)
def pk_nbrs(r, c):
    if (r + c) & 1:
        return [(r, c - 1), (r, c + 1), (r + 1, c)]
    return [(r, c - 1), (r, c + 1), (r - 1, c)]
iso = True
img = set()
for r in range(-12, 13):
    for c in range(-12, 13):
        t = conv((r, c))
        img.add(t)
        iso &= sum(t) in (1, 2)
        iso &= sorted(conv(x) for x in pk_nbrs(r, c)) == sorted(ic.nbrs(t))
check(iso and len(img) == 25 * 25, "coordinate converter is injective and preserves edge adjacency")
hept = ic.free_polyiamonds(7)
check(len(hept) == 24, "24 free heptiamonds (found %d)" % len(hept))
four = [h for h in hept if len(ic.aspects(list(h))) == 4]
M, X = ic.piece_M(), ic.piece_X()
check(len(four) == 1 and ic.canon(X) == four[0], "X is the only heptiamond with exactly 4 aspects")
check(len(set(M)) == 7 and ic.connected(M) and len(ic.aspects(M)) == 6, "M: 7 triangles, connected, 6 aspects")
oM = [conv(tuple(x)) for x in o["pieces"]["M"]]
oX = [conv(tuple(x)) for x in o["pieces"]["X"]]
check(ic.canon(oM) == ic.canon(M), "object's M is congruent to M from the definition")
check(ic.canon(oX) == ic.canon(X), "object's X is congruent to X from the definition")

# 4
def count_placements(piece, rows, cols):
    board = {conv((r, c)) for r in range(rows) for c in range(cols)}
    seen = set()
    for a in ic.aspects(piece):
        a = sorted(a)
        anc = a[0]
        for b in board:
            if sum(b) != sum(anc):
                continue
            d = (b[0] - anc[0], b[1] - anc[1], b[2] - anc[2])
            pl = frozenset((x + d[0], y + d[1], z + d[2]) for x, y, z in a)
            if pl <= board:
                seen.add(pl)
    return len(seen)
for e in o["per_k"]:
    nm = count_placements(M, e["board_rows"], e["board_cols"])
    nx = count_placements(X, e["board_rows"], e["board_cols"])
    check(nm == e["n_placements_M"] and nx == e["n_placements_X"],
          "k=%d: placements in board M %d / X %d (object %d / %d)" % (e["k"], nm, nx, e["n_placements_M"], e["n_placements_X"]))

# 5
# positive control: heptiamond B (package coordinates below) is listed as 2 tiles with M on the page;
# the same search must find a common figure at k = 2, and none for the pair M-C (listed 6) at k = 2.
B = [conv(t) for t in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (1, 3)]]
C = [conv(t) for t in [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (1, 6)]]
check(len(ic.tilings_union(M, 2) & ic.tilings_union(B, 2)) > 0, "control: M-B (listed 2) has a common figure at k=2")
check(len(ic.tilings_union(M, 2) & ic.tilings_union(C, 2)) == 0, "control: M-C (listed 6) has none at k=2")
kmax = int(os.environ.get("KMAX", "4"))
for k in range(2, kmax + 1):
    fm, fx = ic.tilings_union(M, k), ic.tilings_union(X, k)
    check(not (fm & fx), "k=%d: %d connected M-figures, %d connected X-figures, %d in common (no board limit)" % (k, len(fm), len(fx), len(fm & fx)))

print("FAIL" if fails else "PASS")
sys.exit(1 if fails else 0)
