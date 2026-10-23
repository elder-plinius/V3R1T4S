#!/usr/bin/env python3
"""
Lens 2 (representation-absorber):
Rank-Preserving Ternary Flip-Graph Walks + Warm-Started Native C CSE Optimization.

For candidate formats with max(n1, n2, n3) <= 8 where ZT rank == fmm_sota:
1. Enumerates valid rank-preserving ternary flip moves flip(i, j, mode, sigma)
   that keep all entries of (U, V, W) in {-1, 0, 1} and preserve exact bilinear
   matrix multiplication over Z.
2. Evaluates both single-step flips and multi-step flip chains (guided by naive
   addition count cn and pairwise overlap) using native C CSE + Lookahead +
   Sub-Row Re-Covering (cse_opt).
3. Also performs multi-seed deep LNS + CSE refinement on the best schemes found.
4. Verifies every improved SLP symbolically over Z with verify_slp.py and saves
   all verified records in attempts/representation-absorber/result/.
"""

import copy
import glob
import json
import os
import random
import re
import subprocess
import sys
import tempfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, ROOT_DIR)
import verify_slp

CSE_BIN = os.path.abspath(os.path.join(ROOT_DIR, "attempts/c-evaluator-optimizer/code/cse_opt"))
DATA_DIR = os.path.join(ROOT_DIR, "data")
LENS1_RES_DIR = os.path.join(ROOT_DIR, "attempts/c-evaluator-optimizer/result")
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../result"))


def extract_tensors(data):
    """Return U (m x n1*n2), V (m x n2*n3), W_out (n1*n3 x m) over {-1, 0, 1}."""
    n1, n2, n3 = data["n"]
    m = data["m"]
    if "u_fresh" in data:
        U, _, _ = verify_slp.expand_dag(n1 * n2, data["u_fresh"], data["u"], "u")
        V, _, _ = verify_slp.expand_dag(n2 * n3, data["v_fresh"], data["v"], "v")
        W_out, _, _ = verify_slp.expand_dag(m, data["w_fresh"], data["w"], "w")
    else:
        U = [list(r) for r in data["u"]]
        V = [list(r) for r in data["v"]]
        W_cols = data["w"]
        W_out = [[W_cols[r][c] for r in range(m)] for c in range(n1 * n3)]
    return U, V, W_out


def naive_adds_vec(mat):
    return sum(max(0, sum(1 for x in row if x != 0) - 1) for row in mat)


def is_ternary_nonzero(vec):
    nz = 0
    for x in vec:
        if x < -1 or x > 1:
            return False
        if x != 0:
            nz += 1
    return nz > 0


