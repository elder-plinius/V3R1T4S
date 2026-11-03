#!/usr/bin/env python3
"""Rebuild the [[33,3,23;24]]_3 code of PR 405 from recovered data (Python 3, standard library only).

WHAT THIS IS, AND IS NOT
  The contributor's construction script is missing from the package. This script does NOT
  re-run the contributor's search (norm-trace curve, puncturing, scaling search).
  It rebuilds the shipped object from an EXPLICIT description that was RECOVERED from the
  shipped object by reverse engineering (see how-we-built-it/README.md):
     the classical [33,6,23]_9 code D is  rowspace( E * diag(MU)^-1 ),
     where E is the 6 x 33 matrix of the six quadratic monomials x0^2,x0x1,x0x2,x1^2,x1x2,x2^2
     evaluated at the 33 points POINTS of PG(2,9)  (i.e. D = a scaled puncturing of the
     order-2 projective Reed-Muller code [91,6]_9), and MU is a column scaling.
  Then it applies the Hermitian-hull reduction to GF(3) and checks the result against the
  shipped object (same GF(3) row space), and recomputes s, c, k and the exact distance.

GF(9) = GF(3)[i]/(i^2+1); the element a+b*i is coded as the integer a+3*b.
GF(9)-vector c = x + i*z  <->  GF(3) symplectic vector (x | z).  Symplectic form <(x|z),(x'|z')> = x.z' - z.x'.

Usage: python3 rebuild_eaqecc_33_3_23_24.py PATH/TO/eaqecc_33_3_23_24.json
"""
import sys, json, itertools

