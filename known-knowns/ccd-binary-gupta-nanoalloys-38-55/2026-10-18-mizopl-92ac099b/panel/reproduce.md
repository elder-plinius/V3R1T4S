# Panelist Report — REPRODUCE (`ccd-binary-gupta-nanoalloys-38-55`)

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Mandate & Quoted Problem Definition

Following the strict isolation protocol, only files inside `claim/` were read, and an independent verification script was written from scratch directly from the mathematical definition in `claim/CLAIM.md` **before** reading `claim/author_checker_bingupta_check.py`.

### Quoted Success Criterion (`claim/CLAIM.md` §1)

> "Success means coordinates and species labels for one system and composition listed in a CCD archive (for example Cu_12Au_26) such that E* under the exact Gupta parameter set used for that archive (calibrated first: the checker reproduces the header energies of every file in that archive to 1e-6 eV from coordinates) is STRICTLY LOWER (direction: min) by at least 1e-4 eV than the checker's evaluation of the archive structure for that composition (archives re-downloaded immediately before claiming) AND than any published value for the same system, parameters and composition found by an arXiv / Google Scholar search (at least the four papers named in the statement); AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm `\lt` 1e-10 (reduced units of the table), then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| `\lt` 1e-6) and no negative eigenvalue; AND polishing the archive structure gives an energy at least 1e-4 eV higher."

### Quoted Gupta Potential & Parameter Table (`claim/CLAIM.md` §2)

For an $N$-atom binary nanoalloy with species labels $s_i \in \{0\text{ (Cu)}, 1\text{ (Ag)}\}$ and Euclidean interatomic distances $r_{ij} = \|\mathbf{r}_i - \mathbf{r}_j\|_2$:

$$E(\mathbf{r}, \mathbf{s}) = \sum_{i=1}^{N} \left[ \sum_{j \neq i} A_{s_i s_j} \exp\!\left(-p_{s_i s_j}\!\left(\frac{r_{ij}}{r_{0, s_i s_j}} - 1\right)\right) - \sqrt{\sum_{j \neq i} \xi_{s_i s_j}^2 \exp\!\left(-2 q_{s_i s_j}\!\left(\frac{r_{ij}}{r_{0, s_i s_j}} - 1\right)\right)} \right]$$

with the published $\text{Cu-Ag}$ parameter set of Nunez & Johnston (*J. Phys. Chem. C* **114**, 13255–13266, 2010, Table 1), cited verbatim in `CuAg55/reference.txt` inside `claim/CuAg_55.rar`:

| Pair Type $(a, b)$ | $A_{ab}\text{ (eV)}$ | $\xi_{ab}\text{ (eV)}$ | $p_{ab}$ | $q_{ab}$ | $r_{0,ab}\text{ (\AA)}$ |
|---|---:|---:|---:|---:|---:|
| $\text{Cu-Cu}$ ($0, 0$) | `0.0894` | `1.2799` | `10.550` | `2.430` | `2.556` |
| $\text{Cu-Ag}$ ($0, 1$) | `0.0980` | `1.2274` | `10.700` | `2.805` | `2.72405` |
| $\text{Ag-Ag}$ ($1, 1$) | `0.1031` | `1.1895` | `10.850` | `3.180` | `2.8921` |

---

## 2. Independent Derivation of Analytical Gradient and $165 \times 165$ Hessian

Let $V_{ij}(r_{ij}) = A_{s_i s_j} \exp(-p_{s_i s_j}(r_{ij}/r_{0, s_i s_j} - 1))$, $\phi_{ij}(r_{ij}) = \xi_{s_i s_j}^2 \exp(-2 q_{s_i s_j}(r_{ij}/r_{0, s_i s_j} - 1))$, $\rho_i = \sum_{j \neq i} \phi_{ij}(r_{ij})$, and $\mathbf{u}_{ij} = (\mathbf{r}_i - \mathbf{r}_j)/r_{ij}$.

1. **Analytical First Derivative (Gradient):**
   With $V'_{ij} = -(p_{s_i s_j}/r_{0, s_i s_j}) V_{ij}$ and $\phi'_{ij} = -(2 q_{s_i s_j}/r_{0, s_i s_j}) \phi_{ij}$, each unordered pair $\{i, j\}$ has effective radial force coefficient
   $$f_{ij} = \frac{\partial E}{\partial r_{ij}} = 2 V'_{ij}(r_{ij}) - \frac{1}{2}\left(\rho_i^{-1/2} + \rho_j^{-1/2}\right) \phi'_{ij}(r_{ij})$$
   and $\nabla_{\mathbf{r}_i} E = \sum_{j \neq i} f_{ij} \mathbf{u}_{ij}$.

