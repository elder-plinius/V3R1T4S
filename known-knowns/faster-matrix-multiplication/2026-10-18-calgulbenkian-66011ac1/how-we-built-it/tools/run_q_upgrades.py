#!/usr/bin/env python3
import itertools
import json
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from verify_z_brent import load_reference_bounds, verify_scheme
from upgrade_schemes import load_mpl_raw, solve_linear_map, optimize_block
from unfold_z_to_zt import run_c_opt

table, sota = load_reference_bounds(".")

os.makedirs("data/bases", exist_ok=True)
base_specs = [
    ("245", 32, (2, 4, 5), "schemes/known/tensor/2x4x5_tensor.mpl", "schemes/results/ZT/2x4x5_m33_ZT.json"),
    ("336", 40, (3, 3, 6), "schemes/known/tensor/3x3x6_tensor.mpl", "schemes/results/ZT/3x3x6_m42_ZT.json"),
    ("444", 48, (4, 4, 4), "schemes/known/tensor/4x4x4_tensor.mpl", "schemes/results/ZT/4x4x4_m49_ZT.json"),
    ("347", 63, (3, 4, 7), "schemes/known/tensor/3x4x7_tensor.mpl", "schemes/results/ZT/3x4x7_m64_ZT.json"),
]

bases = []
for tag, bsize, mdims, mpl_git, zt_git in base_specs:
    mpl_local = f"data/bases/{tag}.mpl"
    zt_local = f"data/bases/{tag}_ZT.json"
    if not os.path.exists(mpl_local):
        raw = subprocess.check_output(["git", "-C", "data/FastMatrixMultiplication", "show", f"HEAD:{mpl_git}"])
        open(mpl_local, "wb").write(raw)
    if not os.path.exists(zt_local):
        raw = subprocess.check_output(["git", "-C", "data/FastMatrixMultiplication", "show", f"HEAD:{zt_git}"])
        open(zt_local, "wb").write(raw)
    mpl = load_mpl_raw(mpl_local, *mdims)
    zt_d = json.load(open(zt_local))
    zt = [zt_d["u"], zt_d["v"], zt_d["w"]]
    # Check how many leading triads in mpl are purely integer
    lead_int = 0
    for idx in range(bsize):
        if any(x.denominator != 1 for x in mpl[0][idx] + mpl[1][idx] + mpl[2][idx]):
            lead_int = idx
            break
    bases.append((bsize, mpl, zt, mdims, tag, lead_int))


def split_vec_ternary(vec):
    """Decompose integer vector into minimal number of ternary vectors."""
    max_a = max((abs(x) for x in vec), default=0)
    if max_a <= 1:
        return [list(vec)]
    parts = []
    cur = list(vec)
    while any(x != 0 for x in cur):
        step = [1 if x > 0 else (-1 if x < 0 else 0) for x in cur]
        parts.append(step)
        cur = [cur[i] - step[i] for i in range(len(cur))]
    return parts


def fast_split_to_zt(U, V, W):
    Uu, Vv, Ww = [], [], []
    for r in range(len(U)):
        pu = split_vec_ternary(U[r])
        pv = split_vec_ternary(V[r])
        pw = split_vec_ternary(W[r])
        for u1 in pu:
            for v1 in pv:
                for w1 in pw:
                    Uu.append(u1)
                    Vv.append(v1)
                    Ww.append(w1)
    return Uu, Vv, Ww


target_q = [
    "schemes/results/Q/12x13x16_m1509_Q.json",
    "schemes/results/Q/11x12x16_m1278_Q.json",
    "schemes/results/Q/12x16x16_m1815_Q.json",
    "schemes/results/Q/14x16x16_m2128_Q.json",
    "schemes/results/Q/9x12x16_m1035_Q.json",
    "schemes/results/Q/9x10x12_m668_Q.json",
    "schemes/results/Q/11x12x12_m968_Q.json",
    "schemes/results/Q/11x12x14_m1153_Q.json",
    "schemes/results/Q/11x14x16_m1520_Q.json",
    "schemes/results/Q/12x14x14_m1449_Q.json",
]

os.makedirs("results/new_upgrades", exist_ok=True)

