#!/usr/bin/env python3
"""
Standalone exact integer and ternary Brent equation verifier for fmm-ternary-integer-ring-upgrade.
Zero third-party dependencies (standard library only).
"""
import json
import os
import re
import sys


def load_reference_bounds(base_dir="."):
    readme_path = os.path.join(base_dir, "perminov_README.md")
    if not os.path.exists(readme_path):
        readme_path = os.path.join(base_dir, "data", "perminov_README.md")
    sota_path = os.path.join(base_dir, "fmm_sota.json")
    if not os.path.exists(sota_path):
        sota_path = os.path.join(base_dir, "data", "fmm_sota.json")
    merlijn_path = os.path.join(base_dir, "merlijn_SHA256SUMS.txt")
    if not os.path.exists(merlijn_path):
        merlijn_path = os.path.join(base_dir, "data", "merlijn_SHA256SUMS.txt")

    table = {}
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        for line in lines[766:1447]:
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) < 5:
                continue
            fmt = parts[0].strip("`")
            dims = tuple(sorted(map(int, fmt.split("x"))))
            m_zt = re.search(r"\d+", parts[1])
            m_z = re.search(r"\d+", parts[2])
            m_q = re.search(r"\d+", parts[3])
            if m_zt and m_z and m_q:
                table[dims] = {
                    "fmt": fmt,
                    "ZT": int(m_zt.group(0)),
                    "Z": int(m_z.group(0)),
                    "Q": int(m_q.group(0)),
                }

    if os.path.exists(merlijn_path):
        with open(merlijn_path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r"(\d+)x(\d+)x(\d+)_m(\d+)_ZT\.json", line)
                if m:
                    d = tuple(sorted(map(int, m.groups()[:3])))
                    r = int(m.group(4))
                    if d in table:
                        table[d]["ZT"] = min(table[d]["ZT"], r)

    sota = {}
    if os.path.exists(sota_path):
        with open(sota_path, "r", encoding="utf-8") as f:
            sota_raw = json.load(f)
        for k, v in sota_raw.get("sota", sota_raw).items():
            if "x" in k:
                d = tuple(sorted(map(int, k.split("x"))))
                r = v["rank"] if isinstance(v, dict) else int(v)
                sota[d] = min(sota.get(d, 10**9), r)

    if not table:
        table = {
            (4, 13, 15): {"fmt": "4x13x15", "ZT": 536, "Z": 536, "Q": 520},
            (4, 14, 15): {"fmt": "4x14x15", "ZT": 572, "Z": 572, "Q": 557},
            (7, 8, 15): {"fmt": "7x8x15", "ZT": 571, "Z": 571, "Q": 557},
            (9, 10, 14): {"fmt": "9x10x14", "ZT": 820, "Z": 820, "Q": 808},
            (9, 11, 14): {"fmt": "9x11x14", "ZT": 900, "Z": 900, "Q": 882},
            (9, 13, 14): {"fmt": "9x13x14", "ZT": 1050, "Z": 1050, "Q": 1024},
        }
    if not sota:
        sota = {
            (4, 13, 15): 520,
            (4, 14, 15): 557,
            (7, 8, 15): 557,
            (9, 10, 14): 808,
            (9, 11, 14): 882,
            (9, 13, 14): 1024,
        }
    return table, sota


def verify_scheme(path, table=None, sota=None):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    n1, n2, n3 = [int(x) for x in data["n"]]
    m = int(data["m"])
    U = data["u"]
    V = data["v"]
    W = data["w"]

    if not (len(U) == len(V) == len(W) == m):
        return False, f"Length mismatch: m={m}, len(u)={len(U)}, len(v)={len(V)}, len(w)={len(W)}"

    d1, d2, d3 = n1 * n2, n2 * n3, n3 * n1
    max_abs = 0
    U_int, V_int, W_int = [], [], []
    active_r = 0

    for r in range(m):
        if len(U[r]) != d1 or len(V[r]) != d2 or len(W[r]) != d3:
            return False, f"Factor dimension mismatch at term {r}"
        ur = [int(x) for x in U[r]]
        vr = [int(x) for x in V[r]]
        wr = [int(x) for x in W[r]]
        for x, orig in zip(ur + vr + wr, U[r] + V[r] + W[r]):
            if str(orig).strip() != str(x):
                return False, f"Non-integer coefficient {orig} at term {r}"
            if abs(x) > max_abs:
                max_abs = abs(x)
        if any(ur) and any(vr) and any(wr):
            active_r += 1
            U_int.append(ur)
            V_int.append(vr)
            W_int.append(wr)

    ring_class = "ZT" if max_abs <= 1 else "Z"
    r_eff = len(U_int)

    # Fast exact integer verification of all d1 * d2 * d3 Brent equations:
    # For each (a, b) in [d1] x [d2], compute vector S_{a,b}[c] = sum_r U[r][a] * V[r][b] * W[r][c]
    # Pre-group non-zero (r, U[r][a]) for each a in [d1]
    u_by_a = [[] for _ in range(d1)]
    for r in range(r_eff):
        ur = U_int[r]
        for a, val in enumerate(ur):
            if val != 0:
                u_by_a[a].append((r, val))

    # Target tensor for Perminov convention:
    # A is n1 x n2 (index a = i*n2 + k)
    # B is n2 x n3 (index b = k*n3 + j)
    # C = (A*B)^T is n3 x n1 (index c = j*n1 + i)
    for a in range(d1):
        i, k1 = divmod(a, n2)
        active_u = u_by_a[a]
        for b in range(d2):
            k2, j = divmod(b, n3)
            # Accumulate over c in [d3]
            acc = [0] * d3
            for r, u_val in active_u:
                v_val = V_int[r][b]
                if v_val != 0:
                    prod = u_val * v_val
                    wr = W_int[r]
                    for c in range(d3):
                        if wr[c] != 0:
                            acc[c] += prod * wr[c]
            target_c = (j * n1 + i) if (k1 == k2) else -1
            for c in range(d3):
                expected = 1 if c == target_c else 0
                if acc[c] != expected:
                    return False, f"Brent mismatch at a={a}, b={b}, c={c}: got {acc[c]}, expected {expected}"

    dims = tuple(sorted((n1, n2, n3)))
    if dims == (4, 4, 4):
        return False, "Format 4x4x4 is excluded from fmm-ternary-integer-ring-upgrade"

    status_msg = f"PASS: {path} | format={n1}x{n2}x{n3} class={ring_class} max_abs={max_abs} rank={r_eff}"
    if table and dims in table:
        ref = table[dims]
        best_overall = min(ref["ZT"], ref["Z"], ref["Q"])
        if sota and dims in sota:
            best_overall = min(best_overall, sota[dims])
        target_col = ref["ZT"] if ring_class == "ZT" else ref["Z"]
        is_upgrade = (r_eff < target_col) and (r_eff >= best_overall)
        status_msg += (
            f" | ref({ring_class})={target_col} saved={target_col - r_eff}"
            f" best_overall={best_overall} valid_ring_upgrade={is_upgrade}"
        )
        if not is_upgrade:
            return False, status_msg + " [FAILED RING UPGRADE BOUNDS]"

    return True, status_msg


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_z_brent.py scheme_file.json [...]")
        sys.exit(1)
    table, sota = load_reference_bounds(".")
    all_ok = True
    for path in sys.argv[1:]:
        ok, msg = verify_scheme(path, table, sota)
        print(msg)
        if not ok:
            all_ok = False
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
