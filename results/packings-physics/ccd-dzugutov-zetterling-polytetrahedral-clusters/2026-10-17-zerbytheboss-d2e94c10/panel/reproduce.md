# V3R1T4S Reproduction Panel Audit (`reproduce.md`)

context: subagent (fresh invocation)
target_id: ccd-dzugutov-zetterling-polytetrahedral-clusters
cells: mDzugutov_74, mDzugutov_134, mDzugutov_177, mDzugutov_241, Z1_38, Z1_42, Z1_44, Z1_54, Z1_65, Z1_67, Z1_68, Z1_74, Z1_75, Z1_76, Z2_35, Z2_43, Z2_56, Z2_59, Z2_69, Z2_80
file: object/dzugutov_zetterling_20_records_and_502_audit.json
sha256: fa681bfd7a3252d03c7c74a9729d0e8bd16ee2f0cb6a29d94db101bc2ed75e04

## 1. Quoted Mathematical Definitions (Dzugutov, Modified-Dzugutov, and Zetterling-Dzugutov Z1/Z2 Pair Potentials)

Before reading `verify-it-yourself/check_dzugutov_clusters.py`, an independent checker was written directly from the mathematical specifications in M. Dzugutov (*Physical Review A* 46, R2984, 1992), J. P. K. Doye, D. J. Wales, and S. I. Simdyankin (*Faraday Discussions* 118, 159, 2001), J. P. K. Doye and D. J. Wales (*Physical Review Letters* 86, 5719, 2001), and J. P. K. Doye, D. J. Wales, F. H. M. Zetterling, and M. Dzugutov (*Journal of Chemical Physics* 118, 2792, 2003):

- **Total Pairwise Potential Energy**:
  For an $N$-atom cluster with Cartesian coordinates $r_1, \dots, r_N \in \mathbb{R}^3$ and pairwise Euclidean distances $r_{ij} = \|r_i - r_j\|_2$:
  $$
  E = \sum_{1 \le i \neq j \le N} \frac{1}{2} V(r_{ij})
  $$
- **Dzugutov (`Dzugutov`) and Modified-Dzugutov (`mDzugutov`) Pair Potential**:
  $$
  V(r) = A\bigl(r^{-m} - B\bigr)\exp\!\left(\frac{c}{r - a}\right)\Theta(a - r) + B\exp\!\left(\frac{d}{r - b}\right)\Theta(b - r)
  $$
  - `Dzugutov`: $A = 5.82$, $B = 1.28$, $a = 1.87$, $b = 1.94$, $c = 1.10$, $d = 0.27$, $m = 16$.
  - `mDzugutov`: $A = 3.00$, $B = 2.109$, $a = 1.65$, $b = 1.94$, $c = 0.52$, $d = 0.55$, $m = 4$.
- **Zetterling-Dzugutov (`Z1` and `Z2`) Pair Potential**:
  $$
  V(r) = \left[a \frac{\exp(\alpha r)}{r^3}\cos(2 k_F r) + b\left(\frac{\sigma}{r}\right)^n + V_0\right]\Theta(r_c - r)
  $$
  - `Z1`: $a = 1.58$, $\alpha = -0.22$, $k_F = 4.120$, $b = 4.2 \times 10^8$, $\sigma = 0.331$, $n = 18.0$, third-minimum cutoff $r_c = 2.649085591313801$, $V_0 = 0.046826324124149$.
  - `Z2`: $a = 1.04$, $\alpha = 0.33$, $k_F = 4.139$, $b = 4.2 \times 10^6$ (noting the 10x typographical error $4.2 \times 10^7$ in Table I of *J. Chem. Phys.* 118, 2792, 2003), $\sigma = 0.348$, $n = 14.5$, third-minimum cutoff $r_c = 2.644877841213031$, $V_0 = 0.133915425377427$.

## 2. Independent Verification Results on `object/dzugutov_zetterling_20_records_and_502_audit.json`

