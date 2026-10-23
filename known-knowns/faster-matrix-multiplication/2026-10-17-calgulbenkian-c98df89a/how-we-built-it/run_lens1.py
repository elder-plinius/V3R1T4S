#!/usr/bin/env python3
"""
Driver for Lens 1 (c-evaluator-optimizer):
Runs native C multi-threaded optimizer (cse_opt) across candidate FMM formats with
max(n, m, p) <= 8 where ZT rank equals fmm_sota.json best rank, verifies every
output symbolically over Z via verify_slp.py, and saves all strict improvements.
"""

import glob
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, ROOT_DIR)
import verify_slp

CSE_BIN = os.path.join(os.path.dirname(__file__), "cse_opt")
DATA_DIR = os.path.join(ROOT_DIR, "data")
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../result"))


def extract_warm_section(base_dim, fresh_list, out_list):
    """
    Expand a section (U, V, or W) to get its exact target matrix R x C,
    and normalize fresh_list into (a, b, s) triples with val_a = +1.
    Wait: in Perminov's _reduced.json, a fresh variable might have
    [{"index": a, "value": -1}, {"index": b, "value": 1}].
    If the first term has value -1, negating that fresh variable flips its sign in all
    subsequent references! Let's normalize so every fresh variable is v_a + s * v_b.
    """
    target_vecs, _, _ = verify_slp.expand_dag(base_dim, fresh_list, out_list, "sec")

    # Normalize fresh variables so term[0].value == +1
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


def run_cse_section(target_vecs, norm_fresh, norm_out, threads=8, time_ms=1500, seed=42):
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


def optimize_reduced_scheme(path, threads=8, time_ms_per_sec=1200, seed=100):
    with open(path, "r") as f:
        d = json.load(f)
    n1, n2, n3 = d["n"]
    m = d["m"]
    orig_cr = d["complexity"]["reduced"]
    orig_cn = d["complexity"]["naive"]

    best_sections = {}
    for sec_idx, (sec, base_dim) in enumerate([("u", n1 * n2), ("v", n2 * n3), ("w", m)]):
        t_vecs, n_fresh, n_out = extract_warm_section(base_dim, d[sec + "_fresh"], d[sec])
        orig_sec_adds = sum(len(x) - 1 for x in d[sec + "_fresh"]) + sum(len(x) - 1 for x in d[sec])
        adds, f_json, o_json = run_cse_section(
            t_vecs, n_fresh, n_out, threads=threads, time_ms=time_ms_per_sec, seed=seed + 17 * sec_idx
        )
        if adds < orig_sec_adds:
            best_sections[sec] = (adds, f_json, o_json, orig_sec_adds)
        else:
            best_sections[sec] = (orig_sec_adds, d[sec + "_fresh"], d[sec], orig_sec_adds)

    new_cr = sum(best_sections[s][0] for s in ("u", "v", "w"))
    new_fv = sum(len(best_sections[s][1]) for s in ("u", "v", "w"))
    new_data = {
        "n": [n1, n2, n3],
        "m": m,
        "z2": False,
        "complexity": {"naive": orig_cn, "reduced": new_cr},
        "u_fresh": best_sections["u"][1],
        "u": best_sections["u"][2],
        "v_fresh": best_sections["v"][1],
        "v": best_sections["v"][2],
        "w_fresh": best_sections["w"][1],
        "w": best_sections["w"][2],
    }
    return orig_cr, new_cr, new_fv, orig_cn, best_sections, new_data


