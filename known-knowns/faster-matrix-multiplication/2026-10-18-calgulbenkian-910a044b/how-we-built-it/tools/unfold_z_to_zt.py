#!/usr/bin/env python3
import json
import subprocess
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from verify_z_brent import load_reference_bounds, verify_scheme
from upgrade_schemes import try_split_to_zt

table, sota = load_reference_bounds(".")


def count_bad(d):
    U, V, W = d["u"], d["v"], d["w"]
    bt, be = 0, 0
    for r in range(d["m"]):
        b = sum(abs(x) - 1 for x in U[r] + V[r] + W[r] if abs(x) > 1)
        if b > 0:
            bt += 1
            be += b
    return bt, be


def run_c_opt(d, steps=50000, seed=1337, max_c=2):
    n1, n2, n3 = d["n"]
    R = d["m"]
    lines = [f"{n1} {n2} {n3} {R}"]
    for mat in (d["u"], d["v"], d["w"]):
        for r in range(R):
            lines.append(" ".join(str(x) for x in mat[r]))
    inp = "\n".join(lines) + "\n"
    p = subprocess.run(
        ["./bin/zt_flip_reduce", str(steps), str(seed), str(max_c)],
        input=inp,
        text=True,
        capture_output=True,
    )
    out_lines = p.stdout.strip().splitlines()
    h = list(map(int, out_lines[0].split()))
    new_R = h[3]
    idx = 1
    U = [list(map(int, out_lines[idx + r].split())) for r in range(new_R)]
    idx += new_R
    V = [list(map(int, out_lines[idx + r].split())) for r in range(new_R)]
    idx += new_R
    W = [list(map(int, out_lines[idx + r].split())) for r in range(new_R)]
    idx += new_R
    return {"n": [n1, n2, n3], "m": new_R, "u": U, "v": V, "w": W}


def unfold_once(d):
    U, V, W = d["u"], d["v"], d["w"]
    R = d["m"]
    bad_set = set(r for r in range(R) if any(abs(x) > 1 for x in U[r] + V[r] + W[r]))
    if not bad_set:
        return d, False

    cur_bt, cur_be = count_bad(d)
    mats = [U, V, W]
    candidates = []
    for f in range(3):
        M = mats[f]
        bad_f = set(r for r in range(R) if any(abs(x) > 1 for x in M[r]))
        if not bad_f:
            continue
        vec_map = {}
        for r, v in enumerate(M):
            vec_map.setdefault(tuple(v), []).append((r, 1))
            vec_map.setdefault(tuple(-x for x in v), []).append((r, -1))
        for r0 in sorted(bad_f):
            v0 = M[r0]
            for r1 in range(R):
                if r1 == r0:
                    continue
                v1 = M[r1]
                for s1 in (1, -1):
                    diff = tuple(v0[i] - s1 * v1[i] for i in range(len(v0)))
                    if diff in vec_map:
                        for r2, s2 in vec_map[diff]:
                            if r2 > r1 and r2 != r0:
                                nbf = (r0 in bad_f) + (r1 in bad_f) + (r2 in bad_f)
                                nb = (r0 in bad_set) + (r1 in bad_set) + (r2 in bad_set)
                                candidates.append((nbf, nb, f, r0, r1, s1, r2, s2))

    candidates.sort(reverse=True)
    best_next = None
    best_score = (cur_bt, cur_be)

    seen = set()
    for nbf, nb, f, r0, r1, s1, r2, s2 in candidates:
        key = (f, r0, r1, r2)
        if key in seen:
            continue
        seen.add(key)
        U2 = [list(x) for i, x in enumerate(U) if i != r0]
        V2 = [list(x) for i, x in enumerate(V) if i != r0]
        W2 = [list(x) for i, x in enumerate(W) if i != r0]
        t_a = [list(U[r0]), list(V[r0]), list(W[r0])]
        t_b = [list(U[r0]), list(V[r0]), list(W[r0])]
        M = [U, V, W][f]
        t_a[f] = [s1 * x for x in M[r1]]
        t_b[f] = [s2 * x for x in M[r2]]
        U2.extend([t_a[0], t_b[0]])
        V2.extend([t_a[1], t_b[1]])
        W2.extend([t_a[2], t_b[2]])
        d_try = {"n": d["n"], "m": len(U2), "u": U2, "v": V2, "w": W2}
        d_opt = run_c_opt(d_try, steps=5000, seed=1337, max_c=2)
        bt, be = count_bad(d_opt)
        if bt <= cur_bt - 2 and (bt, be) < best_score:
            best_score = (bt, be)
            best_next = (d_opt, (nb, f, r0, r1, r2, bt, be))
            if cur_bt - bt >= 3:
                break

    if best_next is not None:
        d_opt, info = best_next
        print(
            f"  Unfolded f={info[1]} r0={info[2]} (with {info[3]},{info[4]}): R={d_opt['m']} bad_triads {cur_bt}->{info[5]} bad_entries {cur_be}->{info[6]}",
            flush=True,
        )
        return d_opt, True
    return d, False


if __name__ == "__main__":
    os.makedirs("results/new_upgrades", exist_ok=True)
    for zf in [
        "schemes/results/Z/14x15x15_m1895_Z.json",
        "schemes/results/Z/10x15x15_m1389_Z.json",
        "schemes/results/Z/10x15x16_m1484_Z.json",
        "schemes/results/Z/9x10x13_m763_Z.json",
        "schemes/results/Z/9x10x16_m920_Z.json",
        "schemes/results/Z/11x15x16_m1629_Z.json",
    ]:
        raw = subprocess.check_output(
            ["git", "-C", "data/FastMatrixMultiplication", "show", f"HEAD:{zf}"]
        )
        d = json.loads(raw)
        dims = tuple(sorted(d["n"]))
        zt_bound = table[dims]["ZT"]
        bt, be = count_bad(d)
        print(
            f"\n=== Unfolding {zf} (R={d['m']}, ZT_bound={zt_bound}, init_bad={bt}/{be}) ===",
            flush=True,
        )
        cur = run_c_opt(d, steps=10000, seed=1337, max_c=2)
        while cur["m"] < zt_bound - 1:
            cur, ok = unfold_once(cur)
            if not ok:
                break
            sp = try_split_to_zt(cur["u"], cur["v"], cur["w"], zt_bound)
            if sp is not None:
                U_zt, V_zt, W_zt = sp
                cur_zt = {"n": d["n"], "m": len(U_zt), "u": U_zt, "v": V_zt, "w": W_zt}
                cur_zt = run_c_opt(cur_zt, steps=100000, seed=1337, max_c=1)
                n1, n2, n3 = d["n"]
                fmt = f"{n1}x{n2}x{n3}"
                out_path = f"results/new_upgrades/{fmt}_m{cur_zt['m']}_ZT.json"
                with open(out_path, "w") as out_f:
                    json.dump(cur_zt, out_f, separators=(",", ":"))
                v_ok, msg = verify_scheme(out_path, table, sota)
                print(f"  >>> SUCCESS! {msg}", flush=True)
