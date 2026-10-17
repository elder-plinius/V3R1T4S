#!/usr/bin/env python3
"""Rebuild object/qutrit_14_3_8_5.json from the 2-quasi-cyclic Hermitian self-orthogonal [14, 6, 8]_9 seed.
Standard-library Python 3 only. Run from the package root:
  python3 how-we-built-it/build_14_3_8_5.py
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "verify-it-yourself"))
from check_eaqecc import GF9_MUL, nullspace_gf3, verify_package_object

H9_self_orth = [
    [5, 8, 1, 8, 4, 7, 3, 7, 6, 3, 8, 8, 8, 5],
    [3, 5, 8, 1, 8, 4, 7, 5, 7, 6, 3, 8, 8, 8],
    [7, 3, 5, 8, 1, 8, 4, 8, 5, 7, 6, 3, 8, 8],
    [4, 7, 3, 5, 8, 1, 8, 8, 8, 5, 7, 6, 3, 8],
    [8, 4, 7, 3, 5, 8, 1, 8, 8, 8, 5, 7, 6, 3],
    [1, 8, 4, 7, 3, 5, 8, 3, 8, 8, 8, 5, 7, 6],
]

mask = 7
H9_scaled = [
    [GF9_MUL[row[c]][4] if ((mask >> c) & 1) else row[c] for c in range(14)]
    for row in H9_self_orth
]

n = 14
H3 = []
for row in H9_scaled:
    H3.append([val % 3 for val in row] + [val // 3 for val in row])
    H3.append([(2 * (val // 3)) % 3 for val in row] + [val % 3 for val in row])

H3J = [[(2 * r[n + j]) % 3 for j in range(n)] + [r[j] % 3 for j in range(n)] for r in H3]
S = nullspace_gf3(H3J, 2 * n)

obj = {
    "target_id": "eaqecc-qutrit-codetables-gaps",
    "parameters": "[[14, 3, 8; 5]]_3",
    "n": 14,
    "k": 3,
    "d": 8,
    "c": 5,
    "s": 16,
    "d_lower": 7,
    "d_upper": 10,
    "pure": True,
    "field_representation": "S is a 16 x 28 symplectic stabilizer generator matrix over GF(3) = {0, 1, 2} with symplectic form J = [[0, I_14], [2*I_14, 0]] (mod 3). H9 is the corresponding 6 x 14 dual generator matrix over GF(9) = GF(3)[w]/(w^2+1), with elements encoded as a + 3*b in 0..8.",
    "S": S,
    "H9": H9_scaled,
    "H9_self_orthogonal_seed": H9_self_orth,
    "diagonal_scaling_columns": [0, 1, 2],
    "diagonal_scaling_factor_gf9": 4,
}

ok, msg = verify_package_object(obj)
assert ok, msg

pkg_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
obj_path = os.path.join(pkg_root, "object", "qutrit_14_3_8_5.json")
with open(obj_path, "w", encoding="utf-8") as f:
    json.dump(obj, f, indent=2)
    f.write("\n")

with open(obj_path, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()

print(f"Rebuilt object/qutrit_14_3_8_5.json (sha256: {sha})")
print(msg)
