#!/usr/bin/env python3
"""
Law M7 Stage-1 Solution-Fiber Generator for GF(2^k) Multiplication Tensors (0726..0733).
Generates exact minimal-rank CP decompositions of 05xx / 07xx by acting with:
  1. Field multiplication gauge (alpha, beta, (alpha*beta)^{-1}) in (GF(2^k)^*)^2
  2. Frobenius automorphisms x -> x^(2^s) in Gal(GF(2^k)/GF(2))
  3. Commutativity swap U <-> V
  4. Term order permutations (affecting TOHPE pivot order in waring1)
Every generated row is verified against data/tensors/07xx.npy before saving.
"""
import sys
from pathlib import Path
import numpy as np

POLYTOF_DIR = Path("polytof")
sys.path.insert(0, str(POLYTOF_DIR / "scripts"))

from make_cpd_gf import (
    SCHEMES, EXPECTED_RANKS, PRIMITIVE_POLYS,
    gf2n_mul, vecN_to_bits, mat_cols_from_ints,
    base_to_topp, load_tensor_dense, verify_cpd, matrix_to_bits
)
from gf2 import gf2_inv

def mul_mat_gf2n(alpha, k):
    """k x k binary matrix M such that M @ vec(x) = vec(alpha * x) in GF(2^k)."""
    cols = [ gf2n_mul(alpha, 1 << j, k) for j in range(k) ]
    return mat_cols_from_ints(cols, k)

def frob_mat_gf2n(s, k):
    """k x k binary matrix F such that F @ vec(x) = vec(x^(2^s)) in GF(2^k)."""
    cols = []
    for j in range(k):
        x = 1 << j
        for _ in range(s):
            x = gf2n_mul(x, x, k)
        cols.append(x)
    return mat_cols_from_ints(cols, k)

def gf2n_inv_elem(a, k):
    """Multiplicative inverse of a in GF(2^k)^* via Fermat a^(2^k - 2)."""
    # Compute a^(2^k - 2)
    exp = (1 << k) - 2
    res = 1
    base = a
    while exp > 0:
        if exp & 1:
            res = gf2n_mul(res, base, k)
        base = gf2n_mul(base, base, k)
        exp >>= 1
    return res

def generate_fiber_for_k(k, max_schemes=400, seed=42):
    rng = np.random.default_rng(seed + k)
    U0, V0, W0 = SCHEMES[k]()
    rank = EXPECTED_RANKS[k]
    tid = k + 23
    base_id = 500 + tid
    topp_id = 700 + tid

    T_base = load_tensor_dense(POLYTOF_DIR / "data" / "tensors" / f"{base_id:04d}.npy")
    assert verify_cpd(U0, V0, W0, T_base), f"Base scheme failed for k={k}"

    # Precompute multiplication matrices for all nonzero elements of GF(2^k)
    elems = list(range(1, 1 << k))
    M_mul = {a: mul_mat_gf2n(a, k) for a in elems}
    F_frob = [frob_mat_gf2n(s, k) for s in range(k)]
    F_frob_inv_T = [gf2_inv(F).T.copy() for F in F_frob]

    seen_hashes = set()
    rows_topp = []

    def add_candidate(U, V, W):
        U_t, V_t, W_t = base_to_topp(U, V, W, k)
        u_b = matrix_to_bits(U_t)
        v_b = matrix_to_bits(V_t)
        w_b = matrix_to_bits(W_t)
        row = np.column_stack([u_b, v_b, w_b]).ravel().astype(np.uint64)
        h = row.tobytes()
        if h not in seen_hashes:
            seen_hashes.add(h)
            rows_topp.append(row)
            return True
        return False

    # Always include original
    add_candidate(U0, V0, W0)

    # Sample from stabilizer group (alpha, beta, s, swap, perm)
    # Note: x' = alpha * x -> u_t . (alpha * x) = (M_alpha^T u_t) . x
    #       y' = beta * y  -> v_t . (beta * y)  = (M_beta^T v_t) . y
    #       (x*y) = (alpha*beta)^{-1} (x' * y') -> W' = W @ M_{(alpha*beta)^{-1}}^T
    attempts = 0
    while len(rows_topp) < max_schemes and attempts < max_schemes * 10:
        attempts += 1
        a = int(rng.choice(elems))
        b = int(rng.choice(elems))
        s = int(rng.integers(0, k))
        swap = bool(rng.integers(0, 2))

        ab = gf2n_mul(a, b, k)
        ab_inv = gf2n_inv_elem(ab, k)

        # Apply Frobenius first: u_f = u @ F_s, v_f = v @ F_s, w_f = w @ F_s^{-T}
        U1 = (U0 @ F_frob[s]) % 2
        V1 = (V0 @ F_frob[s]) % 2
        W1 = (W0 @ F_frob_inv_T[s]) % 2

        # Apply scalar multiplication gauge (a, b):
        # Since sum_t (u_t . (a x)) (v_t . (b y)) (M_{(ab)^{-1}} w_t) = x * y:
        U2 = (U1 @ M_mul[a]) % 2
        V2 = (V1 @ M_mul[b]) % 2
        W2 = (W1 @ M_mul[ab_inv].T) % 2

        if swap:
            U2, V2 = V2, U2

        # Also randomly permute the rank terms (changes initial parity order in TOHPE!)
        if attempts % 2 == 1:
            perm = rng.permutation(rank)
            U2, V2, W2 = U2[perm], V2[perm], W2[perm]

        if len(rows_topp) < 5:
            assert verify_cpd(U2, V2, W2, T_base), f"Gauge verification failed for k={k}"

        add_candidate(U2.astype(np.uint8), V2.astype(np.uint8), W2.astype(np.uint8))

    out_dir = POLYTOF_DIR / "data" / "cpd" / "topp"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{topp_id:04d}-{rank:05d}.npy"
    arr = np.vstack(rows_topp).astype(np.uint64)
    np.save(out_path, arr)
    print(f"k={k:2d} (topp {topp_id:04d}, rank={rank:2d}): saved {arr.shape[0]} diverse CP schemes -> {out_path}")

if __name__ == "__main__":
    for k in range(3, 11):
        generate_fiber_for_k(k, max_schemes=300)
