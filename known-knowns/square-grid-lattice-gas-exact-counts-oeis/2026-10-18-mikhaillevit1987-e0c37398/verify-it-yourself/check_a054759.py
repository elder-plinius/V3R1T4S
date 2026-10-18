"""Standalone checker for A054759(16) (Python 3 standard library only).
Usage: python check_a054759.py object/a054759_16.txt   -> prints VALID (exit 0) or INVALID (exit 1).

Definition: A054759(n) = number of Eulerian orientations of the n x n torus grid graph (every vertex has
in-degree 2 and out-degree 2; square ice). Checks:
 1. method: an independent whole-row transfer matrix, split into flux sectors, computed exactly with Python
    integers, reproduces the published terms a(1..9);
 2. every prime used below is prime (deterministic Miller-Rabin, valid below 3.3e24);
 3. the claimed integer is below the trivial bound 2^(n^2+n) (an orientation is fixed by its n^2 vertical
    bits plus one horizontal wrap bit per row), and at least two saved runs have a modulus above that bound, so
    each of them alone determines the value (the other runs are agreement checks);
 4. the claimed integer equals, residue by residue, all five independent saved runs (residues.json): the
    author's modes A and B, the reproduction skeptic's two own runs, and the author's program on the
    skeptic's fresh primes."""
import itertools, json, os, sys

N = 16
# OEIS A054759, a(1..9) (b-file https://oeis.org/A054759/b054759.txt)
PUBLISHED = [4, 18, 148, 2970, 143224, 16448400, 4484823396, 2901094068042, 4448410550095612]


def row_count(n):
    """trace(T^n) for the row transfer matrix, block-diagonal by popcount of the vertical bits."""
    total = 0
    for k in range(n + 1):
        st = [sum(1 << i for i in c) for c in itertools.combinations(range(n), k)]
        m = len(st)
        T = [[0] * m for _ in range(m)]
        for i, a in enumerate(st):          # a: vertical arrows entering the row from below
            for j, b in enumerate(st):      # b: vertical arrows leaving the row upward
                for x0 in (0, 1):           # horizontal edge across the wrap
                    h, ok = x0, True
                    for c in range(n):      # ice rule: in(v below) + in(h left) = out(v above) + out(h right)
                        h = ((a >> c) & 1) + h - ((b >> c) & 1)
                        if h not in (0, 1):
                            ok = False
                            break
                    if ok and h == x0:
                        T[i][j] += 1
        R = [[int(i == j) for j in range(m)] for i in range(m)]
        for _ in range(n):
            R = [[sum(R[i][l] * T[l][j] for l in range(m) if R[i][l]) for j in range(m)] for i in range(m)]
        total += sum(R[i][i] for i in range(m))
    return total


def is_prime(p):
    if p < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for q in small:
        if p % q == 0:
            return p == q
    d, s = p - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in small:
        x = pow(a, d, p)
        if x in (1, p - 1):
            continue
        for _ in range(s - 1):
            x = x * x % p
            if x == p - 1:
                break
        else:
            return False
    return True


def main(path):
    ok = True
    text = open(path, encoding="ascii").read()
    if not text.strip().isdigit():
        print("object is not one decimal integer")
        return False
    v = int(text)
    print("claimed a(%d) = %d (%d digits)" % (N, v, len(str(v))))
    small = [row_count(n) for n in range(1, len(PUBLISHED) + 1)]
    print("independent row transfer matrix, n = 1..%d:" % len(PUBLISHED), "match" if small == PUBLISHED else "MISMATCH")
    ok &= small == PUBLISHED
    here = os.path.dirname(os.path.abspath(__file__))
    runs = json.load(open(os.path.join(here, "residues.json"), encoding="utf-8"))
    bound = 1 << (N * N + N)
    if not 0 < v < bound:
        print("value outside (0, 2^%d)" % (N * N + N))
        ok = False
    determined = 0
    for run in runs:
        mods = [int(m) for m in run["residues"]]
        prod = 1
        for m in mods:
            prod *= m
        primes_ok = all(m == 1 << 64 or is_prime(m) for m in mods)
        match = all(v % int(m) == int(r) for m, r in run["residues"].items())
        print("%-58s moduli %s, product 2^%d, residues %s" % (
            run["run"], "ok" if primes_ok else "NOT PRIME", prod.bit_length() - 1, "match" if match else "MISMATCH"))
        ok &= primes_ok and match
        determined += prod > bound
    # a run whose modulus exceeds the bound pins the integer exactly; the others are agreement checks
    print("runs that alone determine a(%d) (modulus > 2^%d): %d" % (N, N * N + N, determined))
    ok &= determined >= 2
    return ok


if __name__ == "__main__":
    good = main(sys.argv[1])
    print("VALID" if good else "INVALID")
    sys.exit(0 if good else 1)