2. **Analytical Second Derivative ($3N \times 3N$ Hessian):**
   With $V''_{ij} = (p_{s_i s_j}/r_{0, s_i s_j})^2 V_{ij}$, $\phi''_{ij} = (2 q_{s_i s_j}/r_{0, s_i s_j})^2 \phi_{ij}$, and $w_{ij} = 2 V''_{ij}(r_{ij}) - \frac{1}{2}(\rho_i^{-1/2} + \rho_j^{-1/2})\phi''_{ij}(r_{ij})$, the $3N \times 3N$ Hessian is the sum of:
   - **Pairwise radial and transverse $3 \times 3$ blocks** for each pair $i \neq j$:
     $$K_{ij} = w_{ij} \mathbf{u}_{ij}\mathbf{u}_{ij}^T + \frac{f_{ij}}{r_{ij}}\left(I_3 - \mathbf{u}_{ij}\mathbf{u}_{ij}^T\right)$$
     added to diagonal blocks $(i,i)$ and $(j,j)$ and subtracted from off-diagonal blocks $(i,j)$ and $(j,i)$.
   - **Three-body density-gradient outer-product terms** from $\frac{d^2}{d\rho_m^2}(-\rho_m^{1/2}) = +\frac{1}{4}\rho_m^{-3/2}$ for each site $m \in \{1,\dots,N\}$:
     $$H^{(3\text{-body})} = \sum_{m=1}^{N} \frac{1}{4}\rho_m^{-3/2} \left(\nabla_{\mathbf{r}}\rho_m\right)\left(\nabla_{\mathbf{r}}\rho_m\right)^T$$
     where $(\nabla_{\mathbf{r}_a}\rho_m) = -\phi'_{ma}\mathbf{u}_{ma}$ for $a \neq m$ and $(\nabla_{\mathbf{r}_m}\rho_m) = \sum_{b \neq m} \phi'_{mb}\mathbf{u}_{mb}$.

3. **Independent Central Finite-Difference Cross-Check on `claim/Cu39Ag16_improved.txt`:**
   Constructing the $165 \times 165$ Hessian via central finite differences of the analytical gradient ($\epsilon = 10^{-6}\text{ \AA}$) and comparing against our analytical $165 \times 165$ Hessian gave:
   - $\max_{a,b} |H_{\text{anal}}(a,b) - H_{\text{fd}}(a,b)| = 2.978 \times 10^{-9}\text{ eV/\AA}^2$
   - $\max_{k} |\lambda_k(H_{\text{anal}}) - \lambda_k(H_{\text{fd}})| = 1.569 \times 10^{-9}\text{ eV/\AA}^2$

---

## 3. File Integrity & SHA-256 Verification

All claimed artifacts in `claim/` were verified for exact byte count and SHA-256 digest:

| File | Bytes | Verified SHA-256 | Match |
|---|---:|---|---|
| `claim/Cu39Ag16_improved.txt` | `6,149` | `92ac099b6963dcaedd5dbc1000731a5a87c99fc6e208b30475c6850e420a991d` | Exact |
| `claim/Cu34Ag21_improved.txt` | `6,150` | `1802a8519f28bed64f8712ee414f461870b9c1cf00c97c3698e0eb289548874e` | Exact |
| `claim/Cu33Ag22_improved.txt` | `6,149` | `e942c06011a9b969ec8d701b228b58c66dcd1837d7cf11d5a82760bc6d3354dd` | Exact |
| `claim/Cu31Ag24_improved.txt` | `6,147` | `c229315ab3d778e5da4a7329879fde3d0117a94fdf1b0331b9216f3bb6acc4ee` | Exact |
| `claim/Cu22Ag33_improved.txt` | `6,149` | `677fe021a76ddcc4e3b254721ac87f8c3b2369f0518c64f7a73380b5b1f28037` | Exact |
| `claim/Cu20Ag35_improved.txt` | `6,146` | `0e1f6e7fd59b164c8c4e53ec3cd00d00722ed69f57abe3e862b0f4399781c712` | Exact |
| `claim/Cu15Ag40_improved.txt` | `6,147` | `18d181026f1f06416e1d11561a5539917b463d2184843b9a56c6fa4b9c9ab60a` | Exact |
| `claim/Cu17Ag38_improved.txt` | `6,148` | `a72814de42efed463752f9092af0c3b77b1ed48f9543e6a4b2e717d620ce025b` | Exact |
| `claim/cuag55_improvements_summary.tsv` | `1,557` | `a8ca7d24a8df4e0e541d3af82dee1ba378391e009312c243d393af4c68d534d0` | Exact |
| `claim/CuAg_55.rar` | `67,636` | `c6cdc7b61eddf14da78c752368618679836f24f40c1a17c84f47230e210d01dd` | Exact |
| `claim/CCD.html` | `15,051` | `9662d9a7fcf599815e22d6dae7fbdeac8b71cf7892f836284f2d0769383183c8` | Exact |
| `claim/author_checker_bingupta_check.py` | `13,637` | `2b73c482228b87c3662a84ad3ba8a078e18d332a93ad17d86b6b03032c803368` | Exact |

