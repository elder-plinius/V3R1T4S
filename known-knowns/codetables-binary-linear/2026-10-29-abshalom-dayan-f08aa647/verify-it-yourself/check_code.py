"""Checker for a claimed linear code over GF(9), written from the definition (Python standard library only).

  prepare OBJECT.json CODE.txt   validate the object, print n, k and rank(G) over GF(9), write G for m3_mindist
  verdict OBJECT.json M3.out     read m3_mindist's output, re-check its witness here (a nonzero combination of the
                                 rows of G, of the reported weight), and compare (n, k, d) with the claim

GF(9) = GF(3)[w]/(w^2 - w - 1); the element a + b*w is stored as the integer a + 3b.
m3_mindist proves d >= W + 1 by examining every W-subset T of the coordinates: a nonzero codeword of weight <= W is
supported inside some T, and with G in systematic form that happens iff a small submatrix has a nonzero left
kernel vector. It walks W = 1, 2, ... and stops at the first W where such a codeword exists, printing it.
Exit status 0 only when everything matches.
"""
import json
import sys


def mul(x, y):
    a, b, c, d = x % 3, x // 3, y % 3, y // 3
    return (a * c + b * d) % 3 + 3 * ((a * d + b * c + b * d) % 3)   # w^2 = w + 1


def add(x, y):
    return (x % 3 + y % 3) % 3 + 3 * ((x // 3 + y // 3) % 3)


def neg(x):
    return (-(x % 3)) % 3 + 3 * ((-(x // 3)) % 3)


INV = {x: next(y for y in range(1, 9) if mul(x, y) == 1) for x in range(1, 9)}


def rank(rows):
    M = [r[:] for r in rows]
    r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        iv = INV[M[r][c]]
        M[r] = [mul(v, iv) for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = neg(M[i][c])
                M[i] = [add(a, mul(f, b)) for a, b in zip(M[i], M[r])]
        r += 1
    return r


def load(path):
    o = json.load(open(path))
    G = o["G"]
    assert o["q"] == 9, "q must be 9"
    assert len(G) == o["k"] and all(len(r) == o["n"] for r in G), "G must be k x n"
    assert all(isinstance(v, int) and 0 <= v <= 8 for r in G for v in r), "entries must be 0..8"
    return o, G


def main():
    mode, obj = sys.argv[1], sys.argv[2]
    o, G = load(obj)
    if mode == "prepare":
        rk = rank(G)
        print("claimed n=%d k=%d d=%d; computed rank(G)=%d" % (o["n"], o["k"], o["d"], rk))
        if rk != o["k"]:
            print("rank does not equal k")
            sys.exit(1)
        with open(sys.argv[3], "w") as f:
            f.write("%d %d\n" % (len(G), len(G[0])))
            for r in G:
                f.write(" ".join(map(str, r)) + "\n")
        return
    out = open(sys.argv[3]).read().splitlines()
    dl = [l for l in out if l.startswith("d=")]
    full = [l for l in out if "no nonzero codeword of weight <=" in l]
    if not dl:
        print("m3_mindist found no codeword")
        sys.exit(1)
    parts = dict(p.split("=", 1) for p in dl[0].split(" witness=")[0].split())
    d = int(parts["d"])
    wit = list(map(int, dl[0].split("witness=")[1].split()))
    wt = sum(1 for v in wit if v)
    in_span = rank(G + [wit]) == rank(G)
    last_full = full[-1] if full else "none"
    print("m3_mindist: %s; d=%d" % (last_full, d))
    print("witness: weight %d, nonzero codeword of the row space: %s" % (wt, in_span and wt > 0))
    print("computed n=%d k=%d d=%d; claimed n=%d k=%d d=%d" % (len(G[0]), rank(G), d, o["n"], o["k"], o["d"]))
    ok = in_span and wt == d and d == o["d"] and len(G[0]) == o["n"] and rank(G) == o["k"] \
        and last_full.startswith("W=%d:" % (d - 1))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