for qf in target_q:
    raw = subprocess.check_output(["git", "-C", "data/FastMatrixMultiplication", "show", f"HEAD:{qf}"])
    d = json.loads(raw)
    n_list = [int(x) for x in d["n"]]
    dims = tuple(sorted(n_list))
    fmt = f"{n_list[0]}x{n_list[1]}x{n_list[2]}"
    ref = table[dims]
    R = d["m"]
    U = [[Fraction(x) for x in row] for row in d["u"]]
    V = [[Fraction(x) for x in row] for row in d["v"]]
    W = [[Fraction(x) for x in row] for row in d["w"]]
    frac_set = set(
        r for r in range(R) if any(x.denominator != 1 for x in U[r] + V[r] + W[r])
    )
    r = 0
    new_U, new_V, new_W = [], [], []
    counts = {b[4]: 0 for b in bases}
    ok = True
    while r < R:
        matched = False
        for bsize, mpl, zt, mdims, tag, lead_int in bases:
            # A block matches at r if r + lead_int is in frac_set
            if (r + lead_int) in frac_set and r + bsize <= R:
                Ub, Vb, Wb = U[r : r + bsize], V[r : r + bsize], W[r : r + bsize]
                for perm in itertools.permutations([0, 1, 2]):
                    PU = solve_linear_map(mpl[perm[0]], Ub)
                    if PU is None:
                        continue
                    PV = solve_linear_map(mpl[perm[1]], Vb)
                    if PV is None:
                        continue
                    PW = solve_linear_map(mpl[perm[2]], Wb)
                    if PW is None:
                        continue
                    P_canon = [None, None, None]
                    P_canon[perm[0]] = PU
                    P_canon[perm[1]] = PV
                    P_canon[perm[2]] = PW
                    u_c, v_c, w_c, sc = optimize_block(
                        P_canon[0], P_canon[1], P_canon[2], zt[0], zt[1], zt[2], *mdims
                    )
                    out_c = [u_c, v_c, w_c]
                    new_U.extend(out_c[perm[0]])
                    new_V.extend(out_c[perm[1]])
                    new_W.extend(out_c[perm[2]])
                    counts[tag] += 1
                    r += bsize
                    matched = True
                    break
            if matched:
                break
        if not matched:
            if r not in frac_set:
                new_U.append([int(x) for x in U[r]])
                new_V.append([int(x) for x in V[r]])
                new_W.append([int(x) for x in W[r]])
                r += 1
            else:
                ok = False
                print(f"Failed to match block at r={r} in {qf}", flush=True)
                break

    if not ok:
        continue

    cur_d = {"n": n_list, "m": len(new_U), "u": new_U, "v": new_V, "w": new_W}
    max_abs = max(abs(x) for mat in (new_U, new_V, new_W) for row in mat for x in row)
    cur_d = run_c_opt(cur_d, steps=50000, seed=1337, max_c=max(1, max_abs))
    max_abs = max(abs(x) for mat in (cur_d["u"], cur_d["v"], cur_d["w"]) for row in mat for x in row)
    coeff_class = "ZT" if max_abs <= 1 else "Z"
    new_R = cur_d["m"]
    if new_R < ref[coeff_class]:
        out_path = f"results/new_upgrades/{fmt}_m{new_R}_{coeff_class}.json"
        with open(out_path, "w") as f:
            json.dump(cur_d, f, separators=(",", ":"))
        v_ok, msg = verify_scheme(out_path, table, sota)
        print(f"UPGRADE {qf} (counts={counts}):\n  {msg}", flush=True)
    else:
        print(f"NO BEAT {qf}: {coeff_class} rank={new_R} vs ref={ref[coeff_class]}", flush=True)

    if coeff_class == "Z":
        U_zt, V_zt, W_zt = fast_split_to_zt(cur_d["u"], cur_d["v"], cur_d["w"])
        if len(U_zt) <= ref["ZT"] + 15:
            zt_d = {"n": n_list, "m": len(U_zt), "u": U_zt, "v": V_zt, "w": W_zt}
            zt_d = run_c_opt(zt_d, steps=100000, seed=1337, max_c=1)
            if zt_d["m"] < ref["ZT"]:
                zt_path = f"results/new_upgrades/{fmt}_m{zt_d['m']}_ZT.json"
                with open(zt_path, "w") as f:
                    json.dump(zt_d, f, separators=(",", ":"))
                v_ok2, msg2 = verify_scheme(zt_path, table, sota)
                print(f"  ZT SPLIT:\n  {msg2}", flush=True)
            else:
                print(f"  ZT SPLIT NO BEAT: rank={zt_d['m']} vs ref(ZT)={ref['ZT']}", flush=True)