1. **Calibration on 48 Embedded Point Files & 502-Cluster CCD Audit (`ccd_502_point_files_audit`, Partial Win `p2`)**:
   - Independently evaluating all 48 embedded calibration cluster coordinate sets (`12` per potential across `Dzugutov`, `mDzugutov`, `Z1`, and `Z2`) reproduces the live 6-decimal Cambridge Cluster Database table energies with maximum absolute difference `4.587e-7` (`Dzugutov`), `4.797e-7` (`mDzugutov`), `4.761e-7` (`Z1`), and `4.669e-7` (`Z2`), all well within `1e-6`.
   - Across all 502 posted point files (`98` `Dzugutov` $N = 3 \dots 100$, `248` `mDzugutov` $N = 3 \dots 250$, `78` `Z1` $N = 3 \dots 80$, and `78` `Z2` $N = 3 \dots 80$) in `ccd_502_point_files_audit`, restoring the 5 truncated origin tokens (`Z1_13`, `Z1_25`, `Z1_33`, `Z1_37`, `Z2_25`) leaves `0` unreproduced rows and maximum deviation `9.953e-7` (under `1e-6`).

2. **Independent `float64`, 55-Digit `mpmath`, Distinct-Basin, Gradient, and $3N \times 3N$ Hessian Spectrum Audit across All 20 Record Clusters**:

