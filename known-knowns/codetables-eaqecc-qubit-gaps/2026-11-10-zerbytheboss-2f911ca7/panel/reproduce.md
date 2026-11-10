# Skeptic Panel — REPRODUCE

- context: fresh research subagent invoked with zero solver history (role: REPRODUCE)
- target_id: `codetables-eaqecc-qubit-gaps`
- object_checked: `object/eaqecc_n19_k2_d11_c9.tsv` (`sha256: 2f911ca7172f460d9a52d48419b462874d7f001334806b9d68c8a7f0d54eba42`)

## 1. Quoted Mathematical Criterion (`KNOWN`)

From the `codetables-eaqecc-qubit-gaps` target specification:

> "Success means, for a cell with c >= 1, an explicit stabilizer matrix S over GF(2) in symplectic form, with n-k+c rows and 2n columns (the standard EA representation), such that an independent script verifies (1) GF(2)-rank of S is n-k+c, (2) the symplectic Gram matrix S Omega S^T has GF(2)-rank exactly 2c (so exactly c ebits are needed), and (3) the EA minimum distance d, defined as in the table (minimum symplectic weight of a vector in the symplectic dual of rowspace(S) that is not in rowspace(S) ∩ its symplectic dual), is computed EXACTLY by full enumeration; and d is STRICTLY GREATER (direction: max) than d_lower for (n,k,c) in http://www.codetables.de/EAQECC/qubit.php re-fetched live immediately before claiming, with d <= d_upper."

## 2. Independent Verification of `object/eaqecc_n19_k2_d11_c9.tsv` From `S` Alone (`PROVED-HERE`)

Before trusting any stored `DUAL` rows or package checker logic, an independent Python 3.9.6 standard-library bitmask verifier (`python3 -B -c '...'`, writing zero files) parsed only the `26` `S` rows of `object/eaqecc_n19_k2_d11_c9.tsv` (`38` binary columns `[x_0..x_18 | z_0..z_18]` for `n = 19`) and computed every invariant from scratch:

1. **File Integrity & Dimensions (`PROVED-HERE`)**:
   - `object/eaqecc_n19_k2_d11_c9.tsv` has SHA-256 `2f911ca7172f460d9a52d48419b462874d7f001334806b9d68c8a7f0d54eba42`, matching `INDEX.csv`.
   - `S` has exact shape `26 x 38` with all entries in `{0, 1}`.
2. **`GF(2)` Stabilizer Rank (`PROVED-HERE`)**:
   - `rank_GF2(S) = 26 = n - k + c` (`19 - 2 + 9 = 26`).
3. **Symplectic Gram Matrix Rank & Ebit Count (`PROVED-HERE`)**:
   - With `Omega = [[0, I_19], [I_19, 0]]` over `GF(2)` and symplectic bilinear form `(u, v)_s = popcount((u_x & v_z) ^ (u_z & v_x)) mod 2`, the `26 x 26` matrix `G = S * Omega * S^T` has zero diagonal, is symmetric (`skew-symmetric` over `GF(2)`), and satisfies `rank_GF2(S * Omega * S^T) = 18 = 2c`, confirming `c = 9 >= 1` ebits and `k = n - rank_GF2(S) + c = 19 - 26 + 9 = 2` logical qubits.
4. **Independent Symplectic Dual `S^{perp_s}` (`PROVED-HERE`)**:
   - Computing `nullspace_GF2([Z | X])` directly from `S` alone produces a `12`-dimensional basis of `S^{perp_s}` (`2n - rank_GF2(S) = 38 - 26 = 12`, spanning `2^12 = 4,096` vectors).
   - Cross-check against stored `DUAL` rows (`12 x 38`): `rank_GF2(DUAL) = 12`, every stored `DUAL` row is symplectically orthogonal to all `26` rows of `S`, and `rank_GF2(indep_dual union DUAL) = 12` (`DUAL` matches the RREF nullspace basis row-for-row).
