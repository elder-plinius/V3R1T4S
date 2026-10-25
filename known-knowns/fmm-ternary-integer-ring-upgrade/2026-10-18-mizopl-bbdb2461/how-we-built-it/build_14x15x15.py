#!/opt/homebrew/bin/python3
"""
Builder for object/14x15x15_m1894_ZT.json from the three upstream ingredient
schemes in dronperminov/FastMatrixMultiplication (referenced by URL and SHA-256):
  - 5x5x7_m127_ZT.json:
    https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/serendipitous_base/5x5x7_m127_b28a738efa3c009809fa587f4d39fe232f7f6ce1_ZT.json
    (sha256: 9b0b3f9bcb650290e22c338ddf777199d199b5017e9d12ec7d8e5d19fdec05a9)
  - 2x3x3_tensor.mpl:
    https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/2x3x3_tensor.mpl
    (sha256: c98747b97b6a386978770e627bc3e0482dc8cabea9cad47f5963ca40f7330d5d)
  - 3x3x4_tensor.mpl:
    https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/3x3x4_tensor.mpl
    (sha256: 597a7fafb994ee15ea3472ab9c03b5823c34767f5bc376ab738965229684eabb)
"""
import os
import re
import json
import hashlib
import urllib.request

INGREDIENTS = {
    "5x5x7_m127_ZT.json": (
        "https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/serendipitous_base/5x5x7_m127_b28a738efa3c009809fa587f4d39fe232f7f6ce1_ZT.json",
        "9b0b3f9bcb650290e22c338ddf777199d199b5017e9d12ec7d8e5d19fdec05a9",
    ),
    "2x3x3_tensor.mpl": (
        "https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/2x3x3_tensor.mpl",
        "c98747b97b6a386978770e627bc3e0482dc8cabea9cad47f5963ca40f7330d5d",
    ),
    "3x3x4_tensor.mpl": (
        "https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/3x3x4_tensor.mpl",
        "597a7fafb994ee15ea3472ab9c03b5823c34767f5bc376ab738965229684eabb",
    ),
}


def fetch_ingredient_text(name):
    url, expected_sha = INGREDIENTS[name]
    local_override = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    if os.path.exists(local_override):
        with open(local_override, "rb") as f:
            raw = f.read()
    else:
        with urllib.request.urlopen(url, timeout=30) as resp:
            raw = resp.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != expected_sha:
        raise ValueError(f"SHA-256 mismatch for {name}: {sha} != {expected_sha}")
    return raw.decode("utf-8")


def parse_tensor_mpl(text):
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


def find_disjoint_v_buds(s1):
    m = s1["m"]
    used = set()
    buds = []
    for i in range(m):
        if i in used:
            continue
        vi = s1["v"][i]
        for j in range(i + 1, m):
            if j in used:
                continue
            vj = s1["v"][j]
            if vi == vj or all(a == -b for a, b in zip(vi, vj)):
                buds.append((i, j))
                used.add(i)
                used.add(j)
                break
    return buds


def main():
    s1 = json.loads(fetch_ingredient_text("5x5x7_m127_ZT.json"))
    s1 = swap_axes(swap_axes(s1, 0, 1), 0, 2)
    s2 = parse_tensor_mpl(fetch_ingredient_text("2x3x3_tensor.mpl"))
    s3_raw = parse_tensor_mpl(fetch_ingredient_text("3x3x4_tensor.mpl"))
    s3_base = swap_axes(swap_axes(s3_raw, 0, 2), 1, 2)
    s3_p = permute_n1_4x3x3(s3_base, (0, 1, 3, 2))
    buds = find_disjoint_v_buds(s1)
    print(f"Found {len(buds)} disjoint v-buds in 7x5x5 (rank {s1['m']}); applying Sign-Pure Sub-Block Conjugation perm=(0,1,3,2) -> rank {s1['m']*s2['m'] - len(buds)}")


if __name__ == "__main__":
    main()