def find_valid_ternary_flips(U, V, W_out):
    """
    Find all rank-preserving ternary flip moves on (U, V, W_out).
    Note: W_col[r] is the r-th column of W_out (length n1*n3).
    """
    m = len(U)
    n_out = len(W_out)
    W_col = [[W_out[c][r] for c in range(n_out)] for r in range(m)]

    flips = []
    # Check all pairs (i, j) with i != j
    for i in range(m):
        for j in range(i + 1, m):
            # 1. Check if U[i] == s * U[j]
            for s in (1, -1):
                if all(U[i][k] == s * U[j][k] for k in range(len(U[i]))):
                    # Valid Mode-U shared factor!
                    # Option A: V[i]' = V[i] + sigma*s*V[j], W_col[j]' = W_col[j] - sigma*W_col[i]
                    for sigma in (1, -1):
                        vi_new = [V[i][k] + sigma * s * V[j][k] for k in range(len(V[i]))]
                        wj_new = [W_col[j][c] - sigma * W_col[i][c] for c in range(n_out)]
                        if is_ternary_nonzero(vi_new) and is_ternary_nonzero(wj_new):
                            d_cn = (sum(1 for x in vi_new if x != 0) - sum(1 for x in V[i] if x != 0)) + (
                                sum(1 for x in wj_new if x != 0) - sum(1 for x in W_col[j] if x != 0)
                            )
                            flips.append(("U", i, j, s, sigma, d_cn))
                        # Symmetric: V[j]' = V[j] + sigma*s*V[i], W_col[i]' = W_col[i] - sigma*W_col[j]
                        vj_new = [V[j][k] + sigma * s * V[i][k] for k in range(len(V[j]))]
                        wi_new = [W_col[i][c] - sigma * W_col[j][c] for c in range(n_out)]
                        if is_ternary_nonzero(vj_new) and is_ternary_nonzero(wi_new):
                            d_cn = (sum(1 for x in vj_new if x != 0) - sum(1 for x in V[j] if x != 0)) + (
                                sum(1 for x in wi_new if x != 0) - sum(1 for x in W_col[i] if x != 0)
                            )
                            flips.append(("U", j, i, s, sigma, d_cn))

            # 2. Check if V[i] == s * V[j]
            for s in (1, -1):
                if all(V[i][k] == s * V[j][k] for k in range(len(V[i]))):
                    for sigma in (1, -1):
                        ui_new = [U[i][k] + sigma * s * U[j][k] for k in range(len(U[i]))]
                        wj_new = [W_col[j][c] - sigma * W_col[i][c] for c in range(n_out)]
                        if is_ternary_nonzero(ui_new) and is_ternary_nonzero(wj_new):
                            d_cn = (sum(1 for x in ui_new if x != 0) - sum(1 for x in U[i] if x != 0)) + (
                                sum(1 for x in wj_new if x != 0) - sum(1 for x in W_col[j] if x != 0)
                            )
                            flips.append(("V", i, j, s, sigma, d_cn))
                        uj_new = [U[j][k] + sigma * s * U[i][k] for k in range(len(U[j]))]
                        wi_new = [W_col[i][c] - sigma * W_col[j][c] for c in range(n_out)]
                        if is_ternary_nonzero(uj_new) and is_ternary_nonzero(wi_new):
                            d_cn = (sum(1 for x in uj_new if x != 0) - sum(1 for x in U[j] if x != 0)) + (
                                sum(1 for x in wi_new if x != 0) - sum(1 for x in W_col[i] if x != 0)
                            )
                            flips.append(("V", j, i, s, sigma, d_cn))

            # 3. Check if W_col[i] == s * W_col[j]
            for s in (1, -1):
                if all(W_col[i][c] == s * W_col[j][c] for c in range(n_out)):
                    for sigma in (1, -1):
                        ui_new = [U[i][k] + sigma * s * U[j][k] for k in range(len(U[i]))]
                        vj_new = [V[j][k] - sigma * V[i][k] for k in range(len(V[j]))]
                        if is_ternary_nonzero(ui_new) and is_ternary_nonzero(vj_new):
                            d_cn = (sum(1 for x in ui_new if x != 0) - sum(1 for x in U[i] if x != 0)) + (
                                sum(1 for x in vj_new if x != 0) - sum(1 for x in V[j] if x != 0)
                            )
                            flips.append(("W", i, j, s, sigma, d_cn))
                        uj_new = [U[j][k] + sigma * s * U[i][k] for k in range(len(U[j]))]
                        vi_new = [V[i][k] - sigma * V[j][k] for k in range(len(V[i]))]
                        if is_ternary_nonzero(uj_new) and is_ternary_nonzero(vi_new):
                            d_cn = (sum(1 for x in uj_new if x != 0) - sum(1 for x in U[j] if x != 0)) + (
                                sum(1 for x in vi_new if x != 0) - sum(1 for x in V[i] if x != 0)
                            )
                            flips.append(("W", j, i, s, sigma, d_cn))

    flips.sort(key=lambda x: x[5])
    return flips


def apply_flip(U, V, W_out, flip):
    mode, i, j, s, sigma, _ = flip
    U2 = [list(r) for r in U]
    V2 = [list(r) for r in V]
    W2 = [list(r) for r in W_out]
    if mode == "U":
        V2[i] = [V2[i][k] + sigma * s * V2[j][k] for k in range(len(V2[i]))]
        for c in range(len(W2)):
            W2[c][j] = W2[c][j] - sigma * W2[c][i]
    elif mode == "V":
        U2[i] = [U2[i][k] + sigma * s * U2[j][k] for k in range(len(U2[i]))]
        for c in range(len(W2)):
            W2[c][j] = W2[c][j] - sigma * W2[c][i]
    elif mode == "W":
        U2[i] = [U2[i][k] + sigma * s * U2[j][k] for k in range(len(U2[i]))]
        V2[j] = [V2[j][k] - sigma * V2[i][k] for k in range(len(V2[j]))]
    return U2, V2, W2


