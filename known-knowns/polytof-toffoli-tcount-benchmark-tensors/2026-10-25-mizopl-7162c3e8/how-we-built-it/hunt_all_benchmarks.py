#!/usr/bin/env python3
"""
Law M7 Full-Suite CP-Fiber + Flip-Graph + Waring Hunter across ZIB-IOL/polytof benchmarks.
"""
import glob
import os
import re
import subprocess
import sys
import time
from pathlib import Path
import numpy as np

POLYTOF_DIR = Path("polytof")
sys.path.insert(0, str(POLYTOF_DIR / "scripts"))

from gf2 import (
    apply_inverse_transform,
    bitvecs_to_dense,
    gf2_inv,
    load_tensor_dense,
    upper_triples,
)
from verify_paper_schemes import compute_bco_tensor, verify_cpd, verify_waring

TENSORS_DIR = POLYTOF_DIR / "data" / "tensors"
PAPER_CPD_DIR = POLYTOF_DIR / "data" / "paper" / "cpd" / "topp"
PAPER_WAR_DIR = POLYTOF_DIR / "data" / "paper" / "waring"
PAPER_TRANS_DIR = POLYTOF_DIR / "data" / "paper" / "transform"

WORK_CPD_DIR = POLYTOF_DIR / "data" / "cpd" / "topp"
WORK_WAR_DIR = POLYTOF_DIR / "data" / "waring"
BIN_DIR = POLYTOF_DIR / "bin"

def save_dense_as_triples(n, T_dense, out_path):
    """Save dense symmetric (n, n, n) tensor as (nnz+1, 3) int64 .npy file."""
    triples = sorted(upper_triples(T_dense))
    arr = np.zeros((len(triples) + 1, 3), dtype=np.int64)
    arr[0] = [n, n, n]
    if triples:
        arr[1:] = np.array(triples, dtype=np.int64)
    np.save(out_path, arr)

def decode_cpd_row(row, n):
    vec_words = (n + 63) // 64
    rank = len(row) // (3 * vec_words)
    all_vecs = bitvecs_to_dense(row.reshape(3 * rank, vec_words), n).astype(np.uint8)
    return all_vecs[0::3].copy(), all_vecs[1::3].copy(), all_vecs[2::3].copy()

def encode_cpd_row(U, V, W, n):
    vec_words = (n + 63) // 64
    rank = U.shape[0]
    out = np.zeros((3 * rank, vec_words), dtype=np.uint64)
    for idx, M in enumerate([U, V, W]):
        for w in range(vec_words):
            b0 = w * 64
            b1 = min(n, b0 + 64)
            width = b1 - b0
            if width > 0:
                shifts = np.arange(width, dtype=np.uint64)
                out[idx::3, w] = (M[:, b0:b1].astype(np.uint64) << shifts).sum(axis=1)
    return out.ravel()

# Precompute all 168 invertible 3x3 binary matrices in GL(3, F_2)
GL3 = []
for m in range(1, 512):
    G = np.array([[(m >> (3*i + j)) & 1 for j in range(3)] for i in range(3)], dtype=np.uint8)
    # det over GF(2)
    det = (
        G[0,0]*(G[1,1]*G[2,2] ^ G[1,2]*G[2,1])
        ^ G[0,1]*(G[1,0]*G[2,2] ^ G[1,2]*G[2,0])
        ^ G[0,2]*(G[1,0]*G[2,1] ^ G[1,1]*G[2,0])
    ) & 1
    if det == 1:
        GL3.append(G)

def plane_basis_with_p(u, v, w, p_vec):
    """Given 3-plane span(u,v,w) containing nonzero p_vec, return basis (p_vec, b2, b3)."""
    vecs = [u, v, w, u ^ v, u ^ w, v ^ w, u ^ v ^ w]
    for b2 in vecs:
        if not np.array_equal(b2, p_vec):
            for b3 in vecs:
                if not np.array_equal(b3, p_vec) and not np.array_equal(b3, b2) and not np.array_equal(b3, p_vec ^ b2):
                    return p_vec.copy(), b2.copy(), b3.copy()
    return u.copy(), v.copy(), w.copy()

def random_flip_walk(U, V, W, rng, n_flips=15):
    """Perform n_flips valid symmetric 3-tensor flip moves on (U, V, W)."""
    U, V, W = U.copy(), V.copy(), W.copy()
    rank = U.shape[0]
    for _ in range(n_flips):
        # Map each nonzero vector in each 3-plane to term index
        vec_to_terms = {}
        for t in range(rank):
            u, v, w = U[t], V[t], W[t]
            for vec in (u, v, w, u ^ v, u ^ w, v ^ w, u ^ v ^ w):
                h = vec.tobytes()
                vec_to_terms.setdefault(h, []).append((t, vec))
        shared = [items for items in vec_to_terms.values() if len(items) >= 2]
        if not shared:
            break
        choice = shared[int(rng.integers(0, len(shared)))]
        idx1, idx2 = rng.choice(len(choice), size=2, replace=False)
        t1, p_vec = choice[idx1]
        t2, _ = choice[idx2]
        if t1 == t2:
            continue
        p1, b1, c1 = plane_basis_with_p(U[t1], V[t1], W[t1], p_vec)
        p2, b2, c2 = plane_basis_with_p(U[t2], V[t2], W[t2], p_vec)
        # Flip: (p, b1, c1) + (p, b2, c2) = (p, b1^b2, c1) + (p, b2, c1^c2)
        if rng.integers(0, 2) == 0:
            U[t1], V[t1], W[t1] = p1, b1 ^ b2, c1
            U[t2], V[t2], W[t2] = p2, b2, c1 ^ c2
        else:
            U[t1], V[t1], W[t1] = p1, b1, c1 ^ c2
            U[t2], V[t2], W[t2] = p2, b1 ^ b2, c2
    return U, V, W