Furthermore, all eight `claim/published_Cu*.txt` files (`2,620` bytes each) were verified to have identical SHA-256 digests to the corresponding `CuAg55/Cu*Ag*.txt` files extracted directly from `claim/CuAg_55.rar` via `bsdtar`.

---

## 4. Full-Archive Calibration (`56/56` Files) & Negative Controls

1. **Full-Archive Calibration (`56/56` files in `claim/CuAg_55.rar`):**
   Extracting `claim/CuAg_55.rar` with `bsdtar` produced `CuAg55/reference.txt` and all 56 composition files `Cu0Ag55.txt` through `Cu55Ag0.txt`. Evaluating every file from its saved coordinates in our independent checker confirmed exact atom counts $(n_{\text{Cu}} = k, n_{\text{Ag}} = 55-k)$ and reproduced all 56 header energies with:
   $$\max_{0 \le k \le 55} |E_{\text{eval}} - E_{\text{header}}| = 4.890353 \times 10^{-9}\text{ eV} \quad (\text{attained on }\text{Cu}_{13}\text{Ag}_{42})$$
   which is more than $200\times$ tighter than the required $1.0 \times 10^{-6}\text{ eV}$ calibration threshold.

2. **Negative Controls:**
   - **Control A (Coordinate perturbation):** Perturbing atom 0's $x$-coordinate in `claim/Cu39Ag16_improved.txt` by $+0.01\text{ \AA}$ raised the energy from $-163.80214265\text{ eV}$ to $-163.80195574\text{ eV}$ and caused the gradient norm to jump by 12 orders of magnitude from $1.643 \times 10^{-14}\text{ eV/\AA}$ (`float64`) to $4.620 \times 10^{-2}\text{ eV/\AA}$, immediately failing the stationarity check.
   - **Control B (Homotop species swap):** Swapping the species labels of atom 0 ($\text{Cu}$) and atom 5 ($\text{Ag}$) in `claim/Cu39Ag16_improved.txt` raised the energy from $-163.80214265\text{ eV}$ to $-163.27802595\text{ eV}$ ($+0.52411670\text{ eV}$) and caused the gradient norm to jump to $2.907\text{ eV/\AA}$, immediately failing both the energy and gradient checks.

---

## 5. Independent Verification of All 8 Certified Lower-Energy Structures (Determinism Verified across 2 Runs)

Running our independent checker twice in succession produced bit-for-bit identical results (total runtime `4.95 s` for both passes combined, plus archive calibration and finite-difference Hessian checks). All 8 structures satisfy every bank requirement:

| Composition | $(n_{\text{Cu}}, n_{\text{Ag}})$ | Archive Eval $E_{\text{arch}}\text{ (eV)}$ | Archive Polished $E_{\text{arch,pol}}\text{ (eV)}$ | Certified $E^*\text{ (eV)}$ | $\Delta E\text{ (eV)}$ | $\|\nabla E^*\|_{\text{mp30}}$ (exact dec) | $\|\nabla E^*\|_{\text{mp30}}$ (`f64` params) | Zero Modes ($\|\lambda\| \lt 10^{-6}$) | Neg. Modes | $\lambda_7\text{ (eV/\AA}^2\text{)}$ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`Cu39Ag16`** | `(39, 16)` | `-162.61229825` | `-162.61229825` | **`-163.80214265`** | **`-1.18984440`** | `2.17e-28` | `1.84e-15` | `6` | `0` | `0.699916` |
| **`Cu34Ag21`** | `(34, 21)` | `-160.81218484` | `-160.81218484` | **`-161.76692486`** | **`-0.95474003`** | `6.34e-23` | `2.10e-15` | `6` | `0` | `0.714086` |
| **`Cu33Ag22`** | `(33, 22)` | `-160.43136967` | `-160.43136967` | **`-161.35336662`** | **`-0.92199695`** | `4.52e-23` | `2.14e-15` | `6` | `0` | `0.733798` |
| **`Cu31Ag24`** | `(31, 24)` | `-159.69487106` | `-159.69487106` | **`-160.49285973`** | **`-0.79798867`** | `1.56e-26` | `2.25e-15` | `6` | `0` | `0.729365` |
| **`Cu22Ag33`** | `(22, 33)` | `-156.38507389` | `-156.38507389` | **`-156.61674699`** | **`-0.23167311`** | `7.04e-26` | `2.65e-15` | `6` | `0` | `0.779003` |
| **`Cu20Ag35`** | `(20, 35)` | `-155.56958143` | `-155.56958143` | **`-155.69839654`** | **`-0.12881511`** | `4.53e-24` | `2.74e-15` | `6` | `0` | `0.777510` |
| **`Cu15Ag40`** | `(15, 40)` | `-153.49887624` | `-153.49887624` | **`-153.62512358`** | **`-0.12624733`** | `2.90e-28` | `2.80e-15` | `6` | `0` | `0.241364` |
| **`Cu17Ag38`** | `(17, 38)` | `-154.40077125` | `-154.40077125` | **`-154.46534927`** | **`-0.06457801`** | `2.57e-28` | `2.70e-15` | `6` | `0` | `0.250397` |

