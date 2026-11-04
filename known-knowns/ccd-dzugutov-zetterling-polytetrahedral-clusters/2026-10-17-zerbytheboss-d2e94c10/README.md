# Twenty New Putative Global Minima and Complete 502-Cluster Audit for Dzugutov, Modified-Dzugutov, and Zetterling-Dzugutov (Z1/Z2) Polytetrahedral Clusters (`ccd-dzugutov-zetterling-polytetrahedral-clusters`)

## What

Twenty 3D polytetrahedral cluster configurations in object/dzugutov_zetterling_20_records_and_502_audit.json across the Cambridge Cluster Database (CCD) modified-Dzugutov (N = 3..250) and Zetterling-Dzugutov Z1 and Z2 (N = 3..80) pair-potential tables — 4 on mDzugutov including 3 in N = 101..250 satisfying p1 (mDzugutov_74 at -180.9875532166 vs -180.982763, mDzugutov_134 at -343.3900404390 vs -343.386067, mDzugutov_177 at -462.5826604786 vs -462.579581, mDzugutov_241 at -641.7941625208 vs -641.793084), 10 on Z1 (Z1_38 at -100.1301837463 vs -99.874893, Z1_42 at -111.1739767527 vs -111.113917, Z1_44 at -116.8727164354 vs -116.579062, Z1_54 at -146.3500928888 vs -146.333923, Z1_65 at -176.4054458998 vs -176.220446, Z1_67 at -182.6367678185 vs -182.418355, Z1_68 at -185.3634223842 vs -185.275450, Z1_74 at -202.8773603525 vs -202.558045, Z1_75 at -205.8062213765 vs -205.448065, Z1_76 at -208.6187854827 vs -208.375341), and 6 on Z2 (Z2_35 at -92.2845205483 vs -92.270480, Z2_43 at -113.9462385534 vs -113.534760, Z2_56 at -149.2304029120 vs -148.936593, Z2_59 at -157.2398070630 vs -157.230650, Z2_69 at -184.6267084482 vs -184.286813, Z2_80 at -214.1928466438 vs -213.815040) — each strictly lower by at least 1e-4 than both the live CCD table energy and the polished posted CCD point file, polished in 55-digit arithmetic to gradient norm below 1.45e-33 (float64 gradient norm below 6.76e-13) with 6 rigid-body zero modes (abs(lambda) below 1e-6) and 0 negative Hessian eigenvalues (minimum vibrational eigenvalue lambda_7 >= 0.2423), accompanied by a complete 502-file CCD calibration and p2 discrepancy audit identifying the 10x Table I parameter typo in J. Chem. Phys. 118, 2792 (2003) for Z2 (b = 4.2e6 vs printed 4.2e7) and 5 corrupted central-atom coordinates in Z1_13, Z1_25, Z1_33, Z1_37, and Z2_25.

