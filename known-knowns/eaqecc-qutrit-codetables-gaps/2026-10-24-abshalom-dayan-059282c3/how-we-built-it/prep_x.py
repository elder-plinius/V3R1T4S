#!/usr/bin/env python3
"""Prepare a Construction X input: C2 subset of C1 (two "K n" code files), output "K1 K2 n" then K1 rows of n with the
first K2 rows a basis of C2 and the last K1 - K2 rows completing a basis of C1 (checks C2 is a subcode of C1).
Usage: prep_x.py C1.code C2.code out.xin"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf9lib import rref9
def rd(f):
    L = open(f).read().split("\n"); K, n = map(int, L[0].split())
    return [list(map(int, l.split())) for l in L[1:1 + K]], K, n
G1, K1, n = rd(sys.argv[1]); G2, K2, n2 = rd(sys.argv[2]); assert n == n2
assert len(rref9(G1 + G2)[0]) == K1, "C2 not inside C1"
B = [r[:] for r in G2]
for r in G1:
    if len(rref9(B + [r])[0]) > len(B):
        B.append(r)
assert len(B) == K1
open(sys.argv[3], "w").write("%d %d %d\n" % (K1, K2, n) + "".join(" ".join(map(str, r)) + "\n" for r in B))
print("C1 [%d,%d] contains C2 [%d,%d]: ok" % (n, K1, n, K2))
