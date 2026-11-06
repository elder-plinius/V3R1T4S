# Panelist Report: CRITERION (`ccd-binary-gupta-nanoalloys-38-55`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
problem_id: ccd-binary-gupta-nanoalloys-38-55
evaluated_artifacts:
  - claim/CLAIM.md
  - claim/REPRODUCE.md
  - claim/Cu39Ag16_improved.txt (6,149 bytes, sha256: 92ac099b6963dcaedd5dbc1000731a5a87c99fc6e208b30475c6850e420a991d)
  - claim/Cu34Ag21_improved.txt (6,150 bytes, sha256: 1802a8519f28bed64f8712ee414f461870b9c1cf00c97c3698e0eb289548874e)
  - claim/Cu33Ag22_improved.txt (6,149 bytes, sha256: e942c06011a9b969ec8d701b228b58c66dcd1837d7cf11d5a82760bc6d3354dd)
  - claim/Cu31Ag24_improved.txt (6,147 bytes, sha256: c229315ab3d778e5da4a7329879fde3d0117a94fdf1b0331b9216f3bb6acc4ee)
  - claim/Cu22Ag33_improved.txt (6,149 bytes, sha256: 677fe021a76ddcc4e3b254721ac87f8c3b2369f0518c64f7a73380b5b1f28037)
  - claim/Cu20Ag35_improved.txt (6,146 bytes, sha256: 0e1f6e7fd59b164c8c4e53ec3cd00d00722ed69f57abe3e862b0f4399781c712)
  - claim/Cu15Ag40_improved.txt (6,147 bytes, sha256: 18d181026f1f06416e1d11561a5539917b463d2184843b9a56c6fa4b9c9ab60a)
  - claim/Cu17Ag38_improved.txt (6,148 bytes, sha256: a72814de42efed463752f9092af0c3b77b1ed48f9543e6a4b2e717d620ce025b)
  - claim/cuag55_improvements_summary.tsv (1,557 bytes, sha256: a8ca7d24a8df4e0e541d3af82dee1ba378391e009312c243d393af4c68d534d0)
  - claim/CuAg_55.rar (67,636 bytes, sha256: c6cdc7b61eddf14da78c752368618679836f24f40c1a17c84f47230e210d01dd)
  - claim/CCD.html (15,051 bytes, sha256: 9662d9a7fcf599815e22d6dae7fbdeac8b71cf7892f836284f2d0769383183c8)
  - claim/published_Cu39Ag16.txt (2,620 bytes, sha256: 9a9bd8253ea858b8b93171f3b6b0c311c1a3970f1c53b673efb814f2b6830f08)
  - claim/author_checker_bingupta_check.py (13,637 bytes, sha256: 2b73c482228b87c3662a84ad3ba8a078e18d332a93ad17d86b6b03032c803368)
confirmed_scope: Eight certified 55-atom Cu_n Ag_{55-n} Gupta nanoalloy local minima in claim/ headlined by claim/Cu39Ag16_improved.txt (6,149 bytes, sha256 92ac099b6963dcaedd5dbc1000731a5a87c99fc6e208b30475c6850e420a991d, E* = -163.8021426482 eV vs archive -162.6122982488 eV, dE = -1.18984440 eV) along with claim/Cu34Ag21_improved.txt (-0.95474003 eV), claim/Cu33Ag22_improved.txt (-0.92199695 eV), claim/Cu31Ag24_improved.txt (-0.79798867 eV), claim/Cu22Ag33_improved.txt (-0.23167311 eV), claim/Cu20Ag35_improved.txt (-0.12881511 eV), claim/Cu15Ag40_improved.txt (-0.12624733 eV), and claim/Cu17Ag38_improved.txt (-0.06457801 eV), calibrated across all 56 files of claim/CuAg_55.rar to 4.890e-09 eV (within the 1e-6 eV tolerance), polished in 30-digit mpmath to gradient norm at most 6.34e-23 (below the 1e-10 threshold), verified by 165x165 analytical Hessians with 6 zero modes (magnitude at most 2.51e-15, below 1e-6) and 0 negative eigenvalues, and separated from the polished archive structures by at least 0.06457801 eV (above the 1e-4 eV threshold).

---

## 1. Clause-by-Clause Audit Against Verbatim `success_criterion`

