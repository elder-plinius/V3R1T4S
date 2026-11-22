#!/usr/bin/env python3
"""check_decision.py - checks object/DECISION.txt against the package and against fresh program output.

Written from the definition (Graham and Sloane 1980): a graph with q edges is harmonious if its vertices get
distinct labels in Z_q such that the q edge sums f(u)+f(v) mod q are pairwise distinct. K_n^(2) is two copies of K_n
sharing one vertex c, so it has 2n-1 vertices and q = n(n-1) edges. Standard library only.

  python3 check_decision.py pins            header lines and every pinned sha256 in object/DECISION.txt
  python3 check_decision.py compare OUTDIR  every 'expect' line against fresh outputs OUTDIR/P1_<n>.txt,
                                            OUTDIR/P2_<n>.txt, OUTDIR/brute_4.txt (P1 files optional)
  python3 check_decision.py n4list          object/evidence/n4_solutions_P{1,2}.txt against an independent
                                            enumeration of all ordered pairs for n = 4 made here
Each mode prints OK lines and ends with 'MODE: PASS' or 'MODE: FAIL'; exit status 0 or 1.
"""
import hashlib, itertools, os, re, sys

DECISION = os.path.join("object", "DECISION.txt")


def load():
    head, expects, pins = {}, [], []
    for line in open(DECISION, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("expect "):
            _, prog, n, field, value = line.split()
            expects.append((prog, int(n), field, int(value)))
        elif line.startswith("pin "):
            _, h, path = line.split()
            pins.append((h, path))
        else:
            k, _, v = line.partition(":")
            head[k.strip()] = v.strip()
    return head, expects, pins


def kv(path):
    out = {}
    if os.path.isfile(path):
        for m in re.finditer(r"([A-Za-z_0-9]+)=(-?\d+)", open(path, encoding="utf-8").read()):
            out[m.group(1)] = int(m.group(2))
        for m in re.finditer(r"brute_force_labelings (\d+)", open(path, encoding="utf-8").read()):
            out["brute_force_labelings"] = int(m.group(1))
    return out


def mode_pins():
    head, expects, pins = load()
    bad = 0
    want = {"target": "windmill-kn2-harmonious-graham-sloane", "cell": "n = 8", "decision": "NOT HARMONIOUS"}
    for k, v in want.items():
        if head.get(k) != v:
            print("header %s: got %r, want %r" % (k, head.get(k), v)); bad += 1
        else:
            print("OK header %s: %s" % (k, v))
    if not pins or not expects:
        print("no pins or no expect lines"); bad += 1
    for h, path in pins:
        if not os.path.isfile(path):
            print("MISSING pinned file %s" % path); bad += 1; continue
        got = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if got != h:
            print("sha256 MISMATCH %s (got %s)" % (path, got)); bad += 1
        else:
            print("OK sha256 %s" % path)
    # the pinned run outputs must state the same n = 8 numbers as the expect lines
    exp = {(p, n, f): v for p, n, f, v in expects}
    for prog, fname in (("P1", "object/evidence/P1_wsearch_n8.txt"), ("P2", "object/evidence/P2_mitm_n8.txt")):
        d = kv(fname)
        for f in ("sum_distinct_sets_containing_0", "solutions_ordered_pairs"):
            if d.get(f) != exp.get((prog, 8, f)):
                print("%s: %s=%s disagrees with DECISION.txt (%s)" % (fname, f, d.get(f), exp.get((prog, 8, f)))); bad += 1
            else:
                print("OK %s %s=%d" % (fname, f, d[f]))
    print("PINS: " + ("PASS" if bad == 0 else "FAIL"))
    return bad == 0


def mode_compare(outdir):
    _, expects, _ = load()
    bad, skipped = 0, 0
    for prog, n, field, value in expects:
        if prog == "N4LIST":
            continue
        path = os.path.join(outdir, "brute_4.txt" if prog == "BRUTE" else "%s_%d.txt" % (prog, n))
        if prog == "P1" and not os.path.isfile(path):
            skipped += 1; continue
        got = kv(path).get(field)
        if got != value:
            print("%s n=%d %s: got %s, DECISION.txt says %d" % (prog, n, field, got, value)); bad += 1
        else:
            print("OK %s n=%d %s=%d" % (prog, n, field, got))
    if skipped:
        print("note: %d P1 lines skipped (no C compiler; P2 and the other checks still decide)" % skipped)
    # the verdict must follow from the counts: n = 8 has zero labelings in every program that ran
    for prog in ("P1", "P2"):
        p = os.path.join(outdir, "%s_8.txt" % prog)
        if os.path.isfile(p):
            t = open(p, encoding="utf-8").read()
            if "VERDICT n=8: NOT HARMONIOUS" not in t or "SOLUTION" in t:
                print("%s n=8: verdict line missing or a SOLUTION was printed" % prog); bad += 1
            else:
                print("OK %s n=8 verdict: NOT HARMONIOUS" % prog)
    if not os.path.isfile(os.path.join(outdir, "P2_8.txt")):
        print("P2 n=8 output missing"); bad += 1
    print("COMPARE: " + ("PASS" if bad == 0 else "FAIL"))
    return bad == 0


def harmonious_pair(n, A, B):
    """A, B: label sets of the two cliques, both containing the shared label 0 (f(c) = 0)."""
    q = n * (n - 1)
    if len(set(A) | set(B)) != 2 * n - 1:
        return False
    sums = [(x + y) % q for S in (A, B) for x, y in itertools.combinations(S, 2)]
    return len(sums) == q and len(set(sums)) == q


def mode_n4list():
    _, expects, _ = load()
    want = {(p, f): v for p, n, f, v in expects if n == 4}
    n, q = 4, 12
    mine = set()
    for a in itertools.combinations(range(1, q), n - 1):
        for b in itertools.combinations([x for x in range(1, q) if x not in a], n - 1):
            if harmonious_pair(n, (0,) + a, (0,) + b):
                mine.add(((0,) + a, (0,) + b))
    bad = 0
    print("independent enumeration here: %d ordered pairs for n = 4" % len(mine))
    if len(mine) != want.get(("N4LIST", "ordered_pairs")):
        print("count differs from DECISION.txt"); bad += 1
    for f in ("n4_solutions_P1.txt", "n4_solutions_P2.txt"):
        rows = set()
        for line in open(os.path.join("object", "evidence", f), encoding="utf-8"):
            if line.strip():
                a, b = line.strip().split("|")
                rows.add((tuple(int(x) for x in a.split(",")), tuple(int(x) for x in b.split(","))))
        if rows != mine:
            print("%s: differs from the independent enumeration (%d rows)" % (f, len(rows))); bad += 1
        else:
            print("OK %s: the same %d ordered pairs" % (f, len(rows)))
    # translation control: 48 pairs x 12 translations x 3! x 3! orderings = unreduced brute-force count
    if len(mine) * q * 36 != want.get(("BRUTE", "brute_force_labelings")):
        print("translation identity fails"); bad += 1
    else:
        print("OK %d x %d x 3! x 3! = %d (unreduced brute force)" % (len(mine), q, len(mine) * q * 36))
    # negative controls straight from the definition: a repeated label, and the same clique twice
    a, b = sorted(mine)[0]
    for name, B in (("repeated label", (0, a[1]) + b[2:]), ("same clique twice", a)):
        if harmonious_pair(n, a, B):
            print("control (%s) accepted" % name); bad += 1
        else:
            print("OK control (%s) rejected" % name)
    print("N4LIST: " + ("PASS" if bad == 0 else "FAIL"))
    return bad == 0


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else ""
    ok = mode_pins() if m == "pins" else mode_compare(sys.argv[2]) if m == "compare" else mode_n4list() if m == "n4list" else None
    if ok is None:
        print(__doc__); sys.exit(2)
    sys.exit(0 if ok else 1)
