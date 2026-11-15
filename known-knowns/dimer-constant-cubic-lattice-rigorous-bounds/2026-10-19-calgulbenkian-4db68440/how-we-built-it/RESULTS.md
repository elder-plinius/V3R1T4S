# Final Results: `dimer-constant-cubic-lattice-rigorous-bounds`

## Executive Summary

We attack **`dimer-constant-cubic-lattice-rigorous-bounds`** across all four win paths (`Full Win`, `p1`, `p2`, `p3`) using exact 256-bit and 128-bit integer arithmetic (`u256` / `u128`) and exact 512-bit cross-multiplied Collatz–Wielandt verification:

1. **Full Win ($\ell_3$ Rigorous Upper Bound Improvement)**:
   - Qidong He (`arXiv:2607.28810v2`, August 11, 2026, Theorem 1.1 & Table 2) established the state-of-the-art rigorous upper bound on the 3D cubic lattice dimer constant $\ell_3 \le 0.452130$ by evaluating the diagonal-layer transfer matrix on $(m, n) = (5, 5)$ ($N = 25$, `35,070` symmetry orbits in sector $i = 12$) up to power-iteration step $p = 2$, where his Java implementation required **16.5 hours** (`main.tex`, Section 4, p. 13) and was forced to stop at $p = 2$.
   - Using four exact algorithmic optimizations in C (`run_he_55_64.c`, `certify_he_55.c`) — greedy neighbor-overlap vertex ordering, future-reachability Hall bitmask pruning, register-only 2-level unrolled leaf counting at $p = 0$, and monotone Collatz–Wielandt sector early stopping (Proposition 3.3) — we evaluate $(m, n) = (5, 5)$ across all sectors through $p = 4$ in **`27.39 seconds`** (**>2,100x faster** than He's 16.5 hours), and through $p = 5$ plus converged positive integer eigenvector certification in **`< 45 seconds`**:
     $$\ell_3 \le \begin{cases} 0.4521291626 \quad (\text{ceil\_6} = 0.452130) & \text{at } p = 2 \text{ (He's bound)}, \\ 0.4520200389 \quad (\text{ceil\_6} = 0.452021) & \text{at } p = 3, \\ \mathbf{0.4520105037} \quad (\text{ceil\_6} = \mathbf{0.452011}) & \text{at } p = 4 \text{ (unquantized } u256 \text{ certificate)}, \\ \mathbf{0.4520096761} \quad (\text{ceil\_6} = \mathbf{0.452010}) & \text{at } p = 5 \text{ (unquantized } u256 \text{ certificate)}, \\ \mathbf{0.4520095976} \quad (\text{ceil\_6} = \mathbf{0.452010}) & \text{at } \text{iter} = 14 \text{ (48-bit positive integer eigenvector certificate)}. \end{cases}$$
   - This improves He's `0.452130` by **$1.204 \times 10^{-4}$** (**$120\times$ larger** than the required $10^{-6}$ margin). We also compute the previously uncomputed $(m, n) = (6, 4)$ entry of He's Table 2 ($N = 24$, `45,270` orbits in sector $i = 12$) through $p = 4$ in `62.81s`, obtaining $\ell_3 \le 0.4526327904$ (`ceil_6 = 0.452633`).

2. **Partial Win `p1` (Complete Exact Reproduction of He's Table 2)**:
   - We independently reproduce **all 12 entries** of He's Table 2 (`(2,2), (3,2), (3,3), (4,2), (4,3), (4,4), (5,2), (5,3), (5,4), (6,2), (6,3)` at $p = 4$, and `(5,5)` at $p = 2$) to all 6 decimal places in `< 30 seconds` total (`test_he_speed.c`, `run_he_55_64.c`, `verify_cubic_dimer.py`).

3. **Partial Win `p2` (3D Cubic Lattice Monomer-Dimer Entropy $h_3$)**:
   - Applying He's Theorem 2.4 (Csikvári's 2-lift matching-generating-function inequality $M(H, t) \le M(G, t)^2$ evaluated at unit monomer/dimer activity $t = 1$) to the diagonal-layer reflection graphs $\mathbb{T}_{m,n,l}$, we prove that $h_3 \le \frac{1}{mn}\log\rho(\widehat{T}_{m,n}^{\text{MD}})$, where $\widehat{T}_{m,n}^{\text{MD}}$ factors into the layer permanent operator $P$ followed by the Subset Zeta Transform (SOS DP).
   - Using exact 128-bit integer Collatz–Wielandt verification (`cubic_md_h3.c`), we certify:
     $$h_3 \le \mathbf{0.7859680768} \quad \text{on } (m, n) = (5, 4)$$
     strictly improving the best published rigorous upper bound $h_3 \le 0.7862023450$ (Friedland & Peled `arXiv:math/0402009`; Friedland, Krop, Lundow, Markström `arXiv:math/0603001`) by **$2.34 \times 10^{-4}$**.

4. **Partial Win `p3` (4D Hypercubic Lattice $\mathbb{Z}^4$ Dimer Constant $\ell_4$)**:
   - Generalizing the diagonal-layer transfer matrix and verified $S_4 \ltimes (\mathbb{Z}_{m_1} \times \mathbb{Z}_{m_2} \times \mathbb{Z}_{m_3})$ symmetry reduction to $\mathbb{Z}^4$ (`hypercubic_d4.c`), we certify at $p = 4$ on $(m_1, m_2, m_3) = (3, 3, 2)$ ($N = 18$, `1,404` orbits in sector $i = 9$, runtime `0.46s`):
     $$\ell_4 \le \mathbf{0.5840147693} \quad (\text{ceil\_6} = \mathbf{0.584015})$$
     strictly improving the best published rigorous upper bound $\ell_4 \le \frac{\ln(8!)}{16} = 0.66278769\dots$ (Butera, Federbush, Pernici, *Phys. Rev. E* **88**, 032113 (2013), `arXiv:1305.7028`, Table III, p. 5) by **$0.07877$**.

---

## 1. Complete Table 2 Reproduction & Extension (`p1` & `Full Win`)

| $(m, n)$ | $N = mn$ | $|K_{m,n}|$ | Orbits in Sector $\lfloor N/2 \rfloor$ | He (`arXiv:2607.28810`) | Our Exact $C_{m,n; p}$ (10 digits) | Our `ceil_6` | Runtime |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $(2, 2)$ | 4 | 24 | 2 | `0.486478` ($p=4$) | `0.4864775373` ($p=4$) | `0.486478` | `0.00s` |
| $(3, 2)$ | 6 | 6 | 5 | `0.471408` ($p=4$) | `0.4714078777` ($p=4$) | `0.471408` | `0.00s` |
| $(3, 3)$ | 9 | 54 | 6 | `0.458558` ($p=4$) | `0.4585572161` ($p=4$) | `0.458558` | `0.00s` |
| $(4, 2)$ | 8 | 16 | 8 | `0.465970` ($p=4$) | `0.4659699158` ($p=4$) | `0.465970` | `0.00s` |
| $(4, 3)$ | 12 | 12 | 86 | `0.457380` ($p=4$) | `0.4573792680` ($p=4$) | `0.457380` | `0.00s` |
| $(4, 4)$ | 16 | 96 | 166 | `0.454673` ($p=4$) | `0.4546725669` ($p=4$) | `0.454673` | `0.01s` |
| $(5, 2)$ | 10 | 10 | 28 | `0.463401` ($p=4$) | `0.4634000925` ($p=4$) | `0.463401` | `0.00s` |
| $(5, 3)$ | 15 | 15 | 435 | `0.454663` ($p=4$) | `0.4546627762` ($p=4$) | `0.454663` | `0.03s` |
| $(5, 4)$ | 20 | 20 | 9,296 | `0.453365` ($p=4$) | `0.4533648604` ($p=4$) | `0.453365` | `1.39s` |
| $(6, 2)$ | 12 | 12 | 88 | `0.462010` ($p=4$) | `0.4620097563` ($p=4$) | `0.462010` | `0.00s` |
| $(6, 3)$ | 18 | 36 | 1,401 | `0.454618` ($p=4$) | `0.4546179726` ($p=4$) | `0.454618` | `0.21s` |
| $(6, 4)$ | 24 | 24 | 112,860 | *not computed* | `0.4526327904` ($p=4$) | **`0.452633`** | `62.81s` |
| $(5, 5)$ | 25 | 150 | 35,070 | `0.452130` ($p=2$) | `0.4521291626` ($p=2$) | `0.452130` | `14.12s` |
| **$(5, 5)$** | **25** | **150** | **35,070** | — | **`0.4520200389` ($p=3$)** | **`0.452021`** | `20.75s` |
| **$(5, 5)$** | **25** | **150** | **35,070** | — | **`0.4520105037` ($p=4$)** | **`0.452011`** | **`27.39s`** |
| **$(5, 5)$** | **25** | **150** | **35,070** | — | **`0.4520096761` ($p=5$)** | **`0.452010`** | `30.80s` |
| **$(5, 5)$** | **25** | **150** | **35,070** | — | **`0.4520095976` (iter 14 cert)** | **`0.452010`** | `42.50s` |

### Sector-by-Sector Breakdown for $(m, n) = (5, 5)$

By Proposition 3.3 of `arXiv:2607.28810`, $C_{5,5; p}^{(i)}$ is monotonically non-increasing in $p$ for each sector $i \in \{0, \dots, 12\}$. Evaluating sector $i = 12$ first establishes the threshold `0.4520095976`, and every smaller sector $i \in \{0, \dots, 11\}$ drops strictly below `0.4520095976` within $p \le 2$:

- **Sector $i = 12$** (`35,070` orbits):
  - $p = 0$: `0.4692800479` (`15498396383 / 1` at `u = 34120`)
  - $p = 1$: `0.4533425353` (`70840300670346690445 / 10140802421` at `u = 34623`)
  - $p = 2$: `0.4521291626` (`465736652230808449294072966961 / 70840300670346690445` at `u = 34623`)
  - $p = 3$: `0.4520200389` (`3045305365172468073012722643555264221865 / 465736652230808449294072966961` at `u = 34623`)
  - $p = 4$: **`0.4520105037`** (`19902802013446182074696171376412264183133509430535 / 3045305365172468073012722643555264221865` at `u = 34623`)
  - $p = 5$: **`0.4520096761`** (`130070744840279991535084424815197554265638051411906723776951 / 19902802013446182074696171376412264183133509430535` at `u = 34623`)
  - Converged 48-bit positive integer eigenvector (`results/cert_he_55_converged_sector12.txt`):
    $$\ell_3 \le \frac{1}{50}\log\left(\frac{68004910275217693829986}{10405826313374}\right) = \mathbf{0.452009597605\dots} \quad (\text{ceil\_6} = \mathbf{0.452010})$$
    with Collatz–Wielandt lower bound `0.452009597599...` (matching to 10 decimal digits!).
- **Sectors $i = 11$ down to $0$**:
  - $i = 11$ (`29,828` orbits): $C_{5,5; 2}^{(11)} = 0.4491342670 \le 0.4520095976$
  - $i = 10$ (`21,924` orbits): $C_{5,5; 1}^{(10)} = 0.4423438983 \le 0.4520095976$
  - $i = 9$ (`13,725` orbits): $C_{5,5; 0}^{(9)} = 0.4470224765 \le 0.4520095976$
  - $i = 8$ (`7,315` orbits): $C_{5,5; 0}^{(8)} = 0.4258596597 \le 0.4520095976$
  - $i = 7 \dots 0$: all $C_{5,5; 0}^{(i)} \le 0.3976542388 \le 0.4520095976$.

---

## 2. 3D Monomer-Dimer Entropy $h_3$ Rigorous Upper Bounds (`p2`)

By He's Theorem 2.4 (`arXiv:2607.28810`, derived from Csikvári's 2-lift theorem for matching generating polynomials $M(H, t) \le M(G, t)^2$ at monomer-dimer activity $t = 1$), the monomer-dimer partition function $Z(\mathbb{T}_{m,n,l})$ on diagonal reflection graphs satisfies $\lim_{l \to \infty} \frac{1}{2mnl}\log Z(\mathbb{T}_{m,n,l}) = \frac{1}{mn}\log\rho(\widehat{T}_{m,n}^{\text{MD}})$, yielding a rigorous upper bound on $h_3$ for every $(m, n)$:

| $(m, n)$ | $N = mn$ | Orbits | Exact Integer Collatz–Wielandt Ratio $\max_u (T^{\text{MD}} x)_u / x_u$ | Rigorous Upper Bound on $h_3$ | vs. Published `0.7862023450` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $(2, 2)$ | 4 | 6 | `6569077928250837 / 281474976710656` | `0.7875213012` | $+1.32 \times 10^{-3}$ |
| $(3, 2)$ | 6 | 14 | `31554237076853152 / 281474976710656` | `0.7865699342` | $+3.68 \times 10^{-4}$ |
| $(4, 2)$ | 8 | 40 | `1876829950380335 / 3474425469056` | `0.7864887879` | $+2.86 \times 10^{-4}$ |
| **$(3, 3)$** | **9** | **44** | `731051554747087 / 618837374495` | **`0.7860440830`** | **$-1.58 \times 10^{-4}$ (Beats published!)** |
| **$(4, 3)$** | **12** | **352** | `281474976710656 / 22551988607` | **`0.7859979651`** | **$-2.04 \times 10^{-4}$ (Beats published!)** |
| **$(5, 3)$** | **15** | **2,192** | `281474976710656 / 2133810619` | **`0.7859926284`** | **$-2.10 \times 10^{-4}$ (Beats published!)** |
| **$(4, 4)$** | **16** | **2,209** | `281474976710656 / 972644338` | **`0.7859709766`** | **$-2.31 \times 10^{-4}$ (Beats published!)** |
| **$(5, 4)$** | **20** | **52,488** | `1891821269973664 / 281869529` | **`0.7859680768`** | **$-2.34 \times 10^{-4}$ (Beats published!)** |

---

## 3. 4D Hypercubic Lattice ($\mathbb{Z}^4$) Dimer Constant $\ell_4$ Rigorous Upper Bounds (`p3`)

Generalizing the diagonal layer construction to $\mathbb{Z}^4$ with step set $D_4 = \{(0,0,0), (1,0,0), (0,1,0), (0,0,1)\} \subset V_{m_1, m_2, m_3}$ and verified $S_4 \ltimes (\mathbb{Z}_{m_1} \times \mathbb{Z}_{m_2} \times \mathbb{Z}_{m_3})$ symmetry reduction (`hypercubic_d4.c`):

| $(m_1, m_2, m_3)$ | $N = m_1 m_2 m_3$ | $|K|$ | Orbits in Sector $N/2$ | Rigorous Upper Bound on $\ell_4$ ($p = 4$) | `ceil_6` | vs. Published `0.66278769` | Runtime |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $(2, 2, 2)$ | 8 | 192 | 4 | **`0.5969480667`** | `0.596949` | $-0.06584$ | `0.00s` |
| $(3, 2, 2)$ | 12 | 24 | 50 | **`0.5893068961`** | `0.589307` | $-0.07348$ | `0.00s` |
| $(4, 2, 2)$ | 16 | 96 | 190 | **`0.5866775970`** | `0.586678` | $-0.07611$ | `0.04s` |
| **$(3, 3, 2)$** | **18** | **36** | **1,404** | **`0.5840147693`** | **`0.584015`** | **$-0.07877$** | **`0.46s`** |

---

## 4. Artifact Inventory & Reproduction Commands

- `PREREG.md`: Pre-registration of baselines, target constants, and verification criteria.
- `test_he_speed.c` & `run_he_55_64.c`: Multithreaded 256-bit exact integer solver reproducing all 12 entries of He's Table 2 and extending $(5, 5)$ and $(6, 4)$ through $p = 4$.
- `certify_he_55.c`: Generates and verifies the exact positive integer Collatz–Wielandt certificates for $(5, 5)$ sector $i = 12$ at $p = 4$, $p = 5$, and converged iteration 14 (`results/cert_he_55_p4_sector12.txt` and `results/cert_he_55_converged_sector12.txt`).
- `cubic_md_h3.c`: Exact 128-bit integer permanent + SOS DP solver and certificate generator for 3D monomer-dimer entropy $h_3$ (`results/cert_md_h3_33.txt`, `results/cert_md_h3_43.txt`, `results/cert_md_h3_44.txt`, `results/cert_md_h3_54.txt`).
- `hypercubic_d4.c`: Exact 256-bit integer 4D diagonal-layer solver and certificate generator for $\ell_4$ (`results/cert_4d_222.txt`, `results/cert_4d_322.txt`, `results/cert_4d_332.txt`).
- `verify_cubic_dimer.py`: Standalone pure-Python exact-integer verifier (`python3 verify_cubic_dimer.py`).
