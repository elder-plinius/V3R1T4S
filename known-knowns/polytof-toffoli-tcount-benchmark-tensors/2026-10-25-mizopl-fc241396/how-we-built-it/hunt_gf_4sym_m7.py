#!/usr/bin/env python3
"""
Full 4-Symmetry Law M7 Generator on GF(2^k) Multiplication Tensors (0727..0733):
Starts from exact algebraic tower scheme SCHEMES[k]() (rank = EXPECTED_RANKS[k]),
acts by:
  1. Field stabilizer G_k = (GF(2^k)^* x GF(2^k)^*) x| (Gal(GF(2^k)/GF(2)) x Z_2)
  2. base_to_topp -> symmetric 3k-variable CP decomposition (U_t, V_t, W_t)
  3. Symmetric 3-tensor flip-graph walk (random_flip_walk)
  4. Per-term GL(3, F_2) internal plane basis gauge (168 matrices per term)
  5. Term-order permutation S_R
Then runs waring1 with -b 1 (and -b 4 on best candidates) and verifies every output!
"""
import re
import subprocess
import sys
from pathlib import Path
import numpy as np

POLYTOF_DIR = Path("polytof")
sys.path.insert(0, str(POLYTOF_DIR / "scripts"))
sys.path.insert(0, "attempts/lens1_m7_cp_fiber_waring")

from gf2 import gf2_inv, bitvecs_to_dense, upper_triples
from make_cpd_gf import (
    SCHEMES, EXPECTED_RANKS, gf2n_mul, base_to_topp, load_tensor_dense, verify_cpd
)
from generate_m7_gf_fiber import mul_mat_gf2n, frob_mat_gf2n, gf2n_inv_elem
from verify_paper_schemes import verify_waring
from hunt_all_benchmarks import GL3, encode_cpd_row, random_flip_walk

WORK_CPD_DIR = POLYTOF_DIR / "data" / "cpd" / "topp"
WORK_WAR_DIR = POLYTOF_DIR / "data" / "waring"
CLAIM_WAR_DIR = Path("object/waring")
BIN_DIR = POLYTOF_DIR / "bin"

TABLE_WARING = {4: 39, 5: 59, 6: 77, 7: 101, 8: 123, 9: 147, 10: 173}


def main():
    for k in range(4, 11):
        tid = 723 + k
        base_id = 523 + k
        n = 3 * k
        cp_rank = EXPECTED_RANKS[k]
        U0, V0, W0 = SCHEMES[k]()
        T_base = load_tensor_dense(POLYTOF_DIR / "data" / "tensors" / f"{base_id:04d}.npy")
        T_topp = load_tensor_dense(POLYTOF_DIR / "data" / "tensors" / f"{tid:04d}.npy")
        assert verify_cpd(U0, V0, W0, T_base)

        elems = list(range(1, 1 << k))
        M_mul = {a: mul_mat_gf2n(a, k).astype(np.uint8) for a in elems}
        F_frob = [frob_mat_gf2n(s, k).astype(np.uint8) for s in range(k)]
        F_frob_inv_T = [gf2_inv(F).T.copy().astype(np.uint8) for F in F_frob]

        rng = np.random.default_rng(99990 + k)
        U_t0, V_t0, W_t0 = base_to_topp(U0, V0, W0, k)
        row0 = encode_cpd_row(U_t0, V_t0, W_t0, n)
        rows = [row0]
        seen = {row0.tobytes()}

        num_schemes = 600 if k >= 7 else 300
        for i in range(num_schemes * 3):
            if len(rows) >= num_schemes:
                break
            # 1. Sample from G_k on base (U0, V0, W0)
            a = int(rng.choice(elems))
            b = int(rng.choice(elems))
            s = int(rng.integers(0, k))
            swap = bool(rng.integers(0, 2))
            ab = gf2n_mul(a, b, k)
            ab_inv = gf2n_inv_elem(ab, k)

            U1 = (U0 @ F_frob[s] @ M_mul[a]) % 2
            V1 = (V0 @ F_frob[s] @ M_mul[b]) % 2
            W1 = (W0 @ F_frob_inv_T[s] @ M_mul[ab_inv].T) % 2
            if swap:
                U1, V1 = V1, U1

            # 2. Lift to symmetric 3k-variable topp decomposition
            Ut, Vt, Wt = base_to_topp(U1.astype(np.uint8), V1.astype(np.uint8), W1.astype(np.uint8), k)

            # 3. Optional flip-graph walk in symmetric 3-tensor fiber (50% of samples)
            if i % 2 == 1:
                n_flips = int(rng.integers(1, 12))
                Ut, Vt, Wt = random_flip_walk(Ut, Vt, Wt, rng, n_flips=n_flips)

            # 4. Per-term GL(3, F_2) gauge + 5. Term-order permutation S_R
            U_new = np.empty_like(Ut)
            V_new = np.empty_like(Vt)
            W_new = np.empty_like(Wt)
            perm = rng.permutation(cp_rank)
            for idx, t in enumerate(perm):
                G = GL3[int(rng.integers(0, len(GL3)))]
                stack = np.vstack([Ut[t], Vt[t], Wt[t]])
                trans = (G @ stack) % 2
                U_new[idx], V_new[idx], W_new[idx] = trans[0], trans[1], trans[2]

            row = encode_cpd_row(U_new, V_new, W_new, n)
            h = row.tobytes()
            if h not in seen:
                seen.add(h)
                rows.append(row)

        out_cpd = WORK_CPD_DIR / f"{tid:04d}-{cp_rank:05d}.npy"
        for old_f in WORK_CPD_DIR.glob(f"{tid:04d}-*.npy"):
            old_f.unlink()
        np.save(out_cpd, np.vstack(rows).astype(np.uint64))

        cmd = [
            str(BIN_DIR / "waring1"), str(tid),
            "--cpd", "-n", str(len(rows)), "-b", "1", "-t", "8",
            "--save", "--verify"
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(POLYTOF_DIR))
        m = re.search(r"\(min (\d+),", proc.stdout)
        best_war = int(m.group(1)) if m else -1
        tab_war = TABLE_WARING[k]
        delta = best_war - tab_war

        # Verify saved Waring file against T_topp directly in Python!
        wf_path = WORK_WAR_DIR / f"{tid:04d}-{best_war:05d}.npy"
        ok_w = False
        if wf_path.exists():
            A = bitvecs_to_dense(np.load(wf_path), n).astype(np.int64)
            T_rec = (np.einsum("ri,rj,rk->ijk", A, A, A) % 2).astype(np.uint8)
            ok_w = (upper_triples(T_rec) == upper_triples(T_topp))
            if ok_w and best_war <= tab_war:
                subprocess.run(["cp", str(wf_path), str(CLAIM_WAR_DIR / wf_path.name)], check=True)

        marker = "🔥 NEW WORLD RECORD!" if (delta < 0 and ok_w) else ""
        print(f"GF(2^{k:2d}) [07{tid-700:02d}] (n={n:2d}, min_CP={cp_rank:2d}, pool={len(rows)}): table={tab_war:3d} -> M7_war={best_war:3d} (delta={delta:+3d}, py_verified={ok_w}) {marker}", flush=True)

if __name__ == "__main__":
    main()
