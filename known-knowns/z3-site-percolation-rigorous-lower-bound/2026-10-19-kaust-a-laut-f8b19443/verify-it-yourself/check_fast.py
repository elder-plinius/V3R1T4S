"""Fast exact checks of the package (Python standard library only; about half a minute).

What it checks:
 1. Integrity: every listed object file matches verify-it-yourself/OBJECT_FILES.sha256.
 2. Definitions: for N = 3..8 it enumerates every neighbour-avoiding walk (NAW) from the origin, computes the
    forced-closed set F = S u C and the extension set E from the complete path exactly as object/PROOF.md defines
    them, and compares the walk count and every coefficient c_f with the tables object/outputs/small/pNN.txt written
    by the package's enumerator (object/code/par). This checker shares no code with that enumerator.
 3. Chain and anchors: sum_f c_f(N) equals the walk total a_(N+1) of the next table wherever both exist, and every
    table agrees with the published neighbour-avoiding walk counts of the simple cubic lattice (OEIS A174319): its
    walk total equals a_N and its sum of c_f equals a_(N+1) (up to a_21 for the N = 20 certificate).
 4. The certificate, in exact integer arithmetic from object/outputs/p20.txt and object/result/bound.json:
    K_20(p*) < 1 at p* = 263376/10^6 (this proves p_c^site(Z^3) >= p*), K_20(p* + 10^-6) > 1 (p* is the largest
    such value on the 10^-6 grid), and K_20(5/19) < 1.
What it does not check (GO=1 and FULL=1 sh verify-it-yourself/run_checks.sh do, with Go): that the enumerator
reproduces the N = 16, 18 and 20 tables (N = 20 takes about 2.5 hours on 6 cores).
"""
import hashlib
import json
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]  # direction index 0..5
# OEIS A174319 (n-step neighbour-avoiding walks on the simple cubic lattice), n = 3..21, copied by script from
# https://oeis.org/A174319/b174319.txt (fetched 2026-10-19T19:18:56Z, sha256 7452b267...e115f)
A174319 = {3: 126, 4: 534, 5: 2214, 6: 9246, 7: 38142, 8: 157974, 9: 649086, 10: 2675022, 11: 10966470, 12: 45054630, 13: 184400910, 14: 755930958, 15: 3089851782, 16: 12645783414, 17: 51635728518, 18: 211059485310, 19: 861083848998, 20: 3516072837894, 21: 14334995983614}
fails = []


def fail(msg):
    fails.append(msg)
    print("FAIL:", msg)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def nbrs(x):
    return [add(x, d) for d in DIRS]


def read_table(path):
    total = ext = n = None
    for line in open(path):
        w = line.split()
        if w and w[0] == "TOTAL":
            n, total = int(w[1]), int(w[2])
        elif w and w[0] == "EXT":
            ext = {int(a): int(b) for a, b in (t.split(":") for t in w[2:])}
    return n, total, {f: c for f, c in ext.items() if c}


def brute(N):
    """Walk count and c_f for N-step NAWs, from the PROOF.md definitions applied to each complete path."""
    path = [(0, 0, 0)]
    on = {path[0]}
    total = 0
    ext = {}

    def leaf():
        idx = {v: i for i, v in enumerate(path)}
        S = set()
        for w in {w for v in path for w in nbrs(v)} - on:
            ids = [idx[z] for z in nbrs(w) if z in idx]
            if max(ids) - min(ids) >= 3:
                S.add(w)
        Cn = set()
        for k in range(1, N):
            a, b, c = path[k - 1], path[k], path[k + 1]
            if sub(c, b) != sub(b, a):
                u = add(sub(a, b), c)
                if DIRS.index(sub(u, c)) < DIRS.index(sub(b, c)):
                    Cn.add(u)
        F = S | Cn
        if F & on:
            fail("F meets the path (Lemma 0) at N = %d" % N)
        E = 0
        for y in nbrs(path[N]):
            if y in on or y in F or any(z in idx and idx[z] < N for z in nbrs(y)):
                continue
            E += 1
        ext[len(F)] = ext.get(len(F), 0) + E

    def rec():
        nonlocal total
        if len(path) == N + 1:
            total += 1
            leaf()
            return
        x = path[-1]
        for y in nbrs(x):
            if y in on or any(z in on and z != x for z in nbrs(y)):
                continue
            path.append(y)
            on.add(y)
            rec()
            on.remove(y)
            path.pop()

    rec()
    return total, {f: c for f, c in ext.items() if c}


