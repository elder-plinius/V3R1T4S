"""Known positive and negative inputs for check_schutte.py."""
import json, os
os.makedirs("tests", exist_ok=True)
def paley(p):
    QR = {(x * x) % p for x in range(1, p)}
    return [[1 if (j - i) % p in QR else 0 for j in range(p)] for i in range(p)]
def cyc3(): return paley(3)
def compose(G1, G2):
    """Proposition 2.3: G1, G2 lists of tournaments on V1 = 0..n1-1, V2 = n1..n1+n2-1.
    Tournaments of G1 keep their edges on V1 and send V1 -> V2; those of G2 keep theirs on V2 and send V2 -> V1.
    The free (dashed) edges inside the other block are set to i -> j for i < j."""
    n1, n2 = len(G1[0]), len(G2[0]); n = n1 + n2
    out = []
    for A in G1:
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j: continue
                if i < n1 and j < n1: B[i][j] = A[i][j]
                elif i < n1 <= j: B[i][j] = 1
                elif j < n1 <= i: B[i][j] = 0
                else: B[i][j] = 1 if i < j else 0
        out.append(B)
    for A in G2:
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j: continue
                if i >= n1 and j >= n1: B[i][j] = A[i - n1][j - n1]
                elif j < n1 <= i: B[i][j] = 1
                elif i < n1 <= j: B[i][j] = 0
                else: B[i][j] = 1 if i < j else 0
        out.append(B)
    return out
def dump(name, m, k, T):
    json.dump({"m": m, "k": k, "n": len(T[0]), "tournaments": [["".join(map(str, r)) for r in A] for A in T]}, open(f"tests/{name}.json", "w"))
P7, P19 = paley(7), paley(19)
dump("pos_qr7_m1k2", 1, 2, [P7])
dump("pos_qr19_m1k3", 1, 3, [P19])
dump("pos_comp_7_7_m2k5", 2, 5, compose([P7], [P7]))            # f(2,5) <= 14
G23 = compose([cyc3()], [cyc3()])                                 # f(2,3) <= 6 (S_3, 2 tournaments)
dump("pos_comp_3_3_m2k3", 2, 3, G23)
dump("pos_comp_7_6_m3k6", 3, 6, compose([P7], G23))               # f(3,6) <= 13
dump("pos_comp_7_3_m2k4", 2, 4, compose([P7], [cyc3()]))         # f(2,4) <= 10
# negatives
P6 = [r[:6] for r in P7[:6]]
dump("neg_qr7_minus_vertex_m1k2", 1, 2, [P6])                    # f(1,2) = 7, so FAIL
C = compose([P7], [P7]); C13 = [[r[:13] for r in A[:13]] for A in C]
dump("neg_comp14_minus_vertex_m2k5", 2, 5, C13)
bad = [r[:] for r in P7]; bad[0][1] = bad[1][0] = 1
dump("neg_not_tournament", 1, 2, [bad])
bad2 = [r[:] for r in P7]; bad2[2][2] = 1
dump("neg_diag", 1, 2, [bad2])
# pitfall: each u in U beaten by v in SOME tournament (T and its reverse) but no single tournament dominates U
import random; random.seed(1)
n = 6; R = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(i + 1, n):
        if random.random() < 0.5: R[i][j] = 1
        else: R[j][i] = 1
Rrev = [[R[j][i] for j in range(n)] for i in range(n)]
dump("neg_reverse_pair_m2k3", 2, 3, [R, Rrev])
dump("neg_wrong_count", 3, 5, compose([P7], [cyc3()]))           # declares m=3 but has 2 matrices
print(sorted(os.listdir("tests")))
