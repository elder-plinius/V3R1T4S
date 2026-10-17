# V3R1T4S Reproduction Panel Audit (`reproduce.md`)

context: subagent (fresh invocation)
target_id: ab-offlattice-protein-3d-best-energies
cells: F89, 2EWH, 1CRN, 1PCH
claimed_values: 87.179252 (F89), 257.505676 (2EWH), 95.720530 (1CRN), 166.978884 (1PCH)
table_values: 86.4318 (F89), 257.0741 (2EWH), 95.3159 (1CRN), 166.7194 (1PCH)

## 1. Quoted Mathematical Definition (`arXiv:1903.01456`, Eqs. 1-4)

An independent checker was implemented directly from the mathematical specification in Borko Boskovic and Janez Brest (*"Two-phase protein folding optimization on a three-dimensional AB off-lattice model"*, *Swarm and Evolutionary Computation* 57, 100711, 2020; `arXiv:1903.01456`, Section 2, Eqs. 1-4):

- **Internal-to-Cartesian Coordinate Reconstruction (Eq. 1 / Eq. 3)**:
  For a chain of $L$ monomers parameterized by $D = 2L - 5$ internal angles $(\theta_1, \dots, \theta_{L-2}, \beta_1, \dots, \beta_{L-3})$:
  $$
  (x_i, y_i, z_i) = \begin{cases}
  (0, 0, 0), & i = 1 \\
  (0, 1, 0), & i = 2 \\
  (\cos\theta_1, 1 + \sin\theta_1, 0), & i = 3 \\
  (x_{i-1} + \cos\theta_{i-2}\cos\beta_{i-3}, \; y_{i-1} + \sin\theta_{i-2}\cos\beta_{i-3}, \; z_{i-1} + \sin\beta_{i-3}), & 4 \le i \le L
  \end{cases}
  $$
- **Potential Energy Function (Eqs. 2-4)**:
  $$
  E = \frac{1}{4}\sum_{i=1}^{L-2} (1 - \cos\theta_i) + 4 \sum_{i=1}^{L-2}\sum_{j=i+2}^{L} \left(r_{ij}^{-12} - c(\sigma_i, \sigma_j) r_{ij}^{-6}\right)
  $$
  where $r_{ij}$ is the Euclidean distance between monomers $i$ and $j$, and the hydrophobicity coupling coefficients (Eq. 4) are:
  $$
  c(\sigma_i, \sigma_j) = \begin{cases}
  +1, & \sigma_i = A \text{ and } \sigma_j = A \\
  +0.5, & \sigma_i = B \text{ and } \sigma_j = B \\
  -0.5, & \sigma_i \neq \sigma_j
  \end{cases}
  $$

## 2. Independent Verification Results on `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json`

1. **File Integrity & `INDEX.csv` Verification**:
   - All four rows in `INDEX.csv` (`F89`, `2EWH`, `1CRN`, `1PCH`) reference `object/ab_3d_records_F89_2EWH_1CRN_1PCH.json` with exact SHA-256 match `336da9346dec169b689fb5bc566e176e2ced799e2fef9ab48c37a3c834b92333`.

2. **Independent `float64`, 50-Digit `mpmath`, Bond-Length, Gradient, and Hessian Audit across All 4 Record Conformations**:

