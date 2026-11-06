"""MacWilliams transform over GF(q): A_i = (1/|C^perp|) sum_j B_j K_i(j), K_i(j) = sum_s (-1)^s (q-1)^(i-s) C(j,s) C(n-j,i-s).
Exact integers. Usage: macwilliams.py DUALENUM_OUTPUT q"""
import sys
from math import comb
lines = open(sys.argv[1]).read().split("\n"); q = int(sys.argv[2])
hdr = [l for l in lines if l.startswith("k=")][0]; n = int(hdr.split("n=")[1].split()[0])
B = {int(l.split()[1]): int(l.split()[2]) for l in lines if l.startswith("B_w")}
tot = sum(B.values())
A = []
for i in range(n + 1):
    s = sum(Bj * sum((-1) ** s_ * (q - 1) ** (i - s_) * comb(j, s_) * comb(n - j, i - s_) for s_ in range(i + 1)) for j, Bj in B.items())
    assert s % tot == 0, (i, s, tot)
    A.append(s // tot)
assert all(a >= 0 for a in A)
k = hdr.split("k=")[1].split()[0]
print(hdr); print("sum A =", sum(A), "= 9^k" if sum(A) == q ** int(k) else "MISMATCH")
d = next(i for i in range(1, n + 1) if A[i])
print("A_1..A_%d = 0; A_%d = %d; minimum distance d = %d" % (d - 1, d, A[d], d))
print("A =", A)
