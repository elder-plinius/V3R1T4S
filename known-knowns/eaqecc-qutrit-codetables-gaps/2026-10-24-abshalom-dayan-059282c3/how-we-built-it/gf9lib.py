"""GF(9) helpers for building claim files (search side). Encoding a + 3b = a + b*w, w^2 = w + 1."""
ADD = [[0]*9 for _ in range(9)]; MUL = [[0]*9 for _ in range(9)]
for x in range(9):
    for y in range(9):
        a, b, c, d = x % 3, x // 3, y % 3, y // 3
        ADD[x][y] = (a+c) % 3 + 3*((b+d) % 3)
        MUL[x][y] = (a*c + b*d) % 3 + 3*((a*d + b*c + b*d) % 3)
NEG = [next(y for y in range(9) if ADD[x][y] == 0) for x in range(9)]
INV = [None] + [next(y for y in range(9) if MUL[x][y] == 1) for x in range(1, 9)]
CONJ = [MUL[MUL[x][x]][x] for x in range(9)]
def sub(x, y): return ADD[x][NEG[y]]
def rref9(M):
    M = [r[:] for r in M]; piv = []; r = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = INV[M[r][c]]; M[r] = [MUL[iv][v] for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [sub(a, MUL[f][b]) for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    return M[:r], piv
def nullspace9(M, ncol):
    R, piv = rref9(M)
    basis = []
    for f in [c for c in range(ncol) if c not in piv]:
        v = [0]*ncol; v[f] = 1
        for i, pc in enumerate(piv): v[pc] = NEG[R[i][f]]
        basis.append(v)
    return basis
def herm_dual(G, n):
    """C^perp_H = {v : sum_t g_t conj(v_t) = 0} = nullspace of conj(G)."""
    return nullspace9([[CONJ[x] for x in r] for r in G], n)
def phi_rows(D):
    """GF(3) symplectic rows (x|z) of the GF(3)-span of D: rows r and w*r."""
    out = []
    for r in D:
        for s in (1, 3):
            v = [MUL[s][x] for x in r]
            out.append([x % 3 for x in v] + [x // 3 for x in v])
    return out
def gram_rank(G):
    H = [[0]*len(G) for _ in G]
    for i, gi in enumerate(G):
        for j, gj in enumerate(G):
            s = 0
            for a, b in zip(gi, gj): s = ADD[s][MUL[a][CONJ[b]]]
            H[i][j] = s
    return len(rref9(H)[0])
def scale_cols(G, cols, lam):
    return [[MUL[lam][x] if t in cols else x for t, x in enumerate(r)] for r in G]