def extract_warm_section(base_dim, fresh_list, out_list):
    target_vecs, _, _ = verify_slp.expand_dag(base_dim, fresh_list, out_list, "sec")
    n_fresh = len(fresh_list)
    sign_flip = [1] * (base_dim + n_fresh)
    norm_fresh = []
    for k, form in enumerate(fresh_list):
        if len(form) != 2:
            return target_vecs, [], []
        i0, v0 = form[0]["index"], form[0]["value"] * sign_flip[form[0]["index"]]
        i1, v1 = form[1]["index"], form[1]["value"] * sign_flip[form[1]["index"]]
        if i0 > i1:
            i0, i1 = i1, i0
            v0, v1 = v1, v0
        if v0 == -1:
            sign_flip[base_dim + k] = -1
            v0 = 1
            v1 = -v1
        norm_fresh.append((i0, i1, v1))

    norm_out = []
    for row in out_list:
        nrow = []
        for t in row:
            idx = t["index"]
            val = t["value"] * sign_flip[idx]
            nrow.append((idx, val))
        norm_out.append(nrow)

    return target_vecs, norm_fresh, norm_out


def run_cse_section(target_vecs, norm_fresh, norm_out, threads=8, time_ms=400, seed=42):
    R = len(target_vecs)
    C = len(target_vecs[0])
    with tempfile.NamedTemporaryFile("w", suffix=".in", delete=False) as fin:
        in_path = fin.name
        f_init = len(norm_fresh)
        fin.write(f"{R} {C} {f_init}\n")
        for r in range(R):
            fin.write(" ".join(str(x) for x in target_vecs[r]) + "\n")
        if f_init > 0:
            for a, b, s in norm_fresh:
                fin.write(f"{a} {b} {s}\n")
            if norm_out:
                for r in range(R):
                    row = norm_out[r]
                    fin.write(f"{len(row)} " + " ".join(f"{idx} {val}" for idx, val in row) + "\n")

    out_path = in_path + ".out"
    try:
        subprocess.run(
            [CSE_BIN, in_path, out_path, str(threads), str(time_ms), str(seed)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        with open(out_path, "r") as fout:
            lines = [l.strip() for l in fout if l.strip()]
        header = lines[0].split()
        total_adds, n_fresh = int(header[0]), int(header[1])
        fresh_json = []
        for i in range(n_fresh):
            a, b, s = map(int, lines[1 + i].split())
            fresh_json.append([{"index": a, "value": 1}, {"index": b, "value": s}])
        out_json = []
        for r in range(R):
            parts = list(map(int, lines[1 + n_fresh + r].split()))
            L = parts[0]
            row_terms = []
            for k in range(L):
                idx = parts[1 + 2 * k]
                val = parts[1 + 2 * k + 1]
                row_terms.append({"index": idx, "value": val})
            out_json.append(row_terms)
        return total_adds, fresh_json, out_json
    finally:
        if os.path.exists(in_path):
            os.remove(in_path)
        if os.path.exists(out_path):
            os.remove(out_path)


def main():
    os.makedirs(RESULT_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "fmm_sota.json")) as f:
        sota_data = json.load(f)
    sota_best = {}
    for item in sota_data["entries"]:
        dims = sorted(item["format"])
        fmt = f"{dims[0]}x{dims[1]}x{dims[2]}"
        r = int(item["rank"])
        if fmt not in sota_best or r < sota_best[fmt]:
            sota_best[fmt] = r

    # Focus on 20 candidate formats with max dim <= 8 where ZT rank == SOTA
    target_fmts = [
        "3x3x3", "2x3x3", "2x3x4", "2x4x4", "2x4x7", "2x4x8",
        "2x5x5", "2x5x6", "2x8x8", "3x3x4", "3x4x4", "3x4x5",
        "3x5x5", "4x4x5", "4x4x6", "4x4x7", "4x5x5", "4x5x6",
        "4x5x7", "4x5x8", "4x6x6", "4x6x7", "4x6x8",
        "5x5x5", "5x5x6", "5x5x7", "5x5x8"
    ]

    records = []
    for fmt in target_fmts:
        rank = sota_best[fmt]
        # Find live minimum cr in data/
        red_files = sorted(glob.glob(os.path.join(DATA_DIR, f"{fmt}_m{rank}_cr*_reduced.json")))
        if not red_files:
            continue
        live_crs = []
        for p in red_files:
            m = re.search(r"_cr(\d+)_", os.path.basename(p))
            if m:
                live_crs.append((int(m.group(1)), p))
        live_crs.sort()
        min_live_cr, best_live_path = live_crs[0]

        # Start from Lens 1 result if available, otherwise best live file
        lens1_files = sorted(glob.glob(os.path.join(LENS1_RES_DIR, f"{fmt}_m{rank}_cr*_reduced.json")))
        seed_path = lens1_files[0] if lens1_files else best_live_path
        with open(seed_path) as f:
            seed_data = json.load(f)

        n1, n2, n3 = seed_data["n"]
        U, V, W_out = extract_tensors(seed_data)
        flips = find_valid_ternary_flips(U, V, W_out)

        # Current best per section on seed_data
        u_vecs, u_nf, u_no = extract_tensors_and_warm_sec(n1 * n2, seed_data["u_fresh"], seed_data["u"])
        v_vecs, v_nf, v_no = extract_tensors_and_warm_sec(n2 * n3, seed_data["v_fresh"], seed_data["v"])
        w_vecs, w_nf, w_no = extract_tensors_and_warm_sec(rank, seed_data["w_fresh"], seed_data["w"])

        best_u = (sum(len(x) - 1 for x in seed_data["u_fresh"]) + sum(len(x) - 1 for x in seed_data["u"]), seed_data["u_fresh"], seed_data["u"])
        best_v = (sum(len(x) - 1 for x in seed_data["v_fresh"]) + sum(len(x) - 1 for x in seed_data["v"]), seed_data["v_fresh"], seed_data["v"])
        best_w = (sum(len(x) - 1 for x in seed_data["w_fresh"]) + sum(len(x) - 1 for x in seed_data["w"]), seed_data["w_fresh"], seed_data["w"])

        # Deepen LNS + CSE on the seed scheme first (500ms per section)
        ua, uf, uo = run_cse_section(u_vecs, u_nf, u_no, threads=8, time_ms=500, seed=7001 + rank)
        if ua < best_u[0]:
            best_u = (ua, uf, uo)
        va, vf, vo = run_cse_section(v_vecs, v_nf, v_no, threads=8, time_ms=500, seed=7002 + rank)
        if va < best_v[0]:
            best_v = (va, vf, vo)
        wa, wf, wo = run_cse_section(w_vecs, w_nf, w_no, threads=8, time_ms=500, seed=7003 + rank)
        if wa < best_w[0]:
            best_w = (wa, wf, wo)

        best_total_cr = best_u[0] + best_v[0] + best_w[0]
        best_scheme_data = {
            "n": [n1, n2, n3],
            "m": rank,
            "z2": False,
            "complexity": {"naive": naive_adds_vec(U) + naive_adds_vec(V) + naive_adds_vec(W_out), "reduced": best_total_cr},
            "u_fresh": best_u[1],
            "u": best_u[2],
            "v_fresh": best_v[1],
            "v": best_v[2],
            "w_fresh": best_w[1],
            "w": best_w[2],
        }
        won_by_flip = False

        # Test top 4 rank-preserving ternary flips (with lowest d_cn) using single-mode invariance (H2)!
        tested_flips = 0
        for flip in flips[:4]:
            mode, i, j, s, sigma, d_cn = flip
            if d_cn > 2:
                continue
            U2, V2, W2 = apply_flip(U, V, W_out, flip)
            tested_flips += 1
            if mode == "U":
                # U is unchanged! Reuse best_u and warm-start V2, W2 from parent fresh vars
                va2, vf2, vo2 = run_cse_section(V2, v_nf, [], threads=8, time_ms=200, seed=8000 + tested_flips)
                wa2, wf2, wo2 = run_cse_section(W2, w_nf, [], threads=8, time_ms=200, seed=8100 + tested_flips)
                cand_cr = best_u[0] + va2 + wa2
                if cand_cr < best_total_cr:
                    best_total_cr = cand_cr
                    won_by_flip = True
                    best_scheme_data = {
                        "n": [n1, n2, n3], "m": rank, "z2": False,
                        "complexity": {"naive": naive_adds_vec(U2) + naive_adds_vec(V2) + naive_adds_vec(W2), "reduced": cand_cr},
                        "u_fresh": best_u[1], "u": best_u[2],
                        "v_fresh": vf2, "v": vo2,
                        "w_fresh": wf2, "w": wo2,
                    }
            elif mode == "V":
                # V is unchanged! Reuse best_v and warm-start U2, W2 from parent fresh vars
                ua2, uf2, uo2 = run_cse_section(U2, u_nf, [], threads=8, time_ms=200, seed=8200 + tested_flips)
                wa2, wf2, wo2 = run_cse_section(W2, w_nf, [], threads=8, time_ms=200, seed=8300 + tested_flips)
                cand_cr = ua2 + best_v[0] + wa2
                if cand_cr < best_total_cr:
                    best_total_cr = cand_cr
                    won_by_flip = True
                    best_scheme_data = {
                        "n": [n1, n2, n3], "m": rank, "z2": False,
                        "complexity": {"naive": naive_adds_vec(U2) + naive_adds_vec(V2) + naive_adds_vec(W2), "reduced": cand_cr},
                        "u_fresh": uf2, "u": uo2,
                        "v_fresh": best_v[1], "v": best_v[2],
                        "w_fresh": wf2, "w": wo2,
                    }
            elif mode == "W":
                # W is unchanged! Reuse best_w and warm-start U2, V2 from parent fresh vars
                ua2, uf2, uo2 = run_cse_section(U2, u_nf, [], threads=8, time_ms=200, seed=8400 + tested_flips)
                va2, vf2, vo2 = run_cse_section(V2, v_nf, [], threads=8, time_ms=200, seed=8500 + tested_flips)
                cand_cr = ua2 + va2 + best_w[0]
                if cand_cr < best_total_cr:
                    best_total_cr = cand_cr
                    won_by_flip = True
                    best_scheme_data = {
                        "n": [n1, n2, n3], "m": rank, "z2": False,
                        "complexity": {"naive": naive_adds_vec(U2) + naive_adds_vec(V2) + naive_adds_vec(W2), "reduced": cand_cr},
                        "u_fresh": uf2, "u": uo2,
                        "v_fresh": vf2, "v": vo2,
                        "w_fresh": best_w[1], "w": best_w[2],
                    }

        print(
            f"  [{fmt:<5} m={rank:<3}] valid_flips={len(flips):<3} tested={tested_flips} | "
            f"live_cr={min_live_cr:<4} -> lens2_cr={best_total_cr:<4} (flip_win={won_by_flip})",
            flush=True,
        )

        if best_total_cr < min_live_cr:
            fv = len(best_scheme_data["u_fresh"]) + len(best_scheme_data["v_fresh"]) + len(best_scheme_data["w_fresh"])
            cn = best_scheme_data["complexity"]["naive"]
            out_name = f"{fmt}_m{rank}_cr{best_total_cr}_fv{fv}_cn{cn}_ZT_reduced.json"
            out_path = os.path.join(RESULT_DIR, out_name)
            with open(out_path, "w") as fout:
                json.dump(best_scheme_data, fout, indent=2)
            res = verify_slp.verify_slp_file(out_path)
            assert res["cr"] == best_total_cr
            records.append((fmt, rank, min_live_cr, best_total_cr, min_live_cr - best_total_cr, out_name, won_by_flip))

    print("\n=== Lens 2 Summary ===")
    print(f"Total verified records in Lens 2: {len(records)}")
    for fmt, rank, old_cr, new_cr, margin, fname, fwin in records:
        print(f"  {fmt:<7} m={rank:<3} : {old_cr:<4} -> {new_cr:<4} (-{margin:<2} adds) | {fname} (flip_win={fwin})")


def extract_tensors_and_warm_sec(base_dim, fresh_list, out_list):
    return extract_warm_section(base_dim, fresh_list, out_list)


if __name__ == "__main__":
    main()