5. **Exhaustive `4,096`-Vector Enumeration of `S^{perp_s}` (`PROVED-HERE`)**:
   - Testing membership in `rowspace(S)` via reduction against `RREF(S)` across all `2^12 = 4,096` vectors of `S^{perp_s}` yields:
     - **Isotropic radical `S cap S^{perp_s}` (`2^8 = 256` vectors)** symplectic weight enumerator:
       `[(0, 1), (4, 6), (8, 21), (10, 12), (12, 48), (14, 84), (16, 60), (18, 24)]` (sum `= 256`, minimum nonzero weight `= 4`, attained on two disjoint 4-qubit supports `(4, 14, 17, 18)` and `(9, 10, 12, 13)`).
     - **Logical cosets `S^{perp_s} \ S` (`4,096 - 256 = 3,840` vectors)** symplectic weight enumerator:
       `[(11, 192), (12, 528), (13, 408), (14, 1152), (15, 552), (16, 528), (17, 360), (18, 96), (19, 24)]` (sum `= 3,840`, minimum symplectic weight `d_EA = 11`, attained by `192` vectors across `64` distinct 11-qubit supports; explicit weight-11 witness: Pauli string `ZYZZIYZIXXYIXIIIXII` on support `[0, 1, 2, 3, 5, 6, 8, 9, 10, 12, 16]`).
   - Because `min_{v in (S cap S^{perp_s}) \ {0}} wt_s(v) = 4 < 11 = d_EA`, the code is strictly degenerate (`d(S^{perp_s}) = 4` while `d_EA = 11 > 10 = d_lower(19, 2, 9)`, `11 <= 17 = d_upper(19, 2, 9)`).
   - **MacWilliams Identity Cross-Check (`PROVED-HERE`)**: Applying the quaternary/symplectic MacWilliams transform `(1/4096) * W_{S^{perp_s}}(x + 3y, x - y)` yields exact integer dual counts `B_0 = 1, B_1 = 0, B_2 = 0, B_3 = 6, B_4 = 213, ..., B_19 = 305733` summing to `67,108,864 = 2^26`, with `B_w >= |Radical_w|` for every `w in 0..19` and confirming via direct search that `rowspace(S)` contains zero weight-1 and zero weight-2 Paulis (not a trivial ancilla lengthening of `n < 19`).
6. **`GF(4)`-Linearity & Griesmer Bound Audit (`PROVED-HERE`)**:
   - Under `w`-multiplication `(x | z) -> (z | x ^ z)` in the normal basis `{w, w^2}` of `GF(4)`, `rowspace(S)`, `S^{perp_s}`, and `S cap S^{perp_s}` are closed, with `S[2i + 1] == mul_w(S[2i])` for all `i = 0..12`.
   - Independent standard polynomial-basis `GF(4)` verification confirms `D_4 = phi^{-1}(S)` has `rank_GF4(D_4) = 13`, its Hermitian dual `C_4 = D_4^{perp_h}` has `dim_GF4(C_4) = 6`, `rank_GF4(C_4 * C_4^dagger) = 2`, Hermitian hull `Hull_h(C_4) = C_4 cap D_4` has `dim_GF4 = 4`, and direct enumeration of all `4^6 = 4,096` codewords in `GF(4)^19` reproduces the identical hull and coset weight enumerators.
   - For classical (non-degenerate) `[n', k', 11]_4` hull ancestors with `n' = k + c + 2l' = 11 + 2l'` and `k' = k + l' = 2 + l'`, the `GF(4)` Griesmer lower bound `g_4(k', d) = sum_{i=0}^{k'-1} ceil(d / 4^i)` gives:
     - `l' = 0` (`[11, 2, 11]_4`): `g_4(2, 11) = 11 + 3 = 14 > 11` (infeasible; max classical Griesmer `d = 8`).
     - `l' = 1` (`[13, 3, 11]_4`): `g_4(3, 11) = 11 + 3 + 1 = 15 > 13` (infeasible; max classical Griesmer `d = 9`).
     - `l' = 2` (`[15, 4, 11]_4`): `g_4(4, 11) = 11 + 3 + 1 + 1 = 16 > 15` (infeasible; max classical Griesmer `d = 10`).
     - `l' = 3` (`[17, 5, 11]_4`): `g_4(5, 11) = 17 <= 17`; `l' = 4` (`[19, 6, 11]_4`): `g_4(6, 11) = 18 <= 19`.
   - Coset-projection averaging over `H_0'` additionally excludes degenerate quaternary ancestors at `l' in {0, 1}`, and `README.md`, `RUN_IT_YOURSELF.md`, `verify-it-yourself/check_eaqecc.py`, and `verify-it-yourself/RECEIPTS.md` accurately qualify the Griesmer check across `l' in {0, 1, 2}` as ruling out all classical (non-degenerate) quaternary hull ancestors.