def K_less_than_one(ext, N, p):
    """Exact test of K_N(p) < 1 for rational p, by integers over a common denominator."""
    a, b = p.numerator, p.denominator
    fmax = max(ext)
    num = sum(c * a ** (N + 1) * (b - a) ** f * b ** (fmax - f) for f, c in ext.items())
    return num < b ** (N + 1 + fmax), Fraction(num, b ** (N + 1 + fmax))


def main():
    # 1. integrity
    listed = [line.split(None, 1) for line in open(os.path.join(ROOT, "verify-it-yourself", "OBJECT_FILES.sha256"))
              if line.strip()]
    for h, name in listed:
        p = os.path.join(ROOT, name.strip().lstrip("*"))
        if not os.path.isfile(p):
            fail("missing object file %s" % name.strip())
        elif hashlib.sha256(open(p, "rb").read()).hexdigest() != h:
            fail("object file changed: %s" % name.strip())
    print("1. integrity: %d object files checked" % len(listed))

    # 2. definitions vs the enumerator's small tables
    tables = {}
    for n in range(3, 15):
        tables[n] = read_table(os.path.join(ROOT, "object", "outputs", "small", "p%02d.txt" % n))
    for n in (16, 18, 20):
        tables[n] = read_table(os.path.join(ROOT, "object", "outputs", "p%d.txt" % n))
    for n, t in tables.items():
        if t[0] != n:
            fail("table for N = %d is labelled N = %s" % (n, t[0]))
    for N in range(3, 9):
        tot, ext = brute(N)
        if (tot, ext) != (tables[N][1], tables[N][2]):
            fail("N = %d: definitions give %d walks %s; the table has %d %s" % (N, tot, ext, tables[N][1], tables[N][2]))
    print("2. definitions: walk counts and every c_f agree for N = 3..8 (enumerated from complete paths)")

    # 3. chain and published anchors
    nchain = 0
    for n in tables:
        if n + 1 in tables:
            nchain += 1
            if sum(tables[n][2].values()) != tables[n + 1][1]:
                fail("sum c_f(%d) != a_%d" % (n, n + 1))
    for n in tables:
        if tables[n][1] != A174319[n]:
            fail("a_%d = %d, OEIS A174319 has %d" % (n, tables[n][1], A174319[n]))
        if sum(tables[n][2].values()) != A174319[n + 1]:
            fail("sum c_f(%d) = %d, OEIS A174319 a_%d = %d" % (n, sum(tables[n][2].values()), n + 1, A174319[n + 1]))
    print("3. chain: sum c_f(N) = a_(N+1) for %d consecutive pairs; all %d tables match OEIS A174319 (a_N and a_(N+1))"
          % (nchain, len(tables)))

    # 4. the certificate
    bound = json.load(open(os.path.join(ROOT, "object", "result", "bound.json")))
    pstar = Fraction(bound["bound"]["numerator"], bound["bound"]["denominator"])
    N, _, ext = tables[20]
    if bound["N"] != 20 or pstar != Fraction(263376, 10 ** 6):
        fail("bound.json does not state N = 20 and p* = 263376/10^6")
    ok, k = K_less_than_one(ext, N, pstar)
    if not ok:
        fail("K_20(p*) >= 1")
    ok2, k2 = K_less_than_one(ext, N, pstar + Fraction(1, 10 ** 6))
    if ok2:
        fail("K_20(p* + 10^-6) < 1: p* is not the largest grid value")
    ok3, k3 = K_less_than_one(ext, N, Fraction(5, 19))
    if not ok3:
        fail("K_20(5/19) >= 1")
    print("4. certificate: K_20(%d/10^6) = %.12f < 1; K_20(p* + 10^-6) = %.12f > 1; K_20(5/19) = %.12f < 1"
          % (pstar * 10 ** 6, float(k), float(k2), float(k3)))

    if fails:
        print("FAIL (%d problems)" % len(fails))
        sys.exit(1)
    print("PASS (fast exact checks: p_c^site(Z^3) >= 263376/10^6; GO=1 or FULL=1 reruns the enumerator)")


main()
