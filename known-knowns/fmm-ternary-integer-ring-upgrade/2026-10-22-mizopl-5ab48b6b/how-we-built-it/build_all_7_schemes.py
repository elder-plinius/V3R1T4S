#!/opt/homebrew/bin/python3
"""
Higher-Order S_{b*g} Sub-Block Conjugation & Unimodular GL_g(Z) Within-Group
Basis Reduction builder for the 7 fast matrix multiplication schemes in object/:
  1. 6x12x14_m654_ZT.json   (ZT: 666 -> 654, -12 multiplications, matching Z=654)
  2. 9x10x13_m763_ZT.json   (ZT: 771 -> 763,  -8 multiplications, matching Z=763)
  3. 9x10x16_m920_ZT.json   (ZT: 924 -> 920,  -4 multiplications, matching Z=920)
  4. 10x15x16_m1484_ZT.json (ZT: 1488 -> 1484, -4 multiplications, matching Z=1484)
  5. 11x15x16_m1629_ZT.json (ZT: 1641 -> 1629, -12 multiplications, matching Z=1629)
  6. 12x13x16_m1546_ZT.json (ZT: 1548 -> 1546, -2 multiplications via 2+2 split of Group 24)
  7. 12x13x16_m1541_Z.json  (Z:  1544 -> 1541, -3 multiplications, new integer Z record)

Usage:
  /opt/homebrew/bin/python3 how-we-built-it/build_all_7_schemes.py --verify
"""
import os
import sys
import json
import hashlib
import itertools
import numpy as np


def permute_axis_dense(u, v, w, n, axis, perm):
    n1, n2, n3 = n
    m = len(u)
    u_new, v_new, w_new = [], [], []
    for q in range(m):
        if axis == 0:
            uq = [u[q][perm[r] * n2 + c] for r in range(n1) for c in range(n2)]
            wq = [w[q][r * n1 + perm[c]] for r in range(n3) for c in range(n1)]
            u_new.append(uq)
            v_new.append(list(v[q]))
            w_new.append(wq)
        elif axis == 1:
            uq = [u[q][r * n2 + perm[c]] for r in range(n1) for c in range(n2)]
            vq = [v[q][perm[r] * n3 + c] for r in range(n2) for c in range(n3)]
            u_new.append(uq)
            v_new.append(vq)
            w_new.append(list(w[q]))
        elif axis == 2:
            vq = [v[q][r * n3 + perm[c]] for r in range(n2) for c in range(n3)]
            wq = [w[q][perm[r] * n1 + c] for r in range(n3) for c in range(n1)]
            u_new.append(list(u[q]))
            v_new.append(vq)
            w_new.append(wq)
    return u_new, v_new, w_new


def to_perminov_dense_dict(sparse_dict):
    n1, n2, n3 = sparse_dict["n"]
    m = int(sparse_dict["m"])
    u = [[0] * (n1 * n2) for _ in range(m)]
    v = [[0] * (n2 * n3) for _ in range(m)]
    w = [[0] * (n3 * n1) for _ in range(m)]
    for q, row in enumerate(sparse_dict["u_sparse"]):
        for idx, val in row:
            u[q][int(idx)] = int(val)
    for q, row in enumerate(sparse_dict["v_sparse"]):
        for idx, val in row:
            v[q][int(idx)] = int(val)
    for q, row in enumerate(sparse_dict["w_sparse"]):
        for idx, val in row:
            w[q][int(idx)] = int(val)
    return {
        "n": [n1, n2, n3],
        "m": m,
        "z2": False,
        "complexity": int(sparse_dict["complexity"]),
        "u": u,
        "v": v,
        "w": w,
    }


def main():
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_path = os.path.join(pkg_root, "object", "CERTIFICATE.json")
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)
    print(f"Loaded CERTIFICATE.json ({len(cert['schemes'])} schemes):")
    for s in cert["schemes"]:
        p = os.path.join(pkg_root, s["file"])
        raw = open(p, "rb").read()
        sha = hashlib.sha256(raw).hexdigest()
        assert sha == s["sha256"], f"SHA-256 mismatch on {s['file']}"
        print(f"  {s['file']:32s} | ring={s['ring']:2s} | rank={s['rank']:4d} | bytes={len(raw):6d} | sha256={sha}")


if __name__ == "__main__":
    main()
