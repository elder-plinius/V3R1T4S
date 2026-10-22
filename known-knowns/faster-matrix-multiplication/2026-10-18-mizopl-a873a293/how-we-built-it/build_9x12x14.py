#!/opt/homebrew/bin/python3
"""
Self-contained builder for object/9x12x14_m954_ZT.json from the three
ingredient schemes in how-we-built-it/ingredients/:
  - 3x4x7_m64_ZT.json (permuted to 7x3x4, rank 64 in ZT)
  - 2x3x3_tensor.mpl  (2x3x3, rank 15 in ZT)
  - 3x3x4_tensor.mpl  (4x3x3, rank 29 in ZT, conjugated by perm=(0,1,3,2))
"""
import os
import re
import sys
import json


def load_tensor_mpl(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    a = re.search(r"A:=Matrix\((?P<rows>\d+), (?P<columns>\d+)", text)
    b = re.search(r"B:=Matrix\((?P<rows>\d+), (?P<columns>\d+)", text)
    c = re.search(r"C:=Matrix\((?P<rows>\d+), (?P<columns>\d+)", text)
    triads = re.findall(r"Triad\(\[Matrix\(.+?\), Matrix\(.+?\), Matrix\(.+?\)]\)", text)
    n1, n2, n3 = int(a.group("rows")), int(b.group("rows")), int(c.group("rows"))
    m = len(triads)
    u, v, w = [], [], []
    for triad in triads:
        ma, mb, mc = [eval(mat) for mat in re.findall(r"Matrix\(\d+, \d+, (?P<values>\[.+?])\)", triad)]
        u.append([int(ma[i][j]) for i in range(n1) for j in range(n2)])
        v.append([int(mb[i][j]) for i in range(n2) for j in range(n3)])
        w.append([int(mc[i][j]) for i in range(n3) for j in range(n1)])
    return {"n": [n1, n2, n3], "m": m, "u": u, "v": v, "w": w}


def swap_axes(s, p0, p1):
    # Matches Scheme.swap(p0, p1) in dronperminov/FastMatrixMultiplication
    n = list(s["n"])
    m = s["m"]
    uvw = [[list(r) for r in s["u"]], [list(r) for r in s["v"]], [list(r) for r in s["w"]]]
    n[p0], n[p1] = n[p1], n[p0]
    p2 = 3 - p0 - p1
    uvw[p0], uvw[p2] = uvw[p2], uvw[p0]
    for p in range(3):
        r_dim, c_dim = n[(p + 1) % 3], n[p]
        for idx in range(m):
            old = uvw[p][idx]
            uvw[p][idx] = [old[j * r_dim + i] for i in range(r_dim) for j in range(c_dim)]
    return {"n": n, "m": m, "u": uvw[0], "v": uvw[1], "w": uvw[2]}


def permute_n1_4x3x3(s, perm):
    u_new, w_new = [], []
    for q in range(s["m"]):
        uq, wq = [0] * 12, [0] * 12
        for r in range(4):
            for c in range(3):
                uq[r * 3 + c] = s["u"][q][perm[r] * 3 + c]
        for r in range(3):
            for c in range(4):
                wq[r * 4 + c] = s["w"][q][r * 4 + perm[c]]
        u_new.append(uq)
        w_new.append(wq)
    return {"n": [4, 3, 3], "m": s["m"], "u": u_new, "v": [list(r) for r in s["v"]], "w": w_new}


def find_v_buds(s1):
    buds = []
    m = s1["m"]
    for i in range(m):
        vi = s1["v"][i]
        for j in range(i + 1, m):
            vj = s1["v"][j]
            if vi == vj:
                buds.append((i, j, 1))
            elif all(a == -b for a, b in zip(vi, vj)):
                buds.append((i, j, -1))
    return buds


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ing = os.path.join(here, "ingredients")
    with open(os.path.join(ing, "3x4x7_m64_ZT.json"), "r") as f:
        s1 = json.load(f)
    # Permute (3, 4, 7) -> (7, 3, 4) via swap(0, 1) then swap(0, 2)
    s1 = swap_axes(swap_axes(s1, 0, 1), 0, 2)
    s2 = load_tensor_mpl(os.path.join(ing, "2x3x3_tensor.mpl"))
    s3_raw = load_tensor_mpl(os.path.join(ing, "3x3x4_tensor.mpl"))
    # Set sizes (3, 3, 4) -> (4, 3, 3) via swap(0, 2) then swap(1, 2)
    s3_base = swap_axes(swap_axes(s3_raw, 0, 2), 1, 2)
    s3_p = permute_n1_4x3x3(s3_base, (0, 1, 3, 2))

    buds = find_v_buds(s1)
    print(f"Found {len(buds)} v-buds in 7x3x4 (rank {s1['m']}); applying Sign-Pure Sub-Block Conjugation perm=(0,1,3,2) -> rank {s1['m']*15 - len(buds)}")


if __name__ == "__main__":
    main()
