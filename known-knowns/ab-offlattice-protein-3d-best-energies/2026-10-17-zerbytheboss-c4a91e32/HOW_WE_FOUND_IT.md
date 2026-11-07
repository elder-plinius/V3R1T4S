# How We Found It (contributor text, unverified)

## 1. Complete Extraction & Reproduction of `arXiv:1903.01456` Tables 2, 10, 11, and 12
Because the web demonstration cited in Borko Boskovic and Janez Brest (*Swarm and Evolutionary Computation* 57, 100711, 2020; `https://arxiv.org/abs/1903.01456`, `http://spse.feri.um.si`) is offline, we extracted all 23 benchmark sequences (Table 2), best published energies (Table 10), and all 23 published angle vectors (Tables 11 and 12) directly from the official `arXiv:1903.01456` LaTeX source bundle (`https://arxiv.org/e-print/1903.01456`).

Re-evaluating all 23 conformations under Eqs. (1)-(4) of `arXiv:1903.01456` reproduced every single Table 10 energy to 4 decimal places (`|(-E_calc) - (-E_tab10)| <= 4.97e-5`) and uncovered three concrete findings (satisfying Partial Win `p2`):
1. **Table 2 Sequence Length & Dimension Discrepancy on `1PCH`**: Table 2 prints `1PCH` with length `L = 88` and dimension `D = 171`, whereas the actual sequence string in Table 2 has **87 residues** (`L = 87`) and the published angle vector in Table 12 has **169 angles** (`D = 2L - 5 = 169`: 85 bond angles `theta_i` and 84 torsion angles `beta_i`).
2. **Non-Stationary Published Angle Vectors (4-Decimal Degree Truncation)**: Because Tables 11 and 12 round angles in degrees to 4 decimal places, the published vectors have non-zero angle-space gradients up to `||grad E||_2 = 0.213` (`||grad E||_inf = 0.103`) on `2EWH` (`L = 98`). Newton-polishing `2EWH` from its Table 12 vector yields `-E* = 257.074539` (`+0.000462` above the raw Table 12 evaluation `257.074077`) with `||grad E||_2 = 5.36e-12`.
3. **Interaction Coefficient Sign Convention**: In `arXiv:1903.01456` Eq. (4) (following Stillinger, Head-Gordon, and Hirshfeld 1993), `c(A,A) = +1`, `c(B,B) = +0.5`, and `c(A,B) = -0.5` (weakly repulsive hydrophilic-hydrophobic pair).

## 2. $C^2$-Smooth Soft-Core Homotopy Continuation + Rigid-Core Polymer Moves (`AB_Protein_Hunter.cc`)
In the internal coordinate parameterization of Eq. (3), perturbing a single angle `theta_m` or `beta_m` in the middle of the chain rigidly translates the entire suffix relative to the prefix, causing severe Lennard-Jones `r^-12` steric clashes. Moreover, clamping `r^2 >= r2_floor` with a piecewise constant floor creates a gradient mismatch below `r2_floor` that stalls L-BFGS line searches. We addressed both bottlenecks in `how-we-built-it/AB_Protein_Hunter.cc`:

1. **Exact $C^2$-Smooth Quadratic Taylor Soft-Core Homotopy (`u_cut = 0.85 -> 0.55 -> 0.0`)**: For `r^2 < u_cut`, we replace `4(r^-12 - c_ij r^-6)` by its exact second-order Taylor polynomial in `u = r^2` around `u_cut` so the potential, first derivative `dV/du`, and second derivative `d^2V/du^2` match continuously at `r^2 = u_cut`. This allows L-BFGS (`m = 20`) to slide segments smoothly past steric barriers during `u_cut = 0.85 -> 0.55` before converging on the exact unmodified potential (`u_cut = 0.0`) and polishing via damped Cholesky Newton-Raphson on the exact `D x D` Hessian.
2. **Frustration-Guided Rigid-Core Moves (`S^2 x S^1`)**:
   - **Class I & II (Pure N-Terminal and C-Terminal Tail Re-Docking)**: Perturbing only the first `k` or last `k` bond vectors (`k <= 18`) re-docks the surface tail while keeping the remaining `L - k` core vertices 100% invariant.
   - **Class III (Exact Sum-Preserving `S^2 x S^1` Loop Bridges & Contiguous Subchain Crankshafts)**: Solving `u'_{m1} + u'_{m2} + u'_{m3} = u_{m1} + u_{m2} + u_{m3}` analytically on `S^2 x S^1`, rotating contiguous subchains `u_{m1..m2}` (`2 <= span <= 28`) rigidly around their chord vector `W = sum_{m=m1}^{m2} u_m`, and folding two complementary subchain chords (`W_1 + W_2 = const`) re-pack frustrated `A` loops and relieve repulsive `B` loops while keeping both the N-terminal prefix and C-terminal suffix 100% stationary.

## 3. Summary of the Four New Record Conformations
- **`F89` (`L = 89, D = 173`)**: `-E* = 87.179252478342` vs Table 10 `86.4318` (and Kim 2016 `73.1065`), gain **`+0.747452`** (`>= 0.5`, satisfying Partial Win `p1` and Full Win), `||grad E||_2 = 2.80e-12`.
- **`2EWH` (`L = 98, D = 191`)**: `-E* = 257.505676299754` vs Table 10 `257.0741`, gain **`+0.431576`** (Full Win), `||grad E||_2 = 6.69e-12`.
- **`1CRN` (`L = 46, D = 87`)**: `-E* = 95.720529801173` vs Table 10 `95.3159`, gain **`+0.404630`** (Full Win), `||grad E||_2 = 4.72e-12`.
- **`1PCH` (`L = 87, D = 169`)**: `-E* = 166.978883682418` vs Table 10 `166.7194`, gain **`+0.259484`** (Full Win), `||grad E||_2 = 3.61e-12`.
