# `iau-mdc-new-meteor-shower-gmn` — Uncatalogued Multi-Year Meteor Showers (`M2_Hercules` $N=20$, `M1_Cepheus_Core` $N=15$, `M1_Cepheus_MC` $N=15$, `M3_Camelopardalis` $N=16$), 2025-Sep-01 4.84h Outburst (`p1`, $N=10$), and 17 Multi-Year Recurrent IAU MDC Working-List Showers (`p2`) in Public GMN Orbits (`2026-10-20-mizopl-56ac1336`)

## What

Across 3,599,504 public GMN trajectories (2018-2026) screened against all 2,192 rows of live-fetched claim/streamfulldata2026.txt (sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe), the artifacts in claim/new_shower_cluster.json (sha256: 56ac13361eb045681ffb2dc1cd32a5697dd4a291fdf43826d8f7a7638fdb1937), claim/new_shower_gmn_lines.txt (sha256: 369b2054ebaed1f04c2cc6758eb515cf0fd5c0a15b1f99a3d84a7381968653d2), claim/m1_cepheus_core_gmn_lines.txt (sha256: 379b26fa5b869788a4d7f35e81de93f0227e8a503d9c0c840efb386776a3d085), claim/m1_cepheus_mc_gmn_lines.txt (sha256: 21d82381f78e3adf0638e52e1e4ffd47af8b57652602e7e7803aeff32247b96a), claim/m3_camelopardalis_gmn_lines.txt (sha256: b5ad6728dff488383e601afbba4599ce73eb6cf46a84ae2c45b8796ba2de6069), claim/p1_outburst_cluster.json (sha256: a9691f53685fb5f73c675aaf2362cdd65547a2ae2283048d074ab7671d44d462), claim/p2_working_list_recurrence.json (sha256: baef22e03a7b245ab9a4d643378c26454e9105fc134ef9096588c20c830ea2ac), and claim/null_test_400_controls.json (sha256: cfc3c177265cb2a42c4e57dc0e5b8711e8ed710db89dba9e8b8dd9f85cc10a22) deterministically certify four uncatalogued multi-year meteor shower clusters meeting every clause of the full success_criterion (M2_Hercules N=20 max D_SH=0.0491 pairwise D_SH=0.0829 min MDC D_SH=0.3539 Z=26.81 sigma; M1_Cepheus_Core N=15 max D_SH=0.0468 Z=33.31 sigma; M1_Cepheus_MC N=15 with 100% per-meteor >=2 countries max D_SH=0.0730 Z=13.31 sigma; M3_Camelopardalis N=16 max D_SH=0.0371 Z=45.84 sigma), one single-night 4.84-hour outburst meeting partial win p1 (N=10, max D_SH=0.0619 < 0.08, min MDC D_SH=0.2521, Z=10.68 sigma), and 17 single-year IAU MDC Working List showers recurring across 3-6 GMN years with D_SH < 0.06 < 0.10 meeting partial win p2.

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~0.5` seconds on CPU (`python3` + `numpy`).

## Compared To

- **Target ID**: `iau-mdc-new-meteor-shower-gmn` (`category: earth-and-sky`)
- **Primary Status Table**: `https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php` (`2026-10-20T18:54:36Z`, `HTTP/1.1 200 OK`, `369,910` bytes, `sha256: 1e37425b8e2b2fcff742b741d7d4acc4b2522b3abfa8876e987357ab893c8454`) and `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt` (`2026-10-20T18:54:36Z`, `HTTP/1.1 200 OK`, `1,555,028` bytes, `sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe`, `2,192` shower rows updated `Oct 19, 20:00:00 UTC, 2026`):
  - **Main Criterion (`object/new_shower_cluster.json`, `object/independent_cluster_audit.json`):** Four uncatalogued multi-year clusters of unassigned (`IAU No == -1`) multi-station (`Num stat >= 3`) GMN orbits (`M2_Hercules` $N=20$, $\max D_{\text{SH}}=0.0491$, $\max \text{pairwise } D_{\text{SH}}=0.0829$, $\min D_{\text{SH}}(\text{MDC})=0.3539$, $\Delta\theta=11.76^\circ$, $7$ countries, $Z=26.81\sigma$; `M1_Cepheus_Core` $N=15$, $\max D_{\text{SH}}=0.0468$, $\min D_{\text{SH}}(\text{MDC})=0.2766$, $13$ countries, $Z=33.31\sigma$; `M1_Cepheus_MC` $N=15$ with 100% per-meteor $\ge 2$ countries, $\max D_{\text{SH}}=0.0730$, $\min D_{\text{SH}}(\text{MDC})=0.2829$, $Z=13.31\sigma$; and `M3_Camelopardalis` $N=16$, $\max D_{\text{SH}}=0.0371$, $\min D_{\text{SH}}(\text{MDC})=0.3151$, $Z=45.84\sigma$, plus `7` additional strict per-meteor multi-country clusters `Indep #1..#7`).
  - **Partial Win `p1` (`object/p1_outburst_cluster.json`):** Single-night `4.84`-hour Cygnus–Draco outburst on `2025-08-31/09-01` ($N=10$, $\max D_{\text{SH}}=0.0619 < 0.08$, $\min D_{\text{SH}}(\text{MDC})=0.2521 \ge 0.20$, $\Delta\theta=20.65^\circ$, $6$ countries, $Z=10.68\sigma$).
  - **Partial Win `p2` (`object/p2_working_list_recurrence.json`):** `17` single-year IAU MDC Working List (`status == 0`) showers recurring in $3\text{--}6$ distinct GMN years with $D_{\text{SH}} < 0.06 < 0.10$ (headlined by `M2025-S1` across 6 years `2021–2026`, $N=107$, $D_{\text{SH}}=0.0023$).

## Not Claimed

- We do not claim a parent-body dynamical stream integration (`p3`), nor do we submit any report or nomenclature proposal directly to the IAU MDC or GMN.

## Credits

- **Global Meteor Network (GMN)**: Denis Vida et al. (`https://globalmeteornetwork.org/data/traj_summary_data/`, open `traj_summary_yearly_2018..2026.txt` orbital archives).
- **IAU Meteor Data Center (MDC)**: Regina Rudawska, Maria Hajduková, and Tadeusz J. Jopek (`https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php` and `streamfulldata2026.txt`).
- **Orbital Dissimilarity Criterion**: R. B. Southworth and G. S. Hawkins (1963), *Smithsonian Contributions to Astrophysics*, Vol. 7, pp. 261–285.
- **Credit**: `mizopl`

