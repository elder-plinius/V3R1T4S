# How We Found It (contributor text, unverified)

## 1. Exact Calibration & 780-Point-File Audit (`Zn`, `Cd`, `Pb`, `Pb_Gupta.rar`, `Na_Gupta`)
We first calibrated the Cleri-Rosato / Gupta second-moment tight-binding potential (`E = sum_i [ sum_{j!=i} A exp(-p(r_ij/r0 - 1)) - xi sqrt(sum_{j!=i} exp(-2q(r_ij/r0 - 1))) ]` with `r0 = 1` in reduced coordinates) across all 780 posted point files downloaded from the Cambridge Cluster Database (`https://www-wales.ch.cam.ac.uk/~wales/CCD/Gupta.html`):
- **Zinc (`Zn`, `N = 3..125`, 123 files, Doye *PRB* 68, 195418, 2003)**: `p = 9.689`, `q = 4.602`, `A = 0.1477 eV`, `xi = 0.8900 eV`. Every posted point file reproduces its 6-decimal CCD table energy within `4.984e-7 eV < 1e-5 eV`.
- **Cadmium (`Cd`, `N = 3..125`, 123 files, Doye *PRB* 68, 195418, 2003)**: `p = 10.612`, `q = 5.206`, `A = 0.1420 eV`, `xi = 0.8117 eV`. Every posted point file reproduces its 6-decimal CCD table energy within `4.955e-7 eV < 1e-5 eV`.
- **Lead (`Pb`, `N = 3..150`, 148 table files + 9 `Pb_Gupta.rar` improvement files, Doye *Comp. Mater. Sci.* 35, 227, 2006)**: `p = 9.576`, `q = 3.648`, `A = 0.0980 eV`, `xi = 0.9140 eV`. Every posted point file reproduces its 6-decimal table energy within `4.998e-7 eV` (and the 8-decimal `Pb_Gupta.rar` energies within `4.75e-9 eV`).
- **Sodium (`Na_Gupta`, `N = 3..379`, 377 files, Li et al. *PRB* 57, 15519, 1998; Noya et al. *EPJD* 43, 57, 2007)**: `p = 10.130`, `q = 1.300`, `A = 0.0159554019 eV`, `xi = 0.2911347198 eV`. Every posted point file reproduces its 6-decimal CCD table energy within `7.165e-7 eV < 1e-5 eV`.

## 2. Multi-Threaded Top-6 Tournament Solver (`how-we-built-it/Gupta_Cluster_Hunter.cc`)
In the divalent hcp metals `Zn` (`p = 9.689, q = 4.602`) and `Cd` (`p = 10.612, q = 5.206`), clusters in the `N = 70..110` regime exhibit strong competition between decahedral, icosahedral, and close-packed polytetrahedral motifs (Doye, *PRB* 68, 195418, 2003). We built a self-contained C++17 multi-threaded solver (`how-we-built-it/Gupta_Cluster_Hunter.cc`) combining three structural operators with a two-stage L-BFGS tournament (150-iteration coarse screen across all candidates in parallel, followed by 2,000-iteration deep relaxation of the top 6 candidates):
1. **Cross-Potential Seeding**: Relaxing all known `Zn`, `Cd`, `Pb`, `Co`, `Na_Gupta`, `Na_MM`, `Ag`, `Mo`, and `Fe` cluster geometries at size `N` under each metal's Gupta potential.
2. **Downward Single-Atom and Surface-Pair Etching (`N+1 -> N` and `N+2 -> N`)**: Removing each atom `i in 0..N` from the best `N+1` parent, and removing pairs `(i, j)` among the 22 weakest-bound surface atoms from the best `N+2` parent:
   - Etching 1 atom from `Cd_107` discovered **`Cd_106`** (`E* = -123.0018760970 eV` vs CCD `-123.000416 eV`, `-0.001460 eV`), and cross-seeding / etching from `Zn_107` discovered the corresponding **`Zn_106`** global minimum (`E* = -141.9309047390 eV` vs CCD `-141.928489 eV`, `-0.002416 eV`).
   - Etching surface atom pair `(88, 92)` from `Cd_96` (`N+2 -> N`) discovered **`Cd_94`** (`E* = -109.0494558230 eV` vs CCD `-109.048698 eV`, `-0.000758 eV`).
3. **Upward Surface Hollow-Site Growth (`N-1 -> N`)**: Placing an adatom over each 3-atom surface triangle (`r_ij, r_ik, r_jk <= 1.38 r_0`) at outward normal height `0.80 r_0`:
   - Growing 1 atom onto `Cd_70` discovered **`Cd_71`** (`E* = -82.3022257380 eV` vs CCD `-82.302019 eV`, `-0.000207 eV`).
   - Growing 1 atom onto `Cd_83` discovered **`Cd_84`** (`E* = -97.4196981104 eV` vs CCD `-97.415006 eV`, `-0.004692 eV`).

## 3. Exact Analytical $3N \times 3N$ Hessian Newton Polishing (Float64 + 55-Digit Decimal)
Each of the 5 discovered structures was polished using the exact analytical $3N \times 3N$ Gupta Hessian pseudoinverse (projecting out the 6 rigid-body translational and rotational zero modes) in `float64` (`||grad E||_2 <= 2.43e-14`) followed by three preconditioned Newton steps in 55-digit `decimal.Decimal` arithmetic (`||grad E||_2 <= 6.58e-35`), and verified to have exactly 6 near-zero rigid-body modes (`|lambda| <= 3.88e-15 < 1e-6`) and `3N - 6` strictly positive vibrational eigenvalues (`lambda_min >= 0.0388 > 0`).
