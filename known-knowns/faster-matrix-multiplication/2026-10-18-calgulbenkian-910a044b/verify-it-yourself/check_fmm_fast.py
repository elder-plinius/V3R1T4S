#!/usr/bin/env python3
"""Exact Brent-equation check for a matrix multiplication scheme, standard library only.

Usage: python3 check_fmm_fast.py SCHEME.json [--expect-rank R] [--expect-class ZT|Z]

The scheme file holds "n": [n1, n2, n3] and lists "u", "v", "w" of equal length (one entry per rank-one term),
in one of three row encodings: dense rows; "encoding": "sparse_flat_pairs" (rows [index, value, index, value, ...]);
or "encoding": "vocab_rle_v1" (comma-separated indices into the list "vocab", "i*k" meaning index i repeated k
times). Values are integers or "p/q" strings. Index convention: u[i*n2 + j] is the coefficient of A[i][j],
v[j*n3 + l] the coefficient of B[j][l], and w[l*n1 + i] the coefficient of C[i][l].

Definition checked (the Brent equations): for all i, i2 in [0,n1), j, j2 in [0,n2), l, l2 in [0,n3),
    sum_t u_t[i*n2 + j] * v_t[j2*n3 + l] * w_t[l2*n1 + i2] = [j == j2] * [l == l2] * [i == i2],
which says that C[i][l] = sum_t w_t[l*n1 + i] * (sum u_t[.] A) * (sum v_t[.] B) equals (A B)[i][l] for all A, B.

Method, all in exact integer arithmetic (no floating point, no modular reduction, no sampling):
1. Each of U, V, W is scaled by the least common multiple of its denominators (DU, DV, DW), giving integers; the
   equations become sum_t U'_t[a] V'_t[b] W'_t[c] = D * target[a][b][c] with D = DU * DV * DW.
2. For each term, the W' row is packed into one Python integer P_t = sum_c W'_t[c] * 2^(s*c) with slot width s
   bits. For every pair (a, b) the packed sum X[a][b] = sum_t U'_t[a] * V'_t[b] * P_t is formed exactly.
3. Slot width: s is chosen with 2^(s-1) > max(D, B), where B = sum_t max|U'_t| * max|V'_t| * max|W'_t| bounds
   every coefficient |sum_t U'_t[a] V'_t[b] W'_t[c]|. A vector of integers each of absolute value below 2^(s-1)
   has a unique balanced base-2^s representation, so X[a][b] equals the packed target Y[a][b] exactly when all
   n3*n1 slot equations hold. Every pair (a, b) is compared, including pairs no term touches (X = 0).
Coefficient-class check (added in this copy): the largest absolute value over all coefficients of u, v and w is
reported as maxabs. The class is ZT when every coefficient is in {-1, 0, 1} (maxabs <= 1) and Z otherwise (all
coefficients integers). With --expect-class the run fails when the computed class differs.
Prints PASS or FAIL with the rank (number of terms with all three factors nonzero) and exits 0 on PASS.
"""
import json
import sys
from fractions import Fraction
from math import gcd


def lcm(a, b):
    return a // gcd(a, b) * b


def rle_row(row, vocab, length):
    dense = []
    for tok in row.split(","):
        if "*" in tok:
            i, k = tok.split("*")
            dense += [vocab[int(i)]] * int(k)
        else:
            dense.append(vocab[int(tok)])
    if len(dense) != length:
        raise ValueError(f"decoded row has length {len(dense)}, expected {length}")
    return list(enumerate(dense))


