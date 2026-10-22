"""Fast exact checks of the package (Python standard library only; seconds).

What it checks:
 1. Integrity: every file in object/ matches verify-it-yourself/OBJECT_FILES.sha256.
 2. The exact trace-count table object/counts_b333_s6.txt is a complete, consistent census of the 2^27 states of
    the 3x3x3 block: for every face f and every number k of open sites, the counts over traces S sum to C(27, k);
    traces fit the 9 sites of a face; and states with fewer than 6 open sites have the empty trace (the designated
    set G is empty when its size is below 6, so it is empty whenever fewer than 6 sites are open).
 3. The chain in object/bound.json: q_1 = 501/1000 > 1/2 (so theta(q_1) > 0 by Campanino-Russo's p_c <= 1/2),
    q_j = p_{j-1}, and the last p equals the claimed bound 4427/10000 < 1/2.
 4. The root condition of every link, in exact rationals from the count table:
    r_f(full face) = P_p(G's trace on the facing face is nonempty) >= q_j for all six faces.
What it does not check (FULL=1 sh verify-it-yourself/run_checks.sh does, with the Go engine, ~12 minutes): the
3066 x 7579 up-set inequalities of each link, which need the joint traces of all 2^27 states.
"""
import hashlib
import json
import os
import sys
from fractions import Fraction
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPP = [1, 0, 3, 2, 5, 4]
fails = []


def fail(msg):
    fails.append(msg)
    print("FAIL:", msg)


def main():
    # 1. integrity
    with open(os.path.join(ROOT, "verify-it-yourself", "OBJECT_FILES.sha256")) as f:
        listed = [line.split(None, 1) for line in f if line.strip()]
    for h, name in listed:
        name = name.strip().lstrip("*")
        p = os.path.join(ROOT, name)
        if not os.path.isfile(p):
            fail("missing object file %s" % name)
            continue
        if hashlib.sha256(open(p, "rb").read()).hexdigest() != h:
            fail("object file changed: %s" % name)
    print("1. integrity: %d object files checked" % len(listed))

    # 2. census
    n = None
    C = {}
    with open(os.path.join(ROOT, "object", "counts_b333_s6.txt")) as fh:
        for line in fh:
            w = line.split()
            if w[0] == "dims":
                n = int(w[w.index("n") + 1])
                ms = int(w[w.index("minSize") + 1])
                continue
            f, k, S, v = map(int, w[1:])
            d = C.setdefault(f, {})
            d[(k, S)] = d.get((k, S), 0) + v
    if n != 27 or ms != 6:
        fail("header says n = %s, minSize = %s" % (n, ms))
    for f in range(6):
        for k in range(n + 1):
            tot = sum(v for (kk, S), v in C[f].items() if kk == k)
            if tot != comb(n, k):
                fail("face %d, k = %d: counts sum to %d, not C(27,%d) = %d" % (f, k, tot, k, comb(n, k)))
        for (k, S), v in C[f].items():
            if not 0 <= S < 512 or v <= 0:
                fail("face %d: bad entry (%d, %d, %d)" % (f, k, S, v))
            if k < ms and S != 0:
                fail("face %d: nonempty trace with only %d open sites" % (f, k))
    print("2. census: 6 faces x 28 values of k sum to the binomial coefficients; minimum size respected")

    # 3. chain logic
    b = json.load(open(os.path.join(ROOT, "object", "bound.json")))
    chain = [(Fraction(x["p"]), Fraction(x["q"])) for x in b["chain"]]
    if chain[0][1] != Fraction(501, 1000) or not chain[0][1] > Fraction(1, 2):
        fail("base q_1 is %s, expected 501/1000 > 1/2" % chain[0][1])
    for j in range(1, len(chain)):
        if chain[j][1] != chain[j - 1][0]:
            fail("link %d: q = %s but the previous p is %s" % (j + 1, chain[j][1], chain[j - 1][0]))
    if chain[-1][0] != Fraction(b["bound"]) or Fraction(b["bound"]) != Fraction(4427, 10000):
        fail("the last p (%s) is not the claimed bound 4427/10000" % chain[-1][0])
    if not Fraction(b["bound"]) < Fraction(1, 2):
        fail("bound not below 1/2")
    print("3. chain: %d links, q_1 = 501/1000, q_j = p_(j-1), last p = %s" % (len(chain), chain[-1][0]))

    # 4. root conditions, exact
    worst = None
    for j, (p, q) in enumerate(chain, 1):
        pw = [p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
        for f in range(6):
            g = OPP[f]
            empty = sum((v * pw[k] for (k, S), v in C[g].items() if S == 0), Fraction(0))
            r = 1 - empty
            if r < q:
                fail("link %d face %d: r(full face) = %s < q = %s" % (j, f, float(r), q))
            m = r - q
            if worst is None or m < worst[0]:
                worst = (m, j, f)
    print("4. root: r_f(full face) - q_j >= %.6f in every link (link %d, face %d)" % (float(worst[0]), worst[1], worst[2]))

    if fails:
        print("FAIL (%d problems)" % len(fails))
        sys.exit(1)
    print("PASS (fast exact checks; FULL=1 reruns the exhaustive certificate with the Go engine)")


if __name__ == "__main__":
    main()
