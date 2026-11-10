"""Exact check of a qubit stabilizer code [[n,k,d]] given as X and Z rows (n-k generators). Standard library only.
Usage: python3 qecc_check.py object.json
 1) symplectic self-orthogonality of all generators
 2) GF(2) rank equals n-k
 3) weight distribution A of the stabilizer group S (2^(n-k) elements) and, by the quantum MacWilliams identity
    in exact integers, the normalizer distribution B; d = min j with B_j > A_j
 4) independent direct check: every Pauli of weight 1..d anticommutes with a generator or lies in S, except
    weight d, where the count of normalizer elements outside S equals B_d - A_d (and is positive)
The last line printed is a JSON object with the result."""
import sys, json, itertools
from math import comb


def bits(row):
    return sum(1 << i for i, b in enumerate(row) if b)


def sp(a, b):
    return (bin((a[0] & b[1]) ^ (a[1] & b[0])).count('1')) & 1


def main(f):
    d = json.load(open(f))
    X = [bits(r) for r in d['X']]
    Z = [bits(r) for r in d['Z']]
    n = d['n']
    k = d['k']
    r = len(X)
    assert len(Z) == r and r == n - k, (r, n, k)
    assert all(len(row) == n for row in d['X']) and all(len(row) == n for row in d['Z'])
    gens = list(zip(X, Z))
    ok_orth = all(sp(a, b) == 0 for a in gens for b in gens)
    basis = []

    def red(v):
        for b in basis:
            v = min(v, v ^ b)
        return v
    for x, z in gens:
        v = red(x | (z << n))
        if v:
            basis.append(v)
            basis.sort(reverse=True)
    rank = len(basis)
    A = [0] * (n + 1)
    elems = [(0, 0)]
    for x, z in gens:
        elems += [(a ^ x, b ^ z) for a, b in elems]
    for a, b in elems:
        A[bin(a | b).count('1')] += 1
    assert sum(A) == 2 ** r

    def Kr(j, i, q=4):
        return sum((-1) ** s * (q - 1) ** (j - s) * comb(i, s) * comb(n - i, j - s) for s in range(j + 1))
    B = []
    for j in range(n + 1):
        tot = sum(A[i] * Kr(j, i) for i in range(n + 1))
        assert tot % (2 ** r) == 0
        B.append(tot // 2 ** r)
    assert sum(B) == 2 ** (n + k)
    dist = min(j for j in range(1, n + 1) if B[j] > A[j])
    syn = [[0] * 3 for _ in range(n)]
    for q in range(n):
        for t, (px, pz) in enumerate([(1, 0), (1, 1), (0, 1)]):
            s = 0
            for i, (x, z) in enumerate(gens):
                a = (x >> q) & 1
                b = (z >> q) & 1
                if (px & b) ^ (pz & a):
                    s |= 1 << i
            syn[q][t] = s
    bad = {}
    for w in range(1, dist + 1):
        c = 0
        for pos in itertools.combinations(range(n), w):
            for ts in itertools.product(range(3), repeat=w):
                s = 0
                for q, t in zip(pos, ts):
                    s ^= syn[q][t]
                if s == 0:
                    x = z = 0
                    for q, t in zip(pos, ts):
                        if t in (0, 1):
                            x |= 1 << q
                        if t in (1, 2):
                            z |= 1 << q
                    if red(x | (z << n)) != 0:
                        c += 1
        bad[w] = c
    ok = (ok_orth and rank == r and bad.get(dist, 0) == B[dist] - A[dist] and B[dist] - A[dist] > 0
          and all(bad[w] == 0 for w in range(1, dist)))
    print('A (weight distribution of S) =', A)
    print('B_j - A_j for j <= d:', [(j, B[j] - A[j]) for j in range(1, dist + 1)])
    print('direct count of normalizer elements outside S by weight 1..d:', bad)
    print(json.dumps({"n": n, "k": k, "rank": rank, "self_orthogonal": ok_orth, "d": dist,
                      "claimed_d": d['d'], "consistent": bool(ok), "VALID": bool(ok and dist == d['d'])}))


if __name__ == '__main__':
    main(sys.argv[1])
