#!/usr/bin/env python3
"""
Search Williamson quadruples for m=29 (n=117) and m=27 (n=109), Kronecker cores for m=104 (n=105),
and audit smaller n == 1 (mod 4) orders with tools/fast_maxdet_search.
"""
import itertools
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_hadamard_maxdet as vm


def find_williamson_m29_quadruples(max_quads=25):
    def get_paf_map(k):
        res = {}
        for comb in itertools.combinations(range(1, 15), k):
            seq = [1] * 29
            for idx in comb:
                seq[idx] = -1
                seq[29 - idx] = -1
            paf = tuple(sum(seq[i] * seq[(i + s) % 29] for i in range(29)) for s in range(1, 15))
            if paf not in res:
                res[paf] = seq
        return res

    t5 = get_paf_map(5)   # sum = 9
    t6 = get_paf_map(6)   # sum = 5
    t8 = get_paf_map(8)   # sum = -3
    t7 = get_paf_map(7)   # sum = 1

    sum_AB = {}
    for p5, s5 in t5.items():
        for p6, s6 in t6.items():
            psum = tuple(p5[i] + p6[i] for i in range(14))
            if psum not in sum_AB:
                sum_AB[psum] = (s5, s6)

    quads = []
    for p8, s8 in t8.items():
        for p7, s7 in t7.items():
            need = tuple(-(p8[i] + p7[i]) for i in range(14))
            if need in sum_AB:
                s5, s6 = sum_AB[need]
                quads.append((s5, s6, s8, s7))
                if len(quads) >= max_quads:
                    return quads
    return quads


def build_williamson_hadamard(m, quad):
    def circ(seq):
        return [[seq[(j - i) % m] for j in range(m)] for i in range(m)]

    A, B, C, D = [circ(s) for s in quad]
    H = [[0] * (4 * m) for _ in range(4 * m)]
    blocks = [
        [(1, A), (1, B), (1, C), (1, D)],
        [(-1, B), (1, A), (-1, D), (1, C)],
        [(-1, C), (1, D), (1, A), (-1, B)],
        [(-1, D), (-1, C), (1, B), (1, A)],
    ]
    for bi in range(4):
        for bj in range(4):
            sgn, blk = blocks[bi][bj]
            for i in range(m):
                for j in range(m):
                    H[bi * m + i][bj * m + j] = sgn * blk[i][j]
    return H


def save_matrix(path, mat):
    with open(path, "w", encoding="utf-8") as f:
        for row in mat:
            f.write(" ".join(str(x) for x in row) + "\n")


def main():
    os.makedirs("results", exist_ok=True)
    with open("data/maxdet_table.json") as f:
        table = json.load(f)

    # 1. Test 25 Williamson quadruples on n=117 (m=116)
    print("=== [1] Testing 25 Williamson m=29 quadruples for n=117 ===")
    quads = find_williamson_m29_quadruples(max_quads=25)
    best_117_fac = 0
    best_117_path = "results/cand_117_best.txt"
    for idx, q in enumerate(quads):
        H116 = build_williamson_hadamard(29, q)
        h_path = f"results/tmp_H116_{idx}.txt"
        out_path = f"results/tmp_cand117_{idx}.txt"
        save_matrix(h_path, H116)
        res = subprocess.run(
            ["./tools/fast_maxdet_search", "117", "2000", "80", h_path, out_path, "8"],
            capture_output=True, text=True, check=True
        )
        line = res.stdout.strip()
        fac = int([t.split("=")[1] for t in line.split() if t.startswith("factor=")][0])
        print(f"  quad #{idx:2d}: {line}")
        if fac > best_117_fac:
            best_117_fac = fac
            with open(out_path) as src, open(best_117_path, "w") as dst:
                dst.write(src.read())
        os.remove(h_path)
        os.remove(out_path)

    # 2. Audit smaller unclosed n == 1 (mod 4) orders with Paley I and Paley II
    print("\n=== [2] Auditing unclosed n == 1 (mod 4) orders in 37..101 ===")
    for n in [37, 45, 49, 53, 57, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101]:
        m = n - 1
        k = m // 4
        rec_D = int(table[str(n)]["exact_norm_det"])
        rec_fac = rec_D / (k ** (2 * k - 1))
        for mode in ["paley1", "paley2"]:
            res = subprocess.run(
                ["./tools/fast_maxdet_search", str(n), "1600", "60", mode, "-", "8"],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                print(f"  {res.stdout.strip()} | rec_factor={rec_fac:.3f}")


if __name__ == "__main__":
    main()
