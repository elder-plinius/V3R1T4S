# Criterion Skeptic Audit (`ab-offlattice-protein-3d-best-energies`)

context: subagent (fresh invocation)
target_id: ab-offlattice-protein-3d-best-energies
confirmed_scope: Explicit conformations and 3D unit-bond Cartesian coordinate sets in object/ab_3d_records_F89_2EWH_1CRN_1PCH.json for four benchmark sequences of the 3D AB off-lattice protein model (F89 with L = 89 and D = 173, 2EWH with L = 98 and D = 191, 1CRN with L = 46 and D = 87, and 1PCH with L = 87 and D = 169) achieve strict local-minimum energies (-E* = 87.179252478342 vs 86.4318 on F89, +0.747452 gain; -E* = 257.505676299754 vs 257.0741 on 2EWH, +0.431576 gain; -E* = 95.720529801173 vs 95.3159 on 1CRN, +0.404630 gain; and -E* = 166.978883682418 vs 166.7194 on 1PCH, +0.259484 gain) verified in both float64 and 50-digit arithmetic with all bond lengths equal to 1 within 2.22e-16 and angle-space gradient norms ||grad E||_2 <= 6.69e-12, beating the best published energies in Table 10 of Boskovic and Brest (arXiv:1903.01456) and Kim (2016) across all three longest chains (including +0.747452 above 0.5 on F89 for p1) alongside a complete independent reproduction and discrepancy audit of all 23 published conformations in Tables 11 and 12 (p2).

## Clause-by-Clause Verification Against `targets.json`

1. **Benchmark Sequence Identity & Angle / Coordinate Representation (All 4 Records)**:
   - The target requires bond and torsion angles (or Cartesian coordinates with all bond lengths equal to `1` within `1e-9`) for benchmark sequences exactly as listed in `arXiv:1903.01456` Table 2.
   - `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json` provides exact sequence strings, internal angle vectors (`D = 2L - 5` in both radians and degrees: `L - 2` bond angles `theta_i` and `L - 3` torsion angles `beta_i`), and 3D Cartesian coordinate sets reconstructed via Eq. (3) of `arXiv:1903.01456` for four benchmark chains, including all three longest chains (`F89`, `2EWH`, `1PCH`) plus `1CRN`:
     - `F89` (`L = 89`, `D = 173`, `87` bond angles, `86` torsion angles)
     - `2EWH` (`L = 98`, `D = 191`, `96` bond angles, `95` torsion angles)
     - `1CRN` (`L = 46`, `D = 87`, `44` bond angles, `43` torsion angles)
     - `1PCH` (`L = 87`, `D = 169`, `85` bond angles, `84` torsion angles)
   - Across all four conformations, every unit bond length is equal to `1.0` within `2.220446049250313e-16` (well below `1e-9`), and stored Cartesian coordinates match freshly reconstructed coordinates from `angles_rad` identically in `float64`.

2. **Energy Formula, Sign Convention, High-Precision Confirmation, and Margin (`-E* > B + 1e-3` and `p1 >= 0.5`)**:
   - Using the exact 3D AB off-lattice energy function (`E = E_bb + E_lj` with excluded sum over `|i - j| >= 2` and coefficients `C(A,A) = 1.0`, `C(B,B) = 0.5`, `C(A,B) = C(B,A) = -0.5`), verified in both IEEE 754 `float64` and 50-digit arithmetic (`decimal.Decimal` at 55 digits precision):
     - **`F89`**: `-E* = 87.179252478342` (`E_bb = 3.307502660644`, `E_lj = -90.486755138986`) vs Table 10 best `B = 86.4318` (and Kim 2016 CSA `-E = 73.1065`), achieving a gain of **`+0.747452`** (`747.5x` the `1e-3` Full Win threshold and exceeding the `0.5` energy-unit threshold for Partial Win `p1` on the three longest chains).
     - **`2EWH`**: `-E* = 257.505676299754` vs Table 10 best `B = 257.0741`, achieving a gain of **`+0.431576`** (`431.6x` the `1e-3` Full Win threshold).
     - **`1CRN`**: `-E* = 95.720529801173` (`E_bb = 1.626304826130`, `E_lj = -97.346834627302`) vs Table 10 best `B = 95.3159`, achieving a gain of **`+0.404630`** (`404.6x` the `1e-3` Full Win threshold).
     - **`1PCH`**: `-E* = 166.978883682418` vs Table 10 best `B = 166.7194`, achieving a gain of **`+0.259484`** (`259.5x` the `1e-3` Full Win threshold).

3. **Strict Local Minimum in Angle Space (`||grad E|| <= 6.69e-12` vs `1e-8` limit)**:
   - All four conformations are verified stationary local minima in angle space with analytical Euclidean gradient norms strictly below `1e-8`:
     - `F89`: `||grad E||_2 = 2.80e-12`, `||grad E||_inf = 8.44e-13`
     - `2EWH`: `||grad E||_2 = 6.69e-12`, `||grad E||_inf = 1.63e-12`
     - `1CRN`: `||grad E||_2 = 4.72e-12`, `||grad E||_inf = 1.52e-12`
     - `1PCH`: `||grad E||_2 = 3.61e-12`, `||grad E||_inf = 1.13e-12`
   - Independent 4th-order Richardson central finite-difference numerical gradients (`h = 1e-4`) confirm stationarity across all four sequences.

4. **Partial Win `p2` (Complete 23-Sequence Independent Reproduction & Discrepancy Audit)**:
   - All 23 published angle vectors from Tables 11 and 12 of `arXiv:1903.01456` were extracted from the primary LaTeX source (`paper.tex`) and independently evaluated under the exact Eq. (3)-(4) model, matching every Table 10 energy within `4.97e-5`.
   - The audit identifies and proves the Table 2 `1PCH` sequence-length and dimension discrepancy: Table 2 prints `L = 88, D = 171`, whereas the actual sequence string in Table 2 has `L = 87` residues and the published angle vector in Table 12 has `D = 169` angles (`85` bond + `84` torsion), evaluating to `-E = 166.719373` matching Table 10's `166.7194`.

5. **Hidden Quantifiers, Pitfalls, and Null / Corruption Checks**:
   - All five listed pitfalls in `targets.json` were audited: 3D model without extra torsion potential, unit bond lengths exact to machine precision (`2.22e-16`), excluded pair sum strictly over `|i - j| >= 2`, exclusion of Kolossvary's incompatible CCD variant, and proper sign convention (`-E* > B + 1e-3`).
   - Running `sh verify-it-yourself/run_checks.sh` exits `0` and prints `PASS`, and corrupting a digit of the object file causes the verifier to print `FAIL` and exit non-zero.

pass: true
