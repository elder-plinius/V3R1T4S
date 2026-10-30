"""Standalone checker for a qutrit EAQECC [[n,k,d;c]]_3 given by its stabilizer matrix S over GF(3) (Python standard
library; the exhaustive distance enumeration is done by enum_min.c, a small C program, because 3^22 vectors are far
too many for pure Python).

Definition checked (bank entry eaqecc-qutrit-codetables-gaps): with s independent generators (rows of S, (x|z),
2n columns, symplectic form <(x|z),(x'|z')> = x.z' - z.x'), c = rank(S J S^T)/2 and k = n - s + c; d is the minimum
symplectic weight (number of positions i with (x_i, z_i) != (0, 0)) over vectors of span(S)^perp that are not in the
isotropic part span(S) ∩ span(S)^perp.

Also checks the object's GF(9) description: D9 is Hermitian-orthogonal to G9 and rowspace(S) = phi(D9), with
GF(9) = GF(3)[w]/(w^2 - w - 1), a + b*w stored as a + 3b, conj(x) = x^3, phi(a + b*w) = (a | b) (rows r and w*r).

Usage: check_eaqecc.py prepare object.json basis.txt   (prints s, c, k; writes the basis of span(S)^perp, isotropic
                                                        part first, for enum_min)
       check_eaqecc.py verdict object.json results.txt  (results.txt = the prepare JSON line, then one enum_min
                                                        line per part; compares with the claimed n, k, c, d)"""
import json, sys
P = 3

def rref(M):
    M = [list(r) for r in M]; piv = []; r = 0
    for col in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][col] % P), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 if M[r][col] % P == 1 else 2
        M[r] = [(v * inv) % P for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] % P:
                f = M[i][col]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        piv.append(col); r += 1
    return M[:r], piv

def rank(M):
    return len(rref(M)[0]) if M else 0

def nullspace(M, ncols):
    R, piv = rref(M)
    basis = []
    for f in (c for c in range(ncols) if c not in piv):
        v = [0] * ncols; v[f] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-R[i][f]) % P
        basis.append(v)
    return basis

def symp(u, v, n):
    return (sum(a * b for a, b in zip(u[:n], v[n:])) - sum(a * b for a, b in zip(u[n:], v[:n]))) % P

# GF(9) arithmetic on the integer encoding a + 3b
def g_add(x, y): return (x % 3 + y % 3) % 3 + 3 * ((x // 3 + y // 3) % 3)
def g_mul(x, y):
    a, b, c, d = x % 3, x // 3, y % 3, y // 3
    return (a * c + b * d) % 3 + 3 * ((a * d + b * c + b * d) % 3)
def g_conj(x): return g_mul(g_mul(x, x), x)

def load(path):
    o = json.load(open(path))
    S = [[int(v) % P for v in row] for row in o["S"]]
    return o, S

def prepare(path, out):
    o, S = load(path)
    n2 = len(S[0]); n = n2 // 2
    assert n2 == 2 * n and all(len(r) == n2 for r in S), "S must have 2n columns"
    s = rank(S)
    gram = [[symp(u, v, n) for v in S] for u in S]
    r2c = rank(gram)
    assert r2c % 2 == 0
    c = r2c // 2; k = n - s + c
    # span(S)^perp: v with <S_i, v> = 0 for all i, i.e. (z_i | -x_i) . v = 0
    perp = nullspace([[*r[n:], *[(-x) % P for x in r[:n]]] for r in S], n2)
    assert len(perp) == n2 - s
    # isotropic part I = span(S) ∩ span(S)^perp = {v in span(S) : <v, S_j> = 0 for all j}:
    # v = a S (a over the rows of a basis of span(S)), condition a (B J S^T) = 0
    B = rref(S)[0]
    A = [[symp(b, sj, n) for b in B] for sj in S]          # rows: constraints over the coefficient vector a
    coef = nullspace(A, len(B))
    I = [[sum(a * b[t] for a, b in zip(cv, B)) % P for t in range(n2)] for cv in coef]
    I = rref(I)[0] if I else []
    for v in I:
        assert all(symp(v, sj, n) == 0 for sj in S)
    basis = [list(v) for v in I]
    for v in perp:
        if rank(basis + [v]) > len(basis):
            basis.append(v)
    assert len(basis) == len(perp)
    with open(out, "w") as f:
        f.write("%d %d %d\n" % (n, len(I), len(basis)))
        for v in basis:
            f.write(" ".join(map(str, v)) + "\n")
    # GF(9) description: D9 ⊥_H G9 and rowspace(S) = phi(D9)
    G9, D9 = o.get("G9"), o.get("D9")
    herm_ok = phi_ok = None
    if G9 and D9:
        herm_ok = all(
            (lambda acc: acc == 0)(__import__("functools").reduce(g_add, (g_mul(a, g_conj(b)) for a, b in zip(g, d)), 0))
            for g in G9 for d in D9)
        PH = []
        for r in D9:
            for lam in (1, 3):
                v = [g_mul(lam, x) for x in r]
                PH.append([x % 3 for x in v] + [x // 3 for x in v])
        phi_ok = rank(PH) == s and rank(S + PH) == s
    print(json.dumps({"n": n, "s": s, "c": c, "k": k, "dim_perp": len(basis), "dim_isotropic": len(I),
                      "D9_herm_orthogonal_to_G9": herm_ok, "rowspace_S_equals_phi_D9": phi_ok}))

def verdict(path, enum_out):
    o, S = load(path)
    lines = [l for l in open(enum_out).read().split("\n") if l.strip()]
    prep = json.loads(lines[0])
    parts = [dict(kv.split("=") for kv in l.split()) for l in lines[1:]]
    d = min(int(e["d"]) for e in parts); total = sum(int(e["enumerated"]) for e in parts)
    words = sum(int(e["count"]) for e in parts if int(e["d"]) == d)
    ok = (total == 3 ** prep["dim_perp"] and prep["n"] == o["n"] and prep["k"] == o["k"] and prep["c"] == o["c"]
          and d == o["d"] and prep["c"] >= 1 and prep["D9_herm_orthogonal_to_G9"] is not False
          and prep["rowspace_S_equals_phi_D9"] is not False)
    print("computed n=%d k=%d c=%d d=%d (%d words of weight d; enumerated %d vectors, 3^%d = %d); claimed n=%s k=%s c=%s d=%s"
          % (prep["n"], prep["k"], prep["c"], d, words, total, prep["dim_perp"], 3 ** prep["dim_perp"], o["n"], o["k"], o["c"], o["d"]))
    print("D9 Hermitian-orthogonal to G9: %s; rowspace(S) = phi(D9): %s" % (prep["D9_herm_orthogonal_to_G9"], prep["rowspace_S_equals_phi_D9"]))
    return ok

if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare(sys.argv[2], sys.argv[3])
    else:
        sys.exit(0 if verdict(sys.argv[2], sys.argv[3]) else 1)