# ---------------- GF(9) by hand ----------------
def add(u, v): return ((u % 3 + v % 3) % 3) + 3 * ((u // 3 + v // 3) % 3)
def neg(u): return ((-(u % 3)) % 3) + 3 * ((-(u // 3)) % 3)
def mul(u, v):
    a, b = u % 3, u // 3
    c, d = v % 3, v // 3
    return ((a * c - b * d) % 3) + 3 * ((a * d + b * c) % 3)
ADD = [[add(u, v) for v in range(9)] for u in range(9)]
MUL = [[mul(u, v) for v in range(9)] for u in range(9)]
NEG = [neg(u) for u in range(9)]
INV = [0] + [next(v for v in range(1, 9) if MUL[u][v] == 1) for u in range(1, 9)]
CONJ = [(u % 3) + 3 * ((-(u // 3)) % 3) for u in range(9)]  # Frobenius x -> x^3

# ---------------- recovered data ----------------
POINTS = [[1, 0, 0], [1, 0, 3], [1, 2, 4], [1, 2, 3], [1, 3, 4], [1, 0, 6], [1, 4, 4], [1, 8, 0], [1, 8, 7],
          [1, 3, 5], [1, 8, 6], [1, 1, 4], [1, 4, 0], [1, 6, 8], [1, 1, 8], [0, 1, 7], [1, 0, 5], [1, 1, 5],
          [1, 2, 6], [1, 8, 4], [1, 3, 0], [0, 1, 4], [1, 6, 3], [1, 4, 8], [1, 0, 7], [1, 1, 3], [1, 6, 7],
          [0, 1, 6], [0, 1, 5], [1, 4, 3], [1, 3, 6], [1, 8, 8], [1, 1, 6]]
MU = [1, 3, 2, 3, 7, 6, 7, 1, 7, 4, 4, 7, 5, 3, 3, 8, 4, 6, 4, 7, 5, 6, 8, 3, 7, 8, 2, 7, 3, 3, 4, 8, 6]
N = 33

# ---------------- linear algebra helpers ----------------
def rref(M, F):
    """Row reduce over GF(3) (F=3) or GF(9) (F=9)."""
    M = [r[:] for r in M]
    piv = []
    r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        if F == 3:
            iv = pow(M[r][c], -1, 3); M[r] = [x * iv % 3 for x in M[r]]
        else:
            iv = INV[M[r][c]]; M[r] = [MUL[iv][x] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                if F == 3:
                    f = M[i][c]; M[i] = [(a - f * b) % 3 for a, b in zip(M[i], M[r])]
                else:
                    f = NEG[M[i][c]]; M[i] = [ADD[a][MUL[f][b]] for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M):
            break
    return M[:r], piv

def nullspace3(M):
    R, piv = rref(M, 3)
    m = len(M[0]); out = []
    for f in (c for c in range(m) if c not in piv):
        v = [0] * m; v[f] = 1
        for i, p in enumerate(piv):
            v[p] = (-R[i][f]) % 3
        out.append(v)
    return out

def same_rowspace3(A, B):
    ra = len(rref(A, 3)[0]); rb = len(rref(B, 3)[0]); rab = len(rref(A + B, 3)[0])
    return ra == rb == rab, ra, rb, rab

def herm_gram(G):
    out = []
    for a in G:
        row = []
        for b in G:
            s = 0
            for j in range(N):
                s = ADD[s][MUL[a[j]][CONJ[b[j]]]]
            row.append(s)
        out.append(row)
    return out

def hull_words(G):
    """All words of the Hermitian hull D & D^perp_H (as tuples)."""
    k = len(G)
    gram = herm_gram(G)                      # gram[a][b] = <g_a, g_b> = sum g_a[j]*conj(g_b[j])
    # x in F9^k with sum_a x_a g_a in hull  <=>  sum_a x_a gram[a][b] = 0 for all b
    cols = [[gram[a][b] for a in range(k)] for b in range(k)]   # equations in x
    R, piv = rref(cols, 9)
    free = [c for c in range(k) if c not in piv]
    basis = []
    for f in free:
        x = [0] * k; x[f] = 1
        for i, p in enumerate(piv):
            x[p] = NEG[R[i][f]]
        basis.append(x)
    words = set()
    for coef in itertools.product(range(9), repeat=len(basis)):
        w = [0] * N
        for c, x in zip(coef, basis):
            for a in range(k):
                t = MUL[c][x[a]]
                if t:
                    w = [ADD[u][MUL[t][g]] for u, g in zip(w, G[a])]
        words.add(tuple(w))
    return words, len(basis)

def weight_distribution(G, skip=frozenset()):
    k = len(G)
    mult = [[[MUL[c][g] for g in row] for c in range(9)] for row in G]
    dist = {}
    def rec(i, vec):
        if i == k:
            w = sum(1 for x in vec if x)
            if w and tuple(vec) not in skip:
                dist[w] = dist.get(w, 0) + 1
            return
        for c in range(9):
            rec(i + 1, [ADD[a][b] for a, b in zip(vec, mult[i][c])] if c else vec)
    rec(0, [0] * N)
    return dist

def main():
    obj = json.load(open(sys.argv[1]))
    S_ship = obj["S"]

    # 1. conic evaluation matrix E, scaled by MU^-1
    mons = list(itertools.combinations_with_replacement(range(3), 2))  # x0^2,x0x1,x0x2,x1^2,x1x2,x2^2
    E = [[MUL[p[a]][p[b]] for p in POINTS] for (a, b) in mons]
    G = [[MUL[E[i][j]][INV[MU[j]]] for j in range(N)] for i in range(6)]
    assert len(rref(G, 9)[0]) == 6
    print("classical code D = rowspace(E*diag(MU)^-1): [33,6]_9, rank", len(rref(G, 9)[0]))

    # 2. exact minimum distance of D (9^6 - 1 nonzero words) and Hermitian hull
    dist_all = weight_distribution(G)
    print("min weight of D (all nonzero words):", min(dist_all))
    print("weight distribution of D:", sorted(dist_all.items()))
    hull = 6 - len(rref(herm_gram(G), 9)[0])
    hw, hd = hull_words(G)
    print("Hermitian hull dimension of D:", hull, "(", len(hw), "words =", "9^%d" % hd, ")")
    dist = weight_distribution(G, frozenset(hw))
    print("min weight of D outside its hull (= quantum distance d):", min(dist))

    # 3. GF(9) -> GF(3): W = GF(3)-span of rows c and i*c, as (x | z) with c = x + i*z
    I = 3  # element i
    Wrows = []
    for row in G:
        for r in (row, [MUL[I][x] for x in row]):
            Wrows.append([x % 3 for x in r] + [x // 3 for x in r])
    W, _ = rref(Wrows, 3)
    print("W = GF(3) image of D: dimension", len(W), "(expect 12)")

    # 4. S = symplectic dual of W: all (x|z) with  x.z' - z.x' = 0 for every (x'|z') in W
    cond = [[(-x) % 3 for x in w[N:]] + w[:N] for w in W]   # row (-z' | x')
    S = nullspace3(cond)
    print("S = symplectic dual of W: rows", len(S), "(expect 54 = 2n - 12)")

    # 5. compare with shipped object
    ok, ra, rb, rab = same_rowspace3(S, S_ship)
    print("rank(S_rebuilt) =", ra, " rank(S_shipped) =", rb, " rank(stacked) =", rab)
    print("REBUILT ROW SPACE EQUALS SHIPPED ROW SPACE:", ok)

    # 6. parameters from the definition
    s = ra
    Jm = lambda r: [(-x) % 3 for x in r[N:]] + r[:N]
    Gm = [[sum(a * b for a, b in zip(r1, Jm(r2))) % 3 for r2 in S] for r1 in S]
    c = len(rref(Gm, 3)[0]) // 2
    k = N - s + c
    print("s = %d, c = %d, k = %d, d (min weight of D outside hull) = %d" % (s, c, k, min(dist)))
    print("RESULT [[%d,%d,%d;%d]]_3" % (N, k, min(dist), c), "MATCHES SHIPPED OBJECT" if ok else "DOES NOT MATCH")

if __name__ == "__main__":
    main()
