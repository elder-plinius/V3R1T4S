#!/usr/bin/env python3
"""Second, independent check (Python standard library): evaluate the scheme as an algorithm on random integer
matrices A (n1 x n2) and B (n2 x n3) in exact rational arithmetic and compare with the schoolbook product AB.
A wrong scheme fails on random inputs with overwhelming probability; this is a spot check that complements the exact
Brent-equation check in check_scheme.py, not a proof on its own.
Usage: check_random_eval.py <dir with u.txt v.txt w.txt> [trials] [seed]     Last line PASS or FAIL; exit 0 / 1."""
import sys, os, re, random
from fractions import Fraction

def load(path):
    fmt = rank = None
    rows = []
    for line in open(path, encoding="ascii"):
        line = line.strip()
        if line.startswith("#"):
            m = re.match(r"#\s*format\s+(\d+)\s+(\d+)\s+(\d+)", line)
            if m:
                fmt = tuple(map(int, m.groups()))
            m = re.match(r"#\s*rank\s+(\d+)", line)
            if m:
                rank = int(m.group(1))
            continue
        rows.append([(int(a), Fraction(b)) for a, b in (tok.split(":") for tok in line.split())])
    return fmt, rank, rows

def main():
    base = sys.argv[1]
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    rnd = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 20261024)
    (f1, r1, U), (f2, r2, V), (f3, r3, W) = (load(os.path.join(base, x + ".txt")) for x in "uvw")
    if not (f1 == f2 == f3 and r1 == r2 == r3 == len(U) == len(V) == len(W)):
        print("files disagree on format or rank"); print("FAIL"); sys.exit(1)
    n1, n2, n3 = f1
    for t in range(trials):
        A = [rnd.randint(-99, 99) for _ in range(n1 * n2)]
        B = [rnd.randint(-99, 99) for _ in range(n2 * n3)]
        C = [Fraction(0)] * (n1 * n3)
        for k in range(r1):
            a = sum(c * A[i] for i, c in U[k])
            if a == 0:
                continue
            b = sum(c * B[i] for i, c in V[k])
            m = a * b
            if m:
                for i, c in W[k]:
                    C[i] += c * m
        want = [sum(A[i * n2 + j] * B[j * n3 + l] for j in range(n2)) for i in range(n1) for l in range(n3)]
        wrong = sum(1 for x, y in zip(C, want) if x != y)
        print("trial %d: %d of %d entries of C differ from AB" % (t + 1, wrong, n1 * n3))
        if wrong:
            print("FAIL"); sys.exit(1)
    print("PASS")

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print("problem: %s: %s" % (type(e).__name__, str(e)[:200])); print("FAIL"); sys.exit(1)