def rows(d, key, length):
    out = []
    for row in d[key]:
        enc = d.get("encoding")
        if enc == "sparse_flat_pairs":
            if len(row) % 2:
                raise ValueError(f"{key} sparse row has odd length")
            pairs = list(zip(row[0::2], row[1::2]))
        elif enc == "vocab_rle_v1":
            pairs = rle_row(row, d["vocab"], length)
        elif enc is None:
            if len(row) != length:
                raise ValueError(f"{key} row has length {len(row)}, expected {length}")
            pairs = list(enumerate(row))
        else:
            raise ValueError(f"unknown encoding {enc!r}")
        r = {}
        for a, x in pairs:
            if isinstance(a, bool) or not isinstance(a, int) or not 0 <= a < length:
                raise ValueError(f"{key} index {a!r} out of range")
            if isinstance(x, bool) or not isinstance(x, (int, str)):
                raise ValueError(f"{key} coefficient {x!r} is not an integer or 'p/q' string")
            v = Fraction(x)
            if a in r:
                raise ValueError(f"{key} index {a} repeated in one row")
            if v:
                r[a] = v
        out.append(r)
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    expect = None
    if "--expect-rank" in args:
        expect = int(args[args.index("--expect-rank") + 1])
    expect_class = args[args.index("--expect-class") + 1] if "--expect-class" in args else None
    d = json.load(open(path))
    n1, n2, n3 = (int(x) for x in d["n"])
    A, B, C = n1 * n2, n2 * n3, n3 * n1
    U, V, W = rows(d, "u", A), rows(d, "v", B), rows(d, "w", C)
    if not len(U) == len(V) == len(W):
        print("FAIL: u, v, w have different lengths")
        return 1
    allvals = [x for R in (U, V, W) for r in R for x in r.values()]
    if any(x.denominator != 1 for x in allvals):
        print("FAIL: a coefficient is not an integer")
        return 1
    maxabs = int(max((abs(x) for x in allvals), default=0))
    coef_class = "ZT" if maxabs <= 1 else "Z"
    terms = [(u, v, w) for u, v, w in zip(U, V, W) if u and v and w]
    rank = len(terms)
    DU = DV = DW = 1
    for u, v, w in terms:
        for x in u.values():
            DU = lcm(DU, x.denominator)
        for x in v.values():
            DV = lcm(DV, x.denominator)
        for x in w.values():
            DW = lcm(DW, x.denominator)
    D = DU * DV * DW
    iterms = []
    bound = 0
    for u, v, w in terms:
        ui = {a: int(x * DU) for a, x in u.items()}
        vi = {b: int(x * DV) for b, x in v.items()}
        wi = {c: int(x * DW) for c, x in w.items()}
        bound += max(map(abs, ui.values())) * max(map(abs, vi.values())) * max(map(abs, wi.values()))
        iterms.append((ui, vi, wi))
    s = max(D, bound).bit_length() + 2  # 2^(s-1) > max(D, bound)
    X = {}
    for ui, vi, wi in iterms:
        P = 0
        for c, x in wi.items():
            P += x << (s * c)
        for a, x in ui.items():
            Pa = x * P
            for b, y in vi.items():
                key = a * B + b
                X[key] = X.get(key, 0) + y * Pa
    bad = 0
    first = None
    for i in range(n1):
        for j in range(n2):
            a = i * n2 + j
            for j2 in range(n2):
                for l in range(n3):
                    b = j2 * n3 + l
                    got = X.pop(a * B + b, 0)
                    want = (D << (s * (l * n1 + i))) if j == j2 else 0
                    if got != want:
                        bad += 1
                        if first is None:
                            first = (i, j, j2, l)
    if X:
        print("FAIL: internal error, unexpected index pairs")
        return 1
    fmt = f"{n1}x{n2}x{n3}"
    if bad:
        i, j, j2, l = first
        print(f"FAIL format={fmt} rank={rank}: {bad} of {A * B} (a, b) blocks differ; first at "
              f"A[{i}][{j}] x B[{j2}][{l}]")
        return 1
    if expect is not None and rank != expect:
        print(f"FAIL format={fmt}: rank {rank} != expected {expect}")
        return 1
    if expect_class is not None and coef_class != expect_class:
        print(f"FAIL format={fmt}: coefficient class {coef_class} (maxabs {maxabs}) != expected {expect_class}")
        return 1
    print(f"coefficient class: {coef_class} (max |coefficient| = {maxabs}; ZT means all coefficients in {{-1, 0, 1}})")
    print(f"exact integer check: D={D} (DU={DU}, DV={DV}, DW={DW}), coefficient bound {bound.bit_length()} bits, "
          f"slot width {s} bits, {A * B} blocks of {C} slots compared")
    print(f"PASS format={fmt} rank={rank}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