| # | Cluster | Potential | $N$ | CCD Table $E$ | Polished CCD $E$ | `float64` / 55-Digit $E^*$ | $\Delta E$ vs Table | $\|\nabla E\|_2$ (`float64`) | $\|\nabla E\|_2$ (`mp55`) | Hessian Zero / Neg / Pos Modes | Vibrational $\lambda_7 \dots \lambda_{\max}$ |
|---:|:---|:---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | **`mDzugutov_74`** | `mDzugutov` | `74` | `-180.982763` | `-180.9827634219` | `-180.9875532166` | **`-0.004790`** | `1.09e-13` | `5.43e-34` | `6 / 0 / 216` | `7.8832 .. 308.17` |
| 2 | **`mDzugutov_134`** | `mDzugutov` | `134` | `-343.386067` | `-343.3860669414` | `-343.3900404390` | **`-0.003973`** (`p1`) | `1.86e-13` | `7.74e-34` | `6 / 0 / 396` | `4.6422 .. 327.92` |
| 3 | **`mDzugutov_177`** | `mDzugutov` | `177` | `-462.579581` | `-462.5795810185` | `-462.5826604786` | **`-0.003079`** (`p1`) | `2.56e-13` | `9.14e-34` | `6 / 0 / 525` | `5.1251 .. 321.22` |
| 4 | **`mDzugutov_241`** | `mDzugutov` | `241` | `-641.793084` | `-641.7930840202` | `-641.7941625208` | **`-0.001079`** (`p1`) | `3.24e-13` | `1.04e-33` | `6 / 0 / 717` | `4.1056 .. 315.86` |
| 5 | **`Z1_38`** | `Z1` | `38` | `-99.874893` | `-99.8748933106` | `-100.1301837463` | **`-0.255291`** | `1.79e-13` | `9.24e-34` | `6 / 0 / 108` | `2.9834 .. 903.21` |
| 6 | **`Z1_42`** | `Z1` | `42` | `-111.113917` | `-111.1139169676` | `-111.1739767527` | **`-0.060060`** | `2.25e-13` | `8.63e-34` | `6 / 0 / 120` | `2.2442 .. 903.48` |
| 7 | **`Z1_44`** | `Z1` | `44` | `-116.579062` | `-116.5790624900` | `-116.8727164354` | **`-0.293654`** | `2.82e-13` | `9.31e-34` | `6 / 0 / 126` | `2.0286 .. 1124.55` |
| 8 | **`Z1_54`** | `Z1` | `54` | `-146.333923` | `-146.3339228268` | `-146.3500928888` | **`-0.016170`** | `2.57e-13` | `1.13e-33` | `6 / 0 / 156` | `4.4127 .. 801.91` |
| 9 | **`Z1_65`** | `Z1` | `65` | `-176.220446` | `-176.2204457282` | `-176.4054458998` | **`-0.185000`** | `3.19e-13` | `1.21e-33` | `6 / 0 / 189` | `3.4451 .. 822.76` |
| 10 | **`Z1_67`** | `Z1` | `67` | `-182.418355` | `-182.4183551867` | `-182.6367678185` | **`-0.218413`** | `3.50e-13` | `1.45e-33` | `6 / 0 / 195` | `3.7862 .. 946.59` |
| 11 | **`Z1_68`** | `Z1` | `68` | `-185.275450` | `-185.2754498541` | `-185.3634223842` | **`-0.087972`** | `3.57e-13` | `1.44e-33` | `6 / 0 / 198` | `3.8098 .. 999.83` |
| 12 | **`Z1_74`** | `Z1` | `74` | `-202.558045` | `-202.5580447800` | `-202.8773603525` | **`-0.319315`** | `3.67e-13` | `1.29e-33` | `6 / 0 / 216` | `1.9453 .. 743.55` |
| 13 | **`Z1_75`** | `Z1` | `75` | `-205.448065` | `-205.4480650664` | `-205.8062213765` | **`-0.358156`** | `3.79e-13` | `1.43e-33` | `6 / 0 / 219` | `1.9344 .. 745.40` |
| 14 | **`Z1_76`** | `Z1` | `76` | `-208.375341` | `-208.3753408505` | `-208.6187854827` | **`-0.243444`** | `3.78e-13` | `1.30e-33` | `6 / 0 / 222` | `1.9460 .. 769.70` |
| 15 | **`Z2_35`** | `Z2` | `35` | `-92.270480` | `-92.2704799550` | `-92.2845205483` | **`-0.014041`** | `3.08e-13` | `9.46e-34` | `6 / 0 / 99` | `4.6805 .. 941.47` |
| 16 | **`Z2_43`** | `Z2` | `43` | `-113.534760` | `-113.5347604224` | `-113.9462385534` | **`-0.411479`** | `3.59e-13` | `1.08e-33` | `6 / 0 / 123` | `2.6272 .. 830.42` |
| 17 | **`Z2_56`** | `Z2` | `56` | `-148.936593` | `-148.9365928361` | `-149.2304029120` | **`-0.293810`** | `4.39e-13` | `1.41e-33` | `6 / 0 / 162` | `0.8358 .. 828.13` |
| 18 | **`Z2_59`** | `Z2` | `59` | `-157.230650` | `-157.2306498078` | `-157.2398070630` | **`-0.009157`** | `4.13e-13` | `1.42e-33` | `6 / 0 / 171` | `0.8714 .. 932.73` |
| 19 | **`Z2_69`** | `Z2` | `69` | `-184.286813` | `-184.2868132669` | `-184.6267084482` | **`-0.339895`** | `4.83e-13` | `1.24e-33` | `6 / 0 / 201` | `0.2781 .. 826.89` |
| 20 | **`Z2_80`** | `Z2` | `80` | `-213.815040` | `-213.8150397848` | `-214.1928466438` | **`-0.377807`** | `6.77e-13` | `1.31e-33` | `6 / 0 / 234` | `0.2423 .. 797.42` |

   - For all 20 clusters, `float64` and 55-digit `Decimal` / `mpmath` energies agree within `1e-11`, `E_new` lowers both `E_table` and `E_ccd_polished` by `-0.001079` to `-0.411479` (`10.8x` to `4,115x` the `1e-4` threshold), gradient norms are at most `6.77e-13` in `float64` and `1.45e-33` in 55-digit arithmetic (well below `1e-10`), and the $3N \times 3N$ analytical Hessian has `6` near-zero rigid-body modes (`|\lambda| \le 1e-6`), `0` negative eigenvalues, and all $3N - 6$ vibrational modes strictly positive ($\lambda_7 \ge 0.2423$).

3. **Execution of `verify-it-yourself/run_checks.sh` and Negative Corruption Test**:
   - Running `sh verify-it-yourself/run_checks.sh` from the package root exited with code `0` and output `PASS: ccd-dzugutov-zetterling-polytetrahedral-clusters verification complete.`
   - Perturbing a middle coordinate digit in `coords_float64` (`+1e-6`) or in `coords_decimal36` (`+1e-8`) on a temporary copy caused `verify-it-yourself/check_dzugutov_clusters.py` to exit with code `1` (`FAIL`), confirming that both the `float64` and 55-digit checks actively reject corrupted coordinates.

pass: true