def generate_m7_cpd_pool(tid, work_id, n, T_bco, num_schemes=200):
    cpd_matches = sorted(glob.glob(str(PAPER_CPD_DIR / f"{tid:04d}-*.npy")))
    if not cpd_matches:
        return None
    cpd_path = Path(cpd_matches[0])
    rank = int(cpd_path.stem.split("-")[1])
    raw = np.load(cpd_path)
    U0, V0, W0 = decode_cpd_row(raw[0], n)

    rng = np.random.default_rng(1000 + tid)
    rows = [raw[0].copy()]
    seen = {raw[0].tobytes()}

    cur_U, cur_V, cur_W = U0.copy(), V0.copy(), W0.copy()
    for i in range(num_schemes * 2):
        if len(rows) >= num_schemes:
            break
        # Either walk from current or reset to U0,V0,W0
        if i % 5 == 0:
            cur_U, cur_V, cur_W = U0.copy(), V0.copy(), W0.copy()
        cur_U, cur_V, cur_W = random_flip_walk(cur_U, cur_V, cur_W, rng, n_flips=int(rng.integers(1, 12)))

        # Apply random GL(3, F_2) per term and random term permutation
        U_new = np.empty_like(cur_U)
        V_new = np.empty_like(cur_V)
        W_new = np.empty_like(cur_W)
        perm = rng.permutation(rank)
        for idx, t in enumerate(perm):
            G = GL3[int(rng.integers(0, len(GL3)))]
            stack = np.vstack([cur_U[t], cur_V[t], cur_W[t]])  # (3, n)
            trans = (G @ stack) % 2
            U_new[idx], V_new[idx], W_new[idx] = trans[0], trans[1], trans[2]

        row = encode_cpd_row(U_new, V_new, W_new, n)
        h = row.tobytes()
        if h not in seen:
            seen.add(h)
            rows.append(row)

    WORK_CPD_DIR.mkdir(parents=True, exist_ok=True)
    out_cpd = WORK_CPD_DIR / f"{work_id:04d}-{rank:05d}.npy"
    np.save(out_cpd, np.vstack(rows).astype(np.uint64))
    return rank, len(rows), out_cpd

def main():
    transform_files = sorted(PAPER_TRANS_DIR.glob("*.npy"))
    tids = [int(f.stem) for f in transform_files]
    print(f"Found {len(tids)} tensors in data/paper/transform/")

    improvements = []
    for tid in tids:
        n, T_bco = compute_bco_tensor(tid)
        if n is None or n > 90:
            # Skip very large n>90 in quick pass (handle separately)
            continue
        war_matches = sorted(glob.glob(str(PAPER_WAR_DIR / f"{tid:04d}-*.npy")))
        if not war_matches:
            continue
        paper_war = int(Path(war_matches[0]).stem.split("-")[1])

        work_id = tid + 3000
        save_dense_as_triples(n, T_bco, TENSORS_DIR / f"{work_id:04d}.npy")

        res = generate_m7_cpd_pool(tid, work_id, n, T_bco, num_schemes=150)
        if res is None:
            continue
        cp_rank, n_pool, _ = res

        wbin = "waring1" if n <= 64 else "waring2"
        cmd = [
            str(BIN_DIR / wbin), str(work_id),
            "--cpd", "-n", str(n_pool), "-b", "1", "-t", "8",
            "--save", "--verify"
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(POLYTOF_DIR))
        m = re.search(r"\(min (\d+),", proc.stdout)
        if not m:
            continue
        new_war = int(m.group(1))
        delta = new_war - paper_war
        marker = "🔥 RECORD!" if delta < 0 else ""
        print(f"tid={tid:04d} (n={n:2d}, CP={cp_rank:2d}): paper_war={paper_war:3d} -> M7_war={new_war:3d} (delta={delta:+3d}) {marker}", flush=True)
        if delta < 0:
            improvements.append((tid, n, cp_rank, paper_war, new_war, delta, work_id))

    print("\n=== SUMMARY OF IMPROVEMENTS ===")
    for item in improvements:
        tid, n, cp_rank, paper_war, new_war, delta, work_id = item
        print(f"  tid={tid:04d} (n={n:2d}, CP={cp_rank:2d}): {paper_war} -> {new_war} ({delta:+d})")

if __name__ == "__main__":
    main()
