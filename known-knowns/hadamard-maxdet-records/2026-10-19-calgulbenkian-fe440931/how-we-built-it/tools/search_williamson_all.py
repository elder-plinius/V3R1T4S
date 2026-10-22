#!/usr/bin/env python3
"""
Find Williamson quadruples for m in {13, 21, 23, 25, 27} and test both
standard Hadamard bordering (fast_maxdet_search) and Orrick-Solomon 3-normalized
bordering (os_3norm_search) on n in {85, 93, 101, 105, 109}.
"""
import itertools
import json
import os
import subprocess
from run_williamson_and_audit import build_williamson_hadamard, save_matrix


def find_williamson_quads(m, k_tuple, max_quads=6):
    half = (m - 1) // 2

    def get_paf_map(k):
        res = {}
        for comb in itertools.combinations(range(1, half + 1), k):
            seq = [1] * m
            for idx in comb:
                seq[idx] = -1
                seq[m - idx] = -1
            paf = tuple(sum(seq[i] * seq[(i + s) % m] for i in range(m)) for s in range(1, half + 1))
            if paf not in res:
                res[paf] = seq
        return res

    maps = [get_paf_map(k) for k in k_tuple]
    sum_AB = {}
    for pA, sA in maps[0].items():
        for pB, sB in maps[1].items():
            psum = tuple(pA[i] + pB[i] for i in range(half))
            if psum not in sum_AB:
                sum_AB[psum] = (sA, sB)

    quads = []
    for pC, sC in maps[2].items():
        for pD, sD in maps[3].items():
            need = tuple(-(pC[i] + pD[i]) for i in range(half))
            if need in sum_AB:
                sA, sB = sum_AB[need]
                quads.append((sA, sB, sC, sD))
                if len(quads) >= max_quads:
                    return quads
    return quads


def kron_H2(H):
    m = len(H)
    out = [[0] * (2 * m) for _ in range(2 * m)]
    for i in range(m):
        for j in range(m):
            v = H[i][j]
            out[i][j] = v
            out[i][m + j] = v
            out[m + i][j] = v
            out[m + i][m + j] = -v
    return out


def main():
    with open("data/maxdet_table.json") as f:
        table = json.load(f)

    # Specs: (n, m_will, k_tuple_list)
    # Note row sum of symmetric sequence of length m with k pairs of -1s is m - 4*k.
    specs = [
        # m=13: 52 = 5^2 + 3^2 + 3^2 + 3^2 -> row sums (5, -3, -3, -3) -> k = (2, 4, 4, 4)
        (105, 13, [(2, 4, 4, 4), (3, 3, 3, 2)]),
        # m=21: 84 = 7^2 + 5^2 + 3^2 + 1^2 -> row sums (-7, 5, -3, 1) -> k = (7, 4, 6, 5)
        (85, 21, [(7, 4, 6, 5), (3, 5, 5, 5)]),
        # m=23: 92 = 9^2 + 3^2 + 1^2 + 1^2 -> row sums (7, -5, 3, 3)? Wait: 49+25+9+9=92!
        # For m=23: m - 4k: k=4 -> 7, k=7 -> -5, k=5 -> 3, k=5 -> 3! (49+25+9+9=92)
        (93, 23, [(4, 7, 5, 5), (8, 5, 6, 6)]),
        # m=25: 100 = 7^2 + 5^2 + 5^2 + 1^2 -> m - 4k: k=8 -> -7, k=5 -> 5, k=5 -> 5, k=6 -> 1
        (101, 25, [(8, 5, 5, 6), (4, 7, 7, 6)]),
        # m=27: 108 = 7^2 + 5^2 + 5^2 + 3^2 -> m - 4k: k=5 -> 7, k=8 -> -5, k=8 -> -5, k=6 -> 3
        (109, 27, [(5, 8, 8, 6), (9, 6, 6, 6)]),
    ]

    for n, mw, k_tuples in specs:
        k_ord = (n - 1) // 4
        rec_D = int(table[str(n)]["exact_norm_det"])
        rec_fac = rec_D / (k_ord ** (2 * k_ord - 1))
        print(f"=== Testing n={n} (Williamson m={mw}, standing rec_fac={rec_fac:.3f}) ===", flush=True)
        for kt in k_tuples:
            quads = find_williamson_quads(mw, kt, max_quads=4)
            print(f"  k_tuple={kt}: found {len(quads)} quads", flush=True)
            for idx, q in enumerate(quads):
                Hw = build_williamson_hadamard(mw, q)
                if n == 105:
                    H = kron_H2(Hw)
                else:
                    H = Hw
                h_path = f"results/tmp_H_{n}_{kt[0]}_{idx}.txt"
                save_matrix(h_path, H)
                r1 = subprocess.run(
                    ["./tools/fast_maxdet_search", str(n), "1600", "60", h_path, f"results/cand_{n}_std_w{idx}.txt", "8"],
                    capture_output=True, text=True, check=True
                )
                r2 = subprocess.run(
                    ["./tools/os_3norm_search", str(n), h_path, f"results/cand_{n}_os_w{idx}.txt", "8"],
                    capture_output=True, text=True, check=True
                )
                print(f"    #{idx} std: {r1.stdout.strip()}", flush=True)
                print(f"    #{idx} os3: {r2.stdout.strip()}", flush=True)
                os.remove(h_path)


if __name__ == "__main__":
    main()