| Sequence | $L$ | $D = 2L-5$ | Table 10 $-E$ | `float64` $-E^*$ | 50-Digit `mpmath` $-E^*$ | Gain over Table 10 | $\|\nabla E\|_2$ | $\|\nabla E\|_\infty$ | Max Bond Error | Hessian $\lambda_{\min} \dots \lambda_{\max}$ (Positive) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **`F89`** | `89` | `173` | `86.4318` | `87.179252478342` | `87.17925247834215775929917` | **`+0.747452`** | `2.794e-12` | `5.219e-13` | `2.220e-16` | `0.108278 .. 10932.858` (`173/173`) |
| **`2EWH`** | `98` | `191` | `257.0741` | `257.505676299754` | `257.5056762997540005028914` | **`+0.431576`** | `6.711e-12` | `1.249e-12` | `2.220e-16` | `0.148501 .. 35935.038` (`191/191`) |
| **`1CRN`** | `46` | `87` | `95.3159` | `95.720529801173` | `95.72052980117251738956962` | **`+0.404630`** | `4.704e-12` | `1.519e-12` | `2.220e-16` | `0.170707 .. 8930.076` (`87/87`) |
| **`1PCH`** | `87` | `169` | `166.7194` | `166.978883682418` | `166.9788836824178105973791` | **`+0.259484`** | `3.613e-12` | `8.102e-13` | `2.220e-16` | `0.133384 .. 23621.799` (`169/169`) |

   - **Energy Component Splits (`float64`)**:
     - `F89`: $E_{\text{bb}} = 3.945563924209$, $E_{\text{LJ}} = -91.124816402551$, $E^* = -87.179252478342$ (`|float64 - mp50| = 1.222e-13`).
     - `2EWH`: $E_{\text{bb}} = 9.236057908470$, $E_{\text{LJ}} = -266.741734208224$, $E^* = -257.505676299754$ (`|float64 - mp50| = 1.995e-13`).
     - `1CRN`: $E_{\text{bb}} = 1.626304826130$, $E_{\text{LJ}} = -97.346834627302$, $E^* = -95.720529801173$ (`|float64 - mp50| = 7.261e-14`).
     - `1PCH`: $E_{\text{bb}} = 5.537609970091$, $E_{\text{LJ}} = -172.516493652509$, $E^* = -166.978883682418$ (`|float64 - mp50| = 2.194e-13`).
   - **Coordinate Reconstruction & Unit Bond Lengths**:
     - For all four sequences, reconstructing Cartesian coordinates from `angles_rad` matches the stored `coordinates_xyz` with maximum coordinate deviation `0.0`, and all $L - 1$ bond lengths equal `1.0` within `2.220446049250313e-16` (well below `1e-9`).
   - **Stationarity & Strict Local Minima**:
     - Every conformation satisfies $\|\nabla E\|_2 \le 6.711 \times 10^{-12}$ and $\|\nabla E\|_\infty \le 1.519 \times 10^{-12}$ (well below `1e-8`), with every eigenvalue of the $D \times D$ angle-space Hessian matrix strictly positive ($\lambda_{\min} \ge 0.108278$).
   - **Gain Margins**:
     - All four conformations beat Table 10 of `arXiv:1903.01456` by margins between `+0.259484` and `+0.747452` (`259.5x` to `747.5x` the `1e-3` Full Win threshold), and `F89` (`L = 89`) exceeds the `0.5` threshold (`+0.747452` over Table 10's `86.4318` and `+14.072752` over Kim 2016's `73.1065`) for Partial Win `p1`.

3. **Exhaustive 23-Sequence Reproduction & `1PCH` Discrepancy Audit (Partial Win `p2`)**:
   - Independently re-evaluating all 23 published angle vectors from Tables 11 and 12 in `arXiv_1903_01456_reproduction_audit` confirms every Table 10 energy within `4.375216e-5` (under `5e-5`).
   - Confirmed the Table 2 vs Table 12 discrepancy for `1PCH`: the actual sequence string in Table 2 has length $L_{\text{actual}} = 87$ (printed as $L = 88$ in Table 2) and the published angle vector in Table 12 has $D_{\text{actual}} = 2(87) - 5 = 169$ angles (printed as $D = 171$ in Table 2), evaluating to `-E = 166.719373` (matching Table 10's `166.7194`).

## 3. Execution of `verify-it-yourself/run_checks.sh`

Running `sh verify-it-yourself/run_checks.sh` from the package root exited with code `0` and output:
```text
Verified F89  (L=89, D=173): -E* = 87.179252478342 (Tab10=86.4318, gain=+0.747452, ||g||_2=2.80e-12, bond_err=2.22e-16)
Verified 2EWH (L=98, D=191): -E* = 257.505676299754 (Tab10=257.0741, gain=+0.431576, ||g||_2=6.69e-12, bond_err=2.22e-16)
Verified 1CRN (L=46, D= 87): -E* = 95.720529801173 (Tab10=95.3159, gain=+0.404630, ||g||_2=4.72e-12, bond_err=2.22e-16)
Verified 1PCH (L=87, D=169): -E* = 166.978883682418 (Tab10=166.7194, gain=+0.259484, ||g||_2=3.61e-12, bond_err=2.22e-16)
Verified all 23 arXiv:1903.01456 Table 11/12 conformations + 1PCH L=87/D=169 discrepancy.
PASS
```

pass: true