### Clause (1): Explicit 3D coordinates and species labels for one system and composition listed in a CCD archive
- **Requirement:** Explicit coordinates and species labels for one system and composition listed in a CCD archive (e.g., $\text{Cu}_n\text{Ag}_{55-n}$ in `claim/CuAg_55.rar`).
- **Verification:** Independently parsed `claim/Cu39Ag16_improved.txt` (`6,149` bytes, `sha256: 92ac099b6963dcaedd5dbc1000731a5a87c99fc6e208b30475c6850e420a991d`) and the 7 additional improved files (`claim/Cu34Ag21_improved.txt` through `claim/Cu17Ag38_improved.txt`). Every file contains exactly $N = 55$ 30-digit Cartesian coordinate rows with explicit integer species labels `0` ($\text{Cu}$) and `1` ($\text{Ag}$) matching the target $(n_{\text{Cu}}, n_{\text{Ag}})$ composition (`(39, 16)` in `claim/Cu39Ag16_improved.txt`, `(34, 21)`, `(33, 22)`, `(31, 24)`, `(22, 33)`, `(20, 35)`, `(15, 40)`, and `(17, 38)`).
- **Verdict:** **SATISFIED.**

### Clause (2): Exact Gupta parameter set calibrated across every file in the archive to `1e-6 eV`
- **Requirement:** Under the exact Gupta parameter set used for that archive, the checker reproduces the header energies of every file in that archive to $10^{-6}\text{ eV}$ from coordinates.
- **Verification:** Extracted all 56 composition files `Cu0Ag55.txt` through `Cu55Ag0.txt` plus `reference.txt` from `claim/CuAg_55.rar` (`67,636` bytes, `sha256: c6cdc7b61eddf14da78c752368618679836f24f40c1a17c84f47230e210d01dd`). Using the exact Nunez & Johnston (2010) / Rapallo et al. (2005) parameters cited in `reference.txt`:
  - $\text{Cu-Cu}$ ($t=0$): $A = 0.0894\text{ eV}$, $\xi = 1.2799\text{ eV}$, $p = 10.550$, $q = 2.430$, $r_0 = 2.556\text{ \AA}$
  - $\text{Cu-Ag}$ ($t=1$): $A = 0.0980\text{ eV}$, $\xi = 1.2274\text{ eV}$, $p = 10.700$, $q = 2.805$, $r_0 = 2.72405\text{ \AA}$
  - $\text{Ag-Ag}$ ($t=2$): $A = 0.1031\text{ eV}$, $\xi = 1.1895\text{ eV}$, $p = 10.850$, $q = 3.180$, $r_0 = 2.8921\text{ \AA}$
  Every single file (`56/56`) reproduces its 8-decimal-place header energy with:
  $$\max_{0 \le k \le 55} |E_{\text{eval}} - E_{\text{header}}| = 4.890410 \times 10^{-9}\text{ eV} \le 10^{-6}\text{ eV}, \qquad \text{mean } |E_{\text{eval}} - E_{\text{header}}| = 2.069747 \times 10^{-9}\text{ eV}.$$
- **Verdict:** **SATISFIED** (calibration error is $204\times$ below the $10^{-6}\text{ eV}$ tolerance, matching 8-decimal-place header rounding).

### Clause (3): $E^*$ strictly lower by at least $10^{-4}\text{ eV}$ than the archive evaluation AND published literature
- **Requirement:** $E^*$ is strictly lower by at least $10^{-4}\text{ eV}$ than the checker's evaluation of the archive structure for that composition and than any published value for the same system, parameters, and composition.
- **Verification:** On headline `Cu39Ag16`:
  - Archive `claim/published_Cu39Ag16.txt` header energy: `-162.61229825 eV`
  - Archive coordinate evaluation (`float64`): `-162.6122982488 eV`
  - Improved structure `claim/Cu39Ag16_improved.txt` energy (`mp.dps = 30`): $E^* = -163.8021426482357908139108\text{ eV}$
  - Improvement margin: $\Delta E = -1.18984440\text{ eV}$, which exceeds the $10^{-4}\text{ eV}$ threshold by a factor of $11,898\times$.
  Across all 8 improved compositions in `claim/`, $\Delta E$ ranges from $-1.18984440\text{ eV}$ (`Cu39Ag16`) to $-0.06457801\text{ eV}$ (`Cu17Ag38`), exceeding the $10^{-4}\text{ eV}$ threshold by $645\times$ to $11,898\times$. None of the benchmark papers (Lai et al. 2011, Wu & Cheng 2014, Rondina & Da Silva 2013, Du et al. 2019, Nunez & Johnston 2010) or citing literature report lower energies for 55-atom $\text{Cu}_n\text{Ag}_{55-n}$ under this Gupta potential.
- **Verdict:** **SATISFIED.**

### Clause (4): Certified local minimum (30-digit `mpmath` gradient norm below `1e-10` and `165x165` Hessian spectrum)
- **Requirement:** Polish in `float128` or `mpmath` (30 digits) to gradient norm below $10^{-10}$, then the $3N \times 3N$ Hessian in double precision has6 near-zero modes ($|\lambda|$ below $10^{-6}$) and no negative eigenvalue.
- **Verification:** Evaluating the saved 30-digit coordinates directly in `mpmath` (`mp.dps = 30`) and computing the exact $165 \times 165$ analytical Hessian in `float64` (cross-checked against central finite differences on `claim/Cu39Ag16_improved.txt` with $\max |H_{\text{ana}} - H_{\text{fd}}| = 2.881 \times 10^{-9}\text{ eV/\AA}^2$):