## 3. Audit of `verify-it-yourself/check_eaqecc.py`, `run_checks.sh`, `RECEIPTS.md`, `RUN_IT_YOURSELF.md`, and `how-we-built-it/search_gf4_hull.c`

1. **`verify-it-yourself/check_eaqecc.py` & `how-we-built-it/PREREG.md` (`PROVED-HERE`)**:
   - `check_eaqecc.py` contains no hardcoded pass, no tautology, and no sampling shortcut. `evaluate_stabilizer(S, 19)` computes `S^{perp_s}` from `S` alone via `gf2_rref([Z | X])`, tests `rowspace(S)` membership via `gf2_rref(S)`, and enumerates all `2^12 = 4,096` dual vectors without consulting `D_stored`, matching the frozen criterion in `how-we-built-it/PREREG.md` (`frozen_utc: 2026-11-10T18:50:00Z`).
   - Built-in single-bit perturbation (`S_corrupt[0][0] ^= 1`) yields `rk_s = 26`, `rk_g = 18`, `cross_orth = False`, and `d_pert = 8 < 11`, which is rejected even by `S`-only distance evaluation.
2. **Read-Only Re-Run of `sh verify-it-yourself/run_checks.sh` (`PROVED-HERE`)**:
   - Executed from the package root; exited with status `0` in under `1` second and printed:
     ```text
     Negative control rejected single-bit stabilizer perturbation (cross_orth=False, d_pert=8).
     Verified S shape = 26 x 38, rank_GF2(S) = 26, rank_GF2(S Omega S^T) = 18 => n=19, k=2, c=9.
     Enumerated all 2^12 = 4096 vectors in S^{perp_s}: |S cap S^{perp_s}| = 256 (min nonzero radical weight = 4), |S^{perp_s} \ S| = 3840.
     Coset weight distribution: [(11, 192), (12, 528), (13, 408), (14, 1152), (15, 552), (16, 528), (17, 360), (18, 96), (19, 24)]
     Exact non-catalytic d_EA = 11 > 10 = d_lower(19, 2, 9) (degenerate EAQECC: d_EA = 11 > 4 = d(S^{perp_s})); Griesmer bound rules out all l' in {0, 1, 2} classical (non-degenerate) quaternary hull ancestors.
     PASS
     ```
   - Programmatic string comparison confirmed **100% byte-for-byte parity** between this live stdout, `verify-it-yourself/RECEIPTS.md`, and the expected output block in `RUN_IT_YOURSELF.md` (resolving the prior repair-round documentation discrepancy).
3. **Line-by-Line Audit of `how-we-built-it/search_gf4_hull.c` (`PROVED-HERE` / `NUMERICAL`)**:
   - Normal-basis arithmetic (`0=0, 1=w, 2=w^2, 3=1=w+w^2`), `herm_ip` (`t0 = Tr(u*conj(v))`, `t1 = Tr(w*u*conj(v))`, `a = t1, b = t0 ^ t1`), and trace-symplectic weight/orthogonality identities are algebraically exact (`PROVED-HERE`).
   - `apply_unitary` implements exact `U(19, GF(4))` transvections (`wt(g)` even, `lam = 1`) and reflections (`wt(g)` odd, `lam in {w, w^2}`), preserving `(u, v)_h` identically (`PROVED-HERE`).
   - `C^{perp_h}` coset moves enforce even weight and `!in_gf4_span(l, ...)` on hull generators `0..l-1` and verify `gf4_gram_rank == k` on `W` generators `l..K-1`, preserving `dim_GF4(Hull_h(C)) = 4`; every candidate `cur_pen == 0` is gated by `verify_binary_eaqecc` (standalone binary RREF, Gram rank `2c`, and `4,096`-vector dual enumeration) (`PROVED-HERE`).
   - Pure-memory Python execution of the `search_gf4_hull.c` algorithm from seed `0x243f6a8885a308d3` independently reached `cur_pen = 0, d_EA = 11` on restart `rep = 0` (`step = 19,002`) (`NUMERICAL`).

pass: true