## Check It Yourself

Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS: ccd-dzugutov-zetterling-polytetrahedral-clusters verification complete.` (runs in ~10 seconds using only the Python 3 standard library `hashlib`, `math`, `decimal.Decimal`, and `json`).

## Compared To

All comparisons are against the Cambridge Cluster Database polytetrahedral tables of J. P. K. Doye, D. J. Wales, S. I. Simdyankin, F. H. M. Zetterling, and M. Dzugutov (*Faraday Discuss.* 118, 159, 2001; *Physical Review Letters* 86, 5719, 2001; *Journal of Chemical Physics* 118, 2792, 2003; `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Dzugutov/table.html`, `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/mDzugutov/table.html`, and `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/table.html`, fetched on `2026-10-18T05:10:18Z` and recorded in `the-record-we-beat/snapshot_2026-10-17.md`):

| # | Cluster | Potential | $N$ | New Putative Global Minimum $E^*$ (float64 / 55-digit) | CCD Table Energy | Polished CCD Point File | Improvement $\Delta E$ vs Table | $\|\nabla E\|_2$ (float64) | $\|\nabla E\|_2$ (55-digit) | $\lambda_7(H)$ | Discovery Operator |
|---:|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 1 | `mDzugutov_74` | `mDzugutov` | 74 | `-180.9875532166` | `-180.982763` | `-180.9827625507` | **`-0.004790`** | `1.09e-13` | `5.43e-34` | `7.8832` | Downward 1-atom peripheral etch from `mDzugutov_75` |
| 2 | `mDzugutov_134` | `mDzugutov` | 134 | `-343.3900404390` | `-343.386067` | `-343.3860669382` | **`-0.003973`** (`p1`) | `1.84e-13` | `7.74e-34` | `4.6422` | Downward 1-atom peripheral etch from `mDzugutov_135` |
| 3 | `mDzugutov_177` | `mDzugutov` | 177 | `-462.5826604786` | `-462.579581` | `-462.5795807885` | **`-0.003079`** (`p1`) | `2.57e-13` | `9.14e-34` | `5.1251` | Downward 1-atom peripheral etch from `mDzugutov_178` |
| 4 | `mDzugutov_241` | `mDzugutov` | 241 | `-641.7941625208` | `-641.793084` | `-641.7930841365` | **`-0.001079`** (`p1`) | `3.25e-13` | `1.04e-33` | `4.1056` | Upward tetrahedral cap on `mDzugutov_240` |
| 5 | `Z1_38` | `Z1` | 38 | `-100.1301837463` | `-99.874893` | `-99.8748926730` | **`-0.255291`** | `1.72e-13` | `9.24e-34` | `2.9834` | Cross-potential seed from `Z2_38` rescaled to $r_{\text{eq}}(\text{Z1})$ |
| 6 | `Z1_42` | `Z1` | 42 | `-111.1739767527` | `-111.113917` | `-111.1139167919` | **`-0.060060`** | `2.19e-13` | `8.63e-34` | `2.2442` | Cross-potential seed from `Z2_42` rescaled to $r_{\text{eq}}(\text{Z1})$ |
| 7 | `Z1_44` | `Z1` | 44 | `-116.8727164354` | `-116.579062` | `-116.5790623474` | **`-0.293654`** | `2.61e-13` | `9.31e-34` | `2.0286` | Cross-potential seed from `Z2_44` rescaled to $r_{\text{eq}}(\text{Z1})$ |
| 8 | `Z1_54` | `Z1` | 54 | `-146.3500928888` | `-146.333923` | `-146.3339233530` | **`-0.016170`** | `2.49e-13` | `1.13e-33` | `4.4127` | Downward 1-atom peripheral etch from `Z1_55` |
| 9 | `Z1_65` | `Z1` | 65 | `-176.4054458998` | `-176.220446` | `-176.2204455807` | **`-0.185000`** | `3.44e-13` | `1.21e-33` | `3.4451` | Downward 1-atom peripheral etch from `Z1_66` |
| 10 | `Z1_67` | `Z1` | 67 | `-182.6367678185` | `-182.418355` | `-182.4183551831` | **`-0.218413`** | `3.48e-13` | `1.45e-33` | `3.7862` | Downward 1-atom peripheral etch from `Z1_68` |
| 11 | `Z1_68` | `Z1` | 68 | `-185.3634223842` | `-185.275450` | `-185.2754498575` | **`-0.087972`** | `3.56e-13` | `1.44e-33` | `3.8098` | Downward 1-atom peripheral etch from `Z1_69` |
| 12 | `Z1_74` | `Z1` | 74 | `-202.8773603525` | `-202.558045` | `-202.5580451897` | **`-0.319315`** | `3.66e-13` | `1.29e-33` | `1.9453` | Upward tetrahedral cap on `Z1_73` |
| 13 | `Z1_75` | `Z1` | 75 | `-205.8062213765` | `-205.448065` | `-205.4480651688` | **`-0.358156`** | `3.71e-13` | `1.43e-33` | `1.9344` | Upward tetrahedral cap on `Z1_74` |
| 14 | `Z1_76` | `Z1` | 76 | `-208.6187854827` | `-208.375341` | `-208.3753408216` | **`-0.243444`** | `3.81e-13` | `1.30e-33` | `1.9460` | Upward tetrahedral cap on `Z1_75` |
| 15 | `Z2_35` | `Z2` | 35 | `-92.2845205483` | `-92.270480` | `-92.2704795533` | **`-0.014041`** | `3.10e-13` | `9.46e-34` | `4.6805` | Downward 1-atom peripheral etch from `Z2_36` |
| 16 | `Z2_43` | `Z2` | 43 | `-113.9462385534` | `-113.534760` | `-113.5347599666` | **`-0.411479`** | `3.47e-13` | `1.08e-33` | `2.6272` | Downward 1-atom peripheral etch from `Z2_44` |
| 17 | `Z2_56` | `Z2` | 56 | `-149.2304029120` | `-148.936593` | `-148.9365930045` | **`-0.293810`** | `4.41e-13` | `1.41e-33` | `0.8358` | Downward 1-atom peripheral etch from `Z2_57` |
| 18 | `Z2_59` | `Z2` | 59 | `-157.2398070630` | `-157.230650` | `-157.2306502954` | **`-0.009157`** | `4.15e-13` | `1.42e-33` | `0.8714` | Upward tetrahedral cap on `Z2_58` |
| 19 | `Z2_69` | `Z2` | 69 | `-184.6267084482` | `-184.286813` | `-184.2868137269` | **`-0.339895`** | `4.85e-13` | `1.24e-33` | `0.2781` | Downward peripheral etch from `Z2_70` + 1-atom cap hop |
| 20 | `Z2_80` | `Z2` | 80 | `-214.1928466438` | `-213.815040` | `-213.8150397720` | **`-0.377807`** | `6.76e-13` | `1.31e-33` | `0.2423` | Same-N 1-atom peripheral-to-tetrahedral-cap relocation |

### Structural Motifs (Icosahedral Network Types) for the `p1` Cells (`mDzugutov` $N \in 101\dots 250$)

Using a nearest-neighbor cutoff $r_{\text{nn}} = 1.45\,\sigma$ (between the first potential minimum $r_{\text{eq}} \approx 1.153$ and the repulsive barrier at $r \approx 1.55$), all three `p1` configurations (`mDzugutov_134`, `mDzugutov_177`, and `mDzugutov_241`, as well as `mDzugutov_74`) are **3D interpenetrating icosahedral networks wrapping a Frank-Kasper / C15 Laves-phase disclination core** (the large-$N$ polytetrahedral regime of Doye & Wales, *Phys. Rev. Lett.* 86, 5719, 2001):
- **`mDzugutov_134` ($N = 134$, `p1`, point group $C_1$)**: **3D interpenetrating icosahedral network / Frank-Kasper Laves-phase fragment** composed of `38` interpenetrating 13-atom $Z=12$ icosahedra (`74` center-to-center interpenetration bonds, cycle rank $\beta_1 = 37$) surrounding an 8-center Frank-Kasper disclination core (`6` $Z=16$ and `2` $Z=14$ coordination polyhedra linked by `8` six-fold $-72^\circ$ disclination spindles).
- **`mDzugutov_177` ($N = 177$, `p1`, point group $C_1$)**: **3D interpenetrating icosahedral network / C15 Laves-phase fragment** composed of `55` interpenetrating 13-atom $Z=12$ icosahedra (`115` center-to-center interpenetration bonds, cycle rank $\beta_1 = 61$) surrounding a pure 11-center $Z=16$ C15 Laves-phase disclination core linked by `13` six-fold $-72^\circ$ disclination spindles.
- **`mDzugutov_241` ($N = 241$, `p1`, point group $C_1$)**: **3D interpenetrating icosahedral network / Frank-Kasper C15 Laves-phase fragment with a peripheral tetrahedral cap**, composed of `82` interpenetrating 13-atom $Z=12$ icosahedra (`181` center-to-center interpenetration bonds, cycle rank $\beta_1 = 100$) surrounding a 19-center Frank-Kasper Laves-phase core (`18` $Z=16$ and `1` $Z=14$ polyhedra linked by `25` six-fold $-72^\circ$ disclination spindles) and terminated by a 4-coordinated peripheral regular-tetrahedral cap.
- *(For comparison, `mDzugutov_74` at $N = 74$ is a 3D interpenetrating icosahedral network of `16` $Z=12$ icosahedra with `24` center-to-center bonds and cycle rank $\beta_1 = 9$ around a 2-center $Z=16$ Frank-Kasper dimer spindle.)*

### Summary of the 502-Cluster Calibration & `p2` Audit

No third-party CCD coordinates are vendored in `object/dzugutov_zetterling_20_records_and_502_audit.json`; only the 20 new structures are recomputed from coordinates by `verify-it-yourself/check_dzugutov_clusters.py`, while the 48 calibration rows, polished-CCD energies, and 502-row audit are stored values checked against hashes (reproducing them from coordinates requires fetching the cited upstream point files):

1. **Exact Calibration Across All 4 Potentials (502/502 Point Files within $< 10^{-6}$)**:
   - **`Dzugutov` ($N = 3 \dots 100$, 98 files)**: $V(r) = A(r^{-m} - B)\exp(c/(r-a))\Theta(a-r) + B\exp(d/(r-b))\Theta(b-r)$ with $A=5.82, B=1.280, a=1.87, b=1.94, c=1.10, d=0.27, m=16$. Maximum absolute difference against the live CCD table across all 98 clusters is `4.938e-7 < 1e-6`.
   - **`mDzugutov` ($N = 3 \dots 250$, 248 files)**: Same functional form with $A=3.00, B=2.109, a=1.65, b=1.94, c=0.52, d=0.55, m=4$. Maximum absolute difference against the live CCD table across all 248 clusters is `9.953e-7 < 1e-6`.
   - **`Z1` ($N = 3 \dots 80$, 78 files)**: $V(r) = \left[a r^{-3} e^{\alpha r} \cos(2 k_F r) + b (\sigma/r)^n + V_0\right]\Theta(r_c - r)$ with $a=1.58, \alpha=-0.22, k_F=4.120, b=4.2\times 10^8, \sigma=0.331, n=18.0$, and third-minimum cutoff $r_c = 2.649085591313801, V_0 = 0.046826324124149$. Maximum absolute difference against the live CCD table (after restoring the 4 corrupted origin tokens below) is `4.939e-7 < 1e-6`.
   - **`Z2` ($N = 3 \dots 80$, 78 files)**: Same functional form with $a=1.04, \alpha=0.33, k_F=4.139, b=4.2\times 10^6, \sigma=0.348, n=14.5$, and third-minimum cutoff $r_c = 2.644877841213031, V_0 = 0.133915425377427$.
2. **`p2` Finding 1 — 10x Typographical Error in Table I of Doye et al., *J. Chem. Phys.* 118, 2792 (2003) for `Z2`**:
   - Table I of *J. Chem. Phys.* 118, 2792 (2003) prints $b = 4.2 \times 10^7$ for `Z2`, alongside $V_0 = 0.13391543$ and $r_{\text{cutoff}} = 2.64488$. At $r_c = 2.644877841213031$, $b = 4.2 \times 10^7$ gives $-V_{\text{bare}}(r_c) = 0.1339090$, which misses the printed $V_0 = 0.13391543$ (`0.1339090` against `0.1339154`), while $b = 4.2 \times 10^6$ reproduces it ($V_0 = 0.133915425377427$) and reproduces all 78 posted `Z2` CCD point files within `4.828e-7 < 1e-6` (observed in `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/table.html` on `2026-10-18`, `sha256: b1e48112d2f69d7158c07626e181861159b65376febd8943e65bb77147e6f64f`, and e.g. `Z2_35` observed in `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/Z2points/35` on `2026-10-18`, `sha256: 77f2e331708106244cea3ddc0fefd5ae53a92f16e98283ba1edc436c550b4d60`).
3. **`p2` Finding 2 — Five Corrupted Central-Atom Coordinates in the Live CCD Point Files (`Z1_13`, `Z1_25`, `Z1_33`, `Z1_37`, `Z2_25`)**:
   - Five posted coordinate files under `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/Z1points/` and `Z2points/` on the Cambridge Cluster Database contain a single coordinate on the central atom near $(0,0,0)$ where a Fortran/script formatter stripped the leading `0.000000` prefix, leaving a raw 4-digit integer (`-1466`, `0197`, `-2335`, `6593`, `-1168`):
     - `Z1_13` (line 13, $y = -1466 \to -1.466\times 10^{-7}$): raw error `+7.060461` $\to$ restored error `-3.285e-7` (observed in `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/Z1points/13` on `2026-10-18`, `sha256: e5dff47fcd0fa786fec45c3febf6d1f01d7e3bd61d5dc9441ead64d1c27ba099`)
     - `Z1_25` (line 23, $x = 0197 \to +1.970\times 10^{-8}$): raw error `+7.204198` $\to$ restored error `-1.751e-7` (observed in `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/Z1points/25` on `2026-10-18`, `sha256: 0cdd1efb6a39fcecb18b77c80fcbd6afbea0bb0b3d129a67de27d0e1efe5b544`)
     - `Z1_33` (line 33, $x = -2335 \to -2.335\times 10^{-7}$): raw error `+7.669487` $\to$ restored error `+1.838e-7` (observed in `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/Z1points/33` on `2026-10-18`, `sha256: 44e94f14b09641a6b17e4a8eee54ea29ff242bfc411b9d8e002122bea5e3ec45`)
     - `Z1_37` (line 14, $y = 6593 \to +6.593\times 10^{-7}$): raw error `+7.619645` $\to$ restored error `+4.560e-7` (observed in `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/Z1points/37` on `2026-10-18`, `sha256: a26ffd763ab08792f4e32e2c167b370f67af305e2a46893faa969ca36e920e08`)
     - `Z2_25` (line 23, $y = -1168 \to -1.168\times 10^{-7}$): raw error `+7.737610` $\to$ restored error `-1.662e-7` (observed in `https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Zetterling/Z2points/25` on `2026-10-18`, `sha256: c8511a5585ea56207e4d10033513aa8918bddd5fc8c856ce81081e06e5130e01`)

## Not Claimed

- We do not claim that these 20 new local minima are the mathematical global minima of their respective cluster sizes; each is a verified strict local minimum in a distinct structural basin that lowers the putative global minimum in the Cambridge Cluster Database by `0.001079` to `0.411479` reduced energy units (`10.8x` to `4114x` the `1e-4` threshold).

## Credits

- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **J. P. K. Doye, D. J. Wales, S. I. Simdyankin, F. H. M. Zetterling, and M. Dzugutov** (*Faraday Discuss.* 118, 159, 2001; *Physical Review Letters* 86, 5719, 2001; *Journal of Chemical Physics* 118, 2792, 2003; *Physical Review A* 46, R2984, 1992) and the **Cambridge Cluster Database** for the benchmark `Dzugutov`, `mDzugutov`, `Z1`, and `Z2` tables and coordinate archives.