Full 30-digit `mpmath` (`mp.dps = 30`) energies $E^*$ directly from the saved coordinate files:
- `claim/Cu39Ag16_improved.txt`: `-163.802142648235790813910794783 eV` (`|\nabla E^*|_{\text{mp30}} = 2.16767 \times 10^{-28}\text{ eV/\AA}`)
- `claim/Cu34Ag21_improved.txt`: `-161.766924864657163449857055989 eV` (`|\nabla E^*|_{\text{mp30}} = 6.34297 \times 10^{-23}\text{ eV/\AA}`)
- `claim/Cu33Ag22_improved.txt`: `-161.353366617687116797121324081 eV` (`|\nabla E^*|_{\text{mp30}} = 4.52048 \times 10^{-23}\text{ eV/\AA}`)
- `claim/Cu31Ag24_improved.txt`: `-160.492859728445981917932498890 eV` (`|\nabla E^*|_{\text{mp30}} = 1.55576 \times 10^{-26}\text{ eV/\AA}`)
- `claim/Cu22Ag33_improved.txt`: `-156.616746993695675307932204397 eV` (`|\nabla E^*|_{\text{mp30}} = 7.03773 \times 10^{-26}\text{ eV/\AA}`)
- `claim/Cu20Ag35_improved.txt`: `-155.698396541716658031829885950 eV` (`|\nabla E^*|_{\text{mp30}} = 4.52775 \times 10^{-24}\text{ eV/\AA}`)
- `claim/Cu15Ag40_improved.txt`: `-153.625123575167212273438381235 eV` (`|\nabla E^*|_{\text{mp30}} = 2.89584 \times 10^{-28}\text{ eV/\AA}`)
- `claim/Cu17Ag38_improved.txt`: `-154.465349265664390587829002157 eV` (`|\nabla E^*|_{\text{mp30}} = 2.57147 \times 10^{-28}\text{ eV/\AA}`)

Note on a minor 10th-decimal-place prose transcription difference in `claim/CLAIM.md` lines 58–59: the table in `claim/CLAIM.md` (§3), `claim/REPRODUCE.md`, `claim/cuag55_improvements_summary.tsv`, the header of `claim/Cu39Ag16_improved.txt`, and `claim/author_checker_bingupta_check.py` all agree on $E^* = -163.80214265\text{ eV}$ (`-163.802142648235790813910794783 eV` in 30-digit `mpmath`) and $E_{\text{arch}} = -162.61229825\text{ eV}$ (`-162.6122982488 eV`), whereas `claim/CLAIM.md` lines 58–59 display `-163.80214264818852...` and `-162.61229825329...` (differing by $4.7 \times 10^{-11}\text{ eV}$ and $4.5 \times 10^{-9}\text{ eV}$, respectively, from binary vs. decimal parameter conversion). This $4.7 \times 10^{-11}\text{ eV}$ difference does not affect the 8-decimal-place energies, $\Delta E = -1.18984440\text{ eV}$, or any certification criterion ($\|\nabla E^*\|_{\text{mp30}} \lt 10^{-10}$ holds under both exact-decimal and float64-converted parameters: $2.17 \times 10^{-28}$ and $1.84 \times 10^{-15}$, respectively).

---

## 6. Author Checker Execution (`claim/REPRODUCE.md`)

After completing independent verification, `claim/author_checker_bingupta_check.py` was inspected and executed from `claim/`, completing in `5.8 s` with exit code `0` and reproducing the output in `claim/REPRODUCE.md` line for line (`56/56` archive calibration $\max |E_{\text{eval}} - E_{\text{header}}| = 4.890 \times 10^{-9}\text{ eV}$, all 8 improved compositions passing 30-digit `mpmath` stationarity, $165 \times 165$ Hessian spectrum with `6` zero modes and `0` negative modes, and distinct-basin archive polishing). Temporary working files in `panel/` were removed upon completion.

pass: true
