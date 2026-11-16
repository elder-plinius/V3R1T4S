# Constructive Architecture for `n = 1 (mod 4)` Maximal Determinant Records

## 1. Three Constructive Mechanisms

1. **Asymmetric 4-Block Circulant Goethals-Seidel Cores + Singly 3-Normalized `[OS-1]` Border + 2-Column `Schur-4` Alignment (`n = 93, 97, 105, 109, 117`):**
   - For `m = n - 1 = 4k` (`k in {23, 24, 26, 27, 29}`), four circulant generator rows `(v_A, v_B, v_C, v_D)` in `{-1, +1}^k` satisfying `PAF_A(s) + PAF_B(s) + PAF_C(s) + PAF_D(s) = 0` (`s != 0`) without restricting `A` to be symmetric (`A^T != A`) populate the Goethals-Seidel array `H_m` with `H_m H_m^T = m I_m`.
   - Selecting a row triplet `(r_0, r_1, r_2)` and normalizing columns by `w_j = H_{r_0, j} H_{r_1, j} H_{r_2, j}` maps the triplet onto the four `[OS-1]` border rows of order `n = m + 1` with initial normalized determinant `(2k + ||H_m w||_1 / 4) * (2k)^(2k - 1)`.
   - Aligning zero-excess rows and climbing on the 2-column border Schur complement (`n = 93, 97, 109, 117`) or unfrozen Sherman-Morrison cofactor ascent (`n = 105`, reaching `7413 * 26^50`) produces strictly larger determinants than the 2003-2005 records.

2. **Closed-Four `4 x k` Hadamard Switching + `[OS-1]` Triplet Border (`n = 81, 89`):**
   - Starting from the archived order-80 Hadamard core (`n = 81`) and the Kronecker product `Paley(43) x H_2` of order 88 (`n = 89`), switching closed-four `4 x k` subarrays moves across Hadamard equivalence classes while preserving `H_m H_m^T = m I_m`, unlocking higher triplet excess `||H_m w||_1` and yielding `200 * 20^39` (`n = 81`) and `226 * 22^43` (`n = 89`, also providing an explicit `89 x 89` witness where the archived catalog carried none).

3. **Doubly 3-Normalized `[OS-2]` Core + Coupled Rank-2 Unfreezing (`n = 101`):**
   - Simultaneously 3-normalizing a row triplet and a column triplet of a switched `H_100` core into `4 x (n - 4)` and `(n - 4) x 4` borders followed by rank-2 Sherman-Morrison updates lifts `D_norm(101)` from `7110 * 25^48` to `7626 * 25^48` (`+7.2574%`, ratio `0.860635` of Barba's bound).

## 2. Bit-Exact Reproducibility

Every record entry in `object/hadamard_maxdet_8_records.json` embeds its exact `generator_params` (`vA..vD` or `core_hex`, `triplet`, `flipped_rows`, `flipped_cols`, `sparse_flips`). Running `python3 how-we-built-it/reconstruct_all_8_records.py` (and `verify-it-yourself/verify.py`) reconstructs all 8 matrices bit-for-bit and verifies Hadamard orthogonality of every order-`(n-1)` core.
