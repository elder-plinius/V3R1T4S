# Criterion Audit (`ab-offlattice-protein-3d-best-energies`)

- Context: independent criterion audit
- Target: `ab-offlattice-protein-3d-best-energies`

## Clause-by-Clause Verification Against `targets.json`

1. **Benchmark Sequence Identity & Angle / Coordinate Representation (All 4 Records)**:
   - The target requires bond and torsion angles (or Cartesian coordinates with all bond lengths equal to `1` within `1e-9`) for benchmark sequences as listed in `arXiv:1903.01456` Table 2.
   - `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json` provides exact sequence strings, internal angle vectors (`D = 2L - 5` in both radians and degrees: `L - 2` bond angles `theta_i` and `L - 3` torsion angles `beta_i`), and 3D Cartesian coordinate sets reconstructed via Eq. (2) of `arXiv:1903.01456` Section 3 for four benchmark chains, including all three longest chains (`F89`, `2EWH`, `1PCH`) plus `1CRN`:
     - `F89` (`L = 89`, `D = 173`, `87` bond angles, `86` torsion angles)
     - `2EWH` (`L = 98`, `D = 191`, `96` bond angles, `95` torsion angles)
     - `1CRN` (`L = 46`, `D = 87`, `44` bond angles, `43` torsion angles)
     - `1PCH` (`L = 87`, `D = 169`, `85` bond angles, `84` torsion angles)
   - Across all four conformations, every unit bond length is equal to `1.0` within `2.220446049250313e-16` (well below `1e-9`), and stored Cartesian coordinates match freshly reconstructed coordinates from `angles_rad` identically in `float64`.

2. **Energy Formula, Sign Convention, High-Precision Confirmation, and Margin (`-E* > B + 1e-3` and `p1 >= 0.5`)**:
   - Using the 3D AB off-lattice energy function of `arXiv:1903.01456` Section 3, Eq. (1) (`E = E_bb + E_lj` with excluded sum over `|i - j| >= 2` and coefficients `c(A,A) = 1`, `c(B,B) = 1/2`, `c(A,B) = c(B,A) = -1/2`), verified in both IEEE 754 `float64` and 50-digit arithmetic (`decimal.Decimal` at 55 digits precision):
     - **`F89`**: `-E* = 87.179252478342` (`E_bb = 3.945563924209`, `E_lj = -91.124816402551`) vs Table 10 best `B = 86.4318` (and Kim 2016 CSA `-E = 73.1065`; note that Kim 2016 covers `F89` only and does not study `2EWH`, `1CRN`, or `1PCH`), achieving a gain of **`+0.747452`** (`747.5x` the `1e-3` Full Win threshold and exceeding the `0.5` energy-unit threshold for Partial Win `p1`).
     - **`2EWH`**: `-E* = 257.505676299754` (`E_bb = 9.236057908470`, `E_lj = -266.741734208224`) vs Table 10 best `B = 257.0741` (and Narloch & Parpinelli 2020 `257.3538`), achieving a gain of **`+0.431576`** over Table 10 (`+0.151876` over Narloch & Parpinelli 2020).
     - **`1CRN`**: `-E* = 95.720529801173` (`E_bb = 1.626304826130`, `E_lj = -97.346834627302`) vs Table 10 best `B = 95.3159`, achieving a gain of **`+0.404630`**.
     - **`1PCH`**: `-E* = 166.978883682418` (`E_bb = 5.537609970091`, `E_lj = -172.516493652509`) vs Table 10 best `B = 166.7194`, achieving a gain of **`+0.259484`**.

3. **Strict Local Minimum in Angle Space (`||grad E||_2 <= 6.688e-12` vs `1e-8` limit)**:
   - All four conformations are verified stationary local minima in angle space with analytical gradient norms matching across the object file and panel reports:
     - `F89`: `||grad E||_2 = 2.801e-12` (`2.80e-12`), `||grad E||_inf = 5.256e-13` (`5.26e-13`)
     - `2EWH`: `||grad E||_2 = 6.688e-12` (`6.69e-12`), `||grad E||_inf = 1.249e-12` (`1.25e-12`)
     - `1CRN`: `||grad E||_2 = 4.718e-12` (`4.72e-12`), `||grad E||_inf = 1.519e-12` (`1.52e-12`)
     - `1PCH`: `||grad E||_2 = 3.606e-12` (`3.61e-12`), `||grad E||_inf = 8.080e-13` (`8.08e-13`)
   - Independent 4th-order Richardson central finite-difference numerical gradients (`h = 1e-4`) confirm stationarity across all four sequences.

4. **Partial Win `p2` (Complete 23-Sequence Independent Reproduction & Discrepancy Audit)**:
   - All 23 published angle vectors from Tables 11 and 12 of `https://arxiv.org/abs/1903.01456` (`paper.tex` sha256 `997f641bd85f77f103e5d5c0c525cf47c71dad0030a25c571c22207647c0f769`) were evaluated under Eqs. (1)-(2) (`c(A,B) = -1/2`), matching every Table 10 `DE2P` energy within `4.38e-5`, with their SHA-256 digests and audit rows stored in `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json`.
   - The audit documents the Table 2 `1PCH` sequence-length and dimension discrepancy: Table 2 prints `L = 88, D = 171`, whereas the actual sequence string in Table 2 has `L = 87` residues and the published angle vector in Table 12 has `D = 169` angles (`85` bond + `84` torsion), evaluating to `-E = 166.719373` matching Table 10's `166.7194`.

5. **Hidden Quantifiers, Pitfalls, and Null / Corruption Checks**:
   - All five listed pitfalls in `targets.json` were audited: 3D model without extra torsion potential, unit bond lengths exact to machine precision (`2.22e-16`), excluded pair sum strictly over `|i - j| >= 2`, exclusion of Kolossváry's incompatible CCD variant, and proper sign convention (`-E* > B + 1e-3`).
   - Running `sh verify-it-yourself/run_checks.sh` exits `0` and prints `PASS`, and corrupting a digit of the object file causes the verifier to print `FAIL` and exit non-zero.

pass: true