def optimize_raw_zt_scheme(path, threads=8, time_ms_per_sec=2000, seed=500):
    with open(path, "r") as f:
        d = json.load(f)
    n1, n2, n3 = d["n"]
    m = d["m"]
    U_vecs = d["u"]
    V_vecs = d["v"]
    W_cols = d["w"]  # m x (n3*n1)
    W_vecs = [[W_cols[r][c] for r in range(m)] for c in range(n1 * n3)]

    u_naive = sum(max(0, sum(1 for x in row if x != 0) - 1) for row in U_vecs)
    v_naive = sum(max(0, sum(1 for x in row if x != 0) - 1) for row in V_vecs)
    w_naive = sum(max(0, sum(1 for x in row if x != 0) - 1) for row in W_vecs)
    cn = u_naive + v_naive + w_naive

    u_adds, u_f, u_o = run_cse_section(U_vecs, [], [], threads=threads, time_ms=time_ms_per_sec, seed=seed + 1)
    v_adds, v_f, v_o = run_cse_section(V_vecs, [], [], threads=threads, time_ms=time_ms_per_sec, seed=seed + 2)
    w_adds, w_f, w_o = run_cse_section(W_vecs, [], [], threads=threads, time_ms=time_ms_per_sec, seed=seed + 3)

    new_cr = u_adds + v_adds + w_adds
    new_fv = len(u_f) + len(v_f) + len(w_f)
    new_data = {
        "n": [n1, n2, n3],
        "m": m,
        "z2": False,
        "complexity": {"naive": cn, "reduced": new_cr},
        "u_fresh": u_f,
        "u": u_o,
        "v_fresh": v_f,
        "v": v_o,
        "w_fresh": w_f,
        "w": w_o,
    }
    return new_cr, new_fv, cn, (u_adds, v_adds, w_adds), new_data


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

    # Group reduced files by format
    red_files = sorted(glob.glob(os.path.join(DATA_DIR, "*_reduced.json")))
    by_fmt = {}
    for p in red_files:
        b = os.path.basename(p)
        m = re.match(r"^(\d+x\d+x\d+)_m(\d+)_cr(\d+)_(?:fv\d+_)?cn(\d+)_ZT_reduced\.json$", b)
        if not m:
            continue
        fmt, rank, cr, cn = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        if rank == sota_best.get(fmt):
            by_fmt.setdefault(fmt, []).append((cr, cn, p))

    print(f"Running Lens 1 (cse_opt) across {len(by_fmt)} SOTA-rank formats (max dim <= 8)...")
    records = []
    for fmt in sorted(by_fmt.keys(), key=lambda x: [int(d) for d in x.split("x")]):
        flist = sorted(by_fmt[fmt])
        min_live_cr = flist[0][0]
        rank = sota_best[fmt]
        best_cand_cr = min_live_cr
        best_cand_data = None
        best_cand_desc = ""

        # Test top 2 reduced files for this format
        for cr, cn, p in flist[:1]:
            orig_cr, new_cr, new_fv, orig_cn, secs, new_data = optimize_reduced_scheme(
                p, threads=8, time_ms_per_sec=350, seed=1000 + cr
            )
            u_a, v_a, w_a = secs["u"][0], secs["v"][0], secs["w"][0]
            u_o, v_o, w_o = secs["u"][3], secs["v"][3], secs["w"][3]
            print(
                f"  [{fmt} m={rank}] warm from cr={orig_cr} (cn={orig_cn}): "
                f"new_cr={new_cr} (U:{u_o}->{u_a}, V:{v_o}->{v_a}, W:{w_o}->{w_a}) fv={new_fv}",
                flush=True,
            )
            if new_cr < best_cand_cr:
                best_cand_cr = new_cr
                best_cand_data = new_data
                best_cand_desc = f"warm({os.path.basename(p)})"

        # Also check if a raw _ZT.json exists with different cn
        raw_p = os.path.join(DATA_DIR, f"{fmt}_m{rank}_ZT.json")
        if os.path.exists(raw_p):
            new_cr, new_fv, cn, (u_a, v_a, w_a), new_data = optimize_raw_zt_scheme(
                raw_p, threads=8, time_ms_per_sec=700, seed=2000 + rank
            )
            print(
                f"  [{fmt} m={rank}] from raw {os.path.basename(raw_p)} (cn={cn}): "
                f"new_cr={new_cr} (U:{u_a}, V:{v_a}, W:{w_a}) fv={new_fv}",
                flush=True,
            )
            if new_cr < best_cand_cr:
                best_cand_cr = new_cr
                best_cand_data = new_data
                best_cand_desc = f"raw({os.path.basename(raw_p)})"

        if best_cand_data is not None and best_cand_cr < min_live_cr:
            fv = best_cand_data["u_fresh"].__len__() + best_cand_data["v_fresh"].__len__() + best_cand_data["w_fresh"].__len__()
            cn = best_cand_data["complexity"]["naive"]
            out_name = f"{fmt}_m{rank}_cr{best_cand_cr}_fv{fv}_cn{cn}_ZT_reduced.json"
            out_path = os.path.join(RESULT_DIR, out_name)
            with open(out_path, "w") as fout:
                json.dump(best_cand_data, fout, indent=2)
            res = verify_slp.verify_slp_file(out_path)
            assert res["cr"] == best_cand_cr
            margin = min_live_cr - best_cand_cr
            print(
                f"  *** NEW RECORD for {fmt} (m={rank}): cr={best_cand_cr} < live {min_live_cr} (-{margin} adds) "
                f"verified over Z! Saved to {out_name} ***"
            )
            records.append((fmt, rank, min_live_cr, best_cand_cr, margin, out_name, best_cand_desc))

    print("\n=== Lens 1 Summary ===")
    print(f"Total strict records found and verified over Z: {len(records)}")
    for fmt, rank, old_cr, new_cr, margin, fname, desc in records:
        print(f"  {fmt:<7} m={rank:<3} : {old_cr:<4} -> {new_cr:<4} (-{margin:<2} adds) | {fname} [{desc}]")


if __name__ == "__main__":
    main()