| Composition | $E^*\text{ (eV, mp30)}$ | $\|\nabla E^*\|_{\text{f64}}$ | $\|\nabla E^*\|_{\text{mp30}}$ | Zero Modes | $\max |\lambda_{\text{zero}}|$ | Neg. Modes | $\lambda_7\text{ (eV/\AA}^2\text{)}$ | $\lambda_{165}\text{ (eV/\AA}^2\text{)}$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Cu39Ag16` | `-163.8021426482` | `1.647e-14` | `2.167e-28` | `6` | `2.514e-15` | `0` | `0.699916` | `22.696578` |
| `Cu34Ag21` | `-161.7669248647` | `1.734e-14` | `6.343e-23` | `6` | `2.429e-15` | `0` | `0.714086` | `21.115277` |
| `Cu33Ag22` | `-161.3533666177` | `1.743e-14` | `4.520e-23` | `6` | `2.343e-15` | `0` | `0.733798` | `20.639062` |
| `Cu31Ag24` | `-160.4928597284` | `1.494e-14` | `1.556e-26` | `6` | `2.449e-15` | `0` | `0.729365` | `20.618256` |
| `Cu22Ag33` | `-156.6167469937` | `1.568e-14` | `7.038e-26` | `6` | `2.040e-15` | `0` | `0.779003` | `18.546874` |
| `Cu20Ag35` | `-155.6983965417` | `1.416e-14` | `4.528e-24` | `6` | `2.166e-15` | `0` | `0.777510` | `17.772748` |
| `Cu15Ag40` | `-153.6251235752` | `1.463e-14` | `2.893e-28` | `6` | `2.408e-15` | `0` | `0.241364` | `21.577011` |
| `Cu17Ag38` | `-154.4653492657` | `1.567e-14` | `2.572e-28` | `6` | `1.298e-15` | `0` | `0.250397` | `23.031566` |

- **Verdict:** **SATISFIED** (30-digit gradient norms are at least $12$ orders of magnitude below $10^{-10}$, and all 8 Hessians have `6` translational/rotational zero modes and `159` strictly positive eigenvalues).

### Clause (5): Distinct-basin check (polishing the archive structure gives energy at least `1e-4 eV` higher)
- **Requirement:** Polishing the archive structure gives an energy at least $10^{-4}\text{ eV}$ higher than $E^*$.
- **Verification:** Relaxing `claim/published_Cu39Ag16.txt` with L-BFGS-B in `float64` followed by 30-digit `mpmath` Newton polishing yields $E_{\text{arch,pol}} = -162.6122982487926334833406\text{ eV}$ (changing from the raw coordinate evaluation by only $-2.7 \times 10^{-12}\text{ eV}$), leaving a distinct-basin separation of $1.1898443994\text{ eV} \ge 10^{-4}\text{ eV}$ above $E^*$. Across all 8 compositions, polishing the archive structure changes its energy by less than $10^{-9}\text{ eV}$, preserving the full improvement margins of $0.06457801\text{ eV}$ to $1.18984440\text{ eV}$.
- **Verdict:** **SATISFIED.**

---

## 2. Null Model & Perturbation Controls

To confirm that `claim/Cu39Ag16_improved.txt` is a genuine chemical-ordering and geometric optimum rather than an artifact:
1. **Random-homotop null model (`400` random permutations of `39` Cu and `16` Ag on the fixed geometry of `claim/Cu39Ag16_improved.txt`):**
   - Minimum energy among 400 random homotops: `-159.12289926 eV`
   - Median energy: `-153.48600704 eV`; maximum energy: `-145.53851229 eV`
   - All `400/400` random homotops lie strictly above $E^* = -163.80214265\text{ eV}$ by at least $4.67924339\text{ eV}$.
2. **Exhaustive single-pair $\text{Cu}\leftrightarrow\text{Ag}$ exchange neighborhood ($39 \times 16 = 624$ neighbors of `claim/Cu39Ag16_improved.txt`):**
   - **Unrelaxed fixed-geometry swaps:** Minimum energy across all `624` single-pair exchanges is `-163.39966345 eV`; `624/624` are strictly higher than $E^*$ by at least $0.40247920\text{ eV}$.
   - **L-BFGS coordinate-relaxed swaps:** Relaxing all `624` single-pair exchanges with L-BFGS-B yields minimum energy `-163.80214265 eV` (`7` symmetry-equivalent swaps relax to an isometric copy of $E^*$, `617/624` relax to strictly higher basins, and `0/624` improve upon $E^*$).

---

## 3. Final Decision

Every clause of the bank's `success_criterion` is met with zero hidden quantifiers or stretched definitions.

pass: true
