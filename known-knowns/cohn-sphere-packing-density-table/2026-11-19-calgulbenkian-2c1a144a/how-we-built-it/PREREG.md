# Pre-Registration (`2026-11-19-0630-cohn-d19-nonisometric-p1-v2`)

preregistered_utc: 2026-11-19T06:49:39Z
target_id: cohn-sphere-packing-density-table
claim_tier: partial_win p1 (dimension n = 19, inside 10 through 31)
null_test: not needed because exact deductive rational algebraic certificate verified deterministically without statistical or distributional claims

## 1. Explicit Amended-Scope Revision Note (`LESSONS.md #3` & `Rule 3`)
This `v2` run succeeds held run `2026-11-19-0120-cohn-sphere-packing-hunt` (which remains untouched under `Rule 3`). In Round `1`, `REPRODUCE` (`pass: true`) and `NOVELTY` (`pass: true`) passed, while `CRITERION` (`HELD_FOR_REVISION`) confirmed that the `6`-translate `Orbit II` packing in `R^19` satisfies all `bank/targets.json` partial win `p1` requirements, and held the package solely because the linear Jacobian rank checks (`95/95` and `285/285`) prove **bilateral bar-framework contact-Jacobian rank** (`0`-dimensional kissing-stratum vertex isolation) rather than unilateral Farkas positive-stress hard-sphere collective jamming (Salvatore Torquato and Frank H. Stillinger `2001`; Aleksandar Donev, Salvatore Torquato, Frank H. Stillinger, and Robert Connelly `2004`). Per `CRITERION` Section `4.3` Option `1` and `LESSONS.md #3`, this pre-registration freezes the exact corrected mathematical scope before generating `v2` outputs and staging `v2/claim/`.

## 2. Frozen Acceptance Criteria for Partial Win `p1` (`P19_II_vtx` vs `P19_ChenHuLiWangWu2025_ref`)
Both independent zero-floating-point exact rational verifiers (`verify_packing_c99.c` in strict ISO C99 with `-Wall -Wextra -Werror -Wpedantic -mgeneral-regs-only` and `verify_packing_py.py` in Python standard library `fractions.Fraction`) must independently verify from scratch and print verbatim:

1. **Ambient Leech Lattice & Positive Calibration**:
   - Reconstruct/verify the `4096`-codeword extended binary Golay code `G_24` and `24 x 24` unimodular Leech lattice basis `leech_B` (`det(Lambda_24) = 1`).
   - Positive calibration on `E_8`: `det = 1`, `min_sq = 2`, `kissing = 240`, `center_density = 1/16`.
2. **Exact Dimension `19`, Leech Saturation, Minimal Distance `52/15`, and Record Center Density**:
   - Rank-`5` section `A_sec` (`det(K) = 300`) and orthogonal rank-`19` complement `B_lll` (`B_lll * A_sec^T = 0`, `B_lll * B_lll^T = 8 * G`, `det(G) = 300`, exact rational `R^T * D * R = G` with positive pivots).
   - **Integer saturation in `Lambda_24` (`leech_sat = 1`)**: integer Leech-coordinate matrices `Y_A` (`Y_A * leech_B = A_sec`) and `Y_B` (`Y_B * leech_B = B_lll`) admit certified integer right-inverses (`Y_A * Z_A = I_5`, `Y_B * Z_B = I_19`, Smith Normal Form invariant factors all `1`), proving `K_II, L_II, K_I, L_I` are saturated sublattices of `Lambda_24` with `L_II = K_II^perp cap Lambda_24` and `L_I = K_I^perp cap Lambda_24`.
   - Exhaustive zero-floating-point Fincke–Pohst enumeration over `L` (`min_sq = 4`) and all `15` unordered pairs among the `6` primitive translates (`0` vectors strictly below `52/15`, global `min_sq = 52/15`), yielding exact squared center density:
     `1461920290375446110677 / 184736485004425048828125 == (3^(-9) * 5^(-21/2) * 13^(19/2))^2`.
3. **Basis-Free, Supercell-Free Euclidean Non-Isometry, Non-Subsumption, and Bilateral Kissing-Stratum Vertex Isolation**:
   - **Intrinsic maximal translation group (`sym_trans_stab_size = 1`)**: verify `(c_i + c_s) mod Z^19` preserves `{c_0, ..., c_5} mod Z^19` ONLY for `s = 0` on both packings, proving `Sym_trans(P19_II_vtx) = L_II` and `Sym_trans(P19_ChenHuLiWangWu2025_ref) = L_I` as unstructured Euclidean point sets, paired with `norm4(L_II) = 6858 != 6942 = norm4(L_I)` (distinct `Co_0`-orbits in `Lambda_24`).
   - **Strictly disjoint point kissing numbers & slide non-reachability**: `P19_II_vtx` has `tau_sorted = (4022, 4022, 4072, 4072, 4072, 4072)` (`min = 4022`, `max = 4072`, `avg = 12166/3`, `tight_pairs = 8/15`, `triangles = 2`, `connected = 1`), whereas `P19_ChenHuLiWangWu2025_ref` has `tau_sorted = (4110, 4110, 4110, 4110, 4110, 4110)` (`min = 4110`, `max = 4110`, `avg = 4110/1`, `tight_pairs = 6/15`, `triangles = 2`, `connected = 0`), with `max(tau_new) = 4072` strictly below `min(tau_ref) = 4110` (ruling out any rigid motion or coset slide of `P19_ChenHuLiWangWu2025_ref`, where every sphere retains `tau ≥ 4110`).
   - **Full bilateral bar-framework contact-Jacobian rank (`0`-dimensional kissing-stratum vertex)**: `P19_II_vtx` has `bilateral_contact_rank_trans = 95/95` (`bilateral_contact_nullity_trans = 0`) and `bilateral_contact_rank_full = 285/285` (`bilateral_contact_nullity_full = 0`), isolating `P19_II_vtx` as a `0`-dimensional vertex of its `12,166`-contact kissing-graph stratum, whereas `P19_ChenHuLiWangWu2025_ref` has `bilateral_contact_rank_trans = 76/95` (`bilateral_contact_nullity_trans = 19`) and `bilateral_contact_rank_full = 266/285` (`bilateral_contact_nullity_full = 19`).
   - **Explicit non-claim**: unilateral Farkas positive-stress hard-sphere collective jamming (`omega^T J_trans = 0, omega strictly positive`) is NOT claimed, because receding along `-u_int / 1860` detaches the `100` one-sided cross-cluster contacts back into `Orbit II`'s open `19`-dimensional rattle cavity over `L_II`.
4. **Negative Controls**:
   - Built-in perturbed translate test and CLI `--corrupt` / middle-digit corruption test must be rejected (`rc = 1`, final line `FAIL`).
